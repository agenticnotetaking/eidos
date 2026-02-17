---
tldr: Discover missing wiki links between specs and prune broken or stale ones
category: core
---

# /eidos:weave

Maintain the wiki-link graph — discover links that should exist and prune ones that shouldn't.
Drift checks spec vs code.
Coherence checks spec vs spec semantics.
Weave checks spec vs spec structure (the links themselves).

## Usage

```
/eidos:weave                     # weave mode: discover missing links
/eidos:weave prune               # prune mode: find broken/stale/redundant links
```

## Instructions

### 1. Determine Mode

- **No args or `weave`** → weave mode (discover missing links)
- **`prune`** → prune mode (identify broken/stale/redundant links)

### 2. Gather All Specs

Read all `*.md` files in `eidos/` (including subdirectories like `eidos/skills/`).
For each, extract:
- Filename (the claim it makes)
- Content topics and domain concepts
- All existing `[[wiki links]]`
- Behaviour claims
- Interaction declarations

### 3a. Weave Mode — Discover Missing Links

For each file, analyse content for concepts that overlap with other specs:
- **Shared concepts** — prose mentions a topic that another spec is about, but doesn't link to it
- **Overlapping domains** — two specs reference the same domain without cross-referencing
- **Uncited claims** — a claim is relevant to a spec that doesn't cite it
- **Missing Interaction entries** — specs that depend on or complement each other but lack Interactions links

Focus on genuinely useful links — not every keyword match warrants a link.
Prioritise links that would help a reader navigate the spec graph.

### 3b. Prune Mode — Identify Problem Links

Scan all `[[wiki links]]` in `eidos/`:
- **Broken links** — point to files that don't exist (resolve relative to `eidos/` and project root)
- **Stale links** — point to files whose content has diverged enough that the linking context no longer applies
- **Redundant links** — same target linked multiple times in the same file without reason

### 4. Create Suggestion File

Write findings to `memory/` before acting:
- Weave mode: `memory/weave - <timestamp> - suggested links.md`
- Prune mode: `memory/weave - <timestamp> - prune suggestions.md`

Use compact timestamp format (`yymmddhhmm`).

Format the file using [[spec - numbered lists - structured selectable output]]:

```markdown
---
tldr: Weave suggestions — [N] potential links discovered
category: core
---

# Weave: suggested links

1 - [Domain/Category]
  - 1.1 - [[spec A]] → [[spec B]] — [reason they should link]
  - 1.2 - [[spec C]] → [[claim D]] — [reason]
2 - [Another Domain]
  - 2.1 - [[spec E]] → [[spec F]] — [reason]
```

For prune mode:

```markdown
---
tldr: Prune suggestions — [N] problem links found
category: core
---

# Weave: prune suggestions

1 - Broken Links
  - 1.1 - [[target]] in [spec file] — file not found
2 - Stale Links
  - 2.1 - [[target]] in [spec file] — context has diverged: [brief reason]
3 - Redundant Links
  - 3.1 - [[target]] linked N times in [spec file]
```

### 5. Present and Prompt

Commit the suggestion file.
Display the numbered list and prompt:

```
Which items to act on? (e.g., "1.1, 2.3")
```

Never act without user confirmation.

### 6. Act on Selections

For each user-selected item:

**Weave selections:**
- Add the wiki link to the appropriate section (usually Interactions, sometimes Behaviour)
- If the link should be bidirectional, add it in both specs

**Prune selections:**
- Broken links → remove the link or suggest creating the target
- Stale links → remove or update the link text
- Redundant links → remove duplicates, keep the most contextually appropriate one

### 7. Update Suggestion File

After acting, update the suggestion file with [[c - arrow prefix marks inline outcomes that emerged during execution|=>]] markers:

```markdown
  - 1.1 - [[spec A]] → [[spec B]] — shared auth domain
    - => added to spec A Interactions section
    - => added to spec B Interactions section
```

Commit the updates.

## Output

- Creates: `memory/weave - <timestamp> - suggested links.md` or `memory/weave - <timestamp> - prune suggestions.md`
- May modify: spec files (only after user approval)
