---
tldr: Template for pull files — raw code collection followed by intent sketch for spec drafting
---

# Pull Template

Output path: `memory/pull - <timestamp> - <claim>.md`

The pull file is working material between reading code and drafting a spec.
It should capture enough to not need to re-read the code, while starting the climb toward intent.
See [[c - pull climbs from code to intent not across from code to prose]].

```markdown
---
tldr: Brief description of what was pulled
status: active
---

# Pull: [Domain / feature name]

## Sources

<!-- One entry per file examined. Brief purpose note — not just filename. -->

- `path/to/file.ts` — [what this file is responsible for]
- `path/to/other.ts` — [what this file is responsible for]

## Existing Specs

<!-- Specs found that already cover this domain. "None found" if none. -->
<!-- This determines whether pull produces a new spec or a diff against an existing one. -->

## Collected Material

<!-- Organised by logical concern, not necessarily per-file. -->
<!-- Multiple files often contribute to one concern. -->
<!-- Capture what matters for re-implementation — skip pure mechanism. -->

### [Concern / component name]

**Purpose:** What it does and why it exists.

**Key behaviours:**
- Observable contracts and guarantees
- What users experience
- Edge cases that matter

**Constants and thresholds:**
- Only those that encode design decisions (e.g. "45° rotation step" = design choice)
- Skip internal implementation details (buffer sizes, variable names)

### [Another concern]

...

## Patterns

<!-- Cross-cutting patterns observed across the collected material. -->
<!-- These often become Design section content in the spec. -->

- [Pattern name] — where it appears, what problem it solves

## Dependencies

<!-- What this code interacts with — other systems, libraries, data sources. -->
<!-- These often become Interactions section content in the spec. -->

## Intent Sketch

<!-- THE CLIMB: this is where collection becomes spec material. -->
<!-- Answer: "what would someone need to know to re-implement this differently?" -->
<!-- NOT: "what does this code do?" -->

<!-- Write 3-7 bullets capturing the intent behind the code. -->
<!-- Each bullet should survive a complete rewrite of the implementation. -->
<!-- If a bullet wouldn't survive a rewrite, it belongs in Collected Material, not here. -->
```

## Field Reference

**Frontmatter:**
- `status` — `active` (still collecting), `complete` (spec drafted), `abandoned`

**Sources:**
- Every file that was read during collection
- Purpose note helps future readers understand why each file was relevant
- Line counts are optional — purpose matters more

**Existing Specs:**
- Search all spec Mapping sections for references to source files
- Also search by domain name
- Drives whether the output is a new spec or a comparison

**Collected Material:**
- Organised by concern, not by file — one concern may span multiple files
- Captures: purpose, key behaviours, design-encoding constants
- Skips: internal variable names, API signatures (unless they _are_ the design), pure mechanism
- The question for each item: "would someone need this to re-implement the feature?"

**Patterns:**
- Repeated structures, shared APIs, architectural choices
- These cross-cut individual concerns
- Often map directly to the spec's Design section

**Dependencies:**
- Systems, libraries, events, data stores this code touches
- Often map to the spec's Interactions section

**Intent Sketch:**
- The most important section — where horizontal collection becomes vertical abstraction
- Each bullet should describe intent that survives a rewrite
- Test: "if I deleted all this code and reimplemented from just these bullets, would the result serve the same purpose?"
- This section feeds directly into spec Behaviour and Target
- Keep it short — 3-7 bullets that capture the essence
