# Content Integration Proposal: Labs 3, 5 & 6

## Status: IMPLEMENTED

This proposal has been implemented. The restructured content is now live in:
- `lab-3-generative-ai/` (7 lessons)
- `lab-5-retrievers/` (4 lessons)
- `lab-6-agents/` (5 lessons)

**Final Lesson Count: 16 lessons (down from 24)**

---

## Executive Summary

After deep analysis of all three labs, this proposal recommends restructuring to create a cohesive story that flows naturally from "Why do LLMs struggle?" through "How do we build knowledge graphs?" to "How do we query them intelligently?" The graph construction process (schema design, chunking, entity resolution, vectors) is *central* to understanding GraphRAG—not an aside.

---

## The Current State

### Lab 3: Building Knowledge Graphs (9 lessons)
1. What is GenAI
2. LLM Limitations
3. Context (RAG introduction)
4. Building the Graph (GraphRAG intro + SimpleKGPipeline)
5. Schema Design
6. Chunking
7. Entity Resolution
8. Vectors
9. Full Dataset

### Lab 5: GraphRAG Retrievers (6 lessons)
1. Understanding GraphRAG
2. What is a Retriever
3. Vector Retriever
4. Vector Cypher Retriever
5. Text2Cypher Retriever
6. Choosing Retrievers

### Lab 6: Intelligent Agents (9 lessons)
1. What is an Agent
2. Microsoft Agent Framework
3. Simple Schema Agent
4. Vector Graph Agent
5. Text2Cypher Agent
6. Multi-Tool Design
7. Aura Agents
8. Best Practices (LLM Config)
9. Congratulations

**Total: 24 lessons**

---

## Issues Identified

### 1. The Story Restarts in Lab 5

Lab 3 builds a complete narrative about *why* we need knowledge graphs and *how* to build them. Then Lab 5 opens by re-explaining GraphRAG from scratch (Lesson 1: "Understanding GraphRAG") as if Lab 3 didn't happen. This breaks the narrative flow.

**Better approach**: Lab 5 should pick up where Lab 3 left off: "You've built a knowledge graph with vectors. Now let's learn how to retrieve context from it."

### 2. Three Retriever Types Introduced Multiple Times

1. Lab 3 Lesson 4 mentions them vaguely in the GraphRAG context
2. Lab 5 Lesson 1 re-introduces them in GraphRAG explanation
3. Lab 5 Lesson 2 lists all three with code examples
4. Lab 5 Lessons 3-5 detail each one
5. Lab 5 Lesson 6 summarizes how to choose
6. Lab 6 reintroduces them as "tools"

**Recommendation**: Introduce clearly once in Lab 5 Lesson 1 as the transition from Lab 3, then build understanding progressively.

### 3. Code-Heavy Lessons Obscure Concepts

Lessons like Lab 5's Vector Retriever and Vector Cypher Retriever contain extensive code blocks that distract from conceptual understanding. Learners need to understand *what* and *why* before diving into *how*.

**Recommendation**: Lessons explain concepts with minimal illustrative code. Notebooks are for implementation details.

### 4. Lab 5 "Choosing Retrievers" Creates Tension with Lab 6

Lab 5 Lesson 6 teaches manual retriever selection as a skill. Then Lab 6 says "agents automate this." This raises the question: Why did I learn to choose if the agent will choose for me?

**Better framing**: "Understanding *why* each retriever works helps you design better agent systems, write better tool descriptions, and debug when things go wrong."

### 5. Lab 6 Agent Lessons Are Very Thin

Lessons 3-5 (Simple Agent, Vector Agent, Text2Cypher Agent) are short because the real content is in notebooks. This creates an uneven reading experience and repetitive structure.

### 6. Vectors Lesson is Crucial But Appears Late

The Vectors lesson (Lab 3 Lesson 8) is foundational—it explains embeddings, similarity search, and how vectors enable semantic retrieval. But it appears *after* schema design, chunking, and entity resolution.

**Consideration**: Vectors could come earlier, as they're essential to understanding why we chunk text in the first place (to create embeddings).

