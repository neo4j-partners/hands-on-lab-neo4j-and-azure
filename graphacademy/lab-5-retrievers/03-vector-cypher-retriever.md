# Vector Cypher Retriever

The Vector Cypher Retriever combines semantic search with graph traversal. It finds relevant content (like Vector Retriever), then follows relationships to gather connected entities and structured data.

![A diagram showing the vector plus graph retrieval process](../images/llm-rag-vector+graph-process.svg)

## When to Use Vector Cypher Retriever

**Ideal for:**
- Questions needing both content and related entities
- Finding patterns across connected data
- Relationship-aware context enrichment
- Combining semantic relevance with graph structure

**Example questions:**
- "Which asset managers are affected by banking regulations?"
- "What products do tech companies discuss in risk sections?"
- "What companies share risks with Apple?"
- "Find discussions about AI and list the companies involved"

## How It Works

1. **Semantic search**: Find relevant chunks (same as Vector Retriever)
2. **Graph traversal**: Execute Cypher from those chunks to related entities
3. **Combine results**: Return both text content and structured entity data
4. **Generate answer**: LLM uses enriched context

**The key insight**: The chunk is your anchor. You can only traverse to entities connected to chunks that semantic search found.

## The Anchor Pattern

Understanding how Vector Cypher works requires understanding the anchor pattern:

```
User Query: "Which asset managers are affected by banking regulations?"
    ↓
Step 1: Vector search finds chunks about "banking regulations"
    ↓
Step 2: From those chunks, traverse to:
    - Documents containing those chunks
    - Companies that filed those documents
    - Asset managers that own those companies
    ↓
Result: Text about banking regulations + list of affected asset managers
```

**Critical point**: If vector search doesn't find chunks about banking regulations, the traversal has nowhere to start. The semantic search must succeed first.

## When It Works Well

**Good fit questions:**

| Question | Why It Works |
|----------|--------------|
| "Which asset managers own companies facing cyber risks?" | Finds cyber risk content → traverses to companies → asset managers |
| "What products do companies mention in risk sections?" | Finds risk content → traverses to companies → products |
| "Which companies share risks with Apple?" | Finds Apple-related content → traverses to shared risk factors → other companies |

In each case, semantic search finds relevant content, then graph traversal enriches it with connected entities.

## When It Struggles

**Questions where Vector Cypher has trouble:**

| Question | Problem |
|----------|---------|
| "What are Apple's risks?" (if Apple isn't in top results) | If no Apple-related chunks surface, can't traverse to Apple's risks |
| "Who owns Microsoft?" | This is a direct relationship query—Text2Cypher is better |
| "How many companies face cyber risks?" | Needs counting, not semantic search |

**The limitation**: Vector Cypher can only traverse from what semantic search retrieves. If your question doesn't naturally surface relevant chunks, the traversal won't reach the entities you need.

## Comparing Vector vs. Vector Cypher

| Feature | Vector | Vector Cypher |
|---------|--------|---------------|
| Finds relevant chunks | ✓ | ✓ |
| Semantic search | ✓ | ✓ |
| Graph traversal | ✗ | ✓ |
| Returns related entities | ✗ | ✓ |
| Relationship-aware | ✗ | ✓ |
| Complexity | Low | Medium |

**Use Vector** when you just need content.
**Use Vector Cypher** when you need content AND connected entities.

## The Traversal Concept

The Cypher query in Vector Cypher Retriever starts from the chunks found by semantic search and traverses outward:

```
Found Chunk → Document → Company → Asset Manager
     ↓
  Content about    Who filed it   Who owns them
  regulations
```

This pattern lets you answer questions that span semantic content and graph structure.

## Best Practices

**1. Match your question to the anchor pattern**

Good: "Which [entities] are affected by [topic]?"
- Semantic search finds chunks about [topic]
- Traversal reaches [entities] connected to those chunks

**2. Understand what must surface first**

If your question requires specific entity data, make sure the semantic search will find chunks related to those entities.

**3. Consider Text2Cypher for direct relationship queries**

"Who owns Microsoft?" doesn't need semantic search—it's a direct graph query. Use Text2Cypher.

## Check Your Understanding

### What makes Vector Cypher different from Vector Retriever?

**Options:**
- [ ] Uses a different embedding model
- [ ] Searches a different index
- [x] Adds graph traversal to semantic search results
- [ ] Returns more chunks

<details>
<summary>Hint</summary>
Think about what "Cypher" adds to the retrieval process.
</details>

<details>
<summary>Show Answer</summary>
**Adds graph traversal to semantic search results**. Vector Cypher performs semantic search (like Vector Retriever), then executes Cypher queries starting from the found chunks to traverse relationships and gather connected entities.
</details>

## Summary

- **Vector Cypher Retriever** combines semantic search with graph traversal
- **Best for** questions needing content + related entities
- **Anchor pattern**: Semantic search finds chunks; traversal extends from there
- **Key insight**: Can only traverse from what semantic search finds
- **Trade-off**: More powerful than Vector, but depends on semantic search succeeding

In the next lesson, you'll learn about Text2Cypher Retriever for precise, fact-based queries that bypass semantic search entirely.

---

**Navigation:**
- [← Previous: Vector Retriever](02-vector-retriever.md)
- [↑ Back to Lab 5](README.md)
- [Next: Text2Cypher Retriever →](04-text2cypher-retriever.md)
