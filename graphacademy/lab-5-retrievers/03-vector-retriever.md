# Vector Retriever

The Vector Retriever is the simplest and most fundamental retriever type in GraphRAG. It uses semantic similarity to find relevant text chunks based on the meaning of your query, not just keyword matching.

This lesson prepares you for Lab 5 Notebook 1, where you'll implement and test a Vector Retriever.

## What is a Vector Retriever?

A Vector Retriever:
1. Takes your natural language query
2. Converts it to an embedding (vector)
3. Searches a vector index for similar chunk embeddings
4. Returns the most semantically similar text chunks
5. Optionally feeds these chunks to an LLM for answer generation

**The Core Idea:** Find content by meaning, not exact keywords.

## How It Works

**Step-by-Step Process:**

```
User Query: "What are the risks that Apple faces?"
    ↓
1. EMBED THE QUERY
   [0.023, -0.015, 0.087, ...] (1536 dimensions)
    ↓
2. SEARCH VECTOR INDEX
   Find chunks with similar embeddings
    ↓
3. RETURN TOP MATCHES
   Chunk 1: "...the Company to potential liabilities..." (score: 0.9148)
   Chunk 2: "...required to provide relief..." (score: 0.9124)
   Chunk 3: "...frequency and sophistication..." (score: 0.9112)
    ↓
4. GENERATE ANSWER (optional)
   LLM uses retrieved chunks as context
```

## Vector Retriever Components

