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


# Vector Retriever (Detailed)

Module 2, Lesson 3

**Note:** This slide will be renumbered in final sequencing

---

## What is a Vector Retriever?

The **simplest and most fundamental** retriever type in GraphRAG.

**Core Function:** Find relevant text chunks using semantic similarity.

**Key Insight:** Search by meaning, not just keywords.

**Use Case:** When you need semantically similar content without complex graph traversal.

---

## How Vector Retriever Works

**5-Step Process:**

1. **Take your natural language query**
2. **Convert it to an embedding** (vector of numbers)
3. **Search vector index** for similar chunk embeddings
4. **Return the most semantically similar chunks**
5. **Optionally feed to LLM** for answer generation

**The magic:** Embeddings capture semantic meaning!

---

## Vector Retriever Flow Diagram

```
User Query: "What are the risks that Apple faces?"
    ↓
[1. EMBED THE QUERY]
    Vector: [0.023, -0.015, 0.087, ...] (1536 dimensions)
    ↓
[2. SEARCH VECTOR INDEX]
    Compare with all chunk embeddings using cosine similarity
    ↓
[3. RETURN TOP MATCHES]
    Chunk 1: "...potential liabilities..." (score: 0.9148)
    Chunk 2: "...provide relief..." (score: 0.9124)
    Chunk 3: "...sophistication..." (score: 0.9112)
    ↓
[4. GENERATE ANSWER]
    LLM uses chunks as context
```

---

## Vector Retriever Components

**1. Embedder**
- Converts text to vectors
- Example: OpenAI's `text-embedding-ada-002`
- Creates 1536-dimensional vectors

**2. Vector Index**
- Neo4j vector index on chunk embeddings
- Enables fast similarity search
- Optimized for large-scale retrieval

**3. Similarity Function**
- Cosine similarity measures vector angles
- Higher score = more similar meaning

**4. Top-K Parameter**
- Controls number of results (e.g., top_k=5)

---

## Creating a Vector Retriever

Using the `neo4j-graphrag` Python package:

```python
from neo4j_graphrag.retrievers import VectorRetriever

# Initialize the retriever
vector_retriever = VectorRetriever(
    driver=driver,                    # Neo4j connection
    index_name='chunkEmbeddings',     # Vector index name
    embedder=embedder,                 # Embedding model
    return_properties=['text']         # Chunk properties to return
)
```

**That's it!** Simple, powerful semantic search.

---

## Performing a Vector Search

**Simple Search:**

```python
query = "What are the risks that Apple faces?"

# Search for top 5 most similar chunks
results = vector_retriever.search(
    query_text=query,
    top_k=5
)

# Process results
for record in results.records:
    print(f"Score: {record['score']}")
    print(f"Text: {record['text']}")
    print("---")
```

---

## Understanding Search Results

**Each result contains:**

- **text**: The chunk content
- **score**: Similarity score (0-1, higher is better)
- **metadata**: Additional chunk properties

**Score Interpretation:**
- 0.95+ : Highly relevant
- 0.85-0.95 : Very relevant
- 0.75-0.85 : Moderately relevant
- < 0.75 : Less relevant

**Tip:** Adjust top_k and score thresholds based on your use case.

---

## Vector Retriever Best For

✅ **Semantic search** across all documents

✅ **Finding conceptually similar** content

✅ **Broad exploratory questions** about topics

✅ **When exact keywords don't match** but meaning does

**Example Queries:**
- "What are cybersecurity threats?"
- "How is AI being used?"
- "What are supply chain challenges?"

---

## Vector Retriever Limitations

❌ **Returns only text chunks**, no entity relationships

❌ **May miss entity-specific context** without graph traversal

❌ **Cannot aggregate** information across multiple entities

❌ **No structured data** from graph relationships

**When Chunks Aren't Enough:** Use Vector + Cypher Retriever (next lesson)

---

## Optimizing Top-K Parameter

**Small top_k (1-3):**
- Faster
- Most relevant results only
- May miss important context

**Medium top_k (5-10):**
- Balanced approach
- Good coverage
- Most common choice

**Large top_k (15-20):**
- Maximum coverage
- More context for LLM
- May include less relevant content

---

## Example: Semantic vs Keyword Search

**Query:** "AI safety risks"

**Keyword Search Finds:**
- Exact phrase: "AI safety risks"
- Variations: "artificial intelligence safety", "AI risks"

**Vector Search Finds:**
- Related concepts: "machine learning vulnerabilities"
- Semantic matches: "algorithmic bias concerns"
- Broader topics: "automated decision-making challenges"

**Vector search understands meaning beyond keywords!**

---

## Practical Tips

**1. Use Descriptive Queries:**
- Good: "What are the financial risks in cloud computing?"
- Less Good: "risks"

**2. Adjust top_k Based on Query:**
- Specific questions: lower top_k
- Broad exploration: higher top_k

**3. Monitor Scores:**
- Low scores? Refine your query or check embeddings

**4. Return Useful Properties:**
- Include metadata for context
- Source document, chunk index, timestamps

---

## Summary

Vector Retriever is your foundation for semantic search:

**Key Concepts:**
- Converts queries to embeddings
- Searches vector index for similarity
- Returns semantically similar chunks
- Fast, simple, powerful

**Best For:** Semantic search without graph complexity

**Limitation:** No entity relationships or graph context

**Next:** Vector + Cypher Retriever adds graph intelligence!

---

## Next Steps

In the next lesson, you will learn about the Vector + Cypher Retriever, which combines semantic search with graph traversal for richer, contextual results.

**Lab 5 Notebook 1:** Hands-on with Vector Retriever
