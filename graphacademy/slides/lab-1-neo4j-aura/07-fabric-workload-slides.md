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

# Neo4j Graph Workload for Microsoft Fabric

Bringing Graph Analytics to Your OneLake Data

---

## What is Microsoft Fabric?

Microsoft Fabric is a **unified analytics platform** that brings together all data and analytics tools in one place.

**Key Components:**
- **Data Engineering** - Build data pipelines and transformations
- **Data Warehousing** - SQL-based analytics at scale
- **Data Science** - Machine learning and AI workloads
- **Real-Time Analytics** - Streaming data processing
- **Power BI** - Business intelligence and visualization

**Everything runs on a unified foundation.**

---

## What is OneLake?

OneLake is the **single, unified data lake** for all of Microsoft Fabric.

**Key Characteristics:**
- **One copy of data** - No data duplication across services
- **Open format** - Delta Lake / Parquet for interoperability
- **Unified governance** - Single security and compliance model
- **Automatic organization** - Data organized by workspace

**Think of OneLake as the "OneDrive for data"** - all your organizational data in one place.

---

## What is a Fabric Workload?

A **Workload** is a specialized capability that extends Microsoft Fabric's functionality.

**Native Workloads:**
- Data Factory, Synapse, Power BI, etc.

**Partner Workloads:**
- Third-party tools integrated natively into Fabric
- Access OneLake data directly
- Use Fabric's security, identity, and compute
- Appear as first-class experiences in the Fabric portal

**Partner workloads extend Fabric without leaving the platform.**

---

## How Workloads Use OneLake

Partner workloads integrate deeply with the Fabric ecosystem:

| Integration Point | What It Provides |
|-------------------|------------------|
| **Entra ID** | Seamless authentication and authorization |
| **Workspaces** | Object persistence and sharing |
| **Lakehouses** | Secure access to tabular data |
| **Fabric Capacity** | In-platform computing resources |

**Workloads operate on your data where it lives.**

---

## Introducing Neo4j Graph Workload

Neo4j provides a **native graph analytics workload** for Microsoft Fabric.

**What It Enables:**
- Transform tabular OneLake data into graph models
- Run graph algorithms and analytics
- Visualize and explore data relationships
- Query with Cypher directly in Fabric

**Available now as a first-class Fabric experience.**

---

![bg contain](../images/fabric_graph_intelligence.jpg)

---

![bg contain](../images/fabric_testimonials.jpg)

---

![bg contain](../images/fabric_easy_start.jpg)

---

<!-- _class: small -->
<style scoped>
section { font-size: 22px; }
h2 { font-size: 32px; }
</style>

## Why Graph Analytics on OneLake Data?

Your OneLake data contains **hidden relationships** that tabular analysis misses.

| Analysis Type | Traditional BI | Graph Analytics |
|---------------|----------------|-----------------|
| Customer segments | Static groupings | Community detection |
| Influence patterns | Not possible | Centrality algorithms |
| Connected risks | Manual joins | Path traversal |
| Recommendations | Rule-based | Similarity algorithms |
| Fraud detection | After the fact | Pattern matching |

**Graph analytics reveals the connections in your data.**

---

<!-- _class: small -->
<style scoped>
section { font-size: 22px; }
h2 { font-size: 32px; }
</style>

## Neo4j Graph Workload Capabilities

**Transform & Load:**
- Map tabular data from Lakehouses to graph models
- Create nodes and relationships from your data
- Load into a Neo4j AuraDB Professional database

**Analyze:**
- Full Cypher query language
- 65+ built-in graph algorithms
- Centrality, community detection, similarity, path finding

**Visualize:**
- Explore interface for interactive graph visualization
- Discover patterns visually

---

<!-- _class: small -->
<style scoped>
section { font-size: 22px; }
h2 { font-size: 32px; }
</style>

## Available Graph Algorithms

The Neo4j Graph Workload includes the full algorithm library:

| Category | Algorithms | Use Cases |
|----------|------------|-----------|
| **Centrality** | PageRank, Betweenness, Degree, Eigenvector | Find influential nodes |
| **Community** | Louvain, Label Propagation, WCC | Detect clusters and groups |
| **Similarity** | Node Similarity, KNN | Recommendations, deduplication |
| **Path Finding** | Dijkstra, A*, Shortest Path | Routing, dependencies |
| **Link Prediction** | Common Neighbors, Adamic Adar | Predict future connections |
| **Embeddings** | FastRP, Node2Vec, GraphSAGE | ML feature generation |

