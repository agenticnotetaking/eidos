---
tldr: One branch per task, one commit per action, --no-ff merges, status reporting after each action
---

# Git Workflow — branch per task with atomic commits

## Target

Code changes need structure.
Without it, work blurs together — commits are hard to review, rollbacks are risky, and history loses meaning.
A consistent git workflow gives each piece of work a clear boundary.

## Behaviour

- This workflow is togglable via [[spec - config - toggleable project settings]] (`git_workflow` setting)
- When disabled, none of the below is enforced

### Branching

- One branch per task: `task/<brief-description>`
  - If `git_prefix` is configured (see [[spec - nested projects - sub-project isolation with shared git]]), use `<prefix>/task/<description>` instead
- Create the branch before any file changes
- Branch from `main` (or current main branch)
- Never commit work directly to `main` after initial repo setup

### Commits

- One commit per action — an action is a logical unit of work
- Commit immediately after completing each action
- Don't batch multiple actions into one commit
- Don't wait for user approval to commit
- Brief, descriptive messages focused on what changed:
  - "Add terrain brush base class"
  - "Fix spell targeting for area effects"

### Merging

- Before switching branches, check `git status` for uncommitted changes
  - If uncommitted changes exist, ask the user whether to stash or commit them before proceeding
  - Don't silently stash or discard — the user decides
- Always use `--no-ff` (no fast-forward) merges
- This preserves branch structure in history
- Never delete branches after merging — branch references are part of history
- `git checkout main && git merge --no-ff task/<branch>`

### Status Reporting

After completing an action, report:

1. **Branch** — name and commit count
2. **Recent commits** — hash, message, files changed
3. **Summary** — what was done

Format: nested bullet lists, not tables.
File paths as clickable links: `[filename](<relative/path>)` (angle brackets for paths with spaces).

```
**Branch:** `task/my-feature` (2 commits)
- `abc1234` Add new feature
  - [feature.md](<memory/feature.md>)
- `def5678` Fix related issue
  - [feature.md](<memory/feature.md>)

**Summary:** Added feature and fixed related issue.
```

After the status report, preview the next step:
```
**Next:** [brief description]
continue?
```

### New Repos

First commit goes directly to `main` (establishes baseline).
Branch workflow applies to all subsequent work.

## Design

The branch is the work unit.
The commit is the action unit.
Together they create a history that's reviewable, rollbackable, and meaningful.

`--no-ff` merges preserve the branch shape in `git log --graph`, so you can see what work was grouped together even after merging.

## Verification

- No direct commits to main after initial setup
- Each task gets its own branch
- Merge commits preserve branch structure
- Status reports follow the format above

## Interactions

- [[spec - config - toggleable project settings]] — `git_workflow` toggle
- [[spec - nested projects - sub-project isolation with shared git]] — `git_prefix` for branch naming in sub-projects
- [[spec - eidos - spec driven development loops]] — commits happen as part of the action loop
- [[spec - plan skill - structured plan for multi step work]] — plan updates are committed as part of each action

## Mapping

> [[CLAUDE.md]]
