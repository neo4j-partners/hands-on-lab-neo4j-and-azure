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

Module 1, Lesson 5

---

## The Problem with Unconstrained Graphs

Without a schema, knowledge graphs are unconstrained:
- Any entity or relationship can be created
- Extraction is based solely on what the LLM finds in text
- Results can be non-specific and difficult to analyze
- Queries become harder to write and maintain

---

## What is a Schema?

A schema defines the structure of your knowledge graph.

You express:
- Desired node types
- Desired relationship types
- Patterns showing how nodes connect

This guides the LLM to extract only relevant information.

---

## Schema Components

**Nodes:**
- Entity types you want to extract (e.g., Person, Organization, Location)

**Relationships:**
- Connection types between entities (e.g., WORKS_AT, LOCATED_IN)

**Patterns:**
- How nodes connect via relationships (e.g., Person-WORKS_AT→Organization)

---

## Benefits of Defining a Schema

**Structure:**
- Creates consistent, predictable graph structure
- Enables repeatable queries

**Clarity:**
- Makes the graph easier to understand and navigate
- Clear semantic meaning

**Performance:**
- Targeted extraction is more efficient
- Reduces noise and irrelevant data

---

## Iterative Schema Development

You don't have to define everything at once.

**Start Simple:**
- Define just nodes or just relationships
- Let the LLM find other connections

**Expand Gradually:**
- Add more constraints as you understand your data
- Refine based on what you observe

This iterative approach helps you build the right schema.

---

## Node Definitions

When defining nodes, you specify:

**Label:**
- The entity type (e.g., Person, Company)

**Optional Description:**
- Guidance for the LLM on what qualifies

**Optional Properties:**
- Specific attributes to extract

---

## Node Definition Best Practices

**Be Domain-Specific:**
- Define node labels relevant to your specific domain
- Don't try to capture everything

**Think About Your Questions:**
- What entities will you query for?
- What do users need to find?

**Consider Relationships:**
- Which entities need to connect to each other?

---

## Relationship Definitions

Relationships define how entities connect.

**Be Specific:**
- Use clear, semantic relationship names
- WORKS_AT is better than RELATED_TO

**Consider Direction:**
- Relationships have direction in graphs
- Person-WORKS_AT→Organization makes sense
- Organization-WORKS_AT→Person doesn't

---

## Pattern Definitions

Patterns show complete connection structures.

**Format:**
- `(NodeType)-[RELATIONSHIP]->(NodeType)`

**Example:**
- `(Person)-[WORKS_AT]->(Organization)`
- `(Organization)-[LOCATED_IN]->(Location)`

Patterns help the LLM understand valid graph structures.

---

## Schema Constrains Extraction

When you provide a schema to the pipeline:
- LLM is instructed to identify only specified nodes and relationships
- Extraction becomes focused and targeted
- Resulting graph has predictable structure
- Queries become simpler and more reliable

---

## Schema Evolution

Schemas can evolve over time:

**Initial Schema:**
- Start with core entities and relationships
- Test with sample data

**Refinement:**
- Add missing entity types
- Include additional relationship types
- Adjust based on query needs

**Maintenance:**
- Keep schema aligned with use cases
- Remove unused elements

---

## Impact on Graph Quality

A well-designed schema results in:
- More meaningful knowledge graphs
- Better query results
- Clearer semantic understanding
- Easier maintenance and evolution

Poor or missing schemas lead to:
- Noisy, cluttered graphs
- Difficult queries
- Unclear semantics

---

## Balancing Flexibility and Structure

**Too Loose:**
- Everything gets extracted
- Graph becomes cluttered
- Hard to query effectively

**Too Tight:**
- Miss important information
- Limited coverage
- May need frequent updates

Find the right balance for your use case.

---

## Summary

Schema design is crucial for effective knowledge graphs:
- Constrains extraction to relevant information
- Creates structured, queryable graphs
- Enables iterative refinement
- Balances flexibility and structure

Define schemas based on your domain and query needs.

---

## Next Steps

In the next lesson, you will learn about optimizing chunk size for entity extraction.

