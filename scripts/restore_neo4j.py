#!/usr/bin/env python3
"""
Neo4j Database Restore Script

Streams and restores the Neo4j database from GitHub or a local file.
Always creates fulltext indexes for entity search on Company, Product, and RiskFactor names.

Usage:
    uv run python scripts/restore_neo4j.py
    uv run python scripts/restore_neo4j.py --force  # Skip confirmation
    uv run python scripts/restore_neo4j.py --file /path/to/backup.json  # Use local file
    uv run python scripts/restore_neo4j.py --file /path/to/backup.json --sample  # Quick test with 100 nodes/rels
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
from dotenv import load_dotenv
from neo4j import AsyncGraphDatabase
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from neo4j import AsyncSession

# GitHub LFS media URLs for backup files (must use media.githubusercontent.com for LFS files)
GITHUB_URL = "https://media.githubusercontent.com/media/neo4j-partners/workshop-financial-data/main/snapshot/financial_backup.json"
GITHUB_CHECKSUM_URL = "https://media.githubusercontent.com/media/neo4j-partners/workshop-financial-data/main/snapshot/financial_backup.checksum.json"

# Batch size for bulk operations
BATCH_SIZE = 500


class RestoreConfig(BaseSettings):
    """Configuration for Neo4j restore loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    uri: str | None = Field(default=None, validation_alias="NEO4J_URI")
    username: str | None = Field(default=None, validation_alias="NEO4J_USERNAME")
    password: str | None = Field(default=None, validation_alias="NEO4J_PASSWORD")

    @property
    def is_configured(self) -> bool:
        return all([self.uri, self.username, self.password])


def get_project_root() -> Path:
    return Path(__file__).parent.parent


