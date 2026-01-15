# Vectors and Semantic Search

## What is a Vector?

Vectors are lists of numbers. A simple vector like `[1, 2, 3]` represents a point in three-dimensional space.

![A diagram showing a 3d representation of the x,y,z coordinates 1,1,1 and 1,2,3](../images/3d-vector.svg)

In machine learning, vectors can represent much more complex data—including the *meaning* of text.

## What are Embeddings?

Embeddings are numerical representations of data—text, images, or audio—encoded as vectors. For text, embedding models convert words, sentences, or paragraphs into high-dimensional vectors (often 1,536 dimensions for models like OpenAI's text-embedding-ada-002).

The key property: **similar meanings produce similar vectors**.

"Apple's business strategy" and "the company's strategic approach" have different words but similar meanings. Their embeddings will be close together in vector space.

"Apple's business strategy" and "banana nutrition facts" have unrelated meanings. Their embeddings will be far apart.

This property enables **semantic search**—finding content by meaning, not just keywords.

![A diagram showing the different meanings for the word "apple"](../images/Apple-tech-or-fruit.png)

## Why Vectors Matter for GraphRAG

Your knowledge graph now has:
- Structured entities (companies, risks, products)
- Relationships (FACES_RISK, OWNS, MENTIONS)
- Text chunks from source documents

But how do you *find* relevant information when a user asks a question?

**Without vectors**: You'd need exact keyword matches. "What challenges does Apple face?" wouldn't find chunks about "risks" or "threats."

**With vectors**: The question and chunks become embeddings. You find chunks with similar *meaning*, regardless of exact words.

This is the foundation of semantic search in GraphRAG.

## Similarity Search

Vector similarity is typically measured by **cosine similarity**—the angle between two vectors:

- **Score near 1.0**: Very similar meanings
- **Score near 0.5**: Somewhat related
- **Score near 0.0**: Unrelated

When you search:
1. Your question becomes an embedding
2. The system finds chunks with embeddings close to your question
3. Those chunks (and their graph connections) become context for the LLM

## Storing Vectors in Neo4j

Neo4j can store embeddings as properties on nodes and create vector indexes for fast similarity search.

When SimpleKGPipeline processes documents:
1. Each chunk gets an embedding from the embedding model
2. The embedding is stored as a property on the Chunk node
3. A vector index enables fast similarity search across all chunks

```cypher
// Chunks have embedding properties
MATCH (c:Chunk)
RETURN c.text, size(c.embedding) AS embeddingDimensions
LIMIT 1
```

## Searching a Vector Index

Cypher can search vector indexes to find similar content:

```cypher
// Create an embedding for the query
WITH genai.vector.encode(
    "What risks does Apple face?",
    "OpenAI",
    { token: $apiKey }
) AS queryEmbedding

// Search the vector index for similar chunks
CALL db.index.vector.queryNodes('chunkEmbeddings', 5, queryEmbedding)
YIELD node, score

RETURN node.text AS content, score
ORDER BY score DESC
```

This finds the 5 chunks most semantically similar to "What risks does Apple face?"—even if they don't contain the exact words "risks" or "Apple."

## Combining Vectors with Graph Traversal

The real power of GraphRAG: start with semantic search, then traverse the graph for connected entities.

```cypher
// Find semantically similar chunks
WITH genai.vector.encode(
    "What risks does Apple face?",
    "OpenAI",
    { token: $apiKey }
) AS queryEmbedding

CALL db.index.vector.queryNodes('chunkEmbeddings', 5, queryEmbedding)
YIELD node, score

// Traverse to connected entities
MATCH (node)<-[:FROM_CHUNK]-(entity)
RETURN node.text AS content, score, collect(entity.name) AS relatedEntities
```

This returns not just similar text, but the entities extracted from that text—giving the LLM both unstructured content and structured data.

## The Complete Knowledge Graph

Your knowledge graph now has everything needed for GraphRAG:

| Component | Purpose |
|-----------|---------|
| **Documents** | Source provenance |
| **Chunks** | Searchable text units |
| **Embeddings** | Enable semantic search |
| **Entities** | Structured domain knowledge |
| **Relationships** | Connections between entities |

This structure enables three retrieval patterns:
1. **Vector search**: Find semantically similar content
2. **Vector + Graph**: Find similar content, then traverse to related entities
3. **Text2Cypher**: Query the graph structure directly

You'll learn these patterns in detail in Lab 5.

## Check Your Understanding

### What do vector embeddings enable in GraphRAG?

**Options:**
- [ ] Faster database writes
- [ ] Smaller storage requirements
- [x] Finding content by meaning, not just keywords
- [ ] Automatic entity extraction

<details>
<summary>Hint</summary>
Think about what embeddings represent and how similarity works.
</details>

<details>
<summary>Show Answer</summary>
**Finding content by meaning, not just keywords**. Embeddings capture semantic meaning, so similar concepts have similar vectors. This enables semantic search—finding relevant content even when the exact words don't match. "Challenges" can find "risks" and "threats" because they have similar meanings.
</details>

## Summary

In this lesson, you learned:

- **Vectors** are numerical representations of data
- **Embeddings** encode text meaning as high-dimensional vectors
- **Similar meanings** produce similar vectors, enabling semantic search
- **Neo4j stores vectors** alongside graph data with vector indexes
- **Semantic search** finds relevant chunks by meaning, not keywords
- **Vector + Graph** combines semantic search with relationship traversal

Your knowledge graph is complete:
- Structured entities and relationships (from schema-driven extraction)
- Appropriately sized chunks (from chunking strategy)
- Resolved entities (from entity resolution)
- Vector embeddings (enabling semantic search)

In Lab 5, you'll learn how to retrieve context from this knowledge graph using three distinct retrieval patterns: Vector, Vector Cypher, and Text2Cypher.

---

**Navigation:**
- [← Previous: Entity Resolution](06-entity-resolution.md)
- [↑ Back to Lab 5](README.md)
- [Next: Lab 6 - GraphRAG Retrievers →](../lab-6-retrievers/README.md)
