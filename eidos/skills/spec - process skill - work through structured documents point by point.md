---
tldr: Work through a structured document item by item — read context, ask, act, update, repeat
---

# /eidos:process

## Target

Skills like coherence, drift, and code-review produce documents with numbered findings.
Each finding needs investigation and resolution, but there's no systematic way to work through them — the user has to manually shepherd each item.
This skill is that systematic way.

## Behaviour

- Args: file path or wiki link to a structured document
- If no file given, searches `memory/` for recent unresolved documents (coherence, drift, review, etc.)
- Scans for actionable items (numbered sections, **Fix:** markers, findings)
- Presents an overview with item count
- Processes each item sequentially: read → present → ask → act → commit → update source
- Marks resolved items inline in the source document
- User can skip, reorder, or stop at any point
- Shows progress summary on completion or early exit

## Design

Process is the resolution loop.
It turns static findings into worked-through outcomes, with the source document becoming the record.

The key difference from plan-continue: plans are forward-looking (actions to take), process is reactive (findings to resolve).
Plans create their own structure; process works with whatever structure the document already has.

### Flow

1. **Load** — read the target document
2. **Scan** — identify actionable items and present overview
3. **Loop** — for each item:
   - Read referenced files
   - Present the issue with context
   - Ask if resolution isn't obvious
   - Make changes
   - Commit
   - Update source with resolution note
   - Present next item, wait for confirmation
4. **Wrap up** — show resolved/skipped/deferred counts, offer to continue skipped items

### Resolution Format

Items are updated in-place with a **Resolved:** note:

```markdown
### 1 - Config file path contradiction

...original finding...

**Resolved:** Updated references in main spec. `abc1234`
```

The original finding is preserved — the resolution is additive.

## Verification

- Correctly identifies numbered/structured items in various document formats
- Reads referenced files before presenting each item
- Waits for user confirmation between items
- Updates source document after each resolution
- Commits changes atomically (fix + source update)

## Interactions

- [[spec - coherence skill - checks spec vs spec for contradictions]] — primary input type
- [[spec - drift skill - read only analysis of spec vs code divergence]] — another input type
- [[spec - code-review skill - general quality and security analysis]] — another input type
- [[spec - plan-continue skill - resume work on existing plan]] — sibling pattern for plans

## Mapping

> [[skills/process/process.md]]
