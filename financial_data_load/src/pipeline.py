"""SimpleKGPipeline-based document enrichment for SEC 10-K filings."""

from __future__ import annotations

import asyncio
import logging
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

from neo4j import Driver

# Labels created internally by SimpleKGPipeline.
_PIPELINE_LABELS = ["__Entity__", "__KGBuilder__"]

# Labels for extracted entity nodes.
_EXTRACTED_LABELS = ["RiskFactor", "Product", "Executive", "FinancialMetric"]

_LOG_DIR = Path(__file__).resolve().parent.parent / "logs"

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------


def _setup_logging() -> Path:
    """Configure file logging for pipeline runs, return log file path."""
    _LOG_DIR.mkdir(exist_ok=True)
    log_file = _LOG_DIR / f"data_load_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    root = logging.getLogger()
    if not any(isinstance(h, logging.FileHandler) for h in root.handlers):
        root.addHandler(file_handler)
        root.setLevel(logging.DEBUG)
        logging.getLogger("neo4j").setLevel(logging.DEBUG)
        logging.getLogger("neo4j_graphrag").setLevel(logging.DEBUG)

    return log_file


# ---------------------------------------------------------------------------
# Processing result tracking
# ---------------------------------------------------------------------------


class PDFProcessingResult:
    """Track results for a single PDF processing run."""

    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.start_time: float = 0
        self.end_time: float = 0
        self.success: bool = False
        self.error: Optional[str] = None
        self.error_traceback: Optional[str] = None

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time if self.end_time else 0


# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------


def process_all_pdfs(
    driver: Driver,
    pdf_files: list[Path],
    company_meta: dict[str, dict],
) -> list[PDFProcessingResult]:
    """Run the SimpleKGPipeline over all PDF files.

    Creates one pipeline instance and reuses it for each PDF.
    Returns a list of processing results for summary reporting.
    """
    from .config import get_llm, get_embedder, AgentConfig
    from .loader import normalize_company_name
    from .schema import build_extraction_schema
    from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline

    log_file = _setup_logging()
    logger.info(f"Logging to: {log_file}")

    print("Initializing Azure AI Foundry LLM and Embedder...")
    llm = get_llm()
    embedder = get_embedder()
    agent_config = AgentConfig()
    print(f"  Model: {agent_config.model_name}")
    print(f"  Embedder: {agent_config.embedding_name}")
    print(f"  Endpoint: {agent_config.inference_endpoint}")

    schema = build_extraction_schema()

    print("Creating SimpleKGPipeline...")
    pipeline = SimpleKGPipeline(
        llm=llm,
        driver=driver,
        embedder=embedder,
        schema=schema,
        from_pdf=True,
        on_error="IGNORE",
        perform_entity_resolution=False,
    )

    results: list[PDFProcessingResult] = []

    async def _run_all():
        for i, pdf_path in enumerate(pdf_files, 1):
            result = PDFProcessingResult(pdf_path)
            result.start_time = time.time()
            meta = company_meta.get(pdf_path.name)

            print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
            print(f"  File size: {pdf_path.stat().st_size / 1024:.1f} KB")
            if meta:
                print(f"  Company: {meta.get('name', 'unknown')} ({meta.get('ticker', '')})")

            metadata = {"source": str(pdf_path)}
            if meta:
                normalized_meta = dict(meta)
                if "name" in normalized_meta:
                    normalized_meta["name"] = normalize_company_name(normalized_meta["name"])
                metadata.update(normalized_meta)

            try:
                await pipeline.run_async(
                    file_path=str(pdf_path),
                    document_metadata=metadata,
                )
                result.end_time = time.time()
                result.success = True
                print(f"  [OK] {pdf_path.name} ({result.duration:.1f}s)")
                logger.info(f"SUCCESS: {pdf_path.name} ({result.duration:.1f}s)")
            except Exception as e:
                result.end_time = time.time()
                result.success = False
                result.error = str(e)
                result.error_traceback = traceback.format_exc()
                print(f"  [FAIL] {pdf_path.name}: {e}")
                logger.error(f"FAILED: {pdf_path.name}: {e}")
                logger.debug(f"Traceback:\n{result.error_traceback}")

            results.append(result)

        # Close LLM async client
        await llm.async_client.close()

    asyncio.run(_run_all())

    # Print summary
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    print(f"\nProcessed {len(results)} PDFs: {len(successful)} successful, {len(failed)} failed")
    if failed:
        print("Failed PDFs:")
        for r in failed:
            print(f"  - {r.pdf_path.name}: {r.error}")

    _write_summary(results, log_file)
    return results


