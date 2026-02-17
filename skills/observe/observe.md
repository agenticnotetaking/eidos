---
tldr: Capture testing observations mid-plan — structure issues, update specs, inject tasks
category: observation
---

# /eidos:observe

Capture what you see that doesn't match what you want.
Used in-session during active plan work — typically after a phase completes and you test the result.
Observations become structured plan entries, spec updates, and implementation tasks.

## Usage

```
/eidos:observe
```

Assumes an active plan is loaded in the current session.
If no plan is active, ask which plan to attach observations to.

## Instructions

### 1. Collect Observations

The user describes what they see — batch mode, multiple issues at once.
For each observation, identify:
- **What it is now** (the current behaviour or appearance)
- **What it should be** (the desired state)

Don't structure yet — just listen and confirm understanding.

### 2. Structure Observations

Identify which phase the observations relate to (usually the most recently completed phase).
Number per-phase, continuing from existing observations: P{phase}-O{n}.

For each observation, write a structured entry:

```markdown
##### P6-O3 — Short description

**Was:** what currently happens or looks like.
**Expected:** what it should be instead.
**Impact:** what needs to change (components, specs, data).
```

If the fix is obvious, use Was/Fix/Verify instead:

```markdown
##### P6-O3 — Short description

**Was:** what currently happens.
**Fix:** what to change.
**Verify:** how to confirm it's fixed.
```

Present the structured batch for confirmation before writing to the plan.

### 3. Update Plan

Add observations inside the relevant phase, as a sub-section after the actions.
Include a timestamp header if this is a new observation batch for that phase:

```markdown
#### Observations (from YYMMDDHHMM user testing)

##### P6-O1 — Line numbers should be per-line, not per-block

**Was:** only block elements got line numbers.
**Expected:** each list item, table row, blockquote child shows its own line number.
```

If the phase already has observations, add after the existing ones.

### 4. Update Specs

For each observation that implies a spec change:
- Read the relevant spec
- Update the spec to reflect the desired state
- Note the spec update in the observation entry:

```markdown
**Spec:** updated — brief description of what changed.
```

Not every observation needs a spec change — only those that clarify or correct design intent.

### 5. Add Tasks to Plan

For each observation (or group of related observations), add implementation tasks.
Tasks reference their observations by phase-scoped ID:

```markdown
1. [ ] Fix P6-O1 — line numbers per-line
   - recursive AST walk for list items
   - see P6-O1 for details
2. [ ] Fix P6-O2, P6-O3 — sidebar viewport and compression
   - related fixes, single code change
```

**Same phase** — if the phase is still open or the fix belongs there, add actions to it.
**New phase after current** — if observations form a distinct chunk of work, insert a new phase.

Group related observations into single actions when the fix is the same code change.

### 6. Commit

Commit plan + spec changes together.
Message: `observations P{n}-O{a}–O{b}: brief summary`

### 7. Offer Next Step

```
Observations P{n}-O{a}–O{b} recorded.
{count} spec(s) updated, {count} task(s) added to {phase name}.

Implement now, or continue with current plan flow?
```

## Interactions

- [[spec - planning - structured intent between spec and code]] — observations are part of the plan lifecycle
- [[template - plan - structured phases with actions and progress tracking]] — defines the per-phase Observations sub-section
- [[spec - plan-continue skill - resume work on existing plan]] — plan-continue picks up observation tasks normally
