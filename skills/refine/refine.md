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

### 3. Write Refinement File

Run `date '+%y%m%d%H%M'` to get the current timestamp.
Create `memory/refinement - <timestamp> - <claim>.md` (per [[spec - naming - prefixes structure filenames as prefix claim pairs]], e.g. `refinement - 2602101418 - refine loop spec comment processing.md`).

Write findings to the file as a feedback surface — don't present them in chat and wait for answers.
See [[c - bias toward artifacts as feedback surfaces over interactive dialogue]].

Handle the two marker types differently in the file:

```markdown
---
tldr: Refinement of [spec name] — [brief topic summary]
---

# Refinement: [spec name]

Spec: [[spec name]]

# A. [Topic] — status: open

**Comment:** `{{original comment text}}`
**Context:** [the section and nearby claims]
**Question:** [specific question to resolve this]

- [ ]

# B. [Topic] — status: open

**Comment:** `{{AI original annotation text}}`
**Reasoning:** [why the AI flagged this]
**Options:**
1. Agree (apply suggested change)
2. Disagree (remove annotation)
3. [other option if relevant]

- [ ]
```

Guidelines:
- Group related comments logically (A, B1, B2, C... format).
- Human `{{comments}}` get a Question — the AI asks what to do.
- AI `{{AI ...}}` annotations get Reasoning + Options — the AI explains, the human decides.
- Each item gets an empty `- [ ]` feedback slot.
- Sections have status: `open` → `resolved`.

Commit the refinement file.

Tell the user:
```
Refinement written to [[refinement - <timestamp> - <claim>]]

Fill in feedback, then I'll update the spec.
```

### 4. Process Feedback (when re-invoked or feedback provided)

When the user comes back with feedback filled in:
1. Read the refinement file
2. For each item with feedback:
   - Apply to the spec: replace resolved `{{comments}}`, convert deferrals to `{[?]}`, remove "not needed" items
   - Mark section status: `open` → `resolved`
3. Items with empty `[ ]` are skipped (no feedback = defer)
4. Update the refinement file with answers for the record
5. Commit updated spec and updated refinement file

### 5. Summary

```
Refined [spec name]:
- N comments resolved
- M deferred as {[?]}
- K skipped (no feedback)

Refinement: [[refinement - <timestamp> - <claim>]]
```

## Output

- Creates: `memory/refinement - <timestamp> - <claim>.md`
- Modifies: target spec file(s) in `eidos/` (after feedback)
