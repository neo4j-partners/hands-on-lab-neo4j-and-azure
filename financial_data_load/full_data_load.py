#!/usr/bin/env python3
"""
Full Data Loading with SimpleKGPipeline and Azure AI Foundry

This solution loads all SEC 10-K filings from the form10k-sample directory,
extracts entities and relationships using GPT-4o via Azure AI Foundry, generates
embeddings with text-embedding-ada-002, and stores everything in Neo4j.

Pipeline Flow:
1. Load CSV metadata (company names, tickers, CIK numbers)
2. Create Company nodes from CSV with normalized names
3. Run SimpleKGPipeline on each PDF to extract entities
4. Library uses MERGE (not CREATE) so extracted entities merge with existing nodes
5. Create AssetManager nodes and OWNS relationships

The neo4j-graphrag-python library now uses MERGE by default for node creation,
which prevents duplicate entities when the same company is mentioned in multiple
chunks of a document.

Run with: cd financial_data_load && uv run python full_data_load.py
Options:
  --limit N        Process only N PDFs (for testing)
  --skip-metadata  Skip loading CSV metadata
  --clear          Clear database before loading

Prerequisites:
- Azure AI Foundry deployed (run: azd up && uv run python setup_env.py)
- Azure CLI logged in (az login --use-device-code)
- Neo4j connection configured in .env
- PDFs in financial-data/form10k-sample (relative to this script)
"""

import asyncio
import csv
import logging
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

import neo4j
from neo4j import GraphDatabase

from azure.identity import AzureCliCredential, DefaultAzureCredential
from dotenv import load_dotenv
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.experimental.components.schema import GraphSchema
from neo4j_graphrag.indexes import create_vector_index, create_fulltext_index
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings import OpenAIEmbeddings

# Load .env from this directory
_root_env = Path(__file__).parent / ".env"
load_dotenv(_root_env)

# Configure logging with file output
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"data_load_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Create formatters and handlers
file_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_formatter = logging.Formatter('%(levelname)s: %(message)s')

# File handler - detailed logging
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

# Console handler - info and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)

# Configure root logger
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
logger = logging.getLogger(__name__)

# Also capture neo4j and neo4j_graphrag logs
logging.getLogger("neo4j").setLevel(logging.DEBUG)
logging.getLogger("neo4j_graphrag").setLevel(logging.DEBUG)

logger.info(f"Logging to: {LOG_FILE}")

# Data directory - relative to this script
DATA_DIR = Path(__file__).parent / "financial-data"
PDF_DIR = DATA_DIR / "form10k-sample"
COMPANY_CSV = DATA_DIR / "Company_Filings.csv"
ASSET_MANAGER_CSV = DATA_DIR / "Asset_Manager_Holdings.csv"


# ============================================================================
# Configuration Classes
# ============================================================================

class Neo4jConfig(BaseSettings):
    """Neo4j configuration loaded from environment variables."""
    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    uri: str = Field(validation_alias="NEO4J_URI")
    username: str = Field(validation_alias="NEO4J_USERNAME")
    password: str = Field(validation_alias="NEO4J_PASSWORD")


class AgentConfig(BaseSettings):
    """Agent configuration loaded from environment variables."""
    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    project_endpoint: str = Field(validation_alias="AZURE_AI_PROJECT_ENDPOINT")
    model_name: str = Field(default="gpt-4o", validation_alias="AZURE_AI_MODEL_NAME")
    embedding_name: str = Field(
        default="text-embedding-ada-002",
        validation_alias="AZURE_AI_EMBEDDING_NAME",
    )

    @computed_field
    @property
    def inference_endpoint(self) -> str:
        """Get the model inference endpoint from project endpoint."""
        if "/api/projects/" in self.project_endpoint:
            base = self.project_endpoint.split("/api/projects/")[0]
            return f"{base}/models"
        return self.project_endpoint


# ============================================================================
# Company Name Normalization
# ============================================================================

