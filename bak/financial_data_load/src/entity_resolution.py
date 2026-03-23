"""LLM-based entity resolution module.

Replaces neo4j-graphrag-python's FuzzyMatchResolver with LLM-powered
pairwise entity comparison. Operates on snapshot files for iterative testing.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from .snapshot import EntitySnapshot, SnapshotEntity, SNAPSHOT_DIR

logger = logging.getLogger(__name__)

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class EntityResolutionConfig(BaseSettings):
    """Entity resolution settings loaded from .env (ER_ prefix)."""

    model_config = SettingsConfigDict(env_prefix="ER_", extra="ignore")

    pre_filter_strategy: str = "fuzzy"
    pre_filter_threshold: float = 0.6
    batch_size: int = 10
    confidence_mode: str = "binary"
    confidence_threshold: float = 0.8
    max_group_size: int = 10
    model_name: str = "gpt-4o"


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


class CandidatePair(BaseModel):
    entity_a: SnapshotEntity
    entity_b: SnapshotEntity
    pre_filter_score: float


class MergeDecision(BaseModel):
    entity_a_name: str
    entity_a_element_id: str
    entity_b_name: str
    entity_b_element_id: str
    decision: str  # "merge" or "no_merge"
    confidence: float | None = None
    reasoning: str


class MergePlan(BaseModel):
    created_at: str
    snapshot_path: str
    config: dict[str, Any]
    total_entities: int
    candidate_pairs: int
    decisions: list[MergeDecision]
    merge_groups: list[dict[str, Any]]


# ---------------------------------------------------------------------------
# Pre-filters
# ---------------------------------------------------------------------------


def _fuzzy_pre_filter(
    entities: list[SnapshotEntity],
    threshold: float,
) -> list[CandidatePair]:
    """Generate candidate pairs using fuzzy string similarity."""
    from rapidfuzz import fuzz, utils

    pairs = []
    for i, a in enumerate(entities):
        for b in entities[i + 1 :]:
            score = fuzz.WRatio(a.name, b.name, processor=utils.default_process) / 100
            if score >= threshold:
                pairs.append(
                    CandidatePair(entity_a=a, entity_b=b, pre_filter_score=score)
                )
    return pairs


def _prefix_pre_filter(
    entities: list[SnapshotEntity],
    threshold: float,
) -> list[CandidatePair]:
    """Generate candidate pairs where one name is a prefix of another."""
    pairs = []
    for i, a in enumerate(entities):
        for b in entities[i + 1 :]:
            a_lower = a.name.lower().strip()
            b_lower = b.name.lower().strip()
            if a_lower.startswith(b_lower) or b_lower.startswith(a_lower):
                score = min(len(a_lower), len(b_lower)) / max(
                    len(a_lower), len(b_lower), 1
                )
                if score >= threshold:
                    pairs.append(
                        CandidatePair(entity_a=a, entity_b=b, pre_filter_score=score)
                    )
    return pairs


PRE_FILTERS = {
    "fuzzy": _fuzzy_pre_filter,
    "prefix": _prefix_pre_filter,
}


# ---------------------------------------------------------------------------
# Exact dedup (same-name entities merged without LLM)
# ---------------------------------------------------------------------------


def _exact_dedup(
    entities: list[SnapshotEntity],
) -> tuple[list[SnapshotEntity], list[dict[str, Any]]]:
    """Group entities by exact name. Returns (unique survivors, auto-merge groups).

    Entities with identical names are auto-merged (no LLM needed).
    The survivor in each group is the entity with the most properties/relationships.
    """
    by_name: dict[str, list[SnapshotEntity]] = defaultdict(list)
    for e in entities:
        by_name[e.name].append(e)

    survivors = []
    auto_groups = []

    for name, group in by_name.items():
        # Pick richest entity as survivor
        survivor = max(
            group,
            key=lambda e: (
                len([v for v in e.properties.values() if v]),
                e.relationship_count,
            ),
        )
        survivors.append(survivor)

        if len(group) > 1:
            consumed = [e for e in group if e.element_id != survivor.element_id]
            auto_groups.append(
                {
                    "status": "ready",
                    "merge_type": "exact_name",
                    "survivor": {
                        "element_id": survivor.element_id,
                        "name": survivor.name,
                    },
                    "consumed": [
                        {"element_id": e.element_id, "name": e.name}
                        for e in consumed
                    ],
                }
            )

    return survivors, auto_groups


# ---------------------------------------------------------------------------
# LLM client and prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an entity resolution expert for a knowledge graph built from SEC 10-K \
financial filings.

For each pair of entities, determine whether they refer to the same real-world entity.

Rules:
- "Apple Inc." and "Apple" (same company) → same_entity: true
- "Apple" and "Apple Vision Pro" (company vs product) → same_entity: false
- Matching ticker symbols or CIK numbers are definitive positive signals.
- Conflicting ticker symbols or CIK numbers are definitive negative signals.
- Generic names like "Competitor", "Our business", "Banks" should NOT match \
named entities.
- When uncertain, return same_entity: false. It is better to keep duplicates \
than to incorrectly merge distinct entities.

Return JSON: {"decisions": [{"pair_index": N, "same_entity": bool, \
"confidence": float, "reasoning": "..."}]}"""


