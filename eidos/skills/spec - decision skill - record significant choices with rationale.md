---
tldr: Record a significant decision with options, rationale, and consequences
---

# /eidos:decision

## Target

Decisions made during work are either lost in chat or buried as `=>` notes in plans.
Significant choices — where alternatives were evaluated and the rationale matters — deserve their own file.
This skill guides that capture.

## Behaviour

- Args: optional topic or question being decided
- Clarifies the decision point (use AskUserQuestion if broad)
- Identifies viable options with trade-offs
- Records chosen option with rationale
- Notes consequences (specs to update, code to adjust, follow-ups)
- Creates `memory/decision - <timestamp> - <claim>.md` following the template
- Links to relevant plans and specs
- Commits immediately

## Design

Decisions sit between plans and specs on the weight hierarchy.
Plans track what to do; specs track what should be; decisions track why we chose this path over that one.

The threshold for using this skill: alternatives were genuinely evaluated and the rationale would help future-you.
Below that threshold, `=>` notes in plans suffice.

### Flow

1. **Clarify** — what are we deciding, what constraints matter
2. **Options** — each with trade-offs and implications
3. **Choose** — which option and why (ask user if not already decided)
4. **Consequences** — what changes as a result
5. **Create** — file following [[template - decision - options rationale and outcome]]
6. **Link** — connect to plans and specs
7. **Offer next steps** — update affected specs, continue work, or done

## Verification

- File follows the decision template structure
- Chosen option has clear rationale, not just selection
- Consequences identify concrete follow-ups
- Linked to originating plan or spec if one exists

## Interactions

- [[template - decision - options rationale and outcome]] — file structure
- [[spec - externalise - persist insights beyond the conversation]] — decisions are an externalisation target
- [[spec - plan skill - structured plan for multi step work]] — decisions often emerge during plan execution

## Mapping

> [[skills/decision/decision.md]]
