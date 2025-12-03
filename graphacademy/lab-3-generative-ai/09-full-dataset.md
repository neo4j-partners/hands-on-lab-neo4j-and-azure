# Working with the Full Dataset

In previous lessons, you learned the concepts using small sample datasets. Now you'll work with a complete, production-scale knowledge graph containing real SEC 10-K filings from multiple companies.

This lesson prepares you for Lab 3 Notebook 4, where you'll load and explore the full dataset.

## Why Start Small, Then Scale?

When building knowledge graphs and learning GraphRAG concepts, it's important to:

**Start Small:**
- Understand core concepts with manageable data
- See immediate results from queries
- Debug and iterate quickly
- Learn the building blocks without complexity

**Then Scale Up:**
- See how concepts work at production scale
- Experience the power of cross-document relationships
- Get realistic search results with diverse data
- Build confidence for real-world applications

## What's in the Full Dataset?

The complete knowledge graph you'll work with contains:

**Documents and Chunks:**
- SEC 10-K filings from multiple major companies
- Apple, Microsoft, NVIDIA, Amazon, Intel, and more
- Thousands of text chunks with embeddings
- Full document provenance and relationships

**Extracted Entities:**
- 12 Companies from Fortune 500
- 820+ Risk Factors mentioned across filings
- 470+ Financial Metrics
- 241 Products and services
- 102 Time Periods
- 29 Executives
- Additional entities (Transactions, Stock Types)

**Structured Data:**
- 15 Asset Managers with holdings information
- OWNS relationships showing institutional ownership
- FILED relationships linking companies to documents
- Cross-company risk factor connections

**Key Statistics:**
- 2,145 total nodes in the graph
- 5,070 relationships connecting entities
- Full text search enabled on chunks and entities
- Vector index for semantic search

## From Sample to Scale: What Changes?

When you move from sample data to the full dataset, several things improve:

**1. Search Quality**

With sample data, vector search returns limited results:
```
Query: "What are Apple's main products?"
Results: 3-5 chunks from one document
```

With full data, you get comprehensive coverage:
```
Query: "What are Apple's main products?"
Results: Multiple relevant chunks across different sections
Context: Product descriptions, financial performance, market positioning
```

**2. Entity Richness**

Sample extraction yields basic entities:
- A few companies, products, services
- Limited relationships
- Single-document context

Full dataset provides a knowledge network:
- Comprehensive entity coverage
- Cross-document entity resolution
- Rich relationship patterns
- Multi-company comparisons

**3. Cross-Document Insights**

The real power of GraphRAG emerges with scale. You can:
- Find shared risks across companies
- Compare product portfolios
- Identify common asset managers
- Discover industry-wide patterns

**Example: Finding Shared Risks**
```cypher
// Which companies share the most risk factors?
MATCH (c1:Company)-[:FACES_RISK]->(r:RiskFactor)<-[:FACES_RISK]-(c2:Company)
WHERE c1 <> c2
WITH c1, c2, count(r) AS sharedRisks
ORDER BY sharedRisks DESC
LIMIT 10
RETURN c1.name, c2.name, sharedRisks
```

## Loading the Full Dataset

In Lab 3 Notebook 4, you'll load the pre-built full dataset using a restore script:

```bash
uv run python scripts/restore_neo4j.py --force
```

This script:
1. Downloads the complete knowledge graph snapshot
2. Clears your existing database
3. Restores all nodes, relationships, and indexes
4. Creates fulltext search indexes
5. Validates the restored data

**What Gets Restored:**
- All 2,145 nodes (Documents, Chunks, Companies, etc.)
- All 5,070 relationships
- Vector index for chunk embeddings
- Fulltext indexes for search
- Schema constraints

## Exploring the Full Graph

Once loaded, you can explore the complete data model:

**View All Node Types:**
```cypher
MATCH (n)
UNWIND labels(n) AS label
WITH label
RETURN label, count(*) AS count
ORDER BY count DESC
```

**View All Relationship Types:**
```cypher
MATCH ()-[r]->()
WITH type(r) AS type
RETURN type, count(*) AS count
ORDER BY count DESC
```

**Explore a Company's Full Profile:**
```cypher
// See everything connected to a company
MATCH (c:Company {name: 'APPLE INC'})
OPTIONAL MATCH (c)-[r1]->(extracted)
WHERE NOT extracted:Chunk AND NOT extracted:Document
OPTIONAL MATCH (am:AssetManager)-[r2:OWNS]->(c)
OPTIONAL MATCH (entity)-[:FROM_CHUNK]->(chunk:Chunk)-[:FROM_DOCUMENT]->(doc:Document)<-[:FILED]-(c)
RETURN c.name,
       count(DISTINCT extracted) AS extractedEntities,
       count(DISTINCT am) AS assetManagers,
       count(DISTINCT chunk) AS textChunks,
       count(DISTINCT doc) AS documents
```

