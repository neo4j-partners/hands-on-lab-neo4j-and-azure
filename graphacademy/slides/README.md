# Workshop Slides

This folder contains presentation-ready slides extracted from the workshop lessons. All slides are formatted for [Marp](https://marp.app/), a markdown presentation tool.

## 📊 Available Presentations

All slides are sequentially numbered 01-22 for easy navigation, aligned with the 24-lesson GraphAcademy structure.

### Module 1: Building Knowledge Graphs (Slides 1-9)

**01. What is Generative AI** (4.2 KB)
   - Introduction to Generative AI
   - Large Language Models (LLMs)
   - Knowledge Graphs & Cypher
   - Retrieval Augmented Generation (RAG)

**02. LLM Limitations** (4.0 KB)
   - LLM Cautions & Limitations
   - Access to Data Issues
   - Hallucination Problem
   - Temperature Settings
   - Transparency Concerns

**03. Context** (2.6 KB)
   - Importance of Context
   - Avoiding Hallucination
   - Improving LLM Responses

**04. Building the Graph** (11 KB) ⭐ **Largest**
   - Complete GraphRAG Pipeline
   - EDGAR SEC Filings Processing
   - Entity Extraction
   - Schema-Driven Knowledge Graphs
   - Structured Data Integration

**05. Schema Design** (4.7 KB)
   - Schema Purpose & Benefits
   - Node and Relationship Definitions
   - Pattern Specifications
   - Iterative Schema Development
   - Balancing Flexibility and Structure

**06. Chunking Strategies** (5.1 KB) 🆕
   - Chunk Size Optimization
   - Large vs Small Chunk Trade-offs
   - FixedSizeSplitter Configuration
   - Chunk Overlap Strategies
   - Impact on Entity Extraction
   - Best Practices by Document Type

**07. Entity Resolution** (6.3 KB) 🆕
   - Entity Duplication Problem
   - Default Resolution Strategies
   - Post-Processing Resolvers (Spacy, FuzzyMatch)
   - Conservative vs Aggressive Resolution
   - Best Practices and Testing

**08. Vectors** (4.8 KB)
   - Vector Fundamentals
   - Embeddings & Similarity
   - Vector Search in Neo4j
   - Document Chunking

**09. Working with Full Datasets** (7.3 KB) 🆕
   - Sample to Production Scale Journey
   - Full Dataset Statistics (2,145 nodes, 5,070 relationships)
   - Cross-Document Insights
   - Search Quality at Scale
   - Performance Considerations

### Module 2: GraphRAG Retrievers (Slides 10-15)

**10. GraphRAG Explained** (5.2 KB)
   - What is GraphRAG?
   - Benefits of GraphRAG
   - Graph-Enhanced Vector Search
   - Full Text Search
   - Text to Cypher

**11. What is a Retriever** (6.3 KB)
   - Vector Retriever Overview
   - Vector + Cypher Retriever Overview
   - Text2Cypher Retriever Overview
   - Choosing the Right Retriever

**12. Vector Retriever (Detailed)** (6.0 KB) 🆕
   - Vector Retriever Fundamentals
   - How Vector Search Works (5-step process)
   - Components: Embedder, Vector Index, Similarity, Top-K
   - Configuration and Code Examples
   - Best Practices and Use Cases
   - Limitations

**13. Vector + Cypher Retriever (Detailed)** (8.9 KB) 🆕
   - Hybrid Retrieval (Semantic + Graph)
   - Two-Step Process Explained
   - Custom Retrieval Query Patterns
   - OPTIONAL MATCH Usage
   - Advanced Traversals and Metadata
   - Performance Considerations

**14. Text2Cypher Retriever (Detailed)** (8.1 KB) 🆕
   - Natural Language to Cypher Conversion
   - Schema's Critical Role
   - LLM Query Generation Process
   - Modern Cypher Syntax Best Practices
   - Complex Query Handling
   - Error Handling and Validation

**15. Choosing the Right Retriever** (9.6 KB) 🆕
   - Decision Framework (3 Key Questions)
   - Content vs Facts Analysis
   - Question Pattern Guides for Each Retriever
   - Real-World Question Analysis Examples
   - Decision Tree
   - Practice Examples with Answers

### Module 3: Intelligent Agents (Slides 16-22)

**16. What is an Agent** (3.7 KB)
   - What are Agents?
   - Agents vs Retrievers
   - Conversational Wrappers
   - Agent Reasoning & Tools

**17. Microsoft Agent Framework** (3.6 KB) 🆕
   - Building Agents with Microsoft Agent Framework
   - AzureAIClient Setup
   - Schema Tools
   - Agent Architecture
   - Tool Definition as Python Functions

**18. Simple Schema Agent** (8.9 KB) 🆕
   - Single-Tool Agent Fundamentals
   - Schema Tool as First Agent Tool
   - How Agents Decide Which Tool to Use
   - Agent Instructions and Streaming
   - Advantages and Limitations
   - Microsoft Foundry Integration

**19. Vector Graph Agent** (5.4 KB)
   - Vector + Graph Retrieval Tool
   - Two-Tool Agent Architecture
   - Automatic Tool Selection
   - Multi-Step Reasoning
   - Progressive Agent Building

**20. Text2Cypher Agent** (6.4 KB)
   - Text2Cypher Query Tool
   - Three-Tool Agent Capabilities
   - Complete GraphRAG Agent
   - Intelligent Multi-Tool Reasoning
   - Real-World Applications

**21. Multi-Tool Agent Design** (11.8 KB) 🆕
   - Tool Selection Process
   - Progressive Enhancement Pattern
   - Tool Specialization Principles
   - Design Patterns (Naming, Docstrings, Composition)
   - Anti-Patterns to Avoid
   - The GraphRAG "Sweet Spot" (3 Tools)
   - Real-World Patterns

**22. Aura Agents** (7.1 KB)
   - No-Code Aura Agents
   - Tool Types & Configuration
   - Testing & Deployment
   - Example Agents

## 🚀 How to Use These Slides

### Option 1: Marp CLI (Recommended)

Install Marp CLI:
```bash
npm install -g @marp-team/marp-cli
```

**Present slides:**
```bash
cd /path/to/slides
marp 01-what-is-genai-slides.md --server
```

**Export to PDF:**
```bash
marp 01-what-is-genai-slides.md --pdf
```

**Export to HTML:**
```bash
marp 01-what-is-genai-slides.md --html
```

**Export all slides:**
```bash
marp *.md --pdf --allow-local-files
```

### Option 2: VS Code with Marp Extension

1. Install the [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) extension
2. Open any slide file
3. Click "Open Preview" button or press `Cmd+K V`
4. Present using the preview window

### Option 3: Marp Web

1. Visit [Marp Web](https://web.marp.app/)
2. Copy and paste slide content
3. Present directly in browser

## 📝 Slide Format

All slides use Marp markdown format:

```markdown
---
marp: true
theme: default
paginate: true
---

# Slide Title

Content here

---

# Next Slide

More content
```

### Features Included

✅ **Pagination** - Automatic slide numbering
✅ **Images** - All images linked to `../images/`
✅ **Code Blocks** - Syntax-highlighted Cypher and Python
✅ **Tables** - Comparison and decision matrices
✅ **Two-Column Layouts** - Where appropriate
✅ **Consistent Styling** - Professional appearance

## 🎨 Customizing Theme

To use a different Marp theme, change the YAML frontmatter:

```markdown
---
marp: true
theme: gaia
paginate: true
backgroundColor: #fff
---
```

Available themes:
- `default` - Clean, professional
- `gaia` - Colorful, modern
- `uncover` - Minimalist, centered

Or create your own custom theme!

## 📊 Presentation Order

### For Full Workshop (5 hours):

**Part 1: GenAI Fundamentals (90 min)**
1. Slide 01: What is Generative AI (15 min)
2. Slide 02: LLM Limitations (15 min)
3. Slide 03: Context (10 min)
4. Slide 04: Building the Graph (20 min)
5. Slide 05: Schema Design (10 min)
6. Slide 06: Chunking Strategies (10 min)
7. Slide 07: Entity Resolution (10 min)

**Part 2: Vectors & Full Scale (40 min)**
8. Slide 08: Vectors (20 min)
9. Slide 09: Working with Full Datasets (20 min)

**Part 3: GraphRAG Retrievers (90 min)**
10. Slide 10: GraphRAG Explained (15 min)
11. Slide 11: What is a Retriever (15 min)
12. Slide 12: Vector Retriever (15 min)
13. Slide 13: Vector + Cypher Retriever (20 min)
14. Slide 14: Text2Cypher Retriever (15 min)
15. Slide 15: Choosing the Right Retriever (10 min)

**Part 4: Intelligent Agents (90 min)**
16. Slide 16: What is an Agent (10 min)
17. Slide 17: Microsoft Agent Framework (15 min)
18. Slide 18: Simple Schema Agent (15 min)
19. Slide 19: Vector Graph Agent (15 min)
20. Slide 20: Text2Cypher Agent (15 min)
21. Slide 21: Multi-Tool Agent Design (10 min)
22. Slide 22: Aura Agents (10 min)

### For Short Workshop (2.5 hours):

**Essential Slides:**
1. Slide 01: What is Generative AI (10 min)
2. Slide 02: LLM Limitations (10 min)
3. Slide 04: Building the Graph (15 min)
4. Slide 08: Vectors (15 min)
5. Slide 11: What is a Retriever (15 min)
6. Slide 15: Choosing the Right Retriever (10 min)
7. Slide 16: What is an Agent (10 min)
8. Slide 18: Simple Schema Agent (15 min)
9. Slide 21: Multi-Tool Agent Design (10 min)
10. Slide 22: Aura Agents (10 min)

### For Theory-Only Session (1.5 hours):

**Conceptual Overview:**
1. Slide 01: What is Generative AI (10 min)
2. Slide 02: LLM Limitations (10 min)
3. Slide 05: Schema Design (10 min)
4. Slide 08: Vectors (15 min)
5. Slide 10: GraphRAG Explained (10 min)
6. Slide 11: What is a Retriever (10 min)
7. Slide 15: Choosing the Right Retriever (10 min)
8. Slide 16: What is an Agent (10 min)
9. Slide 21: Multi-Tool Agent Design (10 min)

## 🖼️ Images

All slides reference images in the `../images/` directory. Make sure the images folder is at the same level as the graphacademy folder:

```
hands-on-lab-neo4j-and-azure/
├── images/              ← Images here
└── graphacademy/
    └── slides/          ← Slides here
```

## 💡 Tips for Presenting

1. **Test beforehand** - Run through slides before presenting
2. **Use presenter mode** - Marp CLI has a presenter mode with notes
3. **Adjust timing** - Each slide deck has suggested duration
4. **Interactive demos** - Pause slides for hands-on exercises in labs
5. **Export PDFs** - Create backup PDFs in case of technical issues
6. **Know your audience** - Use short vs full workshop timing based on audience

## 🔧 Troubleshooting

**Images not showing?**
- Ensure `images/` folder is at correct location (../images from slides/)
- Use `--allow-local-files` flag with Marp CLI

**Formatting issues?**
- Update Marp CLI: `npm update -g @marp-team/marp-cli`
- Try different themes

**PDF export fails?**
- Install Chromium: `npx @marp-team/marp-cli --version`
- Use `--allow-local-files` flag

## 📦 Export All Presentations

**Create PDFs for all slides:**
```bash
cd /path/to/slides
for file in [0-9]*.md; do
  marp "$file" --pdf --allow-local-files
done
```

**Create HTML presentations:**
```bash
for file in [0-9]*.md; do
  marp "$file" --html --allow-local-files
done
```

## 📚 Additional Resources

- [Marp Documentation](https://marpit.marp.app/)
- [Marp CLI Usage](https://github.com/marp-team/marp-cli)
- [Marp Themes](https://github.com/marp-team/marp-core/tree/main/themes)
- [Creating Custom Themes](https://marpit.marp.app/theme-css)
- [GraphAcademy Lessons](../README.md) - Corresponding lesson content

## 🎯 Quick Start

```bash
# Install Marp
npm install -g @marp-team/marp-cli

# Navigate to slides
cd /path/to/graphacademy/slides

# Start presenting first slide
marp 01-what-is-genai-slides.md --server

# Browser will open with presentation
# Use arrow keys to navigate
# Press 'F' for fullscreen
```

---

## 📈 Slide Statistics

**Total Presentations:** 22
**Total Slide Pages:** ~280 individual slides
**Format:** Marp Markdown
**Status:** ✅ Ready to present

### Module Breakdown
- **Module 1:** 9 presentations (Slides 1-9)
- **Module 2:** 6 presentations (Slides 10-15)
- **Module 3:** 7 presentations (Slides 16-22)

### New Slides Added (December 2, 2025)
- 06: Chunking Strategies
- 07: Entity Resolution
- 09: Working with Full Datasets
- 12: Vector Retriever (Detailed)
- 13: Vector + Cypher Retriever (Detailed)
- 14: Text2Cypher Retriever (Detailed)
- 15: Choosing the Right Retriever
- 17: Microsoft Agent Framework (updated from LangChain)
- 18: Simple Schema Agent
- 21: Multi-Tool Agent Design

**Latest Update:** Complete alignment with 24-lesson GraphAcademy structure
**Version:** 2.0 (December 2, 2025)
