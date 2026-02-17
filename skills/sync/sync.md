---
tldr: Bidirectional reconciliation of specs and code
category: core
---

# /eidos:sync

Reconcile specs and code bidirectionally — combines drift analysis with push and pull resolution.

## Usage

```
/eidos:sync                      # sync all specs vs all code
/eidos:sync [file or spec ...]   # sync specific files/specs
/eidos:sync recent [N]           # sync recently changed files
```

## Instructions

### 1. Run Drift

Run the drift analysis (same as `/eidos:drift` with matching args) to identify all discrepancies.
Do not create a separate drift report file — the sync report will capture findings.

### 2. Classify Each Discrepancy

For each item drift found, classify:

- **Spec-ahead** — spec describes something code doesn't do → suggest push
- **Code-ahead** — code does something spec doesn't describe → suggest pull
- **Conflict** — spec and code both changed incompatibly → decision needed

### 3. Present for Resolution

Use [[spec - numbered lists - structured selectable output]] format:

```
Sync found N discrepancies:

Spec-ahead (push):
1 - [claim] in [spec] → code doesn't implement this
2 - [claim] in [spec] → code partially implements this

Code-ahead (pull):
3 - [file:pattern] → not described in any spec
4 - [file:behaviour] → spec is missing this

Conflicts:
5 - [spec] says X, [file] does Y → decision needed

Options:
a - Resolve all (push spec-ahead, pull code-ahead, prompt for conflicts)
b - Select items by number
c - Create drift report only, resolve later
```

### 4. Resolve Selected Items

For each selected item:
- **Spec-ahead** → execute push logic (implement code to match spec)
- **Code-ahead** → execute pull logic (update spec to match code)
- **Conflict** → present both sides, ask the human which direction to take

After each resolution, verify the relevant claims.

### 5. Handle Unresolved Conflicts

For conflicts the user defers:
- Create `memory/decision - <timestamp> - <claim>.md` with both options documented
- Link back to the relevant spec

### 6. Report

Create `memory/sync - <timestamp> - <claim>.md` summarising:
- What was synced
- Which direction each item was resolved
- What remains unresolved

Commit.

## Output

- May modify: code files (push direction)
- May modify: spec files in `eidos/` (pull direction)
- May create: `memory/decision - <timestamp> - <claim>.md` for deferred conflicts
- Creates: `memory/sync - <timestamp> - <claim>.md`