---

## The Story We Should Tell

### The Core Narrative Arc

> **Part 1 (Lab 3)**: "LLMs are powerful but limited. Context helps. Traditional RAG has limits—it treats documents as isolated blobs. Knowledge graphs give us structured context with relationships. Here's how to build one: you need a good schema, appropriate chunking, entity resolution, and vector embeddings for semantic search."

> **Part 2 (Lab 5)**: "You have a knowledge graph with vectors. Now let's retrieve context from it. Three patterns: vector search for semantic questions, vector+graph for relationship-aware questions, and text2cypher for precise facts. Each has its place."

> **Part 3 (Lab 6)**: "Users don't want to choose retrieval patterns. Agents analyze questions and pick the right tool automatically. Here's how to build one."

### Key Principle: Graph Construction IS the Story

The process of building a knowledge graph—defining schemas, chunking documents, resolving entities, creating embeddings—isn't tangential. It's *why* GraphRAG works:

- **Schema design** determines what entities and relationships your graph captures (and what questions you can answer)
- **Chunking** affects retrieval granularity and context quality
- **Entity resolution** determines whether your graph has one "Apple Inc" or ten
- **Vectors** enable semantic search that finds meaning, not just keywords

Understanding these makes learners better GraphRAG practitioners.

---

## Proposed Structure

### Lab 3: Building Knowledge Graphs (7 lessons)

**Theme**: *Why we need knowledge graphs and how to build them*

**Lesson 1: The GenAI Promise and Its Limits**

What LLMs can do and where they fail:
- Hallucination: confident but wrong
- Knowledge cutoff: no access to your data
- Relationship blindness: can't connect information across documents

The key insight: These aren't bugs—they're fundamental limitations of how LLMs work.

*Transition*: "These limitations have solutions. The first step is giving the LLM relevant context."

---

**Lesson 2: Context and the Limits of Traditional RAG**

How context improves LLM responses dramatically. The RAG pattern: retrieve → augment → generate.

But traditional RAG has problems:
- Retrieves based on similarity, not understanding
- Treats documents as isolated, unstructured blobs
- Can't bridge relationships across documents
- Can't answer "Which asset managers own companies facing cyber risks?"

The insight: We need *structured* context. We need a knowledge graph.

*Transition*: "Let's understand what knowledge graphs are and how we build them from documents."

---

**Lesson 3: From Documents to Knowledge Graphs**

What knowledge graphs are: entities (nodes), relationships, and properties that capture domain knowledge.

The SEC filings example: How PDFs containing company information become structured, queryable data.

Introduction to the `neo4j-graphrag` Python package and `SimpleKGPipeline`:
- The pipeline orchestrates the transformation from documents to knowledge graphs
- It handles text extraction, chunking, entity extraction, relationship extraction, and graph storage

The complete picture: Documents → Chunks → Entities → Relationships → Knowledge Graph

*Transition*: "The quality of your knowledge graph depends on the decisions you make. Let's start with schema design."

---

**Lesson 4: Schema Design**

Why schema matters: An unconstrained graph extracts everything, but "everything" is hard to query and analyze.

Schema-driven extraction:
- Define the entities you care about: Company, Executive, Product, RiskFactor, FinancialMetric
- Define the relationships: FACES_RISK, MENTIONS, HAS_METRIC, OWNS
- Guide the LLM to extract what's relevant to your domain

The iterative approach: Start simple, expand as needed. You can define just nodes first and let the LLM discover relationships.

Trade-offs:
- Strict schemas produce consistent, queryable graphs but may miss unexpected insights
- Loose schemas capture more but create messy, hard-to-query structures

*Transition*: "With a schema defined, we need to break documents into chunks for processing."

---

**Lesson 5: Chunking Strategies**

Why chunking matters: LLMs have context limits. Long documents must be broken into smaller pieces.

The trade-offs:
- **Larger chunks**: More context for entity extraction, but less granular retrieval
- **Smaller chunks**: More granular retrieval, but less context for extraction

