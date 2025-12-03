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


# Microsoft Agent Framework Agent

---

## Introduction

In this lesson, you'll build your first agent using the Microsoft Agent Framework that can interact with your Neo4j knowledge graph.

**Key insight:** The agent chooses which tool to use based on your question.

**When you ask: _"Summarize the schema of the graph database"_**

1. **Agent receives** your natural language question
2. **Agent decides** to use the `get_graph_schema` tool
3. **Tool executes** and returns the Neo4j schema
4. **Agent processes** the schema and creates a summary
5. **Agent responds** in natural language

---

## What You'll Build

Open the notebook: `02_01_simple_agent.ipynb`

**This agent:**

- Uses the Microsoft Agent Framework for agent functionality
- Connects to Microsoft Foundry for agent registration and monitoring
- Integrates with your Neo4j database
- Has a single tool: `get_graph_schema`
- Can answer questions about your graph structure

**The goal:** Understand basic agent architecture before adding retriever capabilities.

---

## Agent Architecture

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
        """Get the schema of the graph database including
        node labels, relationships, and properties."""
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

## Try These Questions

**Schema exploration:**

- _"Summarize the schema of the graph database"_
- _"How are Products related to other entities?"_
- _"What questions can I answer using this graph database?"_

**Perfect for understanding data structure before building queries!**

---

## Summary

In this lesson, you built your first agent with schema introspection capabilities:

**Key Concepts:**

- **Schema tool:** Database structure exploration through conversation
- **Agent setup:** Microsoft Agent Framework ChatAgent with introspection tool
- **Tool definition:** Python functions with docstrings become agent tools
- **Streaming responses:** Real-time output using `run_stream()`
- **Graph structure:** Understanding nodes, relationships, and properties

---

## What You Built

- Agent that can answer questions using the database schema
- Conversational interface to graph database schema
- Foundation for adding more retriever tools
- Integration with Microsoft Foundry for monitoring

**Limitations:**

- Only retrieves schema (nodes and relationships) defined in database
- No precise queries or aggregations
- Single tool agent

In the next lesson, you will enhance your agent by adding the Vector + Cypher Retriever tool for contextual relationships and richer answers.
