---
tldr: Structured analysis of eidos skill outputs to surface quality issues and drive improvement
---

# /eidos:meta

## Target

Eidos skills produce outputs — pull generates specs, drift generates reports, coherence finds contradictions.
These outputs vary in quality.
The meta skill closes the feedback loop: analyse what a skill produced, identify problems, and drive improvements through structured dialogue.

This is the skill that was done manually in [[meta - 2602111408 - pull output analysis and abstraction direction]] — now codified.

## Behaviour

- Takes skill output as input (file, paste, or from conversation context)
- Identifies the source skill and what it targeted
- Analyses along relevant dimensions: abstraction level, completeness, coherence, signal-to-noise, spec-worthiness
- Presents structured findings using letter/number grouping (A, B1, B2, C...)
- Drives multi-round dialogue — follows threads the human engages with, drops what they skip
- Creates procedural trace: `memory/meta - <timestamp> - <claim>.md`
- Optionally acts on outcomes: update skills, extract claims, file todos

## Design

Meta is a second-order skill — it operates on the outputs of other skills, not on code or specs directly.

The structured dialogue pattern (A, B1, B2...) is shared with [[spec - refine skill - processes inline comments via structured dialogue|refine]].
Where refine processes `{{comments}}` in specs, meta processes the quality of skill outputs.

The key analytical lens is abstraction level — whether output sits at the right layer for its purpose.
[[c - pull climbs from code to intent not across from code to prose]] emerged from exactly this kind of analysis.

Meta traces in `memory/` serve two purposes:
1. Procedural record of what was found and decided
2. Raw material for improving skills — patterns across multiple meta sessions reveal systematic issues

## Interactions

- [[c - structured dialogue uses letter number grouping for topic threads]] — the A, B1, B2 format used in feedback
- [[spec - refine skill - processes inline comments via structured dialogue]] — shares the structured dialogue pattern
- [[spec - goodjob skill - capture positive calibration with context]] — meta may surface moments worth capturing
- [[spec - externalise - persist insights beyond the conversation]] — meta traces are externalisation
- [[c - pull climbs from code to intent not across from code to prose]] — first output of a meta session
- [[solved - 2602111609 - structured feedback pattern for meta analysis sessions]] — related: the ABC pattern as a reusable concept

## Mapping

> [[skills/meta/meta.md]]
