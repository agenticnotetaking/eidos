---
tldr: Resume work on existing plan
category: planning
---

# /eidos:plan-continue

Resume work on an existing plan file.

## Usage

```
/eidos:plan-continue [plan-name]
```

## Instructions

### 1. Find Active Plans

Search `memory/` for `plan - *.md` files.
Identify incomplete plans by checking:
- Actions without `[x]` completion markers (note: `[p]` postponed actions don't count as incomplete — a plan with only `[x]` and `[p]` actions may be effectively done)
- Status field not `completed` or `abandoned`
- Progress Log entries indicating in-progress work

### 2. Select Plan

**Single incomplete plan:**
```
Only one incomplete plan found: [[plan - 2602101030 - add user auth]]

Next action: Implement login endpoint

continue?
```

**Multiple incomplete plans:**
```
Active plans found:

1 - [[plan - 2602101030 - add user auth]]
  - 3/5 actions complete
  - Next: Implement login endpoint

2 - [[plan - 2602091500 - refactor database layer]]
  - 1/4 actions complete
  - Next: Add connection pooling

Which plan to continue?
```

**No incomplete plans:**
```
No incomplete plans found.

Options:
1 - Create a new plan with /eidos:plan
2 - View completed plans
```

### 3. Load Context

When a plan is selected, read in order:

1. **The plan template** — [[template - plan - structured phases with actions and progress tracking]] (understand expected structure)
2. **The plan file** — understand actions and progress
3. **Linked specs** in `eidos/` — refresh on requirements
4. **Linked goals** in `memory/` — understand desired outcome
5. **Observations** — check for open (non-FIXED) observations that need implementation
6. **Progress Log** — see where we left off
7. **Learnings** — apply discovered insights

### 4. Present Current State

```markdown
## Resuming: [[plan - 2602101030 - add user auth]]

**Spec:** [[spec - user authentication]]

### Progress
1. [x] Set up auth middleware
   - => chose Express middleware over custom wrapper
2. [x] Create user model
   - => [[spec - user model - email based identity]] created
   - => found existing password hashing in utils/crypto.ts
3. [ ] Implement login endpoint
4. [ ] Implement logout endpoint
5. [p] Add session management
   - => deferred — cookie-based auth sufficient for now

### Next Action
Implement login endpoint (skipping 5 — postponed)

Ready to continue?
```

### 5. Continue Work

When user confirms:
1. Begin work on next incomplete `[ ]` action (skip `[p]` postponed actions)
2. Commit after each logical change
3. **IMPORTANT: After every completed action, update the plan file and commit it.**
   - Before marking `[x]`, verify every sub-bullet against actual output (run it, look at it, test it)
   - Only mark `[x]` when all sub-bullets are satisfied — partial stays `[ ]` with `=>` notes for what's done and what remains
   - Add `=>` sub-notes that account for every sub-bullet, not just what was built
   - Add brief Progress Log entry with timestamp
   - The plan is the persistent record — chat is ephemeral.

Action loop:
```
implement → verify each sub-bullet → commit code → update plan ([x] or [ ] with => notes, Progress Log) → commit plan → continue?
```

### 6. Quick Continuation

After completing each action:
```
Completed: Implement login endpoint

Next: Implement logout endpoint
continue?
```

When a phase completes and the result is something the user can see or try, tell them what's now testable:
```
Phase 2 complete.

You can now test: [what to try, where to look, what command to run]

Next: Phase 3 — [description]
continue?
```

### 7. Handling Observations

When the user reports issues during testing (what they see vs what they want), use `/eidos:observe` to structure them.
Observations become numbered entries in the plan and generate implementation tasks.

When resuming a plan that has open (non-FIXED) observations:
- Note them in the state presentation
- Observation-generated tasks are normal actions — pick them up in order like any other
- When an observation's tasks are all done, mark it FIXED

## Output

- Resumes work on selected plan
- Updates plan file with progress after each action

## When to Use

- Starting a new session to continue previous work
- Returning to a paused plan
- Checking status of active work
