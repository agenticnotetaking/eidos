---
tldr: Create, list, and complete git worktrees for parallel task work
category: utility
---

# /eidos:worktree

Manage git worktrees for parallel task work.
Each worktree is a sibling directory with its own `task/` branch.

## Usage

```
/eidos:worktree <task>              # create a new worktree
/eidos:worktree list                # list all worktrees
/eidos:worktree complete [<task>]   # merge and remove a worktree
```

## Instructions

### 1. Determine Context

```bash
repo_root=$(git worktree list --porcelain | head -1 | sed 's/^worktree //')
repo_name=$(basename "$repo_root")
current_dir=$(pwd)
```

Read `git_prefix` from `.eidos-config.yaml` if it exists (for branch naming in nested projects).

### 2. Route by Command

Parse arguments to determine which command to run.

#### `<task>` (create)

1. Derive the worktree path and branch name:
   - Path: `<repo_root>/../<repo_name>--<task>/`
   - Branch: `task/<task>` (or `<git_prefix>/task/<task>` if prefix configured)

2. Check for conflicts:
   - Run `git worktree list` — refuse if a worktree at that path already exists
   - Run `git branch --list <branch>` — refuse if the branch already exists and is checked out elsewhere

3. Create the worktree:
   ```bash
   git worktree add -b <branch> <path> main
   ```

4. Confirm:
   ```
   Worktree created: **<task>**
     Path: `<path>`
     Branch: `<branch>`

   Open this directory in a new Claude Code session to start working.
   ```

#### `list`

1. Run `git worktree list --porcelain` and parse the output
2. For each worktree, determine:
   - Path
   - Branch (from HEAD)
   - Whether it's the main worktree (first entry) or linked
   - Commits ahead of main: `git rev-list --count main..<branch>`
3. Display:
   ```
   Worktrees for <repo_name>:

   → <path>    <branch>    (main worktree)
     <path>    <branch>    (N commits ahead)
   ```
   Mark current worktree with `→`.

#### `complete [<task>]`

1. **Resolve target:**
   - If `<task>` is provided, find the matching worktree
   - If omitted and currently in a linked worktree, use the current one
   - If omitted and in the main worktree, run `list` and ask which to complete

2. **Refuse if:**
   - Target is the main worktree
   - Target worktree has uncommitted changes (`git -C <path> status --porcelain`)
     — tell the user to commit or discard first

3. **Show what will be merged:**
   ```bash
   git log --oneline main..<branch>
   git diff --stat main..<branch>
   ```

4. **Ask for confirmation** using AskUserQuestion:
   - "Merge `<branch>` (N commits) into `main` and remove worktree at `<path>`?"

5. **On confirmation:**
   ```bash
   # Merge from the main worktree
   git -C <repo_root> checkout main
   git -C <repo_root> merge --no-ff <branch>
   git worktree remove <path>
   ```

6. **Confirm:**
   ```
   Worktree completed: **<task>**
     Merged: `<branch>` → `main` (--no-ff)
     Removed: `<path>`
   ```

### 3. Error Handling

- Not in a git repo → "Not in a git repository."
- Path already exists (not a worktree) → "Path `<path>` already exists but is not a worktree."
- Branch checked out elsewhere → "Branch `<branch>` is already checked out in `<other-path>`."

## Output

- Creates: worktree directory as sibling to repo root
- Creates: `task/` branch (branched from main)
- On complete: merges branch, removes worktree directory
