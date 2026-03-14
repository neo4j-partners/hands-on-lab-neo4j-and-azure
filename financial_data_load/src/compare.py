"""Compare entity resolution runs and score against ground truth.

Reads merge plan JSON files from logs/ and produces:
- A per-run summary with key metrics
- Ground truth scoring (expected merges hit, forbidden merges avoided)
- A comparison JSON and readable table
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


# ---------------------------------------------------------------------------
# Ground truth definitions
# ---------------------------------------------------------------------------

# Expected merges: each entry is a set of entity names that should end up
# in the same merge group. The first name is the expected survivor (richest
# metadata), but we score on group membership, not survivor choice.
EXPECTED_MERGES: list[dict[str, Any]] = [
    {
        "label": "Amazon",
        "names": {"Amazon.com, Inc.", "Amazon", "Amazon, Inc.", "Amazon.com"},
    },
    {
        "label": "Microsoft",
        "names": {"Microsoft Corporation", "Microsoft"},
    },
    {
        "label": "NVIDIA",
        "names": {"NVIDIA Corporation", "NVIDIA"},
    },
    {
        "label": "Apple",
        "names": {"Apple Inc.", "Apple Inc", "Apple"},
    },
    {
        "label": "Alphabet",
        "names": {"Alphabet Inc.", "Alphabet"},
    },
    {
        "label": "Google",
        "names": {"Google Inc.", "Google"},
    },
]

# Forbidden merges: pairs of entity names that must NOT end up in the same
# merge group. Each entry has a reason explaining why.
FORBIDDEN_MERGES: list[dict[str, Any]] = [
    {
        "label": "PayPal vs Europe sub",
        "pair": ("PayPal", "PayPal (Europe)"),
        "reason": "Regional subsidiary is a distinct legal entity",
    },
    {
        "label": "PayPal vs Singapore sub",
        "pair": ("PayPal", "PayPal Pte. Ltd."),
        "reason": "Regional subsidiary is a distinct legal entity",
    },
    {
        "label": "Microsoft vs Mobile Oy",
        "pair": ("Microsoft Corporation", "Microsoft Mobile Oy"),
        "reason": "Microsoft Mobile Oy is a separate Finnish subsidiary",
    },
    {
        "label": "Microsoft vs Bing",
        "pair": ("Microsoft Corporation", "Microsoft's Bing"),
        "reason": "Bing is a product, not the company itself",
    },
]


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


class GroundTruthResult(BaseModel):
    label: str
    passed: bool
    detail: str


class RunSummary(BaseModel):
    plan_file: str
    created_at: str
    config: dict[str, Any]
    total_entities: int
    candidate_pairs: int
    llm_decisions: int
    llm_merges: int
    llm_no_merges: int
    exact_name_groups: int
    exact_name_consumed: int
    llm_merge_groups: int
    llm_consumed: int
    flagged_groups: int
    needs_confirmation_groups: int
    expected_merges: list[GroundTruthResult]
    expected_merge_score: str
    forbidden_merges: list[GroundTruthResult]
    forbidden_merge_score: str
    overall_score: str


class Comparison(BaseModel):
    generated_at: str
    runs: list[RunSummary]


# ---------------------------------------------------------------------------
# Merge group analysis
# ---------------------------------------------------------------------------


def _extract_all_merge_groups(plan: dict) -> list[set[str]]:
    """Extract name-based merge groups from a plan (ready status only).

    Returns a list of sets, where each set contains the names of all entities
    in a merge group (survivor + consumed).
    """
    groups = []
    for g in plan.get("merge_groups", []):
        if g["status"] != "ready":
            continue
        names = set()
        if "survivor" in g:
            names.add(g["survivor"]["name"])
        for c in g.get("consumed", []):
            names.add(c["name"])
        if len(names) > 1:
            groups.append(names)
    return groups


def _names_share_group(name_a: str, name_b: str, groups: list[set[str]]) -> bool:
    """Check if two entity names end up in the same merge group."""
    for group in groups:
        if name_a in group and name_b in group:
            return True
    return False


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def _score_expected_merges(groups: list[set[str]]) -> list[GroundTruthResult]:
    """Score each expected merge: did all expected names land in one group?"""
    results = []
    for expected in EXPECTED_MERGES:
        label = expected["label"]
        names = expected["names"]

        # Find which groups contain any of the expected names
        matching_groups = []
        for group in groups:
            overlap = names & group
            if overlap:
                matching_groups.append((group, overlap))

        if not matching_groups:
            results.append(GroundTruthResult(
                label=label,
                passed=False,
                detail=f"No merge group contains any of: {sorted(names)}",
            ))
            continue

        # All expected names should be in a single group
        all_found = set()
        for group, overlap in matching_groups:
            all_found |= overlap

        missing = names - all_found
        if missing:
            results.append(GroundTruthResult(
                label=label,
                passed=False,
                detail=f"Missing from merge groups: {sorted(missing)}",
            ))
        elif len(matching_groups) > 1:
            results.append(GroundTruthResult(
                label=label,
                passed=False,
                detail=f"Expected names split across {len(matching_groups)} groups",
            ))
        else:
            results.append(GroundTruthResult(
                label=label,
                passed=True,
                detail="All names in one merge group",
            ))

    return results


def _score_forbidden_merges(groups: list[set[str]]) -> list[GroundTruthResult]:
    """Score each forbidden merge: did the two names stay in separate groups?"""
    results = []
    for forbidden in FORBIDDEN_MERGES:
        label = forbidden["label"]
        name_a, name_b = forbidden["pair"]

        if _names_share_group(name_a, name_b, groups):
            results.append(GroundTruthResult(
                label=label,
                passed=False,
                detail=f"WRONGLY MERGED: {name_a!r} + {name_b!r} ({forbidden['reason']})",
            ))
        else:
            results.append(GroundTruthResult(
                label=label,
                passed=True,
                detail=f"Correctly kept separate: {name_a!r} / {name_b!r}",
            ))

    return results


# ---------------------------------------------------------------------------
# Run summary extraction
# ---------------------------------------------------------------------------


def summarize_plan(plan_path: Path) -> RunSummary:
    """Extract a summary and ground truth score from a single merge plan."""
    plan = json.loads(plan_path.read_text())

    # Count decisions
    decisions = plan.get("decisions", [])
    merges = sum(1 for d in decisions if d["decision"] == "merge")
    no_merges = len(decisions) - merges

    # Count merge groups by type
    merge_groups = plan.get("merge_groups", [])
    exact_groups = [g for g in merge_groups if g.get("merge_type") == "exact_name" and g["status"] == "ready"]
    llm_groups = [g for g in merge_groups if g.get("merge_type") != "exact_name" and g["status"] == "ready"]
    flagged = [g for g in merge_groups if g["status"] == "flagged"]
    needs_confirm = [g for g in merge_groups if g["status"] == "needs_confirmation"]

    exact_consumed = sum(len(g.get("consumed", [])) for g in exact_groups)
    llm_consumed = sum(len(g.get("consumed", [])) for g in llm_groups)

    # Ground truth scoring
    all_groups = _extract_all_merge_groups(plan)
    expected_results = _score_expected_merges(all_groups)
    forbidden_results = _score_forbidden_merges(all_groups)

    expected_pass = sum(1 for r in expected_results if r.passed)
    forbidden_pass = sum(1 for r in forbidden_results if r.passed)

    return RunSummary(
        plan_file=plan_path.name,
        created_at=plan.get("created_at", ""),
        config=plan.get("config", {}),
        total_entities=plan.get("total_entities", 0),
        candidate_pairs=plan.get("candidate_pairs", 0),
        llm_decisions=len(decisions),
        llm_merges=merges,
        llm_no_merges=no_merges,
        exact_name_groups=len(exact_groups),
        exact_name_consumed=exact_consumed,
        llm_merge_groups=len(llm_groups),
        llm_consumed=llm_consumed,
        flagged_groups=len(flagged),
        needs_confirmation_groups=len(needs_confirm),
        expected_merges=expected_results,
        expected_merge_score=f"{expected_pass}/{len(expected_results)}",
        forbidden_merges=forbidden_results,
        forbidden_merge_score=f"{forbidden_pass}/{len(forbidden_results)}",
        overall_score=f"{expected_pass + forbidden_pass}/{len(expected_results) + len(forbidden_results)}",
    )


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------


def compare_runs(plan_paths: list[Path] | None = None) -> Path:
    """Compare multiple merge plan runs. Returns path to comparison JSON."""
    if plan_paths is None:
        plan_paths = sorted(LOG_DIR.glob("merge_plan_*.json"))

    if not plan_paths:
        print("No merge plans found in logs/.")
        return LOG_DIR / "comparison.json"

    summaries = []
    for path in plan_paths:
        try:
            summaries.append(summarize_plan(path))
        except Exception as e:
            print(f"  Skipping {path.name}: {e}")

    if not summaries:
        print("No valid merge plans to compare.")
        return LOG_DIR / "comparison.json"

    # Sort by overall score descending, then by timestamp
    summaries.sort(
        key=lambda s: (
            -int(s.overall_score.split("/")[0]),
            -int(s.expected_merge_score.split("/")[0]),
            s.created_at,
        )
    )

    comparison = Comparison(
        generated_at=datetime.now().isoformat(),
        runs=summaries,
    )

    # Write comparison JSON
    output_path = LOG_DIR / f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path.write_text(comparison.model_dump_json(indent=2))

    # Print readable table
    _print_comparison_table(summaries)
    _print_ground_truth_detail(summaries)

    print(f"\nComparison saved: {output_path}")
    return output_path


def _print_comparison_table(summaries: list[RunSummary]) -> None:
    """Print a compact comparison table to stdout."""
    # Header
    print()
    print("=" * 120)
    print("ENTITY RESOLUTION CONFIG COMPARISON")
    print("=" * 120)
    print()
    print(
        f"{'Plan':<36} {'Strategy':<8} {'Thresh':>6} {'Conf':>7} "
        f"{'Cands':>6} {'LLM+':>5} {'LLM-':>5} "
        f"{'Groups':>6} {'Flag':>5} "
        f"{'Expect':>7} {'Forbid':>7} {'Score':>6}"
    )
    print("-" * 120)

    for s in summaries:
        conf = s.config.get("confidence_mode", "binary")
        if conf == "scored":
            conf = f"s@{s.config.get('confidence_threshold', 0.8)}"

        print(
            f"{s.plan_file:<36} "
            f"{s.config.get('pre_filter_strategy', '?'):<8} "
            f"{s.config.get('pre_filter_threshold', '?'):>6} "
            f"{conf:>7} "
            f"{s.candidate_pairs:>6} "
            f"{s.llm_merges:>5} "
            f"{s.llm_no_merges:>5} "
            f"{s.llm_merge_groups:>6} "
            f"{s.flagged_groups + s.needs_confirmation_groups:>5} "
            f"{s.expected_merge_score:>7} "
            f"{s.forbidden_merge_score:>7} "
            f"{s.overall_score:>6}"
        )

    print()
    print("Columns: Strategy=pre-filter, Thresh=pre-filter threshold, Conf=confidence mode,")
    print("         Cands=candidate pairs, LLM+=merge decisions, LLM-=no_merge decisions,")
    print("         Groups=LLM merge groups, Flag=flagged+needs_confirmation,")
    print("         Expect=expected merges found, Forbid=forbidden merges avoided, Score=total")


def _print_ground_truth_detail(summaries: list[RunSummary]) -> None:
    """Print per-run ground truth detail."""
    print()
    print("=" * 120)
    print("GROUND TRUTH DETAIL")
    print("=" * 120)

    for s in summaries:
        print(f"\n--- {s.plan_file} (score: {s.overall_score}) ---")

        print("  Expected merges:")
        for r in s.expected_merges:
            status = "PASS" if r.passed else "FAIL"
            print(f"    [{status}] {r.label}: {r.detail}")

        print("  Forbidden merges:")
        for r in s.forbidden_merges:
            status = "PASS" if r.passed else "FAIL"
            print(f"    [{status}] {r.label}: {r.detail}")
