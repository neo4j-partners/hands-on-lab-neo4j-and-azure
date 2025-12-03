# Optimizing Chunk Size

The graph created by the `SimpleKGPipeline` is based on chunks of text extracted from the documents. By default, the chunk size is quite large, which may result in fewer, larger chunks. The larger the chunk size, the more context the LLM has when extracting entities and relationships, but it may also lead to less granular data.

In this lesson, you will modify the `SimpleKGPipeline` to use a different chunk size.

## Delete the existing graph

You will be re-importing the data and modifying the existing graph. To ensure a clean state, you can delete the graph at any time using:

```cypher
// Delete the existing graph
MATCH (n) DETACH DELETE n
```

## Text Splitter Chunk Size

To modify the chunk size you will need to create a `FixedSizeSplitter` object and pass it to the `SimpleKGPipeline` when creating the pipeline instance:

1. Modify the `genai-graphrag-python/kg_builder.py` file to import the `FixedSizeSplitter` class and create an instance with a chunk size of 500 characters.

> **Chunk size and overlap**
>
> The `chunk_size` parameter defines the maximum number of characters in each text chunk. The `chunk_overlap` parameter ensures that there is some overlap between consecutive chunks, which can help maintain context.

2. Update the `SimpleKGPipeline` instantiation to use the custom text splitter.

Run the modified pipeline to recreate the knowledge graph with the new chunk size.

```cypher
// View the documents and chunks
MATCH (d:Document)<-[:FROM_DOCUMENT]-(c:Chunk)
RETURN d.path, c.index, c.text
ORDER BY d.path, c.index
```

You can experiment with different chunk sizes to see how it affects the entities extracted and the structure of the knowledge graph.

```cypher
// View the entities extracted from each chunk
MATCH p = (c:Chunk)-[*..3]-(e:__Entity__)
RETURN p
```

## Check Your Understanding

### What is the primary trade-off when increasing the chunk size in the SimpleKGPipeline?

**Options:**
- [ ] Larger chunks process faster but use more memory
- [x] Larger chunks provide more context for entity extraction but result in less granular data
- [ ] Larger chunks create more entities but fewer relationships
- [ ] Larger chunks improve accuracy but require more computational power

<details>
<summary>Hint</summary>
Consider what happens to the level of detail and context when you make text chunks bigger or smaller.
</details>

<details>
<summary>Show Answer</summary>
**Larger chunks provide more context for entity extraction but result in less granular data**. The larger the chunk size, the more context the LLM has when extracting entities and relationships, but it may also lead to less granular data. This is the key trade-off - more context versus granularity of the extracted information.
</details>

## Lesson Summary

In this lesson, you:

* Learned about the impact of chunk size on entity extraction
* Modified the `SimpleKGPipeline` to use a custom chunk size with the `FixedSizeSplitter`

In the next lesson, you will define a custom schema for the knowledge graph.

---

**Navigation:**
- [← Previous: Schema Design](05-schema-design.md)
- [↑ Back to Module 1](README.md)
- [Next: Entity Resolution →](07-entity-resolution.md)
