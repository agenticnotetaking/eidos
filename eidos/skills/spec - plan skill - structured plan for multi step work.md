---
tldr: Create a persistent plan file for multi-step work with phases, actions, and progress tracking
---

# /eidos:plan

## Target

Non-trivial work benefits from a plan before implementation.
A plan file in `memory/` persists across sessions and tracks progress — unlike chat, which is ephemeral.
The plan skill gathers context, structures work into phases and actions, and produces the file.

## Behaviour

- Args: optional brief description of what to plan
- Searches for related specs in `eidos/`, goals and proposals in `memory/`
- Clarifies scope and approach with the user via dialogue
- Drafts actions as atomic units (one action = one commit)
- Creates `memory/plan - <timestamp> - <claim>.md` using [[template - plan - structured phases with actions and progress tracking]]
- Commits the plan file
- Offers next steps: start working, adjust, or save for later

## Design

The plan sits between intent (specs) and execution (code).
It references specs for what should be built and produces procedural records as work progresses.

The plan file is a living document:
- Actions get checked off as completed
- Observations and created files are tracked inline under each action with `=>` prefix
- Progress Log is updated after every action (this is part of the action, not optional)
- Adjustments section captures plan changes with timestamps

### Workflow

1. **Gather context** — find related specs, goals, proposals
2. **Clarify** — ask the user about scope, approach, constraints
3. **Draft** — structure work into phases with ordered actions
4. **Review** — present draft for user approval
5. **Create** — write the file, commit
6. **Offer** — start working, adjust, or defer

### After Each Action

The plan MUST be updated as part of every completed action:

```
implement → commit code → update plan (mark task, add Progress Log entry) → commit plan → continue
```

## Verification

- Plan file follows the template structure
- Actions are atomic and ordered with dependencies respected
- Related specs are linked in Context
- Plan is committed before work begins

## Interactions

- [[spec - template - basis for output files]] — plan template lives here
- [[spec - push skill - implements code to match spec]] — push can create plans for larger changes
- [[spec - eidos - spec driven development loops]] — plans are procedural artifacts in `memory/`

## Mapping

> [[skills/plan/plan.md]]
