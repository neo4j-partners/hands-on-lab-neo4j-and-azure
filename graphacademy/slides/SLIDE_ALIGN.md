# Slide Alignment Proposal

## Executive Summary

This proposal aligns the workshop slides with the updated 24-lesson GraphAcademy structure. Currently, there are 15 slides covering the original workshop content. This proposal identifies:

- **4 slides** that need content updates (framework changes, duplicates)
- **9 slides** that need to be created (new lessons added to modules)
- **2 organizational issues** (duplicate files, subdirectory cleanup)

---

## Current State Analysis

### Existing Slides (15 total)

**Module 1: Generative AI (6 slides)**
- ✅ 01-what-is-genai-slides.md (3.8 KB)
- ✅ 02-llm-limitations-slides.md (3.6 KB)
- ✅ 03-context-slides.md (2.3 KB)
- ✅ 04-building-the-graph-slides.md (11 KB)
- ✅ 05-schema-design-slides.md (4.6 KB)
- ✅ 06-vectors-slides.md (4.7 KB)

**Module 2: Retrievers (4 slides)**
- ✅ 07-graphrag-explained-slides.md (5.1 KB)
- ✅ 08-what-is-a-retriever-slides.md (5.9 KB)
- ⚠️ 09-setup-slides.md (1.3 KB) - Setup content
- ⚠️ 10-hands-on-retrievers-slides.md (5.6 KB) - Hands-on overview

**Module 3: Agents (5 slides)**
- ✅ 11-what-is-an-agent-slides.md (3.2 KB)
- ❌ 12-langchain-agent-slides.md (2.6 KB) - **NEEDS UPDATE: LangChain → Microsoft Agent Framework**
- ✅ 13-vector-retriever-slides.md (5.3 KB)
- ✅ 14-text2cypher-retriever-slides.md (6.2 KB)
- ✅ 15-aura-agents-slides.md (6.6 KB)

### Issues Identified

1. **Duplicate Files**: Found duplicates in `slides/slides/` subdirectory
2. **Framework Mismatch**: Slide 12 references LangChain instead of Microsoft Agent Framework
3. **Missing Content**: 9 new lessons don't have corresponding slides
4. **Numbering Gaps**: Slides skip from Module 1 (1-6) to Module 2 (7-10) to Module 3 (11-15)

---

## Target State: Updated 24-Lesson Structure

### Module 1: Building Knowledge Graphs (9 lessons → 9 slides)

| Lesson | Slide Status | Action Needed |
|--------|--------------|---------------|
| 01. What is Generative AI | ✅ Exists | None - keep as-is |
| 02. LLM Limitations | ✅ Exists | None - keep as-is |
| 03. Context | ✅ Exists | None - keep as-is |
| 04. Building the Graph | ✅ Exists | None - keep as-is |
| 05. Schema Design | ✅ Exists | None - keep as-is |
| 06. Chunking | ❌ Missing | **CREATE PLACEHOLDER** |
| 07. Entity Resolution | ❌ Missing | **CREATE PLACEHOLDER** |
| 08. Vectors | ✅ Exists | None - keep as-is |
| 09. Full Dataset | ❌ Missing | **CREATE PLACEHOLDER** (NEW) |

### Module 2: GraphRAG Retrievers (6 lessons → 6-7 slides)

| Lesson | Slide Status | Action Needed |
|--------|--------------|---------------|
| 01. GraphRAG Explained | ✅ Exists (slide 07) | Renumber to match if needed |
| 02. What is a Retriever | ✅ Exists (slide 08) | Renumber to match if needed |
| 03. Vector Retriever | ❌ Missing | **CREATE PLACEHOLDER** (NEW - hands-on focused) |
| 04. Vector Cypher Retriever | ❌ Missing | **CREATE PLACEHOLDER** (NEW - hands-on focused) |
| 05. Text2Cypher Retriever | ❌ Missing | **CREATE PLACEHOLDER** (NEW - hands-on focused) |
| 06. Choosing Retrievers | ❌ Missing | **CREATE PLACEHOLDER** (NEW - decision framework) |
| (Optional) Setup | ⚠️ Exists (slide 09) | Keep or merge into hands-on slides |

**Note:** Slide 10 (hands-on-retrievers) may overlap with new slides 13-15. Consider consolidating or repurposing.

### Module 3: Intelligent Agents (9 lessons → 7-8 slides)

