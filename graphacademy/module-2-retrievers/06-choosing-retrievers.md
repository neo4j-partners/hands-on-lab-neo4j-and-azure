# Choosing the Right Retriever

You've learned about three powerful retriever types. Now you need to know which one to use for different questions. This lesson provides a practical decision framework for choosing between Vector, Vector Cypher, and Text2Cypher retrievers.

## The Three Retriever Types

**Quick Summary:**

| Retriever | What It Does | Best For |
|-----------|--------------|----------|
| **Vector** | Semantic similarity search | Finding content about topics/concepts |
| **Vector Cypher** | Semantic search + graph traversal | Content + related entities/relationships |
| **Text2Cypher** | Natural language to database query | Specific facts, counts, lists |

## Decision Framework

Ask yourself these questions:

### 1. Am I looking for content or facts?

**Content (descriptions, explanations, discussions):**
→ Use Vector or Vector Cypher

**Facts (names, numbers, counts, specific values):**
→ Use Text2Cypher

**Examples:**
```
"What is Apple's business strategy?" → Content → Vector
"What companies are in the database?" → Facts → Text2Cypher
```

### 2. Do I need related entities?

**Just the relevant text chunks:**
→ Use Vector

**Text chunks + related entities from graph:**
→ Use Vector Cypher

**Examples:**
```
"What cybersecurity threats are mentioned?" → Just content → Vector
"What cybersecurity threats affect which companies?" → Content + entities → Vector Cypher
```

### 3. Is my question about relationships?

**No specific relationship query needed:**
→ Use Vector

**Need to traverse relationships:**
→ Use Vector Cypher or Text2Cypher

**Examples:**
```
"Tell me about AI technology" → No relationships → Vector
"Which companies are owned by BlackRock?" → Relationship query → Text2Cypher
"What risks connect Apple and Microsoft?" → Semantic + relationships → Vector Cypher
```

## Question Pattern Guide

### Vector Retriever Patterns

Use Vector when questions match these patterns:

**"What is...?"**
- "What is Apple's approach to privacy?"
- "What are the main trends in AI?"

**"Tell me about..."**
- "Tell me about cloud computing"
- "Tell me about supply chain challenges"

**"Describe..."**
- "Describe Microsoft's cloud strategy"
- "Describe the regulatory environment"

**"What does [topic/document] say about...?"**
- "What do the documents say about cybersecurity?"
- "What does Apple mention about competition?"

**Key Indicators:**
- Seeking explanations or descriptions
- Topic or concept-based
- Semantic understanding needed
- No need for precise counts or relationships

### Vector Cypher Retriever Patterns

Use Vector Cypher when questions match these patterns:

**"What [entities] are mentioned in [context]?"**
- "What companies are mentioned in cybersecurity risk sections?"
- "What products appear in regulatory discussions?"

**"Which [entities] are affected by [topic]?"**
- "Which asset managers are affected by banking regulations?"
- "Which companies face supply chain risks?"

**"What [relationships] exist around [topic]?"**
- "What asset managers own companies facing climate risks?"
- "What products are offered by companies with high revenue?"

**"Find [content] and related [entities]"**
- "Find discussions about AI and list the companies involved"
- "Find risk factors and show which companies face them"

**Key Indicators:**
- Need content AND entities
- Require graph traversal
- Relationship-aware context needed
- Combining semantic search with structure

### Text2Cypher Retriever Patterns

Use Text2Cypher when questions match these patterns:

**"How many...?"**
- "How many companies are in the database?"
- "How many risk factors does Apple face?"

**"List all..."**
- "List all asset managers"
- "List all products mentioned by Microsoft"

**"Which [entity] has the most/least...?"**
- "Which company has the most products?"
- "Which asset manager owns the most companies?"

**"What [entities] [specific relationship] [other entities]?"**
- "What companies does BlackRock own?"
- "What risk factors does Apple face?"

**"Who/What/Where [specific fact]?"**
- "Who are the executives at Microsoft?"
- "What stock types has Apple issued?"

**Key Indicators:**
- Needs counting or aggregation
- Requires specific entity names/IDs
- Asks about specific relationships
- Needs structured, factual answers

## Real-World Examples

### Example 1: Understanding vs. Counting

**Question:** "Tell me about risk factors"
- **Type:** Understanding/Content
- **Retriever:** Vector
- **Why:** Seeks semantic understanding of what risk factors are discussed

**Question:** "How many risk factors are there?"
- **Type:** Counting/Facts
- **Retriever:** Text2Cypher
- **Why:** Needs exact count from database

### Example 2: Simple vs. Enriched Search

**Question:** "What does Microsoft say about cloud computing?"
- **Type:** Content only
- **Retriever:** Vector
- **Why:** Just needs relevant text chunks about cloud computing

**Question:** "What products does Microsoft mention in cloud computing contexts?"
- **Type:** Content + Entities
- **Retriever:** Vector Cypher
- **Why:** Needs semantic search (cloud computing) + entity extraction (products)

### Example 3: Semantic vs. Structured

**Question:** "What companies are similar to Apple?"
- **Type:** Semantic similarity
- **Retriever:** Vector (search for chunks about companies, then extract names)
- **Why:** "Similar" is semantic, not a graph relationship

