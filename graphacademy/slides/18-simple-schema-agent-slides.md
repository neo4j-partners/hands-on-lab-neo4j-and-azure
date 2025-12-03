---
marp: true
theme: default
paginate: true
---

<style>
section {
  --marp-auto-scaling-code: false;
}

li {
  opacity: 1 !important;
  animation: none !important;
  visibility: visible !important;
}

/* Disable all fragment animations */
.marp-fragment {
  opacity: 1 !important;
  visibility: visible !important;
}

ul > li,
ol > li {
  opacity: 1 !important;
}
</style>


# Simple Schema Agent

Module 3, Lesson 3

**Note:** This slide will be renumbered in final sequencing

---

## What is an Agent?

An **agent** is an AI system that can:

1. **Understand** natural language questions
2. **Decide** which tools to use
3. **Execute** those tools
4. **Combine** results into a coherent answer

**Key Difference from Retrievers:**
- **Retriever:** You explicitly call it
- **Agent:** It decides when and how to use retrievers as tools

---

## Agents vs Retrievers

<div style="display: flex; gap: 2rem;">

<div style="flex: 1;">

### Direct Retriever Use

```python
# You decide and call
retriever = VectorRetriever(...)
results = retriever.search(query)
```

**You control:**
- Which retriever to use
- When to call it
- How to process results

</div>

<div style="flex: 1;">

### Agent with Tools

```python
# Agent decides and calls
agent = create_agent(
    tools=[schema, vector, text2cypher]
)
result = agent.run(query)
```

**Agent controls:**
- Which tool to use
- When to call it
- How to combine results

</div>

</div>

**Agents add intelligent tool selection!**

---

## Your First Agent: Schema Tool Only

**Start Simple:** One tool, one capability

**The Schema Tool:**
- Returns complete graph schema
- Shows node types, properties, relationships
- Helps users understand data model

**Perfect First Tool Because:**
- Non-ambiguous: schema is always the same
- Deterministic: same query, same result
- Foundation: users need to know what's queryable

---

## The Schema Tool

**As a Python function:**

```python
def get_graph_schema() -> str:
    """Get the schema of the graph database including
    node labels, relationships, and properties."""
    return get_schema(driver)
```

**Key Parts:**
- **Function name:** Clear, descriptive
- **Docstring:** Tells agent when to use it
- **Return type:** String (the schema text)
- **Implementation:** Calls Neo4j's get_schema

**The docstring is critical!** It's how the agent knows what this tool does.

---

## When the Agent Uses Schema Tool

**These questions trigger the schema tool:**

✅ "What entities exist in the database?"
✅ "How are Companies related to other nodes?"
✅ "What properties does the Company node have?"
✅ "Summarize the graph database schema"
✅ "What questions can I answer with this data?"

**The agent reads:**
- Question: "What entities exist..."
- Tool docstring: "Get the schema of the graph database including node labels..."
- Decision: ✅ Use schema tool!

---

## Creating the Agent with Microsoft Agent Framework

**Step 1: Initialize Azure AI Client**

```python
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential

client = AzureAIClient(
    project_endpoint=config.project_endpoint,
    model_deployment_name=config.model_name,
    async_credential=AzureCliCredential(),
)
```

**Connects to Microsoft Foundry** for agent registration and monitoring.

---

## Creating the Agent (continued)

**Step 2: Create Agent with Tools**

```python
async with client.create_agent(
    name="workshop-schema-agent",
    instructions="You are a helpful assistant that can answer
                 questions about a graph database schema.",
    tools=[get_graph_schema],  # Single tool
) as agent:
    # Agent is now created and registered
    query = "What entities are in the database?"

    # Stream the agent's response
    async for update in agent.run_stream(query):
        if update.text:
            print(update.text, end="", flush=True)
```

---

## How the Agent Works

**7-Step Process:**

```
User: "What entities are in the database?"
    ↓
[1. AGENT RECEIVES QUESTION]
    Parses natural language
    ↓
[2. AGENT ANALYZES]
    "User wants to know about database structure"
    ↓
[3. AGENT EVALUATES TOOLS]
    Checks get_graph_schema docstring
    ↓
[4. AGENT DECIDES]
    "I need to use the schema tool"
    ↓
[5. AGENT CALLS TOOL]
    get_graph_schema() executes
    ↓
[6. AGENT RECEIVES SCHEMA]
    Full schema text returned
    ↓
[7. AGENT GENERATES ANSWER]
    "The database contains Companies, RiskFactors, AssetManagers..."
```

