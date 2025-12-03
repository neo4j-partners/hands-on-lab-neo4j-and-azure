# Text2Cypher Retriever

The Text2Cypher Retriever converts natural language questions into Cypher queries, enabling precise, fact-based retrieval from your knowledge graph. Unlike vector search which finds similar content, Text2Cypher queries the graph structure directly for specific answers.

This lesson prepares you for Lab 5 Notebook 3, where you'll build Text2Cypher Retrievers that answer factual questions about your data.

## From Semantic Search to Precise Queries

**Vector Retriever:**
```
Query: "What companies are in the database?"
Returns: Chunks that mention company names (imprecise)
```

**Text2Cypher Retriever:**
```
Query: "What companies are in the database?"
Generates: MATCH (c:Company) RETURN c.name LIMIT 20
Returns: List of actual company names (precise)
```

**The Key Difference:** Text2Cypher generates database queries for exact answers, not similar content.

## What is a Text2Cypher Retriever?

A Text2Cypher Retriever:
1. Takes your natural language question
2. Uses an LLM to generate a Cypher query based on your graph schema
3. Executes the generated Cypher against your database
4. Returns the structured results
5. Optionally feeds results to an LLM for natural language answers

**The Power:** Direct database querying without writing Cypher yourself.

## How It Works

**Step-by-Step Process:**

```
User Query: "Which company faces the most risk factors?"
    ↓
1. ANALYZE QUERY + SCHEMA
   LLM understands: needs to count RiskFactor relationships per Company
    ↓
2. GENERATE CYPHER
   MATCH (c:Company)-[:FACES_RISK]->(r:RiskFactor)
   WITH c, count(r) AS riskCount
   RETURN c.name, riskCount
   ORDER BY riskCount DESC
   LIMIT 1
    ↓
3. EXECUTE QUERY
   Neo4j runs the generated Cypher
    ↓
4. RETURN RESULTS
   Result: "APPLE INC", 45
    ↓
5. GENERATE ANSWER (optional)
   "Apple Inc faces the most risk factors with 45 identified risks."
```

## Creating a Text2Cypher Retriever

**Basic Setup:**
```python
from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.schema import get_schema

# Get your graph schema
schema = get_schema(driver)

# Create the retriever
text2cypher_retriever = Text2CypherRetriever(
    driver=driver,
    llm=llm,                       # LLM for Cypher generation
    neo4j_schema=schema            # Graph schema for context
)
```

**Key Components:**
- `llm`: Language model that generates Cypher
- `neo4j_schema`: Description of your graph structure (nodes, relationships, properties)
- `driver`: Neo4j connection to execute queries

## Understanding the Schema

The schema tells the LLM what's in your graph:

**Example Schema:**
```
Node properties:
Company {name: STRING, ticker: STRING}
RiskFactor {name: STRING}
AssetManager {managerName: STRING}

Relationships:
(:Company)-[:FACES_RISK]->(:RiskFactor)
(:AssetManager)-[:OWNS]->(:Company)
(:Company)-[:FILED]->(:Document)
```

The LLM uses this to generate valid Cypher queries.

## Custom Prompts for Better Cypher

You can customize how Cypher is generated with a custom prompt:

```python
custom_prompt = """Task: Generate a Cypher statement to query a graph database.

Instructions:
- Use only the provided relationship types and properties in the schema.
- Use `WHERE toLower(node.name) CONTAINS toLower('name')` for case-insensitive name matching.
- Always add LIMIT 20 to restrict results.

Modern Cypher Requirements:
- Use `elementId(node)` instead of `id(node)`.
- Use `count{{pattern}}` instead of `size((pattern))`.
- Use `EXISTS {{MATCH pattern}}` instead of `exists((pattern))`.
- When using ORDER BY, filter NULL values first.

Schema:
{schema}

The question is:
{query_text}"""

text2cypher_retriever = Text2CypherRetriever(
    driver=driver,
    llm=llm,
    neo4j_schema=schema,
    custom_prompt=custom_prompt
)
```

**Why Custom Prompts Matter:**
- Enforce modern Cypher syntax
- Add domain-specific rules
- Improve query quality
- Handle edge cases

## Example Queries

**Finding Specific Entities:**
```python
query = "What companies are owned by BlackRock Inc?"
result = text2cypher_retriever.search(query_text=query)

# Generated Cypher:
# MATCH (am:AssetManager {managerName: 'BlackRock Inc.'})-[:OWNS]->(c:Company)
# RETURN c.name
# LIMIT 20

# Results:
# APPLE INC, MICROSOFT CORP, AMAZON, INTEL CORP, ...
```

**Counting Relationships:**
```python
query = "How many risk factors does Apple face?"
result = text2cypher_retriever.search(query_text=query)

# Generated Cypher:
# MATCH (c:Company {name: 'APPLE INC'})-[:FACES_RISK]->(r:RiskFactor)
# RETURN count(r) AS riskCount

# Result: 45
```

**Finding Top Items:**
```python
query = "Which company faces the most risk factors?"
result = text2cypher_retriever.search(query_text=query)

# Generated Cypher:
# MATCH (c:Company)-[:FACES_RISK]->(r:RiskFactor)
# WITH c, count(r) AS riskCount
# RETURN c.name, riskCount
# ORDER BY riskCount DESC
# LIMIT 1

# Result: APPLE INC, 45
```

## Using with GraphRAG

Combine Text2Cypher with LLM generation for natural language answers:

```python
from neo4j_graphrag.generation import GraphRAG

rag = GraphRAG(llm=llm, retriever=text2cypher_retriever)
response = rag.search(
    "Which company faces the most risk factors?",
    return_context=True
)

print(response.answer)
# "Apple Inc faces the most risk factors, with 45 distinct risks identified in their filings."

print(response.retriever_result.metadata["cypher"])
# Shows the generated Cypher query
```

