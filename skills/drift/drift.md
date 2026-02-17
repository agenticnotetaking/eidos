---
tldr: Analyse divergence between eidos specs and code
category: core
---

# /eidos:drift

Read-only analysis of gaps between intent (specs) and implementation (code).
Two modes: broad (project-wide inventory) or focused (deep per-file analysis).

Drift is vertical: spec ↔ code.
For same-level checks (spec vs spec, code vs code), use `/eidos:coherence`.

## Usage

```
/eidos:drift                     # broad: all specs vs all code
/eidos:drift [file ...]          # focused: specific files against their specs
/eidos:drift recent [N]          # scope to recently changed files
```

## Instructions

### 1. Determine Mode

- **No args** → broad mode
- **File paths** → focused mode on those files
- **`recent [N]`** → use `recent_changes.py` to find recently changed files, then run focused mode on each

### 2. Gather Context

#### Broad Mode

1. Run `${CLAUDE_PLUGIN_ROOT}/scripts/orphaned_mappings.py` — collect orphaned mapping pointers
2. Read all spec files in `eidos/` — extract claims from Behaviour sections and mappings from Mapping sections
3. For each mapping that points to an existing file: read the code file and check claims against it
4. Run `${CLAUDE_PLUGIN_ROOT}/scripts/future_items.py` — check if any `{[!]}` items are already implemented in code

#### Focused Mode

1. For each target file: search all spec Mapping sections for a `> [[...]]` reference to it
2. If a spec is found: read the full spec (Target, Behaviour, Design, Interactions)
3. If no spec is found: note the file as unmapped — suggest `/eidos:pull` to create one
4. Read the target code file thoroughly

### 3. Analyse

#### Broad Mode — Surface-Level

For each spec with mappings:
- **Claim verification** — does the code appear to uphold each claim? Mark as checked/unchecked
- **Orphaned mappings** — from script output
- **Future items already implemented** — flag `{[!]}` items where code evidence suggests they're done
- **Code exceeding spec** — significant code behaviours not reflected in any spec (only when obvious, not exhaustive)

#### Focused Mode — Deep Analysis

For each target file with a matching spec:
- **Claim verification** — check each Behaviour claim in detail against the code
- **Design adherence** — do patterns in code match what the Design section describes?
- **Interaction checks** — are dependencies and effects from the Interactions section handled?
- **Code exceeding spec** — behaviours in code that the spec doesn't describe (potential pull candidates)

### 4. Compile Report

Create `memory/drift - <timestamp> - <claim>.md`:

```markdown
---
tldr: Drift report — [scope description]
category: core
---

# Drift: [scope description]

## Claim Verification

- [x] Claim text (spec file) — upheld
- [ ] Claim text (spec file) — diverges: [brief explanation]

## Orphaned Mappings

- `> [[path]]` in [spec file] — file not found

## Code Exceeding Spec

- [file:line] does X, but spec doesn't mention this

## Future Items Already Implemented

- {[!]} [description] (spec file) — evidence: [what in code suggests this is done]

## Suggested Actions

1. `/eidos:push [spec]` — [reason]
2. `/eidos:pull [file]` — [reason]
3. Decision needed: [description]
```

### 5. Assess Drift Level

- **Low** — minor discrepancies, mostly documentation updates needed
- **Moderate** — some implementation fixes needed, or intentional pivots not documented
- **Significant** — major divergence between intent and reality, needs discussion

### 6. Present

Commit the drift report.
Present a summary of findings grouped by category.
For items requiring decisions, use [[spec - numbered lists - structured selectable output]] format:

```
Drift complete. Level: [Low/Moderate/Significant]
- M claims verified, K divergent
- X orphaned mappings
- Y code patterns exceeding spec

Actionable items:
1 - Push: [spec] → code diverges on [claim]
2 - Pull: [file] → code exceeds spec
3 - Decision: [description]

Which items to act on?
```

## Output

- Creates: `memory/drift - <timestamp> - <claim>.md`
- Read-only — never modifies code or specs
