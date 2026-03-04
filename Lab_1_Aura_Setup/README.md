# Lab 1: Neo4j Aura Setup and Exploration

In this lab, you will set up your Neo4j Aura database on Azure Marketplace, restore the knowledge graph from a backup, and explore your graph visually.

## Prerequisites

- Completed **Lab 0** (Azure sign-in)
- Access to Azure Portal

## Part 1: Neo4j Aura Signup

Follow the instructions in [Neo4j_Aura_Signup.md](Neo4j_Aura_Signup.md) to:

1. Subscribe to Neo4j Aura through Azure Marketplace
2. Create your Neo4j Aura account
3. Configure and provision your database instance
4. Save your connection credentials

## Part 2: Restore the Backup

After your Aura instance is running, restore the pre-built knowledge graph:

1. Go to your instance in the [Aura Console](https://console.neo4j.io)
2. Click the **...** menu on your instance and select **Backup & restore**

![](images/backup_restore.png)

3. Click **Upload backup** to open the upload dialog, then drag the backup file into the dialog:

   ![](images/restore_drag.png)

   **Use the pre-built backup file**
   - Drag the file `finance_data.backup` from the `data/` folder in this lab

4. Wait for the restore to complete - your instance will restart with the SEC 10-K filings knowledge graph

5. **Recreate indexes and constraints** - Aura exports are unrecovered backups, so indexes are not preserved. To recreate them:

   1. Go to [console.neo4j.io](https://console.neo4j.io) and click on your instance
   2. Select **Query** in the left sidebar to open the query console
   3. Copy and paste the following Cypher and click **Run**:

   ```cypher
   // Vector index for semantic search over chunk embeddings
   CREATE VECTOR INDEX chunkEmbeddings IF NOT EXISTS
   FOR (n:Chunk) ON (n.embedding)
   OPTIONS {indexConfig: {`vector.dimensions`: 1536, `vector.similarity_function`: 'cosine'}};
   ```

   ```cypher
   // Fulltext indexes for keyword search
   CREATE FULLTEXT INDEX chunkText IF NOT EXISTS FOR (n:Chunk) ON EACH [n.text];
   CREATE FULLTEXT INDEX search_entities IF NOT EXISTS FOR (n:Company|Product|RiskFactor|Executive|FinancialMetric) ON EACH [n.name];
   ```

   ```cypher
   // Uniqueness constraints
   CREATE CONSTRAINT unique_company_name IF NOT EXISTS FOR (n:Company) REQUIRE n.name IS UNIQUE;
   CREATE CONSTRAINT unique_asset_manager_name IF NOT EXISTS FOR (n:AssetManager) REQUIRE n.managerName IS UNIQUE;
   CREATE CONSTRAINT unique_riskfactor_name IF NOT EXISTS FOR (n:RiskFactor) REQUIRE n.name IS UNIQUE;
   CREATE CONSTRAINT unique_product_name IF NOT EXISTS FOR (n:Product) REQUIRE n.name IS UNIQUE;
   CREATE CONSTRAINT unique_executive_name IF NOT EXISTS FOR (n:Executive) REQUIRE n.name IS UNIQUE;
   CREATE CONSTRAINT unique_financialmetric_name IF NOT EXISTS FOR (n:FinancialMetric) REQUIRE n.name IS UNIQUE;
   ```

6. Verify the indexes are online by running `SHOW INDEXES` in the query console - all indexes should show state `"ONLINE"`

The backup contains:
- SEC 10-K filing documents from major companies (Apple, Microsoft, NVIDIA, etc.)
- Extracted entities: Companies, Risk Factors, Products, Executives, Financial Metrics
- Asset manager ownership data
- Text chunks with vector embeddings for semantic search

## Part 3: Explore the Knowledge Graph

Follow [EXPLORE.md](EXPLORE.md) to:

1. Use Neo4j Explore to visually navigate your graph
2. Search for patterns between asset managers, companies, and risk factors
3. Apply graph algorithms like Degree Centrality
4. Identify key entities through visual analysis

## Next Steps

After completing this lab, continue to [Lab 2 - Aura Agents](../Lab_2_Aura_Agents) to build an AI-powered agent using the Neo4j Aura Agent no-code platform.
