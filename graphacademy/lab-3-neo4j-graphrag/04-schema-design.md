# Schema Design in SimpleKGPipeline

## Why Schema Matters

When you extract entities and relationships from documents without guidance, the LLM extracts *everything*—every person, place, concept, and connection it identifies. This creates graphs that are:

- **Non-specific**: Too many entity types with inconsistent labeling
- **Hard to query**: No predictable structure to write queries against
- **Noisy**: Irrelevant entities mixed with important ones

Providing a schema to SimpleKGPipeline solves this by telling the LLM exactly what to look for.

## Schema in SimpleKGPipeline

SimpleKGPipeline accepts a `schema` parameter that guides the extraction process. The schema defines:

- **Node types**: What kinds of entities should be extracted
- **Relationship types**: What connections between entities matter
- **Patterns**: Which specific node-relationship-node combinations are valid

When you provide a schema, the pipeline uses it to:
1. Guide the LLM during entity and relationship extraction
2. Prune extracted data that doesn't match the schema
3. Ensure consistency across all processed documents

## Three Schema Modes

SimpleKGPipeline supports three approaches to schema:

### 1. User-Provided Schema

You define exactly what entities and relationships to extract:

```python
schema = {
    "node_types": [
        {"label": "Company", "description": "A business organization"},
        {"label": "RiskFactor", "description": "A business risk or threat"},
        {"label": "Product", "description": "A product or service"},
    ],
    "relationship_types": [
        {"label": "FACES_RISK", "description": "Company faces this risk"},
        {"label": "MENTIONS", "description": "Company mentions this product"},
    ],
    "patterns": [
        ("Company", "FACES_RISK", "RiskFactor"),
        ("Company", "MENTIONS", "Product"),
    ]
}

pipeline = SimpleKGPipeline(
    driver=driver,
    llm=llm,
    embedder=embedder,
    schema=schema,
)
```

This gives you maximum control and produces predictable, queryable graphs.

### 2. Automatic Schema Extraction

Let the LLM discover the schema from your documents:

```python
pipeline = SimpleKGPipeline(
    driver=driver,
    llm=llm,
    embedder=embedder,
    schema="EXTRACTED",  # or simply omit schema
)
```

The pipeline analyzes your text and generates a schema automatically. This is useful for exploration when you don't know what entities exist in your documents.

### 3. Free Mode (No Schema)

Extract everything without constraints:

```python
pipeline = SimpleKGPipeline(
    driver=driver,
    llm=llm,
    embedder=embedder,
    schema="FREE",
)
```

This produces the most comprehensive extraction but with inconsistent structure.

## Defining Node and Relationship Types

Node and relationship types can be simple strings or detailed dictionaries:

**Simple format:**
```python
node_types = ["Company", "Product", "RiskFactor"]
relationship_types = ["FACES_RISK", "MENTIONS"]
```

**Detailed format with descriptions:**
```python
node_types = [
    {"label": "Company", "description": "A business organization filing SEC reports"},
    {"label": "RiskFactor", "description": "A business, operational, or financial risk"},
    {
        "label": "Product",
        "description": "A product or service offered by a company",
        "properties": [
            {"name": "name", "type": "STRING"},
            {"name": "category", "type": "STRING"}
        ]
    }
]
```

Descriptions help the LLM understand what each type means, improving extraction accuracy.

## Patterns: Valid Connections

Patterns specify which relationships are valid between which node types:

```python
patterns = [
    ("Company", "FACES_RISK", "RiskFactor"),
    ("Company", "MENTIONS", "Product"),
    ("Executive", "WORKS_FOR", "Company"),
]
```

Without patterns, the LLM might create relationships like `(Product)-[:FACES_RISK]->(Company)` which don't make semantic sense.

## Schema for This Workshop

For SEC filings analysis, a focused schema might include:

| Node Type | Description |
|-----------|-------------|
| Company | Organizations filing reports |
| RiskFactor | Business risks identified |
| Product | Products and services mentioned |
| Executive | Company leaders |
| FinancialMetric | Financial measures reported |

| Relationship | Pattern |
|-------------|---------|
| FACES_RISK | Company → RiskFactor |
| MENTIONS | Company → Product |
| WORKS_FOR | Executive → Company |
| HAS_METRIC | Company → FinancialMetric |

This schema focuses extraction on business-relevant information, ignoring generic entities that don't serve the analysis goals.

## When to Use Each Mode

| Mode | Best For |
|------|----------|
| **User-Provided** | Production systems with known query patterns |
| **Extracted** | Exploration when you're learning the domain |
| **Free** | Initial discovery of what's in your documents |

For most production GraphRAG applications, a user-provided schema produces the most reliable results.

## Learn More About Schema Design

This lesson covers how to use schemas in SimpleKGPipeline. For deep dives into schema design principles—including iterative refinement, domain modeling, and advanced patterns—see the dedicated [Neo4j GraphRAG Python course](https://graphacademy.neo4j.com/).

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

- **Schema guides extraction**: Tells SimpleKGPipeline what entities and relationships to find
- **Three modes**: User-provided (control), Extracted (discovery), Free (exploration)
- **Node and relationship types**: Define what to extract with optional descriptions
- **Patterns**: Specify valid connections between node types
- **Production systems**: Benefit most from user-provided schemas

With a schema defined, the next decision is how to break documents into chunks for processing. In the next lesson, you'll learn about chunking strategies and their trade-offs.

---

**Navigation:**
- [← Previous: Building Knowledge Graphs](03-building-knowledge-graphs.md)
- [↑ Back to Lab 3](README.md)
- [Next: Chunking Strategies →](05-chunking.md)
