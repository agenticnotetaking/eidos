---
tldr: Collaboratively think through a spec via Q&A before writing it
---

# /eidos:spec

## Target

Writing a good spec requires thinking it through — target, behaviours, edges, interactions.
Jumping straight to writing often produces specs that miss things or need heavy refinement.
This skill front-loads that thinking via structured Q&A, similar to how `/eidos:plan` works for plans.

## Behaviour

- Args: optional topic or name
- Searches for related specs, claims, code, and memory artifacts
- Asks progressive questions: orientation → behaviour → design → interactions
- Skips what the user already covered in their description
- Drafts spec following [[template - spec - sections and conventions for spec files]]
- Presents draft for review, iterates if needed
- Writes to `eidos/` (or `eidos/skills/` for skill specs)
- Commits immediately

## Design

The skill mirrors `/eidos:plan`'s pattern: gather context → ask questions → draft → review → create.

Questions are progressive, not exhaustive.
Start broad (what, why, who), narrow to specifics (edge cases, boundaries, trade-offs).
The user's initial description seeds the conversation — don't re-ask what they already said.

Unlike `/eidos:pull` (which extracts specs from code) or `/eidos:refine` (which processes comments in existing specs), this skill creates specs from scratch through dialogue.

## Interactions

- [[template - spec - sections and conventions for spec files]] — output structure
- [[spec - push skill - implements code to match spec]] — natural follow-up for small/focused specs
- [[spec - plan skill - structured plan for multi step work]] — natural follow-up for large/multi-concern specs that need a plan before implementation
- [[spec - refine skill - processes inline comments via structured dialogue]] — for post-creation refinement
- [[spec - pull skill - reverse engineers spec from existing code]] — alternative when code exists first

## Mapping

> [[skills/spec/spec.md]]
