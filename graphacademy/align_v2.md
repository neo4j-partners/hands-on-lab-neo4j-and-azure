# GraphAcademy Alignment Proposal - Labs 3, 5, and 6

## Goal

Align GraphAcademy modules directly to the three main technical labs: Lab 3 (Graph Building), Lab 5 (GraphRAG Retrievers), and Lab 6 (Agents).

## Current Module Structure

**Module 1: Generative AI** (8 lessons)
1. What is Generative AI
2. LLM Limitations
3. Context
4. Building the Graph
5. Schema Design
6. Optimizing Chunk Size
7. Entity Resolution (Optional)
8. Vectors

**Module 2: Retrievers** (4 lessons)
1. Understanding GraphRAG
2. What is a Retriever
3. Setup
4. Hands-on Retrievers

**Module 3: Agents** (8 lessons)
1. What is an Agent
2. LangChain Agent (file is actually "Microsoft Agent Framework")
3. Vector Retriever
4. Text2Cypher Retriever
5. Aura Agents
6. Questions (Optional)
7. LLM Configuration (Optional)
8. Congratulations

## Lab Structure (Technical Labs Only)

**Lab 3: Graph Building** (4 notebooks)
- 01_data_loading.ipynb - Document and chunk structure
- 02_embeddings.ipynb - Embeddings and vector search
- 03_entity_extraction.ipynb - Entity extraction
- 04_full_dataset.ipynb - Full dataset loading

**Lab 5: GraphRAG Retrievers** (3 notebooks)
- 01_vector_retriever.ipynb - Vector retriever
- 02_vector_cypher_retriever.ipynb - Vector + Cypher retriever
- 03_text2cypher_retriever.ipynb - Text2Cypher retriever

**Lab 6: Agents** (3 notebooks)
- 01_simple_agent.ipynb - Simple schema agent
- 02_vector_graph_agent.ipynb - Vector + graph agent
- 03_text2cypher_agent.ipynb - Text2Cypher agent

## Alignment Analysis

### Module 1 → Lab 3 Mapping

| Module 1 Lesson | Lab 3 Notebook | Alignment |
|-----------------|----------------|-----------|
| 1. What is Generative AI | (intro) | Good - provides context |
| 2. LLM Limitations | (intro) | Good - provides context |
| 3. Context | (intro) | Good - explains why we need RAG |
| 4. Building the Graph | 01_data_loading.ipynb | Good match |
| 5. Schema Design | 03_entity_extraction.ipynb | Partial - implicit in extraction |
| 6. Optimizing Chunk Size | 02_embeddings.ipynb | Good match |
| 7. Entity Resolution | 03_entity_extraction.ipynb | Good match but marked optional |
| 8. Vectors | 02_embeddings.ipynb | Good match |

**Issues:**
- Lessons 1-3 are intro content, not directly tied to Lab 3
- Lesson 7 (Entity Resolution) is marked optional but core to Lab 3 notebook 3
- No direct lesson for Lab 3 notebook 4 (Full Dataset)

### Module 2 → Lab 5 Mapping

| Module 2 Lesson | Lab 5 Notebook | Alignment |
|-----------------|----------------|-----------|
| 1. Understanding GraphRAG | (intro) | Good - provides context |
| 2. What is a Retriever | (intro) | Good - explains concept |
| 3. Setup | (setup) | Technical setup, not theory |
| 4. Hands-on Retrievers | All 3 notebooks | Too broad - covers all three |

**Issues:**
- Only 1 lesson (lesson 4) covers the actual hands-on work
- Lesson 4 references all three retriever types but doesn't break them down
- No individual lessons for each retriever type
- Students do 3 different notebooks but only get 1 lesson of theory

### Module 3 → Lab 6 Mapping

| Module 3 Lesson | Lab 6 Notebook | Alignment |
|-----------------|----------------|-----------|
| 1. What is an Agent | (intro) | Good - provides context |
| 2. Microsoft Agent Framework | 01_simple_agent.ipynb | Good match |
| 3. Vector Retriever | 02_vector_graph_agent.ipynb | Good match |
| 4. Text2Cypher Retriever | 03_text2cypher_agent.ipynb | Good match |
| 5. Aura Agents | (no lab) | Extra content |
| 6. Questions | (practice) | Optional practice |
| 7. LLM Configuration | (optional) | Optional extra |
| 8. Congratulations | (closing) | Good - wraps up |

