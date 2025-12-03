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


# Optimizing Chunk Size

Module 1, Lesson 6

---

## The Role of Chunks in Knowledge Graphs

The graph created by the `SimpleKGPipeline` is based on **chunks of text** extracted from documents.

**Chunk size matters because:**
- It determines how much context the LLM has for entity extraction
- It affects the granularity of extracted data
- It impacts the number of chunks and their relationships
- It influences retrieval quality and performance

---

## Default Chunk Size Behavior

By default, the chunk size is quite large:

**Large Chunks:**
- ✅ More context for the LLM
- ✅ Better understanding of relationships
- ❌ Less granular data
- ❌ Fewer, broader chunks

**Finding the right balance is critical!**

---

## The Chunk Size Trade-Off

<div style="display: flex; gap: 2rem;">

<div style="flex: 1;">

### Larger Chunks

**Advantages:**
- More context for entity extraction
- Better relationship understanding
- Fewer chunks to manage

**Disadvantages:**
- Less granular results
- Broader, less specific retrieval
- May mix unrelated topics

</div>

<div style="flex: 1;">

### Smaller Chunks

**Advantages:**
- More granular, focused data
- Precise retrieval results
- Better topic separation

**Disadvantages:**
- Less context for extraction
- May miss relationships
- More chunks to process

</div>

</div>

---

## Configuring Chunk Size

Use the `FixedSizeSplitter` to control chunk size:

```python
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter

# Create a text splitter with custom chunk size
text_splitter = FixedSizeSplitter(
    chunk_size=500,      # Maximum characters per chunk
    chunk_overlap=100    # Overlap between chunks
)

# Pass to SimpleKGPipeline
kg_builder_pdf = SimpleKGPipeline(
    llm=llm,
    driver=driver,
    embedder=embedder,
    text_splitter=text_splitter,  # Use custom splitter
    from_pdf=True
)
```

---

## Chunk Overlap Strategy

The `chunk_overlap` parameter ensures continuity between chunks:

**Why Overlap Matters:**
- Maintains context across chunk boundaries
- Prevents entity splitting at chunk edges
- Helps preserve relationship extraction
- Ensures smooth retrieval continuity

**Typical Overlap:**
- 10-20% of chunk size is common
- 100-200 characters for 500-1000 char chunks

---

## Viewing Chunks in Your Graph

After creating the knowledge graph, inspect the chunks:

```cypher
// View all documents and their chunks
MATCH (d:Document)<-[:FROM_DOCUMENT]-(c:Chunk)
RETURN d.path, c.index, c.text
ORDER BY d.path, c.index
```

**What to look for:**
- Are chunks the right size for your domain?
- Do they contain complete thoughts/concepts?
- Is there appropriate overlap?

---

## Experimenting with Chunk Sizes

Try different chunk sizes to optimize for your use case:

**Small (200-300 chars):**
- Good for: Precise entity extraction, focused retrieval
- Use when: Documents have dense, distinct topics

**Medium (500-800 chars):**
- Good for: Balanced context and granularity
- Use when: General-purpose knowledge graphs

**Large (1000-1500 chars):**
- Good for: Rich context, complex relationships
- Use when: Entities span multiple sentences

---

## Impact on Entity Extraction

View entities extracted from chunks:

```cypher
// View entities and their source chunks
MATCH p = (c:Chunk)-[*..3]-(e:__Entity__)
RETURN p
```

**Observe:**
- How many entities per chunk?
- Are relationships captured correctly?
- Is granularity appropriate?

---

## Best Practices for Chunk Sizing

**Consider Your Domain:**
- Technical documents → Larger chunks (more context)
- News articles → Smaller chunks (focused topics)
- SEC filings → Medium chunks (balanced)

**Test and Iterate:**
1. Start with default size
2. Examine results
3. Adjust based on entity quality
4. Re-run pipeline with new size
5. Compare results

---

## Cleaning Up Before Experimenting

To test different chunk sizes, delete the existing graph:

```cypher
// Delete the entire graph for fresh start
MATCH (n) DETACH DELETE n
```

**Then:**
1. Modify chunk size parameters
2. Re-run the pipeline
3. Compare results with previous version
4. Choose optimal configuration

---

## Summary

Chunk size optimization is crucial for knowledge graph quality:

**Key Takeaways:**
- Larger chunks = more context, less granularity
- Smaller chunks = more granularity, less context
- Use `FixedSizeSplitter` for custom chunk sizes
- Chunk overlap maintains continuity
- Experiment to find the right balance for your domain

**The optimal chunk size depends on your documents and use case.**

---

## Next Steps

In the next lesson, you will learn about entity resolution strategies to handle duplicate entities in your knowledge graph.
