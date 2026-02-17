---
tldr: Implement or update code to match eidos specs (Platonic direction)
---

# /eidos:push

## Target

The spec describes what should be. Push makes it real — implementing or updating code to match what the spec says. This is the core Platonic direction: ideal form manifesting as code.

## Behaviour

- Args: specific eidos files, query, `recent [N]`, `recursive [target]`
- Reads target spec(s): Target, Behaviour, Design
- Checks current code via Mappings
- For small changes: implements code directly
- For medium changes: collects spec changes in a push doc (`memory/push - <timestamp> - <claim>.md`), then implements
- For larger changes or `recursive`: collects changes in a push doc, then creates a plan for subsection pushes
- After implementation: verifies claims as checklist
- Updates spec Mapping if new files were created
- The `recent [N]` argument uses `recent_changes.py` to find recently changed eidos files as push targets

## Design

Push is the Platonic direction: making the ideal real.

The `recent` argument supports the organic workflow: you edited a spec, committed it, now push that change to code. `recent 1` is the most common case — push the most recent spec change.

### Push doc and scope escalation

Before implementing, push collects what needs to change into a push doc — a manifest of claims vs current code state.
This serves two purposes: it's a pre-implementation checklist for small/medium pushes, and the working inventory for multi-pass mode.

When the scope is too broad (many claims across unrelated concerns, `recursive` argument, or too complex for one session), push creates a plan for subsection pushes instead of implementing directly.
The plan follows [[template - plan - structured phases with actions and progress tracking]] and work continues via `/eidos:plan-continue`.

### Scope-aware implementation

Push should be smart about scope:
- If a single claim changed, only touch the code relevant to that claim
- If the full spec changed, do a broader implementation pass
- Always verify all claims after pushing, not just the changed ones

{[?] Should push auto-commit code changes, or stage them for user review?}
{[?] How should push handle specs with no existing mapped code — scaffold new files?}

## Verification

- Pushing from a clear spec produces correct code changes
- Claim verification checklist after push is accurate
- Mapping is updated when new files are created
- `recent` argument correctly scopes to recently changed specs
- `recursive` argument triggers multi-pass mode: push doc + plan for subsection pushes
- Auto-detected broad scope triggers the same escalation without explicit `recursive`
- Push doc accurately lists claims vs current code state

## Interactions

- Inverse of [[spec - pull skill - reverse engineers spec from existing code]]
- [[spec - drift skill - read only analysis of spec vs code divergence]] often precedes push — drift identifies what needs pushing
- [[spec - sync skill - bidirectional reconciliation with conflict surfacing]] combines push and pull in one pass

## Mapping

> [[skills/push/push.md]]
> [[scripts/recent_changes.py]]
