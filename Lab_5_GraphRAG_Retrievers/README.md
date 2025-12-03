# Lab 5 - GraphRAG Retrievers

In this lab, you'll learn how to implement Graph Retrieval-Augmented Generation (GraphRAG) using different retriever strategies with the Neo4j GraphRAG Python package. You'll explore vector search, combine vector search with Cypher queries for richer context, and use natural language to generate Cypher queries automatically.

## Prerequisites

Before starting, make sure you have:
- Completed **Lab 0** (Azure sign-in)
- Completed **Lab 1** (Neo4j Aura setup)
- Completed **Lab 2** (Codespace setup with environment variables configured)
- Completed **Lab 3** (Azure AI Foundry setup)
- Completed **Lab 4** (Knowledge graph built with embeddings)

## Lab Overview

This lab consists of three notebooks that demonstrate different retrieval strategies:

### 02_01_vector_retriever.ipynb - Vector Retriever
Learn the fundamentals of semantic search with vector retrieval:
- Set up a VectorRetriever using Neo4j's vector index
- Perform semantic similarity searches on your knowledge graph
- Use GraphRAG to combine vector search with LLM-generated answers
- Understand how vector search finds contextually similar content

### 02_02_vector_cypher_retriever.ipynb - Vector Cypher Retriever
Combine vector search with custom Cypher queries for enhanced context:
- Create custom Cypher retrieval queries to traverse graph relationships
- Return additional context like companies and asset managers alongside text chunks
- Discover shared risks among companies using graph traversal
- Compare results with and without graph-enhanced context

### 02_03_text2cypher_retriever.ipynb - Text2Cypher Retriever
Use natural language to query your graph directly:
- Automatically convert natural language questions to Cypher queries
- Query specific nodes, relationships, and properties without writing Cypher
- Understand the graph schema and how it guides query generation
- Build accessible natural language interfaces to your knowledge graph

## Getting Started

1. Open the first notebook: `02_01_vector_retriever.ipynb`
2. Work through each notebook in order
3. Each notebook introduces a different retrieval strategy

### Running Locally

If you prefer to run the labs from the terminal instead of notebooks, first ensure everything is set up properly:

```bash
uv run setup_env.py
```

Then run the workshop menu:

```bash
uv run new-workshops/main.py
```

Menu items 5, 6, and 7 correspond to notebooks 1, 2, and 3 respectively.

## Key Concepts

- **Vector Retriever**: Uses semantic similarity to find relevant text chunks based on meaning, not just keywords
- **Vector Cypher Retriever**: Combines vector search with Cypher graph traversal to return richer, relationship-aware context
- **Text2Cypher Retriever**: Converts natural language questions into Cypher queries for precise, fact-based answers
- **GraphRAG**: A pipeline that combines retrievers with LLMs to generate contextual answers grounded in your knowledge graph
- **Retrieval Context**: The data returned by retrievers that grounds LLM responses in your actual data

## When to Use Each Retriever

| Retriever | Best For |
|-----------|----------|
| **Vector** | Semantic questions where meaning matters more than exact matches |
| **Vector Cypher** | Questions requiring both semantic similarity and graph relationships |
| **Text2Cypher** | Fact-based questions about specific entities, counts, or relationships |
