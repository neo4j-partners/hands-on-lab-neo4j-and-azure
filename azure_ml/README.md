# Running Lab 5 GraphRAG Retrievers in Azure ML Studio

This guide explains how to set up and run the Lab 5 GraphRAG Retrievers notebooks in Azure ML Studio Notebooks.

## Prerequisites

Before starting, ensure you have:

1. **Azure Subscription** with access to Azure Machine Learning
2. **Completed Labs 0-3** (Neo4j Aura setup, environment configuration, knowledge graph built)
3. **Neo4j Aura credentials** (URI, username, password)
4. **Azure AI Project** deployed via `azd up` (provides OpenAI endpoint)

## Quick Start

### Option 1: Manual Upload

1. Navigate to [Azure ML Studio](https://ml.azure.com)
2. Create or select your workspace
3. Go to **Notebooks** in the left navigation
4. Upload the notebooks from `Lab_5_GraphRAG_Retrievers/`
5. Follow the setup steps below

### Option 2: Using the Setup Script

```bash
# From this directory
python upload_notebooks.py --workspace <your-workspace-name> --resource-group <your-rg>
```

## Detailed Setup Instructions

### Step 1: Create an Azure ML Workspace (if needed)

If you don't have an Azure ML workspace:

1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "Machine Learning"
3. Click **+ Create**
4. Fill in:
   - **Subscription**: Your subscription
   - **Resource group**: Same as your lab resources (or create new)
   - **Workspace name**: e.g., `neo4j-graphrag-workshop`
   - **Region**: Same region as your Azure AI resources
5. Click **Review + Create** then **Create**

### Step 2: Create a Compute Instance

1. In Azure ML Studio, go to **Compute** > **Compute instances**
2. Click **+ New**
3. Configure:
   - **Compute name**: e.g., `graphrag-compute`
   - **Virtual machine type**: CPU
   - **Virtual machine size**: `Standard_DS3_v2` (recommended) or larger
4. Click **Create**
5. Wait for the compute instance to start (3-5 minutes)

### Step 3: Upload Lab Notebooks

1. In Azure ML Studio, go to **Notebooks**
2. Click **Upload files** or **Upload folder**
3. Upload the contents of `Lab_5_GraphRAG_Retrievers/`:
   - `01_vector_retriever.ipynb`
   - `02_vector_cypher_retriever.ipynb`
   - `03_text2cypher_retriever.ipynb`
4. Also upload the required support files:
   - `new-workshops/solutions/config.py`

### Step 4: Install Dependencies

Open a terminal in Azure ML Studio (or use the first cell of any notebook):

```python
%pip install neo4j neo4j-graphrag azure-identity python-dotenv pydantic-settings
```

### Step 5: Configure Environment Variables

Create a `.env` file in your notebook directory with:

```bash
# Neo4j Aura Connection
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

# Azure AI Configuration
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project-id
AZURE_AI_MODEL_NAME=gpt-4o-mini
AZURE_AI_EMBEDDING_NAME=text-embedding-ada-002
```

**To get your Azure AI endpoint**, run:
```bash
azd env get-values | grep AZURE_AI_PROJECT_ENDPOINT
```

### Step 6: Configure Azure Authentication

Azure ML compute instances have managed identity. Modify the `config.py` to use it:

```python
from azure.identity import ManagedIdentityCredential, ChainedTokenCredential, AzureCliCredential

def _get_azure_token() -> str:
    """Get Azure token - works in Azure ML with managed identity."""
    scope = "https://cognitiveservices.azure.com/.default"

    # Chain: try managed identity first, then CLI
    credential = ChainedTokenCredential(
        ManagedIdentityCredential(),
        AzureCliCredential()
    )
    token = credential.get_token(scope)
    return token.token
```

### Step 7: Grant Managed Identity Access

The compute instance's managed identity needs access to your Azure AI services:

1. In Azure Portal, go to your Azure AI Services resource
2. Go to **Access control (IAM)**
3. Click **+ Add** > **Add role assignment**
4. Select role: **Cognitive Services User**
5. Assign to: **Managed identity**
6. Select your compute instance's managed identity
7. Click **Review + assign**

### Step 8: Run the Notebooks

1. Open `01_vector_retriever.ipynb`
2. Select your compute instance as the kernel
3. Run cells sequentially
4. Proceed to notebooks 02 and 03

## Alternative: Using User-Assigned Managed Identity

For production scenarios, use a user-assigned managed identity:

1. Create a user-assigned managed identity in Azure Portal
2. Assign it to your compute instance
3. Grant it **Cognitive Services User** role on your Azure AI resource
4. Update `config.py` to use the specific client ID:

```python
from azure.identity import ManagedIdentityCredential

credential = ManagedIdentityCredential(client_id="<your-identity-client-id>")
```

## Troubleshooting

### Authentication Errors

**"Azure authentication failed"**
- Ensure your compute instance's managed identity has the correct roles
- Try running `az login` in the terminal if using CLI auth
- Restart the kernel after authentication changes

### Neo4j Connection Errors

**"Unable to connect to Neo4j"**
- Verify your Neo4j Aura instance is running
- Check the URI format: `neo4j+s://` (not `bolt://`)
- Ensure credentials are correct in `.env`

### Missing Modules

**"ModuleNotFoundError"**
```python
%pip install neo4j neo4j-graphrag azure-identity python-dotenv pydantic-settings
```
Then restart the kernel.

### Vector Index Not Found

**"Index 'chunkEmbeddings' not found"**
- Ensure you completed Lab 3 (building the knowledge graph)
- Verify the index exists in Neo4j Browser

## Project Structure for Azure ML

Recommended folder structure in Azure ML:

```
Users/<your-name>/
├── neo4j-graphrag-workshop/
│   ├── .env                          # Environment variables
│   ├── config.py                     # Modified config for Azure ML
│   ├── 01_vector_retriever.ipynb
│   ├── 02_vector_cypher_retriever.ipynb
│   └── 03_text2cypher_retriever.ipynb
```

## Cost Optimization

- **Stop compute when not in use**: Compute instances bill per minute
- **Use Standard_DS3_v2**: Sufficient for these notebooks
- **Consider Spot instances**: For non-production workloads

## Next Steps

After completing the notebooks in Azure ML:

1. Explore the generated Cypher queries
2. Modify retrieval queries for your use cases
3. Consider deploying as managed endpoints
4. Integrate with Azure AI Agent Service

## Additional Resources

- [Azure ML Documentation](https://docs.microsoft.com/azure/machine-learning/)
- [Neo4j GraphRAG Python Package](https://neo4j.com/docs/neo4j-graphrag-python/)
- [Azure AI Services Authentication](https://docs.microsoft.com/azure/ai-services/authentication)
