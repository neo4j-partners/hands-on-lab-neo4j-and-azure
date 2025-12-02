# Making Retrievers Conversational

## Introduction

Now that you understand the three types of retrievers, let's learn how to make them **conversational** by wrapping them as *agent* tools.

## What is an Agent? (Formal Definition)

Before diving into our specific implementation, let's understand what makes something an "agent" in artificial intelligence.

### Stuart Russell's Definition

Stuart Russell (co-author of "Artificial Intelligence: A Modern Approach") defines an **agent** as:

> **"Anything that can perceive its environment through sensors and act upon that environment through actuators."**

**Core Components:**

1. **Percepts (Sensors)** - The agent's perceptual inputs from its environment
   - In our case: User messages, conversation history, database schema

2. **Percept Sequence** - The complete history of everything the agent has perceived
   - In our case: Conversation thread with all previous messages

3. **Agent Function** - Maps percept sequences to actions
   - In our case: LLM reasoning that decides which tool to call

4. **Actuators (Actions)** - Mechanisms through which the agent acts
   - In our case: Retriever tools (Schema, Vector+Cypher, Text2Cypher)

### Why Our System is an Agent

Our conversational retriever system fits Russell's definition perfectly:

**Perception:**
- Receives user queries (current percept)
- Accesses conversation history (percept sequence)
- Understands available tools and their capabilities

**Decision Making:**
- Analyzes the question type
- Reasons about which retriever tool is most appropriate
- Considers conversation context

**Action:**
- Executes the selected retriever tool
- Returns results to the user
- Updates conversation state

This is a **Goal-Based Agent** - it selects actions (tool calls) based on achieving the goal of answering the user's question accurately.

## Our Agent Architecture

Now that you understand the formal definition, let's see how we implement it:

**Retrievers as Actuators (Actions):**

- **Schema Retriever** → Database Schema Tool (action: explore structure)
- **Vector + Cypher Retriever** → Hybrid Tool (action: semantic search with context)
- **Text2Cypher Retriever** → Structured Query Tool (action: precise data retrieval)

**Conversation Framework as Perception:**

- User query analysis (current percept)
- Thread management (percept sequence/history)
- Context maintenance
- Natural language interface

**LLM as Agent Function:**

- Maps perceived user intent → appropriate action (tool selection)
- Reasons about which retriever to use
- Formats and presents results


## Agent Intelligence: Tool Selection

**The agent's job is to choose the right retriever tool:**

- **"How are Products related to other entities?"** → Use Schema for data model exploration
- **"Which companies are affected by banking regulations?"** → Use Vector+Cypher for contextual relationships
- **"What risks does Apple face?"** → Use Text2Cypher for precise company data

## Agent Intelligence: Agent Reasoning

**Agent reasoning:**

1. Analyze the user's question
2. Determine what type of information is needed
3. Select the appropriate retriever tool
4. Execute the tool and format the response
5. Maintain conversation context

## Progressive Learning Path

**You'll build the agent incrementally:**

**First Agent:** Basic agent with **schema introspection** tool

- Start simple with database exploration
- Learn agent fundamentals

**Enhanced Agent:** Add **document retrieval** tool

- Add semantic search with graph context
- Compare tool behaviors

**Complete Agent:** Add **text-to-Cypher** tool

- Add structured queries
- Multi-tool agent intelligence

Each step adds one more tool - building complexity step by step.

**The retrievers do the heavy lifting - the agent makes them conversational and smart about when to use each one.**

## Getting Started

In the next lessons, you'll progressively build an agent by adding retriever tools one by one:

1. **Schema tool** for data model exploration
2. **Vector + Cypher tool** for semantic exploration and contextual relationships
3. **Text2Cypher tool** for precise queries

Each lesson shows how to wrap a retriever as a tool and how the agent chooses between available tools.

## Summary

In this lesson, you learned that agents are **conversational wrappers** around the retrievers you already know:

**Key Concept:**

- **Retrievers** = The core functionality (Schema, Vector+Cypher, Text2Cypher)
- **Agents** = Conversational interface + intelligent tool selection
- **Tools** = Retrievers wrapped for agent use

**What Agents Add:**

- User query analysis
- Natural language conversation interface
- Automatic tool selection based on question type
- Flexible context management

**Progressive Learning:**

- **First Agent:** Schema tool → Database exploration
- **Enhanced Agent:** Add document retrieval → Semantic search with context
- **Complete Agent:** Add text2cypher → Structured queries

**The retrievers do the work - the agent makes them conversational and intelligent about when to use each one.**

In the next lesson, you will start building your agent with schema introspection as your first tool.

---

**Navigation:**
- [← Previous: Module 2 Complete](../module-2-retrievers/06-choosing-retrievers.md)
- [↑ Back to Module 3](README.md)
- [Next: Microsoft Agent Framework →](02-microsoft-agent-framework.md)