# Canonical company names mapped from CSV uppercase variants
COMPANY_NAME_MAPPINGS = {
    "AMAZON": "Amazon.com, Inc.",
    "NVIDIA CORPORATION": "NVIDIA Corporation",
    "APPLE INC": "Apple Inc.",
    "PAYPAL": "PayPal Holdings, Inc.",
    "INTEL CORP": "Intel Corporation",
    "AMERICAN INTL GROUP": "American International Group, Inc.",
    "PG&E CORP": "PG&E Corporation",
    "MCDONALDS CORP": "McDonald's Corporation",
    "MICROSOFT CORP": "Microsoft Corporation",
}


def normalize_company_name(name: str) -> str:
    """Normalize a company name to its canonical form."""
    if name in COMPANY_NAME_MAPPINGS:
        return COMPANY_NAME_MAPPINGS[name]
    upper_name = name.upper()
    if upper_name in COMPANY_NAME_MAPPINGS:
        return COMPANY_NAME_MAPPINGS[upper_name]
    return name


# ============================================================================
# Azure Authentication
# ============================================================================

def _get_azure_token() -> str:
    """Get Azure token for cognitive services."""
    scope = "https://cognitiveservices.azure.com/.default"

    # Try Azure CLI first
    try:
        credential = AzureCliCredential()
        token = credential.get_token(scope)
        return token.token
    except Exception:
        pass

    # Fall back to DefaultAzureCredential
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token(scope)
        return token.token
    except Exception as e:
        raise RuntimeError(
            "Azure authentication failed. Please run:\n"
            "  1. az login --use-device-code\n"
            f"Original error: {e}"
        ) from e


def get_llm() -> OpenAILLM:
    """Get LLM using Azure AI Foundry's OpenAI-compatible endpoint."""
    config = AgentConfig()
    token = _get_azure_token()

    return OpenAILLM(
        model_name=config.model_name,
        base_url=config.inference_endpoint,
        api_key=token,
    )


def get_embedder() -> OpenAIEmbeddings:
    """Get embedder using Azure AI Foundry's OpenAI-compatible endpoint."""
    config = AgentConfig()
    token = _get_azure_token()

    return OpenAIEmbeddings(
        model=config.embedding_name,
        base_url=config.inference_endpoint,
        api_key=token,
    )


# ============================================================================
# Schema for SEC 10-K Financial Documents
# ============================================================================

SEC_SCHEMA = GraphSchema.model_validate({
    "node_types": [
        {
            "label": "Company",
            "description": "A publicly traded company",
            "properties": [
                {"name": "name", "type": "STRING", "description": "Company name"},
                {"name": "ticker", "type": "STRING", "description": "Stock ticker symbol"},
            ],
        },
        {
            "label": "RiskFactor",
            "description": "A risk factor disclosed in the 10-K filing",
            "properties": [
                {"name": "name", "type": "STRING", "description": "Short name of the risk"},
                {"name": "description", "type": "STRING", "description": "Detailed description"},
            ],
        },
        {
            "label": "Product",
            "description": "A product or service offered by the company",
            "properties": [
                {"name": "name", "type": "STRING", "description": "Product name"},
            ],
        },
        {
            "label": "Executive",
            "description": "A company executive or board member",
            "properties": [
                {"name": "name", "type": "STRING", "description": "Person's name"},
                {"name": "title", "type": "STRING", "description": "Job title"},
            ],
        },
        {
            "label": "FinancialMetric",
            "description": "A financial metric or KPI",
            "properties": [
                {"name": "name", "type": "STRING", "description": "Metric name"},
                {"name": "value", "type": "STRING", "description": "Metric value"},
                {"name": "period", "type": "STRING", "description": "Reporting period"},
            ],
        },
    ],
    "relationship_types": [
        {"label": "FACES_RISK", "description": "Company faces this risk factor"},
        {"label": "OFFERS", "description": "Company offers this product/service"},
        {"label": "HAS_EXECUTIVE", "description": "Company has this executive"},
        {"label": "REPORTS", "description": "Company reports this financial metric"},
        {"label": "COMPETES_WITH", "description": "Company competes with another company"},
        {"label": "PARTNERS_WITH", "description": "Company partners with another company"},
    ],
    "patterns": [
        ("Company", "FACES_RISK", "RiskFactor"),
        ("Company", "OFFERS", "Product"),
        ("Company", "HAS_EXECUTIVE", "Executive"),
        ("Company", "REPORTS", "FinancialMetric"),
        ("Company", "COMPETES_WITH", "Company"),
        ("Company", "PARTNERS_WITH", "Company"),
    ],
})


