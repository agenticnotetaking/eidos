---
tldr: Export code to script file
category: utility
---

# /eidos:toscript

Extract code from conversation into script files.

## Usage

```
/eidos:toscript [filename]
```

## Instructions

1. Scan conversation for code blocks
2. If multiple blocks with different languages, ask which to export
3. If filename provided, write there; otherwise suggest a sensible default
4. Commit immediately

## Output

- Creates: script file at specified or suggested path
