# Workshop Restructuring Proposal

## Problem Statement

The current workshop mixes no-code and coding labs without clear separation. Attendees who want a quick introduction to Neo4j and AI agents must work through development environment setup (Codespace) before they can explore Aura Agents. This creates a poor experience for:

1. Business users and executives who want to see AI agent capabilities without coding
2. Workshop facilitators who want to offer a shorter no-code track
3. Developers who want to skip basics and jump into coding

The current Lab 1 bundles four distinct activities (signup, restore, explore, agents) into one lab, making it difficult to split the workshop into tracks.

## Proposed Solution

Restructure the workshop into two distinct parts:

**Part 1: No-Code Track** - Getting started with Neo4j and Foundry Agents without any coding. Attendees use the pre-built knowledge graph and visual tools only.

**Part 2: Coding Track** - Advanced development using Python notebooks, building knowledge graphs from scratch, and creating custom agents programmatically.

This allows facilitators to:
- Run a 1-hour executive demo (Part 1 only)
- Run a full 3-4 hour developer workshop (both parts)
- Let attendees skip Part 1 if they already have Aura credentials

## New Lab Structure

### Part 1: No-Code Getting Started

| New Lab | Old Lab | Content | Duration |
|---------|---------|---------|----------|
| Lab 0: Sign In | Lab 0 | Azure portal sign-in | 5 min |
| Lab 1: Neo4j Aura Setup | Lab 1 (parts 1-3) | Marketplace signup, restore backup, visual exploration | 15 min |
| Lab 2: Aura Agents | Lab 1 (part 4) | Build AI agents using Neo4j Aura Agent (no code) | 20 min |
| Lab 3: Foundry Agents | Lab 3 | Microsoft Foundry setup and agent creation | 15 min |

### Part 2: Coding and Advanced Development

| New Lab | Old Lab | Content | Duration |
|---------|---------|---------|----------|
| Lab 4: Start Codespace | Lab 2 | GitHub Codespace setup, environment config | 10 min |
| Lab 5: Building Knowledge Graph | Lab 4 | Data loading, embeddings, entity extraction (4 notebooks) | 30 min |
| Lab 6: GraphRAG Retrievers | Lab 5 | Vector, VectorCypher, Text2Cypher retrievers (3 notebooks) | 30 min |
| Lab 7: GraphRAG Agents | Lab 6 | Schema, Vector+Graph, Multi-tool agents (3 notebooks) | 30 min |
| Lab 8: Hybrid Search | Lab 7 | Fulltext and hybrid search (2 notebooks, optional) | 20 min |

---

## Requirements

### Directory Renaming

1. Rename `Lab_1_Neo4j_Aura` to `Lab_1_Aura_Setup`
2. Create new directory `Lab_2_Aura_Agents`
3. Keep `Lab_3_Foundry_Agents` (name stays same but becomes Part 1)
4. Rename `Lab_2_Start_Codespace` to `Lab_4_Start_Codespace`
5. Rename `Lab_4_Neo4j_GraphRag` to `Lab_5_Knowledge_Graph`
6. Rename `Lab_5_GraphRAG_Retrievers` to `Lab_6_Retrievers`
7. Rename `Lab_6_Agents` to `Lab_7_Agents`
8. Rename `Lab_7_Hybrid_Search` to `Lab_8_Hybrid_Search`

### Content Splitting for Lab 1

Current Lab 1 README has four parts. Split as follows:

**New Lab 1 (Aura Setup):**
- Part 1: Neo4j Aura Signup (keep Neo4j_Aura_Signup.md)
- Part 2: Restore the Backup (keep in README)
- Part 3: Explore the Knowledge Graph (keep EXPLORE.md)

**New Lab 2 (Aura Agents):**
- Part 4: Build an Aura Agent (move AURA_AGENTS.md to new lab)

### Prerequisite Updates

Every lab README must update its prerequisites section:

| Lab | Prerequisites |
|-----|---------------|
| Lab 0 | None |
| Lab 1 | Lab 0 |
| Lab 2 | Lab 0, Lab 1 |
| Lab 3 | Lab 0, Lab 1 |
| Lab 4 | Lab 0, Lab 1 (credentials only) |
| Lab 5 | Lab 0, Lab 1, Lab 4 |
| Lab 6 | Lab 0, Lab 1, Lab 4, Lab 5 |
| Lab 7 | Lab 0, Lab 1, Lab 4, Lab 5, Lab 6 |
| Lab 8 | Lab 0, Lab 1, Lab 4, Lab 5 |