**Run any algorithm directly from the Fabric console.**

---

![bg contain](../images/fabric_workload_setup.jpg)

---

![bg contain](../images/fabric_to_neo4j.jpg)

---

## Table to Graph Conversion

Transform relational data into nodes and relationships.

**Graph Model Interface:**
- Guides the data mapping process visually
- Preview graph structure before loading

**AI-Assisted Modeling:**
- AI Assistant suggests node and relationship types for review
- Generative AI uses schema analysis and Azure OpenAI for suggestions
- Accept, modify, or reject recommendations

**Execution:**
- A Spark job executes the transformation into graph objects
- Scales automatically with your Fabric capacity

---

<!-- _class: small -->
<style scoped>
section { font-size: 22px; }
h2 { font-size: 32px; }
</style>

## Example: Customer 360 Graph

Transform customer data into a connected view:

**Source Tables:**
- `customers` - Customer profiles
- `orders` - Purchase history
- `products` - Product catalog
- `interactions` - Support tickets, emails

**Graph Model:**
```
(Customer)-[:PURCHASED]->(Product)
(Customer)-[:CONTACTED]->(Support)
(Product)-[:SIMILAR_TO]->(Product)
```

**Insights:** Community detection reveals customer segments, PageRank identifies influential customers.

---

<!-- _class: small -->
<style scoped>
section { font-size: 22px; }
h2 { font-size: 32px; }
</style>

## Explore: Visual Graph Analysis

The **Explore** interface provides interactive visualization:

**Visual Capabilities:**
- Interactive graph canvas
- Drag and arrange nodes
- Filter and highlight patterns
- Export visualizations

**Search & Discovery:**
- Pattern-based search
- Find connections between entities
- Expand neighborhoods

**Built into Fabric - no external tools needed.**

---

![bg contain](../images/fabric_analyze_data.jpg)

---

## Integration with Fabric Security

The Neo4j Graph Workload inherits Fabric's enterprise security:

**Authentication:**
- Microsoft Entra ID (Azure AD)
- Single sign-on across Fabric

**Authorization:**
- Workspace-level permissions
- Role-based access control

**Data Governance:**
- Data stays in your tenant
- Audit logging
- Compliance with Fabric policies

**No separate security configuration required.**

---

<!-- _class: small -->
<style scoped>
section { font-size: 22px; }
h2 { font-size: 32px; }
</style>

## Use Cases for Graph Analytics on OneLake

**Supply Chain:**
- Map supplier relationships
- Identify bottlenecks and risks
- Optimize logistics paths

**Financial Services:**
- Detect fraud patterns
- Analyze transaction networks
- Risk propagation analysis

**Manufacturing:**
- Bill of materials graphs
- Quality issue tracing
- Asset relationship mapping

---

## Current Capabilities & Roadmap

**Available Now:**
- Graph creation from Lakehouse tables
- Full Cypher query support
- 65+ graph algorithms
- Explore visualization

**Coming Soon:**
- Writeback of insights to OneLake
- Additional data source support

---

## Summary

Neo4j Graph Workload for Microsoft Fabric:

- **Native Integration** - First-class workload in the Fabric portal
- **Zero ETL** - Transform OneLake data directly to graphs
- **Full Analytics** - 65+ algorithms, Cypher queries, visualization
- **Enterprise Ready** - Inherits Fabric security and governance
- **One-Click Setup** - Install from the Workload Hub

**Unlock the relationships hidden in your OneLake data.**

---

## Learn More

**Resources:**
- [Neo4j Graph Analytics for Microsoft Fabric](https://go.neo4j.com/MicrosoftFabric.html)
- [Neo4j Fabric Workload Documentation](https://neo4j.com/docs/aura/microsoft-fabric/)
- [Announcing the Neo4j Graph Workload](https://neo4j.com/blog/auradb/graph-analytics-workload/)

**Next Steps:**
1. Install the Neo4j workload in your Fabric workspace
2. Connect to a Lakehouse with your data
3. Create your first graph model
4. Run algorithms and explore connections

