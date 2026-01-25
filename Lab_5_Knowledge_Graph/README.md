# Lab 5 - Building a Knowledge Graph

In this lab, you'll learn how to build a knowledge graph in Neo4j for GraphRAG (Graph Retrieval-Augmented Generation) applications. You'll start with the fundamentals of loading text data, then progress through adding embeddings for semantic search, and finally extract entities to create a rich knowledge graph.

## Prerequisites

Before starting, make sure you have:
- Completed **Lab 0** (Azure sign-in)
- Completed **Lab 1** (Neo4j Aura setup)
- Completed **Lab 4** (Codespace setup with environment variables configured)

## Lab Overview

This lab consists of four notebooks that build on each other:

### 01_data_loading.ipynb - Data Loading Fundamentals
Learn the core concepts of loading text data into Neo4j:
- Understand the Document → Chunk graph structure
- Connect to Neo4j from a Jupyter notebook
- Create Document and Chunk nodes
- Link chunks together with NEXT_CHUNK relationships

### 02_embeddings.ipynb - Embeddings and Vector Search
Add semantic search capabilities to your graph:
- Understand what embeddings are and why they matter
- Use `FixedSizeSplitter` to automatically chunk text
- Generate embeddings using Microsoft Foundry
- Create a vector index in Neo4j
- Perform similarity search to find relevant chunks

### 03_vector_retriever.ipynb - Vector Retriever
Learn the fundamentals of semantic search with vector retrieval:
- Set up a VectorRetriever using Neo4j's vector index
- Perform semantic similarity searches on your knowledge graph
- Use GraphRAG to combine vector search with LLM-generated answers
- Understand how vector search finds contextually similar content

### 04_vector_cypher_retriever.ipynb - Vector Cypher Retriever
Combine vector search with custom Cypher queries for enhanced context:
- Create custom Cypher retrieval queries to traverse graph relationships
- Return additional context like companies and asset managers alongside text chunks
- Discover shared risks among companies using graph traversal
- Compare results with and without graph-enhanced context

## Getting Started

### Select the Python Kernel

Before running any notebook, make sure you have the correct Python kernel selected:

1. Click **Select Kernel** in the top right of the notebook, then select **Python Environments...**

   ![Select Kernel](images/select%20kernel.png)

2. Select the **neo4j-azure-ai-workshop** environment (marked as Recommended)

   ![Select neo4j-azure-ai-workshop](images/neo4j-azure-ai-workshop.png)

### Work Through the Notebooks

1. Open the first notebook: `01_data_loading.ipynb`
2. Work through each notebook in order
3. Each notebook builds on concepts from the previous one

### Running Locally

If you prefer to run the labs from the terminal instead of notebooks, first ensure everything is set up properly:

```bash
uv run setup_env.py
```

Then run the workshop menu:

```bash
uv run new-workshops/main.py
```

Menu items 1, 2, and 3 correspond to notebooks 1, 2, and 3 respectively.

After running these, you will need to restore your Neo4j database by running:

```bash
uv run scripts/restore_neo4j.py --force
```

## Key Concepts

- **Chunks**: Smaller pieces of text split from documents for efficient retrieval
- **Embeddings**: Numerical vectors that capture semantic meaning of text
- **Vector Index**: Enables fast similarity search across embeddings
- **Entity Extraction**: Using LLMs to identify companies, products, services, etc.
- **Knowledge Graph**: Combined structure of documents, chunks, and extracted entities

## Next Steps

After completing this lab, continue to [Lab 6 - GraphRAG Retrievers](../Lab_6_Retrievers) to learn how to implement different retrieval strategies for your knowledge graph.
