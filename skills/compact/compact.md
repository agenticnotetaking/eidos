---
tldr: Pre-compact readiness check — verify nothing is lost before clearing session
category: utility
---

# /eidos:compact

Readiness check before compacting or clearing a session.
Not a wrap-up — a pre-flight check that confirms it's safe to let go of current context.

## Usage

```
/eidos:compact
```

## Instructions

### 1. Check Git Status

Run `git status`.
Flag:
- Uncommitted changes (staged or unstaged)
- Untracked files in `eidos/` or `memory/` that might be lost

If clean, note it and move on.
If dirty, list what's pending — the user decides whether to commit or discard.

### 2. Check Active Plan

Look for active plans in `memory/` (files matching `plan - *` with an `active` phase).

If an active plan exists:
- Check whether the Progress Log has a recent entry for this session's work
- Check for any `[x]` actions missing `=>` notes
- Check for in-progress (`[ ]`) actions that look started but unfinished

If the plan is current, note it.
If the plan needs updating, say what's stale — don't fix it automatically.

### 3. Check Open Todos

Scan `memory/` for `todo - *` files.
List any that were relevant to this session's work (based on branch name or recent commits).
Not a blocker — just awareness.

### 4. Verdict

Summarise as one of:

**Clean:**
```
Ready to compact.
- Git: clean
- Plan: up to date
- No loose ends

Safe to /compact or start a new session.
```

**Pending items:**
```
Not quite ready:
- [list items that need attention]

Fix these first, or proceed if they're intentional.
```

## Output

- Reports: git status, plan state, open todos, verdict
- No other files created or modified
