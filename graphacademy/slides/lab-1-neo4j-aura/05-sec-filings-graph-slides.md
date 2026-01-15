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


# The SEC Filings Knowledge Graph

---

## The SEC Filings Example

Throughout this workshop, you'll work with a knowledge graph built from SEC 10-K filings.

**These documents contain:**
- Companies and their business descriptions
- Risk factors they face
- Financial metrics they report
- Products and services they mention
- Executives who lead them

---

![bg contain](../images/structured_text.jpg)

---

## What the Graph Enables

| Question Type | How the Graph Helps |
|--------------|---------------------|
| "What risks does Apple face?" | Traverse FACES_RISK relationships |
| "Which companies mention AI?" | Find MENTIONS relationships to AI products |
| "Who owns Apple?" | Follow OWNS relationships from asset managers |
| "How many risk factors are there?" | Count RiskFactor nodes |

---

## The Pre-Built Knowledge Graph

The graph you restored to your Aura instance has already been processed:

**What was done (Lab 5 covers this in detail):**
- SEC 10-K filing PDFs were ingested
- Documents were chunked into smaller pieces
- An LLM extracted entities and relationships
- Vector embeddings were generated for semantic search

**You get the finished result** ready for exploration with Aura Agents.

---

![bg contain](../images/complete_graph.jpg)

---

## The Processing Pipeline (Preview)

This is what Lab 5 covers in depth:

| Step | What Happens |
|------|--------------|
| **Document Ingestion** | Read SEC 10-K filing PDFs |
| **Chunking** | Break into smaller pieces for processing |
| **Entity Extraction** | LLM identifies companies, products, risks |
| **Relationship Extraction** | LLM finds connections between entities |
| **Graph Storage** | Save entities and relationships to Neo4j |
| **Vector Embeddings** | Generate embeddings for semantic search |

---

![bg contain](../images/building_graph.jpg)

---

## Ready to Explore with Aura Agents

With the knowledge graph pre-built, you can now:

1. **Create an Aura Agent** connected to your graph
2. **Configure retrieval tools** (Cypher templates, similarity search, Text2Cypher)
3. **Ask complex questions** that combine graph traversal and semantic search
4. **See how GraphRAG works** before diving into the code

**Next:** Build your SEC Filings Analyst agent with Aura Agents.

