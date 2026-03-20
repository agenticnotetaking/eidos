---
tldr: Process inline comments in specs via structured dialogue
category: core
---

# /eidos:refine

Process `{{comments}}` and `{{AI ...}}` annotations in eidos spec files through structured Q&A, then update the spec with resolved outcomes.

## Usage

```
/eidos:refine [file ...]         # refine specific file(s) — creates refinement file
/eidos:refine                    # find files with open comments automatically
/eidos:refine inline [file ...]  # resolve comments directly in the spec, no extra file
```

## Mode Detection

Check ARGUMENTS for `inline`:
- If `inline` → go to **Inline Mode**
- Otherwise → go to **Standard Mode** (steps 1-5 below)

---

## Standard Mode

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

---

## Inline Mode

Resolve comments directly in the spec — no refinement file, no async feedback loop.
Good for small batches where the human is present and can answer questions live.

### 1. Find and Extract Comments

Same as Standard Mode steps 1-2 — find files, extract comments.

### 2. Warn If Inline Seems Like a Bad Idea

Before proceeding, check whether inline mode is appropriate.
**Warn and suggest standard mode** if:
- More than ~6 comments across files — too many for interactive resolution
- Multiple comments require deep thought or cross-referencing other specs
- Comments span many unrelated topics — async feedback is better

```
This file has 12 comments across 4 topics — inline might be tedious.
Switch to standard mode (creates a refinement file for async feedback)?
```

If the user insists on inline, proceed.

### 3. Resolve Comments

Process each comment one at a time:

**Trivial comments** (obvious fix, clear intent, no ambiguity):
- Resolve automatically — apply the change, remove the `{{comment}}`
- Show what was done: `Resolved: {{fix typo in claim}} — fixed spelling`

**AI annotations** (`{{AI ...}}`):
- Present the reasoning and options via AskUserQuestion
- Apply the chosen option, remove the annotation

**Ambiguous or substantive human comments** (`{{...}}`):
- Ask the user via AskUserQuestion — present the comment, its context, and a specific question
- The agent can also suggest a resolution as one of the options
- Apply the answer, remove the `{{comment}}`

**Comments the agent isn't sure about:**
- Present reasoning and ask — don't guess silently
- If the user defers, leave the `{{comment}}` in place

After each resolution (or small batch of related ones), commit.

### 4. Summary

```
Refined [spec name] inline:
- N comments resolved
- M left in place (deferred)
```

## Output

**Standard mode:**
- Creates: `memory/refinement - <timestamp> - <claim>.md`
- Modifies: target spec file(s) in `eidos/` (after feedback)

**Inline mode:**
- Modifies: target spec file(s) in `eidos/` directly
- No refinement file created
