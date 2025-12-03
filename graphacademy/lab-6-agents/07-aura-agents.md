# Aura Agents

## No-code Agents

The approach used so far in this module has involved writing code to create agents using Python and LangChain.

**Neo4j Aura** also provides a **no-code interface** to create agents that demonstrate GraphRAG through **Aura Agents**.

## What are Aura Agents?

The key features of Aura Agents are:

* **No-code creation** - Build agents through a web interface
* **GraphRAG integration** - Leverage your knowledge graph structure
* **Multiple tool types** - Combine different query approaches
* **API accessibility** - Make agents available via REST endpoints

## Creating an Agent

To create an agent, select **Agents** from the left hand menu and click **Create**.

You can configure your agent with a:

* **Name** - A clear, descriptive name for the agent
* **Description** - A brief explanation of the agent's purpose
* **Prompt Instructions** - Instructions passed to the LLM to provide context for the agent and how it should behave
* **Target instance** - The Neo4j Aura instance that the agent will connect to
* **Visibility** - The agent can be made available internally for members of the Aura project, or available externally via an API endpoint.

**Setting up our EDGAR SEC Filings agent:**

* **Name:** `EDGAR SEC Filings Agent`

* **Description:**

```
An agent that can answer questions about the EDGAR SEC filings.
```

* **Prompt Instructions:**

```
You are an expert in the EDGAR SEC filings. You have access to a graph database containing information about companies, executives, financial metrics, and business risks extracted from the EDGAR SEC filings.
```

* **Target instance:** _Select Your instance_

* **Visibility:** `Internal`

## Agent Tool Types

Aura Agents support three different tool types:

* **Similarity Search Tools** - Vector-based semantic search
* **Cypher Template Tools** - Predefined queries with parameters
* **Text-to-Cypher Tools** - Natural language to Cypher translation

These tools are used to provide an LLM with the context required to perform the task at hand.

## Similarity Search Tools

**Purpose:** Find semantically similar content using vector embeddings.

**Best for:**

* Document search
* Content discovery
* Finding similar clauses or terms
* Semantic matching

**Example Query:** "What are the risks that Apple faces?"

**Configuration:**

* **Name:** `Risk Finder`
* **Description:** `Find companies that face a type of risk.`
* **Embedding Provider:** `OpenAI`
* **Embedding Model:** `text-embedding-ada-002`
* **Index:** `chunkEmbeddings`
* **Top K:** `10`

## Cypher Template Tools

**Purpose:** Execute predefined Cypher queries with user-provided parameters.

**Best for:**

* Common, repeated questions
* Deterministic results with consistent performance
* Complex queries using full Cypher feature set
* Well-defined business logic patterns

**Connection to Code:** These tools implement the same pattern as direct Cypher queries you've written, but packaged for reuse by the agent.

**Example Query:** "What companies are owned by **BlackRock Inc.**?"

**Configuration:**

* **Name:** `Get holdings for Asset Manager`
* **Description:** `Find all companies owned by a asset manager by their name.`
* **Parameters:**
  * `asset_manager`, a string - `The full name of the asset manager.`
* **Cypher Template:**

```cypher
MATCH (owner:AssetManager {managerName: $asset_manager})
RETURN owner.managerName AS managerName,
    [ (owner)-[:OWNS]->(company) | company.name] AS owned_companies
```

## Text-to-Cypher Tools

**Purpose:** Convert natural language questions into Cypher queries dynamically.

**Best for:**

* Catch-all for unforseen questions
* Well-defined questions that map directly to the schema
* Ad-hoc analysis
* Questions you haven't created templates for

**Example Queries:**

"Which documents mention the metric 'net loss'?"
"List the asset managers in ascending order of the number of companies they own shares in."

**Configuration:**

* **Name:** `Catch-all data tool`
* **Description:**

```
A tool that can answer any question about the graph that cannot be specifically answered by the other tools.
```

## Testing the agent

Clicking an agent in the left hand pane will reveal a chat interface that you can use to test the agent.

You can test the tools in sequence.

1. `List the top 5 asset managers by name in ascending order.` - Text-to-Cypher tool
2. `Which companies does "ALLIANCEBERNSTEIN L.P." hold shares in?` - Cypher Template tool
3. `What are the risks that Apple faces?` - Similarity Search tool

The agent will choose the best tool for each question.

The UI will display the time taken to generate each response.

Expand the **Thought for...** section to view the steps and tool calls taken to generate the answer.

## Example Agents

You can [find example agents in the Neo4j Aura Agents GitHub repository on GitHub](https://github.com/neo4j-product-examples/knowledge-graph-agent).

* [Legal - Contract Review Agent](https://github.com/neo4j-product-examples/knowledge-graph-agent/blob/main/contract-review.md)
* [Financial Services - Know Your Customer Agent](https://github.com/neo4j-product-examples/knowledge-graph-agent/blob/main/know-your-customer.md)

## Continue

Why not experiment yourself by creating your own Aura Agent using your own Neo4j Aura instance?

You can [learn more about getting started with Neo4j Aura in our Aura Fundamentals course](/courses/aura-fundamentals/).

## Summary

In this lesson, you learned about Neo4j Aura Agents and how to create no-code agents for your knowledge graph:

**Key Concepts:**

* **Aura Agents** are a no-code interface for creating GraphRAG-powered chatbots

**Tool Types:**

* **Cypher Template Tools** - Execute predefined queries for known patterns and specific lookups
* **Text-to-Cypher Tools** - Convert natural language to Cypher for flexible exploration
* **Similarity Search Tools** - Use vector embeddings for semantic content discovery

**Example Agents:**
* [Legal - Contract Review Agent](https://github.com/neo4j-product-examples/knowledge-graph-agent/blob/main/contract-review.md)
* [Financial Services - Know Your Customer Agent](https://github.com/neo4j-product-examples/knowledge-graph-agent/blob/main/know-your-customer.md)

---

**Navigation:**
- [← Previous: Multi-Tool Agent Design](06-multi-tool-design.md)
- [↑ Back to Module 3](README.md)
- [Next: Best Practices →](08-best-practices.md)
