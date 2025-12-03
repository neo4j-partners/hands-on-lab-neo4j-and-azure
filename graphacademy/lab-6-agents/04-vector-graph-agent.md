# Vector Graph Agent

## Introduction

In this lesson, you'll enhance your agent by adding a second tool: a vector retriever that combines semantic search with graph traversal. Your agent will now intelligently choose between two tools based on the question type.

This lesson prepares you for Lab 6 Notebook 2, where you'll build a two-tool agent with Microsoft Foundry.

The agent decides automatically which tool is best for each question:

**Schema Tool:**

- Understanding database structure
- "What entities exist in the graph?"
- "How are companies related to risk factors?"

**Document Retrieval Tool:**

- Finding content with company context
- "What are Microsoft's main risk factors?"
- "Tell me about cybersecurity threats mentioned by tech companies"

## Two-Tool Agent

Open the notebook: `02_02_vector_graph_agent.ipynb`

Add the Vector + Cypher Retriever as a second tool:

1. **Keep existing schema tool** (from previous lesson)
2. **Add new document retrieval tool** (vector search with graph context)
3. **Let agent choose** between tools based on question

Now your agent can handle both schema exploration AND contextual relationship queries.

## Try These Questions

**Try these questions to see tool selection:**

- _"How are companies connected through their mentioned products?"_
- _"What type of questions can I ask about Apple using the graph database?"_
- _"What products does Microsoft mention in its financial documents?"_
- _"How are companies connected through their mentioned products?"_

The agent will choose from the 2 tools available:

- Graph Exploration (Schema Tool)
- Contextual Search (Vector + Cypher Tool)

**Notice:** The agent chooses the right tool (or series of tools) automatically based on whether relationships are needed!

## Summary

In this lesson, you enhanced your agent by adding the Vector + Cypher Retriever as a second tool:

**Key Concepts:**

- **Tool selection:** Agent chooses between schema and contextual search
- **Multi-tool agent:** Two retrievers wrapped as conversational tools
- **Intelligent routing:** Questions automatically matched to appropriate tool

**What You Built:**

- Agent with two retriever tools
- Automatic tool selection based on question type
- Enhanced capability for both simple and contextual queries

**Progress:**

- ✅ Schema Exploration tool (get database schema)
- ✅ Vector + Cypher Retriever tool (contextual search)
- ⏳ Text2Cypher Retriever tool (coming next!)

In the next lesson, you will add the final tool: Text2Cypher Retriever for precise database queries.

---

**Navigation:**
- [← Previous: Simple Schema Agent](03-simple-schema-agent.md)
- [↑ Back to Module 3](README.md)
- [Next: Text2Cypher Agent →](05-text2cypher-agent.md)
