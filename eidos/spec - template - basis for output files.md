---
tldr: Templates define the structure of output files — specs, plans, decisions, research, references, pulls
---

# Templates — basis for output files

## Target

Specs, plans, decisions, and drift reports all need consistent structure.
Templates in `eidos/` define that structure — they are the intentional form of what output files should look like.
Without templates, each invocation reinvents the format.

## Behaviour

- Templates live in `eidos/` alongside specs (intentional, not procedural)
- Each template defines the skeleton for one type of output
- Skills reference their template and fill in context-specific content
- The template is a blueprint, not a rigid contract — sections can be omitted or extended as needed
- Template filenames follow `template - <name> - <claim>.md`

## Templates

- [[template - spec - sections and conventions for spec files]] — structure for eidos spec files
- [[template - plan - structured phases with actions and progress tracking]] — used by `/eidos:plan`
- [[template - decision - options rationale and outcome]] — used by decision-recording skills
- [[template - research - source notes and distilled findings]] — used by `/eidos:research`
- [[template - reference - curated external knowledge for project use]] — used by `/eidos:reference`
- [[template - pull - collected code material with intent sketch]] — used by `/eidos:pull`

## Interactions

- [[spec - eidos - spec driven development loops]] — templates are part of the Design section
- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — `template` prefix defined there