async def load_schema_from_file(file_path: Path) -> dict | None:
    """Load schema from checksum file adjacent to backup file."""
    checksum_path = file_path.parent / "financial_backup.checksum.json"
    if not checksum_path.exists():
        print(f"Warning: Checksum file not found at {checksum_path}")
        return None

    with open(checksum_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("schema")


async def load_schema_from_github() -> dict | None:
    """Load schema from GitHub checksum file."""
    try:
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
            response = await client.get(GITHUB_CHECKSUM_URL)
            response.raise_for_status()
            data = response.json()
            return data.get("schema")
    except httpx.HTTPError as e:
        print(f"Warning: Could not load schema from GitHub (HTTP error): {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse schema from GitHub (invalid JSON): {e}")
        return None


async def restore_schema(session: AsyncSession, schema: dict) -> dict:
    """Restore indexes and constraints from schema."""
    results = {"constraints": 0, "indexes": 0}

    # Restore constraints first (they create backing indexes automatically)
    for constraint in schema.get("constraints", []):
        try:
            name = constraint["name"]
            ctype = constraint["type"]
            labels = constraint["labels"]
            properties = constraint["properties"]

            if not labels or not properties:
                continue

            label = labels[0]
            props = ", ".join(f"n.`{p}`" for p in properties)

            if ctype == "UNIQUENESS":
                cypher = f"CREATE CONSTRAINT `{name}` IF NOT EXISTS FOR (n:`{label}`) REQUIRE ({props}) IS UNIQUE"
            elif ctype == "NODE_KEY":
                cypher = f"CREATE CONSTRAINT `{name}` IF NOT EXISTS FOR (n:`{label}`) REQUIRE ({props}) IS NODE KEY"
            elif ctype == "NODE_PROPERTY_EXISTENCE":
                cypher = f"CREATE CONSTRAINT `{name}` IF NOT EXISTS FOR (n:`{label}`) REQUIRE ({props}) IS NOT NULL"
            else:
                print(f"  Skipping unsupported constraint type: {ctype}")
                continue

            await session.run(cypher)
            results["constraints"] += 1
            print(f"  Created constraint: {name}")
        except Exception as e:
            print(f"  Warning: Could not create constraint {constraint.get('name')}: {e}")

    # Restore indexes (skip those already created by constraints)
    constraint_names = {c["name"] for c in schema.get("constraints", [])}

    for index in schema.get("indexes", []):
        try:
            name = index["name"]

            # Skip if this index is backing a constraint
            if name in constraint_names:
                continue

            itype = index["type"]
            labels = index["labels"]
            properties = index["properties"]
            options = index.get("options", {})

            if not labels or not properties:
                continue

            label = labels[0]
            props = ", ".join(f"n.`{p}`" for p in properties)

            if itype == "VECTOR":
                config = options.get("indexConfig", {})
                dimensions = config.get("vector.dimensions", 1536)
                similarity = config.get("vector.similarity_function", "COSINE").lower()

                cypher = (
                    f"CREATE VECTOR INDEX `{name}` IF NOT EXISTS "
                    f"FOR (n:`{label}`) ON (n.`{properties[0]}`) "
                    f"OPTIONS {{indexConfig: {{`vector.dimensions`: {dimensions}, `vector.similarity_function`: '{similarity}'}}}}"
                )
            elif itype == "RANGE":
                cypher = f"CREATE INDEX `{name}` IF NOT EXISTS FOR (n:`{label}`) ON ({props})"
            elif itype == "TEXT":
                cypher = f"CREATE TEXT INDEX `{name}` IF NOT EXISTS FOR (n:`{label}`) ON ({props})"
            elif itype == "FULLTEXT":
                cypher = f"CREATE FULLTEXT INDEX `{name}` IF NOT EXISTS FOR (n:`{label}`) ON EACH [{props}]"
            else:
                print(f"  Skipping unsupported index type: {itype}")
                continue

            await session.run(cypher)
            results["indexes"] += 1
            print(f"  Created index: {name}")
        except Exception as e:
            print(f"  Warning: Could not create index {index.get('name')}: {e}")

    return results


async def create_fulltext_indexes(session: AsyncSession) -> int:
    """Create fulltext indexes for entity search on Company, Product, and RiskFactor names."""
    indexes_created = 0

    # Define fulltext indexes to create
    fulltext_indexes = [
        {
            "name": "search_entities",
            "labels": ["Company", "Product", "RiskFactor"],
            "properties": ["name"],
        },
        {
            "name": "search_chunks",  # For context provider fulltext search
            "labels": ["Chunk"],
            "properties": ["text"],
        },
    ]

    for index in fulltext_indexes:
        try:
            name = index["name"]
            labels = index["labels"]
            properties = index["properties"]

            # Build label string: (n:Label1|Label2|Label3)
            label_str = "|".join(f"`{label}`" for label in labels)
            # Build property string: n.prop1, n.prop2
            prop_str = ", ".join(f"n.`{prop}`" for prop in properties)

            cypher = (
                f"CREATE FULLTEXT INDEX `{name}` IF NOT EXISTS "
                f"FOR (n:{label_str}) ON EACH [{prop_str}]"
            )

            await session.run(cypher)
            indexes_created += 1
            print(f"  Created fulltext index: {name}")
        except Exception as e:
            print(f"  Warning: Could not create fulltext index {index.get('name')}: {e}")

    # Wait for indexes to come online
    if indexes_created > 0:
        print("  Waiting for indexes to come online...")
        await session.run("CALL db.awaitIndexes(300)")

    return indexes_created


async def clear_database(session: AsyncSession) -> None:
    """Clear all data from database using batched deletes."""
    print("Clearing existing data...")
    # Use batched delete to avoid OOM on large databases
    while True:
        result = await session.run(
            "MATCH (n) WITH n LIMIT 10000 DETACH DELETE n RETURN count(*) AS deleted"
        )
        record = await result.single()
        deleted = record["deleted"]
        if deleted == 0:
            break
        print(f"  Deleted {deleted} nodes...")


async def drop_schema(session: AsyncSession) -> None:
    """Drop all indexes and constraints."""
    print("Dropping existing indexes and constraints...")

    # Drop constraints first
    result = await session.run("SHOW CONSTRAINTS YIELD name RETURN name")
    constraints = await result.data()
    for c in constraints:
        try:
            await session.run(f"DROP CONSTRAINT `{c['name']}` IF EXISTS")
            print(f"  Dropped constraint: {c['name']}")
        except Exception as e:
            print(f"  Warning: Could not drop constraint {c['name']}: {e}")

    # Drop indexes (except LOOKUP indexes which are system-managed)
    result = await session.run(
        "SHOW INDEXES YIELD name, type WHERE type <> 'LOOKUP' RETURN name"
    )
    indexes = await result.data()
    for idx in indexes:
        try:
            await session.run(f"DROP INDEX `{idx['name']}` IF EXISTS")
            print(f"  Dropped index: {idx['name']}")
        except Exception as e:
            print(f"  Warning: Could not drop index {idx['name']}: {e}")


async def create_temp_index(session: AsyncSession) -> None:
    """Create temporary index on _backup_id for fast relationship lookups."""
    await session.run(
        "CREATE INDEX _backup_id_temp IF NOT EXISTS FOR (n:_RestoreTemp) ON (n._backup_id)"
    )
    # Wait for index to come online
    await session.run("CALL db.awaitIndexes(300)")


async def drop_temp_index(session: AsyncSession) -> None:
    """Drop temporary index and label."""
    try:
        await session.run("DROP INDEX _backup_id_temp IF EXISTS")
    except Exception:
        pass


async def restore_nodes_batched(
    session: AsyncSession, nodes: list[dict], batch_size: int = BATCH_SIZE
) -> int:
    """Restore nodes using batched UNWIND for performance."""
    total = len(nodes)
    restored = 0

    for i in range(0, total, batch_size):
        batch = nodes[i : i + batch_size]

        # Group nodes by label combination for efficient creation
        by_labels: dict[str, list[dict]] = {}
        for node in batch:
            label_key = ":".join(sorted(node["labels"])) if node["labels"] else ""
            if label_key not in by_labels:
                by_labels[label_key] = []
            by_labels[label_key].append(node)

        for label_key, label_nodes in by_labels.items():
            # Add _RestoreTemp label for indexing, plus original labels
            if label_key:
                label_str = f":_RestoreTemp:{label_key}"
            else:
                label_str = ":_RestoreTemp"

            # Prepare node data with _backup_id
            node_data = []
            for n in label_nodes:
                props = n["properties"].copy()
                props["_backup_id"] = str(n["id"])
                node_data.append(props)

            # Use UNWIND for batch creation
            await session.run(
                f"UNWIND $nodes AS node CREATE (n{label_str}) SET n = node",
                {"nodes": node_data},
            )

        restored += len(batch)
        if restored % 500 == 0 or restored == total:
            print(f"  {restored}/{total} nodes...")

    return restored


async def restore_relationships_batched(
    session: AsyncSession, relationships: list[dict], batch_size: int = BATCH_SIZE
) -> int:
    """Restore relationships using batched UNWIND with index lookups."""
    total = len(relationships)
    restored = 0

    for i in range(0, total, batch_size):
        batch = relationships[i : i + batch_size]

        # Group relationships by type for efficient creation
        by_type: dict[str, list[dict]] = {}
        for rel in batch:
            rel_type = rel["type"]
            if not rel_type or not rel["startId"] or not rel["endId"]:
                continue
            if rel_type not in by_type:
                by_type[rel_type] = []
            by_type[rel_type].append(rel)

        for rel_type, type_rels in by_type.items():
            rel_data = [
                {
                    "startId": str(r["startId"]),
                    "endId": str(r["endId"]),
                    "props": r["properties"],
                }
                for r in type_rels
            ]

            # Use UNWIND with index lookup on _RestoreTemp label
            await session.run(
                f"""
                UNWIND $rels AS rel
                MATCH (a:_RestoreTemp {{_backup_id: rel.startId}})
                MATCH (b:_RestoreTemp {{_backup_id: rel.endId}})
                CREATE (a)-[r:`{rel_type}`]->(b)
                SET r = rel.props
                """,
                {"rels": rel_data},
            )

        restored += len(batch)
        if restored % 500 == 0 or restored == total:
            print(f"  {restored}/{total} relationships...")

    return restored


async def cleanup_restore_artifacts(session: AsyncSession) -> None:
    """Remove temporary _backup_id property and _RestoreTemp label."""
    print("Cleaning up temporary restore artifacts...")

    # Remove _backup_id property and _RestoreTemp label in batches
    while True:
        result = await session.run(
            """
            MATCH (n:_RestoreTemp)
            WITH n LIMIT 10000
            REMOVE n:_RestoreTemp, n._backup_id
            RETURN count(*) AS cleaned
            """
        )
        record = await result.single()
        cleaned = record["cleaned"]
        if cleaned == 0:
            break
        print(f"  Cleaned {cleaned} nodes...")


def parse_backup_data(
    file_path: Path | None,
    sample: bool,
    max_nodes: int | None,
    max_rels: int | None,
) -> tuple[list[dict], list[dict], int]:
    """Parse backup data from file, returning nodes, relationships, and bytes read."""
    nodes: list[dict] = []
    relationships: list[dict] = []
    bytes_read = 0
    kept_node_ids: set[str] = set()

    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                bytes_read += len(line.encode("utf-8"))

                try:
                    item = json.loads(line)
                    if item.get("type") == "node":
                        if max_nodes is None or len(nodes) < max_nodes:
                            node_id = item.get("id")
                            nodes.append({
                                "id": node_id,
                                "labels": item.get("labels", []),
                                "properties": item.get("properties", {}),
                            })
                            kept_node_ids.add(str(node_id))
                    elif item.get("type") == "relationship":
                        start_id = str(item.get("start", {}).get("id"))
                        end_id = str(item.get("end", {}).get("id"))
                        # In sample mode, only keep relationships between kept nodes
                        if sample and (start_id not in kept_node_ids or end_id not in kept_node_ids):
                            continue
                        if max_rels is None or len(relationships) < max_rels:
                            relationships.append({
                                "type": item.get("label"),
                                "startId": start_id,
                                "endId": end_id,
                                "properties": item.get("properties", {}),
                            })
                            # Early exit once we have enough relationships
                            if sample and max_rels and len(relationships) >= max_rels:
                                break
                except json.JSONDecodeError:
                    continue

    return nodes, relationships, bytes_read


async def parse_backup_data_streaming(
    sample: bool,
    max_nodes: int | None,
    max_rels: int | None,
) -> tuple[list[dict], list[dict], int]:
    """Stream and parse backup data from GitHub."""
    nodes: list[dict] = []
    relationships: list[dict] = []
    bytes_read = 0
    kept_node_ids: set[str] = set()
    done = False

    async with httpx.AsyncClient(timeout=600.0, follow_redirects=True) as client:
        async with client.stream("GET", GITHUB_URL) as response:
            response.raise_for_status()

            buffer = ""
            async for chunk in response.aiter_text():
                if done:
                    break
                bytes_read += len(chunk.encode("utf-8"))
                buffer += chunk

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if not line.strip():
                        continue

                    try:
                        item = json.loads(line)
                        if item.get("type") == "node":
                            if max_nodes is None or len(nodes) < max_nodes:
                                node_id = item.get("id")
                                nodes.append({
                                    "id": node_id,
                                    "labels": item.get("labels", []),
                                    "properties": item.get("properties", {}),
                                })
                                kept_node_ids.add(str(node_id))
                        elif item.get("type") == "relationship":
                            start_id = str(item.get("start", {}).get("id"))
                            end_id = str(item.get("end", {}).get("id"))
                            # In sample mode, only keep relationships between kept nodes
                            if sample and (start_id not in kept_node_ids or end_id not in kept_node_ids):
                                continue
                            if max_rels is None or len(relationships) < max_rels:
                                relationships.append({
                                    "type": item.get("label"),
                                    "startId": start_id,
                                    "endId": end_id,
                                    "properties": item.get("properties", {}),
                                })
                                # Early exit once we have enough relationships
                                if sample and max_rels and len(relationships) >= max_rels:
                                    done = True
                                    break
                    except json.JSONDecodeError:
                        continue

                if bytes_read % (10 * 1024 * 1024) < len(chunk.encode("utf-8")):
                    print(f"  Streamed {bytes_read / (1024 * 1024):.1f} MB...")

    return nodes, relationships, bytes_read


async def stream_and_restore(
    config: RestoreConfig,
    file_path: Path | None = None,
    sample: bool = False,
) -> dict:
    """Stream backup from GitHub or local file and restore to Neo4j."""
    # Load schema
    if file_path:
        print(f"Loading from local file: {file_path}")
        schema = await load_schema_from_file(file_path)
    else:
        print(f"Streaming from {GITHUB_URL}...")
        schema = await load_schema_from_github()

    driver = AsyncGraphDatabase.driver(config.uri, auth=(config.username, config.password))

    # Limits for sample mode
    max_nodes = 100 if sample else None
    max_rels = 100 if sample else None

    try:
        await driver.verify_connectivity()
        print(f"Connected to Neo4j at {config.uri}")

        if sample:
            print(f"Sample mode: limiting to {max_nodes} nodes and {max_rels} relationships")

        # Parse data from file or stream
        if file_path:
            nodes, relationships, bytes_read = parse_backup_data(
                file_path, sample, max_nodes, max_rels
            )
        else:
            nodes, relationships, bytes_read = await parse_backup_data_streaming(
                sample, max_nodes, max_rels
            )

        print(f"  Total: {bytes_read / (1024 * 1024):.1f} MB")
        print(f"  Parsed {len(nodes)} nodes, {len(relationships)} relationships")

        # Restore using a session
        async with driver.session() as session:
            # Clear existing data and schema
            await clear_database(session)
            await drop_schema(session)

            # Restore schema (indexes and constraints)
            schema_results = {"constraints": 0, "indexes": 0}
            if schema:
                print("Restoring schema (indexes and constraints)...")
                schema_results = await restore_schema(session, schema)
            else:
                print("Warning: No schema to restore")

            # Create temporary index for fast relationship lookups
            print("Creating temporary index for restore...")
            await create_temp_index(session)

            # Restore nodes using batched UNWIND
            print(f"Restoring {len(nodes)} nodes...")
            await restore_nodes_batched(session, nodes)

            # Restore relationships using batched UNWIND with index
            print(f"Restoring {len(relationships)} relationships...")
            await restore_relationships_batched(session, relationships)

            # Clean up temporary artifacts
            await cleanup_restore_artifacts(session)
            await drop_temp_index(session)

            # Create fulltext indexes for entity search
            print("Creating fulltext indexes...")
            fulltext_count = await create_fulltext_indexes(session)

        return {
            "nodes": len(nodes),
            "relationships": len(relationships),
            "constraints": schema_results["constraints"],
            "indexes": schema_results["indexes"],
            "fulltext_indexes": fulltext_count,
        }
    finally:
        await driver.close()


async def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Neo4j Database Restore from GitHub or local file")
    parser.add_argument("--force", "-f", action="store_true", help="Skip confirmation prompt")
    parser.add_argument(
        "--file",
        type=Path,
        help="Path to local backup JSON file (uses GitHub if not specified)",
    )
    parser.add_argument(
        "--sample", "-s",
        action="store_true",
        help="Sample mode: restore only 100 nodes and 100 relationships (all indexes/constraints still restored)",
    )
    args = parser.parse_args()

    env_path = get_project_root() / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    config = RestoreConfig()
    if not config.is_configured:
        print("Error: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD required in .env")
        return 1

    # Validate file path if provided
    if args.file and not args.file.exists():
        print(f"Error: File not found: {args.file}")
        return 1

    print("=== Neo4j Database Restore ===")
    print()
    if args.file:
        print(f"Source: {args.file}")
    else:
        print(f"Source: GitHub ({GITHUB_URL})")
    if args.sample:
        print("Mode: SAMPLE (100 nodes, 100 relationships, all schema)")
    print()
    print("WARNING: This will DELETE ALL EXISTING DATA AND SCHEMA!")
    print(f"Database: {config.uri}")
    print()

    if not args.force:
        response = input("Continue? [y/N]: ").strip().lower()
        if response not in ("y", "yes"):
            print("Cancelled.")
            return 0

    print()

    try:
        result = await stream_and_restore(
            config,
            file_path=args.file,
            sample=args.sample,
        )
        print()
        print("=== Restore Complete ===")
        print(f"Nodes: {result['nodes']}")
        print(f"Relationships: {result['relationships']}")
        print(f"Constraints: {result['constraints']}")
        print(f"Indexes: {result['indexes']}")
        print(f"Fulltext Indexes: {result['fulltext_indexes']}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
