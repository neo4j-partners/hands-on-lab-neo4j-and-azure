# Lab 7 - Agent Memory

This lab uses the [`neo4j-agent-memory`](https://github.com/neo4j-labs/agent-memory) package — the second Neo4j context provider introduced in Lab 6's README. It's a graph-native memory system that gives AI agents persistent, searchable memory stored in Neo4j.

While the `agent-framework-neo4j` provider in Lab 6 retrieves from a static knowledge base you built, agent memory is dynamic: it grows with every conversation as the agent learns user preferences, extracts entities, and records its own reasoning.

## What is Neo4j Agent Memory?

### Three Memory Types

**Short-Term Memory** stores conversation history as `Message` nodes with embeddings. This lets the agent semantically search past messages — not just replay them in order, but find the most relevant past exchanges for the current question. Messages are grouped into conversations by session, and entities are automatically extracted during ingestion.

**Long-Term Memory** stores structured knowledge as entities, facts, and preferences. Entities follow the **POLE+O** classification — **P**erson, **O**bject, **L**ocation, **E**vent, **O**rganization — and are deduplicated using configurable strategies (exact, fuzzy, semantic, or composite matching). Facts are stored as Subject-Predicate-Object triples (e.g., "Apple → manufactures → iPhone"). Preferences capture user-specific information with category and context.

**Reasoning Memory** captures traces of the agent's ReAct cycle (Reason → Act → Observe). Each trace records the task description, steps taken, tools called, outcome, and success/failure status. When the agent encounters a similar task later, it can retrieve these traces to reuse successful strategies or avoid repeating failures.

### Memory Context Provider

The package provides its own `Neo4jContextProvider` (distinct from the one in Lab 6) that integrates with MAF:

- **`before_run()`** retrieves context from all three memory types: recent conversation history, semantically relevant past messages, matching preferences, related entities, and similar reasoning traces
- **`after_run()`** stores the new messages and automatically extracts entities from the conversation

### Memory Tools

Beyond automatic context injection, the package provides six callable tools via `create_memory_tools()` that give the agent explicit control over its memory:

| Tool | Purpose |
|------|---------|
| `search_memory` | Search across all memory types (messages, entities, preferences) |
| `remember_preference` | Save a user preference with category and context |
| `recall_preferences` | Retrieve saved preferences by topic |
| `search_knowledge` | Query the knowledge graph for entities by type |
| `remember_fact` | Store a factual relationship as a Subject-Predicate-Object triple |
| `find_similar_tasks` | Retrieve similar past reasoning traces to learn from experience |

In Notebook 01, you'll use the **context provider** for automatic memory. In Notebook 02, you'll combine context providers with **memory tools** so the agent can both passively recall and actively manage its memory.

### Context Provider vs Memory Tools

| Aspect | Context Provider (Passive) | Memory Tools (Active) |
|--------|---------------------------|----------------------|
| **Invocation** | Automatic every turn | Agent decides when |
| **Direction** | Recall on entry, store on exit | Search, save, recall on demand |
| **Visibility** | Transparent to user | Visible in agent reasoning |
| **Control** | Framework-managed | Agent-managed |

The most effective pattern is using **both** together: the context provider handles automatic recall and storage on every turn, while memory tools give the agent explicit control for targeted operations like saving preferences or searching past reasoning traces.

> **Note:** Memory tools require explicit, prescriptive agent instructions (e.g., "You MUST call `remember_preference` when a user states a preference"). Without this, the LLM may acknowledge preferences verbally but skip the tool call.

## Prerequisites

Before starting, make sure you have:
- Completed **Lab 0** (Azure sign-in)
- Completed **Lab 1** (Neo4j Aura setup)
- Completed **Lab 4** (Codespace setup with environment variables configured)
- Completed **Lab 5** (Foundry Agents)
- Completed **Lab 6** (Context Providers)

## Lab Overview

This lab consists of two notebooks that demonstrate persistent agent memory:

### 01_memory_context_provider.ipynb - Memory Context Provider
Use Neo4j Agent Memory as a MAF context provider:
- Understand the three memory types: short-term, long-term, and reasoning
- Create a `Neo4jMicrosoftMemory` unified memory interface
- Configure the `Neo4jContextProvider` for automatic context injection
- See how conversation history persists across interactions
- Watch entities get extracted from conversations automatically

### 02_memory_tools_agent.ipynb - Agent with Memory Tools
Build an agent with explicit memory tools:
- Create callable memory tools with `create_memory_tools()`
- Let the agent search memory, save preferences, and recall facts
- Combine context providers with memory tools for full capability
- Build a conversational agent that learns and remembers

## Getting Started

### Select the Python Kernel

Before running any notebook, make sure you have the correct Python kernel selected:

1. Click **Select Kernel** in the top right of the notebook, then select **Python Environments...**
2. Select the **neo4j-azure-ai-workshop** environment (marked as Recommended)

### Work Through the Notebooks

1. Open the first notebook: `01_memory_context_provider.ipynb`
2. Work through each notebook in order
3. Notebook 2 builds on concepts from Notebook 1

## Entity Extraction Dependencies

The `neo4j-agent-memory` package uses a pipeline of entity extractors that run in order: **spaCy → GLiNER → LLM (OpenAI)**. For this workshop we add `spacy` and the `en_core_web_sm` model as project dependencies in `pyproject.toml` so the first stage succeeds and the pipeline doesn't fall through to the OpenAI-only LLM extractor (which requires `OPENAI_API_KEY`).

GLiNER was excluded because it depends on PyTorch (~400MB), which exceeds devcontainer disk limits. spaCy alone handles entity extraction for the workshop.

## Key Concepts

- **Short-Term Memory**: Conversation history with message chains and semantic search
- **Long-Term Memory**: Entities, preferences, and facts extracted from conversations
- **Reasoning Memory**: Traces of past agent reasoning and tool usage for learning
- **Neo4jMicrosoftMemory**: Unified interface combining context provider and chat history store
- **Memory Tools**: Callable `FunctionTool` instances for explicit memory operations (search, save, recall)
- **Entity Extraction**: Automatic identification of people, organizations, and concepts from messages
- **`create_memory_tools()`**: Factory function that creates bound memory tools for an agent

## Memory Types

| Memory Type | What It Stores | How It Helps |
|-------------|---------------|--------------|
| **Short-Term** | Recent messages, conversation chains | Maintains conversation context |
| **Long-Term** | Entities, preferences, facts | Personalizes responses over time |
| **Reasoning** | Past task traces, tool usage | Learns from previous successes/failures |

## Next Steps

After completing this lab, continue to [Lab 8 - Building a Knowledge Graph](../Lab_8_Knowledge_Graph) to learn how to build knowledge graphs from unstructured documents with embeddings and retrieval strategies.
