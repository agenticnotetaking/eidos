---
tldr: Recursive deep research — outline areas, explore each progressively, synthesise across areas
category: observation
---

# /eidos:research-deep

Deep research on a broad topic via recursive area exploration and progressive externalisation.

## Usage

```
/eidos:research-deep [topic or domain]                  # start — will ask for budget
/eidos:research-deep [topic] budget 10                  # start with soft budget of 10
/eidos:research-deep [topic] budget 10 hard             # start with hard budget of 10
/eidos:research-deep [topic] budget none                # start with no budget constraint
/eidos:research-deep continue                           # resume existing deep research
```

## When to Use

Use research-deep (not regular research) when:
- The topic is broad enough to have multiple distinct sub-domains
- You need a landscape view, not a single answer
- The user says "go deep", "step by step", "explore different approaches"
- Research in one area is likely to reveal new areas to explore

Regular `/eidos:research` is better for focused questions with a specific answer.

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
- How many areas (budget)? Each area — top-level or sub-area — costs 1 unit.
- Hard or soft? Soft = agent can exceed with justification or ask for more. Hard = strict cap.
- "None" is valid — no budget constraint, agent uses judgement on depth.

If the user already provided a clear scope (like a detailed prompt), confirm and proceed — but still ask for budget if not specified.

#### 2. Outline Areas

Think about the topic and identify 4-8 areas that together cover the landscape.
This is the research plan — it will evolve as you learn more.

Read the template: [[template - research-deep - recursive area exploration with progressive synthesis]]

Run `date '+%y%m%d%H%M'` to get the current timestamp.
Create `memory/research-deep - <timestamp> - <claim>.md` with:
- Frontmatter including budget fields (`budget`, `budget_type`, `budget_spent`)
- Meta section (standard — explains the living document concept)
- Seed section (verbatim user intent in a blockquote)
- The Question filled in
- Areas outlined with names, brief descriptions, and research plans (checklist items)
- Empty Synthesis and Implications sections

Commit immediately.

Present the area outline to the user:
```
Research plan for [topic]:

1. [Area 1] — brief description
2. [Area 2] — brief description
...

Starting with Area 1. I'll update the file after each area.
continue?
```

#### 3. Research Areas Progressively

For each area:

1. Set area status to `active`
2. Work through the Research Plan — check off items as you investigate them, add `=>` notes
3. Search across sources (web, codebase, memory, documentation)
4. Add sources under Research Results as you find them — don't hold in memory
5. Write area-level Findings after sources are gathered
6. Note any Threads — sub-questions or new areas that emerged
7. If threads warrant a sub-area, add it as the next decimal (Area 1.1, 1.2, etc.) at the same heading level
8. Set area status to `done`
9. Increment `budget_spent` in frontmatter
10. Commit

**Sub-areas** use decimal numbering at the same heading level — hierarchy is in the number, not the markdown structure:
```
### Area 1 - Type theory foundations - status: done
### Area 1.1 - Hindley-Milner inference - status: open
### Area 1.1.1 - Algorithm W variants - status: open
### Area 2 - Gradual typing - status: open
```

**Budget awareness** — after completing each area, check the budget:

- **Under budget:** proceed normally. Note threads that could become sub-areas but weigh them against remaining budget.
- **Approaching budget (>75% spent):** be selective. Only spawn sub-areas for genuinely important threads. Note skipped threads with `=> would explore with more budget: [description]`.
- **At budget (soft):** ask the user — "I've used N/N budget. [Thread X] seems important. Can I get M more units?" If they say no, wrap up with notes on what was left unexplored.
- **At budget (hard):** stop exploring new areas. Finish the current area, then move to Synthesis. Note all unexplored threads in the Trajectory Adjustments section.
- **No budget:** use judgement — go deep where it's valuable, don't explore for the sake of it.

**After each area**, give a brief status update:
```
Area X done: [one-line summary of findings]
Budget: N/M spent [soft|hard]
Threads: [any new areas discovered]
Moving to Area Y.
```

**After every 2-3 areas**, pause for the user:
```
Progress: X/Y areas complete. Budget: N/M spent [soft|hard].
[Brief summary of what's emerging across areas]
continue?
```

#### 4. Adjust Trajectory

If earlier areas reveal that the research direction needs to change:
- Add/remove/reorder areas as needed
- Update Research Plans in upcoming areas based on what was learned
- Document the change in the Trajectory Adjustments section with a timestamp
- Ask the user before adding more than 2 new areas — scope can grow fast

#### 5. Synthesise

After all areas are explored:

1. Write the Synthesis section — patterns, tensions, gaps, frameworks
2. This is cross-area thinking, not area summaries
3. Write Implications — connect to current work
4. Set status to `complete`
5. Commit

#### 6. Present and Offer Next Steps

Show the synthesis (not the full file) and offer:
```
Deep research complete: [[research-deep - <timestamp> - <claim>]]

[Key synthesis points]

Options:
1 - Act on implications (create specs, decisions, etc.)
2 - Go deeper on [specific area or thread]
3 - Done for now
```

---

### Continue Mode

#### 1. Find Deep Research

Search `memory/` for `research-deep - *.md` files with status not `complete` or `superseded`.

**Single active research-deep:** load it directly.
**Multiple active:** present a selection list.
**None active:** offer to start a new one.

#### 2. Read and Assess State

Read the research-deep file thoroughly.
Determine:
- Which areas are done, which are open
- Whether the current area has open research plan items
- What threads were noted but not yet spawned as areas
- Whether trajectory adjustments are needed based on completed areas

#### 3. Present State and Propose Next

**If an area is in progress (status: active):**
```
Resuming: [[research-deep - <timestamp> - <claim>]]

**Area N: [name]** — [M/T research plan items done]
Last finding: [brief summary]

Continuing with next research plan item.
Proceed?
```

**If current area is done, next area is open:**
```
Resuming: [[research-deep - <timestamp> - <claim>]]

Progress: X/Y areas complete.
Last area: [name] — [key finding]
Open threads: [any unspawned threads]

Next: Area N - [name]
Proceed, or adjust trajectory?
```

**If all areas are done:**
```
Resuming: [[research-deep - <timestamp> - <claim>]]

All Y areas complete.
[Brief overview of what emerged]

Ready to write Synthesis and Implications.
Proceed?
```

Then continue with the relevant step from Start Mode (step 3, 4, or 5).

---

## Principles

**Progressive externalisation over end-of-research dumps.**
Write sources and findings as you go.
The file is a living document during research, not a report written at the end.
This preserves detail and lets the user redirect mid-research.

**Area independence.**
Each area should be understandable on its own.
A reader can skip to one area and get its conclusions without reading the rest.

**Threads are first-class.**
When researching one area reveals something about another, capture it.
Threads are how the recursive structure emerges — they connect areas and spawn new ones.

**Trajectory is mutable.**
The initial outline is a hypothesis.
What you learn in Area 1 may completely reshape what matters in Area 5.
Document the evolution — don't pretend you knew the right areas from the start.

**Synthesis earns its place.**
Cross-area synthesis should say things that no single area says.
If the synthesis is just "Area 1 found X, Area 2 found Y" — it's not synthesis.

## Output

- Creates: `memory/research-deep - <timestamp> - <claim>.md`
- Status field starts as `active`, set to `complete` when done
- Intermediate commits after each area
