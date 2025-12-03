# Schema Design

## Why Schema Matters

When you extract entities and relationships from documents, an unconstrained approach extracts *everything*—every person, place, concept, and connection the LLM identifies. This creates graphs that are:

- **Non-specific**: Too many entity types with inconsistent labeling
- **Hard to query**: No predictable structure to write queries against
- **Noisy**: Irrelevant entities mixed with important ones

Schema design solves this by telling the LLM exactly what to look for.

## What is a Schema?

A schema defines the structure of your knowledge graph:

- **Entity types (node labels)**: What kinds of things should be extracted?
- **Relationship types**: How should those entities connect?
- **Properties**: What attributes should entities have?
- **Patterns**: What specific connection patterns matter?

Think of the schema as a blueprint that guides extraction toward relevant, consistent data.

## Schema for SEC Filings

For the SEC filings knowledge graph, a meaningful schema might include:

**Entities:**
- `Company`: Organizations filing reports
- `Executive`: People leading companies
- `Product`: Products and services mentioned
- `RiskFactor`: Business risks identified
- `FinancialMetric`: Financial measures reported
- `StockType`: Types of stock issued
- `TimePeriod`: Relevant time references

**Relationships:**
- `FACES_RISK`: Company → RiskFactor
- `MENTIONS`: Company → Product
- `HAS_METRIC`: Company → FinancialMetric
- `WORKS_FOR`: Executive → Company
- `ISSUED_STOCK`: Company → StockType

This schema focuses extraction on business-relevant information, ignoring generic entities like locations or dates that don't serve the analysis goals.

## Defining a Schema in SimpleKGPipeline

You define entities and relationships as lists, then pass them to the pipeline:

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

pipeline = SimpleKGPipeline(
    driver=driver,
    llm=llm,
    embedder=embedder,
    entities=entities,
    relations=relations,
)
```

The descriptions help the LLM understand what each entity type means, improving extraction accuracy.

## Schema Strictness

The `enforce_schema` parameter controls how strictly the pipeline follows your schema:

**`enforce_schema="STRICT"`**: Only extract defined entity and relationship types. Anything else is ignored.

**`enforce_schema="LOOSE"`** (or not set): Use the schema as guidance, but allow the LLM to extract additional types it considers relevant.

For production graphs with specific query requirements, strict enforcement creates predictable, queryable structures. For exploratory analysis, loose enforcement might surface unexpected insights.

## The Iterative Approach

You don't have to define everything upfront. Schema design is iterative:

1. **Start with core entities**: Define the most important entity types
2. **Let the LLM discover relationships**: Initially, you might define only nodes and see what relationships emerge
3. **Refine based on results**: Add constraints based on what the LLM extracts
4. **Test queries**: Ensure your schema supports the questions you want to answer

This iterative process helps you discover what structure best serves your use case.

## Schema Trade-offs

**Strict, narrow schemas:**
- ✓ Consistent, predictable graphs
- ✓ Clean queries with known patterns
- ✗ May miss unexpected but relevant information
- ✗ Requires upfront domain knowledge

**Loose, broad schemas:**
- ✓ Captures more information
- ✓ Good for exploration and discovery
- ✗ Inconsistent entity labeling
- ✗ Harder to write reliable queries

Choose based on your goals: production systems typically need stricter schemas; research and exploration benefit from flexibility.

## Guided Extraction Prompts

Beyond the schema, you can customize the extraction prompt to add domain-specific guidance:

```python
prompt_template = """
Extract entities and relationships from the following text.

Additional instructions:
- Only extract companies from this approved list: {company_list}
- Resolve "the Company" to the actual company name
- For risk factors, focus on business and operational risks
- Ignore general market commentary

Schema:
{schema}

Text:
{text}
"""
```

Custom prompts help the LLM make better extraction decisions, especially for domain-specific documents.

## Validating Your Schema

After extraction, validate that your schema produces useful results:

```cypher
// Check entity type distribution
MATCH (n)
WHERE NOT n:Document AND NOT n:Chunk
RETURN labels(n) AS entityType, count(n) AS count
ORDER BY count DESC

// Check relationship type distribution
MATCH ()-[r]->()
RETURN type(r) AS relationshipType, count(r) AS count
ORDER BY count DESC

// Verify key patterns exist
MATCH (c:Company)-[:FACES_RISK]->(r:RiskFactor)
RETURN c.name, count(r) AS riskCount
ORDER BY riskCount DESC
LIMIT 5
```

If key patterns are missing or entity counts seem wrong, adjust your schema and re-extract.

## Check Your Understanding

### Why would you define a schema when using SimpleKGPipeline?

**Options:**
- [ ] To improve processing speed
- [ ] To reduce memory usage
- [x] To create a more structured and queryable knowledge graph
- [ ] To extract all possible information

<details>
<summary>Hint</summary>
Think about what happens when you don't provide a schema—the graph becomes unconstrained.
</details>

<details>
<summary>Show Answer</summary>
**To create a more structured and queryable knowledge graph**. Without a schema, the LLM extracts whatever it finds, leading to inconsistent entity types and unpredictable structure. A schema focuses extraction on relevant entities and relationships, creating graphs you can reliably query.
</details>

## Summary

In this lesson, you learned:

- **Schema defines structure**: Entity types, relationships, properties, and patterns
- **Schema guides extraction**: Tells the LLM what to look for, not just what to find
- **Strictness is configurable**: STRICT for production, LOOSE for exploration
- **Iteration improves results**: Start simple, refine based on what you see
- **Custom prompts add control**: Domain-specific guidance improves accuracy

With a schema defined, the next decision is how to break documents into chunks for processing. In the next lesson, you'll learn about chunking strategies and their trade-offs.

---

**Navigation:**
- [← Previous: Building Knowledge Graphs](03-building-knowledge-graphs.md)
- [↑ Back to Lab 3](README.md)
- [Next: Chunking Strategies →](05-chunking.md)
