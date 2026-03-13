# Financial Data Load Workshop

Build AI agents using Microsoft Agent Framework with Azure AI Foundry, integrated with Neo4j graph database capabilities via the neo4j-graphrag-python library.

## Prerequisites

- Azure subscription with access to Azure AI Foundry
- Neo4j Aura instance (or local Neo4j database)
- Python 3.12.x
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [uv](https://docs.astral.sh/uv/) package manager

## Quick Start

All commands below assume you are in the `financial_data_load/` directory:

```bash
cd financial_data_load
```

### 1. Deploy Azure AI Infrastructure

```bash
# Login to Azure
az login --use-device-code
azd auth login --use-device-code

# Deploy infrastructure (AI Services + model deployments)
azd up

# Sync Azure outputs to .env
uv run python setup_env.py
```

### 2. Configure Neo4j

Edit the `.env` file and update the Neo4j credentials:

```bash
NEO4J_URI=neo4j+s://xxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
```

### 3. Install Dependencies

From the **project root**:

```bash
uv sync --prerelease=allow
```

### 4. Test Connections

```bash
uv run python main.py test
```

### 5. Load PDFs and Create Backup (one-time)

This step processes PDFs through the LLM (~25 min for all 8) and creates a backup. You only need to do this once. The `load` command handles both CSV metadata and PDF processing.

```bash
# Test with 1 PDF first (optional)
uv run python main.py load --limit 1 --clear

# Load all 8 PDFs (~25 min)
uv run python main.py load --clear

# Back up the database — saves all nodes, relationships, and embeddings to JSON
uv run python main.py backup
```

The backup file is saved to `backups/` and contains the full database state after PDF processing. This is your checkpoint — you can always restore to this point without re-processing PDFs.

### 6. Run Entity Resolution Pipeline

Restore the database from backup, then run entity resolution and finalization. This is fast and can be repeated with different settings.

```bash
# Restore database to post-PDF-processing state
uv run python main.py restore

# Export entity snapshot for resolution
uv run python main.py snapshot

# Run LLM entity resolution
uv run python main.py resolve

# Review the merge plan (optional)
cat logs/merge_plan_*.json

# Apply merges to Neo4j
uv run python main.py apply-merges

# Create constraints, indexes, asset managers
uv run python main.py finalize

# Verify everything
uv run python main.py verify
```

**Testing different configurations:**

To iterate on entity resolution with different settings, you don't need to restore every time. The snapshot file captures entity state, so you can re-run just the resolution steps:

```bash
# Change ER_ settings in .env, then:
uv run python main.py resolve              # Re-run with new settings
uv run python main.py apply-merges         # Apply new merge plan

# Or just re-run finalization
uv run python main.py finalize
```

To start completely fresh (reset the database to the post-PDF state and re-run everything):

```bash
uv run python main.py restore              # Reset to backup
uv run python main.py snapshot             # Fresh snapshot
uv run python main.py resolve              # Resolve
uv run python main.py apply-merges         # Apply
uv run python main.py finalize             # Finalize
```

### Entity Resolution Configuration

Entity resolution parameters are configured via `.env` with the `ER_` prefix:

```bash
ER_PRE_FILTER_STRATEGY=fuzzy        # Pre-filter: "fuzzy" or "prefix"
ER_PRE_FILTER_THRESHOLD=0.6         # Similarity threshold for candidate pairs
ER_BATCH_SIZE=10                     # Pairs per LLM batch
ER_CONFIDENCE_MODE=binary            # "binary" or "confidence"
ER_CONFIDENCE_THRESHOLD=0.8          # Auto-merge threshold (confidence mode only)
ER_MAX_GROUP_SIZE=10                 # Max entities in a merge group
ER_MODEL_NAME=gpt-4o                # LLM model for entity resolution
```

### All Commands

| Command | Description |
|---------|-------------|
| `main.py test` | Test Neo4j and Azure AI connections |
| `main.py load [--limit N] [--files PDF ...] [--clear]` | Load CSV metadata + process PDFs |
| `main.py backup` | Back up full database to `backups/` |
| `main.py restore [--backup PATH]` | Restore database from backup |
| `main.py snapshot` | Export entity snapshot to `snapshots/` |
| `main.py resolve [--snapshot PATH]` | LLM entity resolution (outputs merge plan to `logs/`) |
| `main.py apply-merges [--plan PATH]` | Apply merge plan to Neo4j |
| `main.py finalize` | Constraints, indexes, asset managers, verify |
| `main.py verify` | Counts + enrichment checks + end-to-end search validation |
| `main.py clean` | Clear all data |
| `main.py samples [--limit N]` | Run sample queries showcasing the graph |

### 7. Run Workshop Solutions

```bash
# Interactive menu
uv run python main.py solutions

# Run specific solution
uv run python main.py solutions 4

# Run all (from option 4 onwards)
uv run python main.py solutions A
```

## Workshop Solutions

### Data Pipeline (01_xx)

These solutions build the knowledge graph — **WARNING: they will delete existing data**:

| # | Solution | Description |
|---|----------|-------------|
| 1 | `01_01_data_loading.py` | Load financial documents into Neo4j |
| 2 | `01_02_embeddings.py` | Generate and store vector embeddings |
| 3 | `01_03_entity_extraction.py` | Extract entities and relationships |
| 4 | `01_04_full_dataset_queries.py` | Explore the loaded data |

### Retrievers (02_xx)

GraphRAG patterns using neo4j-graphrag with Azure AI:

| # | Solution | Description |
|---|----------|-------------|
| 5 | `02_01_vector_retriever.py` | Basic vector search |
| 6 | `02_02_vector_cypher_retriever.py` | Vector search + custom Cypher |
| 7 | `02_03_text2cypher_retriever.py` | Natural language to Cypher |

### Agents (03_xx / 05_xx)

Microsoft Agent Framework with Azure AI Foundry:

| # | Solution | Description |
|---|----------|-------------|
| 8 | `05_01_simple_agent.py` | Basic agent with schema tool |
| 9 | `05_02_context_provider.py` | Context provider intro (user info memory) |
| 10 | `03_02_vector_graph_agent.py` | Agent with vector search + graph traversal |
| 11 | `03_03_text2cypher_agent.py` | Multi-tool agent with Text2Cypher |

### Search (05_xx)

Advanced search patterns:

| # | Solution | Description |
|---|----------|-------------|
| 12 | `05_01_fulltext_search.py` | Full-text search capabilities |
| 13 | `05_02_hybrid_search.py` | Hybrid vector + keyword search |

### Context Providers (06_xx)

Neo4j context providers using agent-framework-neo4j:

| # | Solution | Description |
|---|----------|-------------|
| 14 | `06_01_fulltext_context_provider.py` | Fulltext search context provider |
| 15 | `06_02_vector_context_provider.py` | Vector (semantic) search context provider |
| 16 | `06_03_graph_enriched_provider.py` | Vector search + graph traversal context provider |

### Agent Memory (07_xx)

Persistent agent memory using neo4j-agent-memory:

| # | Solution | Description |
|---|----------|-------------|
| 17 | `07_01_memory_context_provider.py` | Memory as a context provider |
| 18 | `07_02_entity_extraction.py` | Entity extraction pipeline |
| 19 | `07_03_memory_tools_agent.py` | Agent with explicit memory tools |
| 20 | `07_04_reasoning_memory.py` | Reasoning memory traces and tool stats |

## Architecture

- **Azure AI Foundry** — Model hosting (gpt-4o, text-embedding-3-small)
- **Microsoft Agent Framework** — Agent creation and tool management
- **agent-framework-neo4j** — Neo4j context providers for automatic context injection
- **neo4j-graphrag-python** — Graph retrieval capabilities
- **neo4j-agent-memory** — Persistent agent memory backed by Neo4j
- **Neo4j** — Graph database with vector search

## File Structure

```
financial_data_load/
├── azure.yaml              # azd deployment configuration
├── main.py                 # CLI entry point (load, snapshot, resolve, apply-merges, finalize, etc.)
├── setup_env.py            # Sync azd outputs to .env
├── infra/
│   ├── main.bicep          # Azure AI Foundry infrastructure
│   └── main.parameters.json
├── financial-data/         # SEC 10-K data files
│   ├── Company_Filings.csv
│   ├── Asset_Manager_Holdings.csv
│   └── form10k-sample/     # PDF files (8 companies)
├── backups/               # Full database backups (JSON, git-ignored)
├── snapshots/              # Entity snapshots (JSON, git-ignored)
├── logs/                   # Merge plans and processing logs
├── src/                    # Data loader modules
│   ├── config.py           # Settings, Azure auth, Neo4j connection
│   ├── schema.py           # Graph schema, constraints, indexes
│   ├── loader.py           # CSV loading, company/asset manager nodes
│   ├── pipeline.py         # SimpleKGPipeline, PDF processing
│   ├── snapshot.py         # Entity snapshot export (Neo4j → JSON)
│   ├── entity_resolution.py # LLM-based entity resolution
│   ├── backup.py           # Full database backup and restore
│   └── samples.py          # Sample queries
└── solution_srcs/          # Workshop solution files
    ├── config.py           # Shared config for solutions
    ├── test_connection.py  # Connection test script
    ├── 01_01_data_loading.py
    ├── 01_02_embeddings.py
    ├── 01_03_entity_extraction.py
    ├── 01_04_full_dataset_queries.py
    ├── 01_test_full_data_load.py  # Graph structure validation tests
    ├── 02_01_vector_retriever.py
    ├── 02_02_vector_cypher_retriever.py
    ├── 02_03_text2cypher_retriever.py
    ├── 03_02_vector_graph_agent.py
    ├── 03_03_text2cypher_agent.py
    ├── 06_01_fulltext_context_provider.py
    ├── 06_02_vector_context_provider.py
    ├── 06_03_graph_enriched_provider.py
    ├── 05_01_simple_agent.py
    ├── 05_01_fulltext_search.py
    ├── 05_02_context_provider.py
    ├── 05_02_hybrid_search.py
    ├── 07_01_memory_context_provider.py
    ├── 07_02_entity_extraction.py
    ├── 07_03_memory_tools_agent.py
    └── 07_04_reasoning_memory.py
```

## Environment Variables

After running `setup_env.py`, your `.env` file will contain:

```bash
# Azure AI (from azd)
AZURE_AI_EMBEDDING_NAME=text-embedding-3-small
AZURE_AI_MODEL_NAME=gpt-4o
AZURE_AI_PROJECT_ENDPOINT=https://...
AZURE_AI_SERVICES_ENDPOINT=https://...
AZURE_RESOURCE_GROUP=rg-...
AZURE_TENANT_ID=...

# Neo4j Database Connection
NEO4J_URI=neo4j+s://xxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
```

## Cleanup

To remove deployed Azure resources and local azd state:

```bash
azd down --force --purge
```
