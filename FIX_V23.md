# FIX_V23.md - Mismatches Between Labs and Solutions

This document details all mismatches found between the Lab notebooks (3, 5, 6, 7) and their corresponding solution files.

---

## Fix Status Summary

| # | Issue | Status |
|---|-------|--------|
| 1 | RETRIEVAL_QUERY grouping in 05_02_hybrid_search.py | FIXED |
| 2 | SHARED_RISKS_QUERY grouping in 02_02_vector_cypher_retriever.py | FIXED |
| 3 | Null filtering + modern Cypher in 01_03_entity_extraction.py | FIXED |
| 4 | Error handling in Lab 6 notebooks (02, 03) | FIXED |
| 5 | Streaming in 03_01_simple_agent.py | FIXED |
| 6 | Duplicate get_llm() in 02_01_vector_retriever.py | FIXED |
| 7 | Agent instructions in 03_03_text2cypher_agent.py | FIXED |
| 8 | Relationship direction in 01_03_entity_extraction.py | FIXED |
| 9 | TEXT2CYPHER_PROMPT name filter bug (0 results issue) | FIXED |

---

## Lab 3: Graph Building

### 03_entity_extraction.ipynb vs 01_03_entity_extraction.py

#### 1. Cypher Query Style Mismatch in `show_entities()` - FIXED

**Original Issue**: Solution used older WHERE clause style instead of modern label expressions.

**Fix Applied**: Updated solution to use modern label expression syntax:
```python
MATCH (n:Company|Product|Service)
WITH labels(n)[0] as label
RETURN label, count(*) as count
```

---

#### 2. Null Filtering Mismatch in `show_entities()` - FIXED

**Original Issue**: Solution did not filter nulls before ORDER BY.

**Fix Applied**: Added null filtering to solution:
```python
MATCH (n:{label})
WHERE n.name IS NOT NULL
RETURN n.name as name
ORDER BY n.name
```

---

#### 3. Relationship Direction in `find_chunks_for_entity()` - FIXED

**Original Issue**: Solution tried both directions with fallback, differing from notebook.

**Fix Applied**: Updated solution to use single direction matching notebook:
```python
MATCH (e)-[:FROM_CHUNK]->(c:Chunk)
WHERE e.name CONTAINS $name
```

---

## Lab 5: GraphRAG Retrievers

### 01_vector_retriever.ipynb vs 02_01_vector_retriever.py

#### 1. LLM Initialization Duplication - FIXED

**Original Issue**: Solution defined its own local `get_llm()` function duplicating config.py.

**Fix Applied**: Removed local function and now imports from config:
```python
from config import get_embedder, get_neo4j_driver, get_llm
```

---

### 02_vector_cypher_retriever.ipynb vs 02_02_vector_cypher_retriever.py

#### 1. Explicit Grouping Before Aggregation - FIXED

**Original Issue**: Solution `SHARED_RISKS_QUERY` lacked explicit grouping before aggregation.

**Fix Applied**: Added explicit WITH grouping to solution:
```python
WITH node
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)-[:FILED]-(c1:Company)
MATCH (c1)-[:FACES_RISK]->(risk:RiskFactor)<-[:FACES_RISK]-(c2:Company)
WHERE c1 <> c2
WITH c1, c2, risk  # <-- Added explicit grouping
RETURN
  c1.name AS source_company,
  collect(DISTINCT c2.name)[0..10] AS related_companies,
  collect(DISTINCT risk.name)[0..10] AS shared_risks
LIMIT 10
```

---

## Lab 6: Agents

### 01_simple_agent.ipynb vs 03_01_simple_agent.py

#### 1. Streaming vs Non-Streaming Response - FIXED

**Original Issue**: Solution used non-streaming while notebook demonstrated streaming.

**Fix Applied**: Updated solution to use streaming:
```python
print("Assistant: ", end="", flush=True)
async for update in agent.run_stream(query):
    if update.text:
        print(update.text, end="", flush=True)
print("\n")
```

---

### 02_vector_graph_agent.ipynb vs 03_02_vector_graph_agent.py

#### 1. Missing Error Handling in Notebook - FIXED

**Original Issue**: Notebook `retrieve_financial_documents` lacked try/except.

**Fix Applied**: Added error handling to notebook:
```python
def retrieve_financial_documents(...) -> str:
    try:
        results = vector_retriever.search(query_text=query, top_k=3)
        if not results.items:
            return "No documents found matching the query."
        return "\n\n".join(item.content for item in results.items)
    except Exception as e:
        return f"Error searching documents: {e}"
```

---

### 03_text2cypher_agent.ipynb vs 03_03_text2cypher_agent.py

#### 1. Agent Instructions Differ - FIXED

