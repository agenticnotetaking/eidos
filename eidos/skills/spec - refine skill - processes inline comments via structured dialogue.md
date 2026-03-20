---
tldr: Process inline comments in spec files via structured Q&A dialogue
---

# /eidos:refine

## Target

Spec files accumulate `{{comments}}` as the author reads and thinks. These need to be processed through structured conversation into concrete spec updates. Refine is the skill that drives this loop.

## Behaviour

Two modes:

**Standard mode** (default):
- Args: one or more file paths
- Extracts all `{{comments}}` from the target file(s) with surrounding context
- Groups related comments logically
- Writes structured findings to a refinement file with feedback placeholders (A, B1, B2, C... format with `- [ ]` slots)
- Human fills in feedback at their own pace (in-editor, across sessions if needed)
- When re-invoked: processes feedback, updates spec, marks sections resolved
- Unresolved items remain as `{{comments}}` or become `{?}` future items
- Follows [[c - bias toward artifacts as feedback surfaces over interactive dialogue]] — the refinement file is the review surface, not the chat

**Inline mode** (`/eidos:refine inline [file ...]`):
- Resolves comments directly in the spec — no refinement file
- Trivial comments resolved automatically (obvious fixes, clear intent)
- Ambiguous or substantive comments resolved via AskUserQuestion
- AI annotations presented with reasoning and options
- Warns if inline seems like a bad idea (many comments, complex topics) and suggests standard mode
- Deferred comments left as `{{comments}}` in place

## Design

See [[c - spec refine loop uses double curly braces - creates refinement traces and adjusts spec]] for the full spec of this pattern.

The skill is a downstream artifact of that spec — an example of the eidos philosophy in action.

## Interactions

- Implements [[c - spec refine loop uses double curly braces - creates refinement traces and adjusts spec]]
- Follows [[c - bias toward artifacts as feedback surfaces over interactive dialogue]] — write findings to file first, process feedback second
- Uses [[c - open comment discovery - script to find unresolved refinement comments]] to find files that need refining
- Uses [[c - structured dialogue uses letter number grouping for topic threads]] for the A, B1, B2 format

## Mapping

> [[skills/refine/refine.md]]
