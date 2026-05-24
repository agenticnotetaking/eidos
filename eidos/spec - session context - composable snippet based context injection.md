---
tldr: Session context is composed from core and feature snippets plus dynamic state, emitted as one config-gated hook per unit so each stays under the harness's per-hook output cap
---

# Session Context — composable snippet-based context injection

## Target

Claude needs rules and orientation at session start.
A monolithic context file mixes always-on rules with optional features and can't adapt to project configuration.
Snippet-based composition lets the session-start hook assemble the right context for each project.

A second constraint shapes the delivery: the harness caps **each hook's output at 10,000 characters**, so the full context cannot ship from a single hook.
Composition must therefore split across multiple hooks, each under budget.

## Behaviour

### Per-unit hooks (one hook per unit, concatenated)

The harness caps **each `SessionStart` hook's output at 10,000 characters** — over-cap output is truncated to a preview and saved to a file — but it also runs **multiple `SessionStart` hook entries and concatenates their outputs**.
Eidos exploits this: rather than one hook emitting the whole ~29,000-char context (which truncates and loses ~90% of it), it registers **one hook entry per unit**, each emitting a single budget-sized piece.
The dispatcher `hooks/session-start.sh <kind> <name>` emits only the requested unit, gated by config where applicable.

Budget target: **9,000 characters per unit** — headroom under the 10K cap for per-hook wrapper text and growth. Enforced at release time (see [[#Release-time budget guard]]).

Units, in injection order:

1. **Recovery preamble** — emitted first, as a backstop. See [[#Surviving harness truncation]].
2. **Core units** (`inject/core/*.md`) — always loaded, no config gate. Core is split into ordered, budget-sized section files; their concatenation is the full core ruleset.
3. **Feature units** (`inject/feature/*.md`) — each emitted by a config-gated hook; nothing is emitted when its key is disabled.
4. **Dynamic units** — computed at runtime from project state (skill list, eidos specs/concepts, future items, recent changes), each its own gated hook.
5. **Session orientation** — computed from git and memory state (recent branches, open todos, open plans, last session, recent memory files).

### Surviving harness truncation

The harness caps each hook output at 10,000 characters: over-cap output is saved to a file and replaced with a ~2KB preview plus a `Full output saved to: <path>` notice.
The full composed eidos context is ~29,000 characters, so emitting it from a single hook truncated it to the intro and silently dropped skill routing, git workflow, naming, and project state.

**Primary fix: stay under budget.**
Splitting the context into one hook per unit, each under the 9,000-char budget, means no unit truncates — the full context is injected and concatenated, with no file-read step and no reliance on the agent acting.

**Backstop: the recovery preamble.**
The first unit emits a short, conditional instruction: *if* the context was truncated, read the harness-persisted full-output file before working.
This is a safety net for projects whose dynamic content outgrows the budget — not the primary mechanism, because a `SessionStart` hook injects passive context and **cannot force the agent to perform a tool call** before its first reply.
(Observed: with only the preamble in place, the agent greeted the user instead of reading the saved file.)
The preamble is phrased conditionally, so where no truncation occurs it is a harmless no-op.

### Feature snippet → config key mapping

Filename hyphens map to config underscores:
- `git-workflow.md` → `git_workflow`
- `status-reporting.md` → `status_reporting`

Adding a new feature-gated snippet requires:
1. Create the snippet file in `inject/feature/`, kept under the 9,000-char budget
2. Add the config key to [[spec - config - toggleable project settings]]
3. Register a `SessionStart` hook entry for the unit in `hooks/hooks.json`

Missing config file or missing key → default to `true` (all features enabled).

### Release-time budget guard

`scripts/check_session_budget.sh`, run as a `scripts/release.sh` preflight, enforces the model:
- every `inject/core/*.md` and `inject/feature/*.md` is under the 9,000-char budget
- every core/feature unit has a matching `SessionStart` hook entry, and no entry is orphaned
- a canary run of the dynamic-section hooks against the eidos repo stays under budget (catches skill-list / spec-list growth)

The release aborts on any violation, so an over-budget unit can never ship and silently truncate in a user's session.

### CLAUDE.md role

CLAUDE.md is loaded by Claude Code from the project root (the consuming project).
It contains project-specific instructions, not plugin rules.
Plugin rules live in `inject/` and are injected by the session-start hook.

For the bootstrapping case (eidos building eidos), CLAUDE.md has eidos-specific project notes.
For consumer projects, CLAUDE.md has their own project instructions.

## Design

The plugin's context is not a single document — it's a composed output.
This mirrors how the config spec works: features are toggleable, and the context reflects what's enabled.

Core rules are split into ordered section files under `inject/core/` rather than one file: the combined ruleset exceeds the per-hook output cap, so it must span multiple budget-sized hooks.
The split is mechanical (driven by the cap), not by toggling — core units have no config gate and are always loaded together.

Feature snippets are separate files because each maps to a config key and may be independently disabled.

Dynamic context (skill list, specs, future items, branches) stays as hook logic rather than snippets because it's computed from project state at runtime.

Every unit is delivered by its own hook entry so that each stays under the 10K-char cap independently; the harness concatenates them back into one context block.

## Verification

- No config file → all units loaded (same as pre-snippet behaviour)
- Fresh session injects the full context with **no "Output too large" truncation notice**
- Every hook unit's output is under the 9,000-char budget (enforced by `scripts/check_session_budget.sh`)
- Concatenation of `inject/core/*.md` equals the pre-split core ruleset — no rule lost
- Recovery preamble is the first unit and survives even if a later unit truncates
- Setting a feature to `false` → its hook emits nothing
- CLAUDE.md is not injected by the hook (Claude Code loads it from project root)
- PreToolUse branch-check hook respects `git_workflow` config

## Interactions

- [[spec - config - toggleable project settings]] — config keys gate feature snippets
- [[spec - eidos - spec driven development loops]] — context composition is part of plugin structure
- [[spec - git workflow - branch per task with atomic commits]] — first feature-gated snippet
- [[spec - progressive disclosure - surface summaries before reading full files]] — the injected specs/concepts index is an instance of progressive disclosure

## Mapping

> [[inject/core/01-principles.md]]
> [[inject/core/02-conventions.md]]
> [[inject/core/03-workflow.md]]
> [[inject/feature/git-workflow.md]]
> [[inject/feature/status-reporting.md]]
> [[inject/feature/observation-images.md]]
> [[inject/feature/context-tracking-max.md]]
> [[inject/feature/ping-macos.md]]
> [[scripts/read_config.sh]]
> [[scripts/check_session_budget.sh]]
> [[hooks/session-start.sh]]
> [[hooks/hooks.json]]
> [[hooks/pre-tool-use-branch-check.sh]]