def _create_llm_client():
    """Create an OpenAI client using the same credentials as the pipeline."""
    from openai import OpenAI

    from .config import AgentConfig, get_azure_token

    agent_config = AgentConfig()
    if agent_config.use_openai:
        return OpenAI(api_key=agent_config.openai_api_key)
    token = get_azure_token()
    return OpenAI(base_url=agent_config.inference_endpoint, api_key=token)


def _format_entity(entity: SnapshotEntity) -> str:
    """Format an entity for the LLM prompt."""
    props = {
        k: v
        for k, v in entity.properties.items()
        if k != "name" and v is not None and v != ""
    }
    props_str = (
        ", ".join(f"{k}={v}" for k, v in props.items()) if props else "(none)"
    )
    chunks = entity.source_chunks[:2]
    chunk_str = (
        " | ".join(c[:300] for c in chunks) if chunks else "(no source text)"
    )
    label_str = ", ".join(l for l in entity.labels if not l.startswith("__"))
    return (
        f'"{entity.name}" [{label_str}]\n'
        f"    Properties: {props_str}\n"
        f"    Source text: {chunk_str}"
    )


def _build_batch_prompt(pairs: list[CandidatePair]) -> str:
    """Build the user prompt for a batch of candidate pairs."""
    lines = []
    for i, pair in enumerate(pairs, 1):
        lines.append(f"Pair {i}:")
        lines.append(f"  Entity A: {_format_entity(pair.entity_a)}")
        lines.append(f"  Entity B: {_format_entity(pair.entity_b)}")
        lines.append("")
    return "\n".join(lines)


