# Finding the Optimal Entity Resolution Config

## How It Works Today

The entity resolution pipeline has a fast iteration loop. PDF processing ran once (16 min), and we have a backup. Each test run takes about 2-3 minutes:

1. Restore database from backup (same starting point every time)
2. Export snapshot (or reuse the same snapshot — it reads from the JSON file, not Neo4j)
3. Change ER_ settings in .env
4. Run `resolve` — outputs a merge plan JSON to `logs/`
5. Compare

The snapshot file is the input for all resolution runs. Since every test starts from the same snapshot, the only variable is the .env config. No database restore needed between resolve runs — resolve reads the snapshot file and writes a merge plan. You only restore + snapshot once, then iterate on steps 3-4.

## What We're Optimizing For

The ideal config correctly merges genuine duplicates (Apple Inc = Apple) while refusing to merge distinct entities (Apple != Apple Vision Pro). Specifically:

- **All 9 CSV-seeded companies survive** with their metadata intact (ticker, CIK, CUSIP)
- **Genuine duplicates merge**: "NVIDIA Corporation" + "NVIDIA", "Amazon.com, Inc." + "Amazon", etc.
- **Distinct entities stay separate**: "Apple" vs "Apple Vision Pro", "PayPal" vs "PayPal (Europe)"
- **No false merges**: unrelated companies with similar names don't get collapsed
- **Flagged groups are genuinely ambiguous**, not obvious merges that the system is too cautious about

## The 10 Configs

Each config is named for quick reference. All use the same snapshot.

### Group A: Vary the Pre-filter Threshold (fuzzy strategy, binary mode)

These test how wide a net we cast before handing pairs to the LLM. Lower threshold = more candidate pairs = more LLM calls = more chances to find matches (but also more noise).

| # | Name | Strategy | Threshold | Confidence | Notes |
|---|------|----------|-----------|------------|-------|
| 1 | **baseline** | fuzzy | 0.6 | binary | First run config. 914 candidates, 18 LLM merges. Known-good starting point. |
| 2 | **wide-net** | fuzzy | 0.5 | binary | Catches pairs baseline misses. Are there real matches below 0.6? |
| 3 | **tight-filter** | fuzzy | 0.7 | binary | Fewer candidates, faster. Do we lose any real merges? |
| 4 | **very-wide** | fuzzy | 0.4 | binary | Maximum recall. How many more candidates? Does the LLM still reject noise? |

### Group B: Scored Confidence Mode (fuzzy strategy)

Instead of binary yes/no from the LLM, these use the confidence score to filter. A pair might be "yes, same entity" but with only 0.6 confidence — scored mode lets us set a bar.

| # | Name | Strategy | Threshold | Confidence | Conf. Threshold | Notes |
|---|------|----------|-----------|------------|-----------------|-------|
| 5 | **scored-standard** | fuzzy | 0.6 | scored | 0.8 | Same pre-filter as baseline, but LLM's low-confidence merges get blocked. |
| 6 | **scored-strict** | fuzzy | 0.6 | scored | 0.9 | Very conservative — only high-confidence merges go through. |
| 7 | **wide-scored** | fuzzy | 0.5 | scored | 0.8 | Wide net + scored. Catches more candidates but applies a quality bar. |

### Group C: Prefix Strategy

Completely different pre-filter. Instead of fuzzy string similarity, it matches when one name is a prefix of another (e.g., "Apple" is a prefix of "Apple Inc."). Different candidate set.

| # | Name | Strategy | Threshold | Confidence | Notes |
|---|------|----------|-----------|------------|-------|
| 8 | **prefix-loose** | prefix | 0.3 | binary | Low threshold catches short-prefix matches like "PG&E" / "PG&E Corporation". |
| 9 | **prefix-standard** | prefix | 0.5 | binary | Moderate threshold. How does the candidate set differ from fuzzy? |

### Group D: Structural Limit

Same pre-filter as baseline, but restricts merge group size. Forces more flagging.

