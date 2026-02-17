---
tldr: Create a new eidos skill from patterns discovered in conversation
---

# /eidos:toskill

## Target

Reusable patterns emerge during work.
When a workflow is repeated or a useful procedure is discovered, it should become a skill.

## Behaviour

- Args: skill name or description
- Extracts the pattern from conversation
- Creates skill directory: `skills/<name>/`
- Creates skill file: `skills/<name>/<name>.md`
- Creates SKILL.md symlink
- Optionally creates spec in `eidos/skills/`
- Commits all files

## Mapping

> [[skills/toskill/toskill.md]]
