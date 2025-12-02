# Vector Cypher Retriever

The Vector Cypher Retriever enhances basic vector search by combining it with custom Cypher queries. This lets you retrieve not just relevant text chunks, but also related entities and relationships from your knowledge graph.

This lesson prepares you for Lab 5 Notebook 2, where you'll build Vector Cypher Retrievers that traverse the graph to provide richer context.

## Beyond Basic Vector Search

**Vector Retriever:**
```
Query: "What risks does Apple face?"
Returns: Text chunks mentioning risks
```

**Vector Cypher Retriever:**
```
Query: "What risks does Apple face?"
Returns: Text chunks + related companies + specific risk factors + asset managers affected
```

**The Key Difference:** Vector Cypher combines semantic search with graph traversal to return structured, relationship-aware context.

## What is a Vector Cypher Retriever?

A Vector Cypher Retriever:
1. Performs vector similarity search to find relevant chunks (like Vector Retriever)
2. **Then** executes a custom Cypher query starting from those chunks
3. Traverses the graph to gather related entities and relationships
4. Returns both unstructured context (chunks) and structured data (entities)

**The Power:** You get the best of both worlds - semantic search AND graph relationships.

## How It Works

**Step-by-Step Process:**

```
User Query: "Who are the asset managers affected by banking regulations?"
    ↓
1. EMBED AND SEARCH (Vector Part)
   Find chunks mentioning "banking regulations"
    ↓
2. EXECUTE CUSTOM CYPHER (Graph Part)
   Starting from those chunks, traverse to:
   - Companies mentioned in chunks
   - Risk factors the companies face
   - Asset managers who own those companies
    ↓
3. RETURN COMBINED RESULTS
   Chunk text + Company names + Asset manager names + Risk factors
    ↓
4. LLM GENERATES ANSWER
   Using both textual and structured context
```

## Creating a Vector Cypher Retriever

**Basic Setup:**
```python
from neo4j_graphrag.retrievers import VectorCypherRetriever

# Define a Cypher query to run after vector search
retrieval_query = """
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)-[:FILED]-(company:Company)
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
    retrieval_query=retrieval_query
)
```

**Key Components:**
- `retrieval_query`: Custom Cypher that extends vector search results
- Starts with `node` (the chunk from vector search) and `score`
- Traverses from chunks to related entities
- Returns enhanced context

## Understanding the Retrieval Query

The retrieval query runs **after** the vector search:

**What the Library Provides:**
```cypher
CALL db.index.vector.queryNodes($index_name, $top_k, $embedding)
YIELD node, score
// Your retrieval_query starts here
```

**Your Custom Query:**
```cypher
// Start from vector search results (node = Chunk, score = similarity)
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)-[:FILED]-(company:Company)
OPTIONAL MATCH (company)-[:FACES_RISK]->(risk:RiskFactor)
WITH node, score, company, collect(risk.name)[0..20] AS risks
WHERE score IS NOT NULL
RETURN
    node.text AS text,
    score,
    {company: company.name, risks: risks} AS metadata
ORDER BY score DESC
```

**What This Does:**
1. Takes the chunks found by vector search (`node`)
2. Follows relationships to find the Document
3. Finds the Company that filed the Document
4. Collects all RiskFactors the Company faces
5. Returns chunk text + company name + risk names

## Example: Finding Asset Manager Exposure

**Goal:** Find asset managers affected by specific risks.

**The Query:**
```python
asset_manager_query = """
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)-[:FILED]-(company:Company)
WITH node, company, COLLECT {
  MATCH (company)<-[:OWNS]-(manager:AssetManager)
  RETURN manager.managerName
  LIMIT 5
} AS managers
RETURN
    company.name AS company,
    managers AS AssetManagersWithSharesInCompany,
    node.text AS context
"""

vector_cypher_retriever = VectorCypherRetriever(
    driver=driver,
    index_name='chunkEmbeddings',
    embedder=embedder,
    retrieval_query=asset_manager_query
)
```

**Using It:**
```python
from neo4j_graphrag.generation import GraphRAG

rag = GraphRAG(llm=llm, retriever=vector_cypher_retriever)
response = rag.search(
    "Who are the asset managers most affected by banking regulations?",
    retriever_config={"top_k": 5}
)
print(response.answer)
```

**What Gets Retrieved:**
```
Company: BANK OF AMERICA
AssetManagers: ["BlackRock Inc.", "Vanguard", "State Street"]
Context: "...banking regulations require significant capital reserves..."

Company: WELLS FARGO
AssetManagers: ["BlackRock Inc.", "FMR LLC"]
Context: "...regulatory compliance costs have increased..."
```

The LLM can now generate an answer that specifically names the asset managers and explains their exposure.

## Example: Finding Shared Risks

**Goal:** Discover which companies share similar risk factors.

**The Query:**
```python
shared_risks_query = """
WITH node
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)-[:FILED]-(c1:Company)
MATCH (c1)-[:FACES_RISK]->(risk:RiskFactor)<-[:FACES_RISK]-(c2:Company)
WHERE c1 <> c2
WITH c1, c2, risk
RETURN
  c1.name AS source_company,
  collect(DISTINCT c2.name)[0..10] AS related_companies,
  collect(DISTINCT risk.name)[0..10] AS shared_risks
LIMIT 10
"""
```

**Results:**
```
source_company: APPLE INC
related_companies: ["MICROSOFT CORP", "NVIDIA CORPORATION"]
shared_risks: ["supply chain disruptions", "cybersecurity threats"]
```

This reveals connections between companies that face similar challenges.

## Best Practices for Retrieval Queries

**1. Always Start with `node` and `score`**
These are provided by the vector search:
```cypher
// ✓ Correct - use the provided variables
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)
RETURN node.text, score

// ✗ Wrong - don't try to redefine them
MATCH (n:Chunk) WHERE ...
```

