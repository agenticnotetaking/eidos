---
tldr: Template for spec files — the standard sections and conventions for eidos specs
---

# Spec Template

Output path: `eidos/spec - <name> - <claim>.md`

```markdown
---
tldr: One-sentence description of what this spec covers
---

# [Name]

[Optional opening paragraph — brief orientation if the title and tldr aren't enough.]

## Target

What problem this targets or what goal it serves.
Not every spec has a clear "problem" — sometimes it exists for aesthetics, convention, or other reasons.
Target covers both.

## Behaviour

How it behaves.
Claims as bullet points, with wiki links for significant ones:
- When X happens, Y follows
- [[claim name]] — for claims that graduated to their own file
- Nested bullets for detail:
  - Sub-behaviour A
  - Sub-behaviour B

## Design

How it works — patterns, architecture, structure.
Use subsections freely.
Omit if behaviour is self-explanatory.

## Verification

How to verify this works.
Test scenarios, manual checks, acceptance criteria.

## Friction

Known pain points, rough edges, tradeoffs.
Omit if none are known yet.

## Interactions

How this relates to other specs or artifacts.
- Depends on [[other spec]]
- Affects [[another spec]]

## Mapping

> [[src/path/to/file.ext]]
> [[src/path/to/other.ext]]

Wiki links in blockquotes.
Entry points into the implementation, not an exhaustive index.

## Decisions

- [[decision - YYMMDDHHMM - brief description]]

## Future

{[!] planned item — will be implemented}
{[?] aspirational item — worth investigating}

## Notes

Anything else — context, gotchas, open questions.
```

## Section Reference

**Required:** `tldr` frontmatter, `# Title`, `## Target`, `## Behaviour`.
Everything else is included when relevant and omitted when not.

**Exception:** `status: seed` specs are exempt from required sections — they contain raw context awaiting structuring.
See [[c - seed status marks files with unstructured context awaiting template compliance]].

**Section order** follows the template above.
Sections appear in this order when present, but gaps are fine — don't add empty sections.

**Inline markers** (`{[!]}`, `{[?]}`, `{>>}`) can appear anywhere, not just under Future.
See [[spec - gid - semantic symbols for compressed notation]] for marker definitions.

**Claims** start as bullet points in Behaviour and graduate to their own files when they're referenced across specs or need their own detail.
Claim files don't need all sections — sometimes the name and backlinks are the full signal.

**Mapping** uses wiki links in blockquotes for greppability.
Non-md files require the file extension (e.g., `.tsx`, `.py`).
