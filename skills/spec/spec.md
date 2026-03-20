---
tldr: Think through and create a spec via structured Q&A
category: core
---

# /eidos:spec

Think through a spec collaboratively before writing it.
Asks questions to clarify target, behaviour, and design, then produces the spec file.

## Usage

```
/eidos:spec [topic or name]
```

## Instructions

### 1. Gather Context

Search for related artifacts:
- Existing specs in `eidos/` that touch the same domain
- Claims or concepts that relate
- Code that already implements parts of this (check Mapping sections)
- Prior research, decisions, or plans in `memory/`

If found, note them — they inform the questions and shape Interactions.

### 2. Clarify the Spec

Use AskUserQuestion to think through the spec iteratively.

Start with orientation:
- What is this spec about?
- What problem or goal does it target?
- Who or what is affected?

Then drill into behaviour:
- What are the key behaviours or claims?
- What happens in edge cases?
- What should explicitly NOT happen? (boundaries)

Then design if relevant:
- Are there architectural choices to make?
- What patterns should it follow?
- Any constraints from existing code or specs?

Follow up as needed on:
- **Interactions** — what does this depend on, what does it affect?
- **Verification** — how would you know this works?
- **Friction** — known trade-offs or rough edges?

Don't ask everything at once — build understanding progressively.
Skip questions the user already answered in their initial description.

### 3. Create Spec File

Read the template: [[template - spec - sections and conventions for spec files]]

Draft the spec from the Q&A.
Only include sections that have substance — don't add empty sections.

Write directly to `eidos/spec - <name> - <claim>.md`.
If it's a skill spec, write to `eidos/skills/spec - <name> - <claim>.md`.
Don't present a draft first — the user sees the diff and can request changes.
Commit immediately.

### 4. Offer Next Steps

Choose which options to present based on the spec's scope:

- **Small/focused spec** (single concern, clear implementation) → offer `/eidos:push`
- **Large/multi-concern spec** (new feature, multiple files, architectural) → offer `/eidos:plan` — implementation at this scale needs a plan, not a direct push
- Always offer `/eidos:refine` if there are open questions or `{{comments}}`

```
Spec created: [[spec - <name> - <claim>]]

Options:
1 - Plan implementation with /eidos:plan
2 - Implement directly with /eidos:push
3 - Refine further with /eidos:refine
4 - Done for now
```

## Output

- Creates: spec file in `eidos/` or `eidos/skills/`
