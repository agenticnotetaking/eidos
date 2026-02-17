---
tldr: Template for reference docs — curated external knowledge the project relies on but doesn't own
---

# Reference Template

Output path: `eidos/reference - <claim>.md`

```markdown
---
tldr: Brief description of the concept and its relevance
---

# Reference: [Concept name]

## What It Is

Core definition of the concept in the project's own words.
Not a copy-paste from documentation — a distillation tuned to how this project uses it.

## Key Points

- Essential aspects of the concept
- Relevant details, constraints, or gotchas
- What matters for this project specifically

## How We Use It

How this concept applies within the project.
Link to specs, decisions, or code that depend on it.

## Sources

- [Source name](URL) — brief note on what this source covers
- [Another source](URL) — and why it's authoritative
```

## Field Reference

**Frontmatter:**
- `tldr` — one-line summary of the concept and why it's here

**What It Is:**
- Your distillation, not a copy
- Written for someone who needs to *use* the concept, not *learn* it from scratch
- Enough depth to act on without reading the sources

**Key Points:**
- The 20% that covers 80% of usage
- Project-relevant gotchas and constraints
- Things that are easy to get wrong or forget

**How We Use It:**
- Concrete connections to the project's specs, code, or decisions
- Wiki links to relevant files
- Patterns or conventions derived from this concept

**Sources:**
- Authoritative references for deeper reading
- URLs, books, documentation — whatever the knowledge came from
- Brief annotation on each source's scope or authority