| Lesson | Slide Status | Action Needed |
|--------|--------------|---------------|
| 01. What is an Agent | ✅ Exists (slide 11) | None - keep as-is |
| 02. Microsoft Agent Framework | ❌ **CRITICAL UPDATE** | **RENAME & UPDATE slide 12** from LangChain |
| 03. Simple Schema Agent | ❌ Missing | **CREATE PLACEHOLDER** (NEW - single tool agent) |
| 04. Vector Graph Agent | ✅ Partial (slide 13) | Review and align with lesson 04 |
| 05. Text2Cypher Agent | ✅ Partial (slide 14) | Review and align with lesson 05 |
| 06. Multi-Tool Design | ❌ Missing | **CREATE PLACEHOLDER** (NEW - design patterns) |
| 07. Aura Agents | ✅ Exists (slide 15) | None - keep as-is |
| 08. Best Practices | ❌ Missing | **OPTIONAL** - create if time allows |
| 09. Congratulations | N/A | Not needed for slides |

---

## Proposed Changes

### Phase 1: Critical Updates (High Priority)

#### 1.1 Rename and Update Slide 12
**File**: `12-langchain-agent-slides.md` → `12-microsoft-agent-framework-slides.md`

**Changes Required**:
- Replace all "LangChain" references with "Microsoft Agent Framework"
- Update code examples to use `AzureAIClient` instead of LangChain
- Update agent creation patterns to match Module 3 lesson 02
- Update title from "Simple LangChain Agent" to "Microsoft Agent Framework Agent"

**Content Updates**:
```diff
- # Simple LangChain Agent
+ # Microsoft Agent Framework Agent

- Uses LangChain and LangGraph for agent functionality
+ Uses Microsoft Agent Framework for agent functionality

- LangChain ReAct agent with introspection tool
+ Microsoft Agent Framework ChatAgent with introspection tool
```

#### 1.2 Clean Up Duplicate Files
**Action**: Remove or consolidate `slides/slides/` subdirectory (16 duplicate files)

### Phase 2: Create Missing Slide Placeholders (Medium Priority)

#### 2.1 Module 1 Missing Slides (3 slides)

**06-chunking-slides.md** (NEW)
```markdown
---
marp: true
theme: default
paginate: true
---

# Chunking Strategies

## PLACEHOLDER

This slide deck will cover:
- Chunk size optimization
- Overlap strategies
- Impact on retrieval quality
- Best practices for document chunking

**Content to be developed based on:**
- Module 1 Lesson 06: Chunking
- Lab 3 Notebook 3: Chunking experiments

---

# Chunk Size Matters

## PLACEHOLDER

Content about:
- Small chunks vs large chunks
- Context window considerations
- Retrieval accuracy trade-offs

---

# Practical Chunking

## PLACEHOLDER

Content about:
- Chunk overlap
- Sentence boundary detection
- Testing different chunk sizes
```

**07-entity-resolution-slides.md** (NEW)
```markdown
---
marp: true
theme: default
paginate: true
---

# Entity Resolution

## PLACEHOLDER

This slide deck will cover:
- What is entity resolution
- Deduplication strategies
- Linking entities across documents
- Canonical entity creation

**Content to be developed based on:**
- Module 1 Lesson 07: Entity Resolution
- Lab 3 examples of entity linking

---

# Why Entity Resolution Matters

## PLACEHOLDER

Content about:
- Same entities with different names
- Cross-document entity linking
- Improving graph quality

---

# Entity Resolution Techniques

## PLACEHOLDER

Content about:
- Fuzzy matching
- Canonical entity selection
- Graph-based resolution
```

**09-full-dataset-slides.md** (NEW)
```markdown
---
marp: true
theme: default
paginate: true
---

# Working with Full Datasets

## PLACEHOLDER

This slide deck will cover:
- Scaling from sample to production datasets
- Performance considerations
- Cross-document insights
- Production knowledge graph characteristics

**Content to be developed based on:**
- Module 1 Lesson 09: Full Dataset
- Lab 3 Notebook 4: Full dataset processing
- Production graph: 2145 nodes, 5070 relationships

---

# Sample vs Production Scale

## PLACEHOLDER

Content about:
- Sample: 3 documents
- Production: All EDGAR filings
- Query performance at scale

---

# Cross-Document Insights

## PLACEHOLDER

Content about:
- Finding patterns across companies
- Industry-wide risk analysis
- Regulatory compliance trends
```

#### 2.2 Module 2 Missing Slides (4 slides)

**10-vector-retriever-slides.md** (RENUMBER from existing or CREATE)
```markdown
---
marp: true
theme: default
paginate: true
---

# Vector Retriever

## PLACEHOLDER

This slide deck will cover:
- VectorRetriever class
- Semantic similarity search
- Top_k parameters
- Return properties configuration

**Content to be developed based on:**
- Module 2 Lesson 03: Vector Retriever
- Lab 5 Notebook 1: Vector retriever hands-on

---

# How Vector Retriever Works

## PLACEHOLDER

Content about:
- Question → Embedding
- Vector index search
- Cosine similarity ranking
- Chunk text retrieval

---

# Vector Retriever Use Cases

## PLACEHOLDER

Content about:
- Semantic search across documents
- Finding similar content
- Best for conceptual questions
```