# ============================================================================
# Data Loading Functions
# ============================================================================

def load_company_metadata(csv_path: Path) -> dict[str, dict]:
    """Load company metadata from CSV, keyed by PDF filename."""
    companies = {}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            path = row.get("path_Mac_ix", "")
            filename = Path(path).name if path else None
            if filename:
                companies[filename] = {
                    "name": row.get("name", ""),
                    "ticker": row.get("ticker", ""),
                    "cik": row.get("cik", ""),
                    "cusip": row.get("cusip", ""),
                }
    return companies


def load_asset_managers(csv_path: Path) -> list[dict]:
    """Load asset manager holdings from CSV."""
    holdings = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            holdings.append({
                "manager_name": row.get("managerName", ""),
                "company_name": row.get("companyName", ""),
                "shares": int(row.get("shares", 0)),
            })
    return holdings


async def clear_database(driver: neo4j.Driver) -> None:
    """Clear all nodes and relationships from the database."""
    logger.info("Clearing database...")
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    logger.info("Database cleared")


async def create_company_nodes(driver: neo4j.Driver, companies: dict[str, dict]) -> None:
    """Create Company nodes from CSV metadata before LLM extraction."""
    logger.info(f"Creating {len(companies)} Company nodes from metadata...")

    with driver.session() as session:
        session.run("""
            CREATE CONSTRAINT company_name IF NOT EXISTS
            FOR (c:Company) REQUIRE c.name IS UNIQUE
        """)

        for filename, meta in companies.items():
            normalized_name = normalize_company_name(meta["name"])
            session.run("""
                MERGE (c:Company {name: $name})
                SET c.ticker = $ticker,
                    c.cik = $cik,
                    c.cusip = $cusip
            """, name=normalized_name, ticker=meta["ticker"],
                cik=meta["cik"], cusip=meta["cusip"])

    logger.info("Company nodes created")


async def create_asset_manager_relationships(
    driver: neo4j.Driver,
    holdings: list[dict]
) -> None:
    """Create AssetManager nodes and OWNS relationships."""
    logger.info("Creating asset manager relationships...")

    with driver.session() as session:
        session.run("""
            CREATE CONSTRAINT asset_manager_name IF NOT EXISTS
            FOR (a:AssetManager) REQUIRE a.managerName IS UNIQUE
        """)

        for holding in holdings:
            normalized_company = normalize_company_name(holding["company_name"])
            session.run("""
                MERGE (a:AssetManager {managerName: $manager_name})
                WITH a
                MATCH (c:Company {name: $company_name})
                MERGE (a)-[r:OWNS]->(c)
                SET r.shares = $shares
            """, manager_name=holding["manager_name"],
                company_name=normalized_company,
                shares=holding["shares"])

    logger.info("Asset manager relationships created")


