# Text2Cypher Retriever

The Text2Cypher Retriever converts natural language questions directly into Cypher queries. It bypasses semantic search entirely, querying the graph structure for precise, factual answers.

![A diagram showing the text-to-cypher process](../images/llm-text-to-cypher-process.svg)

## When to Use Text2Cypher Retriever

**Ideal for:**
- Counting entities or relationships
- Listing specific entities
- Direct relationship lookups
- Comparisons and aggregations
- Factual questions with precise answers

**Example questions:**
- "How many companies are in the database?"
- "What companies does BlackRock own?"
- "Which company has the most risk factors?"
- "List all asset managers"
- "What products does Apple mention?"

## How It Works

1. **Analyze question**: LLM examines your question and the graph schema
2. **Generate Cypher**: LLM produces a Cypher query to answer the question
3. **Execute query**: Query runs against the database
4. **Return results**: Structured, precise results from the graph
5. **Format answer**: Optionally, LLM formats results as natural language

**The key insight**: No semantic search. The LLM translates your intent directly into a database query.

## Example: How It Translates Questions

![Cypher query language visualization](../images/cypher.svg)

| Question | Generated Cypher |
|----------|-----------------|
| "How many companies?" | `MATCH (c:Company) RETURN count(c)` |
| "Who owns Apple?" | `MATCH (am:AssetManager)-[:OWNS]->(c:Company {name:'APPLE INC'}) RETURN am.managerName` |
| "Which company has the most risks?" | `MATCH (c:Company)-[:FACES_RISK]->(r) RETURN c.name, count(r) ORDER BY count(r) DESC LIMIT 1` |
| "List all products" | `MATCH (p:Product) RETURN p.name LIMIT 20` |

The LLM understands your intent and maps it to the graph structure.

## Strengths

- **Precise answers**: Exact counts, specific entities, direct lookups
- **Aggregations**: Sum, count, average, min, max
- **Comparisons**: "most," "least," "top 5"
- **Direct relationships**: "Who owns," "What faces," "Which connects"
- **No semantic ambiguity**: Query returns exactly what the database contains

## Limitations

- **Schema dependent**: LLM must understand your graph structure
- **May generate invalid Cypher**: Complex questions can produce bad queries
- **Not for semantic questions**: "What is Apple's strategy?" doesn't map to a clean query
- **Requires good prompting**: Custom prompts improve query quality
- **Security consideration**: Executes generated queries—use read-only credentials

## When Text2Cypher Works Best

**Good fit questions:**

| Question Pattern | Why It Works |
|-----------------|--------------|
| "How many [entities]?" | Direct count query |
| "List all [entities]" | Simple MATCH and RETURN |
| "What [entities] does [entity] [relationship]?" | Direct relationship traversal |
| "Which [entity] has the most [relationship]?" | Aggregation with ORDER BY |

**Poor fit questions:**

| Question | Problem | Better Retriever |
|----------|---------|------------------|
| "What is Apple's strategy?" | Semantic, not factual | Vector |
| "Tell me about cybersecurity" | Exploratory content | Vector |
| "What topics are discussed?" | Too vague for Cypher | Vector |

## Comparing All Three Retrievers

| Question Type | Best Retriever | Why |
|--------------|----------------|-----|
| "What is..." / "Tell me about..." | Vector | Semantic content search |
| "Which [entities] are affected by [topic]..." | Vector Cypher | Semantic + graph traversal |
| "How many..." / "List all..." / "Who owns..." | Text2Cypher | Precise database query |

**Decision framework:**
1. **Content or facts?** Content → Vector/Vector Cypher. Facts → Text2Cypher.
2. **Need relationships from content?** Yes → Vector Cypher.
3. **Need precise counts or lists?** Yes → Text2Cypher.

## Security Considerations

Text2Cypher executes LLM-generated queries against your database. Important safeguards:

- **Use read-only credentials**: Prevent accidental data modification
- **Validate queries**: Check for dangerous operations (DELETE, DROP, CREATE)
- **Limit results**: Ensure LIMIT clauses prevent unbounded returns
- **Monitor usage**: Log generated queries for review
- **Don't expose to untrusted users**: Generated Cypher could be exploited

## Check Your Understanding

### When should you use Text2Cypher instead of Vector Retriever?

**Options:**
- [ ] When you want semantic similarity
- [x] When you need precise counts or entity lists
- [ ] When you don't know what you're looking for
- [ ] When you need to search document text

<details>
<summary>Hint</summary>
Think about what kind of questions need database queries vs. semantic search.
</details>

<details>
<summary>Show Answer</summary>
**When you need precise counts or entity lists**. Text2Cypher converts questions to database queries for exact answers. Use Vector Retriever for semantic content search ("Tell me about..."), and Text2Cypher for factual queries ("How many...", "List all...", "Who owns...").
</details>

## Summary

- **Text2Cypher Retriever** converts natural language to Cypher queries
- **Best for** counting, listing, direct lookups, aggregations
- **Works by** LLM generating Cypher from question + schema
- **Strengths**: Precise, structured, factual answers
- **Limitations**: Schema dependent, not for semantic questions, security considerations

## The Complete Picture

You now understand three retrieval patterns:

| Retriever | Finds | Best For |
|-----------|-------|----------|
| **Vector** | Similar content | Conceptual questions, exploration |
| **Vector Cypher** | Content + connected entities | Relationship-aware content |
| **Text2Cypher** | Precise facts | Counts, lists, lookups |

Understanding *why* each retriever works for different questions prepares you for Lab 6, where you'll build agents that automatically choose the right retriever based on the question.

---

**Navigation:**
- [← Previous: Vector Cypher Retriever](03-vector-cypher-retriever.md)
- [↑ Back to Lab 6](README.md)
- [Next: Lab 7 - Intelligent Agents →](../lab-7-agents/README.md)