**11-vector-cypher-retriever-slides.md** (NEW)
```markdown
---
marp: true
theme: default
paginate: true
---

# Vector + Cypher Retriever

## PLACEHOLDER

This slide deck will cover:
- VectorCypherRetriever class
- Semantic search + graph traversal
- Custom retrieval queries
- Enriched context with entities

**Content to be developed based on:**
- Module 2 Lesson 04: Vector Cypher Retriever
- Lab 5 Notebook 2: Vector + Cypher hands-on

---

# Two-Step Retrieval

## PLACEHOLDER

Content about:
Step 1: Vector search for relevant chunks
Step 2: Cypher query for entity context
Result: Rich, connected information

---

# Custom Retrieval Queries

## PLACEHOLDER

Content about:
- Writing retrieval_query Cypher
- Traversing from chunks to entities
- Metadata enrichment
```

**12-text2cypher-retriever-slides.md** (NEW)
```markdown
---
marp: true
theme: default
paginate: true
---

# Text2Cypher Retriever

## PLACEHOLDER

This slide deck will cover:
- Text2CypherRetriever class
- Natural language to Cypher translation
- Schema-aware query generation
- Precise graph queries

**Content to be developed based on:**
- Module 2 Lesson 05: Text2Cypher Retriever
- Lab 5 Notebook 3: Text2Cypher hands-on

---

# How Text2Cypher Works

## PLACEHOLDER

Content about:
1. User question in natural language
2. LLM generates Cypher query
3. Query executes against graph
4. Structured results returned

---

# Text2Cypher Best Practices

## PLACEHOLDER

Content about:
- Modern Cypher syntax
- Schema validation
- Query templates
- Error handling
```

**13-choosing-retrievers-slides.md** (NEW)
```markdown
---
marp: true
theme: default
paginate: true
---

# Choosing the Right Retriever

## PLACEHOLDER

This slide deck will cover:
- Decision framework for retriever selection
- Use case patterns
- Comparison table
- When to use each retriever type

**Content to be developed based on:**
- Module 2 Lesson 06: Choosing Retrievers
- Comparison of all three retriever approaches

---

# Retriever Selection Guide

## PLACEHOLDER

| Retriever | Best For | Example Query |
|-----------|----------|---------------|
| Vector | Semantic search | "What are AI risks?" |
| Vector+Cypher | Context + entities | "Which managers face crypto risks?" |
| Text2Cypher | Precise queries | "List BlackRock holdings" |

---

# Pattern Matching

## PLACEHOLDER

Content about:
- Question analysis patterns
- Selecting appropriate retriever
- Combining multiple approaches
```

#### 2.3 Module 3 Missing Slides (2 slides)

**14-simple-schema-agent-slides.md** (NEW)
```markdown
---
marp: true
theme: default
paginate: true
---

# Simple Schema Agent

## PLACEHOLDER

This slide deck will cover:
- Single-tool agent architecture
- Schema introspection tool
- Basic agent reasoning
- Foundation for multi-tool agents

**Content to be developed based on:**
- Module 3 Lesson 03: Simple Schema Agent
- Lab 6 Notebook 1: Simple agent with one tool

---

# Single Tool Agent

## PLACEHOLDER

Content about:
- One tool: get_graph_schema()
- Agent decides when to use it
- Natural language interface
- Schema exploration queries

---

# Building Block Approach

## PLACEHOLDER

Content about:
- Start simple: 1 tool
- Add complexity incrementally
- Progressive enhancement pattern
```

**17-multi-tool-design-slides.md** (NEW)
```markdown
---
marp: true
theme: default
paginate: true
---

# Multi-Tool Agent Design

## PLACEHOLDER

This slide deck will cover:
- Design patterns for multi-tool agents
- Tool selection logic
- Progressive enhancement
- Agent composition patterns

**Content to be developed based on:**
- Module 3 Lesson 06: Multi-Tool Design
- Design principles from all Lab 6 notebooks

---

# Progressive Enhancement

## PLACEHOLDER

Content about:
- 1 tool → 2 tools → 3 tools
- Each tool adds capability
- Maintaining clarity
- Tool specialization

---

# Tool Selection Intelligence

## PLACEHOLDER

Content about:
- How agents choose tools
- Tool descriptions matter
- Avoiding tool confusion
- Design anti-patterns
```

### Phase 3: Update Existing Content Alignment (Low Priority)

#### 3.1 Review and Update Slide 13
**File**: `13-vector-retriever-slides.md`
**Action**: Verify alignment with Module 3 Lesson 04 (Vector Graph Agent)
**Note**: May need title update from "Vector Retriever Tool" to "Vector Graph Agent"

