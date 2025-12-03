# From Retrievers to Agents

## The Problem

You know three retrieval patterns:
- **Vector** for semantic content
- **Vector Cypher** for content + relationships
- **Text2Cypher** for precise facts

But users don't know about retriever types. They just ask questions:
- "What is Apple's strategy?"
- "How many companies are in the database?"
- "Which asset managers own companies facing cyber risks?"

Each question needs a different retriever. How do you build a system that chooses automatically?

## The Solution: Agents

## What is an Agent?

In AI terms, an agent has four components:

**Perception**: Receives input from its environment
- User questions
- Conversation history
- Available tools and their descriptions

**Reasoning**: Analyzes the situation and decides what to do
- What kind of question is this?
- Which tool would best answer it?
- Do I need multiple tools?

**Action**: Executes decisions
- Calls the selected tool
- Processes results
- Potentially calls additional tools

**Response**: Returns output
- Formats results as natural language
- Maintains conversation context

## How Agents Choose Tools

The agent selects tools based on **semantic matching** between:
- The user's question
- Tool descriptions (names and docstrings)

When you ask "How many companies are there?":
1. Agent sees available tools and their descriptions
2. Matches "how many" and "companies" to a tool that says "query the database for counts and facts"
3. Selects that tool
4. Executes and returns the answer

This is why **descriptive tool definitions matter**—they guide selection.

## Tools are Retrievers

Your agent's tools are based on the retrievers you learned in Lab 5:

| Tool | Based On | When Agent Uses It |
|------|----------|-------------------|
| Schema Tool | Graph schema introspection | Questions about data structure |
| Semantic Search Tool | Vector Retriever | Content and concept questions |
| Database Query Tool | Text2Cypher Retriever | Facts, counts, specific lookups |

The agent wraps each retriever as a callable tool with a description.

**What about Vector Cypher Retriever?**

You learned three retrievers in Lab 5, but agents typically use two retrieval tools. Why? Vector Cypher combines semantic search with graph traversal—functionality that agents achieve through **tool composition**. When an agent needs both content and relationships, it can call Semantic Search first, then Database Query for related entities. This two-step approach gives the agent flexibility to reason between calls and handles a broader range of questions than a single combined tool.

## The ReAct Pattern

![A diagram showing the agent process with perception, reasoning, action, and response](../images/agent-process.svg)

Agents typically follow the **ReAct** pattern (Reasoning + Acting):

```
1. Receive question: "How many risk factors does Apple face?"
2. Reason: "This asks for a count of a specific relationship"
3. Act: Call the Database Query Tool
4. Observe: Receive result "45"
5. Respond: "Apple faces 45 risk factors."
```

For complex questions, the agent may loop through multiple reasoning-action cycles:

```
1. Question: "What are Apple's main risks and which investors are affected?"
2. Reason: "Need risk content AND investor relationships"
3. Act: Call Semantic Search Tool for Apple's risks
4. Observe: Receive risk descriptions
5. Reason: "Now need investors"
6. Act: Call Database Query Tool for investors owning Apple
7. Observe: Receive investor list
8. Respond: Combine both results into comprehensive answer
```

## Why Agents Matter

**Without agents**: You build separate interfaces for each retriever, or force users to choose.

**With agents**: Users ask natural questions; the system figures out how to answer them.

This is what makes GraphRAG *conversational*—users interact naturally while sophisticated retrieval happens behind the scenes.

## An Example: The GraphRAG Agent

An example of an agent is a GraphRAG system that:
1. Receives a user question
2. Analyzes what kind of question it is
3. Selects and executes the appropriate tool(s)
4. Synthesizes results into a coherent answer

Your retrievers become **tools** that the agent can use. The agent's job is deciding *when* to use each one.

## Progressive Learning Path

In this lab, you'll build agents progressively:

1. **Single-tool agent**: Schema introspection only
2. **Two-tool agent**: Add semantic search
3. **Three-tool agent**: Add database queries

Each step adds capability. By the end, your agent handles any question type.

## Summary

- **Agents** analyze questions and choose appropriate tools automatically
- **Tools** are retrievers wrapped with descriptions
- **Selection** happens through semantic matching to tool descriptions
- **ReAct pattern**: Reason → Act → Observe → Respond (potentially looping)
- **Result**: Users ask natural questions; agents figure out how to answer

In the next lesson, you'll learn about the Microsoft Agent Framework that makes building agents straightforward.

---

**Navigation:**
- [← Previous: Text2Cypher Retriever](../lab-5-retrievers/04-text2cypher-retriever.md)
- [↑ Back to Lab 6](README.md)
- [Next: Microsoft Agent Framework →](02-microsoft-agent-framework.md)
