# Entity Resolution

When the entities are identified in the text and subsequently created in the knowledge graph, they may not be unique. For example, the text may refer to `Neo4j` in some places and `Neo4j Graph Database` in others.

The default entity resolution strategy in the `SimpleKGBuilder` is to merge entities that have the same label and identical `name` property.

## No Entity Resolution

You can disable entity resolution by setting the `perform_entity_resolution` parameter to `False` when creating the `SimpleKGBuilder` instance.

Disabling entity resolution will result in all identified entities being created as new nodes.

> **IMPORTANT: Multiple nodes for the same entity**
>
> This may lead to multiple nodes representing the same real-world entity.

## Post Processing Entity Resolution

The `neo4j_graphrag` library includes additional [entity resolver components](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html#entity-resolver). The entity resolvers are used after the creation of the knowledge graph to identify and merge duplicate entities.

For example:

* The [`SpacySemanticMatchResolver`](https://neo4j.com/docs/neo4j-graphrag-python/current/api.html#spacysemanticmatchresolver) uses the [`spaCy`](https://spacy.io/) library to find and resolve entities with the same label and similar set of textual properties.
* The [`FuzzyMatchResolver`](https://neo4j.com/docs/neo4j-graphrag-python/current/api.html#fuzzymatchresolver) finds and resolves entities with the same label and similar set of textual properties using [RapidFuzz](https://rapidfuzz.github.io/RapidFuzz/) for fuzzy matching.

Post processing of entities can result in a more concise knowledge graph with fewer duplicate entities but with the risk of incorrectly merging distinct entities.

Refer to the [Entity Resolver documentation](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html#entity-resolver) for more information and how to use them.

When you're ready you can continue.

## Lesson Summary

In this lesson, you learned about entity resolution strategies.

In the next lesson, you will learn how to use and configure different LLMs.

---

**Navigation:**
- [← Previous: Optimizing Chunk Size](06-chunking.md)
- [↑ Back to Module 1](README.md)
- [Next: Vectors →](08-vectors.md)
