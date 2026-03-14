---
tldr: Skill spec for /eidos:worktree — create, list, and complete git worktrees as sibling directories
---

# Worktree Skill — parallel task work via linked worktrees

## Target

Provide a skill interface for creating and managing git worktrees.
The skill translates the worktree spec's behaviour into actionable Claude Code instructions.

## Behaviour

### Commands

- `eidos:worktree <task>` — create a new worktree at `../<repo>--<task>/` with branch `task/<task>`
- `eidos:worktree list` — show all worktrees with current marked, commits ahead of main
- `eidos:worktree complete [<task>]` — show changes, ask confirmation, merge `--no-ff`, remove directory

### Naming Convention

- Worktree path: `../<repo-name>--<task-description>/`
- Branch: `task/<task-description>` (respects `git_prefix` from config)
- Double dash (`--`) separates repo name from task

### Safety

- Create refuses if path or branch already exists
- Complete refuses if worktree has uncommitted changes
- Complete always asks for confirmation before merging
- Complete never targets the main worktree

## Design

The skill is a thin wrapper around `git worktree` commands.
No scripts needed — the commands are simple enough for inline bash.
The skill file provides the routing logic and output formatting.

## Verification

- `/eidos:worktree my-task` → creates sibling directory and task branch
- `/eidos:worktree list` → formatted table with current marker and commit counts
- `/eidos:worktree complete` → shows diff, asks, merges --no-ff, removes
- Edge cases: duplicate name, uncommitted changes, main worktree target

## Interactions

- [[spec - worktree - parallel task work via linked worktrees]] — parent spec with full design rationale
- [[spec - git workflow - branch per task with atomic commits]] — branch naming and merge discipline
- [[spec - config - toggleable project settings]] — respects `git_prefix`

## Mapping

> [[skills/worktree/worktree.md]]
