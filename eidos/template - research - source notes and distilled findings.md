---
tldr: Template for research files — source-by-source notes followed by distilled conclusions
---

# Research Template

Output path: `memory/research - <timestamp> - <claim>.md`

```markdown
---
tldr: Brief description of what was researched
status: active
---

# Research: [Brief description]

## Question

What we're trying to find out.
Specific enough to know when we have an answer.

## Sources

### [Source name / URL / file reference]

- Key points from this source
- Relevant quotes or data
- Limitations or caveats of this source

### [Another source]

- Key points
- How it agrees or conflicts with other sources

## Distillation

Synthesised conclusions drawn from the sources above.
Not a summary of each source — a synthesis across them.

- What the sources agree on
- Where they conflict and why
- What remains unclear or needs further investigation

## Implications

How this affects the current work.
Specs to update, decisions to make, approaches to reconsider.
```

## Field Reference

**Frontmatter:**
- `status` — `active` (still gathering), `complete`, `superseded`

**Question:**
- Specific and answerable
- Multiple related questions are fine, but scope should be clear

**Sources:**
- One subsection per source
- Capture what the source says, not your interpretation (that goes in Distillation)
- Note limitations, biases, or relevance caveats
- Sources can be URLs, files, codebases, people, experiments

**Distillation:**
- This is the value — the synthesis across sources
- Written after all sources are gathered — but sources themselves are captured progressively
- Should stand on its own — a reader shouldn't need to read every source section
- Flag conflicts and unknowns explicitly

**Implications:**
- Connect findings back to the work at hand
- Link to specs, plans, or decisions that are affected
