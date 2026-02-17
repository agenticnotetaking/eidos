---
tldr: Takes semi-specified text and routes it into the spec system as new or adjusted specs and claims
---

# /eidos:toeidos

## Target

Insights about a system emerge from many places: chat discussions, human notes, code review observations, session reflections.
These insights need to find their home in the spec system, but the triage step — is this a new spec? a new claim? an adjustment to an existing one? — requires judgment.

This skill takes semi-specified text and routes it to the right place in `eidos/`.

## Behaviour

- Args: text describing an insight, observation, or requirement (can be rough/unstructured)
- Reads existing specs and claims in `eidos/` to understand current coverage
- Analyzes the input to determine:
  - **New spec** — a distinct concern not yet covered
  - **New claim** — a verifiable statement that deserves its own file
  - **Adjustment to existing spec** — content that belongs in or modifies an existing file
  - **Adjustment to existing claim** — refinement of an existing claim
- Presents the proposed action to the user for confirmation before executing
- Creates or modifies the appropriate file(s)
- Updates wiki links and references as needed

### Triage Logic

1. **Search** existing specs and claims for overlap
2. **If strong overlap** → propose adjustment to existing file, showing the diff
3. **If partial overlap** → surface the related files, ask whether to extend existing or create new
4. **If no overlap** → propose new spec or claim, with a draft
5. **Always** present the decision to the user — never auto-create without confirmation

### Input Quality

The skill handles rough input:
- Stream of consciousness notes
- Bullet points from a discussion
- Half-formed ideas
- Copy-pasted chat excerpts

It structures and distills, then routes.
The user doesn't need to pre-format.

## Design

This skill is the intake mechanism for the spec system.
Without it, insights stay in chat or human notes and never become part of the persistent spec graph.
It formalises the pattern described in [[c - specs emerge from discussions and serve as fixpoints not required reading]].

The skill embodies the [[spec - externalise - persist insights beyond the conversation]] principle applied specifically to the spec layer.

### Flow

1. **Parse** — extract the core insight(s) from rough text
2. **Search** — find related specs and claims in `eidos/`
3. **Classify** — new spec, new claim, or adjustment
4. **Draft** — prepare the content (new file or proposed edits)
5. **Present** — show the user what will happen and why
6. **Execute** — create or modify files after confirmation
7. **Link** — update references and wiki links

### Multiple Insights

Input may contain several distinct insights.
The skill processes each one independently, presenting them as a batch for user review:

```
Found 3 insights in your input:

1. New spec: "planning as a distinct mode" → create spec - planning - ...
2. Adjust: spec - externalise → add section on spec-layer externalisation
3. New claim: "specs get created based on brief discussions" → c - specs emerge from discussions ...

Proceed with all, or select which to apply?
```

## Verification

- Correctly identifies when input overlaps with existing specs
- Produces well-formed spec or claim files following [[spec - naming - prefixes structure filenames as prefix claim pairs]]
- Never auto-creates without user confirmation
- Handles rough, unstructured input gracefully

## Friction

- May misjudge where content belongs — user confirmation mitigates this
- For very rough input, multiple rounds of clarification may be needed
- Large `eidos/` folders increase the search cost

## Interactions

- [[spec - eidos - spec driven development loops]] — toeidos feeds the spec system
- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — output files follow naming conventions
- [[spec - externalise - persist insights beyond the conversation]] — toeidos is externalisation for the spec layer
- [[spec - refine skill - processes inline comments via structured dialogue]] — refine works on existing comments, toeidos works on external input

## Mapping

> [[skills/toeidos/toeidos.md]]