**2. Filter NULL Scores**
Always include this to avoid errors:
```cypher
WITH node, score, company
WHERE score IS NOT NULL
RETURN ...
```

**3. Limit Collections**
Prevent unbounded arrays:
```cypher
// ✓ Correct - limit the collection
collect(risk.name)[0..20]

// ✗ Wrong - could return thousands
collect(risk.name)
```

**4. Use OPTIONAL MATCH for Missing Data**
Handle cases where relationships might not exist:
```cypher
OPTIONAL MATCH (company)-[:FACES_RISK]->(risk:RiskFactor)
```

**5. Return Structured Metadata**
Organize related data together:
```cypher
RETURN
    node.text AS text,
    score,
    {
        company: company.name,
        risks: risks,
        managers: managers
    } AS metadata
```

## When to Use Vector Cypher Retriever

**Ideal For:**
- **Relationship-aware questions:** "Which asset managers are exposed to cybersecurity risks?"
- **Entity context:** "What companies mention AI and what products do they offer?"
- **Cross-entity patterns:** "What risks are shared across tech companies?"
- **Enriched semantic search:** Basic content + structured relationships

**Examples:**
```
✓ "What asset managers own companies facing supply chain risks?"
  → Combines semantic search (supply chain) with traversal (asset managers)

✓ "What products does Microsoft mention in risk-related sections?"
  → Finds risk content (vector) + traverses to products (graph)

✓ "Which companies share risks with Apple?"
  → Semantic search for Apple + graph traversal for shared risks
```

## Comparing Retrievers

| Feature | Vector Retriever | Vector Cypher Retriever |
|---------|-----------------|-------------------------|
| Finds relevant chunks | ✓ | ✓ |
| Semantic search | ✓ | ✓ |
| Graph traversal | ✗ | ✓ |
| Returns related entities | ✗ | ✓ |
| Custom result structure | ✗ | ✓ |
| Relationship-aware | ✗ | ✓ |
| Complexity | Low | Medium |

## Controlling Results with top_k

The `top_k` parameter becomes more important with Vector Cypher:

**Without Graph Traversal:**
```
top_k=5 → 5 chunks returned
```

**With Graph Traversal:**
```
top_k=5 → 5 chunks found
          → Each traverses to entities
          → Could return 20+ result rows (5 chunks × multiple entities)
```

**Solution:** Use `LIMIT` and slicing in your Cypher query:
```cypher
collect(manager.managerName)[0..5]  -- Limit managers per company
LIMIT 10  -- Limit total rows returned
```

## Debugging Your Retrieval Query

**Test Your Query Separately:**
```cypher
// Simulate vector search results
WITH "4:abc:123" AS nodeId, 0.92 AS score
MATCH (node) WHERE elementId(node) = nodeId
// ... rest of your retrieval_query
```

**Check for Common Issues:**
- Missing `WHERE score IS NOT NULL`
- Unbounded `collect()` without slicing
- Forgetting `OPTIONAL MATCH` for nullable relationships
- Not using the `node` variable from vector search

## Check Your Understanding

### What makes Vector Cypher Retriever different from Vector Retriever?

**Options:**
- [ ] It uses a different embedding model
- [ ] It searches a different index
- [x] It adds graph traversal to vector search results
- [ ] It returns more chunks

<details>
<summary>Hint</summary>
Think about what "Cypher" adds to the retrieval process.
</details>

<details>
<summary>Show Answer</summary>
**It adds graph traversal to vector search results**. The Vector Cypher Retriever performs the same semantic search as Vector Retriever, but then executes a custom Cypher query starting from the found chunks. This allows you to traverse relationships and gather additional context from the graph.
</details>

### When should you use Vector Cypher Retriever instead of basic Vector Retriever?

**Options:**
- [ ] When you only need text content
- [x] When you need both semantic search and related entities
- [ ] When you want faster results
- [ ] When you don't have a vector index

<details>
<summary>Hint</summary>
Consider what types of questions need both content and relationships.
</details>

<details>
<summary>Show Answer</summary>
**When you need both semantic search and related entities**. Use Vector Cypher Retriever when your question requires finding relevant content (vector search) AND understanding the relationships and entities connected to that content (graph traversal). For example, finding not just chunks about risks, but also the companies and asset managers affected.
</details>

## Summary

In this lesson, you learned about the Vector Cypher Retriever:

**Key Concepts:**
- Combines vector similarity search with custom Cypher queries
- Starts with semantically similar chunks, then traverses the graph
- Returns both unstructured text and structured entities
- Provides relationship-aware context for richer answers

**How It Works:**
- Vector search finds relevant chunks
- Custom retrieval_query executes starting from those chunks
- Cypher traverses relationships to gather related data
- Returns enhanced context combining text and entities

**Best Used For:**
- Questions requiring both content and relationships
- Finding related entities from relevant chunks
- Discovering cross-entity patterns
- Enriching semantic search with structured data

**Best Practices:**
- Always use the provided `node` and `score` variables
- Filter with `WHERE score IS NOT NULL`
- Limit collections with slicing `[0..20]`
- Use `OPTIONAL MATCH` for nullable relationships
- Return structured metadata for clarity

In Lab 5 Notebook 2, you'll implement Vector Cypher Retrievers with custom queries that traverse your knowledge graph to provide rich, context-aware retrieval. In the next lesson, you'll learn about Text2Cypher Retriever for precise, fact-based queries.

---

**Navigation:**
- [← Previous: Vector Retriever](03-vector-retriever.md)
- [↑ Back to Module 2](README.md)
- [Next: Text2Cypher Retriever →](05-text2cypher-retriever.md)
