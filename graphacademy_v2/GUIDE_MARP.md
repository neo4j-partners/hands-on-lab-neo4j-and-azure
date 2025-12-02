# Marp Presentation Guide

Complete guide for using Marp to present the workshop slides.

## What is Marp?

[Marp](https://marp.app/) (Markdown Presentation Ecosystem) is a tool that converts markdown files into beautiful presentation slides. It's perfect for technical presentations and workshops.

## Quick Start

### 1. Install Marp CLI

```bash
npm install -g @marp-team/marp-cli
```

Verify installation:
```bash
marp --version
```

### 2. Present Your First Slide

```bash
cd /Users/ryanknight/projects/courses/workshop-markdown/slides
marp 01-what-is-genai-slides.md --server
```

Your browser will open with the presentation. Use arrow keys to navigate.

## Installation Options

### Option 1: Marp CLI (Recommended for Instructors)

**Install:**
```bash
npm install -g @marp-team/marp-cli
```

**Pros:**
- Present from command line
- Export to PDF/HTML/PPTX
- Live reload during editing
- Professional presenter mode

**Cons:**
- Requires Node.js

### Option 2: VS Code Extension (Best for Editing)

**Install:**
1. Open VS Code
2. Install "Marp for VS Code" extension
3. Open any `.md` slide file
4. Click "Open Preview" or press `Cmd+K V`

**Pros:**
- Integrated with VS Code
- Live preview while editing
- Export from editor
- No command line needed

**Cons:**
- Requires VS Code

### Option 3: Marp Web (Quick Testing)

**Use:**
1. Visit [web.marp.app](https://web.marp.app/)
2. Copy/paste slide content
3. Present in browser

**Pros:**
- No installation
- Quick testing
- Works anywhere

**Cons:**
- Can't export
- No local file access
- Limited features

## Basic Usage

### Present Slides

**With server mode (recommended):**
```bash
marp 01-what-is-genai-slides.md --server
```
- Opens in browser
- Live reload on file changes
- Clean URLs

**Direct preview:**
```bash
marp 01-what-is-genai-slides.md --preview
```

### Export Slides

**PDF (best for sharing):**
```bash
marp 01-what-is-genai-slides.md --pdf --allow-local-files
```

**HTML (interactive):**
```bash
marp 01-what-is-genai-slides.md --html --allow-local-files
```

**PowerPoint:**
```bash
marp 01-what-is-genai-slides.md --pptx --allow-local-files
```

**Note:** `--allow-local-files` is required for images to load correctly.

### Export All Slides

**Create PDFs for entire workshop:**
```bash
cd slides
for file in *.md; do
  marp "$file" --pdf --allow-local-files
done
```

**Create HTML versions:**
```bash
for file in *.md; do
  marp "$file" --html --allow-local-files
done
```

## Keyboard Shortcuts

### During Presentation

| Key | Action |
|-----|--------|
| `→` or `Space` | Next slide |
| `←` | Previous slide |
| `Home` | First slide |
| `End` | Last slide |
| `F` or `F11` | Toggle fullscreen |
| `Esc` | Exit fullscreen |
| `P` | Presenter mode (HTML) |
| `?` | Show help |

### While Editing (VS Code)

| Key | Action |
|-----|--------|
| `Cmd+K V` | Open preview |
| `Cmd+Shift+V` | Preview in new window |

## Slide Syntax

### Basic Slide Structure

```markdown
---
marp: true
theme: default
paginate: true
---

# Title Slide

First slide content

---

# Second Slide

Second slide content

* Bullet point 1
* Bullet point 2
```

### Key Elements

**Slide Separator:**
```markdown
---
```
Creates a new slide

**Headers:**
```markdown
# Main Title (usually slide title)
## Subtitle
### Section header
```

**Images:**
```markdown
![Description](../images/filename.svg)
```

**Code Blocks:**
````markdown
```cypher
MATCH (n:Person)
RETURN n
```
````

**Bullet Points:**
```markdown
* Item 1
* Item 2
  * Nested item
```

**Speaker Notes:**
```markdown
<!-- This is a speaker note, only visible in presenter mode -->
```

## Themes

### Built-in Themes

Change theme in YAML frontmatter:

**Default (Professional):**
```markdown
---
theme: default
---
```

**Gaia (Colorful):**
```markdown
---
theme: gaia
---
```

**Uncover (Minimalist):**
```markdown
---
theme: uncover
---
```

### Theme Comparison

| Theme | Best For | Style |
|-------|----------|-------|
| `default` | Professional workshops | Clean, corporate |
| `gaia` | Creative presentations | Colorful, modern |
| `uncover` | Minimal talks | Centered, simple |

### Custom Styling

Add custom CSS in frontmatter:

```markdown
---
marp: true
theme: default
style: |
  section {
    background-color: #f0f0f0;
  }
  h1 {
    color: #0066cc;
  }
---
```

## Advanced Features

### Two-Column Layout

```markdown
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">

<div>

## Left Column

Content here

</div>

<div>

## Right Column

Content here

</div>

</div>
```

### Background Images

```markdown
![bg](../images/background.png)

# Slide with Background
```

### Scoped Styles

```markdown
<!-- _class: lead -->
# Special Styled Slide

This slide uses the 'lead' class
```

### Footer

```markdown
---
footer: 'Neo4j GraphRAG Workshop | Module 1'
---
```

### Page Numbers

```markdown
---
paginate: true
---
```

## Workshop-Specific Tips

### Image Paths

All slides use relative paths to images:
```markdown
![Description](../images/filename.svg)
```

**Important:** Run Marp from the `slides/` directory so paths resolve correctly:
```bash
cd /Users/ryanknight/projects/courses/workshop-markdown/slides
marp 01-what-is-genai-slides.md --server
```

### Code Examples

Slides include Cypher and Python code. Syntax highlighting works automatically:

````markdown
```cypher
MATCH (n:Person)-[:WORKS_AT]->(c:Company)
RETURN n.name, c.name
```
````

### Speaker Notes

Many slides include speaker notes as HTML comments:

```markdown
<!--
Speaker Note: This is a key concept.
Make sure to emphasize the importance of context.
-->
```

These are visible in presenter mode (press `P` in HTML export).

## Presenting Workflows

### Workflow 1: Live Presentation

**For presenting directly from laptop:**

```bash
cd slides
marp 01-what-is-genai-slides.md --server
```

1. Browser opens with slides
2. Press `F` for fullscreen
3. Use arrow keys to navigate
4. File auto-reloads if you edit

**Best for:** Interactive workshops, live coding demos

### Workflow 2: PDF Export

**For sharing or backup:**

```bash
marp 01-what-is-genai-slides.md --pdf --allow-local-files
```

1. Creates PDF in same directory
2. Share with participants
3. Use as backup if tech fails

**Best for:** Handouts, offline access, printing

### Workflow 3: HTML with Presenter Mode

**For professional presenting:**

```bash
marp 01-what-is-genai-slides.md --html --allow-local-files
```

1. Open HTML in browser
2. Press `P` for presenter mode
3. See notes and upcoming slides
4. Share URL with audience

**Best for:** Conference talks, recorded sessions

### Workflow 4: PowerPoint Export

**For PowerPoint users:**

```bash
marp 01-what-is-genai-slides.md --pptx --allow-local-files
```

1. Creates .pptx file
2. Edit in PowerPoint if needed
3. Add animations or transitions

**Best for:** Corporate environments, editing needed

## Workshop Presentation Order

### Full 4-Hour Workshop

**Part 1: Fundamentals (60 min)**
```bash
marp 01-what-is-genai-slides.md --server          # 15 min
marp 02-llm-limitations-slides.md --server        # 15 min
marp 03-context-slides.md --server                # 10 min
marp 04-building-the-graph-slides.md --server     # 20 min
```

**Part 2: Technical (45 min)**
```bash
marp 08-vectors-slides.md --server                # 20 min
marp 02-what-is-a-retriever-slides.md --server    # 25 min
```

**Part 3: Setup (10 min)**
```bash
marp 03-setup-slides.md --server                  # 10 min
```

**Part 4: Agents (45 min)**
```bash
marp 01-what-is-an-agent-slides.md --server       # 15 min
marp 02-langchain-agent-slides.md --server        # 15 min
marp 05-aura-agents-slides.md --server            # 15 min
```

### Quick 2-Hour Workshop

```bash
# Essential slides only
cd slides

marp 01-what-is-genai-slides.md --server          # 10 min
marp 02-llm-limitations-slides.md --server        # 10 min
marp 04-building-the-graph-slides.md --server     # 15 min
marp 02-what-is-a-retriever-slides.md --server    # 15 min
marp 03-setup-slides.md --server                  # 5 min
marp 01-what-is-an-agent-slides.md --server       # 10 min
marp 05-aura-agents-slides.md --server            # 10 min
```

## Troubleshooting

### Images Not Showing

**Problem:** Images show as broken links

**Solution:**
```bash
# Make sure you're in the slides directory
cd /Users/ryanknight/projects/courses/workshop-markdown/slides

# Use --allow-local-files flag
marp 01-what-is-genai-slides.md --pdf --allow-local-files
```

**Check:** Verify images folder exists one level up:
```bash
ls ../images/
```

### PDF Export Fails

**Problem:** PDF export hangs or fails

**Solution:**
```bash
# Install/update Chrome or Chromium
npx @marp-team/marp-cli --version

# Try with explicit browser
marp slides.md --pdf --allow-local-files
```

### Port Already in Use

**Problem:** Server won't start (port 8080 busy)

**Solution:**
```bash
# Use different port
marp slides.md --server --port 8081

# Or kill existing process
lsof -ti:8080 | xargs kill
```

### Styling Issues

**Problem:** Slides look wrong or broken

**Solution:**
```bash
# Update Marp CLI
npm update -g @marp-team/marp-cli

# Try different theme
# Edit frontmatter: theme: gaia
```

### File Watch Not Working

**Problem:** Changes don't auto-reload

**Solution:**
```bash
# Use explicit watch flag
marp slides.md --server --watch

# Or restart server
```

## Best Practices

### Before Presenting

1. **Test all slides**
   ```bash
   marp *.md --preview
   ```

2. **Export PDF backups**
   ```bash
   for file in *.md; do marp "$file" --pdf --allow-local-files; done
   ```

3. **Check images**
   ```bash
   ls ../images/ | wc -l  # Should be 22
   ```

4. **Practice timing**
   - Run through each deck
   - Note approximate duration
   - Plan breaks

### During Presenting

1. **Use fullscreen** (press `F`)
2. **Have PDF backup** ready
3. **Use presenter mode** for notes (HTML export)
4. **Test remote before** workshop
5. **Keep water nearby** 💧

### After Presenting

1. **Share PDFs** with participants
2. **Collect feedback**
3. **Update slides** based on questions
4. **Archive version** for future reference

## Quick Reference

### Essential Commands

```bash
# Present
marp slides.md --server

# Export PDF
marp slides.md --pdf --allow-local-files

# Export all
for f in *.md; do marp "$f" --pdf --allow-local-files; done

# Watch and preview
marp slides.md --server --watch
```

### Essential Shortcuts

- `→` Next slide
- `←` Previous slide
- `F` Fullscreen
- `P` Presenter mode
- `Esc` Exit

### Essential Fixes

```bash
# Images not showing
cd slides && marp file.md --allow-local-files

# Can't export PDF
npm update -g @marp-team/marp-cli

# Port busy
marp file.md --server --port 8081
```

## Resources

### Official Documentation
- [Marp Website](https://marp.app/)
- [Marp CLI GitHub](https://github.com/marp-team/marp-cli)
- [Marpit Documentation](https://marpit.marp.app/)

### Themes & Styling
- [Built-in Themes](https://github.com/marp-team/marp-core/tree/main/themes)
- [Theme Gallery](https://github.com/marp-team/marp/discussions/categories/show-and-tell)
- [Custom CSS Guide](https://marpit.marp.app/theme-css)

### Extensions
- [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
- [Marp Web](https://web.marp.app/)

### Community
- [GitHub Discussions](https://github.com/marp-team/marp/discussions)
- [Examples Repository](https://github.com/marp-team/marp-cli/tree/main/examples)

## Getting Help

### Check Version
```bash
marp --version
```

### View Help
```bash
marp --help
```

### Common Issues
See [GitHub Issues](https://github.com/marp-team/marp-cli/issues)

### Update Marp
```bash
npm update -g @marp-team/marp-cli
```

---

## Workshop-Specific Notes

### Slide Files
- **Location:** `/Users/ryanknight/projects/courses/workshop-markdown/slides/`
- **Count:** 10 presentations
- **Format:** Marp Markdown
- **Theme:** Default (professional)

### Image Files
- **Location:** `/Users/ryanknight/projects/courses/workshop-markdown/images/`
- **Count:** 22 images
- **Formats:** SVG, PNG
- **Usage:** Linked as `../images/filename.ext`

### Content Coverage
- **Module 1:** 5 presentations (GenAI fundamentals)
- **Module 2:** 2 presentations (Retrievers)
- **Module 3:** 3 presentations (Agents)
- **Total Duration:** ~200 minutes with breaks

---

**Quick Start:** `cd slides && marp 01-what-is-genai-slides.md --server`

**Status:** Ready to present! 🎉
