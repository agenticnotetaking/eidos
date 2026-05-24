# Eidos — Claude Code Plugin

> This file is for developing eidos itself.
> Claude Code does not load CLAUDE.md from plugin directories — consumers of the plugin will never see this.

Spec-driven development.
Markdown specs in `eidos/` and code are two representations of the same system, kept in sync bidirectionally.
See [[spec - eidos - spec driven development loops]] for the full design.

Plugin context (rules, skills, feature snippets) is composed from `inject/` at session start.
See [[spec - session context - composable snippet based context injection]].

## This Repo vs the Plugin

This repo is both the **development environment** and the **plugin source**.
Not everything here ships to consumers:

- `memory/` — dev-only (plans, sessions, decisions for building eidos itself)
- `CLAUDE.md` — dev-only (rules for working in this repo)
- `scripts/release.sh`, `scripts/check_session_budget.sh`, `skills/release/`, `TWEET.md`, `INSTALL.md` — dev-only
- `inject/core/` — consumer-facing (injected into every project that uses the plugin; split into budget-sized section files)
- `eidos/`, `skills/`, `templates/` — consumer-facing (shipped as the plugin)

`scripts/release.sh` rsyncs to the downstream repo, filtering out dev-only files.
When adding new files, consider which scope they belong to.

## Bootstrapping

This project uses eidos to build eidos.
Read the main spec before working on anything.

## Key Concepts

- `eidos/` = what it SHOULD be (intentional)
- `memory/` = how we got here (procedural)
- Implementation = what it IS
- [[c - the spec describes the full vision - versioning is for the procedural plan]]
- [[c - eidos is self contained - definitions do not rely on external systems]]

## Workflow

1. Read the relevant spec in `eidos/` before implementing
2. Implement to match the spec's claims (in Behaviour sections)
3. Update Mapping in the spec if new files are created
4. Note any drift or open questions
5. If you notice spec is wrong or stale, surface it — don't silently diverge

## Skills: Update Skill and Spec Together

When changing a skill file (`skills/<name>/<name>.md`), always update its spec (`eidos/skills/spec - <name> skill - <claim>.md`) in the same commit or branch — and vice versa.
They are a pair: the skill is the instructions, the spec is the intent.
One should never drift from the other.

## Critical: Never touch human.md

`human.md` is the human's scratchpad — never read, edit, or reference it.
See [[c - human md is a scratchpad for uncommitted human thinking]].