async def create_search_indexes(driver: neo4j.Driver) -> None:
    """Create vector and fulltext indexes for search.

    Creates:
    - chunkEmbeddings: Vector index on Chunk.embedding for semantic search
    - search_entities: Fulltext index on entity names for keyword search
    """
    logger.info("Creating search indexes...")

    # Vector index for semantic search on chunk embeddings
    # Uses 1536 dimensions for text-embedding-ada-002
    try:
        create_vector_index(
            driver,
            name="chunkEmbeddings",
            label="Chunk",
            embedding_property="embedding",
            dimensions=1536,
            similarity_fn="cosine",
        )
        logger.info("  Created vector index: chunkEmbeddings")
    except Exception as e:
        logger.warning(f"  Vector index creation: {e}")

    # Fulltext index for keyword search on entity names
    # Indexes Company, Product, RiskFactor, Executive, FinancialMetric names
    with driver.session() as session:
        session.run("""
            CREATE FULLTEXT INDEX search_entities IF NOT EXISTS
            FOR (n:Company|Product|RiskFactor|Executive|FinancialMetric)
            ON EACH [n.name]
        """)
        logger.info("  Created fulltext index: search_entities")

    # Fulltext index for chunk text (used by hybrid search)
    with driver.session() as session:
        session.run("""
            CREATE FULLTEXT INDEX chunkText IF NOT EXISTS
            FOR (n:Chunk)
            ON EACH [n.text]
        """)
        logger.info("  Created fulltext index: chunkText")

    logger.info("Search indexes created")


class PDFProcessingResult:
    """Track results for a single PDF processing run."""
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.start_time: float = 0
        self.end_time: float = 0
        self.success: bool = False
        self.error: Optional[str] = None
        self.error_traceback: Optional[str] = None
        self.result: Optional[str] = None

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time if self.end_time else 0


async def process_pdf(
    pipeline: SimpleKGPipeline,
    pdf_path: Path,
    company_meta: Optional[dict] = None,
) -> PDFProcessingResult:
    """Process a single PDF through the KG pipeline."""
    result = PDFProcessingResult(pdf_path)
    result.start_time = time.time()

    logger.info(f"=" * 60)
    logger.info(f"PROCESSING PDF: {pdf_path.name}")
    logger.info(f"  Full path: {pdf_path}")
    logger.info(f"  File size: {pdf_path.stat().st_size / 1024:.1f} KB")
    if company_meta:
        logger.info(f"  Company: {company_meta.get('name', 'unknown')}")
        logger.info(f"  Ticker: {company_meta.get('ticker', 'unknown')}")

    metadata = {"source": str(pdf_path)}
    if company_meta:
        metadata.update(company_meta)

    try:
        logger.debug(f"  Calling pipeline.run_async()...")
        pipeline_result = await pipeline.run_async(
            file_path=str(pdf_path),
            document_metadata=metadata,
        )
        result.end_time = time.time()
        result.success = True
        result.result = str(pipeline_result)

        logger.info(f"  SUCCESS: {pdf_path.name}")
        logger.info(f"  Duration: {result.duration:.1f}s")
        logger.info(f"  Result: {pipeline_result}")

    except Exception as e:
        result.end_time = time.time()
        result.success = False
        result.error = str(e)
        result.error_traceback = traceback.format_exc()

        logger.error(f"  FAILED: {pdf_path.name}")
        logger.error(f"  Duration: {result.duration:.1f}s")
        logger.error(f"  Error type: {type(e).__name__}")
        logger.error(f"  Error message: {e}")
        logger.debug(f"  Full traceback:\n{result.error_traceback}")

    return result


