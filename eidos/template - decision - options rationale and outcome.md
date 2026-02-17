---
tldr: Template for decision files — options considered, trade-offs, chosen option, and rationale
---

# Decision Template

Output path: `memory/decision - <timestamp> - <claim>.md`

```markdown
---
tldr: Brief description of the decision
status: decided
---

# Decision: [Brief description]

## Context

What prompted this decision.
Link to relevant specs, plans, or discussions.

## Options

### A - [Name]

- Trade-offs
- Implications

### B - [Name]

- Trade-offs
- Implications

## Chosen

**[A/B/...]** — [one-line rationale]

## Rationale

Why this option over the others.
What tipped the balance.

## Consequences

What changes as a result.
What to watch for.
```

## Field Reference

**Frontmatter:**
- `status` — `decided`, `revisited`, `superseded`

**Options:**
- Each option gets a named subsection
- Include trade-offs and implications, not just descriptions
- Keep it brief — enough to reconstruct the reasoning, not a dissertation

**Chosen + Rationale:**
- Chosen is the quick answer (scannable)
- Rationale is the longer explanation (for future context)
- These are separate because sometimes you just need to know the outcome, not the reasoning

**Consequences:**
- What changed or will change as a result
- Specs to update, code to adjust, follow-up decisions needed
