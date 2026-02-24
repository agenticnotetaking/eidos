---
tldr: Capture context, decisions, and learnings to files so future sessions can build on them
---

# Externalise — persist insights beyond the conversation

## Target

Conversations are ephemeral.
Insights, decisions, and learnings that stay only in chat are lost when the session ends.
Externalising means writing them to files so future sessions can build on past work.

## Behaviour

- When a pattern is established or a decision is made during work, persist it
- When something "should have happened" (a missed expectation), update the relevant spec, inject snippet, or claim
- When corrected, capture the correction so it doesn't recur
- When in doubt, externalise — deleting unnecessary files is easier than recreating lost context

### What to Externalise Where

| Content | Destination |
|---------|-------------|
| Workflow/behaviour changes | Inject snippet, relevant spec, or CLAUDE.md |
| Conventions discovered | Relevant spec or new spec in `eidos/` |
| Decisions made | Inline in plan/experiment with `=>`, or `memory/decision - ...` for significant ones |
| Reusable patterns | New skill in `skills/` |
| Learnings during work | Inline in plan/experiment with `=>`, promote to files when significant |
| Questions to explore | `memory/question - ...` or `{[?]}` in relevant spec |
| Ideas for later | `{[?]}` in relevant spec or `memory/idea - ...` |
| Screenshots/images | `memory/observation - {timestamp} - {claim}.{ext}`, linked in active plan/experiment |

### When to Externalise

- **During work** — when you establish a pattern or make a decision
- **After completing an action** — observations go inline in the plan or experiment with `=>`
- **At session end** — use `/eidos:done` to export and reflect
- **When corrected** — update specs or CLAUDE.md so the correction persists

## Design

Externalisation is not a separate activity — it's woven into the workflow.
Plan and experiment `=>` notes are the lightest form.
Spec updates are the heaviest.
The right weight depends on how broadly the insight applies.

## Verification

- Decisions and learnings from work sessions are findable in files, not just in chat history
- Corrections to behaviour persist across sessions
- Plan and experiment files capture inline observations via `=>`

## Interactions

- [[spec - eidos - spec driven development loops]] — externalisation feeds both `eidos/` and `memory/`
- [[spec - plan skill - structured plan for multi step work]] — `=>` notes are the primary inline externalisation mechanism
- [[spec - experiment skill - log based iterative exploration with emergent phases]] — experiments also use `=>` for inline externalisation
- [[c - actions carry input and output context - plain bullets before arrow bullets after]] — the input/output principle behind `=>`
- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — prefixes for externalised file types
