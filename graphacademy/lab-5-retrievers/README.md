# Lab 5: GraphRAG Retrievers

Welcome to Lab 5! This lab teaches you three distinct retrieval patterns for getting context from your knowledge graph. Each pattern is optimized for different types of questions.

## Lab Overview

In this lab, you will:

- Understand what retrievers are and how they fit into GraphRAG
- Master three retriever types: Vector, Vector Cypher, and Text2Cypher
- Learn when to use each retriever based on question patterns
- Develop intuition for choosing the right retriever

## The Big Picture

**Where we are**: You have a knowledge graph with structured entities, relationships, and vector-enabled chunks (from Lab 3).

**What you need**: Ways to retrieve relevant context from that graph to answer questions.

**The solution**: Three retriever patterns, each designed for different question types.

## Lessons

1. [Retrievers and the GraphRAG Pattern](./01-retrievers-overview.md) - What retrievers are and how to think about selection
2. [Vector Retriever](./02-vector-retriever.md) - Semantic similarity search for content questions
3. [Vector Cypher Retriever](./03-vector-cypher-retriever.md) - Semantic search + graph traversal for relationship-aware questions
4. [Text2Cypher Retriever](./04-text2cypher-retriever.md) - Natural language to database queries for precise answers

## Learning Path

**Understanding Retrievers (Lesson 1):**
What retrievers do and how to think about which one to use.

**Semantic Search (Lesson 2):**
Vector Retriever for conceptual questions and content exploration.

**Content + Relationships (Lesson 3):**
Vector Cypher Retriever for questions needing both content and connected entities.

**Precise Facts (Lesson 4):**
Text2Cypher Retriever for counts, lists, and specific lookups.

## The Three Retriever Types

| Retriever | What It Does | Best For |
|-----------|--------------|----------|
| **Vector** | Semantic similarity search | "What is...", "Tell me about..." |
| **Vector Cypher** | Semantic search + graph traversal | "Which [entities] are affected by [topic]..." |
| **Text2Cypher** | Natural language to Cypher | "How many...", "List all...", "Who owns..." |

## Decision Framework

When choosing a retriever:

1. **Content or facts?** Content → Vector/Vector Cypher. Facts → Text2Cypher.
2. **Need related entities?** Yes → Vector Cypher.
3. **Need counts or lists?** Yes → Text2Cypher.

## What's Next

Understanding *why* each retriever works for different questions prepares you for Lab 6, where you'll build agents that automatically choose the right retriever based on user questions.

## Navigation

- [← Back to Lab 3: Building Knowledge Graphs](../lab-3-generative-ai/README.md)
- [Start with Lesson 1: Retrievers Overview →](./01-retrievers-overview.md)
- [Skip to Lab 6: Intelligent Agents →](../lab-6-agents/README.md)
