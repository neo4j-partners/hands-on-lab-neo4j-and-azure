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


# Choosing the Right Retriever

Module 2, Lesson 6

**Note:** This slide will be renumbered in final sequencing

---

## The Three Retriever Types

**Quick Summary:**

| Retriever | What It Does | Best For |
|-----------|--------------|----------|
| **Vector** | Semantic similarity search | Finding content about topics/concepts |
| **Vector Cypher** | Semantic search + graph traversal | Content + related entities/relationships |
| **Text2Cypher** | Natural language to database query | Specific facts, counts, lists |

**Your challenge:** Choose the right tool for each question!

---

## Decision Framework

**Three Key Questions:**

### 1. Am I looking for content or facts?

**Content** (descriptions, explanations, discussions)
→ Use Vector or Vector Cypher

**Facts** (names, numbers, counts, specific values)
→ Use Text2Cypher

---

## Content vs Facts Examples

<div style="display: flex; gap: 2rem;">

<div style="flex: 1;">

### Content Questions

**Use Vector/Vector Cypher:**

- "What is Apple's business strategy?"
- "Describe AI safety concerns"
- "What does the document say about privacy?"
- "Explain supply chain challenges"

**Nature:** Exploratory, descriptive

</div>

<div style="flex: 1;">

### Fact Questions

**Use Text2Cypher:**

- "What companies are in the database?"
- "How many risk factors does Apple have?"
- "List all products by Microsoft"
- "Which asset manager owns the most companies?"

**Nature:** Precise, quantifiable

</div>

</div>

---

## Decision Framework (continued)

### 2. Do I need related entities?

**Just the relevant text chunks:**
→ Use Vector

**Text chunks + related entities from graph:**
→ Use Vector Cypher

**Examples:**
```
"What cybersecurity threats are mentioned?"
    → Just content → Vector

"What cybersecurity threats affect which companies?"
    → Content + entities → Vector Cypher
```

---

## Decision Framework (continued)

### 3. Is my question about relationships?

**No specific relationship query needed:**
→ Use Vector

**Need to traverse relationships:**
→ Use Vector Cypher or Text2Cypher

**Examples:**
```
"Tell me about AI technology"
    → No relationships → Vector

"Which companies are owned by BlackRock?"
    → Relationship query → Text2Cypher

"What risks connect Apple and Microsoft?"
    → Semantic + relationships → Vector Cypher
```

---

## Question Pattern Guide: Vector Retriever

**Use Vector when questions match these patterns:**

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
- "What do SEC filings say about cybersecurity?"

---

## Question Pattern Guide: Vector Cypher

**Use Vector Cypher when you need semantic + graph:**

**"Which [entities] are affected by [topic]?"**
- "Which companies are affected by AI regulation?"
- "Which asset managers are exposed to cryptocurrency risk?"

**"What [entities] are related to [content]?"**
- "What companies have products mentioned in cloud computing documents?"
- "What executives are associated with privacy concerns?"

**"Find [content] about [entity] including [relationships]"**
- "Find risks about Apple including related asset managers"

---

## Question Pattern Guide: Text2Cypher

**Use Text2Cypher for precise queries:**

**"How many...?"**
- "How many risk factors does Apple face?"
- "How many companies are owned by Vanguard?"

**"List all..."**
- "List all products by Microsoft"
- "List all asset managers in the database"

**"Which [entity] has the most/least...?"**
- "Which company has the most products?"
- "Which asset manager owns the fewest companies?"

**"What is the [aggregate]...?"**
- "What is the average number of risks per company?"

---

## Real-World Question Analysis

**Question:** "What are Apple's main products?"

**Analysis:**
- Content vs Facts? → **Content** (descriptive)
- Need entities? → No, just text about products
- Relationships? → Not specifically

**Decision:** ✅ **Vector Retriever**

**Why:** Looking for descriptive content about products, not a precise list.

---

## Real-World Question Analysis

**Question:** "Which asset managers own companies facing AI risks?"

**Analysis:**
- Content vs Facts? → **Content + Entities** (AI risks in text + asset managers)
- Need entities? → Yes (asset managers, companies)
- Relationships? → Yes (OWNS, FACES_RISK)

**Decision:** ✅ **Vector Cypher Retriever**

**Why:** Semantic search for "AI risks" + graph traversal for ownership relationships.

---

## Real-World Question Analysis

