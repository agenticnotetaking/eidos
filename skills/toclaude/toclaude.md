---
tldr: Persist behaviour corrections to CLAUDE.md
category: utility
---

# /eidos:toclaude

Update CLAUDE.md or specs to correct undesired behaviour.

## Usage

```
/eidos:toclaude [description of correction]
```

## Instructions

1. Understand the correction — what went wrong, what should happen instead
2. Identify the right location:
   - **`inject/core.md`** — plugin rules that apply to all eidos projects
   - **`inject/feature/*.md`** — rules tied to a config-gated feature
   - **CLAUDE.md** — project-specific rules (not plugin-wide)
   - **Specific spec** — scoped rules that apply to one area
   - **New claim in `eidos/`** — if the correction is a general principle
3. If adding to context files: include an actionable TL;DR inline, not just a link to a spec. Context should be self-sufficient for 90% of work.
4. Draft the addition or modification
5. Present for approval (per [[c - agency in implementation not direction - surface reasoning for human steering]])
6. Write the change and commit

## Output

- Modifies: CLAUDE.md or relevant spec/claim file
