# Neo4j And Azure Lab
Neo4j is the [leading graph database](https://db-engines.com/en/ranking/graph+dbms) vendor.  We've worked closely with Microsoft Azure engineering for years.  Our products, AuraDB and AuraDS are offered as managed services on Azure.  Neo4j Aura Professional Edition is offered in the [Azure Marketplace](https://portal.azure.com/#create/neo4j.neo4j_aura_professional).

This hands-on lab covers Neo4j, Microsoft Foundry, and the [Microsoft Agent Framework](https://github.com/microsoft/agent-framework). It is designed for data scientists, data engineers, and AI developers working with GraphRAG (Graph Retrieval-Augmented Generation).

You'll work with real SEC 10-K company filings to build a knowledge graph from unstructured text, extract entities with generative AI, and implement multiple retrieval strategies: vector similarity search, graph-enhanced retrievers that traverse entity relationships, and natural language to Cypher query generation. The final labs build agents using the Microsoft Agent Framework that select the right tool for each question and reason over the knowledge graph.

By the end, you'll have working experience with:
- Building knowledge graphs from unstructured documents
- Semantic search with vector embeddings
- Graph-enhanced retrieval that traverses relationships for context beyond matched text
- AI agents that combine multiple tools and retrieval strategies
- Deploying GraphRAG applications on Azure infrastructure

## Knowledge Graph Data Model

The workshop builds a hybrid knowledge graph that combines **lexical structure** (documents and chunks) with **semantic knowledge** (entities and relationships extracted by LLM). This architecture enables multiple retrieval strategies.

### Graph Structure

```
                      NEXT_CHUNK
                 ┌──────────────────┐
                 │                  │
                 v                  │
┌──────────┐       ┌──────────┐       ┌──────────┐
│  Chunk   │──────>│  Chunk   │──────>│  Chunk   │
│          │       │          │       │          │
│ text     │       │ text     │       │ text     │
│ embedding│       │ embedding│       │ embedding│
└──────────┘       └──────────┘       └──────────┘
     │                  │                  │
     │ FROM_DOCUMENT    │                  │
     v                  v                  v
┌─────────────────────────────────────────────────┐
│                    Document                      │
│                                                  │
│  path: "sec-10k-filings/apple-10k.pdf"          │
└─────────────────────────────────────────────────┘

     ^                  ^                  ^
     │ FROM_CHUNK       │                  │
     │                  │                  │
┌──────────┐       ┌──────────┐       ┌──────────┐
│ Company  │       │ Product  │       │RiskFactor│
│          │       │          │       │          │
│ Apple    │       │ iPhone   │       │ Supply   │
│ Inc.     │       │          │       │ Chain    │
└──────────┘       └──────────┘       └──────────┘
     │                                      ^
     │ FACES_RISK                           │
     └──────────────────────────────────────┘
```

### Node Types

| Node Label | Description | Key Properties |
|------------|-------------|----------------|
| `Document` | Source PDF file | `path`, `createdAt` |
| `Chunk` | Text segment from document | `text`, `index`, `embedding` (1536-dim vector) |
| `Company` | Extracted company entity | `name`, `ticker` |
| `Product` | Products/services mentioned | `name` |
| `RiskFactor` | Business risks identified | `name` |
| `Executive` | Key personnel | `name`, `title` |
| `FinancialMetric` | Financial data points | `name`, `value` |
| `AssetManager` | Institutional investors | `managerName` |

### Relationship Types

| Relationship | Direction | Description |
|--------------|-----------|-------------|
| `FROM_DOCUMENT` | `(Chunk)->(Document)` | Links chunk to source document |
| `NEXT_CHUNK` | `(Chunk)->(Chunk)` | Sequential chunk ordering |
| `FROM_CHUNK` | `(Entity)->(Chunk)` | Provenance: where entity was extracted |
| `FACES_RISK` | `(Company)->(RiskFactor)` | Company faces this risk |
| `OFFERS` | `(Company)->(Product)` | Company offers this product |
| `HAS_EXECUTIVE` | `(Company)->(Executive)` | Company has this executive |
| `REPORTS` | `(Company)->(FinancialMetric)` | Company reports this metric |
| `OWNS` | `(AssetManager)->(Company)` | Investor owns shares in company |


## Starting the Lab

To get started, follow the labs in the agenda below in order.

**Quick Start Options:**
- **No-Code Track Only (1 hour):** Complete Part 1 (Labs 0-3) to explore Neo4j and AI agents without coding
- **Full Workshop (3-4 hours):** Complete both Part 1 and Part 2 for the full development experience
- **Skip to Coding:** If you already have your Azure account and Aura credentials, go straight to [Lab 4 - Start Codespace](Lab_4_Start_Codespace)

## Duration
3-4 hours (full workshop) or 1 hour (no-code track only).

## Prerequisites
You'll need a laptop with a web browser. Your browser will need to be able to access the Azure Console. If your laptop has a firewall you can't control on it, you may want to bring your personal laptop.

## Agenda

### Part 1 - No-Code Getting Started
*This section requires no coding. You'll use visual tools and pre-built interfaces to explore Neo4j and AI agents.*

* Introductions
* [Lecture - Introduction to Neo4j](https://docs.google.com/presentation/d/1mEXn02TMYJ0nGFj7u5VANQBl1jBJcLGp6dYHB_xY0pQ/edit?usp=sharing) (10 min)
    * What is Neo4j?
    * How is it deployed and managed on Azure?
* [Lab 0 - Sign In](Lab_0_Sign_In) (5 min)
    * Improving the Labs
    * Sign into Azure
* [Lab 1 - Neo4j Aura Setup](Lab_1_Aura_Setup) (15 min)
    * Signing up for Neo4j Aura through Azure Marketplace
    * Restoring the pre-built knowledge graph
    * Visual exploration with Neo4j Explore
* [Lab 2 - Aura Agents](Lab_2_Aura_Agents) (20 min)
    * Building AI agents using Neo4j Aura Agent (no-code)
    * Creating Cypher template tools
    * Adding semantic search and Text2Cypher capabilities
* [Lab 3 - Microsoft Foundry Agents](Lab_3_Foundry_Agents) (15 min)
    * Access Microsoft Foundry
    * Create a Foundry Project
    * Deploy gpt-4o model
    * Build an agent with MCP tools
* Break (5 min)

---

### Part 2 - Core Labs
*This section involves Python programming using Jupyter notebooks.*

* [Lab 4 - Start Codespace](Lab_4_Start_Codespace) (10 min)
    * Launch GitHub Codespace
    * Configure environment variables
* [Lecture - Neo4j and Generative AI](https://docs.google.com/presentation/d/1iHu9vgEG0s6yjKMLUw9XqWGiJrY7Z1oNv0QPa75BCtc/edit?usp=sharing) (15 min)
    * Generating Knowledge Graphs
    * Retrieval Augmented Generation
    * Semantic Search
* [Lecture - Microsoft Foundry](https://docs.google.com/presentation/d/1KPHoVJivbinHg-UtrnTIUbMiFHB8mPEnDO0v0OvvcPM/edit?usp=sharing) (15 min)
    * What is Microsoft Foundry?
    * Generative AI
* [Lab 5 - Foundry Agents](Lab_5_Foundry_Agents) (15 min)
    * Simple Schema Agent with Microsoft Agent Framework
* [Lab 6 - MAF Context Providers](Lab_6_Context_Providers) (30 min)
    * Fulltext Context Provider for keyword-based retrieval
    * Vector Context Provider for semantic search
    * Graph-Enriched Provider with relationship traversal
* [Lab 7 - Agent Memory](Lab_7_Agent_Memory) (30 min)
    * Memory Context Provider with Neo4j Agent Memory
    * Agent with Memory Tools for persistent learning

---

### Part 3 - Advanced Labs
*Optional advanced topics building on the core workshop.*

* [Lab 8 - Building a Knowledge Graph](Lab_8_Knowledge_Graph) (30 min)
    * Background on how the Neo4j data was loaded and embeddings created
    * GraphRAG Retrievers (Vector and VectorCypher)
    * See [`financial_data_load/`](financial_data_load) for the full Python data loading pipeline
* [Lab 9 - Advanced Agents](Lab_9_Advanced_Agents) (30 min)
    * Vector + Graph Agent for Semantic Search with Context
    * Multi-Tool Agent with Text2Cypher
* [Questions and Next Steps](Questions%20and%20Next%20Steps.md) (5 min)

