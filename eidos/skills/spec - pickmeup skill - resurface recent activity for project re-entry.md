---
tldr: Resurface recent git activity, plans, and open work to re-enter a project after time away
---

# /eidos:pickmeup

## Target

After a few days away, the project state has drifted from memory.
Git log, plans, todos, and decisions are scattered — pickmeup aggregates them into a timeline-oriented summary so you can re-enter without archaeology.

## Behaviour

- Args: optional `days` (default 3)
- Scans git history for commits and branches in the window
- Scans `memory/` for timestamped artifacts (plans, sessions, decisions, solved, todos)
- Composes a date-grouped timeline showing what happened on which days
- Summarises plan progress, completed work, and open items
- Synthesises a "where you left off" narrative
- Creates `memory/pickmeup - <timestamp> - <claim>.md`
- Presents content in chat, then offers next-step selection

## Design

Pickmeup is read-heavy, write-light — it reads many sources but only creates one summary file.
The timeline groups by date, skipping silent days, so you see a calendar-light view of activity.

Differs from `/eidos:next`:
- **next** is forward-looking: "what should I work on?"
- **pickmeup** is backward-looking: "what happened while I was away?"

They complement each other — pickmeup for context, then next for action.

## Verification

- Finds all commits, plans, and artifacts within the time window
- Timeline groups correctly by date with no silent days shown
- Plan progress is accurate (checked against actual `[x]`/`[ ]` counts)
- "Where you left off" narrative is coherent

## Interactions

- [[spec - next skill - aggregate actionable items across project]] — pickmeup's "Still Open" section overlaps with next's scope
- [[spec - planning - structured intent between spec and code]] — reads plan files for progress
- [[spec - git workflow - branch per task with atomic commits]] — reads git history

## Mapping

> [[skills/pickmeup/pickmeup.md]]
