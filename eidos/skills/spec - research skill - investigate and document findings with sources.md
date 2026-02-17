---
tldr: Research a topic via web search and codebase exploration, document source notes and distilled findings
---

# /eidos:research

## Target

Development decisions need grounding.
Before choosing an approach, library, or pattern, the team needs to understand the landscape.
Research captures what was found, where it came from, and what it means — so future sessions don't repeat the investigation.

## Behaviour

- Args: topic description or specific question
- Searches web, codebase, and existing eidos/memory files for relevant information
- Documents findings per source before synthesising
- Creates `memory/research - <timestamp> - <claim>.md` using [[template - research - source notes and distilled findings]]
- Commits the research file
- Presents distilled findings and offers next steps

## Design

Research has two distinct phases that must not be collapsed:

1. **Gathering** — find sources, capture what each says on its own terms
2. **Distilling** — synthesise across sources into conclusions

Gathering without distillation produces notes no one reads.
Distillation without source notes loses provenance — you can't verify or revisit the reasoning.

### Workflow

1. **Clarify** — confirm the question, suggest angles to investigate
2. **Search** — web search, codebase grep, existing memory/eidos files
3. **Capture** — one Sources subsection per source with key points
4. **Distil** — synthesise conclusions across sources
5. **Implications** — connect findings to current work, link to affected specs
6. **Create** — write the file, commit
7. **Present** — show distilled findings, offer to act on implications

## Verification

- Source notes are attributable (each has a named source)
- Distillation synthesises rather than summarises
- Implications link to concrete specs or decisions

## Interactions

- [[spec - template - basis for output files]] — research template
- [[spec - plan skill - structured plan for multi step work]] — research often precedes or is embedded in plan actions
- [[spec - externalise - persist insights beyond the conversation]] — research is a primary externalisation mechanism

## Mapping

> [[skills/research/research.md]]
