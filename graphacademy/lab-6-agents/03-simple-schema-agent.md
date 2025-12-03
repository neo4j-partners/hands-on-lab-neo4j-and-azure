# Simple Schema Agent

In this lesson, you'll build your first agent using the Microsoft Agent Framework. This agent will have a single tool that can retrieve and explain your graph database schema.

This lesson prepares you for Lab 6 Notebook 1, where you'll implement a simple schema agent with Microsoft Foundry.

## What is an Agent?

An **agent** is an AI system that can:
1. Understand natural language questions
2. Decide which tools to use
3. Execute those tools
4. Combine results into a coherent answer

**The Key Difference from Retrievers:**
- **Retriever:** You explicitly call it with a query
- **Agent:** It decides when and how to use retrievers as tools

## The Schema Tool

Your first agent will have one tool: `get_graph_schema`

**What it does:**
- Returns the complete graph schema
- Shows node types, properties, and relationships
- Helps users understand what data exists
- Enables exploration of the data model

**When the agent uses it:**
- Questions about database structure
- Questions about what entities exist
- Questions about relationships between nodes
- Questions about data model design

## How the Microsoft Agent Framework Works

The Microsoft Agent Framework provides:
- **AzureAIClient:** Connects to Microsoft Foundry
- **Agent creation:** Define agent instructions and tools
- **Tool definition:** Simple Python functions become agent tools
- **Streaming responses:** See agent thinking in real-time

**Basic Flow:**
```
User Question
    ↓
Agent analyzes question
    ↓
Agent decides: "I need the schema"
    ↓
Agent calls get_graph_schema tool
    ↓
Agent receives schema
    ↓
Agent generates answer using schema as context
    ↓
User sees answer
```

## Building the Agent

**Step 1: Define the Tool**

In the Microsoft Agent Framework, tools are simple Python functions:

```python
def get_graph_schema() -> str:
    """Get the schema of the graph database including node labels, relationships, and properties."""
    return get_schema(driver)
```

**Key Points:**
- Function name: clear and descriptive
- Docstring: tells the agent when to use this tool
- Return type: string (the schema text)
- Simple implementation: just call Neo4j's get_schema

**Step 2: Create the Agent**

```python
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential

# Create client
client = AzureAIClient(
    project_endpoint=config.project_endpoint,
    model_deployment_name=config.model_name,
    async_credential=AzureCliCredential(),
)

# Create agent with the schema tool
async with client.create_agent(
    name="workshop-schema-agent",
    instructions="You are a helpful assistant that can answer questions about a graph database schema.",
    tools=[get_graph_schema],
) as agent:
    # Use the agent
    async for update in agent.run_stream(query):
        if update.text:
            print(update.text, end="", flush=True)
```

**Step 3: Ask Questions**

The agent can now answer schema-related questions:

```python
query = "Summarise the schema of the graph database."
# Agent automatically uses get_graph_schema tool
```

## How the Agent Decides

The agent looks at:
1. **The user's question:** "Summarise the schema..."
2. **Available tools:** get_graph_schema with its docstring
3. **Tool description:** "Get the schema of the graph database..."

**Agent reasoning:**
- Question asks about "schema"
- Tool description mentions "schema of the graph database"
- Match! Use this tool
- Call get_graph_schema()
- Use returned schema to answer

## Example Interactions

**Question:** "What types of nodes are in the database?"
```
Agent thinks: This is about database structure
Agent action: Call get_graph_schema()
Agent response: "The database contains the following node types:
- Company: Properties include name, ticker
- RiskFactor: Properties include name
- AssetManager: Properties include managerName
..."
```

**Question:** "How are companies related to risk factors?"
```
Agent thinks: This is about relationships in the schema
Agent action: Call get_graph_schema()
Agent response: "Companies are related to risk factors through the
FACES_RISK relationship. The pattern is:
(:Company)-[:FACES_RISK]->(:RiskFactor)"
```

