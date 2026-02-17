---
tldr: Route insights into the spec system as new or adjusted specs and claims
category: core
---

# /eidos:toeidos

Take semi-specified text and route it into eidos specs — as a new spec, a new claim, or an adjustment to an existing one.

## Usage

```
/eidos:toeidos [text describing an insight, observation, or requirement]
```

The input can be rough — stream of consciousness, bullet points, half-formed ideas, copy-pasted chat excerpts.

## Instructions

### 1. Parse the Input

Extract the core insight(s) from the rough text.
There may be multiple distinct insights in one input — identify each separately.

### 2. Search Existing Specs

For each insight:
1. Read spec file names in `eidos/` and claim file names
2. Search for overlapping concepts — similar claims, related domains
3. Run `${CLAUDE_PLUGIN_ROOT}/scripts/outline_eidos.py` if needed for structural overview

### 3. Classify Each Insight

- **Strong overlap with existing spec** → propose adjustment (add claim, update section, extend behaviour)
- **Partial overlap** → surface related files, ask whether to extend existing or create new
- **No overlap** → propose new spec or new claim file

For each, determine whether the insight is:
- A **spec** — a distinct concern with target, behaviour, design
- A **claim** — a verifiable statement that deserves its own file (significant, referenced across specs, or pressing)
- An **adjustment** — content that refines or extends an existing file

### 4. Draft

For each insight, prepare:

**New spec:**
```markdown
---
tldr: [brief description]
category: core
---

# [Name]

## Target
[Extracted from insight]

## Behaviour
- [Claims derived from insight]
```

**New claim:**
```markdown
---
tldr: [brief description]
category: core
---

# [Claim as prose]

[Explanation derived from insight]
```

**Adjustment to existing:**
Show the proposed diff — what would be added or changed and where.

### 5. Present for Confirmation

Per [[c - agency in implementation not direction - surface reasoning for human steering]], never auto-create.

If multiple insights:
```
Found N insights in your input:

1 - New spec: "[topic]" → create spec - [name] - [claim].md
2 - Adjust: [existing spec] → add [what] to [section]
3 - New claim: "[statement]" → create c - [claim].md

Proceed with all, select by number, or adjust?
```

If single insight:
```
This looks like [a new spec / an adjustment to X / a new claim].

[show draft or diff]

Create this? (y/adjust/discard)
```

### 6. Execute

For approved items:
1. Create or modify the file(s)
2. Update wiki links — add references from related specs if appropriate
3. Commit

### 7. Summary

```
Routed N insights:
- Created: [[spec - ...]] / [[c - ...]]
- Updated: [[spec - ...]] (added [what])
```

## Output

- Creates or modifies: spec and/or claim files in `eidos/`
