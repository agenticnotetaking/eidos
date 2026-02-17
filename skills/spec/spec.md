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

### 3. Draft the Spec

Read the template: [[template - spec - sections and conventions for spec files]]

Draft the spec from the Q&A.
Only include sections that have substance — don't add empty sections.

Present the full draft for review before writing.

### 4. Revise

If the user wants changes, adjust and re-present.
This may trigger further questions — that's fine, iterate until it's right.

### 5. Create Spec File

Write to `eidos/spec - <name> - <claim>.md`.
If it's a skill spec, write to `eidos/skills/spec - <name> - <claim>.md`.
Commit immediately.

### 6. Offer Next Steps

```
Spec created: [[spec - <name> - <claim>]]

Options:
1 - Implement with /eidos:push
2 - Refine further with /eidos:refine
3 - Done for now
```

## Output

- Creates: spec file in `eidos/` or `eidos/skills/`
