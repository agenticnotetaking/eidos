---
tldr: Discover missing wiki links between specs and prune broken or stale ones
---

# /eidos:weave

## Target

Wiki links form the relationship graph between specs.
This graph is only as useful as it is complete and accurate.
Links get missed when specs are written independently, and go stale when specs are renamed or deleted.
Weave actively maintains the graph — discovering links that should exist and pruning ones that shouldn't.

## Behaviour

- Two modes: **weave** (discover missing links) and **prune** (identify broken/stale links)
- Both modes create a suggestion file in `memory/` before acting
- Suggestions presented via numbered list for user selection
- Only acts on user-approved suggestions

### Weave Mode (default)

- Scans all spec and claim files in `eidos/`
- For each file, analyzes content for concepts that overlap with other specs
- Identifies where wiki links should exist but don't:
  - Shared concepts mentioned in prose but not linked
  - Specs that reference the same domain without cross-referencing
  - Claims relevant to specs that don't cite them
- Creates: `memory/weave - <ts> - suggested links.md`
- Presents suggestions as numbered list

### Prune Mode

- Args: `prune`
- Scans all wiki links in `eidos/`
- Identifies:
  - Broken links — point to files that don't exist
  - Stale links — point to files whose content has diverged from the linking context
  - Redundant links — same target linked multiple times without reason
- Creates: `memory/weave - <ts> - prune suggestions.md`
- Presents suggestions as numbered list

### Acting on Suggestions

After user selects items:
- Weave: adds the wiki link(s) to the appropriate section (usually Interactions or Behaviour)
- Prune: removes or updates the link(s)
- Updates the suggestion file with [[c - arrow prefix marks inline outcomes that emerged during execution|=>]] markers showing what was done

## Design

Weave complements [[spec - coherence skill - checks spec vs spec for contradictions]].
Coherence checks for semantic problems (contradictions, redundancy).
Weave checks for structural problems (missing or broken connections).

The suggestion-file-first pattern ensures:
- Findings are persistent even if the session ends before acting
- The user can review at their own pace
- Multiple sessions can accumulate suggestions

## Verification

- Discovers genuinely useful missing links between related specs
- Correctly identifies broken links to non-existent files
- Suggestion file follows [[spec - numbered lists - structured selectable output]]
- Never adds links without user confirmation

## Interactions

- [[spec - coherence skill - checks spec vs spec for contradictions]] — coherence checks semantics, weave checks structure
- [[spec - eidos - spec driven development loops]] — weave maintains the wiki-link graph
- [[spec - numbered lists - structured selectable output]] — uses the numbered list pattern
- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — link targets follow naming convention
- [[c - arrow prefix marks inline outcomes that emerged during execution]] — acted-upon suggestions use the arrow convention

## Mapping

> [[skills/weave/weave.md]]
