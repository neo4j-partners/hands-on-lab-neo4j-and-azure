# Multi-Tool Agent Design

Now that you've built a complete multi-tool agent, let's explore the design patterns and principles that make agents work effectively. Understanding how agents select tools and combine them will help you build better GraphRAG systems.

## How Agents Select Tools

### The Selection Process

When an agent receives a question, it follows this process:

```
1. ANALYZE QUESTION
   - Parse the user's natural language query
   - Identify key intent and requirements

2. EVALUATE TOOLS
   - Read each tool's name and docstring
   - Match tool capabilities to question needs

3. SELECT TOOL(S)
   - Choose the most appropriate tool
   - May select multiple tools in sequence

4. EXECUTE
   - Call the selected tool(s)
   - Collect results

5. SYNTHESIZE
   - Combine tool results
   - Generate coherent answer
```

### Tool Matching Logic

The agent uses **semantic similarity** between:
- The user's question
- Tool function names
- Tool docstrings

**Example:**
```
Question: "How many companies are in the database?"

Tool Options:
1. get_graph_schema()
   "Get the schema of the graph database..."
   Match: Low (question is about count, not schema)

2. retrieve_financial_documents(query)
   "Find details about companies in their financial documents..."
   Match: Medium (mentions companies but for semantic search)

3. query_database(query)
   "Get answers to specific questions about companies, risks, and financial metrics..."
   Match: High (mentions "specific questions" and "companies")

Selection: Tool 3 (query_database)
```

## Design Pattern 1: Progressive Enhancement

**Start Simple, Add Complexity:**

1. **Single Tool Agent**
   - One focused capability
   - Easy to understand and debug
   - Limited scope

2. **Two-Tool Agent**
   - Adds complementary capability
   - Agent learns to choose
   - Covers more question types

3. **Multi-Tool Agent**
   - Complete capability suite
   - Handles any question type
   - Complex but powerful

**Your Workshop Journey:**
- Lesson 3: Schema tool only
- Lesson 4: + Vector search
- Lesson 5: + Text2Cypher
- Result: Complete GraphRAG agent

## Design Pattern 2: Tool Specialization

**Each Tool Has Clear Purpose:**

| Tool | Specialization | When Agent Uses It |
|------|---------------|-------------------|
| Schema | Graph structure | "What entities exist?" |
| Vector Search | Semantic content | "What does Apple say about...?" |
| Text2Cypher | Precise facts | "How many companies...?" |

**Key Principle:** No overlap in tool responsibilities.

**Bad Design:**
- Tool 1: Search for companies
- Tool 2: Find companies in documents
- Tool 3: List companies
- Problem: Three tools do similar things, agent gets confused

**Good Design:**
- Tool 1: Explore schema/structure
- Tool 2: Search semantic content
- Tool 3: Query precise facts
- Benefit: Clear boundaries, easy selection

## Design Pattern 3: Descriptive Tool Signatures

**Tool signatures guide agent selection:**

```python
# ✓ GOOD: Clear name and detailed docstring
def retrieve_financial_documents(
    query: Annotated[str, Field(description="The search query to find relevant documents")]
) -> str:
    """Find details about companies in their financial documents using semantic search.

    Use this tool when the user asks about:
    - Content or topics in documents
    - What companies mention or discuss
    - Themes or concepts across filings
    """
    ...

# ✗ BAD: Vague name and minimal docstring
def search(query: str) -> str:
    """Search documents."""
    ...
```

**Best Practices:**
- Use descriptive function names
- Write detailed docstrings
- Include example use cases
- Mention key entities/concepts
- Use type annotations

## Design Pattern 4: Tool Composition

**Agents can use multiple tools for complex questions:**

**Question:** "What are Apple's main risks and which asset managers might be affected?"

**Agent Reasoning:**
```
Step 1: This needs risk information (semantic content)
→ Use retrieve_financial_documents("Apple risks")

Step 2: Now I have risk names, need to find asset managers
→ Use query_database("Which asset managers own Apple?")

Step 3: Combine both results into comprehensive answer
```

**This is powerful because:**
- No single tool has all the information
- Agent orchestrates multiple tools
- Results are combined intelligently
- More comprehensive answers

## Design Pattern 5: Fallback Strategies

**What happens when tools fail?**

