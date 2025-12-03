# Building a Graph

## Introduction

In this lesson, you will explore the knowledge graph we've prepared for this workshop and learn how it was built.

You'll start with a completed knowledge graph containing structured entities and relationships extracted from PDF documents. Then we'll show you the transformation process: how raw text became the structured data model you'll be working with.

## The Problem with Traditional RAG

Traditional RAG systems work - but they're blind to context:

- **Retrieves based on similarity, not understanding**
- **No map of your domain or business logic**
- **Treats all chunks as isolated, unstructured blobs**
- **Can't bridge relationships across documents**

## The Problem with Traditional RAG

**The Challenge with PDF Documents:**

- Rich information about companies, financials, and risks locked in unstructured text
- Hard to search, query, or analyze systematically
- Connections between entities are hidden in narrative text
- Traditional RAG can't reason across relationships

**The GraphRAG Solution:**

- Use AI to extract structured entities and relationships
- Create a knowledge graph that preserves connections
- Give the system a "mental map" of your domain
- Enable context-aware retrieval, not just similarity search

It's like giving someone index cards with code snippets vs. an architectural diagram - GraphRAG understands the structure.

## From PDF Documents to Knowledge Graph

![a graph data model showing the separation of structured and unstructured data.](../images/unstructured-structured.svg)

The knowledge graph you'll be exploring was built from unstructured PDF documents transformed into a structured, queryable format.

Let's walk through how this transformation happened - from the original data sources to the final knowledge graph you'll work with in this workshop.

## The Source: EDGAR SEC Filings

The knowledge graph you'll explore was built from EDGAR SEC filing PDF documents.

These documents contain valuable company information, but it was originally locked in free-form text that's difficult to query systematically.

**The Original Challenge:** How do you extract structured insights from thousands of pages of legal text about companies, executives, financial metrics, and business risks?

![a screenshot of an Apple SEC filing PDF document.](../images/apple-edgar-pdf.png)

## Step 1: Documents and Chunks

**Documents** in your knowledge graph are the original PDF files that were processed.

**Chunks** are smaller, semantically meaningful segments of text extracted from each document.

**Why This Chunking Strategy?**

- Improves retrieval and search accuracy
- Enables LLMs to process long documents effectively
- Each chunk becomes a searchable unit linked to its source
- Supports both granular search and traceability

This chunking strategy was crucial for creating a knowledge graph that works at multiple levels of granularity - from specific facts to document-level context. Unlike traditional RAG chunks, these chunks are connected to business entities and relationships.

**Verify Documents and Chunks:**

```cypher
// See what documents were processed and how many chunks each has
MATCH (d:Document)<-[:FROM_DOCUMENT]-(c:Chunk)
RETURN d.path, count(c) as totalChunks
ORDER BY totalChunks DESC
```

Now we have a way to access the unstructured data through chunks, but what about the structure that exists within the unstructured data?

PDF documents aren't truly "unstructured" - they contain rich business entities and relationships hidden in the text. Companies mention products, face risks, report financial metrics, and connect to executives. This structure just isn't explicit or queryable.

## Step 2: Schema-Driven Extraction

The knowledge graph was built using a defined schema combined with carefully crafted prompts to guide the AI extraction process.

**Schema Definition:**

**Entities:**

- Company
- Executive
- Product
- FinancialMetric
- RiskFactor
- StockType
- Transaction
- TimePeriod

**Relationships:**

* Company **HAS_METRIC** FinancialMetric
* Company **FACES_RISK** RiskFactor
* Company **ISSUED_STOCK** StockType
* Company **MENTIONS** Product

## Step 2: Guided Extraction Prompts

**Guided Extraction Prompts:**

The extraction process used carefully crafted prompts to ensure quality:

- **Company Validation:** Only extract approved companies from our list
- **Context Resolution:** Resolve "the Company" to actual company names
- **Schema Enforcement:** Strict adherence to defined entity types
- **Quality Control:** Validate all extracted relationships

This schema + prompt combination acted as the blueprint - telling the AI exactly what to look for and how to connect entities in the knowledge graph you'll explore. It's the difference between isolated chunks and a connected web of business knowledge.

## Step 3: The GraphRAG Pipeline

The complete pipeline orchestrated the transformation from PDF to knowledge graph using AI-powered extraction.

**The GraphRAG Pipeline:**

![Diagram showing the Neo4j GraphRAG pipeline process from PDF documents to knowledge graph](../images/8.png)

## Step 3: SimpleKGPipeline Example

```python
pipeline = SimpleKGPipeline(
    driver=driver, # Neo4j connection driver
    llm=llm, embedder=embedder,  # OpenAI llm and embeddings
    entities=entities, relations=relations,  # Define schema
    enforce_schema="STRICT",
    prompt_template=prompt_template,
)
# Process the SEC filing documents
pdf_documents = [
    "apple-10K-2023.pdf", "microsoft-10K-2023.pdf",
    # ... more company filings
]
# Run the pipeline to transform PDFs into knowledge graph
for pdf_file in pdf_documents:
    pipeline.run(file_path=pdf_file)
```

