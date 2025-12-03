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


# Text2Cypher Retriever (Detailed)

Module 2, Lesson 5

**Note:** This slide will be renumbered in final sequencing

---

## From Semantic Search to Precise Queries

<div style="display: flex; gap: 2rem;">

<div style="flex: 1;">

### Vector Retriever

**Query:** "What companies are in the database?"

**Returns:** Chunks mentioning company names

**Nature:** Imprecise, content-based

</div>

<div style="flex: 1;">

### Text2Cypher Retriever

**Query:** "What companies are in the database?"

**Generates:**
```cypher
MATCH (c:Company)
RETURN c.name LIMIT 20
```

**Returns:** Actual list of company names

**Nature:** Precise, fact-based

</div>

</div>

---

## What is a Text2Cypher Retriever?

**Converts natural language to database queries** using an LLM.

**5-Step Process:**
1. Takes your natural language question
2. Uses LLM to generate Cypher based on graph schema
3. Executes the Cypher against your database
4. Returns structured results
5. Optionally formats as natural language answer

**The Power:** Query databases without writing code!

---

## How Text2Cypher Works

```
User Query: "Which company faces the most risk factors?"
    ↓
[1. ANALYZE QUERY + SCHEMA]
    LLM understands: count FACES_RISK relationships per Company
    ↓
[2. GENERATE CYPHER]
    MATCH (c:Company)-[:FACES_RISK]->(r:RiskFactor)
    WITH c, count(r) AS riskCount
    RETURN c.name, riskCount
    ORDER BY riskCount DESC LIMIT 1
    ↓
[3. EXECUTE QUERY]
    Neo4j runs the generated Cypher
    ↓
[4. RETURN RESULTS]
    Result: "APPLE INC", 45
    ↓
[5. GENERATE ANSWER]
    "Apple Inc faces the most risk factors with 45 identified risks."
```

---

## Creating a Text2Cypher Retriever

```python
from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.schema import get_schema

# Get your graph schema
schema = get_schema(driver)

# Create the retriever
text2cypher_retriever = Text2CypherRetriever(
    driver=driver,
    llm=llm,                       # LLM for Cypher generation
    neo4j_schema=schema            # Graph structure
)
```

**Key Insight:** The schema tells the LLM what's queryable!

---

## The Critical Role of Schema

**Schema tells the LLM:**

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

**Without schema:** LLM guesses (often wrong)
**With schema:** LLM knows exactly what exists (accurate queries)

---

## Example Text2Cypher Generation

**Question:** "List the top 5 asset managers by number of companies they own"

**LLM Generates:**
```cypher
MATCH (am:AssetManager)-[:OWNS]->(c:Company)
WITH am, count(c) AS companiesOwned
RETURN am.managerName, companiesOwned
ORDER BY companiesOwned DESC
LIMIT 5
```

**Result:**
```
BlackRock Inc. | 12
Vanguard Group Inc. | 11
State Street Corporation | 10
...
```

---

## Text2Cypher Best For

✅ **Precise, entity-centric questions**

✅ **When you need exact data** (numbers, dates, counts, names)

✅ **Aggregations and analytical questions**

✅ **Direct graph queries** without semantic search

**Example Queries:**
- "How many risk factors does Apple face?"
- "List all products by Microsoft"
- "Which asset manager owns the most companies?"
- "What's the average number of executives per company?"

---

## Text2Cypher Limitations

❌ **Requires good graph schema** understanding

❌ **May struggle with** ambiguous natural language

❌ **Less effective** for open-ended or exploratory questions

❌ **Cannot find content** beyond graph structure

❌ **Needs modern Cypher syntax** knowledge in LLM

**When questions don't map to schema:** Use Vector or Vector Cypher

---

## Modern Cypher Syntax Matters

**LLMs may generate deprecated syntax** if not guided:

**Old (deprecated):**
```cypher
MATCH (c:Company)-[:FACES_RISK]->(r)
RETURN c.name, collect(r.name)
```

