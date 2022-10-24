# hands-on-lab-neo4j-and-azure-ml
Neo4j is the [leading graph database](https://neo4j.com/whitepapers/forrester-wave-graph-data-platforms/) vendor.  Our products, Neo4j Graph Database, Graph Data Science and Bloom are offered in the Azure Marketplace

In this hands on lab, you’ll get to learn about Neo4j and Azure Machine Learning.  The lab is intended for data scientists and data engineers.  We’ll walk through deploying Neo4j and Machine Learning on Azure in your own Azure account.  Then we’ll get hands on with a real world dataset, building a machine learning pipeline that takes advantage of features generated using Neo4j Graph Data Science to improve prediction in Azure Machine Learning.  You’ll come out of this lab with enough knowledge to apply graph feature engineering to your own datasets.

We’re going to analyze the quarterly filings of asset managers with $100m+ assets under management (AUM).  These are regulatory filings made to the Securities and Exchange Commission’s (SEC) EDGAR system.  We’re going to show how to load that data into Neo4j.  We’ll then explore the relationships of different asset managers and their holdings using the Neo4j Browser and Neo4j’s Cypher query language.

Finally, we’ll use Neo4j Graph Data Science to create a graph embedding from our data, export that out, and run supervised learning algorithms in Azure Machine Learning.  We’ll try to predict what holdings asset managers will maintain or enlarge in the next quarter.  

If you’re in the capital markets space, we think you’ll be interested in potential applications of this approach to creating new features for algorithmic trading, understanding tail risk, securities master data management and so on.  If you’re not in the capital markets space, this session will still be useful to learn about building machine learning pipelines with Neo4j and Azure ML.


## Duration
3 hours.

## Prerequisites
You'll need a laptop with a web browser. Your browser will need to be able to access the Azure Portal and port 7474 on a Neo4j deployment running on Azure.  If your laptop has a firewall you can't control on it, you may want to bring your personal laptop.

If you have an Azure account already, you may be able to use that.  You would need permissions that allow you to deploy an Azure ML instance and deploy a Neo4j Enterprise Edition template from the Marketplace. If your access doesn't meet those requirements, we'll walk you through creating a new account with full access.

## Agenda

### Part 1
* Introductions
* Lecture - Introduction to Neo4j (15 min)
    * What is Neo4j?
    * Customer use cases
    * How is it deployed and managed on Azure?
* [Lab 0 - Signup for Azure](Lab%200%20-%20Signup%20for%20Azure) (15 min)
    * Improving the Labs
    * Signup for Azure
* [Lab 1 - Deploy Neo4j](Lab%201%20-%20Deploy%20Neo4j) (15 min)
    * Deploy Neo4j Enterprise Edition through the Marketplace
    * CloudFormation Template
* [Lab 2 - Connect to Neo4j](Lab%202%20-%20Connect%20to%20Neo4j/README.md) (15 min)
    * Neo4j Browser
    * Neo4j Bloom
    * Interacting via Shell
* Break (5 min)

### Part 2
* Lecture - Moving Data (10 min)
    * LOAD CSV
* [Lab 3 - Moving Data](Lab%203%20-%20Moving%20Data/README.md) (15 min)
    * A Day of Data
    * A Year of Data
* [Lab 4 - Exploring Data](Lab%204%20-%20Exploring%20Data/README.md) 10 min)
    * Vizualization with Neo4j Bloom
* Break (5 min)

### Part 3
* Lecture - Azure ML (10 min)
    * What is Azure ML?
    * Using Azure ML with Neo4j
* [Lab 5 - AzureML](Lab%205%20-%20AzureML) (15 min)
    * Create a Azure ML Instance
    * Import from GitHub to Azure ML Studio
    * Cypher
* Break (5 min)

### Part 4
* Lecture - Graph Data Science (10 min)
    * Why Graph Data Science
    * Similarity
    * Centrality
    * Community Detection
    * Graph Machine Learning
    * Using Azure ML with Neo4j
* [Lab 6 - Graph Data Science](Lab%206%20-%20Graph%20Data%20Science/README.md) (15 min)
    * Create a Graph Embedding
    * Autopilot on Embeddings
    * Autopilot on Raw Data
* [Lab 7 - Cleanup](Lab%207%20-%20Cleanup) (15 min)
* [Discussion - Questions and Next Steps](Discussion%20-%20Questions%20and%20Next%20Steps.md) (5 min)
