---
tldr: Resurface recent activity to re-enter a project after time away
category: observation
---

# /eidos:pickmeup

Re-entry point after days away — surface what happened, what's open, and where you left off.

## Usage

```
/eidos:pickmeup [days]
```

- `days` — how many days back to look (default: 3)

## Instructions

### 1. Determine Window

Parse the optional `days` argument (default 3).
Calculate the start date.

### 2. Gather Git Activity

```bash
# Commits in the window, grouped by date
git log --since="<days> days ago" --format="%h %ad %s" --date=short

# Branches touched in the window
git log --since="<days> days ago" --all --format="%D" | grep -oE 'task/[^ ,]+' | sort -u

# Files changed in the window
git log --since="<days> days ago" --name-only --format="" | sort -u
```

Group commits by date, most recent first.
Only show dates where something actually happened — skip silent days.

### 3. Gather Memory Artifacts

Scan `memory/` for files with timestamps inside the window:

- **Plans** — active or recently completed (`plan -`)
  - For each plan: read status, show phase progress (e.g., "Phase 2: 3/5 done")
- **Sessions** — session exports (`session -`)
- **Decisions** — decisions made (`decision -`)
- **Solved** — completed todos (`solved -`)
- **Todos** — still open (`todo -`)

Match timestamps in filenames (`YYMMDDHHMM`) against the window.

### 4. Gather Open Work

Same as `/eidos:next` but summarised, not interactive:

- Incomplete plan actions (count per plan)
- Open todos
- Unprocessed goodjobs

### 5. Compose the Pickmeup

Create `memory/pickmeup - <timestamp> - <claim>.md` with this structure:

```markdown
---
tldr: Pickmeup for <start date> to <end date>
---

# Pickmeup: <start date> — <end date>

## Timeline

### <date> (<day name>)
- `abc1234` commit message
  - [changed-file.md](<path>)
- `def5678` commit message
- => branch `task/feature-name` active

### <earlier date> (<day name>)
- ...

## Plans

### [[plan - YYMMDDHHMM - claim]]
- **Status:** active
- **Progress:** Phase 2 — 3/5 actions done
- **Last action:** description of most recent [x] action
- **Next action:** description of next [ ] action

## Decisions Made
- [[decision - YYMMDDHHMM - claim]] — one-line summary

## Completed
- [[solved - YYMMDDHHMM - claim]]

## Still Open
- [[todo - YYMMDDHHMM - claim]]
- N unprocessed goodjobs

## Where You Left Off

Brief narrative (2-3 sentences) synthesising: what was the focus, what got done, what's the natural next step.
```

### 6. Present and Commit

Show the pickmeup content directly in chat.
Commit the file.

Then ask:

```
Ready to pick up where you left off?

1 - Continue active plan
2 - Work on open todo
3 - Something else

What feels right?
```

## Output

- Creates: `memory/pickmeup - <timestamp> - <claim>.md`
