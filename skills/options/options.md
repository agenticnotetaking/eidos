---
tldr: Present structured options using numbered lists
category: utility
---

# /eidos:options

Present choices for user decision.

## Usage

```
/eidos:options [context]
```

## Instructions

1. Analyse the situation — what are the distinct options?
2. For each option, identify trade-offs and implications
3. Present using [[spec - numbered lists - structured selectable output]] format:

```
1 - Option A
  - Trade-off: ...
  - Implication: ...
2 - Option B
  - Trade-off: ...
  - Implication: ...

Which approach?
```

4. Wait for user selection before proceeding

## Output

- No files created — presents options inline
- Acts on user selection
