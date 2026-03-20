---
tldr: Recursive research creates a file per area with wiki-linked nesting — same budget system as research-deep but distributed across files
---

# /eidos:research-recursive

## Target

Some research topics are broad enough that cramming everything into one file makes it unwieldy.
Each area deserves its own space — its own research plan, sources, findings, and threads.
And threads that warrant deeper exploration should become their own files, not just subsections.

Research-recursive is research-deep distributed across files.
The root file is the map; area files are the territory.

## Behaviour

- Args: topic description or domain to explore; `continue` to resume
- Two modes: start (new research) and continue (resume existing)
- Creates a root file with the question, area outline, synthesis, and implications
- Each area gets its own file: `memory/research-recursive - <timestamp> - <area claim>.md`
- Area files have `parent` frontmatter linking back to the root (or parent area)
- Threads in an area can spawn nested area files — creating a wiki-linked tree
- Budget is global — tracked in the root file, shared across all area files regardless of depth
- Budget system: same as research-deep — soft, hard, or none. Each area file costs 1 unit.
- Progressive externalisation — each area file committed as it completes
- Cross-area synthesis written in the root file after all areas are explored

## Design

### File Tree Structure

```
research-recursive - 2603201500 - type systems landscape.md          (root)
research-recursive - 2603201501 - static vs dynamic typing.md        (area 1)
research-recursive - 2603201502 - gradual typing.md                  (area 2)
research-recursive - 2603201510 - typescript type narrowing.md       (area 2 sub-area)
research-recursive - 2603201503 - dependent types.md                 (area 3)
```

The tree structure is in the wiki links, not the filenames.
Each file has `parent` in frontmatter pointing to its parent.
The root file lists all top-level areas; area files list their sub-areas in Threads.

### Root vs Area Files

**Root file:** question, area outline (as wiki links with checkboxes), trajectory adjustments, synthesis, implications.
The root is small — it's an index and synthesis surface, not a research document.

**Area files:** research plan, sources, findings, threads.
Each area is a self-contained research cycle.
A reader can open one area and understand it without the root.

### Relationship to Research-Deep

Research-deep puts everything in one file with flat decimal-numbered areas.
Research-recursive distributes areas across files with wiki-linked nesting.

Same budget system, same progressive externalisation, same synthesis-at-the-end pattern.
The difference is structural: one document vs. a tree of documents.

Choose research-deep when: areas are small, the topic fits in one file, you want a single artifact.
Choose research-recursive when: areas are substantial, the topic branches, you want navigable structure.

## Verification

- Root file is a clean index — mostly links and synthesis
- Each area file stands alone — has its own research plan, sources, findings
- Wiki links between files are valid — `parent` frontmatter points correctly
- Budget spent in root matches count of completed area files
- Synthesis in root draws conclusions across areas, not summaries of each
- Nested branching happened where threads warranted it, not gratuitously

## Interactions

- [[spec - research-deep skill - recursive area exploration with progressive synthesis]] — same concept, single-file variant
- [[spec - research skill - investigate and document findings with sources]] — each area is effectively a focused research cycle
- [[spec - template - basis for output files]] — no dedicated template; root and area file structures defined in the skill
- [[spec - externalise - persist insights beyond the conversation]] — progressive externalisation across multiple files

## Mapping

> [[skills/research-recursive/research-recursive.md]]
