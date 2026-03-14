# FIX.md — Solution Issues Found

Solutions 4–20 were run via `uv run python main.py solutions <N>`. Solutions 1–3 were skipped (they are destructive data pipeline operations that clear the database).

## Status Summary

| # | Solution | Status | Notes |
|---|----------|--------|-------|
| 4 | Full Dataset Queries | FIXED | Query used wrong pattern; now uses OFFERS relationship |
| 5 | Vector Retriever | PASS | |
| 6 | Vector Cypher Retriever | PASS | |
| 7 | Text2Cypher Retriever | PASS | |
| 8 | Simple Agent | PASS | |
| 9 | Context Provider Intro | PASS | |
| 10 | Vector Graph Agent | PASS | |
| 11 | Text2Cypher Agent | PASS | |
| 12 | Fulltext Search | FIXED | Changed hybrid_search("Amazon") to hybrid_search("Alphabet") |
| 13 | Hybrid Search | PASS | |
| 14 | Fulltext Context Provider | PASS | |
| 15 | Vector Context Provider | PASS | |
| 16 | Graph-Enriched Provider | PASS | |
| 17 | Memory Context Provider | PASS (warnings) | Neo4j `created_at` property warnings (upstream) |
| 18 | Entity Extraction Pipeline | PASS | |
| 19 | Memory Tools Agent | PASS | |
| 20 | Reasoning Memory | PASS (warnings) | Neo4j `HAS_STEP` relationship warnings (upstream) |

---

## Fixed

### 1. Solution 4 — Wrong query pattern in `show_company_products`

**File:** `solution_srcs/01_04_full_dataset_queries.py`, line 121

**Problem:** Apple Inc. appeared to offer Microsoft products (Azure AI platform, Dynamics, LinkedIn, etc.). The `OFFERS` relationships were actually clean — Apple had no `OFFERS` edges to Microsoft products.

**Root cause:** `show_company_products()` used a shared-chunk co-occurrence pattern instead of the `OFFERS` relationship:

```cypher
-- Was (broken): finds products co-mentioned in the same chunk
MATCH (c:Company)-[:FROM_CHUNK]->(chunk:Chunk)<-[:FROM_CHUNK]-(p:Product)

-- Now (fixed): uses the actual OFFERS relationship
MATCH (c:Company)-[:OFFERS]->(p:Product)
```

Microsoft's 10-K mentions Apple as a competitor in the same chunk as Microsoft products. The shared-chunk join falsely associated Apple with those products.

**Fix applied:** Replaced `FROM_CHUNK` co-occurrence with direct `OFFERS` traversal. Verified Apple now shows only Apple products.

**Lab impact:** None. Searched all notebooks (`Lab_*/*.ipynb`) — no notebooks use the broken shared-chunk pattern. Other solution files (02_02, 03_02, 05_02, 06_03) already use the correct `OFFERS` relationship.

---

### 2. Solution 12 — Hybrid search returned empty results

**File:** `solution_srcs/05_01_fulltext_search.py`, line 174

**Problem:** `hybrid_search("Amazon")` returned no results silently. "Amazon" doesn't match any Company node in the fulltext index (the entity is stored as "Amazon.com, Inc.").

**Fix applied:** Changed to `hybrid_search("Alphabet")` which matches "Alphabet Inc." and returns 35 chunks.

**Lab impact:** None. No notebooks reference `hybrid_search` or "Amazon" as a search term.

---

## Minor / Upstream Issues (No Fix Needed)

### 3. Solution 17 — Neo4j `created_at` property warning

Upstream `neo4j-agent-memory` package queries `ORDER BY c.created_at` on `Conversation` nodes that don't have that property. Noisy but functional.

### 4. Solution 20 — Neo4j `HAS_STEP` relationship warning

Upstream `neo4j-agent-memory` package queries `HAS_STEP` relationship that doesn't exist on first run. Noisy but functional.

---

## Not Tested

- **Solutions 1–3** (Data Loading, Embeddings, Entity Extraction): Destructive — they clear and reload the database. Skipped to preserve existing data.
