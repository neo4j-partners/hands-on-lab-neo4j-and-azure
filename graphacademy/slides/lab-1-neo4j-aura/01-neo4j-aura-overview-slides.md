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

![bg contain](../images/GraphRAG_Agent_Blueprint.jpg)

---

![bg contain](../images/neo4j_msft_customers.jpg)

---

# Neo4j Aura: Cloud Graph Database

---

## What is Neo4j Aura?

Neo4j Aura is a **fully managed cloud graph database service** that eliminates the operational overhead of running a graph database.

**Key Characteristics:**
- **Fully managed** - No infrastructure to maintain
- **Scalable** - Automatically scales with your data and queries
- **Secure** - Enterprise-grade security and compliance
- **Available everywhere** - Deploy in AWS, GCP, or Azure regions

---

## Why Use a Graph Database?

Traditional databases struggle with **connected data**:

| Scenario | Relational DB | Graph DB |
|----------|---------------|----------|
| "Find friends of friends" | Complex JOINs, slow | Natural traversal, fast |
| "What impacts what?" | Multiple queries | Single query |
| "How are these connected?" | Hard to express | Native pattern matching |

**Graphs excel at relationship-heavy queries** that would require dozens of JOINs in SQL.

---

## The Value of Aura for AI/GenAI

Neo4j Aura provides unique capabilities for building AI applications:

**GraphRAG Foundation:**
- Store knowledge graphs that power AI agents
- Vector search for semantic similarity
- Graph traversal for relationship reasoning

**Production-Ready:**
- Built-in vector indexes for embeddings
- Cypher query language for complex retrieval
- APIs for integration with LLM frameworks

---

<!-- _class: small -->
<style scoped>
section { font-size: 22px; }
h2 { font-size: 32px; }
</style>

## Graph Analytics in Explore

The **Explore** tool includes built-in graph algorithms for visual analysis:

**Available in Explore:**
| Category | Algorithms |
|----------|------------|
| **Centrality** | Betweenness, Degree, Eigenvector, PageRank |
| **Community Detection** | Label Propagation, Louvain, Weakly Connected Components |

**Full Algorithm Library (65+):**
Neo4j Aura Graph Analytics provides the complete library via serverless compute with Zero ETL:

| Category | Additional Algorithms | Use Cases |
|----------|----------------------|-----------|
| **Similarity** | Node Similarity, K-Nearest Neighbors | Recommendations, duplicate detection |
| **Path Finding** | Dijkstra, A*, Yen's K-Shortest | Routing, supply chain optimization |
| **Link Prediction** | Common Neighbors, Adamic Adar | Predict future connections |
| **Node Embeddings** | FastRP, GraphSAGE, Node2Vec | ML feature generation |

---


<!-- _class: small -->
<style scoped>
section { font-size: 22px; }
h2 { font-size: 32px; }
</style>

## Aura Tools: Query Workspace

The **Query Workspace** is a developer-friendly environment for Cypher:

**Core Features:**
- Write and execute Cypher queries against your database
- Syntax highlighting and auto-completion
- Save and organize query collections
- Export results in multiple formats

**Query Log Forwarding:**
- Send logs to your cloud logging service
- Better compliance, monitoring, and operational visibility
- Manage directly from Aura console

---

<!-- _class: small -->
<style scoped>
section { font-size: 22px; }
h2 { font-size: 32px; }
</style>

## Aura Tools: Explore

**Explore** (powered by Neo4j Bloom) is a visual graph exploration tool:

**Visual Graph Scene:**
- Interactive canvas showing your graph data
- Click and drag nodes to arrange layouts
- Export as PNG, CSV, or shareable scenes

**Search-First Experience:**
- Natural language and pattern-based search
- "Show me a graph" sample queries
- Find nodes and relationships without Cypher

**AI-Powered Features:**
- GenAI Copilot for query assistance
- Find hidden connections automatically
---

<!-- _class: small -->
<style scoped>
section { font-size: 22px; }
h2 { font-size: 32px; }
</style>

## Aura Tools: Dashboards

**Dashboards** in the Neo4j Console provide data visualization capabilities with low code / no code:

**Visualization Types:**
- Bar charts, line charts, pie charts, etc.
- Geographic maps
- **3D graph visualizations** (WebGL-powered)

**GenAI Copilot:**
- AI-powered dashboard creation
- Natural language to visualization

**Enterprise Ready:**
- SSO integration
- Role-based access

---

## Aura Agents: No-Code GraphRAG

**Coming up in this workshop:** Neo4j Aura Agents

Aura Agents let you build **AI-powered conversational interfaces** to your graph:

- **No code required** - Configure through a simple UI
- **Natural language queries** - Ask questions in plain English
- **Automatic Cypher generation** - LLM translates questions to graph queries
- **Knowledge graph reasoning** - Leverage relationships for better answers

**Why Agents matter:**
- Democratize access to graph insights
- Build chatbots that understand your domain
- Combine vector search + graph traversal automatically

---

## Summary

Neo4j Aura provides:

- **Managed graph database** - Focus on your data, not infrastructure
- **Graph-native storage** - Relationships are first-class citizens
- **AI/GenAI capabilities** - Vector indexes, GraphRAG support
- **Graph Analytics** - Built-in algorithms for insights
- **Integrated Tools** - Query, Explore, and Dashboards
- **Aura Agents** - No-code conversational AI over your graph

**Next:** Learn about Aura Agents for no-code GraphRAG applications.