---

## Agent Instructions Matter

**The `instructions` parameter guides agent behavior:**

```python
instructions = """You are a helpful assistant that can answer
questions about a graph database schema.

When users ask about the database structure, use the
get_graph_schema tool to retrieve accurate information.

Explain the schema in clear, non-technical language."""
```

**Good instructions:**
- Define the agent's role
- Explain when to use tools
- Set tone and style

---

## Streaming Responses

**Why stream?**
- See agent thinking in real-time
- Better user experience (no waiting)
- Can interrupt long responses
- Watch tool selection happen

```python
async for update in agent.run_stream(query):
    if update.text:
        print(update.text, end="", flush=True)
```

**Each update contains:**
- Partial text from the agent
- Tool call information
- Completion status

---

## Example Questions for Schema Agent

Try these questions with your schema agent:

**Structure Questions:**
- "Summarize the schema of the graph database"
- "How are Products related to other entities?"
- "What properties does the Company node have?"

**Capability Questions:**
- "What questions can I answer using this graph database?"
- "What kind of information is stored in the database?"

**Relationship Questions:**
- "How are Companies connected to RiskFactors?"

---

## What the Agent Returns

**For:** "Summarize the graph database schema"

**Agent Response:**
```
The graph database contains several types of entities:

**Companies**: Stores information about corporations including
their names and tickers.

**Risk Factors**: Represents various risks that companies face,
identified by name.

**Asset Managers**: Financial institutions that own shares in
companies, tracked by manager name.

**Relationships:**
- Companies FACE risk factors
- Asset Managers OWN companies
- Companies FILE documents

This structure allows you to query company risks, ownership
patterns, and document relationships.
```

---

## Advantages of Single-Tool Agent

**Why start with just one tool?**

✅ **Simple to understand** - Clear cause and effect
✅ **Easy to debug** - Only one tool can be called
✅ **Low ambiguity** - Agent rarely makes wrong choice
✅ **Foundation** - Learn agent basics before complexity
✅ **Useful** - Schema tool is genuinely helpful

**Next Step:** Add more tools for more capabilities!

---

## Limitations of Single-Tool Agent

**What it CAN'T do:**

❌ Answer questions about specific companies
❌ Perform semantic search
❌ Execute complex queries
❌ Aggregate data
❌ Find related entities

**For:** "What are Apple's main products?"
**Agent:** "I can show you the schema, but I can't search for specific companies."

**Solution:** Add retriever tools! (Next lessons)

---

## Monitoring with Microsoft Foundry

**When using Microsoft Foundry, you get:**

- **Agent registration** in the portal
- **Tool call tracking** - see which tools are used
- **Performance metrics** - response times, token usage
- **Conversation logs** - full message history
- **Error tracking** - failed tool calls, issues

**Access in Azure portal** under your Microsoft Foundry project.

---

## Best Practices for Tool Definitions

**1. Clear Function Names**
```python
✅ get_graph_schema()
❌ schema()
```

**2. Descriptive Docstrings**
```python
✅ """Get the schema of the graph database including node labels,
    relationships, and properties."""
❌ """Get schema"""
```

**3. Appropriate Return Types**
```python
✅ -> str  # Clear, simple
❌ -> Any  # Ambiguous
```

---

## Summary

Simple Schema Agent demonstrates core agent concepts:

**Key Concepts:**
- Agents decide which tools to use
- Tools are Python functions with docstrings
- Docstrings guide agent's tool selection
- Microsoft Agent Framework handles orchestration
- Start simple (one tool) before adding complexity

**What You Built:**
- Agent that explores graph database schema
- Conversational interface to data model
- Foundation for multi-tool agents

---

## Next Steps

In the next lesson, you will enhance your agent by adding a Vector + Cypher Retriever tool, enabling it to answer questions about companies, products, and risks using semantic search combined with graph traversal.

**Lab 6 Notebook 1:** Build your simple schema agent

**Then:** Add more tools for comprehensive GraphRAG capabilities!
