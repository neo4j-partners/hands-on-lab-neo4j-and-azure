# Dev Containers & Codespaces Quick Start Guide

> **Note:** The Codespace/Dev Container prepopulates the `.env` file in the project root with Neo4j connection settings. Review these values to ensure they are accurate for your environment. If running outside of a Codespace or Dev Container, you must manually set the Neo4j environment variables (`NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`) in your `.env` file.

### Setup Steps

1. **Click the badge above** (or go to repo → Code → Codespaces → New)

2. **Wait for container to build** (~3 minutes)

3. **Run in terminal:**
   ```bash
   # Authenticate with Azure
   az login --use-device-code
   azd auth login --use-device-code

   # Select Azure region and initialize environment
   ./scripts/setup_azure.sh

   # Deploy
   azd up
   ```

   > **Note:** The setup script clears the `.azure/` directory and Azure-related settings from `.env` to ensure a fresh deployment. Neo4j settings in `.env` are preserved. See [docs/AZ_CLI_GUIDE.md](docs/AZ_CLI_GUIDE.md) for details.

   > **Note:** If you encounter a `RoleAssignmentExists` error on redeployment, run `azd env set SKIP_ROLE_ASSIGNMENTS true` and then `azd up` again.

4. **Follow the prompts:**
   ```
   ? Enter a unique environment name: mydev
   ? Select an Azure Subscription: 1. Your Subscription
   ? Pick a resource group to use:
     1. Create a new resource group
   > 2. your-existing-resource-group
   ```
   - **Environment name:** Any word (e.g., `mydev`, `workshop`)
   - **Resource group:** Workshop participants should select the resource group mentioned above. 

6. **Login to the Microsoft Foundry Portal:**

link to ai.azure.com

6. **Update Model Token Limits:**

   This creates an Microsoft Foundry project with two model deployments: **gpt-4o** (for chat completions) and **text-embedding-ada-002** (for vector embeddings). Open [ai.azure.com](https://ai.azure.com/) in the same browser where you're logged into Azure to view your project.

   Click **Models** in the left sidebar to see your deployments:

   ![Models Section](images/models_section.png)

   Click on each model and update the **Tokens per Minute Rate Limit** to increase throughput for the workshop:

   ![Token Limits](images/token_limits.png)

   See [docs/FOUNDRY_GUIDE.md](docs/FOUNDRY_GUIDE.md) for more details.

7. **Restore Neo4j database :**
   Populate the database with the sample data:
   ```bash
   uv run scripts/restore_neo4j.py
   ```

8. **Setup environment:**
   ```bash
   uv run setup_env.py
   ```

9. Move on to Lab 3 - Explore the Data: [Lab_3_Explore_Data/README.md](Lab_3_Explore_Data/README.md)