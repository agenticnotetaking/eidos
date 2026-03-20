---
tldr: Deep research explores broad topics via hierarchical areas — each area is a mini research cycle, cross-area synthesis produces the real insight
---

# /eidos:deepresearch

## Target

Some questions are too broad for a single research pass.
"How do different languages handle type systems" isn't answered by finding three articles — it requires mapping a landscape, exploring regions, and then seeing the whole.

Regular research finds answers.
Deep research builds understanding.

## Behaviour

- Args: topic description or domain to explore; `continue` to resume
- Two modes: start (new research) and continue (resume existing)
- Outlines 4-8 areas that cover the landscape
- Explores each area as a mini research cycle: research plan (checklist) → sources → findings → threads
- Sub-areas use decimal numbering at the same heading level (Area 1, Area 1.1, Area 1.1.1) — hierarchy in the number, not the markdown structure
- Threads discovered in one area can spawn sub-areas or reshape later areas
- Trajectory adjustments documented when earlier areas change the research direction
- Progressive externalisation — file updated and committed after each area
- Cross-area synthesis after all areas are explored
- Creates `memory/deepresearch - <timestamp> - <claim>.md` using [[template - deepresearch - recursive area exploration with progressive synthesis]]
- Seed section preserves verbatim user intent; Meta section explains the living document concept
- Budget system: each area (any level) costs 1 unit. Can be soft (exceed with justification), hard (strict cap), or none (unconstrained). Tracked in frontmatter as `budget`, `budget_type`, `budget_spent`

## Design

Deep research has three layers, each building on the last:

1. **Outlining** — identify the areas that together cover the topic
2. **Exploring** — research each area independently (sources -> findings -> threads)
3. **Synthesising** — draw conclusions that span areas

### What Makes It "Deep"

Regular research is flat: sources -> distillation.
Deep research is hierarchical: areas -> per-area sources -> per-area findings -> cross-area synthesis.

The hierarchy serves two purposes:
- **Scope management** — broad topics become tractable when broken into areas
- **Emergence** — threads discovered in one area reveal connections and new areas

### Flat Hierarchy via Decimal Numbering

Sub-areas stay at the same heading level as top-level areas — `### Area 1`, `### Area 1.1`, `### Area 1.1.1`.
This avoids deep markdown nesting while expressing arbitrarily deep topic structure.
The decimal number carries the hierarchy; the heading level keeps the document scannable.

### Budget as Scope Control

Recursive research can expand without bound — every area spawns threads, every thread could be an area.
The budget is a single number that forces trade-off decisions: go broad (many top-level areas) or go deep (fewer areas with sub-areas).

- 1 unit per area, regardless of depth level
- Soft budget: agent can exceed but must justify or ask for more
- Hard budget: strict cap — stop and synthesise when spent
- No budget: agent uses judgement, doesn't explore for its own sake

The budget makes the breadth-vs-depth trade-off explicit and negotiable rather than implicit and invisible.

### Continue Mode

Deep research often spans multiple sessions.
`continue` mode finds the active deepresearch file, reads its state, and proposes the next area to explore.
Same pattern as `/eidos:experiment continue` — find, assess, resume.

### Progressive Externalisation

The file is the working document, not a report.
Each area is committed as it completes.
This means:
- Detail is preserved (not compressed into a final summary)
- The user can redirect mid-research
- Session boundaries don't lose progress
- The file reflects the research journey, not just conclusions

### Relationship to Regular Research

Deep research contains regular research — each area is effectively a focused research cycle.
The added value is the outline (what to explore) and the synthesis (what it means together).

If a deepresearch starts and turns out to be narrow enough for regular research, just collapse it — no ceremony needed.

## Verification

- Areas are independent — each has sources, findings, and threads
- Threads link areas — emergence is captured, not lost
- Synthesis says things no single area says
- File has intermediate commits — not written in one pass
- User had checkpoints to redirect
- Budget spent matches the number of completed areas
- Skipped threads noted with `=> would explore with more budget` when budget constrained

## Interactions

- [[spec - research skill - investigate and document findings with sources]] — deep research contains regular research at the area level
- [[spec - template - basis for output files]] — deepresearch template
- [[spec - planning - structured intent between spec and code]] — outline of areas is structurally similar to plan phases
- [[spec - externalise - persist insights beyond the conversation]] — progressive externalisation is core to the approach

## Mapping

> [[skills/deepresearch/deepresearch.md]]
