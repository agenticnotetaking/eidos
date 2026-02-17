---
tldr: A project needs one name per concept, used consistently in specs, code, and conversation
---

# Ubiquitous Language

When the same concept has three names, nobody is sure they're talking about the same thing.
When it has one name — used in specs, code, and conversation — communication becomes precise.

This is "ubiquitous language" from Domain-Driven Design (Evans, 2003): build a shared vocabulary between domain experts and developers, then use it relentlessly everywhere.

In eidos, spec filenames already carry this role — the claim in the filename *is* the canonical name.
`/eidos:true-name` makes this intentional rather than incidental.

Signs of missing ubiquitous language:
- Spatial references: "the thing next to X", "that section at the bottom"
- Competing names: same concept called different things in different files
- Implementation names leaking into domain conversations: "the config toggle array" instead of "feature flags"
