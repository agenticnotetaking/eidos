---
tldr: End session with export and merge offer
category: utility
---

# /eidos:done

Structured session end.

## Usage

```
/eidos:done
```

## Instructions

### 1. Export Conversation

Run `/eidos:tomd` to create a session export in `memory/`.

### 2. Offer Reflection

```
Session exported: [[session - <timestamp> - <claim>]]

Reflect on this session? (extracts learnings, tasks, incoherences)
```

If yes, run `/eidos:reflect` on the export.

### 3. Update Active Plan

If there's an active plan, add a session summary to its Progress Log:
```
- <timestamp> - Session end. [Brief summary of what was accomplished]
```

### 4. Offer Merge

Show branch status and offer to merge:
```
Branch: task/feature-name (N commits)

Merge to main? (y/n)
```

If yes: `git checkout main && git merge --no-ff task/feature-name`

## Output

- Creates: session export via tomd
- Optionally creates: reflection files via reflect
- Optionally merges: current branch to main