Chunking parameters:
- `chunk_size`: Maximum characters per chunk
- `chunk_overlap`: Overlap between consecutive chunks to maintain context

The insight: Chunk size affects *both* graph construction quality (entity extraction needs context) *and* retrieval quality (smaller chunks = more precise matches).

*Transition*: "Even with good chunking, the same entity may appear with different names. That's where entity resolution comes in."

---

**Lesson 6: Entity Resolution**

The problem: Text refers to the same entity differently. "Neo4j" vs "Neo4j Graph Database" vs "the Company."

Why it matters: Without resolution, your graph has multiple nodes for the same real-world entity. This breaks relationship traversal and aggregation queries.

Resolution strategies:
- **Default merging**: Merge entities with identical labels and names
- **Semantic matching**: Use NLP to find entities with similar textual properties
- **Fuzzy matching**: Use string similarity to catch variations

Trade-offs:
- Too aggressive: Incorrectly merge distinct entities
- Too conservative: Multiple nodes for the same thing

The insight: Entity resolution quality directly affects query accuracy.

*Transition*: "Now let's add the capability that enables semantic search: vector embeddings."

---

**Lesson 7: Vectors and Semantic Search**

What vectors are: Numerical representations that capture meaning. Words with similar meanings have similar vectors.

What embeddings are: High-dimensional vectors (often 1,536 dimensions) that encode the semantic meaning of text.

Why this matters for GraphRAG:
- Convert questions and chunks to vectors
- Find chunks by *meaning*, not just keywords
- "What challenges does Apple face?" finds risk discussions even without the word "challenges"

Storing vectors in Neo4j:
- Vector indexes enable fast similarity search
- Chunks have embeddings stored alongside their text
- Combine vector similarity with graph traversal

The complete picture: Your knowledge graph now has:
- Structured entities and relationships (from schema-driven extraction)
- Text chunks (appropriately sized)
- Resolved entities (no duplicates)
- Vector embeddings (enabling semantic search)

*Transition*: "You've built a complete knowledge graph. In Lab 5, you'll learn how to retrieve context from it."

---

### Lab 5: GraphRAG Retrievers (4 lessons)

**Theme**: *Three ways to get context from your knowledge graph*

**Lesson 1: Retrievers and the GraphRAG Pattern**

Where we are: You have a knowledge graph with structured entities, relationships, and vector-enabled chunks. Now you need to get relevant context for LLM queries.

What retrievers do: A retriever finds relevant information from your knowledge graph and provides it as context for answer generation.

The GraphRAG class: Combines a retriever with an LLM to produce grounded answers.

Three retrieval patterns (preview):
- **Vector Retriever**: Find semantically similar content
- **Vector Cypher Retriever**: Find similar content, then traverse to related entities
- **Text2Cypher Retriever**: Convert natural language to database queries

How to think about selection:
- Is this a *content* question or a *fact* question?
- Do I need *relationships* or just *text*?
- Am I asking about *concepts* or *specific entities*?

*Transition*: "Let's understand each retriever in depth, starting with pure vector search."

---

**Lesson 2: Vector Retriever**

When to use: Semantic questions about concepts, topics, content exploration.

How it works:
1. Your question becomes an embedding
2. The vector index finds chunks with similar embeddings
3. The most similar chunks become context for the LLM
4. The LLM generates an answer grounded in that context

Strengths:
- Finds meaning, not keywords
- Works even when your question uses different words than the documents
- Fast and scalable with vector indexes

Limitations:
- Returns text chunks only—no entity relationships
- Can't count, aggregate, or compare
- Can't traverse to related entities

Example questions that work well:
- "What is Apple's business strategy?"
- "Tell me about cybersecurity threats"
- "What does Microsoft say about cloud computing?"

Example questions that don't work well:
- "How many risk factors does Apple face?" (needs counting)
- "Which asset managers own Apple?" (needs graph traversal)

The key insight: Vector search finds *relevant content*. If you need *relationships* or *facts*, you need something more.

