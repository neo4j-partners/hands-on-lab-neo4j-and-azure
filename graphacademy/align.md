# GraphAcademy Restructuring Proposal

## Current State

GraphAcademy currently has 3 modules with 20 lessons total:

**Module 1: Generative AI** (8 lessons)
- What is Generative AI
- LLM Limitations
- Context
- Building the Graph
- Schema Design
- Optimizing Chunk Size
- Entity Resolution (Optional)
- Vectors

**Module 2: Retrievers** (4 lessons)
- Understanding GraphRAG
- What is a Retriever
- Setup
- Hands-on Retrievers

**Module 3: Agents** (8 lessons)
- What is an Agent
- Microsoft Agent Framework (note: README says "LangChain Agent" but file exists as "Microsoft Agent Framework")
- Vector Retriever
- Text2Cypher Retriever
- Aura Agents
- Questions (Optional)
- LLM Configuration (Optional)
- Congratulations

## Lab Structure

The actual hands-on labs consist of:

**Setup Labs:**
- Lab 0: Sign In (Azure setup)
- Lab 1: Neo4j Aura Signup (database setup)
- Lab 2: Start Codespace (development environment)

**Technical Labs:**
- Lab 3: Graph Building (4 notebooks: data loading, embeddings, entity extraction, full dataset)
- Lab 4: Explore Knowledge Graph (visual exploration using Neo4j Explore tool)
- Lab 5: GraphRAG Retrievers (3 notebooks: vector, vector+cypher, text2cypher)
- Lab 6: Agents (3 notebooks: simple agent, vector+graph agent, text2cypher agent)
- Lab 7: Hybrid Search (2 notebooks: fulltext, hybrid search)

## Key Gaps and Misalignments

### 1. Missing Module Content

**Lab 4 (Graph Exploration) has no corresponding module**
- Lab 4 teaches visual graph exploration using Neo4j Explore
- Students learn to navigate the graph, use graph algorithms, and understand centrality
- This is important for understanding graph structure before building applications
- Currently no theory or explanation in any module

**Lab 7 (Hybrid Search) has no corresponding module**
- Lab 7 introduces fulltext search and hybrid search combining vector and keyword approaches
- This is an advanced retrieval technique not covered in Module 2
- Students encounter this lab without prior context or explanation

**Setup Labs (0-2) have no corresponding module**
- These labs are currently standalone without explanatory content
- Students dive into Azure and Neo4j setup without understanding why
- Missing explanation of the overall architecture and what they're building

### 2. Incomplete or Mismatched Coverage

**Module 1 Schema Design lesson is implicit in Lab 3**
- Module 1 Lesson 5 covers Schema Design theory
- Lab 3 entity extraction implicitly uses schemas but doesn't explicitly teach design
- Connection between theory and practice is unclear

**Module 3 README mentions LangChain but content uses Microsoft Agent Framework**
- The actual lesson file is named "02-microsoft-agent-framework.md"
- The main README.md still references "LangChain Agent"
- Lab 6 uses Microsoft Agent Framework exclusively
- This creates confusion about which framework is being taught

**Module 1 Entity Resolution is optional but core to Lab 3**
- Module 1 Lesson 7 is marked optional
- Lab 3 includes entity extraction as a core component in notebook 03
- This minimizes an important concept

### 3. Module-to-Lab Mapping Issues

**Current mapping is not intuitive:**
- Module 1 maps to Lab 3 (but students do Labs 0-2 first)
- Module 2 maps to Lab 5 (skipping Lab 4)
- Module 3 maps to Lab 6 (skipping Lab 7)
- Students experience setup labs before Module 1 content

## Proposed Restructuring

### Approach 1: Module-First Structure (Aligns modules to labs in order)

Create modules that match the lab sequence students actually experience:

**Module 0: Workshop Setup and Prerequisites**
- Lesson 1: Workshop Overview and Architecture
- Lesson 2: Azure Sign In (Lab 0 guide)
- Lesson 3: Neo4j Aura Setup (Lab 1 guide)
- Lesson 4: Development Environment (Lab 2 guide)
- Lesson 5: What is Generative AI
- Lesson 6: LLM Limitations and Context

**Module 1: Building Knowledge Graphs**
- Lesson 1: Introduction to Knowledge Graphs
- Lesson 2: Document and Chunk Structure (corresponds to Lab 3 notebook 1)
- Lesson 3: Embeddings and Vector Search (corresponds to Lab 3 notebook 2)
- Lesson 4: Entity Extraction and Semantic Graphs (corresponds to Lab 3 notebook 3)
- Lesson 5: Schema Design Best Practices
- Lesson 6: Optimizing Chunk Size
- Lesson 7: Entity Resolution Techniques
- Lesson 8: Working with Full Datasets (corresponds to Lab 3 notebook 4)

**Module 2: Graph Exploration and Analysis**
- Lesson 1: Visual Graph Exploration (corresponds to Lab 4)
- Lesson 2: Graph Algorithms and Centrality
- Lesson 3: Pattern Discovery
- Lesson 4: Using Neo4j Explore

