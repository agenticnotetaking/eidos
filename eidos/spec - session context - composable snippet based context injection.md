---
tldr: Session context is composed from core snippets, config-gated feature snippets, and dynamic project state
---

# Session Context — composable snippet-based context injection

## Target

Claude needs rules and orientation at session start.
A monolithic context file mixes always-on rules with optional features and can't adapt to project configuration.
Snippet-based composition lets the session-start hook assemble the right context for each project.

## Behaviour

### Context sources (in injection order)

1. **Core snippet** (`inject/core.md`) — always loaded. Contains plugin rules that apply to every project using eidos.
2. **Feature snippets** (`inject/feature/*.md`) — loaded when their config key is enabled. Each file maps to a config key by convention.
3. **Dynamic context** — computed at runtime from project state (eidos specs, open comments, future items, recent changes).
4. **Session orientation** — computed from git and memory state (recent branches, open todos, open plans, last session, recent memory files).

### Feature snippet → config key mapping

Filename hyphens map to config underscores:
- `git-workflow.md` → `git_workflow`
- `status-reporting.md` → `status_reporting`

Adding a new feature-gated snippet requires only:
1. Create the snippet file in `inject/feature/`
2. Add the config key to [[spec - config - toggleable project settings]]

Missing config file or missing key → default to `true` (all features enabled).

### CLAUDE.md role

CLAUDE.md is loaded by Claude Code from the project root (the consuming project).
It contains project-specific instructions, not plugin rules.
Plugin rules live in `inject/` and are injected by the session-start hook.

For the bootstrapping case (eidos building eidos), CLAUDE.md has eidos-specific project notes.
For consumer projects, CLAUDE.md has their own project instructions.

## Design

The plugin's context is not a single document — it's a composed output.
This mirrors how the config spec works: features are toggleable, and the context reflects what's enabled.

Core rules are one file rather than many because they're small and always loaded together.
Splitting them would add directory noise without enabling independent toggling.

Feature snippets are separate files because each maps to a config key and may be independently disabled.

Dynamic context (open comments, future items, branches) stays as hook logic rather than snippets because it's computed from project state at runtime.

## Verification

- No config file → all snippets loaded (same as pre-snippet behaviour)
- Setting a feature to `false` → its snippet is not injected
- CLAUDE.md is not injected by the hook (Claude Code loads it from project root)
- No content lost in the extraction from CLAUDE.md to snippets
- PreToolUse branch-check hook respects `git_workflow` config

## Interactions

- [[spec - config - toggleable project settings]] — config keys gate feature snippets
- [[spec - eidos - spec driven development loops]] — context composition is part of plugin structure
- [[spec - git workflow - branch per task with atomic commits]] — first feature-gated snippet

## Mapping

> [[inject/core.md]]
> [[inject/feature/git-workflow.md]]
> [[inject/feature/status-reporting.md]]
> [[inject/feature/observation-images.md]]
> [[scripts/read_config.sh]]
> [[hooks/session-start.sh]]
> [[hooks/pre-tool-use-branch-check.sh]]
