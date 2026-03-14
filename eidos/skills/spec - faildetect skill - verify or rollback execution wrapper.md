---
tldr: Skill spec for /eidos:faildetect — toggleable mode that wraps execution in dry-run, verify, and rollback steps
---

# Faildetect Skill — verify-or-rollback execution wrapper

## Target

Make autonomous and semi-autonomous script execution safer by requiring explicit intent declaration, expected-outcome verification, and automatic rollback on failure.
Particularly useful during agent work, plan execution, and unfamiliar codebases where commands might have unexpected effects.

## Behaviour

### Activation

- `/eidos:faildetect` — enable for the session (behavioural modifier, not a one-shot action)
- `/eidos:faildetect off` — disable, return to normal execution

### Execution Protocol (when active)

Every non-trivial command follows four steps:

1. **Declare intent** — state the command, expected outcome, and rollback strategy
2. **Dry run** — preview the command if possible; stop on unexpected output
3. **Execute** — run the actual command
4. **Verify** — compare output to expected; rollback immediately on failure

### Scope

- **Applies to:** file modifications, scripts, builds, installs, deploys, database operations
- **Exempt:** read-only commands, queries, navigation

### Rollback

Lightest touch that restores prior state:
- `git checkout -- <files>` for uncommitted file changes
- `git reset --soft HEAD~1` for committed changes
- User escalation for side-effectful operations (deploys, API calls)

## Design

Faildetect is a **behavioural modifier**, not a pipeline tool.
It doesn't wrap commands programmatically — it changes how the agent *thinks about* execution.
The protocol is a checklist enforced by the skill's instructions, not a script.

This means:
- No hook scripts or shell wrappers needed
- Works with any command, not just git
- The agent uses judgement for what counts as "non-trivial"
- Dry-run feasibility is assessed per-command (some commands have `--dry-run`, others don't)

### Why Not a Hook?

Hooks fire on every command indiscriminately.
Faildetect needs judgement: is this command worth the overhead?
A behavioural modifier gives the agent discretion while the protocol gives structure.

## Verification

- `/eidos:faildetect` → announces enabled, subsequent commands show intent/verify steps
- `/eidos:faildetect off` → announces disabled, commands return to normal
- Failed command → rollback executed, structured report shown
- Read-only command while active → no protocol overhead
- Dry-run catches issue → execution stops, user asked before proceeding

## Friction

- Overhead: adds steps to every non-trivial command — may slow down confident work
- Judgement calls: "non-trivial" is subjective, may over- or under-apply
- Dry-run gaps: many commands have no dry-run mode, reducing Step 2's value

## Interactions

- [[spec - git workflow - branch per task with atomic commits]] — rollback strategies rely on git state
- [[spec - planning - structured intent between spec and code]] — plan execution benefits most from faildetect
- [[spec - worktree - parallel task work via linked worktrees]] — worktree isolation reduces rollback blast radius

## Mapping

> [[skills/faildetect/faildetect.md]]

## Future

{[?] Hook-level opt-in: a session-start hook that auto-enables faildetect for certain contexts (e.g. agent runs)}
{[?] Structured failure log: persist failed commands and rollbacks to `memory/` for post-session review}
