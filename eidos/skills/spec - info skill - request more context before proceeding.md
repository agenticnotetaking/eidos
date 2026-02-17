---
tldr: Gather additional context from codebase, specs, or user before proceeding with work
---

# /eidos:info

## Target

Sometimes the AI doesn't have enough context to proceed confidently.
Rather than guessing, info explicitly gathers what's needed.

## Behaviour

- Args: optional topic or question
- Searches eidos specs, memory files, and codebase for relevant context
- Presents what was found and what's still unclear
- Asks the user targeted questions to fill gaps
- Does not create files — purely informational

## Interactions

- [[spec - eidos - spec driven development loops]] — reads specs for context
- [[c - agency in implementation not direction - surface reasoning for human steering]] — info is how the AI avoids guessing

## Mapping

> [[skills/info/info.md]]
