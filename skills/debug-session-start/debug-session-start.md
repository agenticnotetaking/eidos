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

1. Run the session-start hook directly: `bash ${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh all`
   - The hook dispatches per unit (`<kind> <name>`); `all` (also the no-arg default) emits every unit in injection order, exactly as the harness concatenates them. To inspect one unit, pass e.g. `dynamic skills-list` or `core 03-workflow`.
2. Display the output verbatim in a fenced code block
3. Note any missing or empty sections — each unit is a separate hook kept under the ~9K-char budget, so an empty unit is normal when its feature is disabled or its data is absent
