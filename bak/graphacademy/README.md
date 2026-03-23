# Neo4j & Generative AI Hands-On Workshop

Welcome to GraphAcademy and the Neo4j and Generative AI workshop.

**Duration:** 4 hours
**Level:** Workshop
**Status:** Active

## In this workshop you will:

- Learn about Generative AI, RAG, and GraphRAG
- Use Vector indexes and embeddings in Neo4j to perform similarity search
- Create vector, vector + cypher, and text to Cypher retrievers
- Build a conversational agent using Neo4j, Python, and LangChain

## What you will learn

- The basics of Generative AI and Large Language Models (LLMs)
- LLM limitations including hallucination and data access issues
- Why context is crucial for accurate LLM responses
- What Retrieval-Augmented Generation (RAG) is and why it is important
- How GraphRAG can improve the quality of LLM-generated content
- How to build knowledge graphs from unstructured PDF documents using entity extraction and relationship mapping
- How to enrich knowledge graphs with structured data using Neo4j Data Importer
- Schema design best practices for knowledge graphs
- Chunk size optimization for entity extraction
- Entity resolution techniques
- How to use Vectors in Neo4j for similarity search
- To build different types of retrievers using the `neo4j-graphrag` for Python package
- To create a conversational agent using Neo4j, Python, and LangChain
- How to configure different LLMs for various tasks

## Prerequisites

Before taking this workshop, you should have:

- A basic understanding of Graph Databases and Neo4j
- Able to read and understand basic Cypher queries
- Knowledge of Python and capable of reading simple programs

We recommend taking the [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/) course.

## This workshop includes

- **24 lessons** across 3 modules
- **10 hands-on notebooks** across 3 labs

## Workshop Modules

### [Module 1: Building Knowledge Graphs](./lab-5-knowledge-graph/README.md)
Learn to build knowledge graphs from unstructured documents. **Aligned with Lab 5 (4 notebooks).**

**Lessons:**
1. [What is Generative AI](./module-1-generative-ai/01-what-is-genai.md) - Foundation concepts
2. [LLM Limitations](./module-1-generative-ai/02-llm-limitations.md) - Understanding constraints
3. [Context](./module-1-generative-ai/03-context.md) - Why RAG matters
4. [Building the Graph](./module-1-generative-ai/04-building-the-graph.md) - Documents, chunks, entities
5. [Schema Design](./module-1-generative-ai/05-schema-design.md) - Entity types and relationships
6. [Optimizing Chunk Size](./module-1-generative-ai/06-chunking.md) - Chunking strategies
7. [Entity Resolution](./module-1-generative-ai/07-entity-resolution.md) - Resolving duplicates
8. [Vectors](./module-1-generative-ai/08-vectors.md) - Embeddings and semantic search
9. [Working with Full Datasets](./module-1-generative-ai/09-full-dataset.md) - Production-scale graphs

### [Module 2: GraphRAG Retrievers](./lab-6-retrievers/README.md)
Master three retriever patterns for intelligent information retrieval. **Aligned with Lab 6 (3 notebooks).**

**Lessons:**
1. [Understanding GraphRAG](./module-2-retrievers/01-graphrag-explained.md) - Why GraphRAG matters
2. [What is a Retriever](./module-2-retrievers/02-what-is-a-retriever.md) - Retriever fundamentals
3. [Vector Retriever](./module-2-retrievers/03-vector-retriever.md) - Semantic similarity search
4. [Vector Cypher Retriever](./module-2-retrievers/04-vector-cypher-retriever.md) - Semantic + graph traversal
5. [Text2Cypher Retriever](./module-2-retrievers/05-text2cypher-retriever.md) - Natural language to queries
6. [Choosing the Right Retriever](./module-2-retrievers/06-choosing-retrievers.md) - Decision framework

### [Module 3: Intelligent Agents](./lab-7-agents/README.md)
Build agents that automatically choose the right retriever. **Aligned with Lab 7 (3 notebooks).**

**Lessons:**
1. [What is an Agent](./module-3-agents/01-what-is-an-agent.md) - Agent concepts
2. [Microsoft Agent Framework](./module-3-agents/02-microsoft-agent-framework.md) - Framework overview
3. [Simple Schema Agent](./module-3-agents/03-simple-schema-agent.md) - Single tool agent
4. [Vector Graph Agent](./module-3-agents/04-vector-graph-agent.md) - Two-tool agent
5. [Text2Cypher Agent](./module-3-agents/05-text2cypher-agent.md) - Three-tool agent
6. [Multi-Tool Agent Design](./module-3-agents/06-multi-tool-design.md) - Tool selection patterns
7. [Aura Agents](./module-3-agents/07-aura-agents.md) - No-code platform (Optional)
8. [Best Practices](./module-3-agents/08-best-practices.md) - Agent design (Optional)
9. [Congratulations](./module-3-agents/09-congratulations.md) - Workshop summary

## Workshop Materials

### 📚 Reading Materials
- [Module 1: Building Knowledge Graphs](./lab-5-knowledge-graph/README.md)
- [Module 2: GraphRAG Retrievers](./lab-6-retrievers/README.md)
- [Module 3: Intelligent Agents](./lab-7-agents/README.md)

### 📊 Presentation Slides
- [**All Workshop Slides**](./slides/README.md) - 15 Marp presentations ready for teaching
- Perfect for instructors and workshop facilitators
- Export to PDF, HTML, or present directly
- **Latest Update:** Phase 1 & 2 slides complete (75% coverage) ✅

### 🖼️ Images
- [All Images](./images/) - 22 diagrams and illustrations

### 📖 Documentation
- [Navigation Guide](./NAVIGATION.md) - How to read the content
- [Review Report](./REVIEW_COMPLETE.md) - Content verification details
- [Images Setup](./IMAGES_SETUP.md) - Image documentation
- [Phase 1 & 2 Complete](./PHASE_1_2_COMPLETE.md) - New slides summary
- [Gap Summary](./GAP_SUMMARY.md) - Updated coverage analysis

## Navigation

- [Start with Module 1: Building Knowledge Graphs →](./lab-5-knowledge-graph/README.md)
- [View Presentation Slides →](./slides/README.md)

---

**Repository:** [neo4j-graphacademy/workshop-genai](https://github.com/neo4j-graphacademy/workshop-genai)
