---
tldr: Update CLAUDE.md and linked specs to correct undesired behaviour so it doesn't recur
---

# /eidos:toclaude

## Target

When the AI does something wrong, saying "don't do that" only fixes this session.
Toclaude persists the correction to CLAUDE.md or a linked spec so future sessions follow the same rule.

## Behaviour

- Args: description of the undesired behaviour and desired correction
- Identifies the right place for the rule: CLAUDE.md for broad rules, specific spec for scoped rules
- Drafts the addition or modification
- Presents for approval before writing
- Commits immediately
- If the correction is significant enough, may create a new claim in `eidos/`

## Design

Toclaude is the feedback loop for AI behaviour.
[[c - agency in implementation not direction - surface reasoning for human steering]] — toclaude is how the human steers persistently, not just for one session.

## Interactions

- [[spec - externalise - persist insights beyond the conversation]] — toclaude is externalisation of behaviour corrections
- [[spec - eidos - spec driven development loops]] — corrections may update specs

## Mapping

> [[skills/toclaude/toclaude.md]]
