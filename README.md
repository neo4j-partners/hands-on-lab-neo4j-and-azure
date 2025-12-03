# hands-on-lab-neo4j-and-azure
Neo4j is the [leading graph database](https://db-engines.com/en/ranking/graph+dbms) vendor.  We've worked closely with Microsoft Azure engineering for years.  Our products, AuraDB and AuraDS are offered as managed services on Azure.  Neo4j Aura Professional Edition is offered in the [Azure Marketplace](https://portal.azure.com/#create/neo4j.neo4j_aura_professional).

In this hands-on lab, you'll learn about Neo4j, Microsoft Azure AI Foundry, and the [Microsoft Agent Framework](https://github.com/microsoft/agent-framework). The lab is designed for data scientists, data engineers, and AI developers who want to master GraphRAG (Graph Retrieval-Augmented Generation) techniques and build production-ready agentic AI applications.

In today's landscape, organizations need AI systems that can extract deep insights from unstructured documents, understand complex entity relationships, and build intelligent systems that can autonomously reason over vast information networks. This hands-on lab addresses this need directly by providing mastery in the most powerful pattern available for complex document intelligence: Graph Retrieval-Augmented Generation (GraphRAG).

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
* [Lab 3 - Building a Knowledge Graph](Lab_3_Neo4j_GraphRag) (30 min)
    * Data Loading Fundamentals
    * Embeddings and Vector Search
    * Entity Extraction
    * Loading the Full Dataset
* [Lab 4 - Exploring the Knowledge Graph](Lab_4_Explore_Knowledge_Graph) (15 min)
    * Visual Graph Exploration with Neo4j Explore
    * Graph Data Science Algorithms
* Break (5 min)

### Part 3 - GraphRAG Retrievers
* [Lecture - Microsoft Foundry](https://docs.google.com/presentation/d/1KPHoVJivbinHg-UtrnTIUbMiFHB8mPEnDO0v0OvvcPM/edit?usp=sharing) (15 min)
    * What is Microsoft Foundry?
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

## Windows Setup Guide for VS Code

This guide will help you set up your Windows machine with VS Code to run this project locally.

### Prerequisites

Before starting, ensure you have:
- Windows 10 or Windows 11
- Administrator access on your machine
- An active Azure subscription
- Neo4j Aura credentials (see [Lab 1 - Neo4j Aura Signup](Lab_1_Neo4j_Aura_Signup))

### Step 1: Download the Project

1. Go to https://github.com/neo4j-partners/hands-on-lab-neo4j-and-azure
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file to a location on your computer (e.g., `C:\Projects\hands-on-lab-neo4j-and-azure`)

### Step 2: Install Python 3.12

This project requires Python 3.12 (not 3.13 or later).

1. Download Python 3.12 from https://www.python.org/downloads/
   - Select a **3.12.x** version (e.g., 3.12.7)
   - Do NOT install Python 3.13 or later as this project requires Python 3.12
2. Run the installer:
   - Check "Add Python 3.12 to PATH"
   - Click "Install Now"
   - Note: pip (Python package installer) is included automatically with Python
3. Verify installation:
   ```powershell
   python --version
   ```
   Should output: `Python 3.12.x`
4. Verify pip is installed:
   ```powershell
   pip --version
   ```

### Step 3: Install uv (Python Package Manager)

uv is a fast Python package installer and resolver used by this project.

1. Open PowerShell as Administrator
2. Install uv using pip:
   ```powershell
   pip install uv
   ```
3. Verify installation:
   ```powershell
   uv --version
   ```

### Step 4: Install Azure CLI

The Azure CLI (az) is required for authenticating with Azure and managing resources.

1. Download the Azure CLI installer from https://aka.ms/installazurecliwindows
2. Run the MSI installer and follow the prompts
3. Restart your terminal (close and reopen PowerShell)
4. Verify installation:
   ```powershell
   az --version
   ```
5. Sign in to Azure:
   ```powershell
   az login
   ```
   This will open a browser window for authentication

   **Note:** If you already have Azure CLI installed and are logged in with different credentials, you must log out first and then log in with your workshop credentials:
   ```powershell
   az logout
   az login
   ```
   Verify you're logged in with the correct account:
   ```powershell
   az account show
   ```

### Step 5: Install Azure Developer CLI (azd)

The Azure Developer CLI (azd) simplifies deploying and managing Azure resources.

1. Open PowerShell as Administrator
2. Install azd using the following command:
   ```powershell
   winget install microsoft.azd
   ```
   If `winget` is not available, download the installer from https://aka.ms/azure-dev/install
3. Restart your terminal
4. Verify installation:
   ```powershell
   azd version
   ```
5. Sign in to Azure Developer CLI:
   ```powershell
   azd auth login
   ```

   **Note:** If you already have Azure Developer CLI installed and are logged in with different credentials, log out first and then log in with your workshop credentials:
   ```powershell
   azd auth logout
   azd auth login
   ```

### Step 6: Install Visual Studio Code

1. Download VS Code from https://code.visualstudio.com/
2. Run the installer with default settings
3. Launch VS Code

### Step 7: Install VS Code Extensions

Install the following extensions for an optimal development experience:

1. **Python Extension**
   - Open VS Code
   - Click the Extensions icon (or press `Ctrl+Shift+X`)
   - Search for "Python" by Microsoft
   - Click Install

2. **Jupyter Extension**
   - Search for "Jupyter" by Microsoft
   - Click Install

3. **Azure Account Extension** (optional but recommended)
   - Search for "Azure Account"
   - Click Install

### Step 8: Open the Project in VS Code

1. Open VS Code
2. Click "File" > "Open Folder"
3. Navigate to where you extracted the project (e.g., `C:\Projects\hands-on-lab-neo4j-and-azure`)
4. Click "Select Folder"

### Step 9: Set Up Python Environment

1. Open a terminal in VS Code (`Ctrl+``)
2. Create the Python environment and install dependencies:
   ```powershell
   uv sync
   ```
   This will create a virtual environment and install all required dependencies

3. Select the Python interpreter:
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose the interpreter from `.venv` folder (e.g., `.venv\Scripts\python.exe`)

### Step 10: Configure Environment Variables

1. Copy the sample environment file:
   ```powershell
   copy .env.sample .env
   ```

2. Edit `.env` file and add your Neo4j credentials:
   - Open `.env` in VS Code
   - Fill in the following values:
     ```
     NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
     NEO4J_USERNAME=neo4j
     NEO4J_PASSWORD=your-password-here
     ```

### Step 11: Deploy Azure Infrastructure

1. Initialize the Azure Developer environment:
   ```powershell
   azd env new
   ```
   - Enter an environment name (e.g., "dev")

2. Set your Azure location (must be one of: eastus2, swedencentral, or westus2):
   ```powershell
   azd env set AZURE_LOCATION eastus2
   ```

3. Set your Azure resource group name:
   ```powershell
   azd env set AZURE_RESOURCE_GROUP your-resource-group-name
   ```

4. Deploy the Azure infrastructure:
   ```powershell
   azd up
   ```
   This will provision:
   - Azure AI Foundry project
   - Microsoft Foundry with gpt-4o-mini and text-embedding-ada-002 models
   - Azure Container Registry
   - Azure Monitor and Application Insights

5. Sync Azure configuration to your `.env` file:
   ```powershell
   uv run setup_env.py
   ```

### Step 12: Run the Notebooks

1. In VS Code, navigate to a lab folder (e.g., `Lab_3_Neo4j_GraphRag`)
2. Open a notebook file (e.g., `01_data_loading.ipynb`)
3. When prompted to select a kernel:
   - Click "Select Kernel" in the top right
   - Choose "Python Environments..."
   - Select the "neo4j-azure-ai-workshop" environment (.venv)
4. Run the notebook cells using `Shift+Enter` or the Run button

### Troubleshooting

**Problem: Python version is not 3.12**
- Solution: Uninstall other Python versions and ensure 3.12.x is installed and in your PATH

**Problem: `uv` command not found**
- Solution: Close and reopen your terminal, or add Python Scripts folder to PATH manually

**Problem: Azure CLI authentication fails**
- Solution: Run `az logout` then `az login` again

**Problem: `azd up` fails with region error**
- Solution: Ensure you set AZURE_LOCATION to one of the supported regions (eastus2, swedencentral, westus2)

**Problem: Jupyter kernel not found**
- Solution: Run `uv sync` again and restart VS Code

**Problem: Import errors in notebooks**
- Solution: Ensure you've selected the correct Python interpreter from the `.venv` folder

### Additional Resources

- [Azure CLI Documentation](https://docs.microsoft.com/en-us/cli/azure/)
- [Azure Developer CLI Documentation](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [VS Code Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
