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


# Understanding GraphRAG

Module 2, Lesson 1

---

## What is GraphRAG?

GraphRAG (Graph Retrieval Augmented Generation) uses the strengths of graph databases to provide relevant and useful context to LLMs.

It can be used in conjunction with vector RAG to enhance information retrieval.

---

## Vector RAG vs. GraphRAG

**Vector RAG:**
- Uses embeddings to find contextually relevant information
- Based on semantic similarity

**GraphRAG:**
- Leverages relationships and structure within a graph
- Enhances vector search with connected information

---

## Benefits of GraphRAG

**Richer Context**
- Graphs capture relationships between entities
- Enables retrieval of more relevant and connected information

**Improved Accuracy**
- Combines vector similarity with graph traversal
- Results are more precise and context-aware

---

## Benefits of GraphRAG (continued)

**Explainability**
- Graphs provide clear paths and connections
- Easier to understand why certain results were retrieved

**Flexible Queries**
- Supports complex queries combining multiple search types
- Full-text, vector, and text-to-cypher searches

---

## Benefits of GraphRAG (continued)

**Enhanced Reasoning**
- Enables reasoning over data
- Supports advanced use cases like recommendations and knowledge discovery

---

## Graph-Enhanced Vector Search

A common GraphRAG approach combines vector search with graph traversal.

**Process:**
1. User submits a query
2. Vector search finds semantically similar nodes
3. Graph is traversed to find related nodes or entities
4. Entities and relationships are added to LLM context
5. Related data can be scored based on relevance

---

## Graph-Enhanced Search Applications

**Example: Movie Plot Search**

Enhance vector search results with:
- Related actors, directors, or genres
- Movies with similar themes or connections
- User ratings to filter or rank results

This provides much richer context than text chunks alone.

---

## Full Text Search

Full text search is another powerful technique that complements GraphRAG.

**Vector Search:**
- Excels at finding semantically similar content

**Full Text Search:**
- Matches specific keywords or phrases
- Quickly locates entities based on exact text matches

---

## Combining Search Techniques

Full text search can be used:

**As a replacement for vector search:**
- When users search for specific names or terms

**In conjunction with vector search:**
- Refine results by filtering based on specific keywords
- Combine semantic understanding with exact matching

---

## Text to Cypher

Text to Cypher allows users to express information needs in natural language, which is automatically translated into graph queries.

**How it works:**
- Leverages LLMs to interpret user intent
- Generates precise graph queries from natural language
- Enables direct access to structured data and relationships

---

## Text to Cypher Benefits

**Accessibility**
- Makes advanced graph querying more accessible
- No need to know Cypher query language

**Flexibility**
- Turns user queries into complex searches, aggregations, or traversals
- Handles sophisticated graph operations

**Direct Access**
- Retrieves precise structured data from the graph
- More accurate than interpreting text chunks

---

## Text to Cypher Process

The process is straightforward:
1. User provides a natural language query
2. User's query and graph schema are passed to an LLM
3. LLM generates a Cypher query
4. Generated query is executed against the graph database
5. Results are returned to the user

---

## Text to Cypher Cautions

**Important Considerations:**

- LLM-generated queries may not always be safe or efficient
- You are trusting Cypher generation to the LLM
- Invalid queries could corrupt data or expose sensitive information
- Production environments need proper security and access controls

Always validate and limit access appropriately.

---

## GraphRAG Techniques Summary

GraphRAG encompasses multiple approaches:

- **Vector + Graph:** Semantic similarity plus relationship traversal
- **Full Text Search:** Keyword and phrase matching
- **Text to Cypher:** Natural language to graph queries

Different techniques excel at different types of questions.

---

## Key Takeaway

GraphRAG doesn't always require vector similarity first.

You can use:
- Full-text search alone
- Text-to-Cypher alone
- Combinations of multiple techniques

The best approach depends on the question type and use case.

---

## Summary

GraphRAG enhances LLM information retrieval by:
- Leveraging graph relationships and structure
- Combining multiple search techniques
- Providing richer, more accurate context
- Enabling explainable results
- Supporting flexible query patterns

---

## Next Steps

In the next lesson, you will learn about the three main types of retrievers and when to use each one.

