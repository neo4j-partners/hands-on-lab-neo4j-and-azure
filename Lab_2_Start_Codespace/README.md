# Lab 2 - Start Codespace

In this lab, you will spin up a GitHub Codespace instance to use as your development environment for the rest of the workshop.

## Prerequisites

Before starting, make sure you have:
- Your **Azure Resource Group name** from Lab 0
- Your **Neo4j Aura credentials** (URI, username, password) from Lab 1

## Launch the Codespace

Click the buttons below to start your development environment:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/neo4j-partners/hands-on-lab-neo4j-and-azure)

## What is a GitHub Codespace?

A GitHub Codespace is a cloud-hosted development environment that runs in your browser. When you launch a Codespace, GitHub provisions a virtual machine with:

- A pre-configured VS Code editor
- All required tools and dependencies already installed (Python, Azure CLI, GitHub CLI)
- Extensions for Azure development, Python, and Jupyter notebooks
- A terminal with access to run commands

This means you don't need to install anything on your local machine—everything is ready to go in the cloud.

## Setup

Once your Codespace has started, you will be prompted to enter your secrets (Resource Group name, Neo4j credentials). After that, run the setup commands provided in the terminal to configure the Azure infrastructure for the remaining labs.

## Viewing Your Azure AI Foundry Project

After running the `azd up` commands in the codespace, it created an Azure AI Foundry project for you.

To view your Foundry project:

1. Go to https://ai.azure.com/

   ![Foundry Home Page](images/Foundry_Home_Page.png)

2. The deployment created two models:
   - **gpt-4o-mini** - for text generation
   - **text-embedding-ada-002** - for creating embeddings

   ![Foundry Models](images/Foundry_Models.png)

## Running the Notebooks

To run the Jupyter notebooks in the labs, you need to select the correct Python kernel:

1. Click **Select Kernel** in the top right of the notebook, then select **Python Environments...**

   ![Select Kernel](images/select%20kernel.png)

2. Select the **neo4j-azure-ai-workshop** environment (marked as Recommended)

   ![Select neo4j-azure-ai-workshop](images/neo4j-azure-ai-workshop.png)

## Running Locally (Without a Codespace)

If you prefer to run the workshop on your local machine instead of using a Codespace, you can do so by following the same setup steps outlined in [GUIDE_DEV_CONTAINERS.md](../GUIDE_DEV_CONTAINERS.md).

You will need to:
1. Clone the repository to your local machine
2. Ensure you have the required tools installed (Python, Azure CLI, `uv`, etc.)
3. Follow the setup steps in the guide to authenticate with Azure and deploy the infrastructure
