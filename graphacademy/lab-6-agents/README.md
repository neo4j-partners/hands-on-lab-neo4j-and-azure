# Lab 6: Intelligent Agents

Welcome to Lab 6! This lab teaches you how to build intelligent agents that automatically choose the right retrieval strategy for each question, making your GraphRAG system conversational and user-friendly.

## Lab Overview

In this lab, you will:

- Understand how agents analyze questions and select tools
- Learn the Microsoft Agent Framework
- Build agents progressively: one tool, two tools, three tools
- Master design patterns for effective multi-tool agents

## The Big Picture

**Where we are**: You have a knowledge graph (Lab 3) and know three retrieval patterns (Lab 5).

**The problem**: Users don't know about retrievers. They just ask questions.

**The solution**: Agents that analyze questions and automatically select the right tool.

## Lessons

1. [From Retrievers to Agents](./01-from-retrievers-to-agents.md) - Why agents matter and how they work
2. [Microsoft Agent Framework](./02-microsoft-agent-framework.md) - Framework components and patterns
3. [Building Your Agent](./03-building-your-agent.md) - Progressive construction from one tool to many
4. [Agent Design Patterns](./04-agent-design-patterns.md) - Patterns for effective agents
5. [Congratulations](./05-congratulations.md) - What you've learned and next steps

## Learning Path

**Understanding Agents (Lesson 1):**
Why we need agents and how they choose tools.

**The Framework (Lesson 2):**
Microsoft Agent Framework components and how they work together.

**Building Agents (Lesson 3):**
Progressive construction from schema tool to full multi-tool agent.

**Design Patterns (Lesson 4):**
Patterns that make agents reliable and effective.

## The Three Tools

Your agent uses three tools—your retrievers from Lab 5:

| Tool | Based On | When Agent Uses It |
|------|----------|-------------------|
| **Schema Tool** | Graph introspection | "What data exists?" |
| **Semantic Search** | Vector Retriever | "What is...", "Tell me about..." |
| **Database Query** | Text2Cypher Retriever | "How many...", "Who owns..." |

The agent matches questions to tool descriptions and selects appropriately.

## What You'll Build

A complete GraphRAG agent that:
- Analyzes user questions
- Selects the right retrieval tool
- Executes queries against your knowledge graph
- Returns coherent, grounded answers
- Handles multi-turn conversations

## Navigation

- [← Back to Lab 5: GraphRAG Retrievers](../lab-5-retrievers/README.md)
- [Start with Lesson 1: From Retrievers to Agents →](./01-from-retrievers-to-agents.md)
- [Back to Workshop Home](../README.md)