### Main README Updates

The root README.md agenda must be restructured to show two parts:

**Part 1 - No-Code Getting Started**
- Lab 0: Sign In
- Lab 1: Neo4j Aura Setup
- Lab 2: Aura Agents
- Lab 3: Foundry Agents

**Part 2 - Coding and Advanced Development**
- Lab 4: Start Codespace
- Lab 5: Building a Knowledge Graph
- Lab 6: GraphRAG Retrievers
- Lab 7: GraphRAG Agents
- Lab 8: Hybrid Search (Optional)

### GraphAcademy Content Updates

The graphacademy folder has content aligned to old lab numbers. Update all references:

1. graphacademy/README.md - Module references to labs
2. graphacademy/slides/README.md - Lab breakdown section
3. All files in graphacademy/lab-4-neo4j-graphrag/ - now Lab 5
4. All files in graphacademy/lab-5-retrievers/ - now Lab 6
5. All files in graphacademy/lab-6-agents/ - now Lab 7
6. Slides folders must be renamed to match new lab numbers

### Notebook File Renaming

Notebooks use numbering prefixes that align with old structure. Consider renaming:

**Lab 5 (old Lab 4) notebooks:**
- 01_data_loading.ipynb (keep as-is, internal to lab)
- 02_embeddings.ipynb (keep as-is)
- 03_entity_extraction.ipynb (keep as-is)
- 04_full_dataset.ipynb (keep as-is)

**Lab 6 (old Lab 5) notebooks:**
- 01_vector_retriever.ipynb (keep as-is)
- 02_vector_cypher_retriever.ipynb (keep as-is)
- 03_text2cypher_retriever.ipynb (keep as-is)

**Lab 7 (old Lab 6) notebooks:**
- 01_simple_agent.ipynb (keep as-is)
- 02_vector_graph_agent.ipynb (keep as-is)
- 03_text2cypher_agent.ipynb (keep as-is)

### new-workshops Folder Updates

The new-workshops/main.py menu references old lab numbers. Update menu item descriptions to reflect new lab numbers.

### AURA_AGENTS.md Prerequisites Fix

Current AURA_AGENTS.md says it requires Labs 2 and 3 (knowledge graph built with embeddings). This is incorrect for the no-code track. The backup file already contains the knowledge graph. Update to state:

"Prerequisite: Completed Lab 1 (Aura setup with backup restored)"

---

## Detailed Checklist

### Phase 1: Directory Structure Changes (COMPLETE)

- [x] Create new directory `Lab_2_Aura_Agents/`
- [x] Create new directory `Lab_2_Aura_Agents/images/`
- [x] Move `Lab_1_Neo4j_Aura/AURA_AGENTS.md` to `Lab_2_Aura_Agents/README.md`
- [x] Copy relevant images from Lab_1 to Lab_2 for AURA_AGENTS content
- [x] Rename `Lab_2_Start_Codespace/` to `Lab_4_Start_Codespace/`
- [x] Rename `Lab_4_Neo4j_GraphRag/` to `Lab_5_Knowledge_Graph/`
- [x] Rename `Lab_5_GraphRAG_Retrievers/` to `Lab_6_Retrievers/`
- [x] Rename `Lab_6_Agents/` to `Lab_7_Agents/`
- [x] Rename `Lab_7_Hybrid_Search/` to `Lab_8_Hybrid_Search/`
- [x] Rename `Lab_1_Neo4j_Aura/` to `Lab_1_Aura_Setup/`

### Phase 2: Lab 1 Content Updates (COMPLETE)

- [x] Edit `Lab_1_Aura_Setup/README.md` to remove Part 4 (Aura Agents section)
- [x] Update Next Steps in Lab 1 to point to Lab 2 (Aura Agents)
- [x] Verify Lab 1 only covers: signup, restore, explore

### Phase 3: Lab 2 (New Aura Agents Lab) Content (COMPLETE)