async def print_graph_summary(driver: neo4j.Driver) -> None:
    """Print a detailed summary of the knowledge graph."""
    print("\n" + "=" * 60)
    print("KNOWLEDGE GRAPH SUMMARY")
    print("=" * 60)

    with driver.session() as session:
        # Node counts by label
        result = session.run("""
            MATCH (n)
            WITH labels(n) AS lbls, count(n) AS cnt
            UNWIND lbls AS label
            RETURN label, sum(cnt) AS count
            ORDER BY count DESC
        """)
        print("\nNODE COUNTS BY LABEL:")
        total_nodes = 0
        for record in result:
            print(f"   {record['label']}: {record['count']}")
            total_nodes += record['count']

        # Relationship counts by type
        result = session.run("""
            MATCH ()-[r]->()
            RETURN type(r) AS type, count(r) AS count
            ORDER BY count DESC
        """)
        print("\nRELATIONSHIP COUNTS BY TYPE:")
        total_rels = 0
        for record in result:
            print(f"   {record['type']}: {record['count']}")
            total_rels += record['count']

        # Lexical graph summary
        result = session.run("""
            MATCH (d:Document)
            OPTIONAL MATCH (d)-[:FROM_DOCUMENT]-(c:Chunk)
            WITH d, count(c) AS chunk_count
            RETURN count(d) AS documents, sum(chunk_count) AS total_chunks
        """)
        record = result.single()
        print("\nLEXICAL GRAPH:")
        print(f"   Documents: {record['documents']}")
        print(f"   Chunks: {record['total_chunks']}")

        # Entity extraction summary
        result = session.run("""
            MATCH (e:__Entity__)
            WITH labels(e) AS lbls
            UNWIND lbls AS label
            WITH label
            WHERE label <> '__Entity__' AND label <> '__KGBuilder__'
            RETURN label, count(*) AS count
            ORDER BY count DESC
        """)
        print("\nEXTRACTED ENTITIES BY TYPE:")
        for record in result:
            print(f"   {record['label']}: {record['count']}")

        # Provenance tracking
        result = session.run("""
            MATCH (e:__Entity__)-[r:FROM_CHUNK]->(c:Chunk)
            RETURN count(DISTINCT e) AS entities_with_provenance,
                   count(r) AS provenance_links
        """)
        record = result.single()
        print("\nPROVENANCE TRACKING:")
        print(f"   Entities with FROM_CHUNK links: {record['entities_with_provenance']}")
        print(f"   Total provenance links: {record['provenance_links']}")

        # Embedding summary
        result = session.run("""
            MATCH (c:Chunk)
            WHERE c.embedding IS NOT NULL
            RETURN count(c) AS chunks_with_embeddings,
                   size(c.embedding) AS embedding_dim
            LIMIT 1
        """)
        record = result.single()
        print("\nEMBEDDINGS:")
        if record and record['chunks_with_embeddings'] > 0:
            print(f"   Chunks with embeddings: {record['chunks_with_embeddings']}")
            print(f"   Embedding dimensions: {record['embedding_dim']}")
        else:
            print("   No chunk embeddings found")

        # Schema relationships
        result = session.run("""
            MATCH (c:Company)-[r]->(target)
            WHERE type(r) IN ['FACES_RISK', 'OFFERS', 'HAS_EXECUTIVE', 'REPORTS', 'COMPETES_WITH', 'PARTNERS_WITH']
            WITH type(r) AS relationship,
                 [l IN labels(target) WHERE NOT l IN ['__KGBuilder__', '__Entity__']][0] AS target_type,
                 r
            RETURN relationship, target_type, count(r) AS count
            ORDER BY count DESC
        """)
        print("\nSCHEMA RELATIONSHIPS (Company -> ...):")
        schema_rels = list(result)
        if schema_rels:
            for record in schema_rels:
                print(f"   Company-[{record['relationship']}]->{record['target_type']}: {record['count']}")
        else:
            print("   No schema relationships found")

        # Asset manager holdings
        result = session.run("""
            MATCH (a:AssetManager)-[r:OWNS]->(c:Company)
            RETURN count(DISTINCT a) AS managers, count(r) AS holdings
        """)
        record = result.single()
        print("\nASSET MANAGER HOLDINGS:")
        print(f"   Asset managers: {record['managers']}")
        print(f"   Total holdings: {record['holdings']}")

        # Summary totals
        print("\n" + "-" * 60)
        print(f"TOTALS: {total_nodes} nodes, {total_rels} relationships")
        print("=" * 60 + "\n")


# ============================================================================
# Main Pipeline
# ============================================================================

