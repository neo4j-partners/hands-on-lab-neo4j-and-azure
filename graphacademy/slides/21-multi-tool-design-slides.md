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


# Multi-Tool Agent Design

Module 3, Lesson 6

**Note:** This slide will be renumbered in final sequencing

---

## How Agents Select Tools

**The Selection Process:**

```
1. ANALYZE QUESTION
   Parse the user's natural language query
   ↓
2. EVALUATE TOOLS
   Read each tool's name and docstring
   ↓
3. SELECT TOOL(S)
   Choose the most appropriate tool
   ↓
4. EXECUTE
   Call the selected tool(s)
   ↓
5. SYNTHESIZE
   Combine results into coherent answer
```

**The agent uses semantic similarity** between question and tool docstrings!

---

## Tool Matching Logic Example

**Question:** "How many companies are in the database?"

**Tool Options:**

**1. get_graph_schema()**
   _"Get the schema of the graph database..."_
   Match: **Low** ❌ (question is about count, not schema)

**2. retrieve_financial_documents(query)**
   _"Find details about companies in their financial documents..."_
   Match: **Medium** ⚠️ (mentions companies but for semantic search)

**3. query_database(query)**
   _"Get answers to specific questions about companies, risks..."_
   Match: **High** ✅ (mentions "specific questions" and "companies")

**Agent Selects:** Tool 3 (query_database)

---

## Design Pattern 1: Progressive Enhancement

**Build Complexity Incrementally:**

### Stage 1: Single Tool Agent
- One focused capability
- Easy to understand and debug
- Limited scope

### Stage 2: Two-Tool Agent
- Adds complementary capability
- Agent learns to choose between options
- Covers more question types

### Stage 3: Multi-Tool Agent
- Complete capability suite
- Handles any question type
- Complex but powerful

---

## Your Workshop Journey

**Progressive Enhancement in Action:**

| Lesson | Tools | Capabilities |
|--------|-------|--------------|
| **Lesson 3** | Schema | Database structure queries |
| **Lesson 4** | + Vector Search | Semantic content retrieval |
| **Lesson 5** | + Text2Cypher | Precise facts and counts |
| **Result** | 3 Tools | Complete GraphRAG agent! |

**Each step adds capability without breaking existing functionality.**

---

## Design Pattern 2: Tool Specialization

**Each Tool Has Clear, Non-Overlapping Purpose:**

| Tool | Specialization | When Agent Uses It |
|------|---------------|-------------------|
| **Schema** | Graph structure | "What entities exist?" |
| **Vector Search** | Semantic content | "What does Apple say about...?" |
| **Text2Cypher** | Precise facts | "How many companies...?" |

**Key Principle:** No overlap in tool responsibilities.

**Why?** Prevents agent confusion and improves tool selection accuracy.

---

## Bad Design: Overlapping Tools

❌ **Don't do this:**

```python
tools = [
    search_for_companies,     # Finds companies by keyword
    find_companies,           # Finds companies in documents
    list_all_companies,       # Lists companies in database
    get_company_info          # Gets company information
]
```

**Problems:**
- Agent confused about which to use
- Redundant functionality
- Increased token usage (all docstrings sent to LLM)
- Slower decision-making

---

## Good Design: Specialized Tools

✅ **Do this instead:**

```python
tools = [
    get_graph_schema,              # Structure only
    retrieve_documents,            # Semantic search only
    query_database                 # Precise queries only
]
```

**Benefits:**
- Clear tool purposes
- Faster agent decisions
- Easier to debug
- Better user experience

**Each tool is the best at ONE thing!**

---

## Design Pattern 3: Clear Tool Naming

**Tool naming affects agent's decision-making:**

### Bad Names
```python
def tool1():  # What does it do?
def get_info():  # What kind of info?
def search():  # Search what? How?
```

### Good Names
```python
def get_graph_schema():  # Clear purpose
def retrieve_financial_documents(query):  # Specific scope
def query_database_for_facts(query):  # Explains when to use
```

**Pattern:** `verb_what_how` or `action_target_context`

---

## Design Pattern 4: Informative Docstrings

**The docstring is the agent's guide!**

### Bad Docstring
```python
def retrieve_documents(query):
    """Get documents"""
    ...
```
❌ Too vague, agent won't know when to use it

### Good Docstring
```python
def retrieve_financial_documents(query):
    """Find details about companies in their financial documents
    using semantic search.

    Best for questions about:
    - Company strategies and approaches
    - Risk factors and challenges
    - Business descriptions and operations
    - Product and service offerings
    """
    ...
```
✅ Clear scope, examples of when to use

---

## Docstring Best Practices

**Include:**

1. **What it does** - Clear description of functionality
2. **When to use** - Question patterns that fit
3. **What it returns** - Type of data/format
4. **Examples** (optional) - Sample questions

```python
def query_database(question: str) -> str:
    """Answer specific factual questions by querying the
    graph database directly.

    Use for:
    - Counting entities ("How many companies?")
    - Listing entities ("List all products")
    - Finding relationships ("Who owns Apple?")
    - Aggregations ("Average risks per company?")

    Returns structured data as natural language.
    """
    ...
```

---

## Design Pattern 5: Composition Over Duplication

**Compose tools from shared components:**

```python
# Shared retriever instances
schema_retriever = SchemaRetriever(driver)
vector_retriever = VectorCypherRetriever(driver, ...)
text2cypher_retriever = Text2CypherRetriever(driver, llm, schema)

# Tools composed from retrievers
def get_graph_schema():
    """..."""
    return schema_retriever.get_schema()

def retrieve_documents(query):
    """..."""
    return vector_retriever.search(query)

def query_database(query):
    """..."""
    return text2cypher_retriever.search(query)
```

