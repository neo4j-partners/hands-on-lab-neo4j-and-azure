# SYNC: Aligning Azure Workshop with GraphAcademy Quality Standards

The GraphAcademy `genai-maf-context-providers` repository establishes a clear pedagogical standard: each lab states what the learner will understand before they touch code, names the limitation that motivates the next concept, and provides skeleton files that force learners to reason through the implementation rather than copy-paste. The Azure workshop covers the same ground with the same frameworks, but its notebooks tend to jump to "how" before establishing "why," and several concepts that the GraphAcademy repo explains explicitly (extraction pipelines, merge strategies, tool-vs-provider tradeoffs) remain implicit or absent.

This document tracks the specific gaps and their resolution. Labs 0-4 are out of scope.

---

## Status Overview

| Topic | GraphAcademy Lab | Azure Workshop Lab | Status |
|-------|-----------------|-------------------|--------|
| Simple Agent | Lab 1 | Lab 5, Notebook 01 | DONE |
| Context Provider Intro | Lab 2 | Lab 5, Notebook 02 | DONE |
| Vector Context Provider | Lab 3 | Lab 6, Notebook 01 | DONE |
| Graph-Enriched Provider | Lab 4 | Lab 6, Notebook 02 | DONE |
| Fulltext Context Provider | Lab 5 | Lab 6, Notebook 03 | DONE |
| Entity Extraction Pipeline | Lab 8 | Lab 7, Notebook 01 | DONE (new) |
| Memory Context Provider | Lab 7 | Lab 7, Notebook 02 | DONE |
| Memory Tools Agent | Lab 9 | Lab 7, Notebook 03 | DONE |
| Knowledge Graph Fundamentals | N/A | Lab 8 | DONE |
| Advanced Agents | N/A | Lab 9 | DONE |

---

## Changes Made

### Lab 5: Foundry Agents

**Notebook 01: Simple Agent** (`01_simple_agent.ipynb`)
- [x] Added "What you will learn" section with 4 learning objectives
- [x] Added "The Limitation of Tools" section after the experimental queries, explaining reactive vs. proactive tools
- [x] Added bridge to next concept: frames context providers as the solution
- [x] Simplified transition cell (detailed transition now in the limitation section)

**Notebook 02: Context Provider** (`02_context_provider.ipynb`)
- [x] Added "Why Context Providers?" motivation paragraph at opening
- [x] Added "What you will learn" section with 4 learning objectives
- [x] Preserved existing strengths: Tools vs Context Providers table, lifecycle diagram, cell-by-cell narrative

---

### Lab 6: Context Providers

**Notebook 01: Vector Context Provider** (`01_vector_context_provider.ipynb`)
- [x] Added "What you will learn" section with 4 learning objectives
- [x] Added conceptual example of semantic search using financial domain ("exposure to foreign currency fluctuations" matching "international revenue risk")
- [x] Added "Experiment" section with suggested queries and guidance on modifying `top_k`
- [x] Added closing transition to graph-enriched provider

**Notebook 02: Graph-Enriched Provider** (`02_graph_enriched_provider.ipynb`)
- [x] Added problem statement: "Vector search returns matching text chunks, but those chunks exist in a graph... Basic vector search discards all of that structure"
- [x] Added "What you will learn" section with 4 learning objectives
- [x] Added inline Cypher comments to retrieval query explaining each traversal step and `[0..5]` list slicing
- [x] Added "Experiment" section suggesting query modifications (asset managers, financial metrics, limit changes)
- [x] Added closing transition to fulltext provider

**Notebook 03: Fulltext Context Provider** (`03_fulltext_context_provider.ipynb`)
- [x] Added "What you will learn" section with 4 learning objectives
- [x] Added BM25 ranking explanation (term frequency, inverse document frequency)
- [x] Added explicit note that fulltext search does not require an embedder
- [x] Added Fulltext vs. Vector comparison table with strengths, weaknesses, and best-for guidance
- [x] Added "Experiment" section comparing fulltext and vector results
- [x] Added closing transition to Lab 7

---

### Lab 7: Agent Memory

