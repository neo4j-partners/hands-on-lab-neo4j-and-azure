# Vector Retriever

The Vector Retriever finds content by semantic similarity—matching the *meaning* of your question to the meaning of stored content, even when the exact words differ.

![A diagram showing vector similarity distance between embeddings](../images/vector-distance.svg)

## When to Use Vector Retriever

**Ideal for:**
- Conceptual questions about topics
- Content exploration and discovery
- Questions where you don't know the exact terminology
- Finding discussions, explanations, or descriptions

**Example questions:**
- "What is Apple's business strategy?"
- "Tell me about cybersecurity threats"
- "What challenges do tech companies face?"
- "Summarize Microsoft's approach to cloud computing"

## How It Works

1. **Embed the query**: Your question becomes a vector embedding (1,536 dimensions with OpenAI models)
2. **Search the index**: Find chunks with embeddings close to your query
3. **Return matches**: Return the most semantically similar chunks
4. **Generate answer**: LLM uses these chunks as context

The key insight: **similar meanings produce similar vectors**. "What challenges does Apple face?" finds chunks about "risks," "threats," and "obstacles"—because these concepts have similar embeddings.

## Strengths

- **Finds meaning, not keywords**: Synonyms and paraphrases work naturally
- **Handles unknown terminology**: You don't need to know exact terms in the documents
- **Fast and scalable**: Vector indexes enable efficient similarity search
- **Flexible**: Works across different topics and domains

## Limitations

- **Can't count or aggregate**: "How many companies?" returns chunks mentioning companies, not a count
- **No relationship traversal**: Can't follow graph connections to related entities
- **Returns text only**: No structured data about entities
- **May miss precision**: "What products does Apple sell?" returns text about products, not a clean list

## Example Questions: Good vs. Poor Fit

**Good fit for Vector Retriever:**
| Question | Why It Works |
|----------|--------------|
| "What are the main risk factors?" | Seeks semantic content about risks |
| "Tell me about AI technology" | Exploratory, topic-based |
| "What does Microsoft say about competition?" | Content search within documents |
| "Summarize Apple's approach to privacy" | Needs contextual understanding |

**Poor fit for Vector Retriever:**
| Question | Why It Struggles | Better Retriever |
|----------|------------------|------------------|
| "How many companies are there?" | Needs counting | Text2Cypher |
| "Which companies does BlackRock own?" | Needs relationship traversal | Text2Cypher |
| "List all asset managers" | Needs structured query | Text2Cypher |
| "What risks connect Apple and Microsoft?" | Needs graph relationships | Vector Cypher |

## Understanding Similarity Scores

Results include similarity scores (0.0 to 1.0):

| Score Range | Meaning |
|-------------|---------|
| 0.95-1.0 | Extremely similar (near-exact match) |
| 0.90-0.95 | Highly relevant |
| 0.85-0.90 | Relevant |
| 0.80-0.85 | Moderately relevant |
| < 0.80 | Weak relevance |

Higher scores indicate stronger semantic matches.

## The top_k Parameter

Controls how many results to return:

- **Lower top_k (3-5)**: More focused, potentially missing relevant content
- **Higher top_k (10-20)**: More comprehensive, potentially including less relevant content
- **Typical range**: 5-10 for most use cases

Balance between relevance and coverage based on your needs.

## When to Move Beyond Vector

If your question needs any of these, consider Vector Cypher or Text2Cypher:

- **Specific entity lookups**: "What products does Apple sell?"
- **Counting**: "How many risk factors?"
- **Relationships**: "Who owns Microsoft?"
- **Comparisons**: "Which company has the most risks?"
- **Lists**: "List all asset managers"

Vector Retriever finds *relevant content*. For *structured answers*, you need different tools.

## Check Your Understanding

### What does Vector Retriever use to find relevant content?

**Options:**
- [ ] Keyword matching
- [ ] SQL queries
- [x] Semantic similarity of embeddings
- [ ] Regular expressions

<details>
<summary>Hint</summary>
Think about what "vector" means in this context.
</details>

<details>
<summary>Show Answer</summary>
**Semantic similarity of embeddings**. The Vector Retriever converts both query and chunks into embeddings (vectors), then finds chunks with similar vectors. This enables finding content by meaning, not exact keywords.
</details>

## Summary

- **Vector Retriever** finds content by semantic similarity
- **Best for** conceptual questions, topic exploration, content discovery
- **Works by** embedding queries and finding similar chunks
- **Strengths**: Meaning-based search, handles synonyms, fast
- **Limitations**: Can't count, traverse relationships, or return structured data

In the next lesson, you'll learn how Vector Cypher Retriever extends semantic search with graph traversal for relationship-aware retrieval.

---

**Navigation:**
- [← Previous: Retrievers Overview](01-retrievers-overview.md)
- [↑ Back to Lab 5](README.md)
- [Next: Vector Cypher Retriever →](03-vector-cypher-retriever.md)