**Issues:**
- Module 3 README says "LangChain Agent" but file is "Microsoft Agent Framework"
- Otherwise this is the best aligned module
- Aura Agents (lesson 5) has no corresponding lab

## Proposed Restructuring

### Module 1: Building Knowledge Graphs (Lab 3)

Restructure to match the 4 notebooks in Lab 3:

1. **Introduction to Generative AI** - Foundation concepts
2. **LLM Limitations and Context** - Why we need RAG and knowledge graphs
3. **Loading Documents and Chunks** - Theory for Lab 3 notebook 1
4. **Embeddings and Vector Search** - Theory for Lab 3 notebook 2
5. **Entity Extraction** - Theory for Lab 3 notebook 3
6. **Schema Design and Entity Resolution** - Best practices for entities
7. **Optimizing Chunk Size** - Chunking strategies
8. **Working with Full Datasets** - Theory for Lab 3 notebook 4

**Changes:**
- Add new lesson 8 for full dataset concepts
- Combine schema design and entity resolution into one comprehensive lesson
- Reorder to follow the notebook sequence
- Remove "optional" tag from entity resolution

### Module 2: GraphRAG Retrievers (Lab 5)

Restructure to match the 3 notebooks in Lab 5:

1. **Introduction to GraphRAG** - What is GraphRAG and why it matters
2. **Understanding Retrievers** - Retriever concepts and types
3. **Vector Retriever** - Theory and use cases for Lab 5 notebook 1
4. **Vector Cypher Retriever** - Theory and use cases for Lab 5 notebook 2
5. **Text2Cypher Retriever** - Theory and use cases for Lab 5 notebook 3
6. **Choosing the Right Retriever** - When to use each type

**Changes:**
- Remove "Setup" lesson (move to setup labs if needed)
- Replace broad "Hands-on Retrievers" lesson with 3 specific retriever lessons
- Add lesson 6 for guidance on selecting retrievers
- Each retriever type gets dedicated theory before the lab

### Module 3: Intelligent Agents (Lab 6)

Minimal changes needed, mostly fixes:

1. **What is an Agent** - Agent concepts and architecture
2. **Microsoft Agent Framework** - Framework overview and setup
3. **Simple Schema Agent** - Theory for Lab 6 notebook 1
4. **Vector Graph Agent** - Theory for Lab 6 notebook 2
5. **Text2Cypher Agent** - Theory for Lab 6 notebook 3
6. **Multi-Tool Agent Design** - How agents select tools
7. **Best Practices** - Agent design patterns (optional)
8. **Congratulations** - Workshop summary

**Changes:**
- Fix README to say "Microsoft Agent Framework" instead of "LangChain Agent"
- Rename lesson 2 for clarity
- Rename lessons 3-5 to match notebook names
- Replace "Aura Agents" with "Multi-Tool Agent Design"
- Replace "Questions" and "LLM Configuration" with single "Best Practices" optional lesson

## Implementation Summary

### Module 1 Changes
- Add 1 new lesson (Working with Full Datasets)
- Reorder lessons to match notebook flow
- Combine and reframe schema/entity resolution content
- Remove "optional" designation from entity resolution

### Module 2 Changes
- Add 2 new lessons (one for each specific retriever: Vector Cypher and Text2Cypher had no dedicated lessons)
- Split broad "Hands-on Retrievers" into 3 specific lessons
- Add "Choosing the Right Retriever" lesson
- Remove or relocate "Setup" lesson

### Module 3 Changes
- Fix naming: LangChain → Microsoft Agent Framework
- Rename lessons to match notebooks
- Replace Aura Agents with Multi-Tool Agent Design
- Consolidate optional lessons

## Result

After restructuring:
- **Module 1**: 8 lessons aligned to 4 Lab 3 notebooks
- **Module 2**: 6 lessons aligned to 3 Lab 5 notebooks
- **Module 3**: 8 lessons aligned to 3 Lab 6 notebooks

Each lab notebook has corresponding theory in the module, and students can follow a clear path from concept to practice.
