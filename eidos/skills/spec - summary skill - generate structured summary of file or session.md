---
tldr: Generate structured summary of a file or session with key points and created artifacts
---

# /eidos:summary

## Target

Long files and sessions need condensed overviews.
Summaries capture what matters without requiring a full read.

## Behaviour

- Args: file to summarise
- Reads the file and extracts key points, decisions, and created artifacts
- Creates `memory/summary - <timestamp> - <claim>.md`
- Commits immediately

## Interactions

- [[spec - externalise - persist insights beyond the conversation]] — summaries are a form of externalisation

## Mapping

> [[skills/summary/summary.md]]
