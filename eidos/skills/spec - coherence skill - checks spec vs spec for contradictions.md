---
tldr: Cross-spec coherence checks to detect contradictions between eidos files
---

# /eidos:coherence

## Target

[[spec - drift skill - read only analysis of spec vs code divergence]] checks spec vs code.
`Coherence` checks spec vs spec.
As the number of spec files grows, contradictions can emerge — one spec assumes shared state while another claims independence.
Coherence surfaces these.

## Behaviour

- Extracts all claims across all specs
- Detects contradictions between specs (claims that conflict with each other)
- Checks wiki-link bidirectionality (if A links to B, does B reference A where expected?)
- Auto-detects general expectations in specs that should be project-wide rules in CLAUDE.md
- Output: `memory/coherence - <ts> - <claim>.md`
- Presents findings via numbered list for user selection

## Design

Coherence operates on the spec graph — the network of wiki-linked spec files.
It looks for:

1. **Claim contradictions** — spec A says X, spec B says not-X
2. **Orphaned links** — wiki links that point to non-existent specs
3. **Missing cross-references** — if specs A, B, C all deal with the same feature but don't link to each other
4. **CLAUDE.md candidates** — claims that are general enough to be project-wide rules (e.g., "all components must be saveable")

Items 2–3 overlap with [[spec - weave skill - discover missing links and prune stale ones]].
Coherence surfaces these during a broader check; weave is the focused tool for link-graph work.

{[?] How to detect contradictions — keyword matching, semantic analysis, or manual curation?}
{[?] Should coherence also check for redundancy — specs that say the same thing?}

### Resolution Workflow

Coherence reports are designed to be worked through step by step.
Each finding gets one of: `**Resolved:**` (fixed), `**Rejected:**` (not a problem), or `**Deferred:**` (acknowledged, not acting now).
The original finding stays intact as the historical record.
Use `/eidos:process` for systematic resolution, or resolve items ad hoc during the session.

## Verification

- Catches known contradictions between test specs
- Wiki-link checks correctly identify orphans and missing cross-references
- CLAUDE.md candidates are sensible recommendations
- Report is actionable — each item has a clear resolution path

## Interactions

- Distinct from [[spec - drift skill - read only analysis of spec vs code divergence]] — drift is spec vs code, coherence is spec vs spec
- [[spec - eidos - spec driven development loops]] — supports the coherence of the spec graph
- Findings may trigger [[c - spec refine loop uses double curly braces - creates refinement traces and adjusts spec]] to resolve contradictions
- [[spec - weave skill - discover missing links and prune stale ones]] — weave handles link-graph structure, coherence focuses on semantic consistency

## Mapping

> [[skills/coherence/coherence.md]]
