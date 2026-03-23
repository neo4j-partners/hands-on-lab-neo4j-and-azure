# Known Issues

## 1. Text2Cypher Token Overflow (Intermittent)

**Affects:** Solution 7 (`02_03_text2cypher_retriever.py`), Solution 11 (`03_03_text2cypher_agent.py`)

**Symptom:** `context_length_exceeded` error (318k tokens vs 272k limit) when the LLM generates Cypher that returns `Chunk.embedding` (a 1536-float vector per row).

**Root cause:** `get_schema(driver)` exposes `Chunk {index: INTEGER, text: STRING, embedding: LIST}` to the LLM. The LLM sometimes generates Cypher that selects chunk nodes with all properties, including the large embedding vectors. When many chunks are returned, the serialized embeddings exceed the model's context window.

**Reproducibility:** Intermittent. Depends on what Cypher the LLM generates. Broad queries like "Summarise the products mentioned in the company filings" are most likely to trigger it.

**Fix options (pick one or both):**

### Option A: Add prompt instruction (simple)

Add to `TEXT2CYPHER_PROMPT` and `CYPHER_PROMPT` in the affected files:

```
- NEVER return or select the Chunk.embedding property — it contains large binary vector data that will exceed context limits.
- When returning Chunk data, only select specific properties like text and index.
```

Files to update:
- `solution_srcs/02_03_text2cypher_retriever.py` — `TEXT2CYPHER_PROMPT`
- `solution_srcs/03_03_text2cypher_agent.py` — `CYPHER_PROMPT`
- `Lab_9_Advanced_Agents/03_text2cypher_agent.ipynb` — cell 9

### Option B: Filter schema before passing to Text2Cypher (robust)

Strip the `embedding` property from the schema string before passing it to `Text2CypherRetriever`. This prevents the LLM from ever seeing it:

```python
schema = get_schema(driver)
# Remove embedding property from schema to prevent LLM from selecting it
schema = schema.replace(", embedding: LIST", "")
```

Files to update: same as Option A, at the point where `get_schema()` is called.

**Recommendation:** Do both. Option B prevents the LLM from knowing about the property; Option A acts as a safety net for any other large properties.
