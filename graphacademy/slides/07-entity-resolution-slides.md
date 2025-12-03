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


# Entity Resolution

Module 1, Lesson 7

---

## The Entity Duplication Problem

When entities are extracted from text, they may not be unique.

**Common Issues:**
- Same entity, different names: "Neo4j" vs "Neo4j Graph Database"
- Abbreviations: "Microsoft" vs "MSFT"
- Variations: "Apple Inc." vs "Apple" vs "Apple Computer"
- Spelling variations: "GPT-4" vs "GPT4"

**Without resolution:** Multiple nodes represent the same real-world entity.

---

## What is Entity Resolution?

**Entity Resolution** is the process of identifying and merging duplicate entities in your knowledge graph.

**Goal:** Create a single, canonical node for each real-world entity.

**Benefits:**
- Cleaner, more maintainable graph
- Better query results
- Accurate relationship counts
- Improved graph analytics

---

## Default Entity Resolution Strategy

The `SimpleKGBuilder` includes built-in entity resolution:

**Default Behavior:**
- Merges entities with the same **label** and identical **name** property
- Exact string matching only
- Happens during graph construction

**Example:**
```python
# These will be merged (exact match)
Entity(label="Company", name="Apple Inc.")
Entity(label="Company", name="Apple Inc.")

# These will NOT be merged (different names)
Entity(label="Company", name="Apple Inc.")
Entity(label="Company", name="Apple")
```

---

## Disabling Entity Resolution

You can disable entity resolution if needed:

```python
kg_builder = SimpleKGBuilder(
    llm=llm,
    driver=driver,
    perform_entity_resolution=False  # Disable resolution
)
```

**When to disable:**
- Testing different resolution strategies
- Entities truly need to be distinct
- Custom post-processing planned

**Warning:** May result in many duplicate nodes!

---

## The Risk of Duplicate Entities

Without entity resolution:

```cypher
// Multiple nodes for the same company
MATCH (c:Company)
WHERE c.name CONTAINS "Apple"
RETURN c.name
```

**Results:**
- Apple
- Apple Inc.
- Apple Computer
- Apple Corporation

**Impact:** Queries become complex, relationships are scattered.

---

## Post-Processing Entity Resolution

The `neo4j_graphrag` library provides advanced resolvers:

**Available Strategies:**
1. **SpacySemanticMatchResolver** - Uses spaCy for semantic matching
2. **FuzzyMatchResolver** - Uses RapidFuzz for fuzzy string matching
3. **Custom Resolvers** - Build your own resolution logic

**When to use:** After initial graph construction for more sophisticated matching.

---

## SpacySemanticMatchResolver

Uses semantic understanding to match entities:

```python
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.experimental.pipeline.entity_resolver import SpacySemanticMatchResolver

# Create resolver
resolver = SpacySemanticMatchResolver(
    driver=driver,
    labels=["Company", "Person"]  # Labels to resolve
)

# Apply to existing graph
resolver.run()
```

**Matches entities with:**
- Same label
- Similar textual properties using spaCy embeddings

---

## FuzzyMatchResolver

Uses fuzzy string matching for resolution:

```python
from neo4j_graphrag.experimental.pipeline.entity_resolver import FuzzyMatchResolver

# Create fuzzy matcher
resolver = FuzzyMatchResolver(
    driver=driver,
    labels=["Company", "Product"],
    threshold=0.85  # Similarity threshold (0-1)
)

# Resolve entities
resolver.run()
```

**Best for:**
- Spelling variations
- Abbreviations
- Typos and minor differences

**Uses RapidFuzz library** for fast, efficient matching.

---

## Entity Resolution Trade-Offs

<div style="display: flex; gap: 2rem;">

<div style="flex: 1;">

### Conservative Resolution

**Approach:**
- High similarity threshold
- Exact or near-exact matches only

**Pros:**
- ✅ Low risk of incorrect merges
- ✅ Preserves distinct entities

**Cons:**
- ❌ More duplicates remain
- ❌ Scattered relationships

</div>

<div style="flex: 1;">

### Aggressive Resolution

**Approach:**
- Low similarity threshold
- Broader matching criteria

**Pros:**
- ✅ Fewer duplicate entities
- ✅ Consolidated relationships

**Cons:**
- ❌ Risk of merging distinct entities
- ❌ Potential data loss

</div>

</div>

---

## Choosing the Right Strategy

**Use Default Resolution when:**
- LLM produces consistent entity names
- Exact matching is sufficient
- Simple use case

**Use SpacySemanticMatchResolver when:**
- Entities have semantic variations
- Need intelligent matching
- Working with named entities

**Use FuzzyMatchResolver when:**
- Dealing with typos and abbreviations
- String similarity is good indicator
- Need fast, efficient matching

---

## Best Practices for Entity Resolution

**1. Start Conservative:**
- Begin with exact matching
- Observe duplicate patterns
- Gradually increase matching aggressiveness

**2. Test Before Production:**
- Sample your data
- Validate merged entities
- Adjust thresholds based on results

**3. Domain-Specific Tuning:**
- Different entity types may need different strategies
- Companies vs Products vs People have different naming patterns

---

## Inspecting Entity Resolution Results

After resolution, verify the results:

```cypher
// Find entities that were merged
MATCH (e:Company)
RETURN e.name, count(*) as instances
ORDER BY instances DESC
```

**Check for:**
- Were the right entities merged?
- Are distinct entities still separate?
- Do relationships look correct?

---

## Summary

Entity resolution is essential for clean knowledge graphs:

**Key Concepts:**
- Default resolution: exact label + name matching
- Can be disabled for custom strategies
- Post-processing resolvers for advanced matching
- SpacySemanticMatchResolver for semantic similarity
- FuzzyMatchResolver for string similarity

**Trade-off:** Balance between eliminating duplicates and avoiding incorrect merges.

---

## Next Steps

In the next lesson, you will learn about vectors and embeddings for semantic search in knowledge graphs.
