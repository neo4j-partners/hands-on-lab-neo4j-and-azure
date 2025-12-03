# Chunking Strategies

## Why Chunking Matters

LLMs have context limits. You can't pass an entire 200-page SEC filing to an LLM for entity extraction. Documents must be broken into smaller pieces—**chunks**—that fit within processing limits.

But chunking isn't just a technical necessity. How you chunk documents affects both **extraction quality** and **retrieval quality**.

## The Dual Impact of Chunk Size

Chunk size creates a fundamental trade-off:

**For Entity Extraction:**
- Larger chunks provide more context for understanding entities and relationships
- The LLM sees more surrounding text, making better extraction decisions
- "The Company" can be resolved to "Apple Inc" when the full context is visible

**For Retrieval:**
- Smaller chunks enable more precise matches
- When searching, you want to return the most relevant *portion*, not a huge blob
- Smaller chunks mean less irrelevant content mixed with relevant content

The same chunk size can't optimize both. You need to find the right balance for your use case.

## Chunk Size Parameters

The `FixedSizeSplitter` in neo4j-graphrag has two key parameters:

**`chunk_size`**: Maximum number of characters per chunk

```python
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter

splitter = FixedSizeSplitter(chunk_size=500)
```

**`chunk_overlap`**: Characters shared between consecutive chunks

```python
splitter = FixedSizeSplitter(chunk_size=500, chunk_overlap=50)
```

Overlap ensures context isn't lost at chunk boundaries. If an important sentence spans two chunks, overlap increases the chance both chunks capture the full meaning.

## The Trade-off Illustrated

**Large Chunks (e.g., 2000 characters):**
```
Chunk 1: [Full paragraph about Apple's risk factors, mentioning cybersecurity,
          supply chain, and regulatory risks with full context about each]
```
- ✓ Better entity extraction (full context)
- ✗ Less precise retrieval (returns more than needed)
- ✗ Fewer chunks to search across

**Small Chunks (e.g., 200 characters):**
```
Chunk 1: [Apple faces cybersecurity risks including...]
Chunk 2: [Supply chain disruptions could impact...]
Chunk 3: [Regulatory changes in key markets...]
```
- ✗ Worse entity extraction (less context)
- ✓ More precise retrieval (each chunk is focused)
- ✓ More granular search results

## Typical Chunk Sizes

There's no universal "correct" chunk size, but common ranges:

| Chunk Size | Best For |
|------------|----------|
| 200-500 chars | High-precision retrieval, FAQ-style content |
| 500-1000 chars | Balanced extraction and retrieval |
| 1000-2000 chars | Context-heavy extraction, narrative documents |
| 2000+ chars | Maximum context, fewer chunks |

For SEC filings with complex, interconnected information, 500-1000 characters often provides a good balance.

## Configuring the Pipeline

To use a custom text splitter with SimpleKGPipeline:

```python
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter

# Create a splitter with your preferred settings
splitter = FixedSizeSplitter(chunk_size=500, chunk_overlap=50)

# Pass it to the pipeline
pipeline = SimpleKGPipeline(
    driver=driver,
    llm=llm,
    embedder=embedder,
    entities=entities,
    relations=relations,
    text_splitter=splitter,  # Custom splitter
)
```

## Evaluating Chunk Quality

After chunking, evaluate the results:

```cypher
// Check chunk count per document
MATCH (d:Document)<-[:FROM_DOCUMENT]-(c:Chunk)
RETURN d.path, count(c) AS chunkCount
ORDER BY chunkCount DESC

// Check chunk size distribution
MATCH (c:Chunk)
RETURN
    min(size(c.text)) AS minSize,
    max(size(c.text)) AS maxSize,
    avg(size(c.text)) AS avgSize

// Sample chunk content
MATCH (c:Chunk)
RETURN c.text
LIMIT 5
```

Look for:
- Reasonable chunk counts per document
- Consistent chunk sizes
- Chunks that contain coherent, complete thoughts

## Chunking and Retrieval Interaction

Remember: chunks become searchable units. When a user asks a question:

1. The question becomes an embedding
2. The system finds chunks with similar embeddings
3. Those chunks (and their connected entities) become context

If your chunks are too large, retrieval returns more irrelevant content. If they're too small, important context might be split across chunks.

## Experiment and Iterate

The best chunk size depends on:
- Document type and structure
- Query patterns you expect
- Balance between extraction and retrieval needs

Start with a moderate size (500-800 characters), evaluate results, and adjust based on:
- Entity extraction quality
- Retrieval relevance
- Query response quality

## Check Your Understanding

### What is the primary trade-off when choosing chunk size?

**Options:**
- [ ] Larger chunks process faster but use more memory
- [x] Larger chunks provide more context for extraction but less precise retrieval
- [ ] Smaller chunks are always better for all use cases
- [ ] Chunk size only affects storage requirements

<details>
<summary>Hint</summary>
Think about what happens during entity extraction vs. during retrieval search.
</details>

<details>
<summary>Show Answer</summary>
**Larger chunks provide more context for extraction but less precise retrieval**. The LLM needs context to understand entities and relationships, favoring larger chunks. But retrieval benefits from smaller, focused chunks that match queries precisely. This trade-off is fundamental to chunking strategy.
</details>

## Summary

In this lesson, you learned:

- **Chunking breaks documents** into processable pieces
- **Chunk size affects both** entity extraction quality and retrieval precision
- **Larger chunks** = better context for extraction, less precise retrieval
- **Smaller chunks** = more precise retrieval, less context for extraction
- **Overlap** helps preserve context across chunk boundaries
- **Experimentation** is key to finding the right balance

Even with good chunking, the same entity might appear with different names in different chunks. In the next lesson, you'll learn about entity resolution—handling duplicate entities.

---

**Navigation:**
- [← Previous: Schema Design](04-schema-design.md)
- [↑ Back to Lab 3](README.md)
- [Next: Entity Resolution →](06-entity-resolution.md)
