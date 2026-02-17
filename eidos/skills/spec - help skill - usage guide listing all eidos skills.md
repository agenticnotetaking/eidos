---
tldr: Usage guide listing all eidos skills with descriptions
---

# /eidos:help

## Target

Users need a quick overview of what eidos can do and how to use it. This skill is the entry point for discovery.

## Behaviour

- Lists all available `/eidos:*` skills with their tldr descriptions
- Groups skills logically: core loop, planning, observation, utility
- Shows argument patterns where applicable
- Works without any eidos/ folder present (useful for first-time setup)
- Reads skill files from the plugin's `skills/` directory, extracts `tldr` from frontmatter

## Design

{[?] Should it also show script usage? Or keep that internal?}

## Mapping

> [[skills/help/help.md]]