**Notebook 01: Memory Context Provider** (`01_memory_context_provider.ipynb`)
- [x] Introduces agent memory basics: three memory types, passive injection, `Neo4jMicrosoftMemory`
- [x] Added "What you will learn" section with 4 learning objectives
- [x] Added memory type explanations with retrieval mechanics (short-term = semantic search, long-term = graph nodes, reasoning = task traces)
- [x] Added extraction timing explanation: "Entity extraction runs after every agent turn via the `after_run()` hook"
- [x] Added passive/active framing in closing transition

**Notebook 02: Entity Extraction Pipeline** (`02_entity_extraction.ipynb`)
- [x] Deep dive into the extraction pipeline referenced in Notebook 01
- [x] Teaches multi-stage extraction pipeline (spaCy, GLiNER, LLM fallback) with SEC 10-K entity types
- [x] Covers manual entity addition via `add_entity()` with deduplication test
- [x] Documents merge strategies (confidence, union, intersection, cascade)
- [x] Documents resolution settings (exact, fuzzy, semantic thresholds)
- [x] Uses Azure credentials via shared config modules
- [x] Created corresponding solution file `solution_srcs/07_00_entity_extraction.py`

**Notebook 03: Memory Tools Agent** (`03_memory_tools_agent.ipynb`)
- [x] Added "What you will learn" section with 4 learning objectives
- [x] Added "The Combined Pattern: Passive + Active Memory" framing at opening
- [x] Strengthened agent instructions with imperative language ("You MUST call the remember_preference tool") and concrete parameter examples
- [x] Added "Experiment" section with specific testing suggestions
- [x] Updated corresponding solution file `07_02_memory_tools_agent.py` with matching imperative instructions

**Notebook 04: Reasoning Memory** (`04_reasoning_memory.ipynb`) — NEW
- [x] Created new notebook adapted from GraphAcademy Lab 10
- [x] Teaches recording agent execution traces with `record_agent_trace()`
- [x] Demonstrates semantic search over past traces with `get_similar_traces()`
- [x] Covers tool usage statistics with `get_tool_stats()`
- [x] Includes both successful and failed trace examples
- [x] Uses Azure credentials via shared config modules

---

### Lab 8: Knowledge Graph (Quality Review)

**Notebook 01: Data and Embeddings** (`01_data_and_embeddings.ipynb`)
- [x] Added embedding model choice explanation (text-embedding-3-small vs. text-embedding-3-large cost/quality tradeoff)

**Notebook 02: GraphRAG Retrievers** (`02_graphrag_retrievers.ipynb`)
- [x] Added COLLECT subquery explanation: why the pattern prevents result set multiplication

---

### Lab 9: Advanced Agents (Quality Review)

**Notebook 01: Vector + Graph Agent** (`02_vector_graph_agent.ipynb`)
- [x] Added "What you will learn" section with 4 learning objectives
- [x] Added "Experiment" section with categorized queries (schema, document, ambiguous)
- [x] Added tools vs. context providers decision framework
- [x] Added retrieval query modification suggestions

**Notebook 02: Text2Cypher Agent** (`03_text2cypher_agent.ipynb`)
- [x] Added "What you will learn" section with 4 learning objectives
- [x] Added "Experiment" section organizing queries by tool type
- [x] Added edge case exploration prompts (invalid Cypher, ambiguous queries)

---

### Infrastructure Changes

- [x] Renamed Lab 7 notebooks: `01_memory_context_provider.ipynb` → `02_`, `02_memory_tools_agent.ipynb` → `03_`
- [x] Updated `main.py`: added entity extraction to SOLUTIONS list (option 17), renumbered memory solutions to 18-19
- [x] Updated `main.py`: adjusted menu display, choice range (0-19), and help text
- [x] Updated solution file docstrings with correct `main.py solutions` numbers (07_01 → 18, 07_02 → 19)

---

## Cross-Cutting Patterns Applied

| Pattern | Labs Applied | Status |
|---------|-------------|--------|
| Learning objectives ("What you will learn") | 5, 6, 7, 9 | DONE |
| Problem-before-solution framing | 5 (tool limitation), 6 (vector limitation, BM25 vs. semantic) | DONE |
| Closing transitions to next lab | 5, 6, 7 | DONE |
| Experimentation sections | 6, 7, 9 | DONE |
| Notebook-solution consistency | 7 (extraction config, agent instructions) | DONE |
| Inline Cypher comments | 6 (graph-enriched retrieval query) | DONE |
| Tools vs. context providers comparison | 5 (table), 9 (decision framework) | DONE |
