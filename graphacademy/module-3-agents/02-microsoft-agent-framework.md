# Microsoft Agent Framework Agent

## Introduction

In this lesson, you'll build your first agent using the Microsoft Agent Framework that can interact with your Neo4j knowledge graph.

**Key insight:** The agent chooses which tool to use based on your question.

**When you ask: _"Summarize the schema of the graph database"_**

1. **Agent receives** your natural language question
2. **Agent decides** to use the `get_graph_schema` tool
3. **Tool executes** and returns the Neo4j schema
4. **Agent processes** the schema and creates a summary
5. **Agent responds** in natural language

## Why This is an Agent Architecture

The Microsoft Agent Framework implements a **Model-Based, Goal-Based Agent** according to classical AI definitions.

### Mapping Framework Components to Agent Theory

| Agent Component | Framework Implementation | How It Works |
|-----------------|-------------------------|--------------|
| **Sensors (Current)** | `ChatMessage` input, user queries | Agent receives current user message |
| **Sensors (Historical)** | `AgentThread`, message stores | Agent maintains conversation history |
| **Percept Sequence** | Thread message history | Complete record of what agent has perceived |
| **Agent Function** | `ChatAgent.run()` + LLM reasoning | Maps percept history → action decision |
| **Actuators** | Tools (Python functions) | Actions agent can perform on environment |
| **Internal State** | `AgentThread` with context | Agent's model of conversation state |

### Agent Classification

**Model-Based Agent:**
- ✅ Maintains internal state (conversation thread)
- ✅ Tracks world state (message history, context)
- ✅ Uses percept sequence to inform decisions

**Goal-Based Agent:**
- ✅ Explicit goals via `instructions` parameter
- ✅ Selects actions (tools) based on achieving goals
- ✅ Reasons about which tool best achieves the objective

**Example:**

```python
# Goal-based agent with explicit objectives
agent = ChatAgent(
    chat_client=client,
    instructions="""
    Your goal: Help users understand their Neo4j graph database.

    - Use schema tool for structure questions
    - Use vector search for semantic exploration
    - Use text2cypher for precise queries
    """,  # ← EXPLICIT GOALS
    tools=[get_graph_schema, vector_search, text2cypher]  # ← ACTUATORS
)

# Agent perceives user query
thread = agent.get_new_thread()  # ← PERCEPT SEQUENCE
result = await agent.run(
    "How are Products related to Companies?",  # ← CURRENT PERCEPT
    thread=thread
)

# Behind the scenes:
# 1. Agent perceives: question about relationships
# 2. Agent reasons: schema tool best for structure questions
# 3. Agent acts: calls get_graph_schema()
# 4. Agent responds: formats schema info as natural language
```

### The ReAct Loop: How Agents Reason

The framework implements the **ReAct** (Reasoning + Acting) pattern:

**ReAct Cycle:**

```
1. Thought: "User wants relationship information"
2. Action: Call get_graph_schema()
3. Observation: Receives schema with Product→SUPPLIED_BY→Company
4. Thought: "I have the information needed"
5. Action: Return formatted answer to user
```

This iterative reasoning allows the agent to:
- Break complex queries into steps
- Use multiple tools in sequence
- Recover from errors by trying different approaches
- Provide transparent reasoning

The framework automatically handles this loop (up to 40 iterations by default) until the agent completes its goal or determines it cannot proceed.

## Framework Features

### Agent Creation Patterns

The Microsoft Agent Framework provides two main approaches for creating agents.

**Using ChatAgent (recommended for most cases):**
```python
# Pre-built agent - simplest and most common approach
agent = ChatAgent(
    chat_client=AzureAIClient(...),
    name="my-agent",
    instructions="You are a helpful assistant",
    tools=[get_graph_schema],
)
```

**Custom agents - inherit from BaseAgent:**
```python
# For advanced customization
class MyCustomAgent(BaseAgent):
    async def run(self, messages): ...
    async def run_stream(self, messages): ...
```

**When to use each:**
- **ChatAgent**: Use for 95% of cases - simple, powerful, and production-ready
- **BaseAgent**: Inherit when you need custom lifecycle hooks or specialized behavior

