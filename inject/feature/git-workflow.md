# Git Workflow

See [[spec - git workflow - branch per task with atomic commits]] for full details.

## No Co-Author Tags in Commits

**NEVER add "Co-Authored-By: Claude" or similar attribution to commit messages.**
Keep the git history clean — no AI attribution, no generated signatures.
Just write the commit message content.
Your help is much appreciated, and you are an amazing enabler, but the git history should stay clean.

- **Branch per task:** `task/<description>` — create before any file changes, never commit to `main`
  - If `git_prefix` is configured in `.eidos-config.yaml`, use `<prefix>/task/<description>` instead
  - Git commands work naturally from subdirectories — no special handling needed for nested projects
- **Commit per action:** one logical unit of work per commit, commit immediately, don't wait for approval
- **`--no-ff` merges:** preserves branch structure in history
- **Never delete branches** after merging — branch references are history
- **New work in existing branch:** if work diverges from the branch purpose, ask whether to merge first and create a new branch — don't silently continue
- **Uncommitted changes:** before switching branches, check `git status` — if changes exist, ask whether to stash or commit. Don't silently stash or discard.
