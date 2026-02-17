---
tldr: Capture testing observations mid-plan — structure issues, update specs, inject tasks back into the plan
---

# Observe skill — capture testing observations mid-plan

## Target

After a phase completes, the human tests the result and notices things that don't match expectations.
These findings need to flow back into the plan as structured entries, with spec updates and implementation tasks.
Without this, observations stay in chat (ephemeral) or get captured ad hoc without consistent structure.

## Behaviour

- Used in-session during active plan work — assumes plan context is loaded
- Accepts batch input: multiple observations described at once
- Numbers observations per-phase: P2-O1, P6-O3, etc. — local and unambiguous
- Each observation structured as: Was/Expected (or Was/Fix/Verify), optional Impact, optional Spec note
- Updates specs when observations clarify or correct design intent
- Adds implementation tasks to the current phase or a new phase after current
- Observations marked FIXED when their tasks are complete

## Design

The skill formalises the organic workflow loop already described in [[spec - eidos - spec driven development loops]]:
observe → adjust spec → push to code → discover → observe again.

Observations live inside the phase they relate to, as a sub-section after the actions.
Each observation is a mini-spec: what was, what should be, what to change.
Implementation tasks reference observations by phase-scoped ID: `[ ] Fix P6-O1 — description`.

### Two levels of observation

- **Inline `=>`** — small discoveries during implementation (stays under the action)
- **Structured P*n*-O*m*** — visible behaviour gaps from testing (lives in phase, generates tasks)

The threshold: if it needs its own implementation task, it's a structured observation.

## Verification

- Observations are numbered and traceable in the plan
- Spec updates are linked from the observation entry
- Implementation tasks exist for each open observation
- FIXED observations have all their tasks marked `[x]`

## Interactions

- [[spec - planning - structured intent between spec and code]] — observations are part of the plan lifecycle
- [[template - plan - structured phases with actions and progress tracking]] — defines the per-phase Observations sub-section
- [[spec - plan-continue skill - resume work on existing plan]] — picks up observation-generated tasks normally