Both synchronous (`run()`) and streaming (`run_stream()`) execution modes are supported.

### Automatic Tool System

Tools are plain Python functions - the framework extracts function names, docstrings, and type hints to automatically generate JSON schemas for LLM function calling.

**Tool definition example:**

```python
def get_graph_schema() -> str:
    """Get the schema of the graph database including node labels, relationships, and properties."""
    return get_schema(driver)
```

The framework:
1. Reads the function docstring for the tool description
2. Extracts parameter types from type hints
3. Generates JSON schema for the LLM
4. Handles invocation, timeout management, and error recovery

**Built-in tool types:**
- **AIFunction**: Decorator-based custom tools (`@ai_function`)
- **HostedCodeInterpreterTool**: Sandboxed code execution
- **HostedFileSearchTool**: Document search capabilities
- **HostedWebSearchTool**: Web search integration
- **MCPTool**: Model Context Protocol server integration

**Why Tools are Actuators:**

In agent terminology, tools are the **actuators** - the mechanisms through which your agent acts on its environment:

- `get_graph_schema()` - Action: Retrieve database structure
- `vector_search()` - Action: Perform semantic search
- `execute_cypher()` - Action: Query graph database

The agent (via the LLM) decides which actuator to use based on:
1. User's question (current percept)
2. Conversation history (percept sequence)
3. Goals (instructions)
4. Available actions (tools list)

### Thread Management for Conversations

The framework supports both single-turn and multi-turn conversations:

**Single-turn (automatic thread):**
```python
# Framework creates thread automatically
async for update in agent.run_stream(query):
    print(update.text)
```

**Multi-turn conversations:**
```python
# Create and reuse thread for conversation context
thread = agent.get_new_thread()

# First message
result1 = await agent.run("What products are available?", thread=thread, store=False)

# Follow-up maintains context
result2 = await agent.run("Tell me more about the first one", thread=thread, store=False)
```

**Thread storage options:**
- `store=False`: Keep messages in memory only (faster, no persistence)
- `store=True`: Persist to Microsoft Foundry (survives restarts, visible in portal)

### Built-in Observability

OpenTelemetry integration provides distributed tracing and metrics out of the box:

**Automatic tracking:**
- Span creation using GenAI semantic conventions
- Token usage histograms and operation duration metrics
- Chat message logging with timestamps
- Exporters for OTLP, Azure Monitor, and custom backends

When using Microsoft Foundry, traces and metrics automatically flow to Application Insights for visualization in the portal.

### Provider Support

The same agent code works across multiple LLM providers:

| Provider | Package | Description |
|----------|---------|-------------|
| OpenAI | `agent-framework` (core) | GPT models via OpenAI API |
| Azure OpenAI | `agent-framework` (core) | GPT models via Azure endpoints |
| Microsoft Foundry | `agent-framework-azure-ai` | Service-managed agents with portal integration |
| Anthropic | `agent-framework-anthropic` | Claude models |

Switching providers requires only changing the client class - agent code remains unchanged.

### Multi-Agent Orchestration

The framework includes graph-based workflow orchestration for complex scenarios:

**Orchestration patterns:**
- **Sequential**: Agents run in order, passing results between steps
- **Concurrent**: Parallel execution with fan-in/fan-out patterns
- **Group Chat**: Multi-agent discussion with AI-powered speaker selection
- **Handoff**: Agent-to-agent transfers based on conversation context

Workflows support checkpointing, event streaming, and resumable execution.

## Try These Questions

**Schema exploration:**

- _"Summarize the schema of the graph database"_
- _"How are Products related to other entities?"_
- _"What questions can I answer using this graph database?"_

**Perfect for understanding data structure before building queries!**

## Microsoft Foundry Integration

The Microsoft Agent Framework is **not** just a wrapper around Azure SDKs - it's a complete agent framework that can operate independently with any supported LLM provider. However, when used with Microsoft Foundry, it unlocks additional enterprise capabilities.

### Registration and Lifecycle

When you create an agent with Microsoft Foundry:

