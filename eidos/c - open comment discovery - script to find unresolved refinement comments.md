---
tldr: Standalone Python script that finds unresolved double curly brace comments across eidos files
---

# Open comment discovery — script to find unresolved refinement comments

## Target

`{{comments}}` left in spec files are temporary — they signal that something needs attention. But they're easy to forget. A script surfaces all unresolved comments so they can be processed via `/eidos:refine` or resolved manually.

## Behaviour

- Scans `.md` files recursively across one or more directories (default: `eidos/`)
- Finds all `{{ ... }}` patterns that haven't been resolved
- Skips `\{{` (backslash-escaped) — used when referencing the syntax without leaving a real comment
- Groups by file, with line numbers and preview text
- Output is usable both standalone and by `/eidos:next`
- `memory/` is not scanned — those are historical records, not active comments

## Design

Standalone Python script: `scripts/open_comments.py`

```
Usage: open_comments.py [--path DIR ...] [--format text|json] [--cap N]
```

- Default path: `eidos/`
- Accepts multiple `--path` arguments: `--path eidos/ skills/`
- `--cap N` limits output to N entries, then prints `"X more in Y files"`
- File paths in output are relative to CWD
- Handles multiline comments (opening `{{` and closing `}}` on different lines)
- Handles the `{{*` collision-avoidance prefix (still counts as an open comment)
- Ignores `\{{` (backslash escape) — for documentation that references the pattern
- Ignores comments inside fenced code blocks (triple backtick)
- Ignores comments inside inline code (backtick pairs)

## Interactions

- [[c - spec refine loop uses double curly braces - creates refinement traces and adjusts spec]] — the process that resolves these comments
- [[spec - eidos - spec driven development loops]] — linked as a script in the main spec
- `/eidos:next` calls this script to surface open comments as actionable items