# Eidos — Claude Code Plugin

Spec-driven development.
Markdown specs in `eidos/` and code are two representations of the same system, kept in sync bidirectionally.
See [[spec - eidos - spec driven development loops]] for the full design.

Plugin context (rules, skills, feature snippets) is composed from `inject/` at session start.
See [[spec - session context - composable snippet based context injection]].

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

## Critical: Never touch human.md

`human.md` is the human's scratchpad — never read, edit, or reference it.
See [[c - human md is a scratchpad for uncommitted human thinking]].
