---
tldr: Research a topic and document findings with sources
category: observation
---

# /eidos:research

Research a topic and produce a structured findings file.

## Usage

```
/eidos:research [topic or question]
```

## Instructions

### 1. Clarify the Question

If the topic is broad, use AskUserQuestion to narrow scope:
- What specifically do we need to know?
- Any preferred sources or angles?
- How deep should we go?

If the question is already specific, confirm and proceed.

### 2. Create Research File

Read the template: [[template - research - source notes and distilled findings]]

Create `memory/research - <timestamp> - <claim>.md` with the Question filled in and empty Sources/Distillation/Implications sections.
Commit immediately.

This file is the working document — it gets updated as research progresses, not written once at the end.

### 3. Investigate and Write Progressively

Search across multiple source types:
- **Web** — documentation, articles, forums, comparisons
- **Codebase** — existing patterns, implementations, dependencies
- **Memory/eidos files** — prior research, decisions, specs that relate

**After each source (or small batch of related sources):**
1. Add a subsection under Sources with key points, relevant detail, and caveats
2. Update the file and commit

Don't hold sources in memory — write them down as you go.
This preserves detail that would be lost in a single end-of-research write, and lets the user see progress and redirect if needed.

### 4. Distil

After gathering all sources, synthesise:
- What the sources agree on
- Where they conflict and why
- What remains unclear
- Actionable conclusions

This is synthesis, not summary. Don't repeat each source — draw conclusions across them.

### 5. Connect Implications

Link findings to current work:
- Specs to update
- Decisions to make
- Approaches to reconsider

### 6. Finalise

Update the file with Distillation and Implications sections.
Set status to `complete`.
Commit.

### 7. Present and Offer Next Steps

Show the distilled findings (not the full file) and offer:
```
Research complete: [[research - <timestamp> - <claim>]]

Options:
1 - Act on implications (update specs, create decision, etc.)
2 - Investigate further on [specific angle]
3 - Done for now
```

## Output

- Creates: `memory/research - <timestamp> - <claim>.md`
- Status field starts as `active`, set to `complete` when done
