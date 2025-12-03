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


# Vector + Cypher Retriever (Detailed)

Module 2, Lesson 4

**Note:** This slide will be renumbered in final sequencing

---

## Beyond Basic Vector Search

<div style="display: flex; gap: 2rem;">

<div style="flex: 1;">

### Vector Retriever

**Query:** "What risks does Apple face?"

**Returns:**
- Text chunks mentioning risks
- Pure semantic search

</div>

<div style="flex: 1;">

### Vector + Cypher Retriever

**Query:** "What risks does Apple face?"

**Returns:**
- Text chunks (semantic)
- Related companies (graph)
- Specific risk factors (entities)
- Asset managers affected (relationships)

</div>

</div>

**The Key Difference:** Adds graph intelligence to semantic search!

---

## What is a Vector Cypher Retriever?

A **hybrid retriever** that combines two powerful techniques:

**1. Vector Search** (Semantic)
- Find relevant chunks by meaning

**2. Graph Traversal** (Structural)
- Navigate from chunks to connected entities
- Gather relationship-aware context

**Result:** The best of both worlds - semantic relevance + structured knowledge

---

## How Vector Cypher Retriever Works

**4-Step Process:**

```
1. EMBED AND SEARCH (Vector Part)
   Find chunks about "banking regulations"
   ↓
2. EXECUTE CUSTOM CYPHER (Graph Part)
   From those chunks, traverse to:
   → Companies mentioned
   → Risk factors they face
   → Asset managers who own them
   ↓
3. RETURN COMBINED RESULTS
   Chunk text + Companies + Asset managers + Risks
   ↓
4. LLM GENERATES ANSWER
   Using both textual and structured context
```

---

## Creating a Vector Cypher Retriever

```python
from neo4j_graphrag.retrievers import VectorCypherRetriever

# Define custom Cypher query
retrieval_query = """
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)
      -[:FILED]-(company:Company)
OPTIONAL MATCH (company)-[:FACES_RISK]->(risk:RiskFactor)
WITH node, score, company, collect(risk.name)[0..20] AS risks
WHERE score IS NOT NULL
RETURN
    node.text AS text,
    score,
    {company: company.name, risks: risks} AS metadata
ORDER BY score DESC
"""

# Create the retriever
vector_cypher_retriever = VectorCypherRetriever(
    driver=driver,
    index_name='chunkEmbeddings',
    embedder=embedder,
    retrieval_query=retrieval_query  # Custom graph traversal
)
```

---

## Understanding the Retrieval Query

**What the library provides automatically:**

```cypher
CALL db.index.vector.queryNodes($index_name, $top_k, $embedding)
YIELD node, score
// Your retrieval_query starts here with 'node' and 'score'
```

**Your retrieval_query:**
- Receives `node` (the matched chunk) and `score` (similarity)
- Traverses from `node` to related entities
- Can go as deep as needed in the graph
- Returns enriched context

---

## Example Retrieval Query Breakdown

```cypher
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)
      -[:FILED]-(company:Company)
```
**Traverses:** Chunk → Document → Company

