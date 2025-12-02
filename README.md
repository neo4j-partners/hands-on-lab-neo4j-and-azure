# hands-on-lab-neo4j-and-azure
Neo4j is the [leading graph database](https://db-engines.com/en/ranking/graph+dbms) vendor.  We've worked closely with Microsoft Azure engineering for years.  Our products, AuraDB and AuraDS are offered as managed services on Azure.  Neo4j Aura Professional Edition is offered in the [Azure Marketplace](https://portal.azure.com/#create/neo4j.neo4j_aura_professional).

In this hands-on lab, you'll learn about Neo4j, Microsoft Azure AI Foundry, and the [Microsoft Agent Framework](https://github.com/microsoft/agent-framework). The lab is designed for data scientists, data engineers, and AI developers who want to master GraphRAG (Graph Retrieval-Augmented Generation) techniques and build production-ready agentic AI applications.

You'll work with a real-world dataset of SEC 10-K company filings to learn fundamental GraphRAG patterns. We'll start by building a knowledge graph from unstructured text using generative AI for entity extraction. Then you'll implement multiple retrieval strategies: vector similarity search for semantic retrieval, graph-enhanced retrievers that leverage entity relationships, and natural language to Cypher query generation. Finally, you'll build intelligent agents using the Microsoft Agent Framework that can autonomously reason over your knowledge graph to answer complex questions.

By the end of this lab, you'll have hands-on experience with:
- Building knowledge graphs from unstructured documents
- Implementing semantic search with vector embeddings
- Creating graph-enhanced retrieval patterns for richer context
- Developing agentic AI systems that combine multiple tools and reasoning strategies
- Deploying GraphRAG applications on Azure infrastructure

These techniques apply to any domain where you need to extract insights from documents, understand entity relationships, and build AI systems that can reason over complex information networks.

## Starting the Lab

To get started, follow the labs in the agenda below in order.

If you already have your Azure account and Aura connection details, you can go straight to [Lab 2 - Start Codespace](Lab_2_Start_Codespace) to start the codespace and begin running the notebooks.

## Duration
3 hours.

## Prerequisites
You'll need a laptop with a web browser.  Your browser will need to be able to access the Azure Console.  If your laptop has a firewall you can't control on it, you may want to bring your personal laptop.

## Agenda
### Part 1 - Getting Started
* Introductions
* [Lecture - Introduction to Neo4j](https://docs.google.com/presentation/d/1mEXn02TMYJ0nGFj7u5VANQBl1jBJcLGp6dYHB_xY0pQ/edit?usp=sharing) (10 min)
    * What is Neo4j?
    * How is it deployed and managed on Azure?
* [Lab 0 - Sign In](Lab_0_Sign_In) (5 min)
    * Improving the Labs
    * Sign into Azure
* [Lab 1 - Neo4j Aura Signup](Lab_1_Neo4j_Aura_Signup) (15 min)
    * Signing up for Neo4j Aura
* [Lab 2 - Start Codespace](Lab_2_Start_Codespace) (10 min)
    * Launch GitHub Codespace
    * Configure environment variables
* Break (5 min)

### Part 2 - Building a Knowledge Graph
* [Lecture - Neo4j and Generative AI](https://docs.google.com/presentation/d/1iHu9vgEG0s6yjKMLUw9XqWGiJrY7Z1oNv0QPa75BCtc/edit?usp=sharing) (15 min)
    * Generating Knowledge Graphs
    * Retrieval Augmented Generation
    * Semantic Search
* [Lab 3 - Building a Knowledge Graph](Lab_3_Graph_Building) (30 min)
    * Data Loading Fundamentals
    * Embeddings and Vector Search
    * Entity Extraction
    * Loading the Full Dataset
* [Lab 4 - Exploring the Knowledge Graph](Lab_4_Explore_Knowledge_Graph) (15 min)
    * Visual Graph Exploration with Neo4j Explore
    * Graph Data Science Algorithms
* Break (5 min)

### Part 3 - GraphRAG Retrievers
* [Lecture - Azure OpenAI](https://docs.google.com/presentation/d/1KPHoVJivbinHg-UtrnTIUbMiFHB8mPEnDO0v0OvvcPM/edit?usp=sharing) (15 min)
    * What is Azure OpenAI?
    * Generative AI
* [Lab 5 - GraphRAG Retrievers](Lab_5_GraphRAG_Retrievers) (30 min)
    * Vector Retriever for Semantic Search
    * Vector Cypher Retriever for Graph-Enhanced Context
    * Text2Cypher Retriever for Natural Language Queries
* Break (5 min)

### Part 4 - GraphRAG Agents
* [Lab 6 - GraphRAG Agents](Lab_6_Agents) (30 min)
    * Simple Schema Agent with Microsoft Agent Framework
    * Vector + Graph Agent for Semantic Search with Context
    * Multi-Tool Agent with Text2Cypher
* [Questions and Next Steps](Questions%20and%20Next%20Steps.md) (5 min)
