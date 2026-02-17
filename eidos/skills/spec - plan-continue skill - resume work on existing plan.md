---
tldr: Resume work on an existing plan by loading context and continuing from the next incomplete action
---

# /eidos:plan-continue

## Target

Plans span multiple sessions.
When returning to work, the assistant needs to reload context: what was planned, what's done, what's next, and what was learned.
This skill handles that handoff.

## Behaviour

- Args: optional plan name or partial match
- Searches `memory/` for incomplete `plan - *.md` files
- Auto-selects if only one is found, presents options if multiple
- Reads the plan template to understand expected structure
- Loads linked specs, goals, and learnings before resuming
- Presents current state and next action for user confirmation
- Continues with normal action loop after confirmation

## Design

Plan-continue is the session boundary skill.
It bridges the gap between ephemeral chat and persistent plan files.

The key insight: the Progress Log in the plan file IS the handoff mechanism.
Without it, the new session starts blind.
This is why updating the plan after every action is mandatory, not optional.

### Flow

1. **Find** — scan `memory/` for plans with unchecked actions
2. **Select** — auto-select or present numbered options
3. **Load** — read plan template, then plan file, linked specs, goals, learnings
4. **Present** — show progress summary and next action
5. **Confirm** — wait for user before starting work
6. **Continue** — normal action loop (implement → commit → update plan → commit plan → continue?)

### Selection Logic

- **Single incomplete plan:** show it, preview next action, ask to continue
- **Multiple incomplete plans:** numbered list with progress counts and next actions
- **No incomplete plans:** inform user, suggest creating a new plan

## Verification

- Correctly identifies incomplete plans (unchecked actions)
- Loads all linked context (specs, goals, learnings) before resuming
- Presents accurate progress state
- After resuming, follows the action loop with plan updates

## Interactions

- [[spec - plan skill - structured plan for multi step work]] — creates the plans this skill continues
- [[spec - eidos - spec driven development loops]] — plans are procedural artifacts in `memory/`

## Mapping

> [[skills/plan-continue/plan-continue.md]]