**Question:** "What companies face the same risks as Apple?"
- **Type:** Shared relationships
- **Retriever:** Vector Cypher or Text2Cypher
- **Why:** Can use graph structure to find shared FACES_RISK relationships

## Combining Retrievers

Sometimes the best approach is using multiple retrievers:

**Multi-Retriever Strategy:**
```python
# First, get list of relevant entities
entities_result = text2cypher_retriever.search("List all tech companies")
companies = [r['name'] for r in entities_result.records]

# Then, get semantic content about those entities
for company in companies:
    content = vector_retriever.search(f"What does {company} say about AI?")
```

**Agent-Based Approach:**
In Module 3, you'll learn to build agents that automatically choose the right retriever based on the question type.

## Common Mistakes

### Mistake 1: Using Text2Cypher for Semantic Questions

**Wrong:**
```
Question: "What is Apple's strategy?"
Retriever: Text2Cypher
Problem: Generates poor Cypher, returns chunks in non-semantic way
```

**Right:**
```
Question: "What is Apple's strategy?"
Retriever: Vector
Why: This is semantic content search
```

### Mistake 2: Using Vector for Counting

**Wrong:**
```
Question: "How many companies are there?"
Retriever: Vector
Problem: Returns chunks mentioning companies, can't count accurately
```

**Right:**
```
Question: "How many companies are there?"
Retriever: Text2Cypher
Why: Needs database count query
```

### Mistake 3: Using Basic Vector When You Need Entities

**Wrong:**
```
Question: "Which asset managers own companies facing cyber risks?"
Retriever: Vector
Problem: Returns text chunks, doesn't traverse to asset managers
```

**Right:**
```
Question: "Which asset managers own companies facing cyber risks?"
Retriever: Vector Cypher
Why: Needs semantic search + graph traversal
```

## Performance Considerations

**Vector Retriever:**
- Fastest for simple semantic search
- Scales well with large document collections
- Minimal database load

**Vector Cypher:**
- Slower than basic vector (adds graph traversal)
- Performance depends on query complexity
- Can return large result sets if not limited

**Text2Cypher:**
- Performance varies by generated query
- Can be slow for complex aggregations
- Risk of inefficient queries if LLM generates poorly

**Optimization Tips:**
- Use appropriate `top_k` values
- Add LIMIT clauses to queries
- Slice collections in Cypher `[0..20]`
- Test queries with EXPLAIN/PROFILE

## Quick Reference Chart

| Your Need | Use This |
|-----------|----------|
| Find content about a topic | Vector |
| Count or list entities | Text2Cypher |
| Find content + related entities | Vector Cypher |
| Answer "how many" | Text2Cypher |
| Answer "what is" | Vector |
| Answer "who owns" | Text2Cypher |
| Answer "what risks affect which companies" | Vector Cypher |
| Explore a concept | Vector |
| Get specific facts | Text2Cypher |
| Combine content + structure | Vector Cypher |

## Check Your Understanding

### Which retriever should you use for "What products does Microsoft mention?"

**Options:**
- [ ] Vector Retriever
- [ ] Vector Cypher Retriever
- [x] Text2Cypher Retriever
- [ ] All of the above

<details>
<summary>Hint</summary>
This question asks for a specific list of entities.
</details>

<details>
<summary>Show Answer</summary>
**Text2Cypher Retriever**. This question asks for a specific list of products (entities), which requires a structured query like `MATCH (c:Company {name: 'MICROSOFT'})-[:MENTIONS]->(p:Product) RETURN p.name`. Text2Cypher is ideal for listing specific entities.
</details>

### Which retriever should you use for "What are Apple's main challenges?"

**Options:**
- [x] Vector Retriever
- [ ] Vector Cypher Retriever
- [ ] Text2Cypher Retriever
- [ ] None work for this

<details>
<summary>Hint</summary>
This question seeks content and understanding, not specific facts.
</details>

<details>
<summary>Show Answer</summary>
**Vector Retriever**. This is a semantic question seeking content about challenges. Vector search will find relevant chunks discussing Apple's challenges, obstacles, and difficulties even if they use different wording. No graph traversal or structured query is needed.
</details>

## Summary

In this lesson, you learned how to choose the right retriever:

**Decision Framework:**
1. Content vs. Facts → Vector vs. Text2Cypher
2. Need related entities? → Add Cypher
3. Relationship queries? → Vector Cypher or Text2Cypher

**Retriever Strengths:**
- **Vector:** Semantic content search, fast, scalable
- **Vector Cypher:** Content + entities, relationship-aware
- **Text2Cypher:** Precise facts, counts, lists, structured queries

**Question Patterns:**
- "What is..." → Vector
- "How many..." → Text2Cypher
- "What [entities] are affected by [topic]..." → Vector Cypher

**Key Principle:**
Match your retriever to your question type. Semantic questions need Vector, factual questions need Text2Cypher, and relationship-aware questions need Vector Cypher.

In Lab 5, you've already implemented all three retriever types. In Module 3, you'll learn to build intelligent agents that automatically choose the right retriever based on the user's question.

---

**Navigation:**
- [← Previous: Text2Cypher Retriever](05-text2cypher-retriever.md)
- [↑ Back to Module 2](README.md)
- [Next: Module 3 - Agents →](../module-3-agents/README.md)
