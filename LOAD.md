# Proposal: Lab Reorganization for Streamlined Learning Flow

## Overview

This proposal outlines a reorganization of Labs 5 and 6 to create a more focused learning experience. The goal is to group embedding-based retrieval together (vector search) and separate text-to-Cypher as its own distinct topic.

---

## Current Structure

**Lab 5 - Knowledge Graph (4 notebooks):**
1. `01_data_loading.ipynb` - Load documents and chunks
2. `02_embeddings.ipynb` - Add embeddings to chunks
3. `03_entity_extraction.ipynb` - Extract entities and relationships
4. `04_full_dataset.ipynb` - Load complete dataset

**Lab 6 - Retrievers (3 notebooks):**
1. `01_vector_retriever.ipynb` - Pure semantic search
2. `02_vector_cypher_retriever.ipynb` - Semantic search + graph traversal
3. `03_text2cypher_retriever.ipynb` - Natural language to Cypher

---

## Proposed New Structure

### Lab 5: Embeddings and Vector Retrieval

**Theme:** Loading data with embeddings and querying it with vector-based retrievers.

**Notebooks:**
1. `01_load_embeddings.ipynb` - Load documents, chunks, and embeddings
2. `02_vector_retriever.ipynb` - Query embeddings with semantic search
3. `03_vector_cypher_retriever.ipynb` - Combine vector search with graph traversal
4. `04_full_dataset.ipynb` (Optional) - Load the complete dataset for those who want more data

**Learning Outcome:** Participants understand how to build and query an embedding-based knowledge graph using vector similarity.

---

### Lab 6: Text-to-Cypher Retrieval

**Theme:** Converting natural language questions directly into Cypher queries for fact-based retrieval.

**Notebooks:**
1. `01_text2cypher_retriever.ipynb` - Natural language to Cypher queries

**Learning Outcome:** Participants understand how LLMs can translate questions into structured graph queries, and when this approach is preferable to vector search.

---

## Simplifying the Data Loading Notebook

The current `Lab_5_Knowledge_Graph/01_data_loading.ipynb` contains educational content that could be streamlined. Here's what's in it and options for simplification:

### What the Current Notebook Does

1. **Setup and Connection** (~20%)
   - Import statements
   - Neo4j connection setup
   - Environment variable loading

2. **Educational Content** (~30%)
   - Explanations of document chunking concepts
   - Why graph structures matter
   - Visual diagrams of the data model

3. **Core Data Loading Logic** (~30%)
   - Sample text definition
   - Paragraph splitting function
   - Create Document node
   - Create Chunk nodes with `FROM_DOCUMENT` relationships
   - Create `NEXT_CHUNK` chain relationships

4. **Verification Queries** (~20%)
   - Queries to confirm data was loaded correctly
   - Display of graph structure

### Option A: Extract to a Python Module (Recommended)

Create a reusable Python module that handles the data loading:

```
Lab_5_Embeddings/
├── lib/
│   └── data_loader.py     # Reusable loading functions
├── 01_load_embeddings.ipynb
├── 02_vector_retriever.ipynb
└── ...
```

**The `data_loader.py` module would contain:**
- `load_sample_documents()` - Load sample data with embeddings
- `load_full_dataset()` - Load complete dataset (for optional use)
- `verify_data()` - Run verification queries
- Connection management utilities

**The notebook would become simpler:**
```python
from lib.data_loader import load_sample_documents, verify_data

# Load the sample data with embeddings
load_sample_documents(driver)

# Verify it worked
verify_data(driver)
```

**Pros:**
- Notebook focuses on concepts and results, not boilerplate code
- Reusable across notebooks (retrievers can call `verify_data()`)
- Easier to maintain - fix once, applied everywhere
- Participants still see what functions exist but aren't distracted by implementation

**Cons:**
- Some participants may want to see all the code inline
- Slightly more complex project structure

---

### Option B: Simplified Inline Notebook

Keep everything in the notebook but reduce it to essentials:

1. Remove redundant explanations (keep concise comments)
2. Combine multiple cells into logical groups
3. Use a single "load all data" function instead of step-by-step
4. Keep one verification cell at the end

**Estimated reduction:** Current ~30 cells → ~10-12 cells

**Pros:**
- All code visible in one place
- Simpler project structure

**Cons:**
- Still more verbose than Option A
- Code duplication if other notebooks need similar functions

---

### Option C: Hybrid Approach

- Extract only the connection management to a shared module
- Keep the loading logic inline but simplified
- Use helper functions within the notebook

---

## What Data Loading is Actually Necessary?

For the vector retriever notebooks to work, the following must exist in Neo4j:

1. **Chunk nodes** with:
   - `text` property (the content to search)
   - Embeddings stored (via `chunkEmbeddings` vector index)

2. **Document nodes** (for context/provenance)

3. **Relationships:**
   - `FROM_DOCUMENT` - links chunks to their source
   - `NEXT_CHUNK` - preserves document order (optional but useful)

**For the vector_cypher_retriever specifically:**
- Company, AssetManager, RiskFactor nodes
- `OWNS`, `FACES_RISK` relationships
- These come from entity extraction or the full dataset

### Minimum Viable Data Load for Lab 5

If using only sample data (not full dataset), the embeddings notebook could:

1. Load a few Document and Chunk nodes
2. Generate and store embeddings for those chunks
3. Create the vector index

The entity extraction step could be skipped if using pre-processed sample data, or the full dataset could be loaded optionally for those who want richer graph traversal examples.

---

## Recommended Implementation

1. **Create a shared `lib/` directory** with:
   - `data_loader.py` - Data loading functions
   - `connection.py` - Neo4j connection utilities

2. **New Lab 5 notebook structure:**
   - `01_load_embeddings.ipynb` - Call `load_sample_documents()`, explain concepts briefly, verify
   - `02_vector_retriever.ipynb` - (Move from current Lab 6)
   - `03_vector_cypher_retriever.ipynb` - (Move from current Lab 6)
   - `04_full_dataset.ipynb` - (Optional, for those who want complete data)

3. **New Lab 6 notebook:**
   - `01_text2cypher_retriever.ipynb` - (Move from current Lab 6)

4. **Update instructions** to note that:
   - Lab 5 focuses on embedding-based retrieval
   - Lab 6 focuses on structured Cypher-based retrieval
   - Full dataset is optional but provides richer examples

---

## Benefits of This Reorganization

1. **Clearer conceptual grouping:** Embedding/vector approaches together, Cypher approach separate
2. **Faster time to value:** Participants can query data immediately after loading
3. **Reduced cognitive load:** Less context switching between building and querying
4. **Optional depth:** Full dataset available for those who want it, not required for core learning
5. **Maintainable code:** Shared utilities reduce duplication

---

## Migration Checklist

- [ ] Create `lib/` directory with shared modules
- [ ] Refactor data loading into reusable functions
- [ ] Create new Lab 5 with combined loading + vector retrieval
- [ ] Create new Lab 6 with text2cypher focus
- [ ] Update any cross-references between notebooks
- [ ] Update main README with new lab descriptions
- [ ] Test full flow on fresh environment
