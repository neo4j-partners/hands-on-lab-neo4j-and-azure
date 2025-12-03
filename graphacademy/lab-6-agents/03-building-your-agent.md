# Building Your Agent

## Progressive Enhancement

Building an effective agent follows a progressive pattern:

1. **Start with one tool**: Understand how agents select and use tools
2. **Add semantic search**: Handle content questions
3. **Add database queries**: Handle factual questions

Each step adds capability while keeping the system testable and understandable.

## Tool 1: Schema Introspection

**Purpose**: Let users explore the data structure.

**When the agent uses it**: Questions about what data exists, what entities are available, how things are organized.

**Example questions**:
- "What types of data are in this database?"
- "What relationships exist?"
- "What properties does a Company have?"

**Why start here**: Schema introspection is simple and helps users (and the agent) understand what's possible.

## Tool 2: Semantic Search

**Purpose**: Find content about topics and concepts.

**Based on**: Vector Retriever from Lab 5.

**When the agent uses it**: Content questions, topic exploration, conceptual understanding.

**Example questions**:
- "What is Apple's business strategy?"
- "Tell me about cybersecurity threats"
- "What risks do tech companies face?"

**Docstring guidance**:
```python
def search_content(query: str) -> str:
    """Search for content about topics, concepts, and themes using semantic search.
    Use for questions like 'What is...', 'Tell me about...', 'Explain...'
    Returns relevant text content from documents."""
```

The docstring tells the agent *when* to use this tool.

## Tool 3: Database Queries

**Purpose**: Answer factual questions with precision.

**Based on**: Text2Cypher Retriever from Lab 5.

**When the agent uses it**: Counts, lists, specific lookups, relationship queries.

**Example questions**:
- "How many companies are in the database?"
- "What companies does BlackRock own?"
- "Which company has the most risk factors?"

**Docstring guidance**:
```python
def query_database(query: str) -> str:
    """Query the database for specific facts, counts, lists, and relationships.
    Use for questions like 'How many...', 'List all...', 'Who owns...'
    Returns precise data from the graph."""
```

## How the Agent Chooses

With three tools, the agent matches questions to tool descriptions:

| Question | Agent Reasoning | Tool Selected |
|----------|-----------------|---------------|
| "What data types exist?" | About structure → schema | Schema Tool |
| "What is Apple's strategy?" | Conceptual content → search | Semantic Search |
| "How many companies?" | Counting → database | Database Query |
| "Tell me about AI" | Topic exploration → search | Semantic Search |
| "Who owns Microsoft?" | Specific relationship → database | Database Query |

The agent analyzes question patterns and matches to tool purposes.

## Example Agent Interactions

**Question**: "What types of data are in this database?"

```
Agent thinks: "Asking about data structure"
Agent calls: get_graph_schema()
Agent observes: "Node labels: Company, RiskFactor, Product..."
Agent responds: "The database contains Companies, Risk Factors, Products..."
```

**Question**: "What does Apple say about AI?"

```
Agent thinks: "Asking about content on a topic"
Agent calls: search_content("Apple AI")
Agent observes: Chunks about Apple's AI initiatives
Agent responds: "Apple discusses AI in several contexts..."
```

**Question**: "How many risk factors does Apple face?"

```
Agent thinks: "Asking for a count"
Agent calls: query_database("How many risk factors does Apple face?")
Agent observes: "45"
Agent responds: "Apple faces 45 risk factors."
```

## Testing Your Agent

Test each tool individually first:

**Schema questions**: "What entities exist?", "What relationships are there?"

**Content questions**: "What is [topic]?", "Tell me about [concept]"

**Fact questions**: "How many [entities]?", "Who [relationship] [entity]?"

Verify the agent selects the correct tool for each type.

## Common Issues

**Wrong tool selected**: Improve docstrings to be more specific about when to use each tool.

**Overlapping tools**: Ensure each tool has a distinct, non-overlapping purpose.

**No tool selected**: Make sure at least one tool can handle the question type.

**Poor results**: Check that underlying retrievers work correctly before debugging the agent.

## The Complete Agent

With all three tools, your agent handles:

| Category | Tool | Example Questions |
|----------|------|-------------------|
| Structure | Schema | "What data exists?", "What can I ask about?" |
| Content | Semantic Search | "What is...?", "Tell me about...", "Explain..." |
| Facts | Database Query | "How many...?", "List all...", "Who owns...?" |

This covers the full range of GraphRAG queries.

## Summary

- **Build progressively**: Start with one tool, add more
- **Tool purposes**: Schema (structure), Semantic Search (content), Database Query (facts)
- **Selection via docstrings**: Clear descriptions guide correct tool choice
- **Test incrementally**: Verify each tool before adding more

In the next lesson, you'll learn design patterns for effective multi-tool agents.

---

**Navigation:**
- [← Previous: Microsoft Agent Framework](02-microsoft-agent-framework.md)
- [↑ Back to Lab 6](README.md)
- [Next: Agent Design Patterns →](04-agent-design-patterns.md)
