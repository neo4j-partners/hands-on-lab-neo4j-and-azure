# Aura Agent Integration

The Aura Agent was created via the Aura Console with AI-generated tools grounded in the SEC 10-K knowledge graph. This document describes two ways to interact with it programmatically.

## Agent Tools

The agent has 11 tools configured:

| # | Tool | Type | Description |
|---|------|------|-------------|
| 1 | Company Details | Cypher Template | Company name, ticker, sector, CIK |
| 2 | Company Risk Factors | Cypher Template | Risk factors from 10-K filings |
| 3 | Companies Owned by Asset Manager | Cypher Template | Asset manager holdings and shares |
| 4 | Company Financial Metrics | Cypher Template | Financial KPIs and reporting periods |
| 5 | Company Products Offered | Cypher Template | Products and services by company |
| 6 | Documents by Company Identifier | Cypher Template | Source documents linked to companies |
| 7 | Company Executives | Cypher Template | Executives and board members |
| 8 | Company Partners | Cypher Template | Partnership relationships |
| 9 | Company Competitors | Cypher Template | Competitive landscape |
| 10 | Search Chunks | Similarity Search | Semantic vector search over document chunks |
| 11 | Natural Language to Cypher | Text2Cypher | Ad-hoc Cypher query generation |

## Environment Variables

All configuration lives in `financial_data_load/.env`:

```
AURA_AGENT_ENDPOINT=https://api.neo4j.io/v2beta1/organizations/.../agents/.../invoke
AURA_AGENT_CLIENT_ID=<your client id>
AURA_AGENT_CLIENT_SECRET=<your client secret>
AURA_AGENT_MCP_SERVER="https://mcp.neo4j.io/agent?project_id=...&agent_id=..."
```

URLs containing `&` must be quoted for `source` compatibility.

---

## Option 1: MCP Server (Claude Code Integration)

**Status:** Configuration complete (`.mcp.json`, `MCP.md`)

Connect the Aura Agent as a remote MCP server so Claude Code can call the agent's tools directly.

### How it works

```
User asks Claude Code a question
    → Claude Code sees the Aura Agent MCP tools
    → Sends the query to the Aura Agent MCP endpoint
    → Aura Agent selects the right tool (Cypher Template, Similarity Search, Text2Cypher)
    → Executes against AuraDB
    → Returns results to Claude Code
    → Claude Code answers using the results
```

### Setup

1. Export env vars: `set -a && source financial_data_load/.env && set +a`
2. Start Claude Code from the repo root: `claude`
3. Run `/mcp` to verify the server and authenticate via browser (Aura Console credentials)
4. Ask questions — Claude Code routes them through the agent automatically

### Files

| File | Purpose |
|------|---------|
| `.mcp.json` | Project-scoped MCP server config (gitignored) |
| `MCP.md` | Setup documentation, tool reference, troubleshooting |

### Limitations

- Requires browser-based OAuth (not headless)
- Agent runs in GCP `europe-west1` regardless of instance location
- Read-only queries only
- $0.35/hour when agent is set to External

---

## Option 2: Standalone Python REST Client

**Status:** Not yet built

A standalone Python program that authenticates with the Aura API and sends queries to the agent's REST endpoint. Runs independently of Claude Code.

### How it works

```
Python program
    → POST https://api.neo4j.io/oauth/token (client_credentials grant)
    → Receives bearer token (valid 1 hour)
    → POST <agent endpoint>/invoke with {"input": "question"}
    → Agent selects tool, executes against AuraDB
    → Returns JSON response with thinking, tool calls, results, and answer
    → Program displays the answer
```

### Planned features

- **OAuth token management** — Obtain and cache bearer tokens, auto-refresh on expiry
- **Interactive mode** — Chat loop for conversational queries
- **Batch mode** — Run predefined example queries that exercise each tool
- **Response parsing** — Extract and display thinking steps, tool invocations, and final answer from the structured JSON response
- **Uses same `.env`** — Reads `AURA_AGENT_ENDPOINT`, `AURA_AGENT_CLIENT_ID`, `AURA_AGENT_CLIENT_SECRET`

### Response format

The agent returns structured JSON with content blocks:

```json
{
  "content": [
    {"type": "thinking", "thinking": "Agent reasoning..."},
    {"type": "cypher_template_tool_use", "name": "Company_Details", "input": {"company": "Apple"}},
    {"type": "cypher_template_tool_result", "output": {"records": [...]}},
    {"type": "text", "text": "Apple Inc. (AAPL) is a technology company..."}
  ],
  "status": "SUCCESS",
  "usage": {"total_tokens": 996}
}
```

### Planned files

| File | Purpose |
|------|---------|
| `financial_data_load/aura_agent/main.py` | CLI entry point (interactive + batch modes) |
| `financial_data_load/aura_agent/client.py` | OAuth authentication and REST client |
| `financial_data_load/aura_agent/examples.py` | Predefined queries exercising each tool |

### Example queries per tool

| Tool | Example query |
|------|--------------|
| Company Details | "What is Apple's ticker symbol and CIK number?" |
| Company Risk Factors | "What risk factors does NVIDIA face?" |
| Companies Owned by Asset Manager | "Which companies does Vanguard own?" |
| Company Financial Metrics | "What are Microsoft's reported financial metrics?" |
| Company Products Offered | "What products does Amazon offer?" |
| Documents by Company Identifier | "Show me the source documents for Intel" |
| Company Executives | "Who are the executives at McDonald's?" |
| Company Partners | "What partnerships does PayPal have?" |
| Company Competitors | "Who are Apple's competitors?" |
| Search Chunks | "Tell me about cybersecurity threats in SEC filings" |
| Natural Language to Cypher | "How many companies are in the technology sector?" |
