---
tldr: Curate external knowledge the project depends on — research or capture mode with structured output
---

# /eidos:reference

## Target

Projects depend on external concepts — frameworks, protocols, patterns, domain knowledge — that aren't owned by the project but are essential to working in it.
Without a place to capture these, the same concepts get re-explained in conversations, scattered across comments, or assumed as tribal knowledge.
Reference docs give external concepts a stable home inside the project's knowledge system.

## Behaviour

- Args: concept name or topic description
- Two modes: **research** (investigate and distil) or **capture** (structure provided knowledge)
- Asks clarifying questions to understand scope and project relevance
- Creates `eidos/reference - <claim>.md` using [[template - reference - curated external knowledge for project use]]
- Commits the reference file
- Presents summary and offers to link from relevant specs

## Design

Reference docs sit between research and specs:
- Unlike **research**, they're not time-bound investigations — they're curated, stable knowledge
- Unlike **specs**, they describe external concepts — things the project uses but doesn't define
- Unlike **claims**, they're not atomic assertions — they're multi-faceted explanations

The key design choice is writing in the project's own words, not copying documentation.
A reference doc should answer "what does this mean *for us*" rather than "what is this in general."

### Two Modes

**Research mode** handles the common case: the user names a concept and the skill investigates it — web search, documentation, codebase patterns — then distils findings into project-relevant terms.

**Capture mode** handles the case where the user already has the knowledge (from a conversation, a document they've read, experience) and just needs it structured and persisted.

Both modes ask clarifying questions to ensure project relevance is captured.

## Verification

- Reference is written in project terms, not copied from docs
- Key Points focus on project-relevant aspects
- How We Use It links to concrete specs or code
- Sources are present and annotated

## Interactions

- [[spec - template - basis for output files]] — reference template
- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — `reference` prefix
- [[spec - externalise - persist insights beyond the conversation]] — reference is an externalisation mechanism
- [[spec - research skill - investigate and document findings with sources]] — research produces time-bound findings; reference curates stable knowledge

## Mapping

> [[skills/reference/reference.md]]
