---
tldr: Toggleable project settings stored in .eidos-config.yaml, presented via eidos:config skill
---

# Config — toggleable project settings

## Target

Not every project wants every eidos feature.
Git workflow enforcement, session hooks, status reporting — these are useful defaults but not universal.
Config lets a project opt in or out without editing spec files.

## Behaviour

- Settings live in `.eidos-config.yaml` at the consumer project root
- `/eidos:config` presents all available settings with current values
- Settings have defaults — a missing file means "use defaults"
- Boolean settings use `key: true`/`key: false`
- Numeric settings use `key: value` or `key: null` to disable (e.g. `context_tracking_max`)
- String settings use `key: value` (for nested project config like `git_root`, `git_prefix`)
- Skills check config before enforcing optional behaviour (e.g., git workflow)

## Design

### Config File Format

`.eidos-config.yaml` uses YAML key-value pairs:

```yaml
# branch-per-task, commit-per-action, --no-ff merges
git_workflow: true
# status report after each action
status_reporting: true
# eidos skill listing in session start context
skills_list: true
# spec/concept listing, future items at session start
specs_and_concepts: true
# session orientation: branches, todos, plans, recent memory
session_context: true
# max tokens for context window tracking (null to disable), used to warn about compaction early
context_tracking_max: 200000
# mono-repo sub-part focus injection at session start
mono_focus: true
# persist pasted images as named observation files in memory/
observation_images: true

# nested project git (only when applicable)
git_root: ../..
git_prefix: my-experiment
```

- Each setting gets a `#` comment on the line above describing its purpose
- `true`/`false` for boolean settings
- Plain values for string settings
- Comments are preserved when changing values
- Missing keys use the default value (true for booleans, omitted for strings)
- Missing file means all defaults

### Available Settings

| Key | Default | Type | Effect |
|-----|---------|------|--------|
| `git_workflow` | `true` | bool | Branch-per-task, commit-per-action, --no-ff merges |
| `status_reporting` | `true` | bool | Status report after each action (branch, commits, summary) |
| `skills_list` | `true` | bool | Skill listing (from frontmatter) in session start context |
| `specs_and_concepts` | `true` | bool | Spec/concept listing, open comments, future items, recent spec changes |
| `session_context` | `true` | bool | Session orientation: recent branches, todos, plans, last session, recent memory |
| `context_tracking_max` | `200000` | int/null | Max token count for context tracking; `null` to disable |
| `mono_focus` | `true` | bool | Mono focus injection at session start (reads external mapping) |
| `observation_images` | `true` | bool | Persist pasted images as named observation files in `memory/` |
| `git_root` | _(omitted)_ | string | Relative path to parent `.git` directory (nested projects only) |
| `git_prefix` | _(omitted)_ | string | Branch name prefix (nested projects only) |

See [[spec - nested projects - sub-project isolation with shared git]] for `git_root` and `git_prefix` usage.

### Skill Presentation

`/eidos:config` requires a complete `.eidos-config.yaml` to operate.
If the file is missing or incomplete (missing boolean keys), config offers to run `/eidos:init` to fix it — it does not create or repair the file itself.
Once config is complete, it presents settings and lets the user toggle items.
After changes, writes the updated `.eidos-config.yaml` file and commits.

```
Eidos config (.eidos-config.yaml):

  git_workflow: true        # branch-per-task, commit-per-action, --no-ff merges
  status_reporting: true    # status report after each action

Toggle which? (e.g., "git_workflow" to disable it)
```

### Inject Snippet Gating

Config keys map to feature snippets in `inject/feature/`.
Filename hyphens become config underscores: `git-workflow.md` → `git_workflow`.
The session-start hook reads config and only injects enabled snippets.
See [[spec - session context - composable snippet based context injection]].

### How Skills Check Config

Skills that depend on optional behaviour should check config early:
- Use `scripts/read_config.sh <key> [default]` to read a value
- If the relevant setting is off, skip that behaviour silently
- Don't warn about disabled features — the user made a choice

## Verification

- Missing `.eidos-config.yaml` file → all defaults apply
- Toggling a setting → file updated, value persisted
- Skills respect config (e.g., disabling git_workflow skips branch enforcement)
- String values readable via `read_config.sh` (e.g. `read_config.sh git_root ""`)

## Interactions

- [[spec - git workflow - branch per task with atomic commits]] — first feature togglable via config
- [[spec - eidos - spec driven development loops]] — config is part of plugin structure
- [[spec - session context - composable snippet based context injection]] — config gates feature snippets
- [[spec - nested projects - sub-project isolation with shared git]] — adds string config entries for nested git
- [[spec - context tracking - hook injects context usage for session awareness]] — adds `context_tracking_max` setting
- [[spec - mono skill - register working subdirectory focus in monorepo]] — adds `mono_focus` setting

## Mapping

> [[skills/config/config.md]]
> [[scripts/read_config.sh]]
> [[.eidos-config.yaml]]
