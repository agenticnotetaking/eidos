---
tldr: Read-only analysis of divergence between eidos specs and code
---

# /eidos:drift

## Target

Specs and code drift apart over time.
Before taking action, you need a clear picture of what has diverged and in which direction.
Drift is the diagnostic — it tells you what's different without changing anything.

Drift is vertical: intent (specs) ↔ implementation (code).
For same-level checks (spec vs spec, code vs code), see `/eidos:coherence`.

## Behaviour

- Args: optional file paths or `recent [N]` for scoping
- **Broad mode** (no args): scans all specs, all mappings, all claims — project-wide inventory
- **Focused mode** (with file args): deep per-file analysis against the relevant spec(s)
- Read-only — never modifies code or specs

### Broad Mode

- Reads all eidos specs, extracts claims and mappings
- For each mapping: verifies file exists, extracts key patterns from the code
- For each claim: attempts to verify against mapped code, presents as a checklist
  - Checked claims (code matches spec)
  - Unchecked claims (code diverges or claim can't be verified)
- Runs `orphaned_mappings.py` to find mappings pointing to deleted files
- Runs `future_items.py` to check if `{!}` items are already implemented in code
- Assesses overall drift level (Low / Moderate / Significant)
- Output: `memory/drift - <ts> - <claim>.md` with actionable items
- Suggests specific push or pull actions for each divergence

### Focused Mode

When given specific files, drift goes deeper:
- Finds the relevant eidos spec(s) via mapping search
- Checks code against claims in the spec's Behaviour section
- Checks adherence to design patterns described in the spec's Design section
- Checks interactions — are dependencies and effects handled correctly?
- Highlights where code **exceeds** spec (potential pull candidates)
- If no spec exists for the target code, suggests running pull first
- Output: same `memory/drift - <ts> - <claim>.md` format, scoped to the target files

### Scoping with `recent`

`recent [N]` uses `recent_changes.py` to scope drift to recently changed files:
- Recent spec changes → check if code still matches
- Recent code changes → check if specs still match

### Decision Prompts

When decisions are needed, presents findings via numbered list for user selection.
Each item includes a suggested action (push, pull, or decision needed).

## Design

Drift is read-only — it never modifies code or specs.
It is the foundation that push, pull, and sync build on.

The drift report groups findings by:
1. **Claim verification** — checklist of claims with pass/fail
2. **Design adherence** — do patterns in code match the spec's Design section?
3. **Orphaned mappings** — pointers to files that no longer exist
4. **Code exceeding spec** — behaviours in code that the spec doesn't describe (pull candidates)
5. **Future items already implemented** — `{!}` items where code suggests they're done
6. **Suggested actions** — specific push/pull recommendations
7. **Drift level** — Low / Moderate / Significant

Depth scales with scope: broad mode does surface-level claim matching across many files; focused mode does deep analysis of specific files.

{[?] How deep should claim verification go in broad mode — surface pattern matching or deeper semantic analysis?}
{[?] Should focused mode also check claims from OTHER specs that might be relevant to the target code?}

## Verification

- Running drift on a project with known divergences produces an accurate report
- Orphaned mappings are correctly identified
- Already-implemented future items are flagged
- Focused mode on a specific file finds its spec and checks claims deeply
- Code that exceeds spec is flagged as a pull candidate
- Missing specs are flagged with pull suggestion
- The report is actionable — each item has a clear next step

## Interactions

- [[spec - eidos - spec driven development loops]] — core command in the sync loop
- [[c - open comment discovery - script to find unresolved refinement comments]] — drift surfaces open comments
- Feeds into [[spec - push skill - implements code to match spec]], [[spec - pull skill - reverse engineers spec from existing code]], and [[spec - sync skill - bidirectional reconciliation with conflict surfacing]] as the diagnostic step

## Mapping

> [[skills/drift/drift.md]]
> [[scripts/orphaned_mappings.py]]
> [[scripts/future_items.py]]
> [[scripts/recent_changes.py]]
