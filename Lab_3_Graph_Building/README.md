# Lab 3 - Building a Knowledge Graph

In this lab, you'll learn how to build a knowledge graph in Neo4j for GraphRAG (Graph Retrieval-Augmented Generation) applications. You'll start with the fundamentals of loading text data, then progress through adding embeddings for semantic search, and finally extract entities to create a rich knowledge graph.

## Prerequisites

Before starting, make sure you have:
- Completed **Lab 0** (Azure sign-in)
- Completed **Lab 1** (Neo4j Aura setup)
- Completed **Lab 2** (Codespace setup with environment variables configured)

## Lab Overview

This lab consists of four notebooks that build on each other:

### 01_01_data_loading.ipynb - Data Loading Fundamentals
Learn the core concepts of loading text data into Neo4j:
- Understand the Document → Chunk graph structure
- Connect to Neo4j from a Jupyter notebook
- Create Document and Chunk nodes
- Link chunks together with NEXT_CHUNK relationships

### 01_02_embeddings.ipynb - Embeddings and Vector Search
Add semantic search capabilities to your graph:
- Understand what embeddings are and why they matter
- Use `FixedSizeSplitter` to automatically chunk text
- Generate embeddings using Azure OpenAI
- Create a vector index in Neo4j
- Perform similarity search to find relevant chunks

### 01_03_entity_extraction.ipynb - Entity Extraction
Extract structured entities and relationships from text:
- Learn the difference between lexical and semantic graphs
- Define a schema with entity and relationship types
- Use `SimpleKGPipeline` to extract entities from text
- Query the combined graph (chunks + entities)

### 01_04_full_dataset.ipynb - Working with the Full Dataset
Load the complete SEC 10-K dataset and explore richer results:
- Load pre-built knowledge graph with multiple company filings
- See improved search results with more data
- Explore the expanded entity and relationship network

## Getting Started

### Select the Python Kernel

Before running any notebook, make sure you have the correct Python kernel selected:

1. Click **Select Kernel** in the top right of the notebook, then select **Python Environments...**

   ![Select Kernel](images/select%20kernel.png)

2. Select the **neo4j-azure-ai-workshop** environment (marked as Recommended)

   ![Select neo4j-azure-ai-workshop](images/neo4j-azure-ai-workshop.png)

### Work Through the Notebooks

1. Open the first notebook: `01_01_data_loading.ipynb`
2. Work through each notebook in order
3. Each notebook builds on concepts from the previous one

## Key Concepts

- **Chunks**: Smaller pieces of text split from documents for efficient retrieval
- **Embeddings**: Numerical vectors that capture semantic meaning of text
- **Vector Index**: Enables fast similarity search across embeddings
- **Entity Extraction**: Using LLMs to identify companies, products, services, etc.
- **Knowledge Graph**: Combined structure of documents, chunks, and extracted entities
