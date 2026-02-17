---
tldr: Extract code blocks from conversation and save as executable script files
---

# /eidos:toscript

## Target

Code written in conversation needs to become actual files.
Toscript extracts code blocks and writes them as scripts.

## Behaviour

- Args: optional filename or language filter
- Scans conversation for code blocks
- If multiple blocks: presents for selection or concatenates by language
- Writes to specified path or suggests a sensible default
- Commits immediately

## Mapping

> [[skills/toscript/toscript.md]]
