---
tldr: Toggleable execution mode — dry-run, verify, run, verify-or-rollback
category: utility
---

# /eidos:faildetect

Wraps script and command execution in a verify-or-rollback loop.
When active, every non-trivial bash execution follows: dry-run → verify → run → verify-or-rollback.

## Usage

```
/eidos:faildetect               # enable for this session
/eidos:faildetect off            # disable for this session
```

## Instructions

### 1. Route by Command

Parse arguments:
- No args or `on` → enable
- `off` → disable

### 2. Enable

Announce the mode change:

```
Faildetect **enabled** — all non-trivial commands will follow the verify-or-rollback loop.
```

From this point forward, follow the **Execution Protocol** below for every bash command that modifies files, runs scripts, or produces meaningful output.
Trivial commands (e.g. `ls`, `pwd`, `date`, `git status`, `git log`, reading files) are exempt.

### 3. Disable

Announce the mode change:

```
Faildetect **disabled** — returning to normal execution.
```

Resume normal command execution without the protocol.

## Execution Protocol

When faildetect is active, wrap each non-trivial command in these steps:

### Step 1: Declare Intent

Before executing, state:
- **Command:** what will be run
- **Expected outcome:** what success looks like (exit code, output patterns, file changes)
- **Rollback strategy:** what to undo on failure (`git checkout -- <files>`, `git reset HEAD~1`, or other)

### Step 2: Dry Run (when possible)

If the command supports a dry-run mode or can be previewed safely:
- Run the dry-run variant (e.g. `--dry-run`, `--check`, `--whatif`, or just `echo` the command)
- Compare output against expected outcome
- If unexpected: **stop**, report the discrepancy, and ask the user before proceeding
- If no dry-run is possible, note this and proceed to Step 3

### Step 3: Execute

Run the actual command.

### Step 4: Verify

Compare actual output against expected outcome:
- **Success:** report briefly and continue
- **Failure:** execute the rollback strategy immediately, then report:
  ```
  **Faildetect rollback:**
  - Command: `<what was run>`
  - Expected: <what should have happened>
  - Actual: <what happened>
  - Rollback: `<what was undone>`
  - Next: <suggested fix or question for user>
  ```

### Rollback Strategies

Choose the lightest rollback that restores the prior state:

1. **File changes only:** `git checkout -- <files>` (restores from last commit)
2. **Committed changes:** `git reset --soft HEAD~1` (uncommit but keep changes staged)
3. **Script with side effects:** report what happened and let the user decide
4. **Nothing to rollback:** some commands (e.g. failed builds) leave no state to undo — just report

### What Counts as Non-Trivial

Apply the protocol to commands that:
- Modify files (writes, edits, moves, deletes)
- Run scripts or build tools
- Install or remove packages
- Execute database operations
- Push, deploy, or release

Skip the protocol for:
- Read-only commands (`cat`, `ls`, `git log`, `git status`, `git diff`)
- Queries and lookups
- Navigation (`cd`, `pwd`)

## Output

- On enable: confirmation message
- On disable: confirmation message
- During execution: intent → dry-run result → execution result → verification
