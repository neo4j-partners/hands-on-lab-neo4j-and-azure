# The Microsoft Agent Framework

## Introduction

The Microsoft Agent Framework provides the infrastructure for building intelligent agents that can use tools, maintain conversations, and integrate with Azure services.

In this lesson, you'll understand how the framework works and what components you'll use to build your agent.

## Framework Components

**AzureAIClient**: Connects to Microsoft Foundry services and handles model interactions.

**ChatAgent**: Pre-built agent class that handles tool selection, conversation flow, and response generation.

**Tools**: Python functions with docstrings that become callable by the agent.

**Threads**: Conversation history for multi-turn interactions.

## Creating an Agent

Basic pattern for agent creation:

```python
async with client.create_agent(
    name="graphrag-agent",
    instructions="You are a helpful assistant that answers questions about a knowledge graph.",
    tools=[get_graph_schema, search_content, query_database],
) as agent:
    # Use the agent
    async for update in agent.run_stream(query):
        if update.text:
            print(update.text, end="", flush=True)
```

**Key elements**:
- `instructions`: Tell the agent its purpose and how to behave
- `tools`: List of functions the agent can call
- `run_stream`: Execute and stream responses

## How Tool Selection Works

Tools are defined as Python functions with descriptive docstrings:

```python
def get_graph_schema() -> str:
    """Get the schema of the graph database including node labels,
    relationships, and properties."""
    return get_schema(driver)
```

The framework:
1. Reads the function name and docstring
2. Registers the tool with the agent
3. When a question arrives, matches it semantically to tool descriptions
4. Calls the best-matching tool

**Why docstrings matter**: The agent reads them to decide when to use each tool. A vague docstring like "Search the database" gives poor guidance. A specific one like "Get answers to factual questions about companies, including counts, lists, and specific attributes" guides selection precisely.

## The ReAct Loop

The framework implements the **ReAct** pattern automatically:

```
User: "How many companies are in the database?"
    ↓
Agent thinks: "This asks for a count—I should use the database query tool"
    ↓
Agent calls: query_database("How many companies are in the database?")
    ↓
Agent observes: Result = 523
    ↓
Agent responds: "There are 523 companies in the database."
```

This loop can iterate multiple times for complex questions requiring multiple tools.

## Thread Management

For multi-turn conversations:

```python
# Create a thread for conversation context
thread = agent.get_new_thread()

# First message
result1 = await agent.run("What companies are in the database?", thread=thread)

# Follow-up maintains context
result2 = await agent.run("Tell me more about the first one", thread=thread)
```

The thread preserves conversation history, enabling context-aware follow-ups.

## Agent Instructions

Instructions guide agent behavior:

**Generic (less effective)**:
```
"You are a helpful assistant."
```

**Specific (more effective)**:
```
"You are a helpful assistant that answers questions about a knowledge graph
containing SEC filings data. You have three tools:

1. get_graph_schema - Use for questions about data structure
2. search_content - Use for semantic questions about topics
3. query_database - Use for specific facts, counts, and lookups

Choose the appropriate tool based on the question type. If unsure,
start with schema exploration."
```

Specific instructions improve tool selection accuracy.

## Streaming Responses

For real-time output:

```python
async for update in agent.run_stream(query):
    if update.text:
        print(update.text, end="", flush=True)
```

Users see responses as they're generated, rather than waiting for completion.

## Summary

The Microsoft Agent Framework provides:
- **AzureAIClient** for Microsoft Foundry integration
- **ChatAgent** for pre-built agent functionality
- **Automatic tool selection** based on docstrings
- **ReAct pattern** for reasoning and acting
- **Thread management** for conversations
- **Streaming** for real-time responses

In the next lesson, you'll use these components to build your agent progressively—starting with one tool and adding more.

---

**Navigation:**
- [← Previous: From Retrievers to Agents](01-from-retrievers-to-agents.md)
- [↑ Back to Lab 6](README.md)
- [Next: Building Your Agent →](03-building-your-agent.md)
