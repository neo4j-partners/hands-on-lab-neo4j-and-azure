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

The `resolve` command accepts CLI overrides so you can test different configs without editing `.env`. Each run writes a separate merge plan to `logs/`. The `compare` command scores all runs against ground truth.

```bash
# Run with different pre-filter thresholds
uv run python main.py resolve --strategy fuzzy --threshold 0.5
uv run python main.py resolve --strategy fuzzy --threshold 0.7
uv run python main.py resolve --strategy prefix --threshold 0.3

# Run with scored confidence mode
uv run python main.py resolve --confidence scored --confidence-threshold 0.9

# Compare all runs side by side with ground truth scoring
uv run python main.py compare

# Or run all 10 predefined configs at once (~25 min total)
./run_all_configs.sh
```

`resolve` reads from the snapshot file and writes a merge plan — it never touches Neo4j. So you can run as many configs as you want without restoring between runs.

To apply your chosen config and finish the pipeline:

```bash
uv run python main.py restore                                  # Reset to backup
uv run python main.py apply-merges --plan logs/<chosen>.json   # Apply the winning plan
uv run python main.py finalize                                 # Constraints, indexes, asset managers
uv run python main.py verify                                   # Check results
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
| `main.py resolve [--snapshot PATH] [--strategy ...] [--threshold ...]` | LLM entity resolution (outputs merge plan to `logs/`) |
| `main.py compare` | Compare all resolution runs and score against ground truth |
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
│   ├── compare.py          # Compare resolution runs, ground truth scoring
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

## Entity Resolution Experimentation Results

We tested 10 entity resolution configs across 4 groups against a ground truth of 6 expected merges and 5 forbidden merges (11 checks total). The dataset is 618 Company entities (181 unique names) extracted from 8 SEC 10-K filings.

### Config Comparison

| Config | Strategy | Threshold | Confidence | Candidates | LLM Merges | Score |
|--------|----------|-----------|------------|----------:|----------:|---------:|
| baseline | fuzzy | 0.6 | binary | 914 | 29 | **11/11** |
| wide-net | fuzzy | 0.5 | binary | 1,689 | 34 | **11/11** |
| tight-filter | fuzzy | 0.7 | binary | 604 | 26 | **11/11** |
| scored-standard | fuzzy | 0.6 | scored@0.8 | 914 | 28 | **11/11** |
| wide-scored | fuzzy | 0.5 | scored@0.8 | 1,689 | 32 | **11/11** |
| **prefix-loose** | **prefix** | **0.3** | **binary** | **28** | **19** | **11/11** |
| scored-strict | fuzzy | 0.6 | scored@0.9 | 914 | 24 | 10/11 |
| prefix-standard | prefix | 0.5 | binary | 18 | 13 | 8/11 |
| very-wide | fuzzy | 0.4 | binary | 5,602 | 13 | 7/11 |

### Findings

**Winner: `prefix` strategy at threshold 0.3.** Scored 11/11 with only 28 candidate pairs — roughly 3% of what the baseline fuzzy config generates. This means ~30x fewer LLM calls for the same ground truth result. It found 14 LLM merge groups (vs 18 for fuzzy), so it misses 4 lower-value matches, but all 6 expected merges passed and all 5 forbidden merges were correctly avoided.

**Key observations:**

- **The LLM is the quality gate, not the pre-filter.** All fuzzy configs from 0.5-0.7 scored identically despite 3x difference in candidate volume. The LLM correctly rejected noise regardless of how much the pre-filter sent.
- **Too wide hurts.** Fuzzy at 0.4 generated 5,602 candidates and paradoxically found fewer merges (13 vs 29). The LLM appears to degrade when batches are dominated by obvious non-matches.
- **Scored mode at 0.9 is too strict.** It dropped Amazon (a correct merge the LLM confirmed with <0.9 confidence). The 0.8 threshold worked identically to binary mode.
- **Prefix at 0.5 is too strict.** "Microsoft" is a prefix of "Microsoft Corporation", but the length ratio (9/23 = 0.39) fails the 0.5 threshold. The 0.3 threshold captures these.

### Recommended Pipeline

```bash
uv run python main.py restore
uv run python main.py apply-merges --plan logs/merge_plan_20260313_180114.json
uv run python main.py finalize
uv run python main.py verify
```

## Cleanup

To remove deployed Azure resources and local azd state:

```bash
azd down --force --purge
```
