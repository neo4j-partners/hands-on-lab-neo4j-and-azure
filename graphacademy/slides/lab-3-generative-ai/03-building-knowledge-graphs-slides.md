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


# From Documents to Knowledge Graphs

---

## What is a Knowledge Graph?

A knowledge graph represents information as:

- **Nodes (Entities)**: Things in your domain—companies, people, products, risks
- **Relationships**: How entities connect—OWNS, FACES_RISK, MENTIONS, WORKS_FOR
- **Properties**: Attributes of nodes and relationships—names, values, dates

Unlike flat document storage, knowledge graphs preserve the *structure* inherent in information.

---

## The SEC Filings Example

Throughout this workshop, you'll work with a knowledge graph built from SEC 10-K filings.

**These documents contain:**
- Companies and their business descriptions
- Risk factors they face
- Financial metrics they report
- Products and services they mention
- Executives who lead them

**In a knowledge graph, this becomes structured and queryable.**

---

## From PDF to Graph

**In raw PDF form:** Information is locked in narrative text.

**In a knowledge graph:** It becomes structured and queryable:

```
(Apple Inc)-[:FACES_RISK]->(Cybersecurity Threats)
(Apple Inc)-[:MENTIONS]->(iPhone)
(BlackRock Inc)-[:OWNS]->(Apple Inc)
```

---

## The neo4j-graphrag Python Package

The `neo4j-graphrag` package provides tools for building and querying knowledge graphs.

**The key component: `SimpleKGPipeline`**

What it does:
1. Extracts text from documents (PDFs, text files)
2. Breaks text into manageable chunks
3. Uses an LLM to identify entities and relationships
4. Stores the structured data in Neo4j
5. Creates vector embeddings for semantic search

---

## The Transformation Process

![height:400px](images/8.png)

---

## Step-by-Step Transformation

| Step | What Happens |
|------|--------------|
| **Document Ingestion** | Read source documents (PDFs) |
| **Chunking** | Break into smaller pieces for processing |
| **Entity Extraction** | LLM identifies companies, products, risks, metrics |
| **Relationship Extraction** | LLM finds connections between entities |
| **Graph Storage** | Save entities and relationships to Neo4j |
| **Vector Embeddings** | Generate embeddings for semantic search |

---

## Using SimpleKGPipeline

```python
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline

pipeline = SimpleKGPipeline(
    driver=driver,           # Neo4j connection
    llm=llm,                 # LLM for entity extraction
    embedder=embedder,       # Embedding model for vectors
    entities=entities,       # Schema: what entities to extract
    relations=relations,     # Schema: what relationships to find
    prompt_template=prompt,  # Custom extraction instructions
)

# Process a document
await pipeline.run(file_path="apple-10K-2023.pdf")
```

---

## The Complete Picture

After processing, your knowledge graph contains:

```
Documents → Chunks (with embeddings)
    ↓
Entities (Company, Product, RiskFactor, Executive, FinancialMetric)
    ↓
Relationships (FACES_RISK, MENTIONS, OWNS, WORKS_FOR, HAS_METRIC)
```

This structure enables questions that traditional RAG can't answer.

---

## What the Graph Enables

| Question Type | How the Graph Helps |
|--------------|---------------------|
| "What risks does Apple face?" | Traverse FACES_RISK relationships |
| "Which companies mention AI?" | Find MENTIONS relationships to AI products |
| "Who owns Apple?" | Follow OWNS relationships from asset managers |
| "How many risk factors are there?" | Count RiskFactor nodes |

---

## Quality Depends on Decisions

The quality of your knowledge graph depends on several key decisions:

- **Schema design**: What entities and relationships should you extract?
- **Chunking strategy**: How large should chunks be?
- **Entity resolution**: How do you handle the same entity mentioned differently?
- **Prompt engineering**: How do you guide the LLM to extract accurately?

The following lessons cover each of these decisions.

---

## Summary

In this lesson, you learned:

- **Knowledge graphs** represent information as entities, relationships, and properties
- **SimpleKGPipeline** orchestrates the transformation from documents to graphs
- **The process**: Document → Chunks → Entity Extraction → Relationship Extraction → Graph Storage → Embeddings
- **Graph structure** enables queries that traverse relationships, not just find similar text

**Next:** Learn about schema design—defining what entities and relationships to extract.
