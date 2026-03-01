---
tldr: Review a plan before implementation and write findings to a structured feedback file
---

# Spec: Plan Review Skill

> TL;DR: Examine a plan, write observations to a file with human feedback placeholders, then process feedback into plan updates.

## Target

Plans are written then immediately executed.
But plans often have gaps, ordering issues, or ambiguities that are cheaper to catch before implementation than during.

A review that happens in chat is ephemeral and pressures immediate response.
Writing findings to a file lets the human review at their own pace and respond selectively.

## Behaviour

- Finds and loads the target plan (same discovery logic as `/eidos:plan-continue`).
- Reviews each phase for completeness, ordering, granularity, ambiguity, risk, and missing steps.
- Writes a `planreview - <timestamp> - <claim>.md` file with per-phase sections.
- Each observation has an empty feedback placeholder (`- [ ]`).
- Sections have status: `open` → `resolved`.
- When re-invoked after human feedback: applies changes to the plan, marks sections resolved.

## Design

Implements [[c - bias toward artifacts as feedback surfaces over interactive dialogue]].

The review file is not a report — it's an interface.
The empty checkboxes are the human's input surface.
Items without feedback are treated as "no issue" — silence is consent.

## Interactions

- [[c - bias toward artifacts as feedback surfaces over interactive dialogue]] — the core pattern
- [[spec - planning - structured intent between spec and code]] — plans are the input
- [[spec - plan-continue skill - resume work on existing plan]] — shares plan discovery logic

## Mapping

- `skills/plan-review/plan-review.md` — skill instructions
- `eidos/skills/spec - plan-review skill - pre-implementation plan review as feedback surface.md` — this file
