# Lab 6 - GraphRAG Retrievers

In this lab, you'll learn how to use natural language to query your knowledge graph, extract structured entities from text, and work with a complete dataset. You'll use Text2Cypher to convert questions into Cypher queries, build richer graphs through entity extraction, and see the full power of GraphRAG with real-world data.

## Prerequisites

Before starting, make sure you have:
- Completed **Lab 0** (Azure sign-in)
- Completed **Lab 1** (Neo4j Aura setup)
- Completed **Lab 4** (Codespace setup with environment variables configured)
- Completed **Lab 5** (Knowledge graph built with embeddings)

## Lab Overview

This lab consists of three notebooks:

### 01_text2cypher_retriever.ipynb - Text2Cypher Retriever
Use natural language to query your graph directly:
- Automatically convert natural language questions to Cypher queries
- Query specific nodes, relationships, and properties without writing Cypher
- Understand the graph schema and how it guides query generation
- Build accessible natural language interfaces to your knowledge graph

### 02_entity_extraction.ipynb - Entity Extraction
Extract structured entities and relationships from text:
- Learn the difference between lexical and semantic graphs
- Define a schema with entity and relationship types
- Use `SimpleKGPipeline` to extract entities from text
- Query the combined graph (chunks + entities)

### 03_full_dataset.ipynb - Working with the Full Dataset
Load the complete SEC 10-K dataset and explore richer results:
- Load pre-built knowledge graph with multiple company filings
- See improved search results with more data
- Explore the expanded entity and relationship network

## Getting Started

1. Open the first notebook: `01_text2cypher_retriever.ipynb`
2. Work through each notebook in order
3. Each notebook builds on the previous one

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

- **Text2Cypher Retriever**: Converts natural language questions into Cypher queries for precise, fact-based answers
- **Entity Extraction**: Using LLMs to identify companies, products, services, and relationships from text
- **Knowledge Graph**: Combined structure of documents, chunks, and extracted entities
- **GraphRAG**: A pipeline that combines retrievers with LLMs to generate contextual answers grounded in your knowledge graph

## Next Steps

After completing this lab, continue to [Lab 7 - GraphRAG Agents](../Lab_7_Agents) to learn how to build intelligent agents that can automatically select the right retriever based on the question.
