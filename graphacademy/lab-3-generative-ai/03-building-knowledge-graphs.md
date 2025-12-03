# From Documents to Knowledge Graphs

## Introduction

Traditional RAG treats documents as isolated text chunks. GraphRAG transforms them into structured knowledge—entities connected by relationships that capture meaning and enable intelligent retrieval.

In this lesson, you'll learn how the transformation works: from raw PDF documents to a queryable knowledge graph.

## What is a Knowledge Graph?

A knowledge graph represents information as:

- **Nodes (Entities)**: Things in your domain—companies, people, products, risks, metrics
- **Relationships**: How entities connect—OWNS, FACES_RISK, MENTIONS, WORKS_FOR
- **Properties**: Attributes of nodes and relationships—names, values, dates

Unlike flat document storage, knowledge graphs preserve the *structure* inherent in information. They capture not just what things are, but how they relate.

![A graph data model showing an Asset Manager who OWNS a Company.](../images/manager-company-data-model.svg)

## The SEC Filings Example

![An Apple SEC EDGAR filing PDF](../images/apple-edgar-pdf.png)

Throughout this workshop, you'll work with a knowledge graph built from SEC 10-K filings. These documents contain rich information:

- Companies and their business descriptions
- Risk factors they face
- Financial metrics they report
- Products and services they mention
- Executives who lead them

In raw PDF form, this information is locked in narrative text. In a knowledge graph, it becomes structured and queryable:

```
(Apple Inc)-[:FACES_RISK]->(Cybersecurity Threats)
(Apple Inc)-[:MENTIONS]->(iPhone)
(BlackRock Inc)-[:OWNS]->(Apple Inc)
```

## The neo4j-graphrag Python Package

The `neo4j-graphrag` package provides tools for building and querying knowledge graphs. The key component for graph construction is `SimpleKGPipeline`.

**What SimpleKGPipeline does:**
1. Extracts text from documents (PDFs, text files)
2. Breaks text into manageable chunks
3. Uses an LLM to identify entities and relationships
4. Stores the structured data in Neo4j
5. Creates vector embeddings for semantic search

This pipeline orchestrates the entire transformation from documents to knowledge graph.

## The Transformation Process

**Step 1: Document Ingestion**

The pipeline reads source documents—in this case, SEC 10-K filings as PDFs. These contain hundreds of pages of financial and business information.

**Step 2: Chunking**

Long documents are broken into smaller pieces for processing. Each chunk becomes a node in the graph, linked to its source document. (You'll learn about chunking strategies in a later lesson.)

**Step 3: Entity Extraction**

An LLM analyzes each chunk to identify entities—companies, products, risks, metrics, people. These become nodes in the graph.

**Step 4: Relationship Extraction**

The LLM also identifies how entities relate. "Apple faces cybersecurity risks" becomes a FACES_RISK relationship. "The Company reported revenue growth" becomes a HAS_METRIC relationship.

**Step 5: Graph Storage**

Entities and relationships are stored in Neo4j, creating a queryable knowledge graph.

**Step 6: Vector Embeddings**

Chunks receive vector embeddings, enabling semantic search alongside graph traversal.

![A graph data model showing the relationship between chunks that have embeddings, the documents, and the company they relate to.](../images/document-chunk-data-model.svg)

## The Complete Picture

After processing, your knowledge graph contains:

```
Documents → Chunks (with embeddings)
    ↓
Entities (Company, Product, RiskFactor, Executive, FinancialMetric)
    ↓
Relationships (FACES_RISK, MENTIONS, OWNS, WORKS_FOR, HAS_METRIC)
```

This structure enables questions that traditional RAG can't answer:

| Question Type | How the Graph Helps |
|--------------|---------------------|
| "What risks does Apple face?" | Traverse FACES_RISK relationships |
| "Which companies mention AI?" | Find MENTIONS relationships to AI products |
| "Who owns Apple?" | Follow OWNS relationships from asset managers |
| "How many risk factors are there?" | Count RiskFactor nodes |

## Using SimpleKGPipeline

The pipeline brings together LLM, embedder, schema, and database connection:

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

The pipeline handles the complexity of:
- Text extraction from PDFs
- Chunking with configurable size and overlap
- Prompting the LLM for entity/relationship extraction
- Storing nodes and relationships in Neo4j
- Creating and indexing embeddings

## Quality Depends on Decisions

The quality of your knowledge graph depends on several key decisions:

- **Schema design**: What entities and relationships should you extract?
- **Chunking strategy**: How large should chunks be?
- **Entity resolution**: How do you handle the same entity mentioned differently?
- **Prompt engineering**: How do you guide the LLM to extract accurately?

In the following lessons, you'll learn about each of these decisions and how they affect your graph.

## Exploring the Graph

Once built, you can explore the graph with Cypher:

```cypher
// See all node types and counts
MATCH (n)
RETURN labels(n) AS nodeType, count(n) AS count
ORDER BY count DESC

// Explore a company's connections
MATCH (c:Company {name: 'APPLE INC'})-[r]->(related)
RETURN type(r) AS relationship, labels(related)[0] AS relatedType, count(*) AS count
```

## Summary

In this lesson, you learned:

- **Knowledge graphs** represent information as entities, relationships, and properties
- **SimpleKGPipeline** orchestrates the transformation from documents to graphs
- **The process**: Document → Chunks → Entity Extraction → Relationship Extraction → Graph Storage → Embeddings
- **Graph structure** enables queries that traverse relationships, not just find similar text

The quality of your knowledge graph depends on schema design, chunking, entity resolution, and prompts. In the next lesson, you'll learn about schema design—defining what entities and relationships your graph should capture.

---

**Navigation:**
- [← Previous: Context and Traditional RAG](02-context-and-rag.md)
- [↑ Back to Lab 3](README.md)
- [Next: Schema Design →](04-schema-design.md)