def _call_llm_batch(
    pairs: list[CandidatePair],
    config: EntityResolutionConfig,
    client,
) -> list[MergeDecision]:
    """Send a batch of candidate pairs to the LLM and parse decisions."""
    prompt = _build_batch_prompt(pairs)

    try:
        response = client.chat.completions.create(
            model=config.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        result = json.loads(response.choices[0].message.content)
        decisions_raw = result.get("decisions", [])
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        logger.error(f"Failed to parse LLM response: {e}")
        return []
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return []

    decisions = []
    for d in decisions_raw:
        idx = d.get("pair_index", 0) - 1
        if idx < 0 or idx >= len(pairs):
            logger.warning(f"LLM returned invalid pair_index: {d.get('pair_index')}")
            continue

        pair = pairs[idx]
        same_entity = d.get("same_entity", False)
        confidence = d.get("confidence", 1.0 if same_entity else 0.0)

        # Apply confidence mode
        if config.confidence_mode == "scored":
            is_merge = same_entity and confidence >= config.confidence_threshold
        else:
            is_merge = same_entity

        decisions.append(
            MergeDecision(
                entity_a_name=pair.entity_a.name,
                entity_a_element_id=pair.entity_a.element_id,
                entity_b_name=pair.entity_b.name,
                entity_b_element_id=pair.entity_b.element_id,
                decision="merge" if is_merge else "no_merge",
                confidence=confidence,
                reasoning=d.get("reasoning", ""),
            )
        )

    return decisions


# ---------------------------------------------------------------------------
# Merge group builder
# ---------------------------------------------------------------------------


def _build_merge_groups(
    decisions: list[MergeDecision],
    entities: list[SnapshotEntity],
    max_group_size: int,
) -> list[dict[str, Any]]:
    """Build merge groups from confirmed decisions, enforcing pairwise confirmation."""
    confirmed = [
        (d.entity_a_element_id, d.entity_b_element_id)
        for d in decisions
        if d.decision == "merge"
    ]

    if not confirmed:
        return []

    entity_map = {e.element_id: e for e in entities}

    # Union-find for connected components
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: str, y: str) -> None:
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py

    for a_id, b_id in confirmed:
        union(a_id, b_id)

    # Group by component
    components: dict[str, list[str]] = {}
    for node_id in parent:
        root = find(node_id)
        components.setdefault(root, []).append(node_id)

    # Set of confirmed pairs for lookup
    confirmed_set = set()
    for a_id, b_id in confirmed:
        confirmed_set.add((min(a_id, b_id), max(a_id, b_id)))

    merge_groups = []
    for component_ids in components.values():
        if len(component_ids) == 1:
            continue

        # Check group size limit
        if len(component_ids) > max_group_size:
            merge_groups.append(
                {
                    "status": "flagged",
                    "reason": f"Group size {len(component_ids)} exceeds max {max_group_size}",
                    "entities": [
                        {"element_id": eid, "name": entity_map[eid].name}
                        for eid in component_ids
                    ],
                }
            )
            continue

        # Check all pairs are confirmed (no transitive chaining)
        missing_pairs = []
        for a_id, b_id in combinations(component_ids, 2):
            pair_key = (min(a_id, b_id), max(a_id, b_id))
            if pair_key not in confirmed_set:
                missing_pairs.append((a_id, b_id))

        if missing_pairs:
            merge_groups.append(
                {
                    "status": "needs_confirmation",
                    "reason": f"{len(missing_pairs)} pair(s) not yet confirmed",
                    "entities": [
                        {"element_id": eid, "name": entity_map[eid].name}
                        for eid in component_ids
                    ],
                    "missing_pairs": [
                        (a_id, b_id) for a_id, b_id in missing_pairs
                    ],
                }
            )
            continue

        # All pairs confirmed — pick survivor (most non-null properties, then most relationships)
        component_entities = [entity_map[eid] for eid in component_ids]
        survivor = max(
            component_entities,
            key=lambda e: (
                len([v for v in e.properties.values() if v]),
                e.relationship_count,
            ),
        )
        consumed = [
            e for e in component_entities if e.element_id != survivor.element_id
        ]

        merge_groups.append(
            {
                "status": "ready",
                "survivor": {
                    "element_id": survivor.element_id,
                    "name": survivor.name,
                },
                "consumed": [
                    {"element_id": e.element_id, "name": e.name} for e in consumed
                ],
            }
        )

    return merge_groups


# ---------------------------------------------------------------------------
# Main entry point: resolve
# ---------------------------------------------------------------------------


def resolve(snapshot_path: Path | str, config_overrides: dict | None = None) -> Path:
    """Run entity resolution on a snapshot file. Returns path to merge plan.

    Args:
        snapshot_path: Path to the snapshot JSON file.
        config_overrides: Optional dict of config fields to override
            (e.g. {"pre_filter_threshold": 0.5, "confidence_mode": "scored"}).
            Values not provided fall back to .env, then defaults.
    """
    snapshot_path = Path(snapshot_path)
    snapshot = EntitySnapshot.model_validate_json(snapshot_path.read_text())
    config = EntityResolutionConfig(**(config_overrides or {}))

    LOG_DIR.mkdir(exist_ok=True)

    print(f"Loaded snapshot: {snapshot.entity_count} {snapshot.label} entities")
    print(
        f"Config: pre_filter={config.pre_filter_strategy}, "
        f"threshold={config.pre_filter_threshold}, "
        f"batch_size={config.batch_size}, "
        f"confidence={config.confidence_mode}"
    )

    # Step 1: Exact dedup — merge identical-name entities without LLM
    unique_entities, auto_groups = _exact_dedup(snapshot.entities)
    exact_consumed = sum(len(g["consumed"]) for g in auto_groups)
    print(
        f"\nExact dedup: {snapshot.entity_count} entities -> "
        f"{len(unique_entities)} unique names "
        f"({exact_consumed} auto-merges in {len(auto_groups)} groups)"
    )

    # Step 2: Fuzzy pre-filter on unique-name survivors only
    pre_filter_fn = PRE_FILTERS.get(config.pre_filter_strategy)
    if not pre_filter_fn:
        raise ValueError(
            f"Unknown pre-filter: {config.pre_filter_strategy}. "
            f"Available: {list(PRE_FILTERS.keys())}"
        )

    candidates = pre_filter_fn(unique_entities, config.pre_filter_threshold)
    print(f"Pre-filter generated {len(candidates)} candidate pairs")

    # Step 3: LLM evaluation
    llm_groups: list[dict[str, Any]] = []
    all_decisions: list[MergeDecision] = []

    if candidates:
        client = _create_llm_client()
        all_decisions = _evaluate_candidates(candidates, config, client)

        # Build merge groups with transitive confirmation
        llm_groups = _build_and_confirm_groups(
            all_decisions, snapshot, config, client
        )

    # Combine auto-merge and LLM merge groups
    all_groups = auto_groups + llm_groups

    # Summary
    ready = [g for g in all_groups if g["status"] == "ready"]
    flagged = [g for g in all_groups if g["status"] != "ready"]
    llm_ready = [g for g in llm_groups if g["status"] == "ready"]

    print(f"\nResults:")
    print(f"  Exact-name merges: {len(auto_groups)} groups ({exact_consumed} nodes)")
    print(f"  LLM-confirmed merges: {len(llm_ready)} groups")
    print(f"  Flagged for review: {len(flagged)} groups")

    for g in llm_ready:
        consumed_names = ", ".join(c["name"] for c in g["consumed"])
        print(f"  MERGE: {g['survivor']['name']} <- {consumed_names}")
    for g in flagged:
        names = ", ".join(e["name"] for e in g["entities"])
        print(f"  FLAG:  {names} ({g['reason']})")

    # Write merge plan
    plan = MergePlan(
        created_at=datetime.now().isoformat(),
        snapshot_path=str(snapshot_path),
        config=config.model_dump(),
        total_entities=snapshot.entity_count,
        candidate_pairs=len(candidates),
        decisions=all_decisions,
        merge_groups=all_groups,
    )

    plan_path = LOG_DIR / f"merge_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    plan_path.write_text(plan.model_dump_json(indent=2))
    print(f"\nMerge plan: {plan_path}")

    return plan_path


