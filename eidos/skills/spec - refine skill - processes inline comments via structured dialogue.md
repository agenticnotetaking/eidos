---
tldr: Process inline comments in spec files via structured Q&A dialogue
---

# /eidos:refine

## Target

Spec files accumulate `{{comments}}` as the author reads and thinks. These need to be processed through structured conversation into concrete spec updates. Refine is the skill that drives this loop.

## Behaviour

- Args: one or more file paths
- Extracts all `{{comments}}` from the target file(s) with surrounding context
- Groups related comments logically
- Presents structured questions (A, B1, B2, C... format)
- Human answers — can be brief, can redirect, can say "correct"
- Creates refinement file in `memory/` with near-verbatim dialogue (both AI presentation and human response — don't condense the AI's side)
- Updates spec file with resolved outcomes
- Unresolved items remain as `{{comments}}` or become `{?}` future items

## Design

See [[c - spec refine loop uses double curly braces - creates refinement traces and adjusts spec]] for the full spec of this pattern.

The skill is a downstream artifact of that spec — an example of the eidos philosophy in action.

## Interactions

- Implements [[c - spec refine loop uses double curly braces - creates refinement traces and adjusts spec]]
- Uses [[c - open comment discovery - script to find unresolved refinement comments]] to find files that need refining
- Uses [[c - structured dialogue uses letter number grouping for topic threads]] for the A, B1, B2 format

## Mapping

> [[skills/refine/refine.md]]
