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


# Vector + Graph Retrieval Tool

Module 3, Lesson 3

---

## Introduction

You will enhance your agent by adding a custom document retrieval tool.

This tool combines:
- Semantic search using vectors
- Graph traversal for related entities

The agent decides automatically which tool is best for each question.

---

## Tool Selection in Multi-Tool Agents

**Schema Tool:**
- Understanding database structure
- "What entities exist in the graph?"
- "How are companies related to risk factors?"

**Document Retrieval Tool:**
- Finding content with company context
- "What are Microsoft's main risk factors?"
- "Tell me about cybersecurity threats mentioned by tech companies"

---

## Building a Two-Tool Agent

Your agent will have two capabilities:

**Tool 1: Schema Tool** (from previous lesson)
- Explores database structure
- Returns available entities and relationships

**Tool 2: Document Retrieval Tool** (new)
- Searches with vector similarity
- Adds graph context from relationships
- Returns content with entity connections

---

## How the Agent Chooses Tools

The agent analyzes each question and determines:

**Schema questions:**
- About database structure
- What can be queried
- Available entities and relationships

**Content questions:**
- About actual document content
- Specific entity information
- Relationships between entities

---

## Vector + Cypher Retriever as a Tool

The Vector + Cypher Retriever becomes a conversational tool:

**What it provides:**
- Semantically similar content (from vector search)
- Related entities and relationships (from graph traversal)
- Rich context combining text and structure

**When to use it:**
- Questions about specific entities
- Questions requiring relationship context
- When text alone isn't sufficient

---

## Agent Tool Wrapping

Retrievers are "wrapped" as agent tools:

**Native retriever:**
- Python function that returns results

**Agent tool:**
- Conversational interface
- Natural language input
- Formatted response for agent reasoning

The agent can call tools as needed to answer questions.

---

## Automatic Tool Selection Benefits

**Simplifies User Experience:**
- Users don't need to know which tool to use
- Just ask questions naturally

**Optimizes Results:**
- Right tool for each question type
- Better answers than single-tool approach

**Enables Complexity:**
- Agent can use multiple tools for complex questions
- Combines information from different sources

---

## Example Tool Selection Scenarios

**"What type of questions can I ask about Apple?"**
- Agent selects: Schema Tool
- Why: Question about capabilities, not content

**"What products does Microsoft mention?"**
- Agent selects: Document Retrieval Tool
- Why: Question about specific entity content with relationships

---

## Multi-Step Reasoning

Agents can use tools in sequence:

**Complex Question:**
"How are companies connected through their products?"

**Agent Reasoning:**
1. Use Schema Tool to understand structure
2. Use Document Retrieval Tool to find product mentions
3. Synthesize results into coherent answer

---

## Tool Capabilities and Descriptions

Each tool has a description that guides agent selection:

**Schema Tool Description:**
- "Get the graph database schema"
- Indicates structural information

**Document Retrieval Tool Description:**
- "Search documents with company context"
- Indicates content search with relationships

Clear descriptions enable accurate tool selection.

---

## Progressive Agent Building

**One-Tool Agent:**
- Can only explore schema
- Limited capability

**Two-Tool Agent:**
- Can explore schema AND search content
- Much more capable

**Three-Tool Agent:** (coming next)
- Adds precise query capability
- Complete GraphRAG system

---

## Key Concepts

**Tool Selection:**
- Agent analyzes question
- Chooses appropriate tool automatically
- No user intervention needed

**Multi-Tool Agent:**
- Multiple retrievers as conversational tools
- Each tool serves different purpose
- Agent orchestrates tool use

---

## Intelligent Routing

The agent routes questions intelligently:

**Structural questions** → Schema Tool
**Content questions** → Document Retrieval Tool

This routing happens automatically based on:
- Question semantics
- Tool descriptions
- Agent's understanding of capabilities

---

## What You've Built

At this point, you have:

✅ Schema Exploration tool (get database schema)
✅ Vector + Cypher Retriever tool (contextual search)
⏳ Text2Cypher Retriever tool (coming next!)

Your agent is becoming more capable with each tool addition.

---

## Summary

You enhanced your agent by adding the Vector + Cypher Retriever as a second tool:

**Key Achievements:**
- Two-tool agent with schema and contextual search
- Automatic tool selection based on question type
- Richer answers combining text and graph relationships

---

## Next Steps

In the next lesson, you will add the final tool: Text2Cypher Retriever for precise database queries.

This completes your three-tool GraphRAG agent.

