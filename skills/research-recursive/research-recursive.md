---
tldr: Recursive research — each area becomes its own file, branching deeper via wiki-linked children
category: observation
---

# /eidos:research-recursive

Recursive research on a broad topic where each area gets its own file.
Areas can branch into sub-areas as nested wiki-linked research files, creating a navigable tree.

## Usage

```
/eidos:research-recursive [topic or domain]                  # start — will ask for budget
/eidos:research-recursive [topic] budget 10                  # start with soft budget of 10
/eidos:research-recursive [topic] budget 10 hard             # start with hard budget of 10
/eidos:research-recursive [topic] budget none                # no budget constraint
/eidos:research-recursive continue                           # resume existing recursive research
```

## When to Use

Use research-recursive (not research-deep) when:
- The topic is broad enough that areas deserve their own files
- You want to branch arbitrarily deep on promising threads
- The research tree should be navigable — readers pick which branches to follow
- Each area may grow large enough that one file would become unwieldy

Use `/eidos:research-deep` when all areas belong in a single document.
Use `/eidos:research` for focused questions with a specific answer.

## Instructions

### Mode Detection

Check ARGUMENTS:
- If `continue` → go to **Continue Mode**
- Otherwise → go to **Start Mode** (ARGUMENTS is the topic)
- Parse `budget N` and optional `hard` from args if present

---

### Start Mode

#### 1. Clarify and Scope

Use AskUserQuestion to establish:
- What's the overarching question or domain?
- Any known areas of interest, or should we discover them?
- How deep should we go? (survey vs. deep dive)
- Any specific angles, constraints, or contexts?

**Budget:** If not provided in args, ask:
- How many areas (budget)? Each area file — top-level or nested — costs 1 unit.
- Hard or soft? Soft = agent can exceed with justification or ask for more. Hard = strict cap.
- "None" is valid — no budget constraint, agent uses judgement on depth.

#### 2. Create Root File

Think about the topic and identify 4-8 areas that together cover the landscape.

Run `date '+%y%m%d%H%M'` to get the current timestamp.
Create `memory/research-recursive - <timestamp> - <claim>.md` — this is the **root file**.

```markdown
---
tldr: Brief description of the research topic
status: active
budget: 10
budget_type: soft
budget_spent: 0
---

# Research: [Topic]

## Meta

This is a recursive research tree.
Each area is explored in its own file, linked from this root.
Areas can branch deeper — sub-areas become nested files linked from their parent.
Budget is shared across the entire tree.

## Seed

> [Verbatim user intent that triggered this research — preserved as-is]

## Question

The overarching question or domain to explore.

## Areas

1. [ ] [[research-recursive - <timestamp> - <area 1 claim>]] — brief description
2. [ ] [[research-recursive - <timestamp> - <area 2 claim>]] — brief description
3. [ ] [[research-recursive - <timestamp> - <area 3 claim>]] — brief description
...

## Trajectory Adjustments

<!-- When earlier areas change the research direction, document it here with timestamps. -->

## Synthesis

<!-- Cross-area conclusions — written after areas are explored, or updated incrementally. -->

## Implications

<!-- How this affects current work. Specs to create, decisions to make, concepts to adopt. -->
```

**Do not create the area files yet** — just list them as wiki links in the root.
Commit the root file.

Present the area outline:
```
Research plan for [topic]:

1. [Area 1] — brief description
2. [Area 2] — brief description
...

Budget: N [soft|hard|none]
Starting with Area 1.
continue?
```

#### 3. Research Areas

For each area:

1. Run `date '+%y%m%d%H%M'` for the area file timestamp
2. Create `memory/research-recursive - <timestamp> - <area claim>.md`:

