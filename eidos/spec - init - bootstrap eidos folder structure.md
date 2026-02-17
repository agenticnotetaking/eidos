---
tldr: Bootstrap eidos folder structure for new projects via /eidos:init
---

# Init — bootstrap eidos folder structure

## Target

New projects need a way to set up the eidos folder structure.
The session-start hook detects missing or incomplete setup and points users to `/eidos:init`.
`/eidos:config` also delegates here when config is missing or incomplete.

## Behaviour

- `/eidos:init` creates the eidos folder structure in the current project
- Each target is created only if missing — existing targets are reported and left untouched
- Targets: `eidos/`, `eidos/seed.md`, `memory/`, `memory/human.md`, `.eidos-config.yaml`
- `.eidos-config.yaml` is created with all settings enabled, or completed if it exists but is missing boolean keys (defaults from [[spec - config - toggleable project settings]])
- `eidos/seed.md` and `memory/human.md` are copied from `copy/` templates in the plugin directory
- Reports what was created vs what already existed
- Commits all created files if git_workflow is enabled

## Design

### Handles Partial Setups

Running init on an existing project is safe — it only adds what's missing.
Existing files and folders are never overwritten.
Config is the one exception: if `.eidos-config.yaml` exists but is missing boolean keys (e.g. after a plugin update adds new settings), init appends the missing keys with defaults while preserving existing values.

### Config Defaults

The default `.eidos-config.yaml` content comes from [[spec - config - toggleable project settings]].
Init does not present the toggle interface — it just writes defaults.
Users run `/eidos:config` afterwards to customise.

### Template Files

`eidos/seed.md` and `memory/human.md` are copied from `copy/` in the plugin directory.
Templates teach by example — they contain self-documenting notes that guide the user into the workflow and are naturally replaced with real content.

`seed.md` explains the spec-driven approach and gives different starting paths for new vs existing projects.
`human.md` demonstrates the scratchpad format with example notes the user removes as they start using it.
See [[c - human md is a scratchpad for uncommitted human thinking]].

## Interactions

- [[spec - config - toggleable project settings]] — init creates `.eidos-config.yaml` with defaults
- [[spec - eidos - spec driven development loops]] — init bootstraps the three-folder structure
- [[spec - session context - composable snippet based context injection]] — session-start hook expects these folders to exist
- [[c - human md is a scratchpad for uncommitted human thinking]] — human.md is created but never touched again

## Mapping

> [[skills/init/init.md]]
> [[copy/seed.md]]
> [[copy/human.md]]
