---
tldr: Pre-implementation review of a plan — write findings to a file as a feedback surface
category: planning
---

# /eidos:plan-review

Review a plan before implementation and write structured findings to a file with human feedback placeholders.

## Usage

```
/eidos:plan-review [plan-name]
```

## Instructions

### 1. Find the Plan

- **Arg given** → find the matching plan in `memory/`
- **No arg** → search `memory/` for `plan - *.md` files, identify incomplete ones (same logic as `/eidos:plan-continue`), let the user choose if multiple

### 2. Load Context

Read in order:
1. **The plan file** — understand phases, actions, goals
2. **Linked specs** in `eidos/` — refresh on requirements and claims
3. **Linked decisions or references** — understand prior choices

### 3. Review the Plan

Examine each phase and action for:
- **Completeness** — does it cover what the spec requires?
- **Ordering** — are dependencies in the right sequence?
- **Granularity** — are actions the right size (not too big, not too small)?
- **Ambiguity** — would you know exactly what to do from the action description alone?
- **Risk** — anything likely to cause rework or surprises?
- **Missing steps** — setup, cleanup, verification, edge cases the plan skips?

### 4. Write the Review File

Run `date '+%y%m%d%H%M'` to get the current timestamp.
Create `memory/planreview - <timestamp> - <claim>.md`:

```markdown
---
tldr: Pre-implementation review of [[plan - <timestamp> - <claim>]]
---

# Plan Review: <plan claim>

Plan: [[plan - <timestamp> - <claim>]]

# Phase 1: <phase name> — <tldr of findings> — status: open

1. <observation>
   - [ ]
2. <observation>
   - [ ]

# Phase 2: <phase name> — <tldr of findings> — status: open

1. <observation>
   - [ ]
2. <observation>
   - [ ]

# General

1. <cross-cutting observation>
   - [ ]
```

Guidelines:
- One section per phase, plus a General section for cross-cutting concerns.
- If a phase has multiple distinct topics, split into subsections (e.g. `## Data model`, `## API surface`).
- Each observation is a concrete, actionable finding — not vague ("consider X" → bad, "Phase 2 action 3 assumes the DB migration runs first but Phase 1 doesn't include it" → good).
- The `- [ ]` line is always empty — that's the human's feedback slot.
- If a phase looks solid with no findings, say so: `No issues found.` (still include the section).
- Status starts as `open` for all sections.

### 5. Commit and Present

Commit the review file.
Tell the user where it is and what to do next:

```
Review written to [[planreview - <timestamp> - <claim>]]

Fill in feedback on items you want addressed, then I'll update the plan.
```

### 6. Processing Feedback (when re-invoked)

When the user comes back with feedback filled in:
1. Read the review file
2. For each item with feedback:
   - Apply the feedback to the plan (add actions, reorder, clarify, remove)
   - Mark the section status: `open` → `resolved`
3. Items with empty `[ ]` are skipped (human chose not to comment = no issue)
4. Commit updated plan and updated review file
5. Summary of changes made

## Notes

- This follows [[c - bias toward artifacts as feedback surfaces over interactive dialogue]] — write first, discuss second.
- The review file is the feedback surface, not the chat.
- The human can fill in feedback across sessions, not just immediately.

## Output

- Creates: `memory/planreview - <timestamp> - <claim>.md`
- May modify: the plan file (when processing feedback)