# ---------------------------------------------------------------------------
# Entity resolution
# ---------------------------------------------------------------------------


def run_entity_resolution(driver: Driver) -> None:
    """Run fuzzy entity resolution to merge near-duplicate entity names."""
    from neo4j_graphrag.experimental.components.resolver import FuzzyMatchResolver

    print("Running fuzzy entity resolution (threshold=0.80)...")
    resolver = FuzzyMatchResolver(
        driver=driver,
        similarity_threshold=0.80,
    )
    stats = asyncio.run(resolver.run())
    print(f"  [OK] Entity resolution complete: {stats}")


# ---------------------------------------------------------------------------
# Summary file
# ---------------------------------------------------------------------------


def _write_summary(results: list[PDFProcessingResult], log_file: Path) -> None:
    """Write processing summary to a separate file."""
    summary_file = log_file.parent / f"summary_{log_file.stem}.txt"
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    total_time = sum(r.duration for r in results)

    with open(summary_file, 'w') as f:
        f.write(f"{'=' * 70}\n")
        f.write("PDF PROCESSING SUMMARY\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'=' * 70}\n\n")
        f.write(f"Total: {len(results)} | Successful: {len(successful)} | Failed: {len(failed)}\n")
        f.write(f"Total time: {total_time:.1f}s\n\n")

        for r in successful:
            f.write(f"  [OK] {r.pdf_path.name} ({r.duration:.1f}s)\n")

        for r in failed:
            f.write(f"\n  [FAIL] {r.pdf_path.name} ({r.duration:.1f}s)\n")
            f.write(f"    Error: {r.error}\n")
            if r.error_traceback:
                for line in r.error_traceback.split('\n'):
                    f.write(f"      {line}\n")

    print(f"Summary written to: {summary_file}")


# ---------------------------------------------------------------------------
# Enrichment validation
# ---------------------------------------------------------------------------

def verify_searches(driver: Driver) -> None:
    """Run end-to-end search checks: retriever + LLM for each search type."""
    from .config import get_llm, get_embedder
    from neo4j_graphrag.generation import GraphRAG
    from neo4j_graphrag.retrievers import (
        VectorRetriever,
        VectorCypherRetriever,
        HybridRetriever,
    )

    print("\nInitializing LLM and Embedder...")
    llm = get_llm()
    embedder = get_embedder()

    # Retrieval query for vector + entity search: traverses from chunk to
    # company and its risk factors, returning enriched context.
    entity_retrieval_query = """
    MATCH (node)<-[:FROM_CHUNK]-(company:Company)-[:FACES_RISK]->(risk:RiskFactor)
    WITH node, company, collect(DISTINCT risk.name)[0..5] AS risks
    RETURN company.name AS company, risks, node.text AS context
    """

    checks = [
        (
            "Vector Search (semantic)",
            VectorRetriever(
                driver=driver,
                index_name="chunkEmbeddings",
                embedder=embedder,
                return_properties=["text"],
            ),
            "What risk factors do companies face?",
        ),
        (
            "Hybrid Search (semantic + keyword)",
            HybridRetriever(
                driver=driver,
                vector_index_name="chunkEmbeddings",
                fulltext_index_name="search_chunks",
                embedder=embedder,
                return_properties=["text"],
            ),
            "What products does Apple offer?",
        ),
        (
            "Vector + Entity Search (semantic + graph traversal)",
            VectorCypherRetriever(
                driver=driver,
                index_name="chunkEmbeddings",
                embedder=embedder,
                retrieval_query=entity_retrieval_query,
            ),
            "What are the top risk factors that companies face?",
        ),
    ]

    print("\nSearch Verification:")
    print("=" * 60)

    passed = 0
    failed = 0

    for name, retriever, query in checks:
        print(f"\n  {name}")
        print(f"  Query: \"{query}\"")
        try:
            rag = GraphRAG(llm=llm, retriever=retriever)
            response = rag.search(query, retriever_config={"top_k": 3}, return_context=True)
            n_results = len(response.retriever_result.items)
            answer = (response.answer or "").strip()

            if n_results == 0:
                print(f"  [FAIL] No results returned from retriever")
                failed += 1
            elif not answer:
                print(f"  [FAIL] Retriever returned {n_results} results but LLM produced no answer")
                failed += 1
            else:
                snippet = answer[:200] + "..." if len(answer) > 200 else answer
                print(f"  [PASS] {n_results} results, LLM answer: {snippet}")
                passed += 1
        except Exception as e:
            print(f"  [FAIL] {e}")
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Search verification: {passed} passed, {failed} failed")
    if failed:
        print("  Check that indexes exist (run: uv run python main.py load --clear)")
    print()