## Vector Search at Scale

With the full dataset, vector search becomes much more powerful:

**Small Sample Results:**
- Limited context from 3-5 chunks
- Single document perspective
- Basic entity mentions

**Full Dataset Results:**
- Rich context from multiple relevant chunks
- Cross-document insights
- Comprehensive entity coverage
- Better semantic understanding

**Example Comparison:**

Query: "What products does Apple make?"

*With Sample Data:*
- Returns 1-2 chunks mentioning iPhone and Mac
- Limited product details
- Single source document

*With Full Data:*
- Returns multiple chunks covering full product lines
- Details on iPhone, Mac, iPad, Services, Wearables
- Context from different document sections
- Related financial metrics and market positioning

## Best Practices for Scale

When working with production-scale knowledge graphs:

**1. Use Appropriate top_k Values**
- Sample data: top_k=3 might be sufficient
- Full data: top_k=5-10 provides better coverage
- Balance between context and relevance

**2. Leverage Graph Traversal**
- Don't just retrieve chunks
- Follow relationships to entities
- Explore cross-document connections
- Use graph patterns for insights

**3. Monitor Query Performance**
- Vector index is optimized for scale
- Graph traversals are efficient
- Combine vector + graph smartly
- Test queries before production

**4. Understand Data Provenance**
- Track which document chunks come from
- Validate entity extraction quality
- Check relationship accuracy
- Maintain data lineage

## Real-World Applications

The full dataset enables real-world GraphRAG scenarios:

**Financial Analysis:**
- Compare risk factors across tech companies
- Analyze product portfolio overlaps
- Track institutional ownership patterns

**Competitive Intelligence:**
- Understand market positioning
- Identify strategic priorities
- Compare business models

**Risk Assessment:**
- Find companies facing similar risks
- Analyze risk factor trends
- Assess interconnected exposures

**Investment Research:**
- Analyze asset manager holdings
- Research company fundamentals
- Discover related companies and sectors

## Check Your Understanding

### What is the main advantage of working with the full dataset compared to sample data?

**Options:**
- [ ] It's faster to query
- [ ] It uses less memory
- [x] It enables cross-document insights and comprehensive entity coverage
- [ ] It's easier to understand

<details>
<summary>Hint</summary>
Think about what becomes possible when you have data from multiple companies and documents.
</details>

<details>
<summary>Show Answer</summary>
**It enables cross-document insights and comprehensive entity coverage**. The full dataset allows you to find patterns across companies, compare entities between documents, and get much richer search results. This is the key benefit of production-scale data - the ability to see connections and patterns that don't exist in small samples.
</details>

### When moving from sample to full dataset, what should you consider adjusting in your queries?

**Options:**
- [ ] The database connection string
- [x] The top_k parameter for retrieving more relevant results
- [ ] The embedding model
- [ ] The Cypher syntax

<details>
<summary>Hint</summary>
Consider what parameter controls how many results are returned from a search.
</details>

<details>
<summary>Show Answer</summary>
**The top_k parameter for retrieving more relevant results**. With more data, you may want to retrieve more results (higher top_k) to ensure you get comprehensive coverage of relevant information. The optimal top_k value often increases as your dataset grows.
</details>

## Summary

In this lesson, you learned about working with production-scale knowledge graphs:

**Key Concepts:**
- Starting small helps you learn concepts, then scaling shows real power
- Full dataset contains 2,145 nodes and 5,070 relationships across multiple companies
- Cross-document insights emerge at scale
- Vector search quality improves dramatically with more data

**What the Full Dataset Enables:**
- Comprehensive entity coverage across companies
- Rich relationship networks
- Cross-document pattern discovery
- Real-world GraphRAG applications

**Important Considerations:**
- Adjust top_k values for scale
- Leverage graph traversal for context
- Monitor query performance
- Validate data quality

In Lab 3 Notebook 4, you'll load this full dataset and experience firsthand how GraphRAG works at production scale. This prepares you for the retriever and agent patterns you'll learn in Modules 2 and 3.

---

**Navigation:**
- [← Previous: Vectors](08-vectors.md)
- [↑ Back to Module 1](README.md)
- [Next: Module 2 - Retrievers →](../module-2-retrievers/README.md)
