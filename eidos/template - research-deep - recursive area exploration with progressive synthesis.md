---
tldr: Template for deep research files — hierarchical areas explored recursively with per-area findings and cross-area synthesis
---

# Deep Research Template

Output path: `memory/research-deep - <timestamp> - <claim>.md`

```markdown
---
tldr: Brief description of the research topic
status: active
budget: 10
budget_type: soft
budget_spent: 0
---

# Deep Research: [Topic]

## Meta

This is a living research document.
Areas are explored one at a time — each has a research plan (what to investigate) and research results (what was found).
The trajectory of later areas can be adjusted as earlier results reshape understanding.
Cross-area synthesis emerges progressively, not as a single final pass.
Sub-areas use decimal numbering (1, 1.1, 1.1.1) — all at the same heading level, hierarchy expressed in the number.

## Seed

> [Verbatim user intent that triggered this research — preserved as-is]

## Question

The overarching question or domain to explore.
Broad enough to warrant multiple areas of investigation.

## Areas

<!-- Outline of areas to explore — discovered upfront, refined as research progresses. -->
<!-- Each area is a self-contained research cycle. -->
<!-- Sub-areas use decimal numbering at the same heading level: Area 1, Area 1.1, Area 1.1.1 -->
<!-- New areas can be added as earlier areas reveal them. -->

### Area 1 - [Name] - status: open

#### Research Plan

1. [ ] First thing to investigate
   - context or approach notes
2. [ ] Second thing to investigate
3. [ ] ...

#### Research Results

##### [Source name / URL]

- Key points
- Relevant detail
- Caveats

##### Findings

Local synthesis for this area — what did we learn?

##### Threads

- Sub-questions or areas that emerged from this research
- => spawned Area 1.1
- => updated Area 3 research plan

---

### Area 1.1 - [Sub-area spawned from Area 1] - status: open

#### Research Plan

1. [ ] ...

#### Research Results

...

---

### Area 2 - [Name] - status: open

#### Research Plan

1. [ ] ...

#### Research Results

...

---

## Trajectory Adjustments

<!-- When earlier areas change the research direction, document it here with timestamps. -->
<!-- Brief reason for each adjustment — don't delete history. -->

## Synthesis

<!-- Written after areas are explored — or updated incrementally as areas complete. -->

Cross-area conclusions drawn from the area-level findings.
Not a summary of each area — a synthesis across them.

- Patterns that span areas
- Tensions or contradictions between areas
- Gaps — what no area covered but matters
- Mental models or frameworks that emerged

## Implications

How this affects the current work.
Specs to create, decisions to make, concepts to adopt.
```

## Field Reference

**Frontmatter:**
- `status` — `active` (still exploring), `complete`, `superseded`
- `budget` — total area units available (integer, or `none` for unconstrained)
- `budget_type` — `soft` (can exceed with justification) or `hard` (strict cap)
- `budget_spent` — number of areas completed so far (incremented after each area, regardless of level)

**Meta:**
- Always present — one paragraph explaining the document's nature
- Keeps the concept visible to anyone opening the file cold

**Seed:**
- Verbatim user prompt/intent in a blockquote
- Preserved as-is — no editing or paraphrasing
- Optional — omit if the research was self-initiated

**Areas:**
- Discovered during initial outline, refined as research progresses
- Each area has two sections: Research Plan (what to do) and Research Results (what was found)
- Status per area: `open`, `active`, `done`, `deferred`
- Sub-areas use decimal numbering at the same heading level: `### Area 1`, `### Area 1.1`, `### Area 1.1.1`
- This keeps all areas at the same structural depth — hierarchy is in the number, not the heading level
- When an area's research reveals a sub-topic, add it as a new area with the next decimal and link from Threads with `=> spawned Area 1.1`

**Research Plan (per area):**
- Checklist of things to investigate, same format as plan actions
- Use `[ ]` for pending, `[x]` for done, `[p]` for deferred
- `=>` notes for observations during investigation
- Can be updated mid-research as earlier findings reshape what matters

**Research Results (per area):**
- Sources: one subsection per source with key points and caveats
- Findings: local synthesis for just this area — should stand alone
- Threads: sub-questions or new areas discovered — use `=>` for acted-on threads

**Trajectory Adjustments:**
- Like plan Adjustments — timestamped entries when direction changes
- Triggered when earlier areas reveal that later areas need reshaping
- Don't delete the original outline — document the evolution

**Synthesis:**
- Cross-area conclusions — the main intellectual output
- Updated incrementally as areas complete, or written in one pass at the end
- Should be valuable even without reading individual areas

**Implications:**
- Connect findings back to current work
- May reference specific areas for detail