*Transition*: "What if we want the relevant content AND its connected entities?"

---

**Lesson 3: Vector Cypher Retriever**

When to use: Questions needing both content and connected entities.

How it works:
1. Vector search finds relevant chunks (just like Vector Retriever)
2. A custom Cypher query traverses *from those chunks* to related entities
3. Returns both text content and structured entity data

The key insight: **The chunk is your anchor**. You can only traverse to entities connected to chunks that vector search found. If your question doesn't surface chunks about Apple, your Cypher query can't reach Apple's relationships.

Strengths:
- Combines semantic search with graph intelligence
- Returns both content and relationships
- Can find patterns across entities (shared risks, common managers)

When it works well:
- "Which asset managers are exposed to banking regulations?"
  - Vector finds chunks about banking regulations
  - Cypher traverses to companies mentioned → then to asset managers
- "What products do tech companies discuss in risk sections?"
  - Vector finds risk-related chunks
  - Cypher traverses to companies → then to products

When it struggles:
- "What are Apple's risks?" with no Apple-related chunks in top results
  - If vector search doesn't find Apple content, Cypher can't reach Apple entities

*Transition*: "What about precise facts, counts, and specific lookups?"

---

**Lesson 4: Text2Cypher Retriever**

When to use: Facts, counts, specific entity lookups, comparisons.

How it works:
1. LLM analyzes your question and your graph schema
2. LLM generates a Cypher query to answer the question
3. Query executes against the database
4. Returns structured, precise results

Strengths:
- Precise answers from the database
- Counts, aggregations, comparisons
- Direct entity lookups without semantic search
- Can answer "How many..." and "Which company has the most..."

Limitations:
- Requires good schema understanding by the LLM
- May generate invalid Cypher for complex questions
- Not suitable for semantic or exploratory questions
- Security consideration: read-only credentials essential

Example questions that work well:
- "How many companies are in the database?"
- "Which company has the most risk factors?"
- "What companies does BlackRock own?"
- "List all asset managers"

Example questions that don't work well:
- "What is Apple's strategy?" (semantic, not factual)
- "Tell me about cybersecurity" (exploratory)

**The Decision Framework**:

| Question Pattern | Best Retriever | Why |
|-----------------|----------------|-----|
| "What is..." / "Tell me about..." | Vector | Semantic content search |
| "Which [entities] are affected by [topic]..." | Vector Cypher | Content + relationships |
| "How many..." / "List all..." / "Who owns..." | Text2Cypher | Precise database query |

The key insight: Understanding *why* each retriever works for different questions helps you build better systems—and becomes essential when designing agents that choose automatically.

*Transition*: "You know three retrieval strategies. But users don't want to think about this. In Lab 6, you'll build agents that make these decisions automatically."

---

### Lab 6: Intelligent Agents (5 lessons)

**Theme**: *Making GraphRAG conversational*

**Lesson 1: From Retrievers to Agents**

The problem: Users ask questions in natural language. They don't know about retriever types. They just want answers.

The solution: Build a system that:
- Analyzes the question
- Decides which retrieval strategy to use
- Executes the appropriate tool(s)
- Synthesizes a coherent answer

What makes something an "agent":
- **Perceives**: Receives user questions, understands conversation history
- **Reasons**: Analyzes what kind of question this is, what information is needed
- **Acts**: Selects and executes the appropriate tool(s)
- **Responds**: Combines results into a coherent answer

The key insight: Your retrievers become *tools* that the agent can use. The agent's job is deciding *when* to use each one—exactly what you learned in Lab 5's decision framework.

*Transition*: "Let's see how the Microsoft Agent Framework enables this."

---

**Lesson 2: The Microsoft Agent Framework**

What the framework provides:
- **AzureAIClient**: Connection to Azure AI services
- **ChatAgent**: Pre-built agent that handles tool selection
- **Tools**: Python functions with descriptive docstrings
- **Threads**: Conversation history for multi-turn interactions

How tool selection works:
- Tools are defined as Python functions with docstrings
- The agent reads the function name and docstring
- When a question arrives, the agent matches it semantically to tool descriptions
- The best-matching tool gets called

