# Module 1: Building Knowledge Graphs

Welcome to Module 1! This module teaches you how to build knowledge graphs for GraphRAG applications. You'll start with the fundamentals of Generative AI, then learn to transform unstructured documents into structured, searchable knowledge graphs.

## Module Overview

In this module, you will:

- Understand Generative AI concepts and LLM limitations
- Learn why context is crucial for accurate LLM responses
- Master the Document → Chunk → Entity data model
- Build knowledge graphs from unstructured documents
- Work with embeddings and vector search
- Extract entities and relationships using LLMs
- Design effective schemas for entity extraction
- Optimize chunking strategies for your data
- Work with production-scale datasets

## Alignment with Lab 3: Graph Building

This module provides the conceptual foundation for Lab 3, which has 4 hands-on notebooks:

| Lesson | Lab 3 Notebook | Focus |
|--------|----------------|-------|
| Lessons 1-3 | (Introduction) | GenAI concepts, LLM limitations, importance of context |
| Lesson 4 | Notebook 1: Data Loading | Document and Chunk structure, relationships |
| Lessons 6 & 8 | Notebook 2: Embeddings | Vector search, FixedSizeSplitter, semantic similarity |
| Lessons 4 & 5 | Notebook 3: Entity Extraction | Schema definition, SimpleKGPipeline, entity types |
| Lesson 9 | Notebook 4: Full Dataset | Production-scale data, cross-document insights |

## Lessons

1. [What is Generative AI](./01-what-is-genai.md) - Foundation concepts
2. [LLM Limitations](./02-llm-limitations.md) - Understanding constraints
3. [Context](./03-context.md) - Why RAG matters
4. [Building the Graph](./04-building-the-graph.md) - Documents, chunks, and entities
5. [Schema Design](./05-schema-design.md) - Designing entity types and relationships
6. [Optimizing Chunk Size](./06-chunking.md) - Chunking strategies for better extraction
7. [Entity Resolution](./07-entity-resolution.md) - Resolving duplicate entities
8. [Vectors](./08-vectors.md) - Embeddings and semantic search
9. [Working with Full Datasets](./09-full-dataset.md) - Production-scale knowledge graphs

## Learning Path

**Conceptual Foundation (Lessons 1-3):**
Learn why GraphRAG exists and what problems it solves.

**Building Basics (Lessons 4-5):**
Understand the data model and schema design principles.

**Optimization (Lessons 6-7):**
Learn techniques for improving extraction quality.

**Search and Scale (Lessons 8-9):**
Add semantic search and work with production data.

## Navigation

- [← Back to Workshop Home](../README.md)
- [Start with Lesson 1: What is Generative AI →](./01-what-is-genai.md)
- [Skip to Module 2: Retrievers →](../module-2-retrievers/README.md)