def write_processing_summary(results: list[PDFProcessingResult], log_file: Path) -> None:
    """Write a detailed processing summary to a separate file."""
    summary_file = log_file.parent / f"summary_{log_file.stem}.txt"

    with open(summary_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("PDF PROCESSING SUMMARY\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        # Overall stats
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]
        total_time = sum(r.duration for r in results)

        f.write(f"Total PDFs: {len(results)}\n")
        f.write(f"Successful: {len(successful)}\n")
        f.write(f"Failed: {len(failed)}\n")
        f.write(f"Total processing time: {total_time:.1f}s\n\n")

        # Successful PDFs
        if successful:
            f.write("-" * 70 + "\n")
            f.write("SUCCESSFUL PDFS\n")
            f.write("-" * 70 + "\n")
            for r in successful:
                f.write(f"\n  {r.pdf_path.name}\n")
                f.write(f"    Duration: {r.duration:.1f}s\n")
                f.write(f"    Result: {r.result}\n")

        # Failed PDFs
        if failed:
            f.write("\n" + "-" * 70 + "\n")
            f.write("FAILED PDFS\n")
            f.write("-" * 70 + "\n")
            for r in failed:
                f.write(f"\n  {r.pdf_path.name}\n")
                f.write(f"    Duration: {r.duration:.1f}s\n")
                f.write(f"    Error: {r.error}\n")
                if r.error_traceback:
                    f.write(f"    Traceback:\n")
                    for line in r.error_traceback.split('\n'):
                        f.write(f"      {line}\n")

        f.write("\n" + "=" * 70 + "\n")

    logger.info(f"Processing summary written to: {summary_file}")


async def main(
    pdf_limit: Optional[int] = None,
    skip_metadata: bool = False,
    clear_db: bool = False,
) -> None:
    """
    Run the full data loading pipeline.

    Args:
        pdf_limit: Limit number of PDFs to process (for testing). None = all.
        skip_metadata: Skip loading CSV metadata (Company, AssetManager nodes).
        clear_db: Clear all nodes/relationships before loading.
    """
    overall_start = time.time()
    processing_results: list[PDFProcessingResult] = []

    logger.info("=" * 70)
    logger.info("STARTING FULL DATA LOAD")
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)

    # Check data directory exists
    if not DATA_DIR.exists():
        logger.error(f"Data directory not found: {DATA_DIR}")
        logger.error("Please update DATA_DIR in this file or symlink the data.")
        return

    if not PDF_DIR.exists():
        logger.error(f"PDF directory not found: {PDF_DIR}")
        return

    # Get list of PDFs
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        logger.error(f"No PDF files found in: {PDF_DIR}")
        return

    if pdf_limit:
        pdf_files = pdf_files[:pdf_limit]
        logger.info(f"PDF limit set: processing {pdf_limit} of {len(list(PDF_DIR.glob('*.pdf')))} PDFs")

    logger.info(f"Found {len(pdf_files)} PDF files to process:")
    for i, pdf in enumerate(pdf_files, 1):
        logger.info(f"  {i}. {pdf.name} ({pdf.stat().st_size / 1024:.1f} KB)")

    # Load metadata
    company_meta = {}
    if COMPANY_CSV.exists():
        company_meta = load_company_metadata(COMPANY_CSV)
        logger.info(f"Loaded metadata for {len(company_meta)} companies")
        for filename, meta in company_meta.items():
            logger.debug(f"  {filename} -> {meta.get('name')} ({meta.get('ticker')})")
    else:
        logger.warning(f"Company CSV not found: {COMPANY_CSV}")

    asset_holdings = []
    if ASSET_MANAGER_CSV.exists():
        asset_holdings = load_asset_managers(ASSET_MANAGER_CSV)
        logger.info(f"Loaded {len(asset_holdings)} asset manager holdings")
    else:
        logger.warning(f"Asset manager CSV not found: {ASSET_MANAGER_CSV}")

    # Initialize Neo4j
    config = Neo4jConfig()
    logger.info(f"Connecting to Neo4j: {config.uri}")

    driver = GraphDatabase.driver(
        config.uri,
        auth=(config.username, config.password),
    )

    try:
        driver.verify_connectivity()
        logger.info("Neo4j connection verified successfully")

        # Clear database if requested
        if clear_db:
            await clear_database(driver)

        # Create metadata nodes BEFORE extraction
        if not skip_metadata and company_meta:
            await create_company_nodes(driver, company_meta)

        # Initialize Azure AI LLM and Embedder
        logger.info("Initializing Azure AI Foundry LLM and Embedder...")
        try:
            llm = get_llm()
            embedder = get_embedder()

            agent_config = AgentConfig()
            logger.info(f"  Model: {agent_config.model_name}")
            logger.info(f"  Embedder: {agent_config.embedding_name}")
            logger.info(f"  Endpoint: {agent_config.inference_endpoint}")
        except Exception as e:
            logger.error(f"Failed to initialize Azure AI: {e}")
            logger.error(traceback.format_exc())
            return

        # Create pipeline
        logger.info("Creating SimpleKGPipeline...")
        try:
            pipeline = SimpleKGPipeline(
                llm=llm,
                driver=driver,
                embedder=embedder,
                schema=SEC_SCHEMA,
                from_pdf=True,
                on_error="IGNORE",  # Continue on extraction errors
                perform_entity_resolution=True,
            )
            logger.info("Pipeline created successfully")
        except Exception as e:
            logger.error(f"Failed to create pipeline: {e}")
            logger.error(traceback.format_exc())
            return

        # Process each PDF
        logger.info("\n" + "=" * 70)
        logger.info("BEGINNING PDF PROCESSING")
        logger.info("=" * 70)

        for i, pdf_path in enumerate(pdf_files, 1):
            logger.info(f"\n[{i}/{len(pdf_files)}] Starting {pdf_path.name}")
            meta = company_meta.get(pdf_path.name)
            result = await process_pdf(pipeline, pdf_path, meta)
            processing_results.append(result)

            # Log running totals
            successful = sum(1 for r in processing_results if r.success)
            failed = sum(1 for r in processing_results if not r.success)
            logger.info(f"  Running totals: {successful} successful, {failed} failed")

        # Write processing summary
        logger.info("\n" + "=" * 70)
        logger.info("PDF PROCESSING COMPLETE")
        logger.info("=" * 70)

        successful = [r for r in processing_results if r.success]
        failed = [r for r in processing_results if not r.success]

        logger.info(f"Processed {len(processing_results)} PDFs")
        logger.info(f"  Successful: {len(successful)}")
        logger.info(f"  Failed: {len(failed)}")

        if failed:
            logger.warning("Failed PDFs:")
            for r in failed:
                logger.warning(f"  - {r.pdf_path.name}: {r.error}")

        # Write detailed summary file
        write_processing_summary(processing_results, LOG_FILE)

        # Create asset manager relationships (after Companies exist)
        if not skip_metadata and asset_holdings:
            await create_asset_manager_relationships(driver, asset_holdings)

        # Create search indexes (after all data is loaded)
        await create_search_indexes(driver)

        # Calculate overall timing
        overall_duration = time.time() - overall_start
        logger.info("\n" + "=" * 70)
        logger.info("DATA LOADING COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Total duration: {overall_duration:.1f}s ({overall_duration/60:.1f} minutes)")
        logger.info(f"Log file: {LOG_FILE}")

        # Show detailed summary
        await print_graph_summary(driver)

    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        logger.error(traceback.format_exc())
        raise

    finally:
        driver.close()
        logger.info("Connection closed")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load SEC 10-K data into Neo4j using Azure AI Foundry")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of PDFs to process (for testing)",
    )
    parser.add_argument(
        "--skip-metadata",
        action="store_true",
        help="Skip loading CSV metadata",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear database before loading",
    )
    args = parser.parse_args()

    asyncio.run(main(pdf_limit=args.limit, skip_metadata=args.skip_metadata, clear_db=args.clear))
