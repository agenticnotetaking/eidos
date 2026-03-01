---
tldr: Write findings to files with feedback placeholders rather than presenting interactively — the file becomes the review surface
---

# Bias toward artifacts as feedback surfaces over interactive dialogue

## Target

When AI reviews, analyses, or processes something, the default instinct is to present findings in chat and wait for interactive responses.
This is ephemeral — the conversation compresses, the context vanishes, and the feedback loop dies with the session.

Better: write findings to a structured file with explicit placeholders for human feedback.
The file becomes the review surface.
The human fills in feedback at their own pace, across sessions if needed.
The AI processes the feedback when invoked again.

## Behaviour

- When a skill produces observations, findings, or review items: write them to a file first, present second.
- Each finding gets a feedback placeholder — typically a checkbox or empty slot the human can fill.
- The file is committed immediately so it persists.
- The human reviews and fills in feedback (in-editor, at their own pace).
- A follow-up invocation (or the same skill re-invoked) picks up the feedback and acts on it.

### Structure Pattern

```markdown
# Section - <summary> - status: open

1. <observation>
   - [ ] <empty — human feedback>
2. <observation>
   - [ ] <empty — human feedback>
```

Sections move from `open` → `resolved` as feedback is processed.

### When This Applies

- Plan reviews (`/eidos:plan-review`)
- Spec refinement (`/eidos:refine`) — write the structured Q&A to file with feedback slots, then process
- Code reviews (`/eidos:code-review`)
- Any skill that produces a list of items needing human judgement

### When Interactive Is Still Fine

- Quick confirmations (yes/no, continue?)
- Single-item decisions
- Conversations where the back-and-forth IS the value (brainstorming, spec creation)

## Design

This extends [[spec - externalise - persist insights beyond the conversation]] with a specific bias: when the choice is between "present in chat" and "write to file", default to writing.

The file is not just a record — it's a **feedback surface**.
The checkboxes and empty slots are not decoration — they're the interface.

## Interactions

- [[spec - externalise - persist insights beyond the conversation]] — the parent principle
- [[c - spec refine loop uses double curly braces - creates refinement traces and adjusts spec]] — refine can adopt this pattern
