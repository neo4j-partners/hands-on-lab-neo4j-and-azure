# Dev Containers & Codespaces Quick Start Guide

> If you are running locally instead of using a Codespace, see [Quick Start: Open in a Local Dev Container](#quick-start-open-in-a-local-dev-container) below.

## Quick Start: GitHub Codespaces

> **Warning:** It may take several minutes for the Codespace to start. After it starts, please wait a couple of minutes for all post-install scripts to finish running.

### Setup Steps

1. **Authenticate with Azure:**
   ```bash
   az login --use-device-code
   ```

2. **Configure CONFIG.txt:**

   Edit the `CONFIG.txt` file in the project root and fill in your values:

   - Add your **Neo4j credentials** from Lab 1 (`NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`)
   - Add your **Azure AI Foundry project endpoint** from Lab 3 (`AZURE_AI_PROJECT_ENDPOINT`)

   > **Note:** Set `AZURE_AI_MODEL_NAME` to whichever model you deployed in Lab 3 (`gpt-4o-mini` or `gpt-4o`).

3. Move on to Lab 5 - Foundry Agents: [Lab_5_Foundry_Agents/README.md](Lab_5_Foundry_Agents/README.md)

---

## Alternative Local Quick Start: Open in a Local Dev Container

If you have Docker and VS Code installed locally, you can run the workshop in an isolated container volume without using a Codespace:

1. Install [Docker](https://www.docker.com/get-started/) and ensure it is running
2. Install [VS Code](https://code.visualstudio.com/) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Open VS Code and run **Dev Containers: Clone Repository in Container Volume...** from the Command Palette (`F1`)
4. Enter `neo4j-partners/neo4j-and-azure-lab` and press Enter
5. VS Code will reload, clone the repo, and build the dev container — this may take several minutes
6. Once the build completes, continue with the [Setup Steps](#setup-steps) above

For more details, see the [VS Code Dev Containers documentation](https://code.visualstudio.com/docs/devcontainers/containers#_quick-start-open-a-git-repository-or-github-pr-in-an-isolated-container-volume).
