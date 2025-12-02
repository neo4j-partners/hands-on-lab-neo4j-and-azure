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


# Working with Retrievers

Module 2, Lesson 4

---

## Overview

This lesson explores all three retriever types in practice.

You will see:
- How each retriever is initialized
- How they are customized for your requirements
- How they fit into a GraphRAG pipeline
- How their results differ for the same questions

---

## The Three Retriever Types

**Vector Retriever:**
- Returns semantically similar text chunks

**Vector + Cypher Retriever:**
- Provides both content and relationships

**Text2Cypher Retriever:**
- Direct, precise answers from graph structure

---

## Vector Retriever Characteristics

**Strengths:**
- Good for exploratory questions
- Finds semantically similar content
- Simple to set up and use

**Limitations:**
- May miss entity-specific context
- No relationship information
- Limited to text chunk similarity

---

## Vector Retriever Use Cases

**Best For:**
- Broad semantic questions
- General topic exploration
- When relationships aren't critical

**Examples:**
- "What are the main cybersecurity threats mentioned?"
- "Tell me about risk factors in the documents"
- "What themes appear across multiple filings?"

---

## Vector + Cypher Retriever Characteristics

**Strengths:**
- Provides both content and relationships
- Richer context with entity information
- Better for comprehensive answers

**Approach:**
- Starts with vector similarity
- Traverses graph for related entities
- Combines text and structured data

---

## Vector + Cypher Retriever Use Cases

**Best For:**
- Entity-specific questions
- Questions requiring context about relationships
- When you need "why" and "how" connections

**Examples:**
- "What products does Apple mention in their filings?"
- "Which companies face similar regulatory challenges?"
- "How do risk factors relate across companies?"

---

## Text2Cypher Retriever Characteristics

**Strengths:**
- Direct, precise answers from graph structure
- Perfect for factual queries
- Handles aggregations and counts

**Approach:**
- Converts natural language to Cypher
- Executes query against graph
- Returns structured results

---

## Text2Cypher Retriever Use Cases

**Best For:**
- Precise data questions
- Counting and aggregation
- Factual queries with exact answers

**Examples:**
- "How many companies mention cloud computing?"
- "Count the risk factors for Microsoft"
- "What stock has Microsoft issued?"

---

## Comparing Retriever Approaches

**Vector:**
- Semantic similarity → Text chunks

**Vector + Cypher:**
- Semantic similarity → Text chunks + Related entities

**Text2Cypher:**
- Natural language → Cypher query → Structured data

Different approaches for different question types.

---

## Model Configuration

All retrievers use consistent models:

**LLM:**
- Generates responses and interprets queries
- Same model ensures consistent behavior

**Embedder:**
- Converts text to vectors
- Same embedder ensures compatible similarity

Consistency across retrievers enables fair comparison.

---

## Question Types to Try

**Broad Semantic Questions:**
- Test with Vector Retriever
- Exploratory and general topics

**Entity-Specific Questions:**
- Test with Vector + Cypher Retriever
- Questions about specific companies or relationships

**Precise Data Questions:**
- Test with Text2Cypher Retriever
- Counting, aggregation, exact facts

---

## Observing Result Differences

When you test the same question across retrievers:

**Different Information:**
- Vector returns text chunks
- Vector + Cypher adds entities and relationships
- Text2Cypher returns structured query results

**Different Styles:**
- Some more comprehensive
- Some more precise
- Some more exploratory

---

## Retriever Selection Strategy

**Choose Vector when:**
- Exploring broad topics
- Semantic understanding is key
- Relationships not critical

**Choose Vector + Cypher when:**
- Need entity context
- Relationships matter
- Want comprehensive coverage

---

## Retriever Selection Strategy (continued)

**Choose Text2Cypher when:**
- Need precise facts
- Counting or aggregating
- Query structured data directly

Understanding these trade-offs guides selection.

---

## Combining Retrievers

In practice, you often use multiple retrievers:

**In Sequence:**
- Use one retriever first, then another for follow-up

**In Parallel:**
- Compare results from multiple approaches

**Dynamically:**
- Let an agent choose the right retriever for each question

---

## Preparation for Agents

Understanding how each retriever works sets you up for:
- Building intelligent agents
- Automatic tool selection
- Multi-retriever strategies

Agents can choose the right retriever for each question automatically.

---

## Key Insights

**Different retrievers excel at different questions:**
- No single best retriever for everything

**Combining approaches gives comprehensive coverage:**
- Use multiple retrievers together

**Understanding strengths guides selection:**
- Match retriever to question type

---

## Summary

You explored three retriever types in practice:
- Vector Retriever for semantic search
- Vector + Cypher Retriever for contextual search
- Text2Cypher Retriever for precise queries

Each has distinct strengths and ideal use cases.

---

## Next Steps

In the next module, you will learn how to combine these retrievers into intelligent agents that choose the right retrieval method automatically.

