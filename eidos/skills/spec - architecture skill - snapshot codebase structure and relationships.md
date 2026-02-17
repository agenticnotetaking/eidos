---
tldr: Snapshot codebase structure, component relationships, and architectural patterns
---

# /eidos:architecture

## Target

Codebases grow organically.
Without periodic snapshots, the actual structure drifts from what anyone thinks it is.
Architecture snapshots capture the current state so it can be compared against specs and shared with new sessions.

## Behaviour

- Args: optional scope (specific directory, module, or "full")
- Act as a documentarian, not an evaluator — document what exists without suggesting improvements
- Explores codebase structure: directories, key files, entry points, dependencies
- Identifies architectural patterns in use
- Creates `memory/architecture - <timestamp> - <claim>.md`
- Commits the architecture file
- Presents summary and links to related specs
- Follow-up questions append to the existing file rather than creating a new one

## Design

Architecture snapshots are descriptive, not prescriptive.
They capture what IS, not what should be — that's the spec's job.
Comparing an architecture snapshot against specs is one input to drift analysis.

### What to Capture

- **Git State** — current branch, recent commits, active branches
- **Directory Structure** — top-level organisation, key directories and purposes
- **Tech Stack** — languages, frameworks, key dependencies, build tools
- **Module Breakdown** — major components, how they connect, data flow
- **Entry Points** — where execution begins, key config, environment requirements
- Patterns in use (state management, routing, data flow, testing)
- Notable deviations from expected patterns

## Verification

- Snapshot accurately reflects current codebase structure
- Component relationships are correct
- Patterns identified are actually present in code

## Interactions

- [[spec - drift skill - read only analysis of spec vs code divergence]] — architecture snapshots inform drift analysis
- [[spec - eidos - spec driven development loops]] — architecture is a procedural artifact in `memory/`

## Mapping

> [[skills/architecture/architecture.md]]
