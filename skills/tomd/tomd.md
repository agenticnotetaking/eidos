---
tldr: Export conversation to markdown
category: utility
---

# /eidos:tomd

Export the current conversation to markdown.

## Usage

```
/eidos:tomd [optional claim]
```

## Instructions

1. If no claim provided, derive one from the session's main topic
2. Create `memory/session - <timestamp> - <claim>.md`
3. Format the conversation as readable markdown:
   - Preserve human/assistant turns
   - Include code blocks
   - Omit tool call details (keep results if informative)
4. Commit immediately

## Output

- Creates: `memory/session - <timestamp> - <claim>.md`
