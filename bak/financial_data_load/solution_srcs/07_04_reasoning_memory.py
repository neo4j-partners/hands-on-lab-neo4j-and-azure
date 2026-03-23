"""
Reasoning Memory

This workshop demonstrates recording agent execution traces, searching
for similar past tasks, and viewing tool usage statistics using
neo4j-agent-memory's reasoning memory.

Run with: uv run python main.py solutions 20
"""

import asyncio

from pydantic import SecretStr

from neo4j_agent_memory import MemoryClient, MemorySettings
from neo4j_agent_memory.integrations.microsoft_agent import (
    Neo4jMicrosoftMemory,
    record_agent_trace,
    get_similar_traces,
)

from azure_embedder import get_memory_embedder
from config import Neo4jConfig


async def main():
    """Demonstrate reasoning memory."""
    neo4j_config = Neo4jConfig()

    settings = MemorySettings(
        neo4j={
            "uri": neo4j_config.uri,
            "username": neo4j_config.username,
            "password": SecretStr(neo4j_config.password),
        },
        extraction={
            "enable_gliner": False,  # GLiNER disabled: downloads ~500MB model from HuggingFace, impractical in a workshop
            "enable_llm_fallback": False,  # LLM extractor requires OPENAI_API_KEY, not available in this workshop
        },
    )

    async with MemoryClient(settings, embedder=get_memory_embedder()) as memory_client:
        memory = Neo4jMicrosoftMemory.from_memory_client(
            memory_client=memory_client,
            session_id="reasoning-demo",
            include_short_term=True,
            include_long_term=True,
            include_reasoning=True,
        )

        # Record a successful trace
        trace = await record_agent_trace(
            memory=memory,
            messages=[],
            task="Find risk factors related to supply chain disruptions in Apple's 10-K filing",
            tool_calls=[
                {
                    "name": "search_knowledge",
                    "arguments": {"query": "Apple supply chain risk factors"},
                    "result": ["Component supply constraints", "Single-source supplier risk", "Geopolitical disruptions"],
                    "status": "success",
                    "duration_ms": 180,
                },
                {
                    "name": "search_memory",
                    "arguments": {"query": "user interest in supply chain"},
                    "result": ["User previously expressed concern about supply chain risks"],
                    "status": "success",
                    "duration_ms": 95,
                },
            ],
            outcome="Identified 3 key supply chain risk factors from Apple's 10-K and connected them to user's stated interest",
            success=True,
        )
        print(f"Recorded trace: {trace.id}")
        print(f"Task: {trace.task}")
        print(f"Steps: {len(trace.steps)}")
        print(f"Success: {trace.success}")

        # Record a failed trace
        failed_trace = await record_agent_trace(
            memory=memory,
            messages=[],
            task="Find competitive analysis between Apple and Microsoft from SEC filings",
            tool_calls=[
                {
                    "name": "search_knowledge",
                    "arguments": {"query": "Apple vs Microsoft competition"},
                    "result": [],
                    "status": "success",
                    "duration_ms": 210,
                },
            ],
            outcome="No competitive analysis found — 10-K filings discuss risks independently, not as head-to-head comparisons",
            success=False,
        )
        print(f"\nRecorded failed trace: {failed_trace.id}")
        print(f"Task: {failed_trace.task}")
        print(f"Success: {failed_trace.success}")

        # Find similar traces
        traces = await get_similar_traces(
            memory=memory,
            task="What are the supply chain risks in Microsoft's annual report?",
            limit=3,
        )
        print(f"\nFound {len(traces)} similar traces:")
        for t in traces:
            print(f"  Task: {t.task}")
            print(f"  Outcome: {t.outcome}")
            print(f"  Success: {t.success}")
            print()

        # View tool statistics
        stats = await memory_client.reasoning.get_tool_stats()
        if stats:
            print("Tool Statistics:")
            for tool in stats:
                print(f"  {tool.name}: {tool.total_calls} calls, {tool.success_rate:.0%} success rate")
                if tool.avg_duration_ms:
                    print(f"    Avg duration: {tool.avg_duration_ms:.0f}ms")

    await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