**1. Embedder**
Converts text to vectors using an embedding model (e.g., OpenAI's text-embedding-ada-002).

**2. Vector Index**
Neo4j vector index that enables fast similarity search across thousands of chunk embeddings.

**3. Similarity Function**
Compares vectors using cosine similarity (measures the angle between vectors).

**4. Top-K Parameter**
Controls how many results to return (e.g., top_k=5 returns the 5 most similar chunks).

## Creating a Vector Retriever

Using the `neo4j-graphrag` Python package:

```python
from neo4j_graphrag.retrievers import VectorRetriever

# Initialize the retriever
vector_retriever = VectorRetriever(
    driver=driver,                    # Neo4j connection
    index_name='chunkEmbeddings',     # Vector index name
    embedder=embedder,                 # Embedding model
    return_properties=['text']         # What to return from chunks
)
```

**Key Parameters:**
- `driver`: Your Neo4j database connection
- `index_name`: The vector index to search
- `embedder`: The model that converts queries to embeddings
- `return_properties`: Which chunk properties to include in results

## Performing a Vector Search

**Simple Search:**
```python
query = "What are the risks that Apple faces?"
results = vector_retriever.search(query_text=query, top_k=5)

for item in results.items:
    print(f"Score: {item.metadata['score']:.4f}")
    print(f"Content: {item.content}\n")
```

**What You Get:**
- `score`: Similarity score (0.0 to 1.0, higher is better)
- `content`: The text from the matching chunk
- `metadata`: Additional information like chunk ID

## Using GraphRAG for Answer Generation

The `GraphRAG` class combines retrieval with LLM generation:

```python
from neo4j_graphrag.generation import GraphRAG

# Create a GraphRAG pipeline
rag = GraphRAG(
    llm=llm,                           # Language model for generation
    retriever=vector_retriever         # Vector retriever for search
)

# Search and generate an answer
response = rag.search(
    query_text=query,
    retriever_config={"top_k": 5},    # Retriever parameters
    return_context=True                # Include retrieved chunks in response
)

print(response.answer)  # Generated answer
```

**The GraphRAG Pipeline:**
1. Retriever finds relevant chunks
2. Chunks are formatted as context
3. LLM generates an answer grounded in the retrieved context
4. Returns both the answer and the source chunks

## When Vector Retriever Works Best

**Ideal For:**
- **Semantic questions:** "What is Apple's strategy?"
- **Concept matching:** "Tell me about cybersecurity threats"
- **Topic exploration:** "What products does Microsoft offer?"
- **Content similarity:** Finding similar discussions across documents

**Strengths:**
- Finds content by meaning, not just keywords
- Works even when query words don't match document words
- Handles synonyms and paraphrasing naturally
- Fast and scalable with vector indexes

## Limitations of Vector Retriever

**What It Can't Do:**

**1. Specific Facts:**
```
Query: "How many risk factors does Apple face?"
Problem: Returns chunks about risks, but doesn't count them
```

**2. Relationships:**
```
Query: "Which companies are owned by BlackRock?"
Problem: Returns chunks mentioning BlackRock, but doesn't traverse relationships
```

**3. Comparisons:**
```
Query: "Which company faces the most risks?"
Problem: Can't compare across companies or aggregate data
```

**4. Structured Queries:**
```
Query: "List all products where name contains 'iPhone'"
Problem: Not designed for precise filtering or matching
```

## Vector Search Parameters

**top_k: Number of Results**
```python
results = vector_retriever.search(query_text=query, top_k=5)
```
- Higher top_k = more context but potentially less relevant results
- Lower top_k = more focused but might miss important context
- Typical values: 3-10 depending on your use case

**return_properties: What to Include**
```python
vector_retriever = VectorRetriever(
    driver=driver,
    index_name='chunkEmbeddings',
    embedder=embedder,
    return_properties=['text', 'index']  # Include chunk text and index
)
```

## Understanding Similarity Scores

Similarity scores help you evaluate result quality:

**Score Ranges:**
- **0.95-1.0:** Extremely similar (near-exact semantic match)
- **0.90-0.95:** Highly relevant (strong semantic similarity)
- **0.85-0.90:** Relevant (good match)
- **0.80-0.85:** Moderately relevant (partial match)
- **< 0.80:** Weak relevance (consider adjusting query or top_k)

**Example:**
```
Query: "What products does Apple make?"

Results:
Score: 0.9340 - "...smartphones, personal computers, tablets..."
Score: 0.9182 - "...iPhone...Mac...iPad..."
Score: 0.9140 - "...Services, AppleCare..."
```

High scores indicate the chunks strongly match the query's semantic meaning.

## Example Queries for Vector Retriever

**Good Vector Retriever Queries:**
- "What are the main risk factors mentioned in the documents?"
- "Summarize Apple's business strategy"
- "What cybersecurity threats do companies face?"
- "Tell me about Microsoft's cloud services"
- "What are the challenges in the semiconductor industry?"

**Poor Vector Retriever Queries:**
- "How many companies are in the database?" (needs Text2Cypher)
- "Which asset managers own Apple?" (needs graph traversal)
- "What is the exact revenue figure for Q3?" (needs precise extraction)
- "List all products alphabetically" (needs structured query)

## Check Your Understanding

### What does a Vector Retriever use to find relevant content?

**Options:**
- [ ] Keyword matching
- [ ] SQL-like queries
- [x] Semantic similarity of embeddings
- [ ] Regular expressions

<details>
<summary>Hint</summary>
Think about what "vector" means in the context of embeddings.
</details>

<details>
<summary>Show Answer</summary>
**Semantic similarity of embeddings**. The Vector Retriever converts both the query and the stored chunks into embeddings (vectors), then finds chunks with embeddings that are close to the query embedding in vector space. This allows it to find semantically similar content even when different words are used.
</details>

### When should you use a Vector Retriever instead of Text2Cypher?

**Options:**
- [ ] When you need to count nodes
- [x] When you want to find content about a concept or topic
- [ ] When you need exact property values
- [ ] When you want to list all entities of a type

<details>
<summary>Hint</summary>
Consider what kind of question focuses on finding relevant content by meaning.
</details>

<details>
<summary>Show Answer</summary>
**When you want to find content about a concept or topic**. Vector Retriever excels at semantic search - finding chunks that discuss a particular topic or concept, even if they don't use the exact words in your query. For counting, exact values, or listing entities, you'd use Text2Cypher instead.
</details>

## Summary

In this lesson, you learned about the Vector Retriever:

**Key Concepts:**
- Vector Retriever finds content by semantic similarity, not keywords
- Converts queries to embeddings and searches a vector index
- Returns the most similar chunks based on cosine similarity
- Can be combined with an LLM for answer generation using GraphRAG

**How It Works:**
- Query → Embedding → Vector Search → Results → (Optional) LLM Generation
- Uses the `VectorRetriever` class from neo4j-graphrag
- Configurable with top_k and return_properties
- Scores indicate similarity strength

**Best Used For:**
- Semantic questions about concepts and topics
- Finding content by meaning
- Exploring document collections
- When exact keywords aren't known

**Limitations:**
- Can't perform counts or aggregations
- Doesn't traverse graph relationships
- Not ideal for specific facts or comparisons
- Returns chunks, not structured answers

In Lab 5 Notebook 1, you'll implement a Vector Retriever and see how it performs semantic search across your knowledge graph. In the next lesson, you'll learn how to enhance it with graph traversal using the Vector Cypher Retriever.

---

**Navigation:**
- [← Previous: What is a Retriever](02-what-is-a-retriever.md)
- [↑ Back to Module 2](README.md)
- [Next: Vector Cypher Retriever →](04-vector-cypher-retriever.md)