_SAMPLE_SIZE = 5

# Companies that must exist as exactly one node after entity resolution.
# (display_name, list of name variants that should have been merged into it)
_EXPECTED_UNIQUE_COMPANIES = [
    ("Apple", ["Apple", "Apple Inc", "Apple Inc."]),
    ("Microsoft", ["Microsoft", "Microsoft Corporation"]),
    ("NVIDIA", ["NVIDIA", "NVIDIA Corporation"]),
    ("Amazon", ["Amazon", "Amazon, Inc.", "Amazon.com", "Amazon.com, Inc."]),
    ("Alphabet", ["Alphabet", "Alphabet Inc."]),
    ("Google", ["Google", "Google Inc."]),
    ("Intel", ["Intel Corporation"]),
    ("PG&E", ["PG&E Corporation"]),
    ("McDonald's", ["McDonald's Corporation"]),
    ("AIG", ["American International Group, Inc."]),
    ("PayPal", ["PayPal Holdings, Inc."]),
]

# Entities that must NOT have been merged together.
_EXPECTED_SEPARATE = [
    ("PayPal Holdings, Inc.", "PayPal (Europe)"),
    ("PayPal Holdings, Inc.", "PayPal Pte. Ltd."),
    ("Microsoft Corporation", "Microsoft Mobile Oy"),
    ("Microsoft Corporation", "Microsoft's Bing"),
]


