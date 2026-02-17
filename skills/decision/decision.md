---
tldr: Record a significant decision with options, rationale, and consequences
category: planning
---

# /eidos:decision

Record a decision worth preserving — one where alternatives were evaluated and the rationale matters for future context.

## Usage

```
/eidos:decision [topic or question]
```

## Instructions

### 1. Clarify the Decision

If the decision point is unclear or broad, use AskUserQuestion:
- What exactly are we deciding?
- What constraints matter?
- Are there options already in mind?

If the decision is already specific, confirm and proceed.

### 2. Identify Options

For each viable option, capture:
- What it is (brief)
- Trade-offs — what you gain, what you lose
- Implications — what changes downstream

Don't list exhaustively — include options that were genuinely considered.

### 3. Record the Choice

Ask the user which option they chose (or confirm if already decided).
Capture:
- **Chosen:** which option, one-line rationale
- **Rationale:** why this over the others, what tipped the balance

### 4. Note Consequences

What changes as a result:
- Specs to update
- Code to adjust
- Follow-up decisions needed
- Things to watch for

### 5. Create Decision File

Read the template: [[template - decision - options rationale and outcome]]

Create `memory/decision - <timestamp> - <claim>.md` following the template.
Commit immediately.

### 6. Link to Context

If this decision emerged from a plan, add an `=>` note linking to the decision file.
If it affects a spec, note the implication (offer to update the spec).

### 7. Present and Offer Next Steps

Show the chosen option and key rationale (not the full file), then offer:
```
Decision recorded: [[decision - <timestamp> - <claim>]]

Options:
1 - Update affected specs
2 - Continue current work
3 - Done for now
```

## When to Use This vs `=>` Notes

- **`=>` in plans:** lightweight, in-context choices that don't need standalone rationale
- **This skill:** alternatives were evaluated, trade-offs weighed, and the reasoning should survive beyond the current plan

## Output

- Creates: `memory/decision - <timestamp> - <claim>.md`
- Status field: `decided` (can become `revisited` or `superseded`)
