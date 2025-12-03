# Proposal: Adding Neo4j Aura Agent Lab

## Overview

This proposal outlines a new lab section to add to `Lab_4_Explore_Knowledge_Graph/` that introduces **Neo4j Aura Agent** - a managed platform for building graph-backed AI agents. This lab would bridge the gap between visual exploration (current Lab 4) and programmatic agents (Lab 6), providing a no-code/low-code approach to building GraphRAG agents.

The lab is inspired by the Neo4j blog post: [Build a Context-Aware GraphRAG Agent](https://neo4j.com/blog/genai/build-context-aware-graphrag-agent/)

---

## Why Add This Lab?

### Current Lab Progression Gap

| Lab | Approach | Skill Level |
|-----|----------|-------------|
| Lab 4 (current) | Visual exploration with Neo4j Explore | No-code |
| Lab 5 | GraphRAG retrievers in Python | Code-heavy |
| Lab 6 | Agents with Microsoft Agent Framework | Advanced coding |

**Gap Identified:** There's a jump from visual exploration (Lab 4) directly to Python-based retrievers (Lab 5). The Aura Agent lab provides an intermediate step using a managed, GUI-based approach to building agents.

### Value Proposition

1. **Accessibility**: Build production-ready agents without extensive Python knowledge
2. **Rapid Prototyping**: Test GraphRAG patterns before implementing in code
3. **Production Path**: Deploy to authenticated API endpoints directly from the console
4. **Transparency**: Tool explanations provide visibility into agent reasoning
5. **Contextual Bridge**: Shows concepts that will be implemented programmatically in Labs 5 & 6

---

## Proposed Lab Structure

### Lab 4.5: Build an Aura Agent for SEC Filings Analysis

**Prerequisites:**
- Completed Lab 0 (Azure sign-in)
- Completed Lab 1 (Neo4j Aura setup)
- Completed Lab 3 (Knowledge graph built with embeddings)

### Step 1: Enable Generative AI Assistance

Navigate to the Neo4j Aura console and enable the Generative AI features:
1. Go to [console.neo4j.io](https://console.neo4j.io)
2. Click on your database instance
3. Navigate to **Aura Agent** in the left sidebar
4. Enable Generative AI assistance if prompted

### Step 2: Create the SEC Filings Agent

Create a new agent with the following configuration:

**Agent Name:** `sec-filings-analyst`

**System Instructions:**
```
You are an expert financial analyst assistant specializing in SEC 10-K filings analysis.
You help users understand:
- Company risk factors and how they compare across companies
- Asset manager ownership patterns and portfolio compositions
- Financial metrics and products mentioned in company filings
- Relationships between companies, their documents, and extracted entities

Always provide specific examples from the knowledge graph when answering questions.
Ground your responses in the actual data from SEC filings.
```

### Step 3: Add Cypher Template Tools

Add pre-defined Cypher query tools for common use cases:

#### Tool 1: Get Company Overview
```cypher
MATCH (c:Company {name: $company_name})
OPTIONAL MATCH (c)-[:FILED]->(d:Document)
OPTIONAL MATCH (c)-[:FACES_RISK]->(r:RiskFactor)
OPTIONAL MATCH (am:AssetManager)-[:OWNS]->(c)
WITH c, d,
     collect(DISTINCT r.name)[0..10] AS risks,
     collect(DISTINCT am.managerName)[0..10] AS owners
RETURN
    c.name AS company,
    c.ticker AS ticker,
    d.path AS filing_path,
    risks AS top_risk_factors,
    owners AS major_asset_managers
```

**Tool Name:** `get_company_overview`
**Description:** Get comprehensive overview of a company including their SEC filing, risk factors, and major institutional owners.
**Parameters:** `company_name` (string) - The company name to look up (e.g., "APPLE INC", "NVIDIA CORPORATION")

#### Tool 2: Find Shared Risks Between Companies
```cypher
MATCH (c1:Company)-[:FACES_RISK]->(r:RiskFactor)<-[:FACES_RISK]-(c2:Company)
WHERE c1.name = $company1 AND c2.name = $company2
WITH c1, c2, collect(DISTINCT r.name) AS shared_risks
RETURN
    c1.name AS company_1,
    c2.name AS company_2,
    shared_risks,
    size(shared_risks) AS num_shared_risks
```

**Tool Name:** `find_shared_risks`
**Description:** Find risk factors that two companies have in common from their SEC filings.
**Parameters:**
- `company1` (string) - First company name
- `company2` (string) - Second company name

### Step 4: Add Similarity Search Tool

Configure a semantic search tool using the existing vector index:

**Tool Name:** `search_filing_content`
**Description:** Search SEC filing content semantically to find relevant passages about specific topics, risks, or business information.
**Vector Index:** `chunkEmbeddings`
**Return Properties:** `text`
**Top K:** 5

**Retrieval Query (for enhanced context):**
```cypher
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)-[:FILED]-(company:Company)
OPTIONAL MATCH (company)-[:FACES_RISK]->(risk:RiskFactor)
WITH node, score, company, collect(DISTINCT risk.name)[0..10] AS risks
RETURN
    node.text AS content,
    score AS relevance,
    company.name AS source_company,
    risks AS company_risks
ORDER BY score DESC
```

### Step 5: Add Text2Cypher Tool

Enable natural language to Cypher translation:

**Tool Name:** `query_database`
**Description:** Query the SEC filings knowledge graph using natural language. Use this for specific questions about companies, risks, metrics, or ownership that require precise data lookup.

**Custom Prompt:**
```
Task: Generate a Cypher statement to query the SEC 10-K filings knowledge graph.

Instructions:
- Use only the provided node labels and relationship types
- When filtering by name, use case-insensitive matching: WHERE toLower(node.name) CONTAINS toLower('value')
- Always add LIMIT 20 to restrict results
- Use elementId(node) instead of id(node)
- Use explicit grouping with WITH clauses for aggregations

Available Node Labels:
- Company (properties: name, ticker)
- Document (properties: path, name)
- Chunk (properties: text, embedding)
- RiskFactor (properties: name)
- AssetManager (properties: managerName)
- Product (properties: name)
- FinancialMetric (properties: name)
- Executive (properties: name)

Key Relationships:
- (Company)-[:FILED]->(Document)
- (Company)-[:FACES_RISK]->(RiskFactor)
- (AssetManager)-[:OWNS]->(Company)
- (Company)-[:MENTIONS]->(Product)
- (Chunk)-[:FROM_DOCUMENT]->(Document)

Generate only valid Cypher. No explanations.
```

### Step 6: Test the Agent

Test your agent with these sample questions:

**Cypher Template Questions:**
- "Tell me about Apple's SEC filing and their major investors"
- "What risks do Apple and Microsoft share?"

**Semantic Search Questions:**
- "What do the filings say about AI and machine learning?"
- "Find content about supply chain risks"
- "What do companies say about climate change?"

**Text2Cypher Questions:**
- "Which company has the most risk factors?"
- "How many products does NVIDIA mention?"
- "What executives are mentioned by Apple?"

### Step 7: Review Agent Reasoning

After each query, observe:
1. Which tool the agent selected and why
2. The context retrieved from the knowledge graph
3. How the agent synthesized the response
4. Tool explanations showing the reasoning process

### Step 8: (Optional) Deploy to API

Deploy your agent to a production endpoint:
1. Click **Deploy** in the Aura Agent console
2. Copy the authenticated API endpoint
3. Use the endpoint in your applications

---

## Learning Objectives

By completing this lab, participants will:

1. **Understand the three retrieval patterns** used in GraphRAG:
   - Cypher Templates for controlled, precise queries
   - Similarity Search for semantic retrieval
   - Text2Cypher for flexible natural language queries

2. **Learn tool selection principles**: When to use each retrieval approach based on question type

3. **Practice prompt engineering**: Write effective system instructions and tool descriptions

4. **Experience agent transparency**: Understand how agents reason about tool selection

5. **Bridge to programmatic implementation**: Recognize that Lab 5 & 6 implement these same patterns in Python code

---

## Connection to Other Labs

| Aura Agent Tool | Lab 5 Equivalent | Lab 6 Equivalent |
|-----------------|------------------|------------------|
| Similarity Search | VectorRetriever (01) | `retrieve_financial_documents` tool |
| Similarity Search + Cypher | VectorCypherRetriever (02) | Vector+Graph Agent (02) |
| Text2Cypher | Text2CypherRetriever (03) | `query_database` tool (03) |
| Cypher Templates | N/A (custom) | `get_graph_schema` tool |

---

## Sample Agent Conversation

**User:** What risks do Apple and Microsoft share, and what does Apple say about supply chain risks in their filing?

**Agent Reasoning:**
1. First, I'll use `find_shared_risks` to compare Apple and Microsoft's risk factors
2. Then, I'll use `search_filing_content` to find relevant passages about Apple's supply chain risks
3. Finally, I'll synthesize the findings

**Agent Response:**
Based on the SEC filings, Apple and Microsoft share several common risk factors:

**Shared Risk Factors:**
- Supply chain disruptions
- Foreign exchange rate fluctuations
- Interest rate risk
- Macroeconomic conditions
- Climate change impacts

**Apple's Supply Chain Commentary:**
From Apple's 10-K filing, the company discusses significant supply chain concerns including reliance on single-source suppliers, geopolitical risks affecting manufacturing partners, and the potential for component shortages to impact product availability and margins.

*[Tool calls: find_shared_risks (APPLE INC, MICROSOFT CORP), search_filing_content ("Apple supply chain risks")]*

---

## Implementation Considerations

### Prerequisites for Aura Agent
- Neo4j Aura Enterprise or Professional tier
- Generative AI add-on enabled
- Knowledge graph with vector embeddings (from Lab 3)

### Estimated Time
- Lab completion: 30-45 minutes
- Includes testing and experimentation

### Potential Challenges
1. Aura Agent availability (may require enterprise tier)
2. Rate limits on Generative AI features
3. Vector index naming must match (`chunkEmbeddings`)

---

## Alternative: Simulated Aura Agent with Screenshots

If Aura Agent is not available to all participants, create a walkthrough version:
1. Document the setup process with screenshots
2. Show example conversations and tool selections
3. Provide "what would happen" explanations
4. Use as conceptual introduction before Lab 5

---

## File Structure Proposal

```
Lab_4_Explore_Knowledge_Graph/
├── README.md                        # Current visual exploration lab
├── AURA_AGENT_README.md            # New: Aura Agent lab instructions
├── images/
│   ├── ... (existing images)
│   ├── aura_agent_create.png       # Agent creation screen
│   ├── aura_agent_tools.png        # Tool configuration
│   ├── aura_agent_test.png         # Testing interface
│   └── aura_agent_reasoning.png    # Tool selection reasoning
└── cypher_templates/
    ├── get_company_overview.cypher
    └── find_shared_risks.cypher
```

---

## Future Tools

These additional Cypher template tools can be added to extend the agent's capabilities:

### Get Asset Manager Portfolio
```cypher
MATCH (am:AssetManager {managerName: $manager_name})-[o:OWNS]->(c:Company)
OPTIONAL MATCH (c)-[:FACES_RISK]->(r:RiskFactor)
WITH am, c, o, collect(DISTINCT r.name)[0..5] AS company_risks
RETURN
    am.managerName AS asset_manager,
    collect({
        company: c.name,
        ticker: c.ticker,
        position_status: o.position_status,
        key_risks: company_risks
    }) AS portfolio
```

**Tool Name:** `get_manager_portfolio`
**Description:** Get all companies owned by a specific asset manager and their associated risk factors.
**Parameters:** `manager_name` (string) - The asset manager name (e.g., "BlackRock Inc.", "Berkshire Hathaway Inc")

### List All Companies
```cypher
MATCH (c:Company)
OPTIONAL MATCH (c)-[:FACES_RISK]->(r:RiskFactor)
WITH c, count(r) AS risk_count
RETURN c.name AS company, c.ticker AS ticker, risk_count
ORDER BY risk_count DESC
LIMIT 20
```

**Tool Name:** `list_companies`
**Description:** List all companies in the knowledge graph with their risk factor counts.
**Parameters:** None

---

## Conclusion

Adding the Aura Agent lab to Lab 4 provides:

1. **Progressive complexity**: No-code → Low-code (Aura Agent) → Full code (Labs 5 & 6)
2. **Conceptual foundation**: Introduces retrieval patterns before programming them
3. **Production relevance**: Shows a real deployment path for GraphRAG agents
4. **Hands-on experience**: Interactive agent building without Python
5. **Perfect bridge**: Prepares participants for understanding the programmatic implementations

The lab leverages the existing SEC 10-K knowledge graph and demonstrates the same three retrieval patterns (Vector, VectorCypher, Text2Cypher) that participants will implement in Python during Labs 5 and 6.