| # | Name | Strategy | Threshold | Confidence | Max Group | Notes |
|---|------|----------|-----------|------------|-----------|-------|
| 10 | **small-groups** | fuzzy | 0.6 | binary | 5 | Do large groups (like Amazon's 4 variants) get flagged instead of auto-merged? |

## .env Settings for Each Config

Copy-paste into `.env` before each run. All other settings stay the same.

```bash
# Config 1: baseline
ER_PRE_FILTER_STRATEGY=fuzzy
ER_PRE_FILTER_THRESHOLD=0.6
ER_BATCH_SIZE=10
ER_CONFIDENCE_MODE=binary
ER_CONFIDENCE_THRESHOLD=0.8
ER_MAX_GROUP_SIZE=10
ER_MODEL_NAME=gpt-4o

# Config 2: wide-net
ER_PRE_FILTER_THRESHOLD=0.5

# Config 3: tight-filter
ER_PRE_FILTER_THRESHOLD=0.7

# Config 4: very-wide
ER_PRE_FILTER_THRESHOLD=0.4

# Config 5: scored-standard
ER_PRE_FILTER_THRESHOLD=0.6
ER_CONFIDENCE_MODE=scored
ER_CONFIDENCE_THRESHOLD=0.8

# Config 6: scored-strict
ER_PRE_FILTER_THRESHOLD=0.6
ER_CONFIDENCE_MODE=scored
ER_CONFIDENCE_THRESHOLD=0.9

# Config 7: wide-scored
ER_PRE_FILTER_THRESHOLD=0.5
ER_CONFIDENCE_MODE=scored
ER_CONFIDENCE_THRESHOLD=0.8

# Config 8: prefix-loose
ER_PRE_FILTER_STRATEGY=prefix
ER_PRE_FILTER_THRESHOLD=0.3
ER_CONFIDENCE_MODE=binary

# Config 9: prefix-standard
ER_PRE_FILTER_STRATEGY=prefix
ER_PRE_FILTER_THRESHOLD=0.5
ER_CONFIDENCE_MODE=binary

# Config 10: small-groups
ER_PRE_FILTER_STRATEGY=fuzzy
ER_PRE_FILTER_THRESHOLD=0.6
ER_CONFIDENCE_MODE=binary
ER_MAX_GROUP_SIZE=5
```

## Tracking and Comparing Results

### What the Code Already Does

Each `resolve` run writes a merge plan JSON to `logs/merge_plan_<timestamp>.json`. The merge plan contains:
- The full config used (pre_filter_strategy, threshold, confidence_mode, etc.)
- Total entities, candidate pair count
- Every LLM decision (merge/no_merge with reasoning)
- All merge groups (ready, flagged, needs_confirmation)

This is already a complete audit trail for each run. The problem is comparing across 10 of them.

### What's Missing: A Run Summary

Each merge plan is hundreds of lines. To compare configs side by side, we need a compact summary extracted from each merge plan. The key metrics:

| Metric | Why It Matters |
|--------|---------------|
| Candidate pairs generated | How much work the pre-filter creates |
| LLM calls made | Cost proxy (batches x batch_size) |
| Total merges (exact + LLM) | Overall aggressiveness |
| LLM merge groups (ready) | Quality signal — these are the interesting ones |
| Flagged groups | Ambiguous cases the system punted on |
| False merges (manual check) | The real quality number — requires human review |
| Missed merges (manual check) | Known duplicates the config failed to catch |

### Proposed Approach: Export a Comparison JSON

After running all 10 configs, add a `compare` command that reads all merge plans from `logs/` and writes a single comparison JSON and a readable table. The comparison file would contain one entry per run with the summary metrics above, making it trivial to sort by any column.

The comparison should also show a per-entity view: for each of the 9 canonical companies, which configs merged their duplicates correctly? This is the ground truth test.

### Ground Truth Checklist

These are the merges we know should happen (from the first run analysis):

| Expected Merge Group | Survivor | Consumed |
|----------------------|----------|----------|
| Amazon | Amazon.com, Inc. | Amazon, Amazon, Inc., Amazon.com |
| Microsoft | Microsoft Corporation | Microsoft |
| NVIDIA | NVIDIA Corporation | NVIDIA |
| Apple | Apple Inc | Apple |
| Alphabet | Alphabet Inc. | Alphabet |
| Google | Google Inc. | Google |
| Intel | Intel Corp | Intel Corporation |
| PG&E | PG&E Corporation | PG&E Corp, PG&E |
| McDonald's | McDonald's Corporation | McDonald's |

And these should NOT merge:
- Apple Inc (CSV, ticker=INTC bug) + Apple Inc (LLM-extracted) — until CSV is fixed
- PayPal Holdings + PayPal (Europe) + PayPal Pte. Ltd. — distinct subsidiaries

A config scores well if it gets all the "should merge" right and none of the "should not merge" wrong.

## Is the Code Modular Enough?

Yes. The implementation is well-structured for this kind of testing:

**What's already good:**
- `resolve()` reads from a snapshot file, not Neo4j — no database needed for testing
- All config comes from .env via Pydantic — change settings without touching code
- Pre-filters are registered in a `PRE_FILTERS` dict — adding a new strategy is one function + one dict entry
- Merge plan output is structured JSON with full audit trail
- Backup/restore makes resetting the database to pre-resolution state trivial

**What would make comparison easier (code changes needed):**
1. Add a `compare` CLI command that reads all merge plans and produces a summary table + JSON
2. Have `resolve()` return a run summary dict in addition to writing the merge plan (or extract it from the plan)
3. The summary should include a ground-truth scorecard: did each expected merge happen? Did any forbidden merge happen?

These are small additions. The core resolution logic doesn't need to change — it's the reporting layer that needs a comparison view on top of what already exists.

## Execution Plan

1. Take snapshot once (already done: `snapshot_Company_20260313_151540.json`)
2. Run configs 1-10, changing .env before each `resolve` run
3. After all 10 runs, compare merge plans
4. Pick the config that scores best on the ground truth checklist
5. Restore from backup, run that config's resolve, apply-merges, finalize
6. Verify with `verify` and `samples`