**Question:** "How many companies does BlackRock own?"

**Analysis:**
- Content vs Facts? → **Facts** (specific count)
- Need entities? → Yes, but as structured data
- Relationships? → Yes (OWNS relationship)

**Decision:** ✅ **Text2Cypher Retriever**

**Generated Cypher:**
```cypher
MATCH (am:AssetManager {managerName: "BlackRock Inc."})-[:OWNS]->(c:Company)
RETURN count(c) AS companiesOwned
```

---

## Ambiguous Questions: How to Decide

**Question:** "Tell me about Apple"

**Too broad!** Could mean:
- Company description → Vector
- All facts about Apple → Text2Cypher + Vector Cypher
- Related entities → Vector Cypher

**Best Approach:**
1. Use Vector for initial exploration
2. Follow up with Text2Cypher for specific facts
3. Use Vector Cypher for relationship insights

**In agents:** Let the LLM choose based on conversation context!

---

## Combining Retrievers

**Best Practice:** Use multiple retrievers in sequence

**Example Flow:**

1. **Vector:** "What does the document say about AI safety?"
   → Get content overview

2. **Vector Cypher:** "Which companies are mentioned in AI safety content?"
   → Get content + entities

3. **Text2Cypher:** "How many AI-related risk factors does each company have?"
   → Get precise counts

**Each retriever provides a different lens on the data!**

---

## Performance Considerations

| Retriever | Speed | Complexity | Use Case |
|-----------|-------|------------|----------|
| **Vector** | Fast | Simple | Most common questions |
| **Vector Cypher** | Medium | Moderate | Balanced needs |
| **Text2Cypher** | Varies | Variable | Depends on query complexity |

**Optimization Tips:**
- Start with faster retrievers when possible
- Cache common queries
- Use appropriate `top_k` for Vector searches
- Profile Text2Cypher generated queries

---

## Common Mistakes to Avoid

❌ **Using Text2Cypher for content questions**
```
"What is Apple's strategy?" → Will fail or return minimal data
```

❌ **Using Vector for precise counts**
```
"How many companies?" → Will return chunks mentioning numbers, not actual count
```

❌ **Using Vector when you need relationships**
```
"Which asset managers own Apple?" → Won't traverse OWNS relationships
```

✅ **Match retriever to question type!**

---

## Decision Tree

```
START: Analyze Question
    ↓
Need specific facts/counts? ——YES——→ Text2Cypher
    ↓ NO
Need related entities/relationships? ——YES——→ Vector Cypher
    ↓ NO
Looking for content/descriptions? ——YES——→ Vector
    ↓ NO
Ambiguous/Complex? ——→ Use Multiple Retrievers or Agent
```

---

## Practice: Classify These Questions

**1.** "What are the top 5 companies by number of products?"
**Answer:** Text2Cypher (count/aggregation)

**2.** "Describe cloud computing trends"
**Answer:** Vector (content/descriptive)

**3.** "Which companies face cybersecurity risks and who are their major shareholders?"
**Answer:** Vector Cypher (semantic + relationships)

**4.** "List all executives"
**Answer:** Text2Cypher (precise list)

**5.** "What challenges do tech companies face?"
**Answer:** Vector (exploratory content)

---

## Building Intelligent Applications

**Single-Retriever Apps:** Simple, focused use cases

**Multi-Retriever Apps:** More flexible, handles diverse questions

**Agent-Based Apps:** Automatically selects retriever based on question
- Analyzes question pattern
- Chooses appropriate retriever(s)
- Combines results intelligently
- Provides comprehensive answers

**Next Module:** Build agents that use all three retrievers!

---

## Summary

Choosing the right retriever is crucial for quality results:

**Key Decision Factors:**
- Content vs Facts
- Need for related entities
- Relationship traversal requirements
- Question pattern recognition

**Three Retrievers, Three Strengths:**
- Vector: Semantic content search
- Vector Cypher: Content + graph intelligence
- Text2Cypher: Precise facts and counts

**Best Practice:** Combine retrievers for comprehensive coverage

---

## Next Steps

You've completed Module 2: GraphRAG Retrievers!

**You now understand:**
- Vector Retriever for semantic search
- Vector Cypher Retriever for hybrid retrieval
- Text2Cypher Retriever for precise queries
- How to choose the right retriever for each question

**Next:** Module 3 - Build intelligent agents that use these retrievers as tools!
