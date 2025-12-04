---
marp: true
theme: default
paginate: true
---

<style>
section {
  --marp-auto-scaling-code: false;
}

li {
  opacity: 1 !important;
  animation: none !important;
  visibility: visible !important;
}

/* Disable all fragment animations */
.marp-fragment {
  opacity: 1 !important;
  visibility: visible !important;
}

ul > li,
ol > li {
  opacity: 1 !important;
}
</style>


# Neo4j Aura Agents

Building GraphRAG Applications Without Code

---

## What Are Aura Agents?

Aura Agents is a **no-code platform** for building AI agents grounded in your Neo4j graph data.

**Key Capabilities:**
- Build agents directly in the Aura Console
- Configure retrieval tools without writing code
- Test in an integrated chat playground
- Deploy to production via API
---

## The Three-Tool Architecture

Aura Agents combine three complementary retrieval methods:

| Tool | Purpose | Best For |
|------|---------|----------|
| **Cypher Templates** | Precise, parameterized queries | Known question patterns |
| **Similarity Search** | Semantic vector search | Finding relevant content |
| **Text2Cypher** | Natural language to Cypher | Ad-hoc exploration |

The agent **automatically selects** the right tool for each question.

---

## Tool 1: Cypher Templates

Pre-defined queries with parameters for common questions.

**Example:** Company Overview Tool
```cypher
MATCH (c:Company {name: $company_name})
OPTIONAL MATCH (c)-[:FILED]->(d:Document)
OPTIONAL MATCH (c)-[:FACES_RISK]->(r:RiskFactor)
RETURN c.name AS company,
       collect(DISTINCT r.name)[0..10] AS risks
```

**User asks:** "Tell me about Apple's risks"
**Agent:** Extracts "APPLE INC", executes template, returns structured answer

---

## Tool 2: Similarity Search

Semantic search using vector embeddings stored in Neo4j.

**How It Works:**
1. User question is embedded into a vector
2. Vector index finds similar content
3. Retrieval query enriches with graph context
4. Agent synthesizes the response

**Example Question:** "What do companies say about AI and machine learning?"

Returns semantically relevant passages with company context.

---

## Tool 3: Text2Cypher

Converts natural language to Cypher queries dynamically.

**How It Works:**
1. User asks a question in plain English
2. LLM generates appropriate Cypher query
3. Query executes against the database
4. Results are returned to the agent

**Example:** "Which company has the most risk factors?"

```cypher
MATCH (c:Company)-[:FACES_RISK]->(r:RiskFactor)
RETURN c.name, count(r) AS risk_count
ORDER BY risk_count DESC LIMIT 1
```

---

## Why Graph Context Matters

Traditional RAG retrieves text chunks. GraphRAG retrieves **connected knowledge**.

**Vector-Only RAG:**
- "Find documents about cybersecurity risks"
- Returns: text chunks mentioning cybersecurity

**GraphRAG with Aura Agents:**
- "Which asset managers own companies facing cybersecurity risks?"
- Returns: traverses OWNS and FACES_RISK relationships

**Graphs enable questions that pure vector search cannot answer.**

---

## Creating an Aura Agent

Building an agent takes minutes:

1. **Define the agent** - Name, description, system instructions
2. **Select your database** - Connect to your AuraDB instance
3. **Add tools** - Configure Cypher templates, similarity search, Text2Cypher
4. **Test in playground** - Interact with your agent
5. **Deploy** - Get an authenticated API endpoint

No coding required - just configuration.

---

## Agent Configuration Example

**Agent Name:** SEC Filings Analyst

**System Instructions:**
```
You are an expert financial analyst specializing in
SEC 10-K filings analysis. You help users understand:
- Company risk factors and comparisons
- Asset manager ownership patterns
- Financial metrics and products
- Relationships between entities

Ground your responses in actual data from SEC filings.
```

---

## Testing Your Agent

The Aura Console provides an integrated chat playground:

**Cypher Template Test:**
> "What risks do Apple and Microsoft share?"
- Agent selects `find_shared_risks` template
- Executes with company parameters
- Returns comparison results

**Semantic Search Test:**
> "What do filings say about supply chain?"
- Agent uses similarity search tool
- Finds relevant passages across companies
- Synthesizes insights

---

## Tool Selection in Action

The agent reasons about which tool to use:

| Question | Tool Selected | Why |
|----------|--------------|-----|
| "Tell me about NVIDIA" | Cypher Template | Matches known pattern |
| "Find content about climate" | Similarity Search | Semantic search needed |
| "How many products total?" | Text2Cypher | Aggregation query |
| "Compare Apple and Google risks" | Cypher Template | Two-company comparison |

**The agent explains its reasoning** in each response.

---

## Deployment Options

**Internal Testing:**
- Share with team members in Aura Console
- Test different configurations

**Production API:**
- Deploy to authenticated REST endpoint
- Client credentials from user profile
- Integrate into your applications

**Coming Soon:**
- MCP (Model Context Protocol) support
- Additional integration protocols

---

## From No-Code to Code

Aura Agents demonstrates the same patterns you'll implement programmatically:

| Aura Agent Tool | Python Implementation |
|-----------------|----------------------|
| Cypher Template | Parameterized queries |
| Similarity Search | VectorCypherRetriever |
| Text2Cypher | Text2CypherRetriever |
| Agent orchestration | Microsoft Agent Framework |

**Labs 5 and 6** implement these patterns in Python.

---

## The Value of Aura Agents

**For Prototyping:**
- Validate GraphRAG approach quickly
- Test retrieval strategies without code
- Iterate on prompts and tools

**For Production:**
- Deploy agents in minutes
- Secure, authenticated endpoints
- Scalable infrastructure
---

## Summary

Aura Agents provide:

- **No-code GraphRAG** - Build agents without programming
- **Three retrieval tools** - Cypher templates, similarity search, Text2Cypher
- **Intelligent orchestration** - Automatic tool selection
- **Easy deployment** - Test in playground, deploy to API

**The fastest path from knowledge graph to AI agent.**

---

## Next Steps

1. **Create your Aura instance** (if not done already)
2. **Build the knowledge graph** (Labs 2-3)
3. **Create an Aura Agent** using the console
4. **Test with sample questions**
5. **Continue to Python implementation** (Labs 5-6)

