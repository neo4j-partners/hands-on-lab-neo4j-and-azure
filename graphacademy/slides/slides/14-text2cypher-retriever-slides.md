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


# All Three Tools

Module 3, Lesson 4

---

## Introduction

You will complete your agent by adding a Text2Cypher query tool as the third tool.

The agent automatically chooses the best tool for each question type.

This creates a comprehensive GraphRAG agent.

---

## Three-Tool Agent Capabilities

**Schema Tool:**
- Understanding database structure
- "What entities exist in the graph?"

**Document Retrieval Tool:**
- Finding content with company context
- "What products does Microsoft mention in its documents?"

**Database Query Tool:**
- Precise queries and counts
- "How many risk factors does Apple face?"

---

## The Final Tool: Text2Cypher

Text2Cypher converts natural language to graph queries:

**What it does:**
- Interprets user's question intent
- Generates Cypher query from natural language
- Executes query against graph
- Returns precise, structured results

**When to use it:**
- Exact counts and aggregations
- Precise factual queries
- Structured data retrieval

---

## Complete Tool Suite

Your agent now has three complementary tools:

**Tool 1: Schema Tool**
- Database structure exploration

**Tool 2: Document Retrieval Tool**
- Vector search + graph context

**Tool 3: Database Query Tool** ← NEW
- Text-to-Cypher for precise queries

---

## How Tool Selection Works

The agent analyzes each question:

**Structural question** → Schema Tool
**Content question with relationships** → Document Retrieval Tool
**Precise data question** → Database Query Tool

Selection happens automatically based on question characteristics.

---

## Text2Cypher Tool Benefits

**Precision:**
- Exact answers to factual questions
- No semantic approximation needed

**Aggregation:**
- Counts, sums, averages
- Complex analytical queries

**Structured Access:**
- Direct graph database queries
- Leverage full graph query power

---

## Example Tool Selections

**"What stock has Microsoft issued?"**
- Agent selects: Database Query Tool
- Why: Precise factual query

**"What are the main risk factors mentioned?"**
- Agent selects: Document Retrieval Tool
- Why: Content search across entities

**"How does the schema connect companies to risks?"**
- Agent selects: Schema Tool
- Why: Structural question

---

## Complex Questions

Some questions require multiple tools:

**"Summarize Apple's risk factors and how they relate to other companies"**

**Agent Process:**
1. Database Query Tool: Get Apple's risk factors
2. Document Retrieval Tool: Find related company information
3. Synthesize: Combine results into comprehensive answer

---

## Intelligent Multi-Tool Reasoning

The agent can:

**Use tools in sequence:**
- One tool's results inform next tool choice

**Combine results:**
- Integrate information from multiple tools

**Retry with different tools:**
- If first tool doesn't satisfy query, try another

This creates sophisticated question-answering capability.

---

## Tool Complementarity

Each tool serves a distinct purpose:

**Schema Tool:**
- What's possible to query

**Document Retrieval Tool:**
- What's written in documents (with context)

**Database Query Tool:**
- What's true in the structured data

Together, they cover all question types.

---

## Progressive Capability

Your journey building the agent:

**One-Tool Agent:**
- Schema exploration only

**Two-Tool Agent:**
- Schema + contextual search

**Three-Tool Agent:**
- Schema + contextual search + precise queries

Each addition expands capability significantly.

---

## The Complete GraphRAG Agent

You now have:

✅ Knowledge Graph Creation (PDF to graph)
✅ Retriever Development (three retriever types)
✅ Agent Tools (retrievers as conversational tools)

**Result:** A complete GraphRAG agent that answers any question using the optimal retrieval strategy.

---

## Automatic Strategy Selection

The agent handles question routing:

**No user decision needed:**
- Users ask questions naturally
- Agent determines best approach

**Optimal results:**
- Right tool for each question
- Better than any single retriever alone

**Flexible:**
- Can adapt to new question types
- Combines tools as needed

---

## From Retrievers to Agent

**Module 1:** Built knowledge graph
**Module 2:** Developed three retriever types
**Module 3:** Wrapped retrievers as agent tools

This progression creates a powerful, flexible system.

---

## Key Concepts

**Complete Tool Suite:**
- All three retrievers available as conversational tools

**Intelligent Routing:**
- Agent automatically selects best tool(s)

**Progressive Capability:**
- From simple search to complex multi-tool reasoning

**Conversational Interface:**
- Natural language input
- Sophisticated graph operations behind the scenes

---

## Real-World Applications

This agent architecture works for many domains:

**Financial Services:**
- Query filings, find risks, understand relationships

**Healthcare:**
- Patient data, treatment relationships, medical literature

**E-Commerce:**
- Product data, customer relationships, inventory queries

**Any Knowledge Graph:**
- Same pattern applies across domains

---

## What Makes This Powerful

**Flexibility:**
- Handles diverse question types

**Accuracy:**
- Each tool optimized for its purpose

**Usability:**
- Simple conversational interface

**Extensibility:**
- Easy to add more tools

---

## Summary

You completed your GraphRAG agent by adding the Text2Cypher Retriever:

**Three Tools:**
- Schema exploration
- Contextual content search
- Precise graph queries

**Intelligent Routing:**
- Automatic tool selection for optimal answers

**Complete System:**
- Handles any question type effectively

---

## Your Journey

You've built a complete GraphRAG system:

**Foundation:** Knowledge graphs from documents
**Capabilities:** Three retrieval strategies
**Interface:** Conversational agent with automatic routing

This is production-ready GraphRAG architecture.

---

## Next Steps

In the next lesson, you will learn about Aura Agents, a no-code interface for building GraphRAG agents.