```markdown
---
tldr: Brief description of this area
status: active
parent: "[[research-recursive - <root timestamp> - <root claim>]]"
---

# [Area Name]

## Research Plan

1. [ ] First thing to investigate
   - context or approach notes
2. [ ] Second thing to investigate
3. [ ] ...

## Sources

### [Source name / URL]

- Key points
- Relevant detail
- Caveats

## Findings

Local synthesis for this area — what did we learn?

## Threads

- Sub-questions or areas that emerged
- => spawned [[research-recursive - <timestamp> - <sub-area claim>]]
```

3. Work through the Research Plan — investigate, add sources, write findings
4. Note threads — sub-questions that emerged
5. **If a thread warrants its own area and budget allows:** create a nested area file, link it from Threads with `=>`, and add it to the parent's Areas list
6. Set status to `done`
7. Mark `[x]` in the parent file's area list
8. Increment `budget_spent` in the **root** file's frontmatter
9. Commit

**Budget awareness** — after completing each area, check budget in the root file:

- **Under budget:** proceed normally. Note threads that could branch but weigh against remaining budget.
- **Approaching budget (>75% spent):** be selective. Only branch for genuinely important threads. Note skipped threads with `=> would explore with more budget: [description]`.
- **At budget (soft):** ask the user — "I've used N/N budget. [Thread X] seems important. Can I get M more units?"
- **At budget (hard):** stop exploring new areas. Finish current area, then move to Synthesis.
- **No budget:** use judgement.

**After each area**, give a brief status update:
```
Area done: [one-line summary]
Budget: N/M spent [soft|hard]
Threads: [any new branches created]
Moving to next area.
```

**After every 2-3 areas**, pause:
```
Progress: X/Y areas complete. Budget: N/M spent.
[Brief summary of what's emerging]
continue?
```

#### 4. Adjust Trajectory

If earlier areas reveal that the research direction needs to change:
- Add/remove areas in the root file
- Update research plans in upcoming area files
- Document the change in the root's Trajectory Adjustments section with timestamp
- Ask the user before adding more than 2 new top-level areas

#### 5. Synthesise

After all areas are explored:

1. Write the Synthesis section in the **root file** — patterns, tensions, gaps, frameworks
2. This is cross-area thinking, not area summaries
3. Write Implications — connect to current work
4. Set status to `complete`
5. Commit

#### 6. Present and Offer Next Steps

```
Research complete: [[research-recursive - <timestamp> - <claim>]]

[Key synthesis points]

Tree: N files (root + M area files)

Options:
1 - Act on implications (create specs, decisions, etc.)
2 - Go deeper on [specific area or thread]
3 - Done for now
```

---

### Continue Mode

#### 1. Find Research

Search `memory/` for `research-recursive - *.md` files that have no `parent` in frontmatter (these are root files) and status not `complete` or `superseded`.

**Single active root:** load it.
**Multiple active:** present a selection list.
**None active:** offer to start a new one.

#### 2. Read and Assess State

Read the root file.
For each area listed, check if the linked file exists and read its status.
Determine:
- Which areas are done, which are open
- Whether the current area has open research plan items
- What threads were noted but not yet branched
- Whether trajectory adjustments are needed

#### 3. Resume

Present state and propose next action, then continue with the relevant step from Start Mode.

---

## Principles

**One file per area.**
Each area is self-contained — a reader can open one area file and understand it without reading the rest.
The root file is the map; area files are the territory.

**Wiki links are the structure.**
The tree emerges from `[[wiki links]]` between files, not from heading hierarchy.
This means areas can be reorganised by updating links, not restructuring a monolith.

**Budget is global.**
All area files — regardless of nesting depth — draw from the same budget in the root file.
This forces the same breadth-vs-depth trade-off as research-deep.

**Depth follows value.**
Don't branch just because you can.
A thread becomes a sub-area file only when it has enough substance to warrant its own research cycle.

## Output

- Creates: `memory/research-recursive - <timestamp> - <claim>.md` (root)
- Creates: `memory/research-recursive - <timestamp> - <area claim>.md` (per area)
- Nested areas create further files linked from their parent
- Root status starts as `active`, set to `complete` when done
- Intermediate commits after each area file
