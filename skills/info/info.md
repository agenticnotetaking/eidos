---
tldr: Request more context before proceeding
category: utility
---

# /eidos:info

Gather context before proceeding.

## Usage

```
/eidos:info [topic]
```

## Instructions

1. Search for relevant context:
   - Specs in `eidos/` related to the topic
   - Memory files (plans, decisions, research) related to the topic
   - Codebase patterns if the topic is implementation-related
2. Present what was found
3. Identify gaps — what's still unclear
4. Ask the user targeted questions to fill gaps
5. Suggest next steps based on gathered context

## Output

- No files created — purely informational
- Presents gathered context and asks clarifying questions
