---
tldr: Aggregate actionable items from plans, specs, and todos into a prioritised snapshot
---

# /eidos:next

## Target

Actionable items scatter across plans, specs ({!} markers), and todo files.
Starting a session or choosing what to work on next requires seeing them in one place.

## Behaviour

- Scans `memory/` for: incomplete plan actions, open todos
- Scans `eidos/` for: `{!}` items (planned), open `{{comments}}`
- Aggregates into a prioritised list
- Creates `memory/next - <timestamp> - <claim>.md`
- Presents via [[spec - numbered lists - structured selectable output]] for user selection

## Design

Next is read-only aggregation — it doesn't change any files.
Selection leads to action (start a plan action, resolve a todo, process a comment).

Priority heuristic:
1. In-progress plan actions (already started)
2. Open plan actions (next in sequence)
3. Unresolved `{{comments}}` (spec refinement needed)
4. `{!}` items (planned but not yet in a plan)
5. Standalone todos

## Verification

- Finds all actionable items across memory/ and eidos/
- Prioritisation is sensible
- Selection leads to the right action

## Interactions

- [[spec - plan skill - structured plan for multi step work]] — surfaces incomplete plan actions
- [[spec - eidos - spec driven development loops]] — surfaces {!} items and \{{comments}}

## Mapping

> [[skills/next/next.md]]
