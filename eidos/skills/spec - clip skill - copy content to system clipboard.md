---
tldr: Cross-platform clipboard copy via shell — minimal skill, no file output
---

# /eidos:clip

## Target

The user sometimes needs generated content (commands, snippets, paths) on the clipboard for pasting elsewhere.
Rather than selecting and copying from terminal output, this skill pipes it directly.

## Behaviour

- Determines what to copy from user request or recent context
- Detects platform and uses the appropriate clipboard command (pbcopy, xclip, wl-copy, clip.exe)
- Confirms briefly

## Design

Minimal skill — no file creation, no ceremony.
Platform detection uses `uname` / environment checks.

## Mapping

> [[skills/clip/clip.md]]