def _evaluate_candidates(
    candidates: list[CandidatePair],
    config: EntityResolutionConfig,
    client,
) -> list[MergeDecision]:
    """Evaluate all candidate pairs in batches via LLM."""
    all_decisions: list[MergeDecision] = []
    batches = [
        candidates[i : i + config.batch_size]
        for i in range(0, len(candidates), config.batch_size)
    ]

    for i, batch in enumerate(batches, 1):
        print(f"  LLM batch {i}/{len(batches)} ({len(batch)} pairs)...")
        decisions = _call_llm_batch(batch, config, client)
        all_decisions.extend(decisions)

        merges = sum(1 for d in decisions if d.decision == "merge")
        print(f"    -> {merges} merge, {len(decisions) - merges} no_merge")

    return all_decisions


def _build_and_confirm_groups(
    all_decisions: list[MergeDecision],
    snapshot: EntitySnapshot,
    config: EntityResolutionConfig,
    client,
) -> list[dict[str, Any]]:
    """Build merge groups, confirming any transitive gaps with additional LLM calls."""
    entity_map = {e.element_id: e for e in snapshot.entities}

    # Track all evaluated pairs (both merge and no_merge) to avoid re-sending
    evaluated_pairs: set[tuple[str, str]] = set()
    for d in all_decisions:
        pair_key = (
            min(d.entity_a_element_id, d.entity_b_element_id),
            max(d.entity_a_element_id, d.entity_b_element_id),
        )
        evaluated_pairs.add(pair_key)

    for round_num in range(2):
        merge_groups = _build_merge_groups(
            all_decisions, snapshot.entities, config.max_group_size
        )
        needs_confirm = [
            g for g in merge_groups if g["status"] == "needs_confirmation"
        ]
        if not needs_confirm:
            break

        # Collect only pairs not yet evaluated
        additional_pairs = []
        for group in needs_confirm:
            for a_id, b_id in group["missing_pairs"]:
                pair_key = (min(a_id, b_id), max(a_id, b_id))
                if pair_key in evaluated_pairs:
                    continue
                a_entity = entity_map.get(a_id)
                b_entity = entity_map.get(b_id)
                if a_entity and b_entity:
                    additional_pairs.append(
                        CandidatePair(
                            entity_a=a_entity,
                            entity_b=b_entity,
                            pre_filter_score=0.0,
                        )
                    )

        if not additional_pairs:
            break

        print(
            f"\n  Confirming {len(additional_pairs)} transitive pairs "
            f"(round {round_num + 1})..."
        )
        additional_decisions = _evaluate_candidates(
            additional_pairs, config, client
        )
        all_decisions.extend(additional_decisions)
        for d in additional_decisions:
            pair_key = (
                min(d.entity_a_element_id, d.entity_b_element_id),
                max(d.entity_a_element_id, d.entity_b_element_id),
            )
            evaluated_pairs.add(pair_key)

    return merge_groups


