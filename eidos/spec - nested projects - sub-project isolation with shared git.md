---
tldr: Sub-projects run isolated eidos instances, discovering and sharing the parent's git repo via config
---

# Nested Projects — sub-project isolation with shared git

## Target

A parent project may contain sub-projects (experiments, modules, spikes) that each run their own eidos instance.
Each sub-project has its own `eidos/`, `memory/`, and `.eidos-config.yaml` — a full isolated context.
The complication: sub-projects often don't have their own `.git`, living inside the parent's repository.

This spec defines how eidos detects and handles that situation without assuming anything about the parent-child relationship.

## Behaviour

### Isolation

- Each sub-project is a standalone eidos context — its own specs, memory, config, and session context
- Wiki links do not cross project boundaries
  - A tool like Obsidian opening the parent root would resolve all links across both, but eidos treats each context as isolated
- Session-start loads only the sub-project's own `eidos/` and its own configuration for parts of eidos `inject/` — no parent context is surfaced
- Skills operate within the sub-project scope by default

### Git Detection

- When `/eidos:init` runs and no `.git` is found in the working directory, it offers a choice:
  1. **Create fresh** — `git init` a new repository here
  2. **Find parent** — walk ancestor directories to find a `.git`, use that repository
  3. **Disable git** — set `git_workflow` to off, work without version control
- If "find parent" is chosen:
  - Eidos walks up the directory tree until it finds `.git`
  - If found, asks whether branch names should use a prefix (e.g. `my-experiment/task/feature`)
  - Stores the relative path and optional prefix in `.eidos-config.yaml`
  - If not found, falls back to offering "create fresh" or "disable git"

### Config Entries

- `git_root` — relative path from sub-project to the directory containing `.git` (e.g. `../..`)
  - This is informational for eidos — git itself resolves the parent `.git` automatically
  - Tells eidos "git is available via a parent repo" so it doesn't warn about missing local `.git`
  - Skills should never check `[ -d .git ]` — they should check whether `git_workflow` is enabled
- `git_prefix` — optional string prepended to branch names (e.g. `my-experiment`)
  - When set, branch names become `<prefix>/task/<description>` instead of `task/<description>`
  - Skills that create branches must respect this prefix
- Both entries are omitted by default (no value = local `.git` assumed)

### Skill Compatibility

- Git commands work naturally from subdirectories — git walks up the tree to find `.git`
- Skills must not check for `.git` in the working directory (e.g. `[ -d .git ]`) — check `git_workflow` config instead
- When `git_workflow` is disabled, skills skip git operations silently (existing behaviour from [[spec - config - toggleable project settings]])
- Audited: no skills or hooks check `[ -d .git ]` — clean
- Branch creation: `git_prefix` documented in [[spec - git workflow - branch per task with atomic commits]] and [[inject/feature/git-workflow.md]]

## Design

### Config Format — YAML

`.eidos-config.yaml` uses YAML format.
YAML handles mixed types (booleans, strings) cleanly and is widely understood.

```yaml
git_workflow: true
status_reporting: true
skills_list: true
specs_and_concepts: true
session_context: true

# nested project git
git_root: ../..
git_prefix: my-experiment
```

- Boolean keys: `true`/`false` (replaces `[x]`/`[ ]`)
- String keys: plain values
- Missing keys use defaults (same principle as before)
- Missing file means all defaults

Config spec, config skill, `read_config.sh`, and session-start hook all migrated to YAML format.

### Why Not Submodules or Worktrees

Git submodules and worktrees solve similar problems but add complexity.
This spec targets the simpler case: directories inside a repo that want their own eidos context.
Nothing prevents a sub-project from being a submodule — the git detection flow would just find `.git` locally and skip the parent walk.

## Verification

- Run `/eidos:init` in a directory without `.git` inside a git repo → detection flow triggers
- Choose "find parent" → config written with correct relative path and optional prefix
- Git operations from sub-project directory work without extra configuration
- Branch names use prefix when `git_prefix` is configured
- Session-start in sub-project → loads only sub-project context
- No skill checks for `.git` directory directly

## Friction

- Relative paths in `git_root` break if the sub-project moves within the repo — user must update config
- Branch prefix collisions possible if two sub-projects pick the same prefix — user's responsibility
- Parent project has no awareness of which sub-projects exist — discovery is manual
- YAML config is a breaking change from markdown checkbox format — existing `.eidos-config` files need migrating to `.eidos-config.yaml`

## Interactions

- [[spec - config - toggleable project settings]] — format changes from markdown checkboxes to YAML, gains string key support
- [[spec - init - bootstrap eidos folder structure]] — init gains git detection flow for nested projects
- [[spec - git workflow - branch per task with atomic commits]] — branch naming respects `git_prefix`
- [[spec - session context - composable snippet based context injection]] — unchanged, already scoped to working directory

## Future

{[?] parent context summary — optional config to include a compact parent project summary in session-start}
{[?] cross-project wiki links — resolve `[[parent:spec name]]` syntax across boundaries}
{[?] sub-project registry — parent config lists known sub-projects for discovery}