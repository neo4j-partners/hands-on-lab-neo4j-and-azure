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


# Schema Design

---

## Why Schema Matters

Without a schema, extraction is unconstrained—the LLM extracts *everything*.

**This creates graphs that are:**
- **Non-specific**: Too many entity types with inconsistent labeling
- **Hard to query**: No predictable structure to write queries against
- **Noisy**: Irrelevant entities mixed with important ones

Schema design solves this by telling the LLM exactly what to look for.

---

## What is a Schema?

A schema defines the structure of your knowledge graph:

- **Entity types (node labels)**: What kinds of things should be extracted?
- **Relationship types**: How should those entities connect?
- **Properties**: What attributes should entities have?
- **Patterns**: What specific connection patterns matter?

Think of the schema as a blueprint that guides extraction.

---

## Schema for SEC Filings

**Entities:**
- `Company`: Organizations filing reports
- `Executive`: People leading companies
- `Product`: Products and services mentioned
- `RiskFactor`: Business risks identified
- `FinancialMetric`: Financial measures reported

**Relationships:**
- `FACES_RISK`: Company → RiskFactor
- `MENTIONS`: Company → Product
- `HAS_METRIC`: Company → FinancialMetric
- `WORKS_FOR`: Executive → Company

---

## Defining a Schema in SimpleKGPipeline

```python
entities = [
    {"label": "Company", "description": "A business organization"},
    {"label": "RiskFactor", "description": "A business risk or threat"},
    {"label": "Product", "description": "A product or service"},
    {"label": "Executive", "description": "A company leader or officer"},
    {"label": "FinancialMetric", "description": "A financial measure or KPI"},
]

relations = [
    {"type": "FACES_RISK", "description": "Company faces this risk"},
    {"type": "MENTIONS", "description": "Company mentions this product"},
    {"type": "HAS_METRIC", "description": "Company reports this metric"},
    {"type": "WORKS_FOR", "description": "Executive works for company"},
]
```

Descriptions help the LLM understand what each type means.

---

## Schema Strictness

The `enforce_schema` parameter controls how strictly the pipeline follows your schema:

**`enforce_schema="STRICT"`**
- Only extract defined entity and relationship types
- Anything else is ignored
- Best for production graphs with specific query requirements

**`enforce_schema="LOOSE"`** (or not set)
- Use the schema as guidance
- Allow the LLM to extract additional types it considers relevant
- Good for exploratory analysis

---

## The Iterative Approach

You don't have to define everything upfront. Schema design is iterative:

1. **Start with core entities**: Define the most important entity types
2. **Let the LLM discover relationships**: See what relationships emerge
3. **Refine based on results**: Add constraints based on what the LLM extracts
4. **Test queries**: Ensure your schema supports the questions you want to answer

---

## Schema Trade-offs

<div style="display: flex; gap: 2rem;">

<div style="flex: 1;">

### Strict, Narrow Schemas

- ✅ Consistent, predictable graphs
- ✅ Clean queries with known patterns
- ❌ May miss unexpected but relevant info
- ❌ Requires upfront domain knowledge

</div>

<div style="flex: 1;">

### Loose, Broad Schemas

- ✅ Captures more information
- ✅ Good for exploration and discovery
- ❌ Inconsistent entity labeling
- ❌ Harder to write reliable queries

</div>

</div>

---

## Guided Extraction Prompts

Beyond the schema, customize the extraction prompt for domain-specific guidance:

```python
prompt_template = """
Extract entities and relationships from the following text.

Additional instructions:
- Only extract companies from this approved list: {company_list}
- Resolve "the Company" to the actual company name
- For risk factors, focus on business and operational risks
- Ignore general market commentary

Schema: {schema}
Text: {text}
"""
```

---

## Validating Your Schema

After extraction, validate that your schema produces useful results:

```cypher
// Check entity type distribution
MATCH (n)
WHERE NOT n:Document AND NOT n:Chunk
RETURN labels(n) AS entityType, count(n) AS count
ORDER BY count DESC

// Verify key patterns exist
MATCH (c:Company)-[:FACES_RISK]->(r:RiskFactor)
RETURN c.name, count(r) AS riskCount
ORDER BY riskCount DESC LIMIT 5
```

---

## Summary

In this lesson, you learned:

- **Schema defines structure**: Entity types, relationships, properties, patterns
- **Schema guides extraction**: Tells the LLM what to look for
- **Strictness is configurable**: STRICT for production, LOOSE for exploration
- **Iteration improves results**: Start simple, refine based on what you see
- **Custom prompts add control**: Domain-specific guidance improves accuracy

**Next:** Learn about chunking strategies and their trade-offs.
