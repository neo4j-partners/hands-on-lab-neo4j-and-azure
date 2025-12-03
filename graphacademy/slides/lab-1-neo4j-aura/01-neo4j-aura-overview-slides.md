---
marp: true
theme: default
paginate: true
---

<style>
section {
  --marp-auto-scaling-code: false;
}

li {
  opacity: 1 !important;
  animation: none !important;
  visibility: visible !important;
}

/* Disable all fragment animations */
.marp-fragment {
  opacity: 1 !important;
  visibility: visible !important;
}

ul > li,
ol > li {
  opacity: 1 !important;
}
</style>

![bg contain](../images/GraphRAG_Agent_Blueprint.jpg)

---

# Neo4j Aura: Cloud Graph Database

---

## What is Neo4j Aura?

Neo4j Aura is a **fully managed cloud graph database service** that eliminates the operational overhead of running a graph database.

**Key Characteristics:**
- **Fully managed** - No infrastructure to maintain
- **Scalable** - Automatically scales with your data and queries
- **Secure** - Enterprise-grade security and compliance
- **Available everywhere** - Deploy in AWS, GCP, or Azure regions

---

## Why Use a Graph Database?

Traditional databases struggle with **connected data**:

| Scenario | Relational DB | Graph DB |
|----------|---------------|----------|
| "Find friends of friends" | Complex JOINs, slow | Natural traversal, fast |
| "What impacts what?" | Multiple queries | Single query |
| "How are these connected?" | Hard to express | Native pattern matching |

**Graphs excel at relationship-heavy queries** that would require dozens of JOINs in SQL.

---

## The Value of Aura for AI/GenAI

Neo4j Aura provides unique capabilities for building AI applications:

**GraphRAG Foundation:**
- Store knowledge graphs that power AI agents
- Vector search for semantic similarity
- Graph traversal for relationship reasoning

**Production-Ready:**
- Built-in vector indexes for embeddings
- Cypher query language for complex retrieval
- APIs for integration with LLM frameworks

---

## What You'll Build Today

In this workshop, you'll use Neo4j Aura to:

1. **Create a knowledge graph** from SEC 10-K filings
2. **Store embeddings** for semantic search
3. **Build retrievers** that combine vector and graph queries
4. **Deploy AI agents** that reason over your data

The graph structure enables questions that pure vector search cannot answer.

---


## Summary

Neo4j Aura provides:

- **Managed graph database** - Focus on your data, not infrastructure
- **Graph-native storage** - Relationships are first-class citizens
- **AI/GenAI capabilities** - Vector indexes, GraphRAG support

**Next:** Learn about Aura Agents for no-code GraphRAG applications.