```cypher
OPTIONAL MATCH (company)-[:FACES_RISK]->(risk:RiskFactor)
```
**Gathers:** Related risk factors (optional, won't filter out companies without risks)

```cypher
WITH node, score, company, collect(risk.name)[0..20] AS risks
```
**Aggregates:** Up to 20 risk names per company

```cypher
RETURN node.text, score, {company: company.name, risks: risks} AS metadata
```
**Returns:** Text + metadata with company and risks

---

## The Power of OPTIONAL MATCH

**Without OPTIONAL MATCH:**
```cypher
MATCH (company)-[:FACES_RISK]->(risk:RiskFactor)
```
❌ Only returns companies that have risk factors
❌ Filters out companies with no risks

**With OPTIONAL MATCH:**
```cypher
OPTIONAL MATCH (company)-[:FACES_RISK]->(risk:RiskFactor)
```
✅ Returns all companies
✅ Risk list is empty for companies without risks
✅ No data loss

**Use OPTIONAL MATCH** when you want complete results!

---

## Vector Cypher Retriever Best For

✅ **Getting both content and rich context**

✅ **Understanding relationships** between entities

✅ **Questions requiring entity-specific aggregations**

✅ **Comprehensive answers** from multiple connected data points

**Example Queries:**
- "Which asset managers are most affected by cryptocurrency policies?"
- "What products do cloud computing companies offer?"
- "Which executives work at AI companies?"

---

## Example: Asset Manager Query

**Query:** "Which asset managers are affected by cryptocurrency policies?"

**Vector Search Finds:**
- Chunks mentioning cryptocurrency regulations

**Cypher Traversal Gets:**
```cypher
MATCH (node)-[:FROM_DOCUMENT]-(doc)-[:FILED]-(company)
MATCH (company)<-[:OWNS]-(manager:AssetManager)
RETURN node.text, company.name, manager.managerName
```

**Returns:**
- Regulatory text (context)
- Affected companies (entities)
- Their asset managers (relationships)

---

## Comparison: Vector vs Vector Cypher

| Aspect | Vector Only | Vector + Cypher |
|--------|-------------|-----------------|
| **Search** | Semantic similarity | Semantic + graph |
| **Returns** | Text chunks | Chunks + entities |
| **Context** | Unstructured | Structured + unstructured |
| **Relationships** | ❌ No | ✅ Yes |
| **Speed** | Faster | Slightly slower |
| **Complexity** | Simple | Requires Cypher knowledge |
| **Power** | Limited | Full graph capabilities |

---

## When Vector Cypher Can Fail

**Problem:** If vector search doesn't find relevant chunks, graph traversal won't help.

**Example:**
```
Query: "What are Apple's risks?"
Vector Search: Finds chunks about "risk management frameworks"
            (not specifically about Apple)
Cypher Traversal: Traverses from those chunks
Result: May not find Apple-specific information
```

**The chunk is the anchor** - you can only traverse from what vector search finds!

---

## Making Vector Cypher Queries Robust

**Good Query Design:**

1. **Use OPTIONAL MATCH** for relationships that may not exist
2. **Add WHERE clauses** to filter results
3. **Limit collections** to prevent huge result sets
4. **Order by score** to prioritize most relevant results

```cypher
MATCH (node)-[:FROM_DOCUMENT]-(doc)-[:FILED]-(company)
OPTIONAL MATCH (company)-[:FACES_RISK]->(risk)
WITH node, score, company, collect(risk.name)[0..20] AS risks
WHERE score > 0.8  // Only high-confidence matches
RETURN node.text, score, {company: company.name, risks: risks}
ORDER BY score DESC
```

---

## Advanced Traversals

**You can go multiple hops deep:**

```cypher
// Find asset managers through company ownership
MATCH (node)-[:FROM_DOCUMENT]-(doc)-[:FILED]-(company)
MATCH (company)<-[:OWNS]-(manager:AssetManager)
OPTIONAL MATCH (company)-[:FACES_RISK]->(risk)
OPTIONAL MATCH (company)-[:HAS_PRODUCT]->(product)
RETURN
    node.text,
    score,
    {
        company: company.name,
        manager: manager.managerName,
        risks: collect(DISTINCT risk.name)[0..10],
        products: collect(DISTINCT product.name)[0..10]
    } AS metadata
```

---

## Metadata Structure

**Return structured metadata for LLM context:**

```python
results = vector_cypher_retriever.search(query)

for record in results.records:
    print(record['text'])      # Chunk text
    print(record['score'])     # Similarity score
    print(record['metadata'])  # Structured data:
    # {
    #   'company': 'Apple Inc.',
    #   'risks': ['Data Privacy', 'Supply Chain'],
    #   'products': ['iPhone', 'iPad']
    # }
```

**LLM uses both text and metadata** to generate informed answers.

---

## Performance Considerations

**Vector Search:** Very fast (indexed)

**Graph Traversal:** Speed depends on:
- Depth of traversal
- Number of relationships
- Complexity of MATCH patterns

**Optimization Tips:**
- Limit collection sizes: `collect()[0..20]`
- Use indexes on frequently queried properties
- Profile queries with `EXPLAIN` and `PROFILE`
- Keep traversal depth reasonable (2-3 hops max)

---

## Summary

Vector Cypher Retriever = Semantic Search + Graph Intelligence

**Key Concepts:**
- Two-step process: vector search → graph traversal
- Custom Cypher query extends vector results
- Returns both chunks and entity relationships
- Starts with `node` and `score` from vector search

**Best For:** Questions requiring both semantic relevance and graph context

**Limitation:** Quality depends on vector search finding right chunks

**Next:** Text2Cypher Retriever for precise graph queries

---

## Next Steps

In the next lesson, you will learn about the Text2Cypher Retriever, which converts natural language directly into Cypher queries for precise, structured data retrieval.

**Lab 5 Notebook 2:** Hands-on with Vector + Cypher Retriever