**Graceful Degradation:**
```
Question: "Tell me about Microsoft's cloud strategy"

Try 1: Vector search for "Microsoft cloud strategy"
Result: ✓ Found relevant chunks

Question: "How many products does XYZ Corp offer?"

Try 1: Text2Cypher "count products for XYZ Corp"
Result: ✗ Company "XYZ Corp" not found

Fallback: Agent responds:
"I couldn't find a company named 'XYZ Corp' in the database.
The available companies are: [list from schema]"
```

**Agent should:**
- Detect tool failures
- Explain why it couldn't answer
- Suggest alternatives
- Not hallucinate information

## Common Multi-Tool Patterns

### Pattern: Explore → Search
```
Question: "What can I learn about tech companies?"

Agent:
1. get_graph_schema() → See what data exists
2. retrieve_financial_documents("technology companies") → Get content
3. Synthesize answer with context
```

### Pattern: Query → Enhance
```
Question: "Tell me about the top 3 companies by risk factors"

Agent:
1. query_database("companies with most risk factors") → Get top 3
2. retrieve_financial_documents("risks for [company names]") → Get details
3. Combine counts with semantic descriptions
```

### Pattern: Validate → Execute
```
Question: "How many risk factors does Banana Corp face?"

Agent:
1. get_graph_schema() → Check if Company nodes exist
2. query_database("count risks for Banana Corp") → Run query
3. Return precise answer
```

## Tool Design Anti-Patterns

### Anti-Pattern 1: Tool Overload
```
✗ 10+ tools with overlapping purposes
✓ 3-5 well-defined tools with clear boundaries
```

### Anti-Pattern 2: Black Box Tools
```
✗ def tool_x() -> str:
    """Does stuff."""

✓ def get_company_risks(company: str) -> str:
    """Retrieves risk factors that a specific company faces.
    Returns a list of risk names from the FACES_RISK relationships."""
```

### Anti-Pattern 3: Over-Specific Tools
```
✗ get_apple_risks()
✗ get_microsoft_products()
✗ count_amazon_metrics()

✓ query_database(query: str)  # Handles all specific queries
```

### Anti-Pattern 4: Under-Specific Tools
```
✗ def search_everything(query: str) -> str:
    """Search for anything."""
    # Does vector + cypher + text2cypher all in one

✓ Separate tools for each search type
```

## Agent Instructions Matter

**The agent's system instructions guide tool usage:**

**Generic Instructions:**
```
"You are a helpful assistant."
```
→ Agent may struggle to know when to use tools

**Specific Instructions:**
```
"You are a helpful assistant that answers questions about a graph database
containing financial documents. You have three tools:

1. get_graph_schema - Use when asked about data structure
2. retrieve_financial_documents - Use for semantic content questions
3. query_database - Use for specific facts, counts, or precise queries

Choose the appropriate tool(s) based on the question type."
```
→ Clear guidance on tool selection

## Testing Multi-Tool Agents

**Test Each Tool Independently:**
```
✓ Test schema tool with structure questions
✓ Test vector tool with semantic questions
✓ Test Text2Cypher tool with fact questions
```

**Test Tool Selection:**
```
✓ Verify agent picks right tool for each question type
✓ Check agent uses multiple tools when needed
✓ Ensure fallback when tools fail
```

**Test Edge Cases:**
```
✓ Ambiguous questions
✓ Out-of-scope questions
✓ Questions requiring multiple tools
✓ Questions with no good answer
```

## Summary

In this lesson, you learned multi-tool agent design patterns:

**Key Principles:**
- Agents use semantic matching to select tools
- Each tool should have a clear, distinct purpose
- Descriptive names and docstrings guide selection
- Agents can compose multiple tools for complex questions

**Design Patterns:**
- Progressive Enhancement: Start simple, add complexity
- Tool Specialization: Clear boundaries between tools
- Descriptive Signatures: Help agents choose correctly
- Tool Composition: Multiple tools for complex needs
- Fallback Strategies: Handle failures gracefully

**Best Practices:**
- 3-5 well-defined tools
- Detailed docstrings with examples
- Clear system instructions
- Test tool selection logic
- Handle edge cases

**Anti-Patterns to Avoid:**
- Too many overlapping tools
- Vague tool descriptions
- Over-specific or under-specific tools
- Poor agent instructions

You now understand how to design effective multi-tool agents that intelligently route questions to the right retrievers, creating powerful and user-friendly GraphRAG systems.

---

**Navigation:**
- [← Previous: Text2Cypher Agent](05-text2cypher-agent.md)
- [↑ Back to Module 3](README.md)
- [Next: Aura Agents →](07-aura-agents.md)
