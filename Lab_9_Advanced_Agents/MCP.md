# Aura Agent MCP Server Setup

Connect the Neo4j Aura Agent directly to Claude Code as a remote MCP server. This gives Claude Code access to all 11 agent tools (Cypher Templates, Similarity Search, Text2Cypher) configured on the Aura Agent.

## Prerequisites

- A deployed Neo4j Aura Agent with **External** access and **MCP server** enabled
- The MCP server endpoint URL (copied from the Aura Console)
- An Aura Console account (for OAuth authentication)

## 1. Set the environment variable

Claude Code resolves `${VAR}` references in `.mcp.json` from your **shell environment** (it does not load `.env` files automatically).

Export the MCP server URL before launching Claude Code:

```bash
export AURA_AGENT_MCP_SERVER="https://mcp.neo4j.io/agent?project_id=YOUR_PROJECT_ID&agent_id=YOUR_AGENT_ID"
```

To persist this, add the export to your shell profile (`~/.zshrc` or `~/.bashrc`), or source the `.env` file before starting Claude Code:

```bash
cd financial_data_load
set -a && source .env && set +a
cd ..
claude
```

## 2. Verify the `.mcp.json` configuration

The repo root contains `.mcp.json` which configures the Aura Agent as a remote MCP server:

```json
{
  "mcpServers": {
    "neo4j-aura-agent": {
      "type": "http",
      "url": "${AURA_AGENT_MCP_SERVER}"
    }
  }
}
```

This is project-scoped — it only applies when Claude Code is run from this repository.

## 3. Authenticate

The first time the MCP server is invoked, Claude Code will open a browser window for Aura OAuth authentication. Log in with the same credentials you use for the [Aura Console](https://console.neo4j.io).

Tokens are stored securely and refreshed automatically. To re-authenticate or check status:

```
/mcp
```

## 4. Use it

Once connected, Claude Code has access to the Aura Agent's tools. Ask questions about the knowledge graph:

- "What products does Apple offer?"
- "Show me risk factors for technology companies"
- "Which asset managers own Microsoft?"
- "What are NVIDIA's main competitors?"
- "Find documents related to Intel"

Claude Code will route queries through the Aura Agent, which selects the appropriate tool (Cypher Template, Similarity Search, or Text2Cypher) automatically.

## Available Agent Tools

| Tool | Type | Description |
|------|------|-------------|
| Company Details | Cypher Template | Look up company information (name, ticker, sector) |
| Company Risk Factors | Cypher Template | Risk factors disclosed in 10-K filings |
| Companies Owned by Asset Manager | Cypher Template | Asset manager holdings and share counts |
| Company Financial Metrics | Cypher Template | Financial KPIs and metrics |
| Company Products Offered | Cypher Template | Products and services by company |
| Documents by Company Identifier | Cypher Template | Source documents linked to companies |
| Company Executives | Cypher Template | Executives and board members |
| Company Partners | Cypher Template | Partnership relationships |
| Company Competitors | Cypher Template | Competitive landscape |
| Search Chunks | Similarity Search | Semantic vector search over document chunks |
| Natural Language to Cypher | Text2Cypher | Ad-hoc Cypher query generation |

## Troubleshooting

**MCP server not appearing:** Verify the env var is set in your shell (`echo $AURA_AGENT_MCP_SERVER`). Claude Code does not read `.env` files.

**Authentication fails:** Run `/mcp` in Claude Code to check server status and re-authenticate. Ensure you can log in to [console.neo4j.io](https://console.neo4j.io).

**Agent not responding:** Check that the agent is set to **External** and not paused in the Aura Console. External agents cost $0.35/hour when active.
