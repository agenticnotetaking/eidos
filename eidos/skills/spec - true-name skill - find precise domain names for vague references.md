---
tldr: Establish ubiquitous language by finding precise domain names for vague references
---

# /eidos:true-name

## Target

Domain concepts get referred to by different names — or worse, by spatial descriptions ("the thing next to X").
Without authoritative names, every conversation burns cycles translating.

See [[c - ubiquitous language - shared vocabulary across specs code and conversation]].
Spec filenames already act as a naming system, but naming is incidental rather than intentional.

## Behaviour

- Args: vague description, concept, or explicit rename (`X → Y`)
- **Discovery mode:** surveys specs, code, and memory for competing references, then proposes a canonical name with rationale
- **Rename mode:** skips discovery, surveys where the old name appears, shows propagation plan
- Propagates via `git mv` for filenames, content updates for prose, and optionally code identifiers
- Does not rewrite historical files (sessions, solved) — they record what *was*
- A true name is domain-native, precise, stable, self-evident, and consistent with project patterns

## Design

The skill makes naming intentional — it's the DDD practice of establishing ubiquitous language, applied to spec-driven development.
Spec filenames are already a naming system (claim = true name) — this skill elevates that from convention to practice.

No glossary — the specs themselves *are* the glossary.
If a concept has a spec, its filename is the authoritative name.
If it doesn't have a spec, maybe it should.

## Verification

- Finds all references to the concept across specs, code, and memory
- Proposed name meets criteria (precise, stable, self-evident, consistent)
- All wiki links updated after rename — no broken references
- Historical files left untouched

## Interactions

- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — true names must fit the naming convention
- [[spec - eidos - spec driven development loops]] — naming is part of the spec-code bidirectional loop
- [[c - brevity - as much as needed but as little as possible]] — names should be as short as possible while remaining precise

## Mapping

> [[skills/true-name/true-name.md]]
