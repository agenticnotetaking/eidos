---
tldr: Work through a structured document point by point, resolving each item
category: planning
---

# /eidos:process

Work through a structured document (coherence report, drift analysis, or any file with numbered findings) item by item — reading context, asking questions, making changes, and updating the source document with resolutions.

Like `/eidos:plan-continue` but for any document with actionable items, not just plans.

## Usage

```
/eidos:process [file path or wiki link]
```

## Instructions

### 1. Load the Document

Read the target file.
If no file is given, search `memory/` for recent unresolved documents (coherence, drift, review, etc.) and present options.

### 2. Identify Actionable Items

Scan for numbered items, sections with **Fix:** markers, or any structured findings that need resolution.
Present an overview:

```
Processing: [[coherence - 2602140242 - spec graph contradictions]]

Items:
1 - Config file path contradiction (Contradictions §1)
2 - Claim file naming prefix (Contradictions §2)
3 - Progressive disclosure vs session context (Contradictions §3)
4 - Main spec missing 4 skills (Missing Cross-References §4)
...

11 total items. Start from the beginning?
```

The user may choose to start at a specific item or skip items.

### 3. Process Each Item

For each item:

1. **Read** — read the relevant files referenced by the item
2. **Present** — show the issue with enough context to decide
3. **Ask** — if the resolution isn't obvious, ask the user what to do (use AskUserQuestion or numbered options)
4. **Act** — make the agreed changes (edit files, update specs, add links)
5. **Commit** — commit the changes immediately
6. **Update source** — mark the item as resolved in the source document with a brief note

### 4. Update the Source Document

After resolving an item, update it in the source file.
Add resolution notes inline — don't delete the original finding:

```markdown
### 1 - Config file path: `eidos/.config` vs `.eidos-config`

...original finding...

**Resolved:** Updated two references in main spec. `abc1234`
```

Commit the source document update.

### 5. Continue Loop

After each item:
```
Resolved: Item 1 — Config file path contradiction

Next: Item 2 — Claim file naming prefix
continue?
```

Wait for confirmation before proceeding.
The user may skip items, reorder, or stop at any point.

### 6. Wrap Up

When all items are processed (or user stops):
```
Processed: [[coherence - 2602140242 - spec graph contradictions]]

Resolved: 8/11 items
Skipped: 2 (items 6, 9)
Deferred: 1 (item 3 — needs broader discussion)

Options:
1 - Continue with skipped items
2 - Done
```

## Output

- Modifies: files referenced by each item (specs, claims, inject snippets, etc.)
- Updates: the source document with resolution notes
- No new file created — the source document becomes the record