**Original Issue**: Solution had shorter instructions missing guidance about using returned data.

**Fix Applied**: Added the extra instruction to solution:
```python
"Choose the appropriate tool based on the question type. "
"When a tool returns data, use that data to answer the question directly."
```

---

#### 2. Missing Error Handling in Notebook - FIXED

**Original Issue**: Notebook `query_database` and `retrieve_financial_documents` lacked try/except.

**Fix Applied**: Added error handling to both tool functions in notebook.

---

## Lab 7: Hybrid Search

### 02_hybrid_search.ipynb vs 05_02_hybrid_search.py

#### 1. RETRIEVAL_QUERY Grouping Mismatch - FIXED

**Original Issue**: Solution lacked explicit grouping before aggregation.

**Fix Applied**: Added explicit WITH grouping to solution:
```python
// Explicit grouping before aggregations for modern Cypher compliance
WITH node.text AS text, score, company.name AS company, doc.path AS document, risk, product

// Return enriched results
RETURN text,
       score,
       company,
       document,
       collect(DISTINCT risk.name)[0..3] AS risks,
       collect(DISTINCT product.name)[0..3] AS products
```

---

## Summary of All Fixes Applied

| Lab | File | Issue | Fix |
|-----|------|-------|-----|
| 3 | 01_03_entity_extraction.py | Cypher syntax style | Updated to modern label expressions |
| 3 | 01_03_entity_extraction.py | Null filtering | Added WHERE n.name IS NOT NULL |
| 3 | 01_03_entity_extraction.py | Relationship direction | Simplified to match notebook |
| 5 | 02_01_vector_retriever.py | Duplicate get_llm() | Removed, now uses config import |
| 5 | 02_02_vector_cypher_retriever.py | Missing grouping | Added WITH clause before RETURN |
| 6 | 03_01_simple_agent.py | Non-streaming | Updated to use run_stream() |
| 6 | 02_vector_graph_agent.ipynb | Missing error handling | Added try/except |
| 6 | 03_text2cypher_agent.ipynb | Missing error handling | Added try/except to both tools |
| 6 | 03_03_text2cypher_agent.py | Instructions differ | Added missing sentence |
| 7 | 05_02_hybrid_search.py | Missing grouping | Added WITH clause before RETURN |

---

## Additional Fix: TEXT2CYPHER_PROMPT Name Filter Bug

### Issue Discovered During Testing

**Problem**: Running `uv run new-workshops/main.py 7` showed "Number of results returned: 0" but still returned an answer.

**Root Cause**: The TEXT2CYPHER_PROMPT contained this instruction:
```
- Use `WHERE toLower(node.name) CONTAINS toLower('name')` to filter nodes by name.
```

The LLM was literally copying `toLower('name')` into generated Cypher, searching for entities with "name" in their name, which returned 0 results. The LLM then fell back to general knowledge to answer the question.

**Fix Applied**: Updated the prompt to be clearer about when to apply name filtering:
```
- Only filter by name when a specific entity name is mentioned in the question.
  When filtering by name, use case-insensitive matching:
  `WHERE toLower(node.name) CONTAINS toLower('ActualEntityName')`
- Do NOT add name filters if no specific entity name is mentioned in the question.
```

**Files Updated**:
- `02_03_text2cypher_retriever.py` - Fixed prompt + added warning when 0 results
- `03_03_text2cypher_agent.py` - Fixed prompt
- `Lab_5_GraphRAG_Retrievers/03_text2cypher_retriever.ipynb` - Fixed prompt
- `Lab_6_Agents/03_text2cypher_agent.ipynb` - Fixed prompt

---

## Files Modified

### Solutions (new-workshops/solutions/)
- `01_03_entity_extraction.py` - Modern Cypher syntax, null filtering, relationship direction
- `02_01_vector_retriever.py` - Removed duplicate get_llm()
- `02_02_vector_cypher_retriever.py` - Added explicit Cypher grouping
- `02_03_text2cypher_retriever.py` - Fixed TEXT2CYPHER_PROMPT, added 0-results warning
- `03_01_simple_agent.py` - Added streaming output
- `03_03_text2cypher_agent.py` - Added missing instruction, fixed CYPHER_PROMPT
- `05_02_hybrid_search.py` - Added explicit Cypher grouping

### Notebooks (Lab_5_GraphRAG_Retrievers/)
- `03_text2cypher_retriever.ipynb` - Fixed TEXT2CYPHER_PROMPT

### Notebooks (Lab_6_Agents/)
- `02_vector_graph_agent.ipynb` - Added try/except to retrieve_financial_documents
- `03_text2cypher_agent.ipynb` - Added try/except to both tool functions, fixed cypher_prompt

---

*Generated: 2025-12-02*
*All issues fixed: 2025-12-02*
