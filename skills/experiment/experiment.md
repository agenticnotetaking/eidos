---
tldr: Log-based iterative exploration with emergent phases and intent/try/outcome steps
category: planning
---

# /eidos:experiment

Iterative exploration where each step's outcome determines the next step's intent.
For work where the shape isn't known upfront — UI design, prototyping, debugging, spikes.
The log IS the artifact, mineable for specs and learnings after.

## Usage

```
/eidos:experiment [topic]       # start a new experiment
/eidos:experiment continue      # resume an existing experiment
```

## Instructions

### Mode Detection

Check ARGUMENTS:
- If `continue` → go to **Continue Mode**
- Otherwise → go to **Start Mode** (ARGUMENTS is the topic)

---

### Start Mode

#### 1. Clarify Desired Outcome

Brief dialogue — 1–2 questions, skip what's obvious from the topic.
Focus on:
- What are we trying to achieve or figure out?
- Any known constraints or invariants upfront?

#### 2. Create Experiment File

**Always run `date '+%y%m%d%H%M'` to get the actual current time.**

Create `memory/experiment - <timestamp> - <claim>.md`:

```markdown
---
tldr: Brief description of what we're exploring
status: active
---

# Experiment: [Brief description]

## Context

- Related: [[...]]

**Desired outcome:** [from the dialogue]

**Resolution:** _[filled at experiment end]_

## Invariants

_[none yet — added as they're discovered]_

## Phase 1: [name or "TBD"] - status: open

```

Include Context links if related specs, plans, or prior experiments exist.
Include known invariants if any were identified during clarification.

#### 3. Branch and Commit

Create a branch (`task/experiment-<name>`) unless already on a working branch.
Commit the experiment file.

#### 4. Begin Phase 1

Ask for or propose the first step's intent.
Format:

```
Experiment started: [[experiment - <timestamp> - <claim>]]

**Phase 1** — what should we try first?
```

---

### Continue Mode

#### 1. Find Experiment

Search `memory/` for `experiment - *.md` files with status not `completed` or `abandoned`.

**Single active experiment:** load it directly.
**Multiple active experiments:** present a selection list.
**No active experiments:** offer to start a new one.

#### 2. Read and Assess State

Read the experiment file thoroughly.
Determine:
- Which phase is current (last phase without `status: done` or `status: abandoned`)
- Whether there are open steps without outcomes
- Whether the last outcome suggests a direction
- Current invariants list

#### 3. Present State and Propose Next

**If open tasks/steps exist in current phase** — infer the next step from context and propose it:

```
Resuming: [[experiment - <timestamp> - <claim>]]

**Phase N: [name]** — [M steps completed]
Last outcome: [brief summary]
Invariants: [count] active

Proposed next step:
**Intent:** [inferred from last outcome]

Proceed, or different direction?
```

**If current phase is complete** — summarise and ask for direction:

```
Resuming: [[experiment - <timestamp> - <claim>]]

**Phase N: [name]** — done
Takeaway: [phase takeaway summary]
Invariants: [count] active

What's the next intent? Or is the experiment done?
```

**If a direction shift is apparent** — suggest a new phase:

```
The last outcome suggests a shift from [old focus] to [new focus].
Start Phase N+1, or continue in Phase N?
```

---

### Working Within an Experiment

These apply in both modes once work is underway.

#### Recording Steps

Each step follows the intent/try/outcome pattern.
Write the step to the experiment file as work progresses:

1. **Before starting:** write the Intent
2. **During work:** write the Try (what was actually done)
3. **After:** write the Outcome (what happened, what we observed)

```markdown
### Step N.M

**Intent:** [what we're trying]
**Try:** [what we did]
**Outcome:** [what happened]
- => [inline observations]
- => invariant: [promoted to Invariants section]
```

Steps can contain checkbox tasks for concrete sub-actions:
```markdown
**Try:**
- [x] Changed the layout to flex
- [x] Added responsive breakpoints
- [ ] Tested on mobile viewport
```

#### Phase Transitions

A new phase starts when:
- The direction or focus shifts (suggest it: "this feels like a new direction — new phase?")
- The user explicitly says "new phase"

When closing a phase:
1. Write the **Phase takeaway** — what shifted in understanding
2. Update phase status to `done`
3. Promote any discovered invariants to the top-level Invariants section
4. Commit the experiment file

When starting a new phase:
1. Review the invariants list — these are the "don't break this" contract
2. Name the new phase (can be backfilled later)
3. Ask for or propose the first step's intent

#### Invariants

Invariants are constraints that must hold across phases.
They can be:
- **Discovered** — emerge from a step's outcome, marked with `=> invariant:` and promoted to the Invariants section
- **Specified** — stated upfront or added explicitly by the user

Format in the top-level section:
```markdown
## Invariants

- [description of what must remain true]
  - origin: Phase 1, Step 1.2
  - [notes on why this matters]
```

Before starting each new phase, surface the invariants list as a reminder.

#### Ending an Experiment

An experiment ends when:
- The work converges on artifacts that are good enough
- The experiment is abandoned (with learnings)
- The experiment gets absorbed into a spec or plan

To end:
1. Fill the **Resolution** section — what happened, artifacts produced, learnings, specs to extract
2. Update frontmatter `status` to `completed` or `abandoned`
3. Commit the experiment file
4. Offer next steps:

```
Experiment completed: [[experiment - <timestamp> - <claim>]]

Options:
1 - Extract specs with /eidos:toeidos
2 - Create a plan from learnings with /eidos:plan
3 - Done
```

#### Commits and Status Reporting

- Commit the experiment file after each meaningful step (outcome recorded)
- After each step, report per the standard pattern (branch, recent commits, summary)
- Preview the next step or ask for direction

## Output

- Creates: `memory/experiment - <timestamp> - <claim>.md`
- Branch: `task/experiment-<name>` (unless on existing working branch)