**Benefits:** Reusable components, easier testing, consistent behavior

---

## Anti-Pattern 1: Too Many Tools

❌ **Don't overwhelm the agent:**

```python
tools = [
    get_schema, get_nodes, get_relationships, get_properties,
    search_companies, search_products, search_risks,
    count_companies, count_products, count_risks,
    list_companies, list_products, list_risks,
    ...  # 20+ tools total
]
```

**Problems:**
- Agent decision paralysis
- High token costs (all docstrings to LLM)
- Slower responses
- More errors in tool selection

**Rule of thumb:** 3-7 tools is optimal

---

## Anti-Pattern 2: Tools That Do Everything

❌ **Don't create super-tools:**

```python
def do_everything(query, mode, options, filters, ...):
    """Does everything: schema, search, queries, aggregations..."""
    if mode == "schema":
        return get_schema()
    elif mode == "search":
        return vector_search(query)
    elif mode == "query":
        return text2cypher(query)
    # ... 100 more lines
```

**Problems:**
- Agent doesn't know when to use it
- Complex docstring confuses selection
- Hard to debug
- Violates single responsibility principle

---

## Anti-Pattern 3: Vague Tool Boundaries

❌ **Avoid ambiguous overlap:**

```python
def search_documents(query):
    """Search for information in documents"""
    # Uses vector search
    ...

def find_information(query):
    """Find information about topics"""
    # Also uses vector search?
    ...
```

**When are they different?** Agent can't tell!

**Fix:** Consolidate into one well-defined tool or clearly differentiate.

---

## Tool Selection Debugging

**When agent picks wrong tool:**

**1. Check docstrings:**
- Are they clear and distinct?
- Do they describe when to use each tool?

**2. Test with explicit questions:**
```python
# Should use schema tool
"What entities exist in the database?"

# Should use vector search
"What does Apple say about AI?"

# Should use text2cypher
"How many products does Microsoft have?"
```

**3. Monitor tool usage:**
- Microsoft Foundry shows tool call history
- Look for patterns in errors

---

## Balancing Tool Count

**Too Few Tools (1-2):**
- ✅ Simple, easy to debug
- ❌ Limited capabilities
- ❌ Can't handle diverse questions

**Optimal Range (3-7):**
- ✅ Comprehensive coverage
- ✅ Clear specialization
- ✅ Good agent decision-making
- ✅ Reasonable token usage

**Too Many Tools (10+):**
- ❌ Agent confusion
- ❌ High token costs
- ❌ Slower decisions
- ✅ Maximum coverage (but at cost)

---

## The GraphRAG "Sweet Spot"

**Three specialized tools:**

1. **Schema Tool** - Structure understanding
2. **Vector Search Tool** - Semantic content
3. **Text2Cypher Tool** - Precise facts

**Why this works:**
- Clear non-overlapping purposes
- Covers all major question types
- Easy for agent to choose correctly
- Low token overhead
- Fast decision-making

**This is the pattern you built in the workshop!**

---

## Evolution Example: From 1 to 3 Tools

**Agent with 1 Tool (Schema):**
```
Q: "What entities exist?"
A: ✅ "Companies, RiskFactors, AssetManagers..."
Q: "What are Apple's risks?"
A: ❌ "I can only show you the schema."
```

**Agent with 2 Tools (Schema + Vector):**
```
Q: "What are Apple's risks?"
A: ✅ "Apple faces data privacy risks..."
Q: "How many risk factors does Apple have?"
A: ⚠️ Returns text mentioning numbers, not exact count
```

**Agent with 3 Tools (Schema + Vector + Text2Cypher):**
```
Q: "How many risk factors does Apple have?"
A: ✅ "Apple has exactly 45 risk factors." (precise!)
```

---

## Testing Multi-Tool Agent Design

**Validation Questions:**

✅ **Can each tool be described in one sentence?**
   If not, it might be doing too much

✅ **Do tools have clear, non-overlapping purposes?**
   No ambiguity in which tool handles what

✅ **Can you predict which tool should handle each question type?**
   Agent should be able to too

✅ **Are there fewer than 10 tools?**
   Optimal decision-making range

✅ **Does each tool have a clear docstring with examples?**
   Agent needs good documentation

---

## Real-World Patterns

**Enterprise Knowledge Graph Agents:**
- Schema introspection tool
- Vector search for documents/content
- Text2Cypher for business intelligence queries
- (Optional) External API tools for live data

**Customer Service Agents:**
- FAQ retriever (vector search)
- Order status checker (precise query)
- Product catalog searcher (structured query)

**Research Agents:**
- Literature search (vector/semantic)
- Citation finder (precise query)
- Related work finder (graph traversal)

---

## Summary

Multi-tool agent design requires careful planning:

**Key Patterns:**
- **Progressive Enhancement:** 1 tool → 2 tools → Multi-tool
- **Tool Specialization:** Non-overlapping, clear purposes
- **Clear Naming:** Descriptive function names
- **Informative Docstrings:** When to use, what it returns
- **Composition:** Build tools from shared components

**Anti-Patterns to Avoid:**
- Too many tools (>10)
- Tools that do everything
- Vague/overlapping boundaries

**The GraphRAG Sweet Spot:** 3 specialized tools (schema, vector, text2cypher)

---

## Next Steps

In the next lesson, you will learn about Aura Agents - Neo4j's no-code interface for building GraphRAG agents without writing Python code.

**What You've Learned:**
- How agents select tools
- Design patterns for multi-tool agents
- Best practices for tool definitions
- Common anti-patterns to avoid

**Apply This:** When designing your own agents!
