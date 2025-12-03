# Schema Design

The knowledge graph you created is unconstrained, meaning that any entity or relationship can be created based on the data extracted from the text. This can lead to graphs that are non-specific and may be difficult to analyze and query.

In this lesson, you will modify the `SimpleKGPipeline` to use a custom schema for the knowledge graph.

## Schema

When you provide a schema to the `SimpleKGPipeline`, it will pass this information to the LLM instructing it to only identify those nodes and relationships. This allows you to create a more structured and meaningful knowledge graph.

You define a schema by expressing the desired nodes, relationships, or patterns you want to extract from the text.

For example, you might want to extract the following information:

* nodes - `Person`, `Organization`, `Location`
* relationships - `WORKS_AT`, `LOCATED_IN`
* patterns - `(Person)-[WORKS_AT]->(Organization)`, `(Organization)-[LOCATED_IN]->(Location)`

> **Iterate your schema**
>
> You don't have to define nodes, relationships, and patterns all at once. You can start with just nodes or just relationships and expand your schema as needed.
>
> For example, if you only define nodes, the LLM will find any relationships between those nodes based on the text.
>
> This approach can help you iteratively build and refine your knowledge graph schema.

## Nodes

Open `genai-graphrag-python/kg_builder_schema.py` and review the code.

You define the `NODES` as a list of node labels and pass the list to the `SimpleKGPipeline` when creating the pipeline instance.

> **Define relevant nodes**
>
> You should define the node labels that are relevant to your domain and the information you want to extract from the text.

You can also provide a description for each node label and associated properties to help guide the LLM when extracting entities.

Run the program to create the knowledge graph with the defined nodes.

> **Remember to delete the existing graph before re-running the pipeline**
>
> ```cypher
> // Delete the existing graph
> MATCH (n) DETACH DELETE n
> ```

The graph created will be constrained to only include the defined node labels.

```cypher
// View the entities extracted from each chunk
MATCH p = (c:Chunk)-[*..3]-(e:__Entity__)
RETURN p
```

## Relationships

You express required relationship types by providing a list of relationship types to the `SimpleKGPipeline`.

You can also provide patterns that define how nodes types are connected by relationships.

Nodes, relationships and patterns are all passed to the `SimpleKGPipeline` as the `schema` when creating the pipeline.

Review the `data/genai-fundamentals_1-generative-ai_1-what-is-genai.pdf` PDF document and experiment by creating a set of nodes, relationships and patterns relevant to the data.

## Process all the documents

When you are happy with the schema, you can modify the program to process all the PDF documents from the [Neo4j and Generative AI Fundamentals course](https://graphacademy.neo4j.com/courses/genai-fundamentals).

You can run the program to create a knowledge graph based on all the documents using the defined schema.

> **OpenAI Rate Limiting?**
>
> When using a free OpenAI API key, you may encounter rate limiting issues when processing multiple documents. You can add a `sleep` between document processing to mitigate this.

Review the knowledge graph and observe how the defined schema has influenced the structure of the graph.

```cypher
// Documents, Chunks, and Entity counts
RETURN
  count{ (:Document) } as documents,
  count{ (:Chunk) } as chunks,
  count{ (:__Entity__) } as entities
```

## Check Your Understanding

### Why would you define a schema when using the SimpleKGPipeline?

**Options:**
- [ ] To improve the performance and speed of data processing
- [ ] To reduce the computational resources required by the LLM
- [x] To create a more structured and meaningful knowledge graph by constraining entities and relationships
- [ ] To ensure that all possible entities and relationships are extracted from the text

<details>
<summary>Hint</summary>
Think about what happens when you don't provide a schema - the knowledge graph becomes unconstrained. What problems might this cause?
</details>

<details>
<summary>Show Answer</summary>
Defining a schema allows you to **create a more structured and meaningful knowledge graph by constraining entities and relationships** that are extracted. Without a schema, the knowledge graph is unconstrained, meaning any entity or relationship can be created, which can lead to graphs that are non-specific and difficult to analyze and query.
</details>

## Lesson Summary

In this lesson, you learned how to define a custom schema for the knowledge graph.

In the next lesson, you will learn how to add structured data to the knowledge graph.

---

**Navigation:**
- [← Previous: Building the Graph](04-building-the-graph.md)
- [↑ Back to Module 1](README.md)
- [Next: Optimizing Chunk Size →](06-chunking.md)
