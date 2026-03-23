# hands-on-lab-neo4j-and-azure
Neo4j is the [leading graph database](https://db-engines.com/en/ranking/graph+dbms) vendor.  We’ve worked closely with Microsoft engineering for years.  Our SaaS database, Neo4j Aura, is offered as a managed service on Azure.  This is available through the [Azure Marketplace](https://marketplace.microsoft.com/en-us/product/neo4j.neo4j-aura).

In this hands on lab, you’ll get to learn about [Neo4j](https://neo4j.com/) and [Microsoft Foundry](https://azure.microsoft.com/en-us/products/ai-foundry).  The lab is intended for data scientists and data engineers.  We’ll walk through deploying Neo4j and Foundry in a Microsoft Azure account.  Then we’ll get hands on with a real world dataset.  First we'll use AI to parse and load data.  Then we'll show how to layer an AI agent over the knowledge graph.  You’ll come out of this lab with enough knowledge to apply graph AI to your own datasets.

We’re going to analyze the quarterly filings of asset managers with $100m+ assets under management (AUM).  These are regulatory filings made to the Securities and Exchange Commission’s (SEC) EDGAR system.  We’re going to show how to load that data from a Google Cloud Storage bucket into Neo4j.  We’ll then explore the relationships of different asset managers and their holdings using the Neo4j Browser and Neo4j’s Cypher query language.

If you’re in the capital markets space, we think you’ll be interested in potential applications of this approach to creating new features for algorithmic trading, understanding tail risk, securities master data management and so on.  If you’re not in the capital markets space, this session will still be useful to learn about building agentic AI pipelines with Neo4j and Microsoft Foundry.

## Venue
These workshops are organized onsite in a Microsoft office.

## Duration
3 hours.

## Prerequisites
You'll need a laptop with a web browser.  Your browser will need to be able to access the Azure Portal and port 7474 on a Neo4j deployment running on Azure.  If your laptop has a firewall you can't control, you may want to bring your personal laptop.

## Agenda
### Part 1
* Introductions
* Lecture - [Introduction to Neo4j](https://docs.google.com/presentation/d/1mEXn02TMYJ0nGFj7u5VANQBl1jBJcLGp6dYHB_xY0pQ/edit?usp=sharing) (10 min)
    * What is Neo4j?
    * How is it deployed and managed on Microsoft Azure?
* [Lab 0 - Sign In](Lab%200%20-%20Sign%20In) (5 min)
    * Improving the Labs
    * Sign into Microsoft Azure
* [Lab 1 - Deploy Neo4j](Lab%201%20-%20Deploy%20Neo4j) (15 min)
    * Deploying Neo4j Aura Professional
* [Lab 2 - Connect to Neo4j](Lab%202%20-%20Connect%20to%20Neo4j/README.md) (10 min)
* Break (5 min)

### Part 2
* Lecture - [Moving Data](https://docs.google.com/presentation/d/1B7pyEKfDRrwKQrfdjN7udM0bWYedPXaFUBM1LKyBdEk/edit?usp=sharing) (10 min)
    * LOAD CSV
    * Knowledge Graph Builder
    * Apache Spark and Azure Databricks
    * Apache Kafka and Azure Event Hubs
* [Lab 3 - Moving Data](Lab%203%20-%20Moving%20Data/README.md) (15 min)
    * Simple Load Statement
    * More Performant Load
* [Lab 4 - Exploration](Lab%204%20-%20Exploration/README.md) 10 min)
    * Exploration with Neo4j Bloom
* Break (5 min)

### Part 3
* Lecture - Foundry (15 min)
    * Microsoft and AI
    * What is Foundry
* Lecture - [Neo4j and AI](https://docs.google.com/presentation/d/1iHu9vgEG0s6yjKMLUw9XqWGiJrY7Z1oNv0QPa75BCtc/edit?usp=sharing) (15 min)
    * Generating Knowledge Graphs
    * Retrieval Augmented Generation
    * Semantic Search
    * Using AI with Neo4j
* [Lab 5 - Aura Agents](Lab%205%20-%20Aura%20Agents/README.md) (20 min)
* [Lab 6 - Foundry Agents](Lab%206%20-%20Foundry%20Agents/README.md) (20 min)
* [Questions and Next Steps](Questions%20and%20Next%20Steps.md) (5 min)