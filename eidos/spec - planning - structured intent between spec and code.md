---
tldr: Planning as a distinct mode that structures work between spec intent and code execution
---

# Planning — structured intent between spec and code

## Target

Planning is a distinct mode of work.
It sits between knowing what the system should be (spec) and making it real (code).
Without a plan, multi-step work either gets done reactively or loses coherence across sessions.

Planning deserves its own spec because it's more than a skill — it's a workflow mode with its own philosophy, constraints, and interactions.

## Behaviour

- Planning mode is entered when work is non-trivial — multiple steps, unclear scope, or cross-cutting concerns
- A plan produces a file in `memory/` that persists across sessions
- The plan references specs for what should be built (linking intent to execution)
- Plans are living documents — they evolve as implementation reveals new information
- The action loop enforces discipline: implement → commit → update plan → commit plan → continue
- Progress tracking is the session handoff mechanism — without it, the next session starts blind
- Plans can be created from specs (formal, top-down) or from observations (organic, bottom-up)
- The human decides when to plan — the assistant suggests but doesn't force planning mode
- Small work doesn't need a plan — judgment call, not a rule

### When to Plan

- Multi-step work that spans more than a few commits
- Work where the sequence matters (dependencies between steps)
- Unclear scope that needs structuring before implementation
- Cross-cutting changes that touch multiple specs or subsystems
- Work that will span multiple sessions

### When Not to Plan

- Single-action fixes or changes
- Work where the next step is obvious and self-contained
- Exploration or research (use `/eidos:research` instead)
- Pure spec work (adjust specs directly)

## Design

### Plans as Bridge

```
spec (what it should be)
  ↓
plan (how to get there, in what order)
  ↓
code (what it is)
```

Specs describe the destination.
Plans describe the journey.
Code is the result.

Plans are procedural by nature — they have a beginning, middle, and end.
This is why they live in `memory/`, not `eidos/`.
Specs describe timeless intent; plans describe time-bound work.

### The Action Loop

The action loop is the core discipline of planning:

```
1. Read current plan state
2. Pick the next incomplete action
3. Implement
4. Commit code
5. Update plan (mark done, add observations with =>, add Progress Log entry)
6. Commit plan
7. Report status
8. Ask to continue
```

This loop is mandatory, not optional.
The plan update is part of the action, not cleanup after it.
Skipping plan updates defeats the purpose — the plan becomes stale and the next session starts blind.

### Postponing Actions

Actions can be deferred with `[p]` (postponed) when they're intentionally skipped — not blocked, not forgotten, just not now.
Add a `=>` note with the reason:

```
4. [p] Add comprehensive error messages
   - => deferred — core flow works, will revisit after user testing
```

Postponed actions are skipped by the action loop, `/eidos:next`, and `/eidos:plan-continue`.
They remain visible in the plan as a record of what was consciously deferred.
To resume a postponed action, change `[p]` back to `[ ]`.

### Inline Observations During Work

Work reveals things the plan didn't anticipate.
These are captured inline under the action with `=>` prefix:

```
2. [x] Implement auth middleware
   - => discovered existing rate limiter in utils/
   - => session tokens chosen over JWT — simpler for our case
   - => created [[spec - auth - session based authentication]]
```

Inline observations feed back into specs.
A plan that only checks boxes without capturing discoveries wastes the learning opportunity.

### Structured Observations from Testing

After a phase completes, the human tests the result and reports what doesn't match expectations.
These are larger-scope findings than inline `=>` notes — they describe visible behaviour gaps, not implementation details.

Structured observations live inside the phase they relate to, as a sub-section after the actions.
Numbered per-phase: P2-O1, P6-O3, etc. — keeps references local and unambiguous.
Each has: short title, Was/Expected (or Was/Fix/Verify), optional Impact and Spec notes.
Marked `FIXED` in the title when resolved.
Implementation tasks reference their observations: `[ ] Fix P6-O1 — line numbers per-line`.

The observation loop:

```
1. Phase completes → user tests
2. User describes what's wrong (/eidos:observe)
3. Observations structured and added to plan
4. Specs updated where design intent needs clarification
5. Implementation tasks added to current or new phase
6. Normal action loop picks up the new tasks
```

This is the organic workflow loop in action: observe → adjust spec → push to code → discover → observe again.
The plan is the vehicle that keeps this loop structured rather than ad hoc.

### Plan Evolution

Plans change as work progresses.
The Adjustments section in the plan file captures these changes with timestamps.
Don't delete history — add to it.
A plan that evolved is more valuable than one that was perfect from the start.

## Verification

- Plans reference relevant specs in their Context section
- The action loop is followed consistently (plan updated after every action)
- Progress Log reflects actual work done
- Inline observations captured with `=>` provide useful context for future sessions
- Structured observations from testing are numbered, tracked, and resolved via the plan

## Friction

- Overhead for small work — planning a single-commit change wastes effort
- Plan staleness if the action loop isn't followed
- Judgment required on when to plan vs when to just do

## Interactions

- [[spec - eidos - spec driven development loops]] — planning is a procedural concern within eidos
- [[spec - plan skill - structured plan for multi step work]] — the `/eidos:plan` skill creates plan files
- [[spec - plan-continue skill - resume work on existing plan]] — the `/eidos:plan-continue` skill resumes plans
- [[spec - observe skill - capture testing observations mid plan]] — the `/eidos:observe` skill structures testing findings into plan entries
- [[template - plan - structured phases with actions and progress tracking]] — defines plan file structure
- [[spec - externalise - persist insights beyond the conversation]] — plans are one form of externalisation
