---
tldr: Implement or update code to match eidos spec
category: core
---

# /eidos:push

Implement or update code to match what the spec describes (Platonic direction: spec → code).

## Usage

```
/eidos:push [spec ...]           # push specific spec(s) to code
/eidos:push recent [N]           # push recently changed specs
/eidos:push recursive [target]   # force multi-pass mode: collect changes, then plan for subsections
```

## Instructions

### 1. Identify Target Specs

- **Spec paths** → use those specs directly
- **`recent [N]`** → run `${CLAUDE_PLUGIN_ROOT}/scripts/recent_changes.py --commits N`, use the eidos/ files
- If no args, ask the user what to push

### 2. Read the Spec(s)

For each target spec, read thoroughly:
- **Target** — what it's trying to achieve
- **Behaviour** — the claims that must be upheld in code
- **Design** — the patterns and architecture to follow
- **Mapping** — existing code entry points

### 3. Collect Spec Changes

Compare what the spec says against the current code state.
Produce a **push doc** — `memory/push - <timestamp> - <claim>.md` — that lists:

- Each claim or design element that needs implementation or updating
- The current code state for each (exists/missing/diverged)
- Grouped by logical concern, not per-spec

Skip the push doc only for very small pushes (single claim, obvious change).

### 4. Assess Scope

Based on the push doc (or direct reading for small pushes), classify:

- **Small change** (single claim, few lines) → implement directly
- **Medium change** (multiple claims, single concern) → implement with claim-by-claim verification
- **Large change** (new feature, multiple files, multiple concerns) → create a plan

**Triggers for multi-pass mode** (any of these):
- `recursive` argument was used
- Multiple unrelated concerns need implementation
- The scope would require too many changes to track in one pass
- The scope is well defined but still too complex to push in a single session

**If multi-pass triggers:**

1. The push doc becomes the working inventory of what needs to happen
2. **Create a plan** via `/eidos:plan` using [[template - plan - structured phases with actions and progress tracking]]
   - File: `memory/plan - <timestamp> - push subsections for <claim>.md`
   - One action per concern/subsection, each a focused push
   - Reference the push doc for the change list
   - Present the plan to the user for approval
   - Work proceeds via `/eidos:plan-continue`
3. **Stop here** — the push doc and plan are the output. Don't implement in this pass.

**If scope is manageable:** continue to step 5.

Present the scope assessment to the user before proceeding.

### 5. Implement

For small/medium changes:
1. Make the code changes to match the spec's claims
2. Follow the patterns described in the spec's Design section
3. Respect interactions described in the spec

For each change, briefly explain which claim or design element it implements.

### 6. Verify Claims

After implementation, verify each Behaviour claim as a checklist:

```
Claim verification:
- [x] Claim A — implemented in [file:line]
- [x] Claim B — implemented in [file:line]
- [ ] Claim C — could not verify: [reason]
```

Present any claims that couldn't be verified for user decision.

### 7. Update Spec Mapping

If new code files were created during implementation:
- Add them to the spec's Mapping section
- Commit the spec update alongside the code changes

### 8. Commit

Commit code changes with a message referencing the spec:
- `implement [claim summary] per [spec name]`

## Output

**Single-pass mode:**
- Modifies: code files referenced in spec Mapping (or new files)
- May modify: spec Mapping section (if new files created)

**Multi-pass mode (recursive):**
- Push doc: `memory/push - <timestamp> - <claim>.md`
- Plan for subsections: `memory/plan - <timestamp> - push subsections for <claim>.md`
- Implementation proceeds later via `/eidos:plan-continue`
