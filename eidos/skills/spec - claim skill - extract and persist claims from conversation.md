---
tldr: Capture specific learnings, principles, or conventions as standalone claim files
---

# /eidos:claim

## Target

Claims often emerge mid-conversation — after fixing a bug, clarifying a convention, or discovering why something works a certain way.
Without a dedicated skill, these insights either stay in chat (ephemeral) or get awkwardly forced into specs (wrong abstraction level).
This skill gives claims a direct path from conversation to file.

## Behaviour

- Args: optional topic or insight description
- Extracts the claim from conversation context or user input
- Scans for existing claims that overlap — suggests updating rather than duplicating if it makes sense
- Names the file as a prose claim: `c - <claim>.md` 
- Writes minimal but self-sufficient content — most claims are 5-15 lines
- Structure scales with complexity: simple principle = just prose, complex convention = subsections
- Commits immediately

## Design

Lighter than `/eidos:spec` — no structured Q&A progression, no template.
Claims are freeform by nature; the skill's job is extraction and naming, not structure.

The skill is particularly useful after:
- Fixing a bug (what was the root cause / lesson?)
- Clarifying a convention (what did we decide?)
- Discovering an architectural constraint (why does this work this way?)
- Correcting a misconception (what's the right mental model?)

## Interactions

- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — `c` prefix for claims
- [[template - spec - sections and conventions for spec files]] — claims graduate from spec Behaviour bullets; this skill creates them directly
- [[spec - externalise - persist insights beyond the conversation]] — claims are a form of externalisation
- [[spec - weave skill - discover and prune wiki links between specs]] — natural follow-up to link the new claim

## Mapping

> [[skills/claim/claim.md]]