**Module 3: GraphRAG Retrievers**
- Lesson 1: Understanding GraphRAG
- Lesson 2: What is a Retriever
- Lesson 3: Vector Retriever (corresponds to Lab 5 notebook 1)
- Lesson 4: Vector Cypher Retriever (corresponds to Lab 5 notebook 2)
- Lesson 5: Text2Cypher Retriever (corresponds to Lab 5 notebook 3)
- Lesson 6: Fulltext Search (corresponds to Lab 7 notebook 1)
- Lesson 7: Hybrid Search (corresponds to Lab 7 notebook 2)
- Lesson 8: Choosing the Right Retriever

**Module 4: Building Intelligent Agents**
- Lesson 1: What is an Agent
- Lesson 2: Microsoft Agent Framework Overview
- Lesson 3: Simple Schema Agent (corresponds to Lab 6 notebook 1)
- Lesson 4: Vector Graph Agent (corresponds to Lab 6 notebook 2)
- Lesson 5: Text2Cypher Agent (corresponds to Lab 6 notebook 3)
- Lesson 6: Multi-Tool Agent Design
- Lesson 7: Aura Agents (Optional)
- Lesson 8: LLM Configuration (Optional)
- Lesson 9: Congratulations and Next Steps

### Approach 2: Keep 3 Modules but Expand Coverage (Minimal restructuring)

Keep the current 3-module structure but add missing content:

**Module 1: Generative AI and Knowledge Graphs** (expand from 8 to 11 lessons)
- Keep existing lessons 1-8
- Add Lesson 9: Graph Exploration and Visualization (covers Lab 4)
- Add Lesson 10: Graph Algorithms (covers Lab 4)
- Add Lesson 11: Setup Prerequisites (consolidate Labs 0-2 overview)

**Module 2: Retrievers** (expand from 4 to 8 lessons)
- Keep existing lessons 1-4
- Add Lesson 5: Fulltext Search (covers Lab 7 notebook 1)
- Add Lesson 6: Hybrid Search (covers Lab 7 notebook 2)
- Add Lesson 7: Choosing the Right Retriever
- Add Lesson 8: Advanced Retrieval Patterns

**Module 3: Agents** (keep 8 lessons but fix references)
- Update Lesson 2 name in README from "LangChain Agent" to "Microsoft Agent Framework"
- Keep all other lessons as is
- Ensure all references consistently use "Microsoft Agent Framework"

### Approach 3: Lab-Embedded Structure (Radical restructuring)

Restructure to embed theory directly before each lab:

**Module 1: Getting Started**
- Theory: Workshop Overview, GenAI Basics, LLM Limitations
- Labs: Lab 0 (Azure), Lab 1 (Neo4j), Lab 2 (Codespace)

**Module 2: Building Knowledge Graphs**
- Theory: Knowledge Graphs, Schema Design, Chunking, Entity Extraction, Vectors
- Lab: Lab 3 (all 4 notebooks)

**Module 3: Exploring Your Knowledge Graph**
- Theory: Graph Visualization, Algorithms, Pattern Discovery
- Lab: Lab 4 (Neo4j Explore)

**Module 4: Retrieval Strategies**
- Theory: GraphRAG, Retriever Types, Vector Search, Hybrid Search
- Labs: Lab 5 (Retrievers), Lab 7 (Hybrid Search)

**Module 5: Intelligent Agents**
- Theory: Agent Concepts, Microsoft Agent Framework, Multi-Tool Design
- Lab: Lab 6 (all 3 notebooks)

## Recommendation

**Approach 2 (Keep 3 Modules but Expand)** is recommended because:

1. **Minimal disruption** - Keeps existing content structure
2. **Fills gaps** - Adds missing content for Labs 4 and 7
3. **Fixes inconsistencies** - Corrects LangChain/Microsoft Agent Framework naming
4. **Maintains simplicity** - Three modules is clean and manageable
5. **Backward compatible** - Existing slides and references mostly still work

## Implementation Steps

### Phase 1: Fix Immediate Issues
1. Update Module 3 README to say "Microsoft Agent Framework" instead of "LangChain Agent"
2. Add a brief intro lesson to Module 1 that references Labs 0-2
3. Change Module 1 Lesson 7 (Entity Resolution) from "Optional" to core

### Phase 2: Add Missing Content
1. Add 3 new lessons to Module 1 for graph exploration and visualization (Lab 4 content)
2. Add 3 new lessons to Module 2 for fulltext and hybrid search (Lab 7 content)

### Phase 3: Enhance Lab Connections
1. Add clear callouts in module lessons showing which lab notebooks they correspond to
2. Add "Prerequisites" section to each module showing which labs must be completed
3. Add "Related Notebooks" section to each lesson pointing to specific lab notebooks

### Phase 4: Polish and Review
1. Review all lessons for consistency in terminology
2. Ensure all navigation links work correctly
3. Update main README with new lesson count and structure
4. Add a visual diagram showing module-to-lab mapping

## Summary

The current GraphAcademy structure has solid foundational content but is missing coverage for two important labs (Lab 4 graph exploration and Lab 7 hybrid search) and has naming inconsistencies around the agent framework. The recommended approach is to expand the existing 3-module structure to add the missing content rather than doing a complete restructuring. This keeps disruption minimal while ensuring all lab activities have corresponding theoretical content for students to learn from.
