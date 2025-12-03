# Agent Design Patterns

## Introduction

Building effective agents requires thoughtful design. Tools must have clear purposes, descriptions must guide selection accurately, and the system must handle edge cases gracefully.

This lesson covers patterns that make agents reliable and effective.

## Pattern 1: Tool Specialization

Each tool should have a **distinct, non-overlapping purpose**.

**Bad design** (overlapping):
```
Tool 1: "Search for companies"
Tool 2: "Find company information"
Tool 3: "Look up companies"
```
Problem: Agent can't distinguish between tools. Which handles "Tell me about Apple"?

**Good design** (specialized):
```
Tool 1: "Explore database structure and schema"
Tool 2: "Search content semantically about topics and concepts"
Tool 3: "Query specific facts, counts, and relationships"
```
Benefit: Clear boundaries. Each question type maps to one tool.

## Pattern 2: Descriptive Signatures

Tool names and docstrings guide selection. Be specific about *when* to use each tool.

**Vague (poor selection)**:
```python
def search(query: str) -> str:
    """Search the database."""
```

**Specific (accurate selection)**:
```python
def search_content_semantically(query: str) -> str:
    """Search for content about topics, concepts, and themes using semantic similarity.

    Use this tool when the user asks:
    - "What is..." or "Tell me about..."
    - Questions about strategies, approaches, or concepts
    - Exploratory questions about topics

    Do NOT use for:
    - Counting questions ("How many...")
    - Specific lookups ("Who owns...")
    - List requests ("List all...")
    """
```

Include both positive and negative guidance.

## Pattern 3: Tool Composition

Complex questions may need multiple tools in sequence.

**Example**: "What are Apple's main risks and which investors are affected?"

This requires:
1. Semantic search for Apple's risk content
2. Database query for investors owning Apple

The agent should:
1. Recognize the compound question
2. Call semantic search for risk content
3. Call database query for investor relationships
4. Synthesize both results

**Agent instructions can help**:
```
"For complex questions requiring both content and facts,
use multiple tools and combine results."
```

## Pattern 4: Graceful Fallbacks

Tools sometimes fail or return empty results. The agent should handle this gracefully.

**Poor handling**:
```
User: "What is XYZ Corp's strategy?"
Agent: Error: No results found.
```

**Graceful handling**:
```
User: "What is XYZ Corp's strategy?"
Agent: "I couldn't find specific information about XYZ Corp's strategy
in the available documents. You might want to check if XYZ Corp
is in the database, or try a different company name."
```

**Agent instructions can help**:
```
"If a tool returns no results, explain what happened and
suggest alternatives. Never make up information."
```

## Pattern 5: Clear Error Messages

When tools can't answer, explain *why*.

**Unhelpful**:
```
"I don't know."
```

**Helpful**:
```
"I searched for content about quantum computing but found no relevant
documents. The database primarily contains SEC filings which may not
discuss this topic in detail."
```

This helps users understand system limitations and refine their questions.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Too Many Similar Tools

Don't create multiple tools that do similar things:
```
search_companies()
find_companies()
get_companies()
list_companies()
```

Consolidate into one tool with a clear description.

### Anti-Pattern 2: Tools Without Clear Boundaries

If you can't clearly explain when to use a tool vs. another, rethink the design.

### Anti-Pattern 3: Overly Generic Tools

A single "answer any question" tool defeats the purpose of specialized tools.

### Anti-Pattern 4: Missing Docstrings

Tools without descriptions leave the agent guessing.

## Production Considerations

### Security

**Text2Cypher tools execute generated queries.** Always:
- Use read-only database credentials
- Validate queries for dangerous operations
- Limit result sizes

### Performance

- Cache common queries
- Limit result set sizes
- Set appropriate timeouts
- Consider parallel tool execution for independent queries

### Monitoring

- Log which tools are selected
- Track success/failure rates
- Monitor query patterns for improvement opportunities

### Testing

- Test each tool in isolation
- Test tool selection with various question phrasings
- Test multi-tool scenarios
- Test error handling

## Check Your Understanding

### What is the main purpose of specific tool docstrings?

**Options:**
- [ ] To document the code for developers
- [x] To guide the agent's tool selection
- [ ] To improve code readability
- [ ] To satisfy documentation requirements

<details>
<summary>Hint</summary>
Think about what the agent reads when deciding which tool to use.
</details>

<details>
<summary>Show Answer</summary>
**To guide the agent's tool selection**. The agent reads tool names and docstrings to decide which tool to use for a given question. Specific docstrings that describe when to use (and when not to use) a tool lead to more accurate selection.
</details>

## Summary

- **Tool Specialization**: Each tool has distinct, non-overlapping purpose
- **Descriptive Signatures**: Specific docstrings guide accurate selection
- **Tool Composition**: Complex questions may need multiple tools
- **Graceful Fallbacks**: Handle empty results and errors informatively
- **Production Considerations**: Security, performance, monitoring, testing

These patterns create agents that are reliable, accurate, and user-friendly.

---

**Navigation:**
- [← Previous: Building Your Agent](03-building-your-agent.md)
- [↑ Back to Lab 6](README.md)
- [Next: Congratulations →](05-congratulations.md)