#### 3.2 Review and Update Slide 14
**File**: `14-text2cypher-retriever-slides.md`
**Action**: Verify alignment with Module 3 Lesson 05 (Text2Cypher Agent)
**Note**: May need title update to clarify it's about the agent, not just the retriever

#### 3.3 Optional Best Practices Slide
**File**: `18-best-practices-slides.md` (OPTIONAL)
**Action**: Create if time allows, based on Module 3 Lesson 08
**Priority**: Low - content issue noted in lesson 08

---

## Proposed Slide Numbering

### Option A: Sequential Numbering (1-24)
Match lesson numbers exactly:
- Module 1: Slides 01-09
- Module 2: Slides 10-15
- Module 3: Slides 16-24

**Pros**: Perfect 1:1 mapping with lessons
**Cons**: Many slides to create, may be too detailed for presentation

### Option B: Presentation-Focused Numbering (1-18)
Keep essential slides, add key missing content:
- Module 1: Slides 01-09 (add 3 new: chunking, entity resolution, full dataset)
- Module 2: Slides 10-15 (add 4 new: individual retriever slides, choosing)
- Module 3: Slides 16-18 (update 12, add simple agent, multi-tool design; keep 11, 15)

**Pros**: More manageable presentation length
**Cons**: Not all lessons have slides

### Option C: Current Numbering + New (1-24)
Keep current numbering (1-15), add new as 16-24:
- Module 1: Keep 01-06, add 16-18 (chunking, entity resolution, full dataset)
- Module 2: Keep 07-10, add 19-22 (individual retrievers, choosing)
- Module 3: Keep 11-15, update 12, add 23-24 (simple agent, multi-tool design)

**Pros**: Minimal disruption to existing slides
**Cons**: Confusing numbering doesn't match lesson order

**RECOMMENDATION**: **Option B** - Presentation-focused with key content additions

---

## Implementation Plan

### Immediate Actions (Week 1)

1. **Clean up duplicates**
   - Remove or consolidate `slides/slides/` subdirectory
   - Verify no content loss

2. **Update Slide 12** (CRITICAL)
   - Rename: `12-langchain-agent-slides.md` → `12-microsoft-agent-framework-slides.md`
   - Replace all LangChain references with Microsoft Agent Framework
   - Update code examples to match Module 3 Lesson 02

3. **Create placeholder slides** (9 slides)
   - Module 1: 06-chunking, 07-entity-resolution, 09-full-dataset
   - Module 2: 10-vector-retriever, 11-vector-cypher, 12-text2cypher, 13-choosing
   - Module 3: 14-simple-schema-agent, 17-multi-tool-design

### Content Development (Week 2-3)

4. **Develop Module 1 missing slides**
   - 06-chunking-slides.md: Chunk size strategies
   - 07-entity-resolution-slides.md: Entity linking and deduplication
   - 09-full-dataset-slides.md: Scaling to production

5. **Develop Module 2 missing slides**
   - 10-vector-retriever-slides.md: Vector-only retrieval
   - 11-vector-cypher-retriever-slides.md: Hybrid retrieval
   - 12-text2cypher-retriever-slides.md: Query generation
   - 13-choosing-retrievers-slides.md: Decision framework

6. **Develop Module 3 missing slides**
   - 14-simple-schema-agent-slides.md: Single-tool agent
   - 17-multi-tool-design-slides.md: Design patterns

### Final Review (Week 4)

7. **Alignment verification**
   - Verify all slides match lesson content
   - Test presentation flow
   - Update README.md with new slide list

8. **Update documentation**
   - Update slides/README.md with new slide count
   - Update presentation timing guidelines
   - Create slide deck combinations for different workshop lengths

---

## Success Criteria

✅ All 24 lessons have corresponding slide content (or intentional exclusion)
✅ No references to "LangChain" in Module 3 slides
✅ Placeholder slides clearly marked with content sources
✅ README.md accurately reflects available slides
✅ No duplicate files in subdirectories
✅ Slide numbering is logical and consistent
✅ Presentation flow matches updated module structure

---

## Notes

- **Placeholders are intentional**: Slides marked as PLACEHOLDER indicate where content needs to be developed, with clear references to source lessons and notebooks
- **Optional slides**: Best Practices (Module 3 Lesson 08) has content issues noted; create slide only after lesson content is finalized
- **Congratulations slide**: Not needed - workshop ends with Aura Agents demo
- **Setup slides**: Consider consolidating 09-setup-slides.md into relevant hands-on sections

---

**Status**: Proposal ready for review
**Next Step**: Approve proposal and begin Phase 1 critical updates
**Estimated Effort**:
- Phase 1 (Critical): 4-6 hours
- Phase 2 (Placeholders): 2-3 hours
- Phase 3 (Content Development): 15-20 hours
