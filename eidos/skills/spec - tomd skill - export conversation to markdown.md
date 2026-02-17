---
tldr: Export the current conversation to a markdown file in memory
---

# /eidos:tomd

## Target

Conversations are ephemeral.
Exporting to markdown preserves the full exchange for later reflection, search, and reference.

## Behaviour

- Creates `memory/session - <timestamp> - <claim>.md`
- Captures the conversation in readable markdown
- Claim derived from the session's main topic
- Commits immediately

## Mapping

> [[skills/tomd/tomd.md]]
