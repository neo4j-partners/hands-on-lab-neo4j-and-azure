# Vectors

## What is a Vector?

Vectors are simply a list of numbers.

The vector `[1, 2, 3]` is a list of three numbers and could represent a point in three-dimensional space.

You can use vectors to represent many different types of data, including text, images, and audio.

![A diagram showing a 3d representation of the x,y,z coordinates 1,1,1 and 1,2,3](../images/3d-vector.svg)

## Vectors in the Real World

* 3D space
* Navigation
* Calculations with external forces
* And many other uses!

![a diagram showing an airplane in 3D space, with vectors representing its position and direction](../images/vector-airplane.png)

## What are embeddings?

_Embeddings are numerical translations of data objects, for example images, text, or audio, represented as vectors. This way, LLM algorithms will be able to compare two different text paragraphs by comparing their numerical representations._

* A type of data compression
* Transform messy data into compact format
* Numeric vectors with 100s or 1000s of elements

## "apple"

You can use an embedding model to turn words and phrases into vectors:

```
[
  -0.0023064255,
  -0.009327292,
  -0.0028842222,
  -0.025206208,
  -0.031195037,
  -0.015127062,
  -0.0067710704,
  0.021772403,
  -0.018287908,
  -0.013451733,
  ...]
```

## Similarity Search

Semantic search aims to understand search phrases' intent and contextual meaning.

Are you searching about the fruit, the tech company, or something else?

![A diagram showing the different meanings for the word "apple"](../images/Apple-tech-or-fruit.png)

## Similarity Search

You can use the _distance_ or _angle_ between vectors to find similar data.

Words with similar meanings or contexts will have vectors that are close together, while unrelated words will be farther apart.

![A 3 dimensional chart illustrating the distance between vectors. The vectors are for the words "apple" and "fruit"](../images/vector-distance.svg)

## Knowledge Graphs and Vectors

Vectors and embeddings can be used to facilitate similarity search in knowledge graphs.

![A graph data model showing the relationship between chunks that have embeddings, the documents, and the company they relate to.](../images/document-chunk-data-model.svg)

## Create embeddings

You can use Cypher to create an embedding for a chunk of text:

```cypher
WITH genai.vector.encode(
    "Create an embedding for this text",
    "OpenAI",
    { token: "sk-..." }) AS embedding
RETURN embedding
```

> **IMPORTANT: OpenAI API Key**
>
> You need to replace `sk-...` with your OpenAI API key.

## Search a vector index

You can search a vector index to find similar chunks of text.

```cypher
WITH genai.vector.encode(
    "What is the latest with Apple Inc?",
    "OpenAI",
    { token: "sk-..." }) AS embedding
CALL db.index.vector.queryNodes('chunkEmbeddings', 6, embedding)
YIELD node, score
RETURN node.text, score
```

## Traverse the graph

From the results of the vector search, you can traverse the graph to find related entities:

```cypher
WITH genai.vector.encode(
    "Whats the latest with Apple Inc?",
    "OpenAI",
    { token: "sk-..." }) AS embedding
CALL db.index.vector.queryNodes('chunkEmbeddings', 6, embedding)
YIELD node, score
MATCH (node)<-[:FROM_CHUNK]-(entity)
RETURN node.text, score, collect(entity.name) AS entities
```

## Summary

In this lesson, you learned about vectors and embeddings for semantic search:

**Key Concepts:**

- Vectors are numerical representations that enable semantic similarity search
- Embeddings transform text into high-dimensional vectors that capture meaning and context
- Neo4j can store vectors alongside graph data for hybrid retrieval
- Vector indexes enable fast similarity search across large document collections

**Practical Applications:**

- Create embeddings for text chunks using OpenAI's embedding API
- Store embeddings in Neo4j with vector indexes for efficient search
- Combine vector similarity with graph traversal for contextual retrieval
- Use semantic search to find relevant content even when exact keywords don't match

**What You Can Do:**

- Search for similar content based on meaning, not just keywords
- Find relevant document chunks that relate to your query semantically
- Traverse from retrieved chunks to related entities in the knowledge graph
- Enable more intelligent, context-aware search capabilities

In the next module, you will learn how to build different types of retrievers that combine vector search with graph traversal for powerful GraphRAG applications.

---

**Navigation:**
- [← Previous: Entity Resolution](07-entity-resolution.md)
- [↑ Back to Module 1](README.md)
- [Next: Working with Full Datasets →](09-full-dataset.md)
