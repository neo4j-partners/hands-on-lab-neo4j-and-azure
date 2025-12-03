# Lab 3: Building Knowledge Graphs

Welcome to Lab 3! This lab teaches you why knowledge graphs are essential for GenAI applications and how to build them from documents.

## Lab Overview

In this lab, you will:

- Understand LLM limitations and why context matters
- Learn why traditional RAG isn't enough for complex questions
- Discover how knowledge graphs provide structured context
- Master the key decisions in graph construction: schema, chunking, entity resolution
- Enable semantic search with vector embeddings

## The Big Picture

**The Problem**: LLMs are powerful but limited. They hallucinate, lack access to your data, and can't reason over relationships.

**The Solution**: Provide structured context through knowledge graphs that preserve entities, relationships, and meaning.

**The Process**: Transform documents into queryable knowledge graphs using the `neo4j-graphrag` Python package.

## Lessons

1. [The GenAI Promise and Its Limits](./01-genai-and-limitations.md) - What LLMs can and cannot do
2. [Context and Traditional RAG](./02-context-and-rag.md) - Why context helps and where traditional RAG falls short
3. [From Documents to Knowledge Graphs](./03-building-knowledge-graphs.md) - The transformation process and SimpleKGPipeline
4. [Schema Design](./04-schema-design.md) - Defining what entities and relationships to extract
5. [Chunking Strategies](./05-chunking.md) - Breaking documents into processable pieces
6. [Entity Resolution](./06-entity-resolution.md) - Handling duplicate entities
7. [Vectors and Semantic Search](./07-vectors.md) - Enabling meaning-based search

## Learning Path

**Understanding the Problem (Lessons 1-2):**
Why LLMs need context, and why traditional RAG isn't enough for relationship-aware questions.

**Building Knowledge Graphs (Lessons 3-4):**
How to transform documents into structured knowledge with schema-driven extraction.

**Quality Decisions (Lessons 5-6):**
How chunking and entity resolution affect graph quality.

**Enabling Search (Lesson 7):**
How vector embeddings enable semantic search over your knowledge graph.

## What You'll Build

By the end of this lab, you'll understand how to create a knowledge graph with:

- **Structured entities**: Companies, risks, products, executives, metrics
- **Meaningful relationships**: FACES_RISK, OWNS, MENTIONS, WORKS_FOR
- **Searchable chunks**: Text segments with vector embeddings
- **Document provenance**: Links back to source documents

This knowledge graph becomes the foundation for intelligent retrieval in Lab 5.

## Key Concepts

| Concept | What It Does | Why It Matters |
|---------|--------------|----------------|
| **Schema** | Defines entity and relationship types | Determines what you can query |
| **Chunking** | Breaks documents into pieces | Affects extraction and retrieval quality |
| **Entity Resolution** | Merges duplicate entities | Ensures query accuracy |
| **Vectors** | Enable semantic search | Find content by meaning, not keywords |

## Navigation

- [Start with Lesson 1: GenAI Promise and Limits →](./01-genai-and-limitations.md)
- [Skip to Lab 5: GraphRAG Retrievers →](../lab-5-retrievers/README.md)
- [Back to Workshop Home](../README.md)
