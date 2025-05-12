# hands-on-lab-neo4j-and-azure
Neo4j is the [leading graph database](https://db-engines.com/en/ranking/graph+dbms) vendor.  We’ve worked closely with Microsoft Azure engineering for years.  Our products, AuraDB and AuraDS are offered as managed services on Azure.  Neo4j Aura Professional Edition is offered in the [Azure Marketplace](https://portal.azure.com/#create/neo4j.neo4j_aura_professional).

In this hands on lab, you’ll get to learn about Neo4j, Azure ML and the Azure OpenAI Service.  The lab is intended for data scientists and data engineers.  We’ll walk through deploying Neo4j and Azure ML in an Azure account.  Then we’ll get hands on with a real world dataset.  First we'll use generative AI to parse and load data.  Then we'll show how to layer a chatbot powered by generative AI with LangChain over the knowledge graph.  We'll even use the new vector search and index functionality in Neo4j with Azure OpenAI Service for semantic search.  You’ll come out of this lab with enough knowledge to apply graph generative AI to your own datasets.

We’re going to analyze the quarterly filings of asset managers with $100m+ assets under management (AUM).  These are regulatory filings made to the Securities and Exchange Commission’s (SEC) EDGAR system.  We’re going to show how to load that data from Azure Blob Storage into Neo4j.  We’ll then explore the relationships of different asset managers and their holdings using the Neo4j Browser and Neo4j’s Cypher query language.

If you’re in the capital markets space, we think you’ll be interested in potential applications of this approach to creating new features for algorithmic trading, understanding tail risk, securities master data management and so on.  If you’re not in the capital markets space, this session will still be useful to learn about building machine learning pipelines with Neo4j and the Azure OpenAI Service.

## Venue
These workshops are organized onsite in a Microsoft office.

## Duration
3 hours.

## Prerequisites
You'll need a laptop with a web browser.  Your browser will need to be able to access the Azure Console.  If your laptop has a firewall you can't control on it, you may want to bring your personal laptop.

## Agenda
### Part 1
* Introductions
* [Lecture - Introduction to Neo4j](https://docs.google.com/presentation/d/1mEXn02TMYJ0nGFj7u5VANQBl1jBJcLGp6dYHB_xY0pQ/edit?usp=sharing) (10 min)
    * What is Neo4j?
    * How is it deployed and managed on Azure?
* [Lab 0 - Sign In](Lab%201%20-%20Neo4j%20Aura%20Signup) (5 min)
    * Improving the Labs
    * Sign into Azure
* [Lab 1 - Deploy Neo4j](Lab%201%20-%20Deploy%20Neo4j) (15 min)
    * Signing up Aura DS Instance
* Break (5 min)

### Part 2
* [Lecture - Importing Data](https://docs.google.com/presentation/d/1B7pyEKfDRrwKQrfdjN7udM0bWYedPXaFUBM1LKyBdEk/edit?usp=sharing) (10 min)
    * LOAD CSV
* [Lab 3 - Importing Data](Lab%203%20-%20Importing%20Data/README.md) (15 min)
    * Using Data Importer
* [Lab 4 - Exploration](Lab%204%20-%20Exploration/README.md) 10 min)
    * Exploration with Neo4j Aura
* Break (5 min)

### Part 3
* [Lecture - Azure OpenAI](https://docs.google.com/presentation/d/1KPHoVJivbinHg-UtrnTIUbMiFHB8mPEnDO0v0OvvcPM/edit?usp=sharing) (15 min)
    * What is Azure OpenAI?
    * Generative AI
* [Lecture - Neo4j and Generative AI](https://docs.google.com/presentation/d/1iHu9vgEG0s6yjKMLUw9XqWGiJrY7Z1oNv0QPa75BCtc/edit?usp=sharing) (15 min)
    * Generating Knowledge Graphs
    * Retrieval Augmented Generation
    * Semantic Search
    * Using Azure OpenAI Service with Neo4j
* [Lab 5 - Parsing Data](Lab%205%20-%20Parsing%20Data/README.md) (20 min)
    * Create an Azure ML Service
    * Setup Azure OpenAI
    * Import Lab Notebooks to ML Studio
    * Parsing Data
* [Lab 6 - Chatbot](Lab%206%20-%20Chatbot/README.md) (20 min)
    * Prompt Engineering 
    * Few Shot Learning
    * Using the Chatbot
* [Lab 7 - Semantic Search](Lab%207%20-%20Semantic%20Search/README.md) (20 min)
    * Text Embedding
    * Vector Search
    * Graph Traversal
    * Graph Algorithms for Similairty
* [Questions and Next Steps](Questions%20and%20Next%20Steps.md) (5 min)
