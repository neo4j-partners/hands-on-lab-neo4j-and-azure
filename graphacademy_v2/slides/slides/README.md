# Workshop Slides

This folder contains presentation-ready slides extracted from the workshop lessons. All slides are formatted for [Marp](https://marp.app/), a markdown presentation tool.

## 📊 Available Presentations

All slides are sequentially numbered 01-15 for easy navigation.

### Module 1: Generative AI (Slides 1-6)

**01. What is Generative AI** (3.8 KB)
   - Introduction to Generative AI
   - Large Language Models (LLMs)
   - Knowledge Graphs & Cypher
   - Retrieval Augmented Generation (RAG)

**02. LLM Limitations** (3.6 KB)
   - LLM Cautions & Limitations
   - Access to Data Issues
   - Hallucination Problem
   - Temperature Settings
   - Transparency Concerns

**03. Context** (2.3 KB) ⭐ **Smallest**
   - Importance of Context
   - Avoiding Hallucination
   - Improving LLM Responses

**04. Building the Graph** (11 KB) ⭐ **Largest**
   - Complete GraphRAG Pipeline
   - EDGAR SEC Filings Processing
   - Entity Extraction
   - Schema-Driven Knowledge Graphs
   - Structured Data Integration

**05. Schema Design** (4.6 KB) 🆕
   - Schema Purpose & Benefits
   - Node and Relationship Definitions
   - Pattern Specifications
   - Iterative Schema Development
   - Balancing Flexibility and Structure

**06. Vectors** (4.7 KB)
   - Vector Fundamentals
   - Embeddings & Similarity
   - Vector Search in Neo4j
   - Document Chunking

### Module 2: Retrievers (Slides 7-10)

**07. GraphRAG Explained** (5.1 KB) 🆕
   - What is GraphRAG?
   - Benefits of GraphRAG
   - Graph-Enhanced Vector Search
   - Full Text Search
   - Text to Cypher

**08. What is a Retriever** (5.9 KB)
   - Vector Retriever
   - Vector + Cypher Retriever
   - Text2Cypher Retriever
   - Choosing the Right Retriever

**09. Setup** (1.3 KB)
   - Environment Setup
   - Configuration Steps

**10. Hands-On Retrievers** (5.6 KB) 🆕
    - Vector Retriever Use Cases
    - Vector + Cypher Retriever Use Cases
    - Text2Cypher Retriever Use Cases
    - Comparing Retriever Approaches
    - Retriever Selection Strategy

### Module 3: Agents (Slides 11-15)

**11. What is an Agent** (3.2 KB)
    - What are Agents?
    - Conversational Wrappers
    - Agent Reasoning & Tools

**12. LangChain Agent** (2.6 KB)
    - Building LangChain Agents
    - Schema Tools
    - Agent Architecture

**13. Vector Retriever Tool** (5.3 KB) 🆕
    - Vector + Graph Retrieval Tool
    - Two-Tool Agent Architecture
    - Automatic Tool Selection
    - Multi-Step Reasoning
    - Progressive Agent Building

**14. Text2Cypher Tool** (6.2 KB) 🆕
    - Text2Cypher Query Tool
    - Three-Tool Agent Capabilities
    - Complete GraphRAG Agent
    - Intelligent Multi-Tool Reasoning
    - Real-World Applications

**15. Aura Agents** (6.6 KB)
    - No-Code Aura Agents
    - Tool Types & Configuration
    - Testing & Deployment

## 🚀 How to Use These Slides

### Option 1: Marp CLI (Recommended)

Install Marp CLI:
```bash
npm install -g @marp-team/marp-cli
```

**Present slides:**
```bash
cd /Users/ryanknight/projects/courses/workshop-markdown/slides
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
✅ **Images** - All images linked to `images/`
✅ **Code Blocks** - Syntax-highlighted Cypher and Python
✅ **Speaker Notes** - Hidden as HTML comments
✅ **Bullet Points** - Clear, hierarchical formatting
✅ **Two-Column Layouts** - Where appropriate

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

### For Full Workshop (4 hours):

**Part 1: GenAI Fundamentals (70 min)**
1. Slide 01: What is Generative AI (15 min)
2. Slide 02: LLM Limitations (15 min)
3. Slide 03: Context (10 min)
4. Slide 04: Building the Graph (20 min)
5. Slide 05: Schema Design (10 min)

**Part 2: GraphRAG & Retrievers (50 min)**
6. Slide 06: Vectors (20 min)
7. Slide 07: GraphRAG Explained (15 min)
8. Slide 08: What is a Retriever (15 min)

**Part 3: Setup (10 min)**
9. Slide 09: Setup (10 min)

**Part 4: Hands-On & Agents (60 min)**
10. Slide 10: Hands-On Retrievers (15 min)
11. Slide 11: What is an Agent (15 min)
12. Slide 12: LangChain Agent (10 min)
13. Slide 13: Vector Retriever Tool (10 min)
14. Slide 14: Text2Cypher Tool (10 min)
15. Slide 15: Aura Agents (15 min)

### For Short Workshop (2 hours):

**Essential Slides Only:**
1. Slide 01: What is Generative AI (10 min)
2. Slide 02: LLM Limitations (10 min)
3. Slide 04: Building the Graph (15 min)
4. Slide 08: What is a Retriever (20 min)
5. Slide 09: Setup (5 min)
6. Slide 11: What is an Agent (10 min)
7. Slide 15: Aura Agents (10 min)

## 🖼️ Images

All slides reference images in the `images/` directory. Make sure the images folder is at the same level as the slides folder for proper rendering:

```
workshop-markdown/
├── images/           ← Images here
└── slides/           ← Slides here
```

## 💡 Tips for Presenting

1. **Test beforehand** - Run through slides before presenting
2. **Use presenter mode** - Marp CLI has a presenter mode with notes
3. **Adjust timing** - Each slide deck has suggested duration
4. **Interactive demos** - Pause slides for hands-on exercises
5. **Export PDFs** - Create backup PDFs in case of technical issues

## 🔧 Troubleshooting

**Images not showing?**
- Ensure `images/` folder is one level up from `slides/`
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
cd /Users/ryanknight/projects/courses/workshop-markdown/slides
for file in *.md; do
  marp "$file" --pdf --allow-local-files
done
```

**Create HTML presentations:**
```bash
for file in *.md; do
  marp "$file" --html --allow-local-files
done
```

## 📚 Additional Resources

- [Marp Documentation](https://marpit.marp.app/)
- [Marp CLI Usage](https://github.com/marp-team/marp-cli)
- [Marp Themes](https://github.com/marp-team/marp-core/tree/main/themes)
- [Creating Custom Themes](https://marpit.marp.app/theme-css)

## 🎯 Quick Start

```bash
# Install Marp
npm install -g @marp-team/marp-cli

# Navigate to slides
cd /Users/ryanknight/projects/courses/workshop-markdown/slides

# Start presenting first slide
marp 01-what-is-genai-slides.md --server

# Browser will open with presentation
# Use arrow keys to navigate
# Press 'F' for fullscreen
```

---

**Total:** 15 presentations, ~2,400 lines
**Format:** Marp Markdown
**Status:** ✅ Ready to present
**Latest:** Phase 1 & 2 slides added (December 2, 2024)
