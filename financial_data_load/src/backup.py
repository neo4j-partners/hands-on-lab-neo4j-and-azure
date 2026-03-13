"""Full database backup and restore for skipping PDF reprocessing.

Exports all nodes and relationships to a JSON file. Restoring clears the
database and recreates everything from the backup, avoiding the ~25 min
PDF processing step.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from neo4j import Driver

BACKUP_DIR = Path(__file__).resolve().parent.parent / "backups"

_BATCH_SIZE = 500


def backup_database(driver: Driver) -> Path:
    """Export all nodes and relationships to a JSON file."""
    BACKUP_DIR.mkdir(exist_ok=True)

    print("Exporting nodes...")
    nodes, _, _ = driver.execute_query(
        "MATCH (n) "
        "RETURN elementId(n) AS eid, labels(n) AS labels, properties(n) AS props"
    )

    print("Exporting relationships...")
    rels, _, _ = driver.execute_query(
        "MATCH (a)-[r]->(b) "
        "RETURN elementId(a) AS start_eid, elementId(b) AS end_eid, "
        "       type(r) AS type, properties(r) AS props"
    )

    # Map element IDs to sequential backup IDs
    eid_to_bid: dict[str, int] = {}
    node_list = []
    for i, node in enumerate(nodes):
        eid_to_bid[node["eid"]] = i
        props = {k: v for k, v in node["props"].items() if v is not None}
        node_list.append({"bid": i, "labels": node["labels"], "props": props})

    rel_list = []
    for rel in rels:
        props = (
            {k: v for k, v in rel["props"].items() if v is not None}
            if rel["props"]
            else {}
        )
        rel_list.append({
            "s": eid_to_bid[rel["start_eid"]],
            "e": eid_to_bid[rel["end_eid"]],
            "type": rel["type"],
            "props": props,
        })

    now = datetime.now()
    backup = {
        "exported_at": now.isoformat(),
        "node_count": len(node_list),
        "relationship_count": len(rel_list),
        "nodes": node_list,
        "relationships": rel_list,
    }

    output_path = BACKUP_DIR / f"backup_{now.strftime('%Y%m%d_%H%M%S')}.json"
    output_path.write_text(json.dumps(backup, default=str))

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"Backed up {len(node_list)} nodes, {len(rel_list)} relationships ({size_mb:.1f} MB)")
    print(f"Backup: {output_path}")
    return output_path


def _validate_backup(backup: dict) -> None:
    """Check backup structure before destructive restore."""
    for key in ("node_count", "relationship_count", "nodes", "relationships"):
        if key not in backup:
            raise ValueError(f"Invalid backup file: missing '{key}'")
    if not backup["nodes"]:
        raise ValueError("Invalid backup file: no nodes found")
    sample = backup["nodes"][0]
    for key in ("bid", "labels", "props"):
        if key not in sample:
            raise ValueError(f"Invalid backup file: node missing '{key}'")


def restore_database(driver: Driver, backup_path: Path) -> None:
    """Clear database and restore all nodes and relationships from a backup."""
    backup = json.loads(backup_path.read_text())
    _validate_backup(backup)

    n_nodes = backup["node_count"]
    n_rels = backup["relationship_count"]

    print(f"Restoring {n_nodes} nodes, {n_rels} relationships...")

    # Use the robust batched clear from loader (handles constraints + indexes)
    from .loader import clear_database
    clear_database(driver)

    # Group nodes by label combination for batch creation.
    # Return elementId from each CREATE so we can map bid -> eid
    # without a separate query or temporary property.
    label_groups: dict[tuple[str, ...], list[dict]] = defaultdict(list)
    for node in backup["nodes"]:
        key = tuple(sorted(node["labels"]))
        label_groups[key].append(node)

    bid_to_eid: dict[int, str] = {}
    created_nodes = 0
    for labels, group_nodes in label_groups.items():
        labels_cypher = ":".join(f"`{l}`" for l in labels)
        for i in range(0, len(group_nodes), _BATCH_SIZE):
            batch = group_nodes[i:i + _BATCH_SIZE]
            batch_props = [n["props"] for n in batch]
            rows, _, _ = driver.execute_query(
                f"UNWIND $batch AS props "
                f"CREATE (n:{labels_cypher}) SET n = props "
                f"RETURN elementId(n) AS eid",
                batch=batch_props,
            )
            for node, row in zip(batch, rows):
                bid_to_eid[node["bid"]] = row["eid"]
        created_nodes += len(group_nodes)
        print(f"    {len(group_nodes):>5}  :{':'.join(labels)}")

    print(f"  {created_nodes} nodes created")

    # Group relationships by type for batch creation
    rel_groups: dict[str, list[dict]] = defaultdict(list)
    for rel in backup["relationships"]:
        rel_groups[rel["type"]].append({
            "s": bid_to_eid[rel["s"]],
            "e": bid_to_eid[rel["e"]],
            "props": rel["props"],
        })

    created_rels = 0
    for rel_type, group_rels in rel_groups.items():
        for i in range(0, len(group_rels), _BATCH_SIZE):
            batch = group_rels[i:i + _BATCH_SIZE]
            driver.execute_query(
                f"""
                UNWIND $batch AS rel
                MATCH (a) WHERE elementId(a) = rel.s
                MATCH (b) WHERE elementId(b) = rel.e
                CREATE (a)-[r:`{rel_type}`]->(b)
                SET r = rel.props
                """,
                batch=batch,
            )
        created_rels += len(group_rels)
        print(f"    {len(group_rels):>5}  {rel_type}")

    print(f"  {created_rels} relationships created")
    print("Restore complete.")
    print("\nNote: indexes and constraints were not restored.")
    print("Run 'uv run python main.py finalize' after entity resolution to recreate them.")


def latest_backup() -> Path | None:
    """Find the most recent backup file."""
    if not BACKUP_DIR.exists():
        return None
    files = sorted(BACKUP_DIR.glob("backup_*.json"), reverse=True)
    return files[0] if files else None
