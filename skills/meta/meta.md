---
tldr: Analyse eidos skill output for quality, abstraction level, and coherence
category: observation
---

# /eidos:meta

Analyse the output of an eidos skill and drive a structured feedback loop to surface quality issues, abstraction-level problems, and improvement directions.

## Usage

```
/eidos:meta [file or paste]      # analyse specific output
/eidos:meta                      # look for recent skill output in conversation
```

## Instructions

### 1. Identify the Output

- **File arg** → read the file (could be a pull output, drift report, spec draft, etc.)
- **Pasted content** → use the pasted text directly
- **No arg** → scan the current conversation for the most recent skill output (look for patterns like `<pull>`, `<spec>`, drift reports, coherence findings)

Identify which skill produced the output (pull, drift, coherence, push, etc.) and what it was targeting.

### 2. Analyse

Evaluate the output against these dimensions:

- **Abstraction level** — is it at the right layer? (behaviour vs technique vs code detail)
  - Use the swappability test: could you swap the mechanism and the claim still holds?
  - Technicals that encode design preferences are fine; pure mechanism is not
- **Completeness** — does it cover what it should? Missing sections, gaps in coverage?
- **Coherence** — does it contradict itself or existing specs?
- **Signal vs noise** — is every sentence earning its place, or is there filler?
- **Spec-worthiness** — would you downstream code from this? Would it survive a rewrite of the implementation?

Not all dimensions apply to every output.
Focus on what matters for the specific skill and context.

### 3. Structured Feedback

Present findings grouped by topic using letter/number notation:

```
Meta: [skill name] output on [target]

A. [First topic]
   Observation: [what you noticed]
   Example: [concrete quote or reference from the output]
   Question: [specific question for the human]

B. [Second topic]
   B1. [Sub-point]
       Observation: ...
   B2. [Sub-point]
       Observation: ...
```

Wait for the human's responses.
Responses can be:
- Agreement or disagreement with reasoning
- A redirect ("actually the real issue is...")
- "skip" for topics to defer
- Elaboration that refines the observation

Multiple rounds are expected.
Follow up on responses, go deeper where the human engages, drop threads they skip.

### 4. Create Meta Trace

When the dialogue reaches natural conclusions, create `memory/meta - <timestamp> - <claim>.md`:

```markdown
---
tldr: [Analysis of skill output — brief summary of what was found]
category: observation
---

# Meta: [what was analysed]

Context: [which skill, what target, what prompted the analysis]

---

## A. [Topic]

**Observation:** [what was noticed]
**Human:** [verbatim or close paraphrase of their response]
**Resolution:** [what this means — a concrete takeaway]

---

## B. [Topic]
...

---

## Next Steps

- [ ] [Concrete actions that emerged — spec updates, skill changes, claims to extract]
```

Show the draft to the user.
If approved, write and commit.

### 5. Act on Outcomes (optional)

If the meta analysis surfaces concrete changes:
- Offer to update the skill or spec that produced the output
- Offer to extract claims (e.g. `[[c - ...]]`)
- Offer to create todos for deferred items
- Offer to run the skill again with the improvements

Don't push — present options and let the human decide.

## Output

- Creates: `memory/meta - <timestamp> - <claim>.md`
- May trigger: spec updates, skill updates, new claims, new todos
