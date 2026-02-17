---
tldr: Create persistent plan for multi-step work
category: planning
---

# /eidos:plan

Create a persistent plan file for multi-step work.

## Usage

```
/eidos:plan [brief description]
```

## Instructions

### 1. Gather Context

Search for related artifacts:
- Specs in `eidos/` that relate to the work
- Goals (`memory/goal - *.md`) or proposals (`memory/proposal - *.md`)

If found, link to them in the plan's Context section.
If not, gather context from the user.

### 2. Clarify the Plan

Use AskUserQuestion to gather details.

If a brief description was provided, confirm understanding.
Otherwise ask:
- What should this plan accomplish?
- What are the key steps?
- Any constraints or preferences?

Follow up as needed on:
- **Scope** — what's in and what's out?
- **Approach** — preferred methods or technologies?
- **Verification** — how will we know it's done?
- **Decisions** — open choices to resolve before starting

### 3. Draft Actions

Structure work into phases with ordered actions.
Each action should be:
- **Atomic** — one logical unit of work, one commit
- **Verifiable** — clear completion criteria
- **Ordered** — dependencies respected

Prefer phasing that surfaces visible, human-testable results early.
If a phase can end with something the user can see or try, structure it that way — unless it would require a significant detour from the natural implementation order.
This isn't a hard rule, but when the effort difference is small, early visibility wins.

Present the draft for user review before creating the file.

### 4. Create Plan File

Read the template: [[template - plan - structured phases with actions and progress tracking]]

Create `memory/plan - <timestamp> - <claim>.md` following the template structure.
Fill in:
- Frontmatter with current timestamp
- Context with links to related specs/goals
- Phases with drafted actions
- Verification criteria

### 5. Commit

Commit the plan file immediately after creation.

### 6. Offer Next Steps

```
Plan created: [[plan - <timestamp> - <claim>]]

Options:
1 - Start working on the first action
2 - Review and adjust the plan first
3 - Save for later (use /eidos:plan-continue to resume)
```

## IMPORTANT: Update the Plan After Every Action

The plan file MUST be updated as part of every completed action's commit cycle.
This is not optional cleanup — it's part of the action itself.

After each action:
```
implement → commit code → update plan → commit plan → continue
```

Plan update includes:
1. Mark action `[x]`
2. Add `=>` sub-notes under the action for observations, decisions, and created files
3. Add brief Progress Log entry with timestamp

```
3. [x] Implement login endpoint
   - use bcrypt for password hashing
   - => session tokens chosen over JWT — simpler for our case
   - => [[spec - auth - session based authentication]] created
```

The plan is the persistent record for future sessions.
Chat is ephemeral.
If the plan isn't updated, the next session has no idea what happened.

## Plans Are Living Documents

Plans can and should be adjusted as work progresses.

When adjustments are needed:
1. Document the change in Adjustments with timestamp and reason
2. Update the Phases/Actions as needed
3. Don't delete history — mark completed items, add new ones

## Output

- Creates: `memory/plan - <timestamp> - <claim>.md`
- Status field starts as `active`

## Status Values

For both the plan and its phases:
- `open` — not started yet
- `active` — work in progress
- `paused` — on hold (document why in Adjustments)
- `completed` — all actions done, verification passed
- `abandoned` — stopped (document why in Adjustments)