**What happened during `pipeline.run()`:**

1. **PDF Text Extraction:** Extracted raw text from PDF documents
2. **Document Chunking:** Broke text into semantically meaningful chunks
3. **Entity Extraction:** Used LLM to identify companies, metrics, risks, etc.
4. **Relationship Extraction:** Found connections between entities
5. **Graph Storage:** Saved structured entities and relationships to Neo4j
6. **Vector Embeddings:** Generated embeddings for chunks and stored them

This transformed hundreds of pages of unstructured PDF text into the queryable knowledge graph with thousands of connected entities.

## Step 3: Verify Entity Extraction

**Verify Entity Extraction:**

```cypher
// Count what entities were extracted by type
MATCH (e)
WHERE NOT e:Document AND NOT e:Chunk
RETURN labels(e) as entityType, count(e) as count
ORDER BY count DESC
```

## Step 4: Adding Structured Data

But PDF extraction was only part of the story. The knowledge graph also includes structured data loaded from CSV files to complement the extracted PDF entities.

**Structured Data Sources:**

- **Asset Manager Holdings:** Ownership information connecting asset managers to companies
- **Company Filing Information:** Metadata linking companies to their PDF documents

**Why Both Data Types?**

- **Unstructured (PDFs):** Rich content about companies, risks, metrics
- **Structured (CSVs):** Precise ownership data and document relationships

This created a complete picture: detailed company information from PDFs **plus** structured ownership and filing relationships. The bridge between structured and unstructured data enables the powerful GraphRAG queries you'll explore.

## Step 4: How the Data Was Loaded

**How The Data Was Loaded:**

1. **Neo4j Data Importer** processed the CSV files
2. **AssetManager nodes** were created from holdings data
3. **OWNS relationships** connected asset managers to companies with holding values
4. **FILED relationships** linked companies to their PDF documents

**Verify the Complete Graph:**

```cypher
// See the complete data model - all node types
MATCH (n)
RETURN labels(n) as nodeType, count(n) as count
ORDER BY count DESC
```

## Step 5: Exploring What Was Created

Now that we've seen how the knowledge graph was built, let's explore what was created. Your complete knowledge graph contains:

**The Complete Data Model:**

- **500+ Company entities** extracted from SEC filings
- **Asset Manager entities** with ownership information
- **2,000+ Financial metrics and risk factors** as structured nodes
- **Clear entity relationships** connecting business concepts
- **Document links** bridging structured and unstructured data

**Visualize the Complete Schema:**

```cypher
CALL db.schema.visualization()
```

This shows the complete knowledge graph schema including both extracted entities (Company, Product, FinancialMetric, etc.) and loaded structured data (AssetManager, ownership relationships) that you'll work with.

## Step 5: Explore a Complete Company Profile

**Explore a Complete Company Profile:**

```cypher
// See how all three data types connect for one company
MATCH (c:Company {name: 'APPLE INC'})
OPTIONAL MATCH (c)-[r1]->(extracted)
WHERE NOT extracted:Chunk AND NOT extracted:Document
OPTIONAL MATCH (am:AssetManager)-[r2:OWNS]->(c)
OPTIONAL MATCH (c)<-[:FROM_CHUNK]->(chunk:Chunk)
RETURN c.name,
       count(DISTINCT extracted) as extractedEntities,
       count(DISTINCT am) as assetManagers,
       count(DISTINCT chunk) as textChunks
```

## Key Takeaways

✅ **Unstructured → Structured:** PDF text was transformed into business entities and relationships

✅ **Schema-Driven:** Clear entity definitions guided accurate extraction

✅ **AI-Powered:** LLMs identified and extracted meaningful business concepts

✅ **Relationship-Aware:** Connections between entities were preserved and made explicit

✅ **Data Model Ready:** Clean, structured data prepared for the knowledge graph you'll explore

This structured data model is the foundation for everything that follows - without it, you'd still have unstructured text instead of the queryable business entities you'll work with!

## Summary

In this lesson, you learned how we extracted structured data from unstructured PDF documents:

**The Process:**

- Started with EDGAR SEC filing PDFs containing company information
- Defined a clear schema with entities (Company, Executive, Product, etc.) and relationships
- Applied AI-powered extraction with carefully crafted prompts to identify business entities
- Used guided extraction to ensure data quality and consistency
- Created structured entities and relationships from free-form text

**What Was Created:**

- 500+ company entities from SEC filings
- 2,000+ financial metrics and risk factors as structured nodes
- Clear entity relationships connecting business concepts
- Clean, structured data model ready for graph storage

**Key Technologies:**

- Schema definition for consistent entity extraction
- OpenAI GPT-4 for entity and relationship identification
- Guided prompts for data quality control
- Structured extraction pipeline

This structured data model is now ready to be stored in a knowledge graph and enhanced with vector embeddings for search.

In the next lesson, you will learn about vectors and embeddings that enable semantic search across this structured data.

---

**Navigation:**
- [← Previous: Context](03-context.md)
- [↑ Back to Module 1](README.md)
- [Next: Schema Design →](05-schema-design.md)
