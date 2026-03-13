# Proposal: LLM-Based Entity Resolution Module

## Design Decisions

| # | Question | Decision |
|---|----------|----------|
| 1 | Pre-filter strategy | Configurable via .env. Prototype multiple options (string similarity, embedding similarity, prefix matching). |
| 2 | LLM model | gpt-4o |
| 3 | One-pair-per-call vs. batching | Batching — send multiple candidate pairs per LLM call. |
| 4 | Chunk context inclusion | Always include source chunk text. |
| 5 | Idempotency | Not needed. Use snapshot-based workflow instead (export pre-resolution state, re-run from snapshot). |
| 6 | Scope | Company entities only for Phase 1. Other labels (RiskFactor, Product, Executive, FinancialMetric) added later. |
| 7 | Transitive group size limit | Configurable via .env. Prototype multiple thresholds. |
| 8 | Integration point | After PDF processing. Snapshot export enables repeated testing without re-running PDF ingestion. |
| 9 | Confidence scores vs. binary | Configurable via .env. Prototype both binary and confidence-scored modes. |

**Guiding principles**: Simplicity first. Cost is not a constraint. All tunable parameters configurable via .env. PDF processing runs once; entity resolution iterates cheaply against a snapshot.

## Problem Statement

The entity resolution step in our knowledge graph pipeline is destroying data instead of deduplicating it. The current `FuzzyMatchResolver` in `neo4j-graphrag-python` uses string similarity with transitive merging — if entity A fuzzy-matches B, and B fuzzy-matches C, all three collapse into one node regardless of whether A and C are actually the same thing. In our SEC 10-K pipeline, this reduced ~2,500 entities down to 121 groups and silently destroyed 7 of 9 canonical company nodes (Apple, Microsoft, PG&E, PayPal, Intel, AIG, McDonald's). Downstream RAG queries return wrong answers because Apple's document chunks now link to NVIDIA and Amazon.

String similarity cannot solve entity resolution reliably. "Apple Inc." and "Apple" are the same company. "Apple" and "Apple Vision Pro" are not. Fuzzy matching cannot tell the difference — but an LLM can.

## Proposed Solution

Build a standalone LLM-based entity resolution module that replaces the library's `FuzzyMatchResolver`. Instead of computing string similarity scores and transitively chaining matches, this module sends candidate entity pairs to an LLM and asks it to determine whether two entities refer to the same real-world thing. The LLM considers entity names, labels, properties, and the source chunk text where the entity was extracted to make a judgment call — exactly the kind of semantic reasoning that string matching fails at.

The module uses a two-phase workflow that separates expensive PDF processing from cheap, iterative entity resolution:

**Phase A — Snapshot**: After PDF processing completes, a small export module queries Neo4j for all extracted entities and their associated chunk text, then writes this to a JSON snapshot file. This snapshot captures the pre-resolution state of the graph. PDF processing only needs to run once.

**Phase B — Resolve and Apply**: The entity resolution module loads entities from the snapshot file (not from Neo4j), groups them by label, generates candidate pairs through a configurable pre-filter, sends batches to the LLM for confirmation, and outputs a merge plan. The merge plan is a structured list of confirmed merges with the LLM's reasoning. A separate apply step executes the merge plan against Neo4j. To re-test with different settings, just re-run Phase B from the same snapshot — no PDF reprocessing needed.

When merging, the module preserves the entity with the richest metadata (most properties, most relationships) as the surviving node. CSV-seeded canonical entities with known properties like ticker symbols and CIK numbers naturally survive because they carry more metadata.

## Requirements

1. The module must run standalone, independent of the `neo4j-graphrag-python` pipeline. It takes a Neo4j driver and an LLM client as inputs.

2. Phase 1 scope is Company entities only. The module must be structured so adding other label types (RiskFactor, Product, Executive, FinancialMetric) is straightforward in later phases.

3. A snapshot export module must query Neo4j after PDF processing and write all extracted entities (names, labels, properties) and their source chunk text to a JSON file. This snapshot is the input for all subsequent resolution runs.

4. The resolution module must load entities from the snapshot file, not directly from Neo4j. This enables repeated testing without re-running PDF processing.

5. The module must use a configurable pre-filter to generate candidate pairs before calling the LLM. The pre-filter strategy (string similarity, embedding similarity, etc.) and its threshold must be configurable via .env. The pre-filter nominates candidates — it does not make merge decisions.

6. Candidate pairs must be sent to the LLM in batches. Each batch contains multiple pairs. The LLM evaluates each pair independently within the batch. The LLM receives both entity names, their properties, their labels, and the source chunk text for each entity.

7. The LLM response format (binary yes/no vs. confidence-scored) must be configurable via .env. In confidence mode, a configurable threshold determines which pairs are auto-merged vs. flagged for review.

8. There must be no transitive chaining. If the LLM confirms A=B and B=C, the module must separately confirm A=C before merging all three. Each merge decision stands on its own. The maximum group size for pairwise confirmation must be configurable via .env.

9. The resolution module must output a merge plan (structured JSON) containing every merge decision — accepted and rejected — with the LLM's reasoning. The merge plan is reviewed before being applied to Neo4j.

10. A separate apply step reads the merge plan and executes merges in Neo4j. The surviving node is the one with the most properties and relationships. All labels and relationships from the consumed node transfer to the survivor.

11. The module must not merge entities that were seeded from external metadata (CSV-loaded Company nodes with ticker, cik, cusip) unless the LLM explicitly confirms the match. Seeded entities are treated as high-confidence anchors.

12. The module must use Pydantic models for all configuration and data structures.

13. All configurable parameters must be loadable from .env: pre-filter strategy, pre-filter threshold, batch size, confidence mode, confidence threshold, group size limit, LLM model name.

## Expected Outcomes

- Canonical company entities survive the resolution process intact, with their CSV-seeded metadata preserved.
- Genuine duplicates (e.g., "Apple" and "Apple Inc.", "NVIDIA" and "NVIDIA Corporation") are correctly merged.
- Unrelated entities with superficially similar names are not merged.
- RAG queries return correct results because entity-to-chunk relationships point to the right nodes.
- Every merge decision is auditable through the structured merge plan.
- Resolution can be re-run with different parameters in seconds without re-processing PDFs.

## Prototype Workflow

```
1. Run PDF processing once:
   uv run python main.py load --clear

2. Export entity snapshot:
   uv run python main.py snapshot

3. Run entity resolution (iterative — change .env settings and re-run):
   uv run python main.py resolve

4. Review merge plan:
   cat logs/merge_plan_<timestamp>.json

5. Apply merges to Neo4j:
   uv run python main.py apply-merges

6. Verify results:
   uv run python main.py verify
```

Steps 3-6 can be repeated as many times as needed. Step 1 only runs once.

## Implementation Plan

### Phase 1: Analysis
- [x] Document current entity resolution behavior and failure modes (WTF_GRAPHRAG.md)
- [x] Catalog Company entity name patterns in the SEC 10-K dataset (via snapshot — 618 entities, 181 unique names)
- [x] Define the LLM prompt structure for batched pairwise entity comparison
- [x] Define the snapshot file format (JSON schema — Pydantic EntitySnapshot model)
- [x] Define the merge plan file format (JSON schema — Pydantic MergePlan model)
- [x] Identify initial pre-filter strategies to prototype (fuzzy via rapidfuzz, prefix matching)

### Phase 2: Implementation
- [x] Build the snapshot export module (`src/snapshot.py`: Neo4j → JSON file)
- [x] Build the entity resolution module (`src/entity_resolution.py`: JSON file → merge plan)
  - [x] Pydantic config model with .env loading (ER_ prefix)
  - [x] Configurable pre-filter (fuzzy string similarity, prefix matching)
  - [x] Exact-name dedup step (auto-merges identical names without LLM)
  - [x] Batched LLM calls with structured output parsing (JSON mode)
  - [x] Configurable response format (binary vs. confidence-scored)
  - [x] Independent pairwise confirmation (no transitive chaining, 2-round confirmation)
  - [x] Merge plan output with full audit trail
- [x] Build the merge apply module (merge plan → Neo4j writes via apoc.refactor.mergeNodes)
- [x] Add CLI commands to main.py: `snapshot`, `resolve`, `apply-merges`
- [x] Update `load` command to stop after PDF processing (no entity resolution)
- [x] Update `finalize` command to skip entity resolution

### Phase 3: Verification
- [x] Run full pipeline load and export snapshot (618 Company entities, 8 PDFs)
- [x] Run resolution: 48 exact-name groups (437 auto-merges), 18 LLM-confirmed merge groups, 1 flagged (PayPal subsidiaries)
- [ ] Apply merges and verify all 9 CSV-seeded companies survive with correct metadata
- [ ] Verify genuine duplicates are merged (e.g., "Apple" and "Apple Inc." become one node)
- [ ] Verify unrelated entities are not merged (e.g., "Apple" and "Apple Vision Pro" remain separate)
- [ ] Verify document chunk relationships point to correct company nodes
- [ ] Run downstream RAG queries and confirm correct retrieval results
- [ ] Test iterative workflow: change .env parameters, re-run resolution, compare merge plans

### First Run Results (2026-03-13)

| Step | Count |
|------|-------|
| Raw Company entities | 618 |
| Unique names (after exact dedup) | 181 |
| Exact-name auto-merge groups | 48 (437 nodes consumed) |
| Fuzzy pre-filter candidate pairs | 914 |
| LLM batches (10 pairs each) | 92 + 2 confirmation rounds |
| LLM-confirmed merge groups | 18 |
| Flagged for review | 1 (PayPal regional subsidiaries) |

Key LLM merge decisions:
- Amazon.com, Inc. <- Amazon, Amazon, Inc., Amazon.com
- Microsoft Corporation <- Microsoft
- NVIDIA Corporation <- NVIDIA
- Apple Inc <- Apple
- Alphabet Inc. <- Alphabet
- Google Inc. <- Google

Flagged: PayPal, PayPal Holdings, Inc., PayPal, Inc., PayPal (Europe), PayPal Pte. Ltd. — correctly flagged because regional subsidiaries are distinct entities.

### CSV Data Bug: `Company_Filings.csv`

The LLM entity resolution correctly refused to merge "Apple Inc" (LLM-extracted, no ticker) with "Apple Inc." (CSV-seeded, ticker=INTC) because of conflicting identifiers. The root cause is bad data in `Company_Filings.csv`:

| Row | Name | CIK | Ticker | PDF | Bug |
|-----|------|-----|--------|-----|-----|
| 4 | APPLE INC | 1490054 | AAPL | 0001096906-23-001489.pdf | CIK 1490054 is not Apple (Apple is 320193) |
| 6 | APPLE INC | 320193 | **INTC** | 0000320193-23-000106.pdf | Ticker should be AAPL, not INTC (Intel's ticker) |
| 7 | INTEL CORP | 50863 | **INTL** | 000050863-23-000006.pdf | Ticker should be INTC, not INTL |

**Impact**: After entity resolution, there are two Apple Company nodes in the graph — "Apple Inc." (with wrong ticker=INTC from CSV) and "Apple Inc" (LLM-extracted, merged with "Apple"). The LLM correctly treated the conflicting ticker as a definitive negative signal and refused to merge them. Fixing the CSV data would allow these to merge properly.

**Fix**: Correct the tickers in Company_Filings.csv — row 6 should be AAPL, row 7 should be INTC.