def _write_empty_plan(
    snapshot_path: Path,
    config: EntityResolutionConfig,
    entity_count: int,
) -> Path:
    """Write an empty merge plan when there are no candidates."""
    LOG_DIR.mkdir(exist_ok=True)
    plan = MergePlan(
        created_at=datetime.now().isoformat(),
        snapshot_path=str(snapshot_path),
        config=config.model_dump(),
        total_entities=entity_count,
        candidate_pairs=0,
        decisions=[],
        merge_groups=[],
    )
    plan_path = LOG_DIR / f"merge_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    plan_path.write_text(plan.model_dump_json(indent=2))
    print(f"Merge plan: {plan_path}")
    return plan_path


# ---------------------------------------------------------------------------
# Apply merge plan to Neo4j
# ---------------------------------------------------------------------------


def apply_merge_plan(driver, plan_path: Path | str) -> None:
    """Apply a merge plan to Neo4j, merging confirmed entity groups."""
    plan_path = Path(plan_path)
    plan = MergePlan.model_validate_json(plan_path.read_text())

    # Load snapshot for property fill data
    snapshot = EntitySnapshot.model_validate_json(
        Path(plan.snapshot_path).read_text()
    )
    entity_map = {e.element_id: e for e in snapshot.entities}

    ready_groups = [g for g in plan.merge_groups if g["status"] == "ready"]

    if not ready_groups:
        print("No merge groups ready to apply.")
        return

    total_consumed = sum(len(g["consumed"]) for g in ready_groups)
    print(f"Applying {len(ready_groups)} merge groups ({total_consumed} merges)...")

    ok_count = 0
    fail_count = 0

    for i, group in enumerate(ready_groups, 1):
        survivor_id = group["survivor"]["element_id"]
        survivor_name = group["survivor"]["name"]
        survivor_entity = entity_map.get(survivor_id)
        consumed_list = group["consumed"]
        merge_type = group.get("merge_type", "llm")

        if len(consumed_list) > 3:
            print(f"  [{i}/{len(ready_groups)}] {survivor_name} <- {len(consumed_list)} duplicates ({merge_type})")
        else:
            consumed_names = ", ".join(c["name"] for c in consumed_list)
            print(f"  [{i}/{len(ready_groups)}] {survivor_name} <- {consumed_names} ({merge_type})")

        group_ok = 0
        group_fail = 0

        for consumed in consumed_list:
            consumed_id = consumed["element_id"]
            consumed_entity = entity_map.get(consumed_id)

            # Compute fill properties: consumed's non-null props that survivor lacks
            fill_props = {}
            if survivor_entity and consumed_entity:
                for k, v in consumed_entity.properties.items():
                    if k.startswith("__"):
                        continue
                    survivor_val = survivor_entity.properties.get(k)
                    if v and (not survivor_val):
                        fill_props[k] = v

            try:
                driver.execute_query(
                    """
                    MATCH (survivor) WHERE elementId(survivor) = $survivor_id
                    MATCH (consumed) WHERE elementId(consumed) = $consumed_id
                    CALL apoc.refactor.mergeNodes([survivor, consumed],
                         {properties: 'discard', mergeRels: true})
                    YIELD node
                    SET node += $fill_props
                    RETURN node.name AS name
                    """,
                    survivor_id=survivor_id,
                    consumed_id=consumed_id,
                    fill_props=fill_props,
                )
                group_ok += 1
            except Exception as e:
                group_fail += 1
                logger.error(f"Failed merging {consumed['name']} into {survivor_name}: {e}")

        ok_count += group_ok
        fail_count += group_fail
        if group_fail:
            print(f"       {group_ok} OK, {group_fail} FAILED")

    print(f"\nDone: {ok_count} merged, {fail_count} failed.")
    print("Run 'uv run python main.py verify' to check results.")


def latest_merge_plan() -> Path | None:
    """Find the most recent merge plan file."""
    if not LOG_DIR.exists():
        return None
    files = sorted(LOG_DIR.glob("merge_plan_*.json"), reverse=True)
    return files[0] if files else None
