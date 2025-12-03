# Module 3: Intelligent Agents

Welcome to Module 3! This module teaches you how to build intelligent agents that use your knowledge graph as a tool. You'll learn to create agents that automatically choose the right retriever for each question, making your GraphRAG system conversational and user-friendly.

## Module Overview

In this module, you will:

- Understand what agents are and how they work
- Learn the Microsoft Agent Framework for building agents
- Build agents that use tools to access your knowledge graph
- Progressively add tools: schema introspection, vector search, and Text2Cypher
- Create multi-tool agents that intelligently select the right retriever
- Understand agent design patterns and best practices

## Alignment with Lab 6: Agents

This module provides the conceptual foundation for Lab 6, which has 3 hands-on notebooks:

| Lesson | Lab 6 Notebook | Focus |
|--------|----------------|-------|
| Lessons 1-2 | (Introduction) | What agents are, Microsoft Agent Framework basics |
| Lesson 3 | Notebook 1: Simple Agent | Single tool agent with schema introspection |
| Lesson 4 | Notebook 2: Vector Graph Agent | Two-tool agent (schema + vector search) |
| Lesson 5 | Notebook 3: Text2Cypher Agent | Three-tool agent (schema + vector + Text2Cypher) |
| Lesson 6 | (All notebooks) | Agent design patterns and tool selection |
| Lessons 7-9 | (Optional/Closing) | Aura Agents, best practices, wrap-up |

## Lessons

1. [What is an Agent](./01-what-is-an-agent.md) - Agent concepts and architecture
2. [Microsoft Agent Framework](./02-microsoft-agent-framework.md) - Framework overview
3. [Simple Schema Agent](./03-simple-schema-agent.md) - Single tool for schema introspection
4. [Vector Graph Agent](./04-vector-graph-agent.md) - Adding vector retriever tool
5. [Text2Cypher Agent](./05-text2cypher-agent.md) - Multi-tool agent with all retrievers
6. [Multi-Tool Agent Design](./06-multi-tool-design.md) - How agents select tools
7. [Aura Agents](./07-aura-agents.md) - No-code agent platform (Optional)
8. [Best Practices](./08-best-practices.md) - Agent design patterns (Optional)
9. [Congratulations](./09-congratulations.md) - Workshop summary

## Learning Path

**Foundation (Lessons 1-2):**
Understand agents and the Microsoft Agent Framework.

**Simple Agent (Lesson 3):**
Build your first agent with a single schema tool.

**Enhanced Agent (Lesson 4):**
Add vector retriever for semantic search capabilities.

**Complete Agent (Lesson 5):**
Create a multi-tool agent that chooses between three retrievers.

**Design Patterns (Lessons 6-7):**
Learn how agents select tools and design best practices.

## The Three Tools

**Quick Reference:**

| Tool | What It Does | When Agent Uses It |
|------|--------------|-------------------|
| **Schema Tool** | Returns graph schema | Questions about data structure |
| **Vector Retriever Tool** | Semantic search | Questions about content/topics |
| **Text2Cypher Tool** | Database queries | Questions about facts/counts |

## Navigation

- [← Back to Module 2: GraphRAG Retrievers](../module-2-retrievers/README.md)
- [Start with Lesson 1: What is an Agent →](./01-what-is-an-agent.md)
- [Back to Workshop Home](../README.md)
