# Lab 5 - Foundry Agents

In this lab, you'll build your first agents using the **Microsoft Agent Framework (MAF)** with Microsoft Foundry.

## What is the Microsoft Agent Framework?

The [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) is a framework for building AI agents that can reason, use tools, and maintain context across conversations. At its core, it solves a fundamental problem: LLMs are stateless. Every time you send a message, the model has no memory of previous interactions and no access to your data. The agent framework bridges this gap by orchestrating a lifecycle around each LLM invocation — injecting relevant knowledge before the call (via context providers), giving the model the ability to take actions (via tools), and extracting useful information from the response afterward. This turns a bare LLM into an agent that can retrieve, reason, and act.

The framework provides:

- **Agents** — AI systems that receive instructions, use tools, and generate responses via an LLM
- **Tools** — Python functions the agent can decide to call based on the user's query
- **Context Providers** — Hooks that run automatically before/after each agent invocation to inject or extract information
- **Sessions** — Per-conversation containers with persistent state that survives across turns
- **Middleware** — Interceptors for logging, validation, and custom processing at the agent, chat, and function layers

### What is a Context Provider?

A context provider is a pluggable component that participates in the **context engineering pipeline** — the practice of dynamically managing what context (history, RAG results, instructions, tools) reaches the model. Rather than hardcoding all context upfront, context providers let you compose independent concerns — memory, search, user preferences — into a single agent without them knowing about each other.

Each provider extends `BaseContextProvider` and implements two lifecycle hooks:

- **`before_run()`** — Called before each model invocation. Add instructions, messages, or tools to the `SessionContext`.
- **`after_run()`** — Called after each model invocation. Process the response — extract data, store memories, update state.

Providers are **composable**: you register multiple providers when creating an agent, each identified by a unique `source_id`. The framework runs all `before_run()` hooks in order, invokes the model, then runs all `after_run()` hooks in reverse order. Each provider's contributions are tracked by source, so providers can filter or build on each other's context. The framework ships with several built-in providers (Azure AI Search, Mem0 memory, Neo4j graph), but writing your own is straightforward.

### Tools vs Context Providers

This is the most important distinction in the framework:

| | Tools | Context Providers |
|---|---|---|
| **When they run** | Only when the agent decides to call them | Automatically before every agent invocation |
| **How they work** | Agent sees the function name + docstring and chooses whether to call it | `before_run()` injects instructions/messages into the context |
| **Best for** | On-demand actions (lookups, calculations, API calls) | Always-available background knowledge (RAG, memory, user preferences) |

In Notebook 01, you'll use **tools**. In Notebook 02, you'll use **context providers**. The rest of the workshop combines both approaches with Neo4j.

### Architecture

```
Agent.run(query)
    │
    ├── 1. Context Providers: before_run()
    │       └── Inject instructions, messages, and tools into SessionContext
    │
    ├── 2. LLM Invocation
    │       ├── Process instructions + context + user query
    │       ├── Decide which tools to call (if any)
    │       └── Generate response
    │
    └── 3. Context Providers: after_run()
            └── Extract data, store messages, update session state
```

## Prerequisites

Before starting, make sure you have:
- Completed **Lab 0** (Azure sign-in)
- Completed **Lab 4** (Codespace setup with environment variables configured)

## Lab Overview

### 01_simple_agent.ipynb - Simple Company Info Agent
Build your first agent using the Microsoft Agent Framework:
- Connect to Microsoft Foundry using `AzureOpenAIResponsesClient`
- Define a tool as a Python function with a docstring and type annotations
- Create an agent that looks up company information from SEC 10-K filings
- Stream agent responses in real-time

### 02_context_provider.ipynb - Introduction to Context Providers
Learn how context providers automatically inject context before each agent invocation:
- Build a `UserInfoMemory` context provider using `BaseContextProvider`
- Use `before_run()` to inject dynamic instructions based on session state
- Use `after_run()` to extract structured data from conversations with Pydantic
- Inspect `session.state` to see extracted data persist across turns

## Getting Started

### Select the Python Kernel

Before running the notebook, make sure you have the correct Python kernel selected:

1. Click **Select Kernel** in the top right of the notebook, then select **Python Environments...**
2. Select the **neo4j-azure-ai-workshop** environment (marked as Recommended)

### Work Through the Notebooks

1. Open `01_simple_agent.ipynb` — build an agent with tools
2. Open `02_context_provider.ipynb` — learn about context providers
3. Read through the code and run each cell

## Key Concepts

- **`AzureOpenAIResponsesClient`** — Connects to Azure OpenAI via Microsoft Foundry
- **`as_agent()`** — Creates a local agent with a name, instructions, tools, and optional context providers
- **`run_stream()` / `run()`** — Sends a query to the agent and returns a streaming or complete response
- **`BaseContextProvider`** — Base class for building context providers with `before_run()` and `after_run()` lifecycle hooks
- **`SessionContext`** — Per-invocation context; providers use `extend_instructions()` and `extend_messages()` to inject data
- **`AgentSession`** — Per-conversation container with a `state` dict that persists across turns
- **`Annotated` + `Field`** — Type annotations that describe tool parameters to the agent

## Next Steps

After completing this lab, continue to [Lab 6 - MAF Context Providers](../Lab_6_Context_Providers) to use `Neo4jContextProvider` for automatic knowledge graph retrieval.
