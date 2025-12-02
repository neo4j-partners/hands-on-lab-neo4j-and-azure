# hands-on-lab-neo4j-and-azure
Neo4j is the [leading graph database](https://db-engines.com/en/ranking/graph+dbms) vendor.  We’ve worked closely with Microsoft Azure engineering for years.  Our products, AuraDB and AuraDS are offered as managed services on Azure.  Neo4j Aura Professional Edition is offered in the [Azure Marketplace](https://portal.azure.com/#create/neo4j.neo4j_aura_professional).

In this hands on lab, you’ll get to learn about Neo4j, Azure ML and the Azure OpenAI Service.  The lab is intended for data scientists and data engineers.  We’ll walk through deploying Neo4j and Azure ML in an Azure account.  Then we’ll get hands on with a real world dataset.  First we'll use generative AI to parse and load data.  Then we'll show how to layer a chatbot powered by generative AI with LangChain over the knowledge graph.  We'll even use the new vector search and index functionality in Neo4j with Azure OpenAI Service for semantic search.  You’ll come out of this lab with enough knowledge to apply graph generative AI to your own datasets.

We’re going to analyze the quarterly filings of asset managers with $100m+ assets under management (AUM).  These are regulatory filings made to the Securities and Exchange Commission’s (SEC) EDGAR system.  We’re going to show how to load that data from Azure Blob Storage into Neo4j.  We’ll then explore the relationships of different asset managers and their holdings using the Neo4j Browser and Neo4j’s Cypher query language.

If you’re in the capital markets space, we think you’ll be interested in potential applications of this approach to creating new features for algorithmic trading, understanding tail risk, securities master data management and so on.  If you’re not in the capital markets space, this session will still be useful to learn about building machine learning pipelines with Neo4j and the Azure OpenAI Service.

## Starting the Lab

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/neo4j-partners/hands-on-lab-neo4j-and-azure)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/neo4j-partners/hands-on-lab-neo4j-and-azure)


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

### Part 3 - RAG Retrievers
* [Lecture - Azure OpenAI](https://docs.google.com/presentation/d/1KPHoVJivbinHg-UtrnTIUbMiFHB8mPEnDO0v0OvvcPM/edit?usp=sharing) (15 min)
    * What is Azure OpenAI?
    * Generative AI
* [Lab 5 - RAG Retrievers](Lab_5_RAG_Retrievers) (30 min)
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
