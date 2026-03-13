"""Entity snapshot export from Neo4j for iterative entity resolution testing."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from neo4j import Driver
from pydantic import BaseModel

logger = logging.getLogger(__name__)

SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "snapshots"


class SnapshotEntity(BaseModel):
    """A single entity exported from Neo4j."""

    element_id: str
    name: str
    labels: list[str]
    properties: dict[str, Any]
    source_chunks: list[str]
    relationship_count: int


class EntitySnapshot(BaseModel):
    """Complete entity snapshot for a label group."""

    exported_at: str
    label: str
    entity_count: int
    entities: list[SnapshotEntity]


def export_snapshot(driver: Driver, label: str = "Company") -> Path:
    """Export all entities of a given label from Neo4j to a JSON snapshot file."""
    SNAPSHOT_DIR.mkdir(exist_ok=True)

    rows, _, _ = driver.execute_query(
        """
        MATCH (e:"""
        + label
        + """)
        OPTIONAL MATCH (e)-[:FROM_CHUNK]->(c:Chunk)
        WITH e, collect(DISTINCT c.text)[0..3] AS source_chunks
        OPTIONAL MATCH (e)-[r]-()
        WITH e, source_chunks, count(r) AS rel_count
        RETURN elementId(e) AS element_id,
               e.name AS name,
               labels(e) AS all_labels,
               properties(e) AS props,
               source_chunks,
               rel_count
        ORDER BY e.name
    """
    )

    entities = []
    for row in rows:
        # Filter out internal labels and properties
        labels = [l for l in row["all_labels"] if not l.startswith("__")]
        props = {
            k: v
            for k, v in row["props"].items()
            if not k.startswith("__") and not isinstance(v, list)
        }
        entities.append(
            SnapshotEntity(
                element_id=row["element_id"],
                name=row["name"] or "",
                labels=labels,
                properties=props,
                source_chunks=[c for c in row["source_chunks"] if c],
                relationship_count=row["rel_count"],
            )
        )

    snapshot = EntitySnapshot(
        exported_at=datetime.now().isoformat(),
        label=label,
        entity_count=len(entities),
        entities=entities,
    )

    output_path = (
        SNAPSHOT_DIR
        / f"snapshot_{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    output_path.write_text(snapshot.model_dump_json(indent=2))

    print(f"Exported {len(entities)} {label} entities to: {output_path}")
    return output_path


def latest_snapshot(label: str = "Company") -> Path | None:
    """Find the most recent snapshot file for a label."""
    if not SNAPSHOT_DIR.exists():
        return None
    files = sorted(SNAPSHOT_DIR.glob(f"snapshot_{label}_*.json"), reverse=True)
    return files[0] if files else None