## When to Use Text2Cypher

**Ideal For:**
- **Counting queries:** "How many companies are in the database?"
- **Specific facts:** "What products does Apple mention?"
- **Comparisons:** "Which company has the highest revenue?"
- **Filtered searches:** "List companies in the tech sector"
- **Relationship queries:** "Who owns Microsoft?"

**Example Questions:**
```
✓ "What companies are owned by BlackRock?"
✓ "How many risk factors does Apple face?"
✓ "List all asset managers"
✓ "Which company mentions AI the most?"
✓ "What products does NVIDIA sell?"
```

## When NOT to Use Text2Cypher

**Poor Fits:**
- **Semantic questions:** "What is Apple's strategy?" (use Vector Retriever)
- **Content exploration:** "Tell me about cybersecurity" (use Vector Retriever)
- **Ambiguous questions:** "What's interesting about tech companies?" (too vague)
- **Multi-hop reasoning:** "Why did Microsoft acquire LinkedIn?" (needs interpretation)

## Comparing All Three Retrievers

| Question Type | Best Retriever | Why |
|--------------|----------------|-----|
| "What are Apple's main risks?" | Vector Retriever | Semantic content about risks |
| "Which asset managers own Apple?" | Text2Cypher | Specific ownership facts |
| "What risks do Apple and Microsoft share?" | Vector Cypher | Semantic + relationship traversal |
| "How many companies face cyber risks?" | Text2Cypher | Counting + filtering |
| "Summarize Microsoft's strategy" | Vector Retriever | Finding relevant content by meaning |

## Inspecting Generated Cypher

Always review generated queries for quality:

```python
result = text2cypher_retriever.get_search_results(query)

print("Original Query:", query)
print("Generated Cypher:", result.metadata["cypher"])
print("Results:", result.records)
```

**Check For:**
- Correct node labels and relationship types
- Appropriate LIMIT clauses
- Valid property names
- Modern Cypher syntax

## Common Issues and Solutions

**Issue: LLM generates invalid Cypher**
Solution: Improve your custom prompt with examples

**Issue: Query returns too many results**
Solution: Add `LIMIT` clauses in your prompt template

**Issue: LLM uses old Cypher syntax**
Solution: Include modern syntax requirements in prompt

**Issue: Query doesn't match entity names**
Solution: Add case-insensitive matching instructions

**Example Solution:**
```python
# Add to your custom prompt:
"Use `WHERE toLower(node.name) CONTAINS toLower('search_term')` for name matching"
```

## Security Considerations

**Important:** Text2Cypher executes generated queries directly against your database.

**Best Practices:**
- Use read-only database credentials
- Implement query timeouts
- Validate generated Cypher before execution (if possible)
- Limit result sizes with LIMIT clauses
- Monitor for malicious query patterns
- Don't expose this in untrusted environments

**Production Safety:**
```python
# Add query validation
def validate_query(cypher: str) -> bool:
    # Check for dangerous keywords
    dangerous = ['DELETE', 'REMOVE', 'DETACH', 'DROP', 'CREATE', 'MERGE', 'SET']
    return not any(keyword in cypher.upper() for keyword in dangerous)
```

## Check Your Understanding

### What does the Text2Cypher Retriever do?

**Options:**
- [ ] Searches for similar text in documents
- [x] Converts natural language to Cypher queries
- [ ] Translates Cypher to English
- [ ] Generates embeddings for text

<details>
<summary>Hint</summary>
Think about what "Text2Cypher" means literally.
</details>

<details>
<summary>Show Answer</summary>
**Converts natural language to Cypher queries**. The Text2Cypher Retriever uses an LLM to transform your plain English question into a Cypher query, then executes that query against the database to get precise, structured results.
</details>

### When should you use Text2Cypher instead of Vector Retriever?

**Options:**
- [x] When you need to count specific entities or relationships
- [ ] When you want to find semantically similar content
- [ ] When you don't know what you're looking for
- [ ] When you need to search document text

<details>
<summary>Hint</summary>
Consider what kind of questions need precise database queries vs. semantic search.
</details>

<details>
<summary>Show Answer</summary>
**When you need to count specific entities or relationships**. Text2Cypher is ideal for factual, structured queries like "How many companies..." or "Which asset manager owns...". Use Vector Retriever for semantic content search like "Tell me about Apple's strategy".
</details>

## Summary

In this lesson, you learned about the Text2Cypher Retriever:

**Key Concepts:**
- Converts natural language questions into Cypher queries
- Uses LLM + graph schema to generate valid queries
- Returns precise, structured results from the database
- Best for factual questions, counts, and specific entities

**How It Works:**
- LLM analyzes question and schema
- Generates appropriate Cypher query
- Executes query against Neo4j
- Returns structured results
- Optionally formats as natural language

**Best Used For:**
- Counting entities or relationships
- Finding specific facts
- Listing entities with filters
- Querying structured data
- Precise lookups

**Key Differences:**
- Vector Retriever: Finds similar content (semantic)
- Vector Cypher: Semantic + graph traversal
- Text2Cypher: Precise queries (factual)

**Important Considerations:**
- Requires good schema definition
- Custom prompts improve quality
- Security: only use with read-only credentials
- Validate generated Cypher when possible

In Lab 5 Notebook 3, you'll implement a Text2Cypher Retriever and see how it answers factual questions about your knowledge graph. In the next lesson, you'll learn how to choose the right retriever for different types of questions.

---

**Navigation:**
- [← Previous: Vector Cypher Retriever](04-vector-cypher-retriever.md)
- [↑ Back to Module 2](README.md)
- [Next: Choosing the Right Retriever →](06-choosing-retriev

ers.md)
