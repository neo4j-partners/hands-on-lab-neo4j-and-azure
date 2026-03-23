"""
Entity Extraction Pipeline

This workshop demonstrates the entity extraction pipeline configuration,
manual entity addition, deduplication, merge strategies, and resolution
settings using neo4j-agent-memory.

Run with: uv run python main.py solutions 18
"""

import asyncio

from pydantic import SecretStr

from neo4j_agent_memory import MemoryClient, MemorySettings

from azure_embedder import get_memory_embedder
from config import Neo4jConfig


async def main():
    """Demonstrate entity extraction pipeline."""
    neo4j_config = Neo4jConfig()

    settings = MemorySettings(
        neo4j={
            "uri": neo4j_config.uri,
            "username": neo4j_config.username,
            "password": SecretStr(neo4j_config.password),
        },
        extraction={
            "extractor_type": "pipeline",
            "enable_spacy": True,
            "enable_gliner": False,  # Disabled: downloads ~500MB model, impractical in a workshop
            "enable_llm_fallback": False,  # LLM extractor requires OPENAI_API_KEY, not available in this workshop
            "confidence_threshold": 0.5,
            "entity_types": [
                "PERSON", "ORGANIZATION", "LOCATION", "EVENT", "OBJECT"
            ],
        },
    )

    async with MemoryClient(settings, embedder=get_memory_embedder()) as memory_client:
        # Add a manual entity
        entity, dedup_result = await memory_client.long_term.add_entity(
            name="Apple Inc",
            entity_type="ORGANIZATION",
            description="Technology company that manufactures iPhone, iPad, Mac, and other consumer electronics",
        )
        print(f"Added entity: name={entity.name}, type={entity.entity_type}, id={entity.id}")

        # Test deduplication
        duplicate, dedup_result = await memory_client.long_term.add_entity(
            name="Apple",
            entity_type="ORGANIZATION",
            description="Consumer electronics company known for iPhone and Mac products",
        )
        print(f"Duplicate test: name={duplicate.name}, id={duplicate.id}")
        print(f"Same entity? {duplicate.id == entity.id}")

    await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
