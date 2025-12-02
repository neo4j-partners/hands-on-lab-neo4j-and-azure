# Slide Files Renamed to Sequential Numbering ✅

**Date:** December 2, 2024
**Status:** Complete

## What Changed

All slide files have been renamed from module-based numbering to sequential numbering (01-15) for easier navigation and to eliminate duplicate numbers.

## Before (Module-Based Numbering)

Files were numbered based on their lesson number within each module, causing duplicates:

```
01-what-is-genai-slides.md         (Module 1, Lesson 1)
01-graphrag-explained-slides.md    (Module 2, Lesson 1) ❌ Duplicate "01"
01-what-is-an-agent-slides.md      (Module 3, Lesson 1) ❌ Duplicate "01"
02-llm-limitations-slides.md       (Module 1, Lesson 2)
02-what-is-a-retriever-slides.md   (Module 2, Lesson 2) ❌ Duplicate "02"
02-langchain-agent-slides.md       (Module 3, Lesson 2) ❌ Duplicate "02"
... and so on
```

This made it confusing when viewing the directory listing.

## After (Sequential Numbering)

Files are now numbered sequentially 01-15 following the workshop presentation order:

### Module 1: Generative AI (01-06)
- 01-what-is-genai-slides.md
- 02-llm-limitations-slides.md
- 03-context-slides.md
- 04-building-the-graph-slides.md
- 05-schema-design-slides.md
- 06-vectors-slides.md

### Module 2: Retrievers (07-10)
- 07-graphrag-explained-slides.md
- 08-what-is-a-retriever-slides.md
- 09-setup-slides.md
- 10-hands-on-retrievers-slides.md

### Module 3: Agents (11-15)
- 11-what-is-an-agent-slides.md
- 12-langchain-agent-slides.md
- 13-vector-retriever-slides.md
- 14-text2cypher-retriever-slides.md
- 15-aura-agents-slides.md

## Benefits

✅ **No duplicate numbers** - Each slide has unique sequential number
✅ **Clear order** - Numbers reflect presentation sequence
✅ **Easy navigation** - Simple to find "next" slide
✅ **Better organization** - Follows workshop flow naturally
✅ **Cleaner directory listing** - No confusion about which module

## Mapping Table

| Old Name | New Name | Module |
|----------|----------|--------|
| 01-what-is-genai-slides.md | 01-what-is-genai-slides.md | Module 1 |
| 02-llm-limitations-slides.md | 02-llm-limitations-slides.md | Module 1 |
| 03-context-slides.md | 03-context-slides.md | Module 1 |
| 04-building-the-graph-slides.md | 04-building-the-graph-slides.md | Module 1 |
| 05-schema-design-slides.md | 05-schema-design-slides.md | Module 1 |
| 08-vectors-slides.md | 06-vectors-slides.md | Module 1 |
| 01-graphrag-explained-slides.md | 07-graphrag-explained-slides.md | Module 2 |
| 02-what-is-a-retriever-slides.md | 08-what-is-a-retriever-slides.md | Module 2 |
| 03-setup-slides.md | 09-setup-slides.md | Module 2 |
| 04-hands-on-retrievers-slides.md | 10-hands-on-retrievers-slides.md | Module 2 |
| 01-what-is-an-agent-slides.md | 11-what-is-an-agent-slides.md | Module 3 |
| 02-langchain-agent-slides.md | 12-langchain-agent-slides.md | Module 3 |
| 03-vector-retriever-slides.md | 13-vector-retriever-slides.md | Module 3 |
| 04-text2cypher-retriever-slides.md | 14-text2cypher-retriever-slides.md | Module 3 |
| 05-aura-agents-slides.md | 15-aura-agents-slides.md | Module 3 |

## Usage Examples

### Present slides in order
```bash
cd /Users/ryanknight/projects/courses/workshop-markdown/slides

# Present slide 1
marp 01-what-is-genai-slides.md --server

# Present slide 7
marp 07-graphrag-explained-slides.md --server

# Present slide 15
marp 15-aura-agents-slides.md --server
```

### Export all slides to PDF
```bash
cd slides
for i in {01..15}; do
  marp ${i}-*.md --pdf --allow-local-files
done
```

### Present specific range
```bash
# Present Module 1 only (slides 1-6)
marp 0[1-6]-*.md --server

# Present Module 2 only (slides 7-10)
marp 0[7-9]-*.md 10-*.md --server

# Present Module 3 only (slides 11-15)
marp 1[1-5]-*.md --server
```

## Documentation Updated

✅ `slides/README.md` - Updated with sequential numbering
✅ Presentation order reflects new numbers
✅ All examples use new naming scheme

## No Breaking Changes

- All content within slides unchanged
- Marp format preserved
- Image links still work
- Only filenames changed

## Quick Reference

To find a slide:
- **Slides 01-06:** Module 1 (Generative AI)
- **Slides 07-10:** Module 2 (Retrievers)
- **Slides 11-15:** Module 3 (Agents)

---

**Status:** ✅ Complete
**Files Renamed:** 15 slide decks
**Location:** `/Users/ryanknight/projects/courses/workshop-markdown/slides/`