**Question:** "What questions can I ask about this database?"
```
Agent thinks: Need to understand schema to suggest questions
Agent action: Call get_graph_schema()
Agent response: "Based on the schema, you can ask questions like:
- Which companies face specific risk factors?
- What asset managers own which companies?
- What products are mentioned by companies?
..."
```

## Tool Definition Best Practices

**Good Tool Definitions:**
```python
✓ def get_graph_schema() -> str:
    """Get the schema of the graph database including node labels, relationships, and properties."""
    return get_schema(driver)
```
- Clear function name
- Descriptive docstring
- Simple implementation

**Poor Tool Definitions:**
```python
✗ def tool1() -> str:
    """A tool."""
    return data
```
- Vague name
- Unclear purpose
- Agent won't know when to use it

**Docstring Guidelines:**
- Describe what the tool does
- Mention key entities or concepts
- Use language that matches user questions
- Be specific but concise

## Single-Tool vs Multi-Tool Agents

**Your Current Agent:**
- 1 tool: get_graph_schema
- Answers: Schema and structure questions
- Can't: Search documents, query data

**In Next Lessons:**
- Add more tools (vector search, Text2Cypher)
- Agent chooses between multiple tools
- Can handle any type of question

**The Progression:**
1. **This lesson:** 1-tool agent (schema only)
2. **Next lesson:** 2-tool agent (schema + vector search)
3. **Following lesson:** 3-tool agent (schema + vector + Text2Cypher)

## When to Use a Simple Agent

**Good Use Cases:**
- Schema exploration and documentation
- Data model Q&A
- Teaching users about the database
- First step before more complex agents

**Limitations:**
- Can't search document content
- Can't query specific facts
- Can't traverse relationships
- Single purpose only

**Next Step:**
Add more tools to handle different question types!

## Check Your Understanding

### What determines when an agent uses a tool?

**Options:**
- [ ] The order tools are defined
- [ ] Random selection
- [x] The tool's docstring and function name
- [ ] User explicitly specifies the tool

<details>
<summary>Hint</summary>
Think about what information the agent has about each tool.
</details>

<details>
<summary>Show Answer</summary>
**The tool's docstring and function name**. The agent analyzes the user's question and compares it to each tool's function name and docstring description. It uses semantic matching to decide which tool is most appropriate for answering the question.
</details>

### Why start with a simple single-tool agent?

**Options:**
- [ ] It's faster to execute
- [x] It's easier to understand how agents work
- [ ] Multi-tool agents don't work as well
- [ ] Single tools are more accurate

<details>
<summary>Hint</summary>
Consider the learning path and complexity.
</details>

<details>
<summary>Show Answer</summary>
**It's easier to understand how agents work**. Starting with a single tool lets you focus on understanding the core concepts: how agents analyze questions, how they decide to use tools, and how they incorporate tool results into answers. Once you understand this with one tool, adding more tools is straightforward.
</details>

## Summary

In this lesson, you learned to build a simple schema agent:

**Key Concepts:**
- Agents analyze questions and choose appropriate tools
- Tools are defined as Python functions with descriptive docstrings
- Microsoft Agent Framework handles the tool selection logic
- Single-tool agents are perfect for focused use cases

**What You Built:**
- Simple agent with one tool (get_graph_schema)
- Tool that retrieves and explains database schema
- Foundation for more complex multi-tool agents

**How It Works:**
- User asks schema-related question
- Agent recognizes it needs schema information
- Agent calls get_graph_schema tool
- Agent uses schema to generate helpful answer

**Advantages:**
- Simple to implement and understand
- Clear, focused purpose
- Great for learning agent concepts
- Useful for schema exploration

**Limitations:**
- Only handles schema questions
- Can't search document content
- Can't query specific facts
- Single-purpose design

In Lab 6 Notebook 1, you'll implement this simple schema agent and see how it responds to different schema-related questions. In the next lesson, you'll enhance this agent by adding a vector search tool, enabling it to answer both schema AND content questions.

---

**Navigation:**
- [← Previous: Microsoft Agent Framework](02-microsoft-agent-framework.md)
- [↑ Back to Module 3](README.md)
- [Next: Vector Graph Agent →](04-vector-graph-agent.md)
