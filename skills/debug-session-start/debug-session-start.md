---
tldr: Print session-start context verbatim for inspection
category: utility
---

# /eidos:debug-session-start

Display the session-start context that was injected into this conversation.

## Usage

```
/eidos:debug-session-start
```

## Instructions

1. Run the session-start hook directly: `bash ${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh`
2. Display the output verbatim in a fenced code block
3. Note any missing or empty sections