1. `client.create_agent()` returns an async context manager
2. Entering the context sends a creation request to Microsoft Foundry
3. Microsoft Foundry creates the agent and returns an agent ID
4. The agent appears in the portal under your project
5. Exiting the context automatically deletes the agent (cleanup)

**No manual ID management required** - the framework handles everything.

```python
# Agent lifecycle managed automatically
async with client.create_agent(
    name="schema-agent",
    instructions="You are a helpful assistant...",
    tools=[get_graph_schema],
) as agent:
    # Agent exists and is registered
    result = await agent.run(query)
# Agent automatically cleaned up
```

### Enterprise Features

**When used with Microsoft Foundry:**
- **Portal Visibility**: Agents appear in the Microsoft Foundry portal
- **Monitoring**: Traces and metrics flow to Application Insights
- **Evaluation**: Agent runs can be analyzed using Foundry evaluation tools
- **Server-Side State**: Threads and messages can persist to Azure services
- **Human-in-the-Loop**: Approval workflows for sensitive tool executions

**The framework provides two Azure client classes:**

| Client | SDK | Use Case |
|--------|-----|----------|
| `AzureAIAgentClient` | `azure-ai-agents` (V1) | Legacy Agents API |
| `AzureAIClient` | `azure-ai-projects` (V2) | Current recommended path |

This workshop uses `AzureAIClient` (V2) which aligns with current Microsoft documentation.

### Advanced Features

**Middleware Pipeline:**

Three middleware types for interception and modification:
- **AgentMiddleware**: Intercepts `agent.run()` calls
- **ChatMiddleware**: Intercepts LLM requests
- **FunctionMiddleware**: Intercepts tool execution

Use cases: logging, filtering, authentication, caching

**Context Providers:**

Dynamic injection of instructions, messages, and tools before execution:
- **ContextProvider**: Single source of dynamic context
- **AggregateContextProvider**: Combines multiple context providers

Perfect for adding user-specific instructions or session data.

## Summary

In this lesson, you built your first agent with schema introspection capabilities:

**Key Concepts:**

- **Schema tool:** Database structure exploration through conversation
- **Agent setup:** Microsoft Agent Framework with introspection tool
- **Tool definition:** Python functions with docstrings become agent tools
- **Streaming responses:** Real-time output using `run_stream()`
- **Graph structure:** Understanding nodes, relationships, and properties

**What You Built:**

- Agent that can answer questions using the database schema
- Conversational interface to graph database schema
- Foundation for adding more retriever tools
- Integration with Microsoft Foundry for monitoring

**Limitations:**

- Only retrieves schema (nodes and relationships) defined in database
- No precise queries or aggregations
- Single tool agent

In the next lesson, you will enhance your agent by adding the Vector + Cypher Retriever tool for contextual relationships and richer answers.

## What You'll Build

Open the notebook: `02_01_simple_agent.ipynb`

**This agent:**

- Uses the Microsoft Agent Framework for agent functionality
- Connects to Microsoft Foundry for agent registration and monitoring
- Integrates with your Neo4j database
- Has a single tool: `get_graph_schema`
- Can answer questions about your graph structure

**The goal:** Understand basic agent architecture before adding retriever capabilities.

**Agent Architecture:**

```python
# 1. Initialize Azure AI Client with credentials
async with AzureCliCredential() as credential:
    client = AzureAIClient(
        project_endpoint=config.project_endpoint,
        model_deployment_name=config.model_name,
        async_credential=credential,
    )

    # 2. Define tool as Python function
    def get_graph_schema() -> str:
        """Get the schema of the graph database including node labels, relationships, and properties."""
        return get_schema(driver)

    # 3. Create agent with tool
    async with client.create_agent(
        name="schema-agent",
        instructions="You are a helpful assistant...",
        tools=[get_graph_schema],
    ) as agent:
        # 4. Stream agent responses
        async for update in agent.run_stream(query):
            if update.text:
                print(update.text, end="", flush=True)
```

---

**Navigation:**
- [← Previous: What is an Agent](01-what-is-an-agent.md)
- [↑ Back to Module 3](README.md)
- [Next: Simple Schema Agent →](03-simple-schema-agent.md)
