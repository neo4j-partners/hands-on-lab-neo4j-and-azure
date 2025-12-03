# Module 2: GraphRAG Retrievers

Welcome to Module 2! This module teaches you how to build intelligent retrievers that combine semantic search with graph traversal. You'll learn three distinct retriever patterns, each optimized for different types of questions.

## Module Overview

In this module, you will:

- Understand what GraphRAG is and why it's powerful
- Master three retriever types: Vector, Vector Cypher, and Text2Cypher
- Learn when to use each retriever type
- Build retrievers using the neo4j-graphrag Python package
- Combine retrievers with LLMs for natural language answers
- Develop intuition for choosing the right retriever for each question

## Alignment with Lab 5: GraphRAG Retrievers

This module provides the conceptual foundation for Lab 5, which has 3 hands-on notebooks:

| Lesson | Lab 5 Notebook | Focus |
|--------|----------------|-------|
| Lessons 1-2 | (Introduction) | GraphRAG concepts, retriever fundamentals |
| Lesson 3 | Notebook 1: Vector Retriever | Semantic similarity search, vector indexes |
| Lesson 4 | Notebook 2: Vector Cypher Retriever | Combining vector search with graph traversal |
| Lesson 5 | Notebook 3: Text2Cypher Retriever | Natural language to Cypher queries |
| Lesson 6 | (All notebooks) | Decision framework for choosing retrievers |

## Lessons

1. [Understanding GraphRAG](./01-graphrag-explained.md) - Why GraphRAG matters
2. [What is a Retriever](./02-what-is-a-retriever.md) - Retriever fundamentals
3. [Vector Retriever](./03-vector-retriever.md) - Semantic similarity search
4. [Vector Cypher Retriever](./04-vector-cypher-retriever.md) - Semantic + graph traversal
5. [Text2Cypher Retriever](./05-text2cypher-retriever.md) - Natural language to queries
6. [Choosing the Right Retriever](./06-choosing-retrievers.md) - Decision framework

## Learning Path

**Foundation (Lessons 1-2):**
Understand why GraphRAG exists and what retrievers do.

**Vector Retriever (Lesson 3):**
Learn semantic search using embeddings and vector indexes.

**Vector Cypher Retriever (Lesson 4):**
Enhance semantic search with graph relationships and entities.

**Text2Cypher Retriever (Lesson 5):**
Generate database queries from natural language for precise answers.

**Decision Framework (Lesson 6):**
Learn to choose the right retriever for different question types.

## The Three Retriever Types

**Quick Reference:**

| Retriever | Best For | Example Question |
|-----------|----------|------------------|
| **Vector** | Semantic content search | "What is Apple's business strategy?" |
| **Vector Cypher** | Content + related entities | "What risks affect tech companies?" |
| **Text2Cypher** | Facts, counts, specific queries | "How many companies are in the database?" |

## Navigation

- [← Back to Module 1: Building Knowledge Graphs](../module-1-generative-ai/README.md)
- [Start with Lesson 1: Understanding GraphRAG →](./01-graphrag-explained.md)
- [Skip to Module 3: Agents →](../module-3-agents/README.md)