- [x] Create `Lab_2_Aura_Agents/README.md` from AURA_AGENTS.md content
- [x] Update prerequisites to say: "Completed Lab 1 (Aura Setup)"
- [x] Remove incorrect reference to Labs 2 and 3 for knowledge graph building
- [x] Add "Next Steps" pointing to Lab 3 (Foundry Agents)
- [x] Move these images to Lab_2_Aura_Agents/images/:
  - [x] aura_agents.png
  - [x] add_cypher_template_tool.png
  - [x] agent_tool_shared_risk.png
  - [x] similiarity_search_tool.png
  - [x] text2cypher_tool.png
  - [x] apple_query_agent.png
  - [x] apple_agent_reasoning.png
  - [x] ai_ml_agent_response.png
  - [x] company_risk_factors.png

### Phase 4: Lab 3 Content Updates (COMPLETE)

- [x] Update `Lab_3_Foundry_Agents/README.md` prerequisites
- [x] Change from "Completed Labs 0, 1, 2" to "Completed Labs 0, 1"
- [x] Remove reference to Lab 2 (Codespace) as prerequisite
- [x] Update "What's Next" to say Lab 4 (Start Codespace) or Lab 5 (Knowledge Graph)
- [x] Add note that Lab 3 completes the No-Code track

### Phase 5: Lab 4 Content Updates (formerly Lab 2) (COMPLETE)

- [x] Update `Lab_4_Start_Codespace/README.md` title to "Lab 4 - Start Codespace"
- [x] Update prerequisites to reference correct lab numbers
- [x] Update all internal references to other labs
- [x] Update link to ../GUIDE_DEV_CONTAINERS.md if needed
- [x] Update "What's Next" to point to Lab 5

### Phase 6: Lab 5 Content Updates (formerly Lab 4) (COMPLETE)

- [x] Update `Lab_5_Knowledge_Graph/README.md` title
- [x] Update prerequisites to reference Labs 0, 1, 4
- [x] Update "Next Steps" reference to Lab 6 (Retrievers)
- [x] Update any cross-references to other labs in notebooks

### Phase 7: Lab 6 Content Updates (formerly Lab 5) (COMPLETE)

- [x] Update `Lab_6_Retrievers/README.md` title
- [x] Update prerequisites to reference Labs 0, 1, 4, 5
- [x] Update all lab number references in the README
- [x] Update "Next Steps" reference to Lab 7 (Agents)

### Phase 8: Lab 7 Content Updates (formerly Lab 6) (COMPLETE)

- [x] Update `Lab_7_Agents/README.md` title
- [x] Update prerequisites to reference Labs 0, 1, 4, 5, 6
- [x] Update all lab number references in the README
- [x] Update "Next Steps" reference to Lab 8 (Hybrid Search)

### Phase 9: Lab 8 Content Updates (formerly Lab 7) (COMPLETE)

- [x] Update `Lab_8_Hybrid_Search/README.md` title
- [x] Update prerequisites to reference Labs 0, 1, 4, 5
- [x] Mark as optional extension lab

### Phase 10: Main README Updates (COMPLETE)

- [x] Update root `README.md` agenda with new part structure
- [x] Update Part 1 heading to "Part 1 - No-Code Getting Started"
- [x] Add Lab 2 (Aura Agents) to agenda
- [x] Update Part 2+ headings to reflect new structure
- [x] Renumber all lab references in the agenda
- [x] Update "Starting the Lab" section shortcuts
- [x] Update Windows Setup Guide lab references

### Phase 11: GUIDE_DEV_CONTAINERS.md Updates (COMPLETE)

- [x] Update all lab number references in GUIDE_DEV_CONTAINERS.md
- [x] Update references to Lab 4 (now Lab 5) for notebook examples
- [x] Fixed image path from Lab_2 to Lab_4
- [x] Fixed next lab reference from Lab 3 to Lab 5

### Phase 12: GraphAcademy README Updates (COMPLETE)

- [x] Update `graphacademy/README.md` module alignments
- [x] Change "Aligned with Lab 4" to "Aligned with Lab 5"
- [x] Change "Aligned with Lab 5" to "Aligned with Lab 6"
- [x] Change "Aligned with Lab 6" to "Aligned with Lab 7"

### Phase 13: GraphAcademy Slides README Updates (COMPLETE)

- [x] Update `graphacademy/slides/README.md` lab references
- [x] Update "Lab Breakdown" section with new lab numbers
- [x] Update Lab 4/5/6 references throughout

