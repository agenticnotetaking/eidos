---
tldr: Bidirectional reconciliation of specs and code with conflict surfacing
---

# /eidos:sync

## Target

Push and pull are one-directional. When both spec and code have changed independently, you need to reconcile both directions at once. Sync is the combination of push and pull with conflict detection — where drift is the read-only analysis, sync is the action.

## Behaviour

- Reads all specs + mapped code
- Classifies each discrepancy:
  - **Spec-ahead:** spec describes something code doesn't do → suggest push
  - **Code-ahead:** code does something spec doesn't describe → suggest pull
  - **Conflict:** incompatible differences → decision prompt (neither auto-wins)
- Presents findings as numbered list, user selects items to resolve
- For each selected item: executes the appropriate push or pull
- Conflicts that can't be auto-resolved create decision files in `memory/`

## Design

Sync builds on drift's analysis but adds resolution. Think of it as: drift tells you what's wrong, sync helps you fix it.

The numbered list presentation lets the user:
- Resolve all items at once
- Cherry-pick specific items
- Defer items for later
- Override the suggested direction (e.g., choose push when sync suggests pull)

{[?] Should sync support `recent [N]` scoping like push and pull?}
{[?] What's the right granularity for conflict detection — per-claim, per-file, per-section?}

## Verification

- Sync correctly classifies spec-ahead, code-ahead, and conflict
- User can selectively resolve items
- Resolved items result in correct push or pull operations
- Unresolved conflicts become decision files

## Interactions

- Combines [[spec - push skill - implements code to match spec]] and [[spec - pull skill - reverse engineers spec from existing code]] in one pass
- Uses [[spec - drift skill - read only analysis of spec vs code divergence]]'s analysis as foundation
- [[spec - eidos - spec driven development loops]] — core command in the sync loop

## Mapping

> [[skills/sync/sync.md]]
