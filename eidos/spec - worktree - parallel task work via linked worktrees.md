---
tldr: Sibling-directory worktrees for parallel task work — skill to create, list, complete, and session-start awareness
---

# Worktree — parallel task work via linked worktrees

## Target

Branch-per-task means one active working directory at a time.
Switching between tasks requires stashing or committing, and you lose the physical separation.
Git worktrees let you check out multiple branches simultaneously in separate directories — parallel work without the context-switching tax.

## Behaviour

### Creating a Worktree

`/eidos:worktree <task-description>` creates a linked worktree:

- Path: `../<repo-name>--<task-description>/` (sibling directory)
- Branch: `task/<task-description>` (created automatically, branched from `main`)
- If `git_prefix` is configured, branch becomes `<prefix>/task/<task-description>`
- The repo name is the basename of the main worktree's root directory

Example:
```
# From ~/repos/eidos (main worktree, on main)
/eidos:worktree auth-fix

# Creates:
#   ~/repos/eidos--auth-fix/   (linked worktree)
#   branch: task/auth-fix      (checked out in that worktree)
```

Refuses if:
- A worktree with that name already exists
- The branch name is already in use (checked out elsewhere)

### Listing Worktrees

`/eidos:worktree list` shows all worktrees for this repo:

```
Worktrees for eidos:

→ ~/repos/eidos                 main           (main worktree)
  ~/repos/eidos--auth-fix       task/auth-fix  (2 commits ahead)
  ~/repos/eidos--perf-tuning    task/perf      (5 commits ahead)
```

Current worktree marked with `→`.
Commit count ahead of main gives a sense of how much work is in each.

### Completing a Worktree

`/eidos:worktree complete [<task>]` merges and removes a worktree:

1. If `<task>` is omitted and you're inside a linked worktree, use the current one
2. If `<task>` is omitted and you're in the main worktree, show the list and ask which to complete
3. Show what will be merged (commits, files changed)
4. Ask for confirmation before merging
5. On confirmation:
   - Switch to main worktree's `main` branch
   - `git merge --no-ff task/<task-description>`
   - `git worktree remove <path>`
6. On decline: do nothing

Refuses if:
- The worktree has uncommitted changes — ask the user to commit or discard first
- The worktree is the main worktree

### Session-Start Awareness

At session start, detect worktree state via `git worktree list`:

**When in a linked worktree:**
Announce in first response:
> Worktree: **task/auth-fix** (`~/repos/eidos--auth-fix`)

**When multiple worktrees exist (in any worktree):**
List other active worktrees after the announcement or greeting:
```
Other worktrees:
  ~/repos/eidos--perf-tuning    task/perf (5 commits ahead)
```

**When only the main worktree exists:** say nothing.

### Config Toggle

- `.eidos-config.yaml` key: `worktrees` (boolean, default `true`)
- When `false`: session-start skips worktree detection, skill still works on demand
- Follows [[spec - config - toggleable project settings]] patterns

## Design

### Why Sibling Directories

Worktrees can't nest inside the repo they're linked from (they're full checkouts of the same repo).
Sibling directories are the natural location — visible in file managers, easy to `cd` to, and the naming convention makes the relationship clear.

The `<repo>--<task>` pattern uses double dash as separator — unlikely to collide with repo names and visually distinct.

### Relationship to Branch-per-Task

Worktrees don't replace the branch workflow — they extend it.
Each worktree checks out a `task/` branch, following the same naming convention.
The difference is physical: instead of switching branches in one directory, each task gets its own directory.

Within a worktree you can still switch branches freely — a worktree is just a checkout location, not a branch lock.
But typically each worktree stays on its task branch.

### Shared State

Git worktrees share:
- All refs (branches, tags)
- Object database (commits, blobs)
- Config (`.gitconfig`, hooks)
- Reflog

Per-worktree:
- Working directory (files on disk)
- Staging area (index)
- HEAD (which branch is checked out)

This means `memory/`, `eidos/`, and all other tracked files are per-checkout — each worktree sees its branch's version.
Once merged, everything consolidates.

### Complete Flow

Complete is deliberately interactive (show changes, ask confirmation) because merging affects shared history.
This matches the existing git workflow principle: uncommitted changes require user decision before branch operations.

After removal, the directory is gone but the branch remains — consistent with "never delete branches after merging."

## Verification

- `/eidos:worktree my-task` → creates `../<repo>--my-task/` with `task/my-task` branch
- `/eidos:worktree list` → shows all worktrees with current marked
- `/eidos:worktree complete` from linked worktree → shows changes, asks confirmation, merges --no-ff, removes directory
- Session start in linked worktree → announces worktree name and path
- Session start with multiple worktrees → lists others
- Session start with only main worktree → no mention
- Worktree with uncommitted changes → complete refuses, asks to commit/discard
- `git_prefix` configured → branch uses prefix
- `worktrees: false` in config → session-start skips detection

## Friction

- Sibling directories can clutter the parent folder if many worktrees accumulate
- Each worktree is a full checkout — disk usage scales linearly (though git shares objects)
- IDE/editor needs to open the worktree directory separately — it's a different path
- `complete` from within the worktree being removed is awkward — the working directory disappears. The skill should `cd` to main worktree first or instruct the user to switch.

## Interactions

- [[spec - git workflow - branch per task with atomic commits]] — worktrees use the same branch naming, merge discipline, and status reporting
- [[spec - config - toggleable project settings]] — adds `worktrees` setting
- [[spec - session context - composable snippet based context injection]] — worktree detection added to session-start
- [[spec - nested projects - sub-project isolation with shared git]] — worktrees are orthogonal; nested projects use `git_prefix` which worktrees also respect

## Mapping

> [[skills/worktree/worktree.md]]

## Future

{[?] Worktree-aware status — `/eidos:status` could show progress across all worktrees}
{[?] Auto-complete stale worktrees — detect worktrees with no recent commits and offer cleanup}
