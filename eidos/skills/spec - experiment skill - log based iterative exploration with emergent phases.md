---
tldr: Skill for log-based iterative exploration — emergent phases with intent/try/outcome steps, designed for work where the next step depends on the last outcome
---

# Experiment Skill

Experiments are for work where you don't know the shape upfront.
Plans assume known phases and actions; experiments discover them as they go.
Each step's outcome determines the next step's intent.

The experiment file is both the working tool and the artifact — the log IS the deliverable, mineable for specs and learnings after.

## Target

Iterative, exploratory work where:
- The next step depends on the outcome of the current one
- Phases emerge from direction shifts, not upfront design
- The record of what was tried and what happened is itself valuable
- Work may converge on artifacts, get absorbed into specs/plans, or be abandoned with learnings

Plans are wrong for this because they require knowing the actions beforehand.
Research is wrong because it's about gathering information, not trying things.
Experiments are about doing and observing.

## Behaviour

### Invocation

- `/eidos:experiment [topic]` — start a new experiment
- `/eidos:experiment continue` — resume an existing experiment

### Starting (`/eidos:experiment [topic]`)

- Clarify the desired outcome with brief dialogue (1–2 questions, skip what's obvious from the topic)
- Create `memory/experiment - <timestamp> - <claim>.md` with Context, Desired Outcome, and Phase 1 header
- Create a branch (`task/experiment-<name>`) unless already on a working branch (e.g., during a plan)
- Commit the experiment file
- Begin Phase 1 — ask for or propose the first step's intent

### Continuing (`/eidos:experiment continue`)

- Read the experiment file
- If open tasks or steps exist in the current phase: infer the next step from context and propose it
- If the current phase is complete: summarise where we are, ask what the next intent is
- If a direction shift is apparent: suggest starting a new phase

### Phases

- Phases are logical groupings that share a direction or focus
- Named when the direction becomes clear — can be backfilled
- Each phase has a status: `open`, `done`, `abandoned`
- A new phase starts when:
  - The direction or focus shifts (suggested by AI)
  - The user explicitly says "new phase"
- Phase takeaway captures what shifted in understanding

### Steps

Steps within a phase record individual iterations:

- **Intent** — what we're trying to achieve this step
- **Try** — what we actually did
- **Outcome** — what happened, what we observed

Steps can also contain:
- Checkbox tasks (`[ ]`, `[x]`) for concrete actions within a step
- `=>` notes for inline observations that emerge during work
- Links to created files or artifacts

### Invariants

- Things that must remain true across phases — constraints discovered or specified during the experiment
- Discovered in phases (marked with `=>`) and promoted to a top-level Invariants section
- Each invariant has a brief description and nested bullets for notes and origin phase
- Checked before starting a new phase — the invariant list is the "don't break this" contract
- Can also be specified upfront if known constraints exist before experimenting

### Resolution

Filled when the experiment ends.
Captures: what happened, artifacts produced, learnings, specs to extract.
Lives right after Desired Outcome so the start and end of the experiment are visible together.

### Status

Mirrors plan statuses: `open`, `active`, `paused`, `completed`, `abandoned`.

### Git

- Usually its own branch: `task/experiment-<name>`
- Can run on an existing branch when the experiment is part of larger work (e.g., during a plan)
- Commit per meaningful step, not per sub-task

### Status Reporting

After each step, report per the standard pattern (branch, recent commits, summary).
Preview the next step or ask for direction.

## Design

### Template

Output path: `memory/experiment - <timestamp> - <claim>.md`

```markdown
---
tldr: Brief description of what we're exploring
status: active
---

# Experiment: [Brief description]

## Context

- Related: [[spec - ...]]
- Prior: [[experiment - ...]]

**Desired outcome:** What we're trying to achieve or figure out.

**Resolution:** _[filled at experiment end]_

## Invariants

- Invariant description
  - origin: Phase 1
  - notes on why this matters

## Phase 1: [name — can be backfilled] - status: open

### Step 1.1

**Intent:** what we're trying this step
**Try:** what we did
**Outcome:** what happened

### Step 1.2

**Intent:** ...
**Try:** ...
**Outcome:** ...
- => observation that emerged
- => [[spec - ...]] updated
- => invariant: [description — promoted to Invariants section]

**Phase takeaway:** what shifted in our understanding

## Phase 2: ...
```

### Relationship to Other Skills

- `/eidos:observe` — can be used within an experiment to structure testing observations, though the step-level intent/try/outcome often captures this naturally
- `/eidos:reflect` — useful at experiment end to extract learnings
- `/eidos:spec` or `/eidos:toeidos` — for mining the experiment log into specs
- `/eidos:plan` — an experiment can conclude by creating a plan when the shape of the work becomes clear

## Interactions

- Depends on [[spec - git workflow - branch per task with atomic commits]] (branching)
- Depends on [[spec - naming - prefixes structure filenames as prefix claim pairs]] (file naming)
- Relates to [[spec - planning - structured intent between spec and code]] (the experiment is what you do when a plan is premature)
- Relates to [[spec - externalise - persist insights beyond the conversation]] (the log externalises iterative learning)

## Mapping

> [[skills/experiment/experiment.md]]

## Future

{[?] Mine experiment for spec — automated extraction of patterns from completed experiments}
{[?] Experiment comparison — side-by-side view of multiple experiments on the same topic}