The ReAct pattern (Reasoning + Acting):
1. Agent receives question
2. Agent reasons: "This asks about counts, so I need the database query tool"
3. Agent acts: Calls the tool
4. Agent observes: Gets results
5. Agent responds: Formats answer (or calls another tool if needed)

Why descriptive docstrings matter:
- "search" tells the agent nothing
- "Find content about topics and concepts using semantic search" tells the agent exactly when to use it

*Transition*: "Let's build an agent step by step."

---

**Lesson 3: Building Your Agent**

The progressive approach:
1. Start with one tool (schema introspection)
2. Add semantic search (vector retriever)
3. Add precise queries (text2cypher)

Why start simple:
- Understand how agents analyze questions
- See how tool selection works
- Validate at each stage before adding complexity

Tool 1: Schema introspection
- Returns the graph schema
- Helps users understand what data exists
- Agent uses it for "What entities exist?" questions

Tool 2: Vector retriever (semantic search)
- Finds content about topics and concepts
- Agent uses it for "What does X say about Y?" questions

Tool 3: Text2Cypher (database queries)
- Answers factual questions with precision
- Agent uses it for "How many..." and "List all..." questions

Example interactions showing routing:
- "What types of data are in this database?" → Schema tool
- "What does Apple say about AI?" → Vector retriever
- "How many risk factors does Apple face?" → Text2Cypher

*Transition*: "Now let's understand the design principles that make agents effective."

---

**Lesson 4: Agent Design Patterns**

**Tool Specialization**: Each tool should have a clear, distinct purpose. Overlapping responsibilities confuse the agent.

Bad design:
- Tool 1: "Search for companies"
- Tool 2: "Find companies in documents"
- Tool 3: "List companies"
- Problem: Which one should handle "What companies mention AI?"

Good design:
- Tool 1: "Explore database structure"
- Tool 2: "Search content semantically"
- Tool 3: "Query precise facts"
- Benefit: Clear boundaries, reliable selection

**Descriptive Signatures**: Tool names and docstrings guide selection.

```python
# Vague - agent doesn't know when to use
def search(query: str) -> str:
    """Search the database."""

# Clear - agent knows exactly when to use
def find_content_about_topics(query: str) -> str:
    """Find content about topics, concepts, and themes using semantic search.
    Use for questions like 'What does X say about Y?' or 'Tell me about Z'."""
```

**Tool Composition**: Complex questions may need multiple tools.

"What are Apple's main risks and which asset managers might be affected?"
1. Vector search: Find content about Apple's risks
2. Database query: Find asset managers who own Apple
3. Synthesize: Combine into comprehensive answer

**Fallback Strategies**: When tools fail, explain why—don't hallucinate.

Production considerations:
- Security: Read-only credentials for Text2Cypher
- Performance: Limit result sizes, cache common queries
- Testing: Verify tool selection across question types

---

**Lesson 5: Congratulations & Next Steps**

What you've accomplished:
- Understand why LLMs need structured context
- Know how to build knowledge graphs with schemas, chunking, entity resolution, and vectors
- Master three retrieval patterns for different question types
- Can build agents that automate retrieval strategy selection

The complete picture:
```
Documents → Knowledge Graph → Retrievers → Agent → User
     ↓              ↓              ↓           ↓
  Chunking     Schema Design    Vector     Tool Selection
  Embeddings   Entity Resolution  VectorCypher  ReAct Pattern
                                 Text2Cypher
```

Where to go next:
- Aura Agents: No-code agent creation through Neo4j Aura's web interface
- Advanced schema design for production graphs
- Evaluation frameworks for measuring agent quality

Resources:
- Neo4j GraphRAG Developer Guide
- Microsoft Agent Framework documentation
- neo4j-graphrag Python package documentation

---

## Summary of Changes

### Content Preserved and Emphasized

