# Entity Resolution

## The Duplicate Entity Problem

When entities are extracted from text, they may not be unique. The same real-world entity can appear with different names:

- "Neo4j" vs "Neo4j Graph Database" vs "Neo4j, Inc."
- "Apple" vs "Apple Inc" vs "Apple Inc." vs "the Company"
- "Tim Cook" vs "Timothy Cook" vs "CEO Tim Cook"

Without resolution, your graph contains multiple nodes representing the same thing. This breaks queries:

```cypher
// This might miss risks if Apple appears under different names
MATCH (c:Company {name: 'Apple Inc'})-[:FACES_RISK]->(r:RiskFactor)
RETURN r.name
```

If some risks are connected to "Apple" and others to "APPLE INC", your query returns incomplete results.

## Why Entity Resolution Matters

Entity resolution ensures:

- **Query accuracy**: One node per real-world entity
- **Relationship completeness**: All relationships connect to the canonical entity
- **Aggregation correctness**: Counts and summaries reflect reality

Without resolution, you can't trust basic queries like "How many risk factors does Apple face?"

## Default Resolution in SimpleKGPipeline

By default, `SimpleKGPipeline` performs basic resolution:

- Entities with the **same label** and **identical name** are merged
- "Company: Apple Inc" + "Company: Apple Inc" = one node

This catches exact duplicates but misses variations:
- "Apple Inc" and "APPLE INC" (case difference)
- "Apple Inc" and "Apple Inc." (punctuation)
- "Apple" and "Apple Inc" (name variation)

## Disabling Resolution

You can disable entity resolution entirely:

```python
pipeline = SimpleKGPipeline(
    driver=driver,
    llm=llm,
    embedder=embedder,
    entities=entities,
    relations=relations,
    perform_entity_resolution=False,  # No resolution
)
```

This creates separate nodes for every extracted entity mention. Useful for:
- Debugging extraction to see all variations
- Later applying custom resolution logic
- Understanding how entities appear in source text

## Post-Processing Resolution

For more sophisticated matching, `neo4j-graphrag` provides entity resolvers that run *after* graph construction:

**SpacySemanticMatchResolver**: Uses spaCy NLP to find entities with similar textual properties. Good for catching semantic similarities.

**FuzzyMatchResolver**: Uses string similarity (via RapidFuzz) to catch typos, abbreviations, and minor variations.

These resolvers:
1. Find candidate duplicate nodes
2. Compute similarity scores
3. Merge nodes above a threshold

## Resolution Trade-offs

Entity resolution involves a fundamental trade-off:

**Too Aggressive:**
- "Apple Inc" (tech company) merged with "Apple Records" (music label)
- Distinct entities incorrectly combined
- Relationships become meaningless

**Too Conservative:**
- "Apple Inc" and "APPLE INC" remain separate
- Queries miss connections
- Aggregations are wrong

The right balance depends on your domain. For SEC filings with a known set of companies, aggressive resolution to canonical names works well. For general documents with many similar-named entities, conservative resolution avoids false merges.

## Resolution Strategies

**Strategy 1: Upstream Normalization**

Handle resolution during extraction by guiding the LLM:

```python
prompt_template = """
When extracting company names, normalize to official names:
- "Apple", "Apple Inc", "Apple Inc.", "the Company" → "APPLE INC"
- Use uppercase for company names
- Use the full legal name when known
"""
```

This produces cleaner extraction, reducing the need for post-processing.

**Strategy 2: Reference Lists**

Provide a canonical list of entities:

```python
prompt_template = """
Only extract companies from this approved list:
- APPLE INC
- MICROSOFT CORP
- ALPHABET INC

Match variations to the canonical name.
"""
```

This works well when you know the entities in advance.

**Strategy 3: Post-Processing Resolvers**

Apply resolvers after extraction:

```python
from neo4j_graphrag.experimental.components.entity_resolvers import FuzzyMatchResolver

resolver = FuzzyMatchResolver(
    driver=driver,
    similarity_threshold=0.85,  # How similar names must be to merge
)

# Run after pipeline completion
resolver.resolve()
```

This catches variations the LLM missed.

## Validating Resolution

After resolution, verify your entity counts:

```cypher
// Check for potential duplicates
MATCH (c:Company)
WITH c.name AS name, collect(c) AS nodes
WHERE size(nodes) > 1
RETURN name, size(nodes) AS duplicates

// Check company name variations
MATCH (c:Company)
WHERE c.name CONTAINS 'Apple' OR c.name CONTAINS 'APPLE'
RETURN c.name, count{(c)-[:FACES_RISK]->()}  AS risks
```

Look for:
- Multiple nodes with similar names
- Low relationship counts (might indicate split entities)
- Unexpected entity variations

## Check Your Understanding

### What happens if entity resolution is too aggressive?

**Options:**
- [ ] The graph has too many nodes
- [ ] Queries become slower
- [x] Distinct entities are incorrectly merged together
- [ ] Relationships are duplicated

<details>
<summary>Hint</summary>
Think about what happens if two different real-world entities have similar names.
</details>

<details>
<summary>Show Answer</summary>
**Distinct entities are incorrectly merged together**. If resolution is too aggressive, entities like "Apple Inc" (technology) and "Apple Records" (music) might be merged into one node, making the graph incorrect. All relationships from both entities would connect to a single, conflated node.
</details>

## Summary

In this lesson, you learned:

- **Entity resolution** merges duplicate nodes representing the same real-world entity
- **Default resolution** catches exact matches only
- **Post-processing resolvers** catch variations using semantic or fuzzy matching
- **The trade-off**: Too aggressive merges distinct entities; too conservative keeps duplicates
- **Strategies include**: Upstream normalization, reference lists, post-processing resolvers

With schema, chunking, and entity resolution addressed, your graph has structured entities and relationships. The final piece is enabling semantic search—that's where vectors come in.

---

**Navigation:**
- [← Previous: Chunking Strategies](05-chunking.md)
- [↑ Back to Lab 3](README.md)
- [Next: Vectors and Semantic Search →](07-vectors.md)
