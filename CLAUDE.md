# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A hands-on workshop teaching GraphRAG (Graph Retrieval-Augmented Generation) techniques using Neo4j with Microsoft Azure services. The lab uses real SEC 10-K company filings to demonstrate building knowledge graphs, implementing retrieval strategies, and creating AI agents.

## Commands

### Setup & Dependencies
```bash
uv sync --prerelease=allow                    # Install dependencies
uv run setup_env.py                           # Sync azd outputs to .env
```

### Azure Infrastructure
```bash
azd env new                                    # Initialize environment
azd env set AZURE_LOCATION eastus2             # Set region (eastus2, swedencentral, westus2)
azd up                                         # Deploy infrastructure
azd down                                       # Cleanup resources
```

### Running Workshop Solutions
```bash
cd financial_data_load
uv run python main.py                          # Interactive menu
uv run python main.py 4                        # Run specific solution
uv run python main.py A                        # Run all from option 4 onwards
uv run python src/test_connection.py           # Test Neo4j and Azure connections
```

### Data Loading
```bash
cd financial_data_load
uv run python full_data_load.py --limit 1 --clear   # Test with 1 PDF
uv run python full_data_load.py --clear             # Load all 8 PDFs
```

### Jupyter Notebooks
Select kernel: `.venv` (neo4j-azure-ai-workshop), run cells with `Shift+Enter`

### Local Library Development
```bash
uv pip install --force-reinstall ~/projects/neo4j-graphrag-python
```

## Architecture

### Knowledge Graph Data Model
- **Lexical layer**: `Document` → `Chunk` nodes with `NEXT_CHUNK` relationships
- **Semantic layer**: Entities (`Company`, `Product`, `RiskFactor`, `Executive`, `FinancialMetric`, `AssetManager`) extracted via LLM
- **Provenance**: `FROM_DOCUMENT` and `FROM_CHUNK` relationships link entities to source text

### Retrieval Strategies (in `financial_data_load/src/02_*.py`)
1. **Vector Retriever** - Semantic similarity using chunk embeddings
2. **Vector Cypher Retriever** - Vector search + custom Cypher traversal for enriched context
3. **Text2Cypher** - Natural language to Cypher query generation
4. **Hybrid Search** - Combined keyword (fulltext) and semantic (vector) search

### Agent Framework (in `financial_data_load/src/03_*.py`)
Uses Microsoft Agent Framework with Azure AI Foundry. Agents combine multiple tools:
- Schema retrieval tool
- Vector search + graph traversal tool
- Text2Cypher tool

### Configuration
- `financial_data_load/src/config.py` - Pydantic settings for Neo4j and Azure
- Uses `AzureCliCredential` for authentication (run `az login` first)

## Project Structure

```
Lab_5_Knowledge_Graph/     # Jupyter notebooks: KG fundamentals
Lab_6_Retrievers/          # Jupyter notebooks: GraphRAG patterns
Lab_7_Agents/              # Jupyter notebooks: Agent Framework
financial_data_load/       # Python CLI solutions
  ├── src/                 # Numbered solution files (01_xx, 02_xx, 03_xx, 05_xx)
  ├── main.py              # Interactive solution runner
  ├── full_data_load.py    # SimpleKGPipeline data loader
  └── financial-data/      # SEC 10-K PDFs and CSV metadata
infra/                     # Bicep templates for Azure deployment
```

## Key Technical Details

- **Python**: Requires 3.12.x (not 3.13+)
- **Embeddings**: 1536 dimensions via text-embedding-ada-002
- **Vector Index**: `chunkEmbeddings` on `Chunk.embedding`
- **Fulltext Indexes**: `chunkText` (keyword search), `search_entities` (entity lookup)
- **Local Fork**: Uses local `neo4j-graphrag-python` from `~/projects/neo4j-graphrag-python`

## Environment Variables

Required in `.env`:
```
NEO4J_URI=neo4j+s://xxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<password>
```

Auto-populated by `setup_env.py`:
```
AZURE_AI_PROJECT_ENDPOINT=<foundry endpoint>
AZURE_AI_MODEL_NAME=gpt-4o-mini
AZURE_AI_EMBEDDING_NAME=text-embedding-ada-002
```