def _verify_entity_resolution(driver: Driver) -> None:
    """Verify entity resolution results against expected outcomes."""
    print(f"\n  Entity Resolution Checks:")

    passed = 0
    failed = 0

    # Check each expected company is exactly one node
    for display, variants in _EXPECTED_UNIQUE_COMPANIES:
        rows, _, _ = driver.execute_query(
            "MATCH (c:Company) WHERE c.name IN $names RETURN c.name AS name",
            names=variants,
        )
        names_found = [r["name"] for r in rows]
        if len(names_found) == 1:
            print(f"    [PASS] {display}: 1 node ({names_found[0]})")
            passed += 1
        elif len(names_found) == 0:
            print(f"    [FAIL] {display}: no node found (searched: {variants})")
            failed += 1
        else:
            print(f"    [FAIL] {display}: {len(names_found)} nodes — not fully merged: {names_found}")
            failed += 1

    # Check entities that should be separate
    for name_a, name_b in _EXPECTED_SEPARATE:
        rows, _, _ = driver.execute_query(
            "MATCH (a:Company {name: $a}), (b:Company {name: $b}) "
            "RETURN a.name AS a, b.name AS b",
            a=name_a, b=name_b,
        )
        if rows:
            print(f"    [PASS] Separate: {name_a} / {name_b}")
            passed += 1
        else:
            # Could be merged (bad) or one doesn't exist (check which)
            a_exists, _, _ = driver.execute_query(
                "MATCH (c:Company {name: $name}) RETURN c.name AS name",
                name=name_a,
            )
            b_exists, _, _ = driver.execute_query(
                "MATCH (c:Company {name: $name}) RETURN c.name AS name",
                name=name_b,
            )
            if not a_exists or not b_exists:
                missing = name_a if not a_exists else name_b
                print(f"    [SKIP] Separate: {name_a} / {name_b} — {missing!r} not in graph")
            else:
                print(f"    [FAIL] Separate: {name_a} and {name_b} were wrongly merged")
                failed += 1

    # Check no duplicate Company names exist at all
    dup_rows, _, _ = driver.execute_query(
        "MATCH (c:Company) WHERE c.name IS NOT NULL "
        "WITH c.name AS name, count(*) AS cnt "
        "WHERE cnt > 1 "
        "RETURN name, cnt ORDER BY cnt DESC LIMIT 10"
    )
    if dup_rows:
        print(f"    [FAIL] Duplicate Company names still exist:")
        for r in dup_rows:
            print(f"           {r['name']!r} x{r['cnt']}")
        failed += 1
    else:
        print(f"    [PASS] No duplicate Company names")
        passed += 1

    print(f"\n  Entity resolution: {passed} passed, {failed} failed")


def validate_enrichment(driver: Driver) -> None:
    """Run sample queries to verify embeddings, entities, and provenance."""

    print(f"\nValidation (sample size {_SAMPLE_SIZE}):")

    # 1. Chunks with embeddings linked to documents
    rows, _, _ = driver.execute_query(f"""
        MATCH (c:Chunk)-[:FROM_DOCUMENT]->(d:Document)
        WHERE c.embedding IS NOT NULL
        RETURN elementId(c) AS chunk_id, size(c.embedding) AS dims
        LIMIT {_SAMPLE_SIZE}
    """)
    print(f"\n  Chunks with embeddings ({len(rows)} samples):")
    for r in rows:
        print(f"    {r['chunk_id'][:20]}...  dims={r['dims']}")
    if not rows:
        print("    [WARN] No chunks with embeddings found!")

    # 2. Extracted entities by type
    for label in _EXTRACTED_LABELS:
        rows, _, _ = driver.execute_query(f"""
            MATCH (n:{label})
            RETURN n.name AS name
            LIMIT {_SAMPLE_SIZE}
        """)
        if rows:
            names = ", ".join(r["name"] for r in rows)
            print(f"\n  {label} ({len(rows)} samples): {names}")

    # 3. Schema relationships
    rows, _, _ = driver.execute_query(f"""
        MATCH (c:Company)-[r]->(target)
        WHERE type(r) IN ['FACES_RISK', 'OFFERS', 'HAS_EXECUTIVE', 'REPORTS',
                          'COMPETES_WITH', 'PARTNERS_WITH']
        WITH type(r) AS rel, count(r) AS cnt
        RETURN rel, cnt ORDER BY cnt DESC
        LIMIT {_SAMPLE_SIZE}
    """)
    if rows:
        print(f"\n  Schema relationships:")
        for r in rows:
            print(f"    {r['rel']}: {r['cnt']}")
    else:
        print(f"\n  [WARN] No schema relationships found!")

    # 4. Provenance chain
    rows, _, _ = driver.execute_query("""
        MATCH (e:__Entity__)-[:FROM_CHUNK]->(c:Chunk)-[:FROM_DOCUMENT]->(d:Document)
        RETURN count(DISTINCT e) AS entities,
               count(DISTINCT c) AS chunks,
               count(DISTINCT d) AS docs
    """)
    if rows:
        r = rows[0]
        print(f"\n  Provenance: {r['entities']} entities -> {r['chunks']} chunks -> {r['docs']} documents")

    # 5. Entity resolution verification
    _verify_entity_resolution(driver)