**Modern (correct):**
```cypher
MATCH (c:Company)-[:FACES_RISK]->(r)
RETURN c.name, collect(r.name) AS risks
```

**Solution:** Use custom prompts to enforce modern Cypher syntax (covered in lesson)

---

## Customizing Text2Cypher Prompts

**Provide specific instructions to the LLM:**

```python
custom_prompt = """
Generate Cypher queries using modern syntax:
- Always use RETURN aliases
- Use COLLECT for aggregating lists
- Limit results to reasonable numbers
- No deprecated syntax
- Use WHERE instead of filtering in MATCH when possible
"""

text2cypher_retriever = Text2CypherRetriever(
    driver=driver,
    llm=llm,
    neo4j_schema=schema,
    custom_prompt=custom_prompt  # Guide LLM behavior
)
```

---

## Handling Complex Questions

**Simple Question:** "What companies are in the database?"
```cypher
MATCH (c:Company) RETURN c.name
```

**Complex Question:** "Which companies share the most risk factors?"
```cypher
MATCH (c1:Company)-[:FACES_RISK]->(r:RiskFactor)
      <-[:FACES_RISK]-(c2:Company)
WHERE c1 <> c2
WITH c1, c2, count(r) AS sharedRisks
RETURN c1.name, c2.name, sharedRisks
ORDER BY sharedRisks DESC
LIMIT 10
```

**LLM handles complexity** if schema is clear!

---

## Query Validation and Error Handling

**Text2Cypher can generate invalid queries:**

**Common Issues:**
- Syntax errors
- Non-existent property references
- Invalid relationship patterns
- Incorrect aggregations

**Best Practices:**
1. Validate generated Cypher before execution
2. Use try/catch for error handling
3. Provide error feedback to LLM for correction
4. Test with diverse questions to identify edge cases

---

## Comparison: All Three Retrievers

| Question Type | Best Retriever | Reason |
|---------------|----------------|--------|
| "What is AI safety?" | Vector | Semantic content search |
| "What AI safety risks affect companies?" | Vector Cypher | Content + related entities |
| "Which company has the most AI-related risks?" | Text2Cypher | Precise count/aggregation |
| "List all companies" | Text2Cypher | Factual enumeration |
| "Tell me about cloud computing" | Vector | Exploratory content |

---

## When Text2Cypher Fails

**Problem:** Question doesn't map to schema

**Example:**
```
Question: "What's the sentiment about AI regulation?"
Schema: Has no sentiment properties
Result: Cannot generate valid query
```

**Solution:** Use Vector retriever for content-based questions

**Problem:** Ambiguous questions

**Example:**
```
Question: "What does Apple do?"
Could mean: products, business strategy, recent activities...
LLM may generate overly generic query
```

**Solution:** Use Vector for exploratory questions

---

## Combining Retrievers in Applications

**Best Practice:** Use multiple retrievers for comprehensive coverage

**Example Agent Setup:**
1. **Schema Tool:** Understand graph structure
2. **Text2Cypher:** Answer factual questions
3. **Vector Cypher:** Provide content + context
4. **Vector:** Exploratory semantic search

**The agent chooses** the right retriever based on question type!

---

## Summary

Text2Cypher Retriever = Natural Language → Database Query

**Key Concepts:**
- LLM converts questions to Cypher
- Schema is critical for accuracy
- Returns precise, factual results
- Best for structured data queries
- May need prompt customization for modern syntax

**Best For:** Specific facts, counts, lists, aggregations

**Limitation:** Requires questions that map to graph schema

**Next:** Learn how to choose the right retriever for each question!

---

## Next Steps

In the next lesson, you will learn a decision framework for choosing between Vector, Vector Cypher, and Text2Cypher retrievers based on question patterns.

**Lab 5 Notebook 3:** Hands-on with Text2Cypher Retriever
