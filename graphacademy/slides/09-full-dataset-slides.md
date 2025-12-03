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


# Working with the Full Dataset

Module 1, Lesson 9

---

## Learning Journey: Sample to Scale

In previous lessons, you learned concepts using **small sample datasets**.

Now you'll work with a **complete, production-scale knowledge graph** containing real SEC 10-K filings from multiple Fortune 500 companies.

**This lesson prepares you for Lab 3 Notebook 4.**

---

## Why Start Small, Then Scale?

<div style="display: flex; gap: 2rem;">

<div style="flex: 1;">

### Start Small

**Benefits:**
- ✅ Understand core concepts with manageable data
- ✅ See immediate results from queries
- ✅ Debug and iterate quickly
- ✅ Learn building blocks without complexity
- ✅ Fast feedback loops

</div>

<div style="flex: 1;">

### Then Scale Up

**Benefits:**
- ✅ See how concepts work at production scale
- ✅ Experience cross-document relationships
- ✅ Get realistic search results with diverse data
- ✅ Build confidence for real-world applications
- ✅ Understand performance characteristics

</div>

</div>

---

## What's in the Full Dataset?

### Documents and Chunks
- SEC 10-K filings from **12 major Fortune 500 companies**
- Apple, Microsoft, NVIDIA, Amazon, Intel, Google, Meta, and more
- **Thousands of text chunks** with embeddings
- Full document provenance and relationships

### Key Statistics
- **2,145 total nodes** in the graph
- **5,070 relationships** connecting entities
- Full text search enabled on chunks and entities
- Vector index for semantic search

---

## Extracted Entities: The Knowledge Network

**Companies:** 12 Fortune 500 tech companies

**Risk Factors:** 820+ unique risk factors mentioned across filings

**Financial Metrics:** 470+ metrics tracked across companies

**Products:** 241 products and services

**Executives:** 29 named executives and leaders

**Time Periods:** 102 temporal references

**Plus:** Asset Managers, Transactions, Stock Types, and more

---

## Structured Data: Asset Manager Holdings

**15 Asset Managers** with institutional holdings data:

- BlackRock Inc.
- Vanguard Group Inc.
- State Street Corporation
- Fidelity Investments
- Geode Capital Management
- And more...

**Relationships:**
- OWNS relationships showing institutional ownership
- FILED relationships linking companies to documents
- Cross-company risk factor connections

---

## From Sample to Scale: What Changes?

### 1. Search Quality Improves

**With sample data (3 documents):**
```
Query: "What are Apple's main products?"
Results: 3-5 chunks from one document
```

**With full data (12 companies):**
```
Query: "What are Apple's main products?"
Results: Multiple relevant chunks across different sections
Context: Product descriptions, financial performance, market positioning
Comparison: Apple vs competitors' product portfolios
```

---

## 2. Entity Richness Increases

<div style="display: flex; gap: 2rem;">

<div style="flex: 1;">

### Sample Extraction
- A few companies, products
- Limited relationships
- Single-document context
- Isolated entities

</div>

<div style="flex: 1;">

### Full Dataset
- Comprehensive entity coverage
- Cross-document entity resolution
- Rich relationship patterns
- Multi-company comparisons
- Network effects

</div>

</div>

---

## 3. Cross-Document Insights Emerge

The real power of GraphRAG emerges with scale:

**Find shared risks across companies:**
```cypher
MATCH (c1:Company)-[:FACES_RISK]->(r:RiskFactor)
      <-[:FACES_RISK]-(c2:Company)
WHERE c1 <> c2
WITH c1, c2, count(r) AS sharedRisks
ORDER BY sharedRisks DESC
RETURN c1.name, c2.name, sharedRisks
LIMIT 10
```

**Discover:**
- Which companies face similar challenges?
- What are industry-wide trends?
- How do product portfolios compare?

---

## Example: Shared Risk Analysis

**Query:** Which tech companies share the most risk factors?

**Insights you can discover:**
- Regulatory risks common across FAANG companies
- Cybersecurity concerns shared by cloud providers
- Supply chain risks in hardware manufacturers
- Competition risks among social media platforms

**This analysis is impossible with sample data!**

---

## Example: Asset Manager Analysis

**Query:** Which asset managers have the most diversified holdings?

```cypher
MATCH (am:AssetManager)-[:OWNS]->(c:Company)
WITH am, collect(c.name) AS companies, count(c) AS holdings
ORDER BY holdings DESC
RETURN am.managerName, companies, holdings
```

**Discover:**
- Portfolio diversification strategies
- Concentration in specific tech sectors
- Cross-company ownership patterns

---

## Performance Considerations at Scale

**Vector Search:**
- Indexed for fast semantic similarity
- Handles thousands of chunks efficiently
- Returns top-k most relevant results

**Graph Traversals:**
- Optimized relationship queries
- Indexes on key properties
- Efficient pattern matching

**Full Text Search:**
- Lucene-based search on text properties
- Fast keyword matching across entities

---

## Lab 3 Notebook 4: What You'll Do

**You will:**
1. Load the full dataset into Neo4j
2. Explore the complete knowledge graph
3. Run cross-document queries
4. Compare results with sample data
5. Understand production-scale GraphRAG

**Key Learning:**
- How knowledge graphs scale
- The power of cross-document relationships
- Real-world query patterns
- Performance characteristics

---

## Comparing Sample vs Full Dataset

| Aspect | Sample (3 docs) | Full (12 companies) |
|--------|-----------------|---------------------|
| **Nodes** | ~100-200 | 2,145 |
| **Relationships** | ~200-400 | 5,070 |
| **Companies** | 1-3 | 12 |
| **Risk Factors** | 10-20 | 820+ |
| **Cross-Document Insights** | Limited | Rich |
| **Vector Search Quality** | Basic | Production-ready |

---

## Best Practices for Production Datasets

**1. Incremental Loading:**
- Load and validate in batches
- Monitor memory and performance
- Use constraints and indexes

**2. Query Optimization:**
- Profile slow queries with `EXPLAIN` and `PROFILE`
- Add indexes on frequently queried properties
- Use parameterized queries

**3. Monitoring:**
- Track query performance
- Monitor graph size and growth
- Set up alerts for anomalies

---

## Summary

Working with full datasets reveals the true power of GraphRAG:

**Key Takeaways:**
- Start small for learning, scale up for production
- Full dataset: 2,145 nodes, 5,070 relationships
- Cross-document insights emerge at scale
- Vector search quality improves with more data
- Production graphs enable real-world applications

**The knowledge graph transforms from a demo to a powerful analytical tool.**

---

## Next Steps

You've completed Module 1: Building Knowledge Graphs!

**You now understand:**
- Generative AI and LLM limitations
- Knowledge graph construction
- Schema design and entity extraction
- Chunking and entity resolution
- Vectors and embeddings
- Production-scale considerations

**Next:** Module 2 - GraphRAG Retrievers
