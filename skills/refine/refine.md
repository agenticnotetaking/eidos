---
tldr: Process inline comments in specs via structured dialogue
category: core
---

# /eidos:refine

Process `{{comments}}` and `{{AI ...}}` annotations in eidos spec files through structured Q&A, then update the spec with resolved outcomes.

## Usage

```
/eidos:refine [file ...]         # refine specific file(s)
/eidos:refine                    # find files with open comments automatically
```

## Instructions

### 1. Find Comments

- **File args** → use those files
- **No args** → run `${CLAUDE_PLUGIN_ROOT}/scripts/open_comments.py` to find all files with unresolved `{{comments}}` or `{{AI ...}}` annotations

If multiple files have comments and no args were given, present a numbered list and let the user choose which to refine.

### 2. Extract Comments

For each target file:
1. Read the full file
2. Extract all `{{comments}}` and `{{AI ...}}` annotations with their surrounding context (the section they're in, nearby claims)
3. Group related comments logically
4. Note the author of each marker — human `{{...}}` vs AI `{{AI ...}}`

### 3. Structured Dialogue

Present items in a structured format, grouped by topic.
Handle the two marker types differently:

**Human `{{comments}}`** — the AI asks questions to resolve:
```
A. [Topic]
   {{original comment text}}
   Context: [the section and nearby claims]
   Question: [specific question to resolve this]
```

**AI `{{AI ...}}` annotations** — the AI explains its reasoning, the human decides:
```
B. [Topic]
   {{AI original annotation text}}
   Reasoning: [why the AI flagged this]
   Options:
   1 - Agree (apply suggested change)
   2 - Disagree (remove annotation)
   3 - Discuss
```

Wait for the human's answers.
Answers can be:
- A direct response
- "correct" (confirms the comment's assumption)
- A redirect to a different approach
- "skip" or "defer" (leave for later)

### 4. Create Refinement Trace

Create `memory/refinement - <timestamp> - <claim>.md` capturing both sides of the dialogue near-verbatim.
Don't condense the AI's presentation — the user's answer only makes sense in the context of what was asked and explained.

```markdown
---
tldr: Refinement of [spec name] — [brief topic summary]
category: core
---

# Refinement: [spec name]

## Questions and Answers

### A. [Topic]
**Comment:** {{original text}}
**Presented:**

[The AI's full explanation, options, and reasoning as presented in chat — not a summary]

**Answer:**

[Verbatim human response]

**Resolution:** [what this means for the spec]

### B. [Topic]
...
```

The trace is the record of how a decision was reached.
If the AI's explanation is condensed, the answer loses its context and the reasoning becomes opaque.

Commit the refinement trace.

### 5. Update Spec

Apply resolved outcomes to the spec file:
- Replace resolved `{{comments}}` with the decided content
- Convert deferred items to `{[?]}` future markers
- Remove comments that were answered with "not needed" or similar

Show the diff to the user before writing.
Commit the spec update.

### 6. Summary

```
Refined [spec name]:
- N comments resolved
- M deferred as {[?]}
- K removed

Refinement trace: [[refinement - <timestamp> - <claim>]]
```

## Output

- Creates: `memory/refinement - <timestamp> - <claim>.md`
- Modifies: target spec file(s) in `eidos/`