### Phase 14: GraphAcademy Slides Directory Renaming (COMPLETE)

- [x] Rename `graphacademy/slides/lab-4-neo4j-graphrag/` to `graphacademy/slides/lab-5-knowledge-graph/`
- [x] Rename `graphacademy/slides/lab-5-retrievers/` to `graphacademy/slides/lab-6-retrievers/`
- [x] Rename `graphacademy/slides/lab-6-agents/` to `graphacademy/slides/lab-7-agents/`

### Phase 15: GraphAcademy Content Directory Renaming (COMPLETE)

- [x] Rename `graphacademy/lab-4-neo4j-graphrag/` to `graphacademy/lab-5-knowledge-graph/`
- [x] Rename `graphacademy/lab-5-retrievers/` to `graphacademy/lab-6-retrievers/`
- [x] Rename `graphacademy/lab-6-agents/` to `graphacademy/lab-7-agents/`

### Phase 16: GraphAcademy Content File Updates (COMPLETE)

- [x] graphacademy/lab-5-knowledge-graph/ files - Fixed all "Back to Lab" references
- [x] graphacademy/lab-6-retrievers/ files - Fixed all lab references and navigation
- [x] graphacademy/lab-7-agents/ files - Fixed all lab references and navigation
- [x] Fixed README titles (Lab 5, Lab 6, Lab 7)
- [x] Fixed all internal cross-references between modules

### Phase 17: GraphAcademy Slides File Updates (COMPLETE)

- [x] Directory names updated
- [x] Fixed lab-5-knowledge-graph/07-vectors-slides.md "Lab 5" → "Lab 6" for retrievers
- [x] Fixed lab-1-neo4j-aura/05-sec-filings-graph-slides.md "Lab 3" → "Lab 5" for knowledge graph
- [x] Fixed lab-7-agents slides body text references

### Phase 18: new-workshops Updates (COMPLETE)

- [x] Added lab alignment comments to `new-workshops/main.py` (01_xx=Lab 5, 02_xx=Lab 6, 03_xx=Lab 7, 05_xx=Lab 8)

### Phase 19: Verification (COMPLETE)

- [x] Verify all internal links work (README references to other files)
- [x] Verify all image paths work after moves
- [x] Verify notebook kernel references are correct
- [x] Run through Part 1 labs to verify flow
- [x] Run through Part 2 labs to verify flow
- [x] Check for any remaining references to old lab numbers using grep
- [x] Fixed GUIDE_DEV_CONTAINERS.md image path
- [x] Fixed README.md Windows Setup Guide path

---

## Files Requiring Changes (Complete List)

### Root Level Files
1. README.md
2. GUIDE_DEV_CONTAINERS.md

### Lab README Files
3. Lab_0_Sign_In/README.md (minimal - verify)
4. Lab_1_Aura_Setup/README.md (major rewrite)
5. Lab_2_Aura_Agents/README.md (new file from AURA_AGENTS.md)
6. Lab_3_Foundry_Agents/README.md (update prerequisites and next steps)
7. Lab_4_Start_Codespace/README.md (renumber references)
8. Lab_5_Knowledge_Graph/README.md (renumber references)
9. Lab_6_Retrievers/README.md (renumber references)
10. Lab_7_Agents/README.md (renumber references)
11. Lab_8_Hybrid_Search/README.md (renumber references)

### GraphAcademy Root
12. graphacademy/README.md

### GraphAcademy Slides
13. graphacademy/slides/README.md
14-20. All slide files in lab-5/lab-6/lab-7 folders

### GraphAcademy Content
21-35. All markdown files in graphacademy content folders

### New Workshops
36. new-workshops/main.py
37. new-workshops/README.md

### REQS.md
38. REQS.md (if it references lab structure)

---

## Success Criteria

1. Part 1 can be completed without any coding or Codespace setup
2. Part 2 begins with Codespace setup and all coding labs follow
3. All internal links and references work correctly
4. All prerequisites are accurate for the new structure
5. GraphAcademy content aligns with new lab numbers
6. No orphaned files or broken image references

---

## Next Steps

1. Review and approve this proposal
2. Execute the checklist in order (phases 1-19)
3. Test both workshop tracks end-to-end
4. Update any external links or documentation that reference this workshop