| Topic | Status | Rationale |
|-------|--------|-----------|
| Vectors and Embeddings | **Core lesson** | Foundation for all semantic search |
| Schema Design | **Core lesson** | Determines what entities you can work with |
| Chunking | **Core lesson** | Affects both extraction and retrieval quality |
| Entity Resolution | **Core lesson** | Essential for graph quality |
| SimpleKGPipeline | **Integrated** | The tool that orchestrates graph construction |

### Content Consolidated or Removed

| Current Content | Recommendation |
|-----------------|----------------|
| Lab 5 Lesson 1 (GraphRAG Explained) | Merge into Lab 5 Lesson 1 as transition from Lab 3 |
| Lab 5 Lesson 2 overview + Lesson 6 choosing | Integrate into retriever lessons directly |
| Lab 6 Lessons 3, 4, 5 (three separate agent lessons) | Consolidate into "Building Your Agent" |
| Lab 6 Lesson 7 (Aura Agents) | Brief mention in wrap-up |
| Lab 6 Lesson 8 (LLM Config) | Remove (tangential to main narrative) |

### Code Reduction Approach

Lessons explain concepts with minimal, illustrative code. Implementation details stay in notebooks.

**Example transformation**:

*Before* (current Vector Retriever lesson - ~100 lines of code):
```python
from neo4j_graphrag.retrievers import VectorRetriever
vector_retriever = VectorRetriever(
    driver=driver,
    index_name='chunkEmbeddings',
    embedder=embedder,
    return_properties=['text']
)
results = vector_retriever.search(query_text=query, top_k=5)
for item in results.items:
    print(f"Score: {item.metadata['score']:.4f}")
    print(f"Content: {item.content}\n")
```

*After* (proposed):
> The Vector Retriever converts your question into an embedding and searches the vector index for similar chunks. You configure it with your database connection, index name, and embedding model. The `top_k` parameter controls how many results to return.
>
> In the notebook, you'll create a retriever and test it with questions like "What is Apple's business strategy?" Notice how it finds relevant content even when your question uses different words than the documents—that's the power of semantic search.

### Lesson Count

| Lab | Current | Proposed | Change |
|-----|---------|----------|--------|
| Lab 3 | 9 lessons | 7 lessons | -2 |
| Lab 5 | 6 lessons | 4 lessons | -2 |
| Lab 6 | 9 lessons | 5 lessons | -4 |
| **Total** | **24 lessons** | **16 lessons** | **-8** |

---

## Narrative Transitions

Each lesson ends with an explicit bridge to the next:

**Lab 3 Lesson 2 → 3**: "Traditional RAG treats documents as isolated blobs. We need structured context—a knowledge graph. Let's understand how to build one."

**Lab 3 Lesson 6 → 7**: "Even with good chunking and entity resolution, we can't find information by *meaning* yet. That's where vectors come in."

**Lab 3 → Lab 5**: "You've built a complete knowledge graph with vectors. Now let's learn how to retrieve context from it—three patterns for three kinds of questions."

**Lab 5 → Lab 6**: "You know three retrieval strategies and when each works best. But users don't want to think about this. In Lab 6, you'll build agents that make these decisions automatically."

---

## Benefits

1. **Graph construction is central**: Schema, chunking, entity resolution, and vectors are the *foundation*, not an aside
2. **Clear narrative**: Problem → Solution (graphs) → Retrieval → Automation (agents)
3. **Reduced repetition**: GraphRAG explained once, referenced thereafter
4. **Better focus**: Lessons explain concepts; notebooks show implementation
5. **Logical progression**: Each lesson builds on the previous
6. **Reduced length**: 16 vs 24 lessons (33% reduction) while keeping all essential content
7. **Clearer transitions**: Explicit bridges between all lessons and labs

---

## The Core Message

This workshop teaches that **GraphRAG is a complete system**:
- You build knowledge graphs deliberately (schema, chunking, entity resolution)
- You enable semantic search with vectors
- You retrieve context using the right pattern for each question type
- You automate pattern selection with agents

Understanding *all* of this—not just the agent at the end—is what makes someone a GraphRAG practitioner.
