---
tldr: Quickly create timestamped todo files in memory for tasks that need doing
---

# /eidos:todo

## Target

Not everything warrants a plan.
Small tasks need a quick way to be captured and tracked.
Todos are lightweight, timestamped, and rename to `solved` when done.

## Behaviour

- Args: task description
- Creates `memory/todo - <timestamp> - <claim>.md`
- Minimal structure — description and optional context
- Commits immediately
- When completed, rename `todo -` to `solved -` (preserving timestamp and claim)

## Interactions

- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — `todo` and `solved` prefixes
- [[spec - next skill - aggregate actionable items across project]] — next surfaces open todos

## Mapping

> [[skills/todo/todo.md]]
