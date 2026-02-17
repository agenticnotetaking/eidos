---
tldr: Show actionable items to work on
category: observation
---

# /eidos:next

Aggregate actionable items into a prioritised list.

## Usage

```
/eidos:next
```

## Instructions

### 1. Scan Sources (fast)

Use grep/glob to quickly filter without reading full files.
Only read a file when you need detail for presentation.

```bash
# Active plans with unchecked actions
grep -rl '\[ \]' memory/plan\ -\ *.md 2>/dev/null

# Open todos (existence = open)
ls memory/todo\ -\ *.md 2>/dev/null

# Unprocessed goodjobs
grep -rl 'status: unprocessed' memory/goodjob\ -\ *.md 2>/dev/null

# Planned items
grep -rn '{{\[!\]' eidos/ 2>/dev/null

# Postponed plan actions
grep -rn '\[p\]' memory/plan\ -\ *.md 2>/dev/null

# Open comments
${CLAUDE_PLUGIN_ROOT}/scripts/open_comments.py --path eidos/ skills/ memory/ --cap 20
```

These pattern checks are fast — don't read entire files just to check status.

### 2. Prioritise

1. In-progress plan actions (already started)
2. Open plan actions (next in sequence) — skip `[p]` (postponed) actions
3. Unresolved `{{comments}}`
4. `{[!]}` items not yet in a plan
5. Standalone todos
6. Unprocessed goodjobs
7. Postponed plan actions (`[p]`) — low priority awareness, not a call to action

### 3. Present

Use [[spec - numbered lists - structured selectable output]] format:

```
1 - Active Plan: [[plan - 2602101614 - migrate mono]]
  - 1.1 - Research skill + spec (Phase 3.1)
  - 1.2 - Architecture skill + spec (Phase 3.2)
2 - Open Comments
  - 2.1 - {{should push auto-commit?}} in spec - push
3 - Planned Items
  - 3.1 - {[!] PreToolUse hook} in spec - eidos
4 - Todos
  - 4.1 - [[todo - 2602111642 - pull spec from session context hook]]
5 - Postponed
  - 5.1 - [p] Add comprehensive error messages (plan - 2602101614 - migrate mono, Phase 4)

Which items to work on?
```

### 4. Create Snapshot

Create `memory/next - <timestamp> - <claim>.md` with the aggregated list.
Commit.

### 5. Act on Selection

Route to the appropriate action:
- Plan action → start implementing or use `/eidos:plan-continue`
- `{{comment}}` → use `/eidos:refine`
- `{[!]}` item → suggest creating a plan or implementing directly
- Todo → start the work
- Goodjob → use `/eidos:toeidos` to extract pattern, then mark `status: processed`

## Output

- Creates: `memory/next - <timestamp> - <claim>.md`
