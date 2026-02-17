---
tldr: Leave inline AI feedback in files for human review
category: core
---

# /eidos:annotate

Leave `{{AI ...}}` annotations inline in files — observations, questions, and suggestions for the human to review.

## Usage

```
/eidos:annotate [file ...]                  # annotate specific file(s)
/eidos:annotate [file ...] --focus <type>   # constrain annotation focus
```

Focus types: `coherence`, `clarity`, `gaps`, `stale`

## Instructions

### 1. Identify Targets

- **File args** → use those files
- **No args** → ask the user what to annotate

### 2. Determine Focus

- **`--focus coherence`** — contradictions within the file or against linked specs
- **`--focus clarity`** — vague claims, missing specificity, ambiguous language
- **`--focus gaps`** — missing sections, uncovered edge cases, absent rationale
- **`--focus stale`** — claims that may no longer match the codebase (read relevant code to check)
- **No focus** → use judgement, err toward fewer, higher-signal observations

### 3. Read and Analyse

Read each target file thoroughly.
If focus is `stale` or `coherence`, also read linked specs and mapped code files.

For each observation, check:
- Is this actionable? (vague concern → skip)
- Is this non-obvious? (restating what the file already says → skip)
- Does this earn its place? (if removing it loses nothing → skip)

### 4. Insert Annotations

Place `{{AI ...}}` markers inline at the relevant point in the file.
Use GID prefixes where they add signal:

- `{{AI ? ...}}` — question
- `{{AI ! ...}}` — important observation
- `{{AI ^ ...}}` — claim/correction
- `{{AI > ...}}` — suggestion
- `{{AI ...}}` — general observation (no prefix)

Each annotation should be self-contained — readable without external context.
Keep annotations concise: one observation per marker.

Target density: **3-7 annotations** for a typical spec file.
If you have more than 7, prioritise and drop the weakest.

### 5. Commit and Report

Commit the annotated file.

```
Annotated [file name]:
- N annotations added (focus: [focus or "general"])
- Key observations: [1-2 sentence summary of themes]

Review inline, then /eidos:refine to process.
```

## Output

- Modifies: target file(s) with `{{AI ...}}` markers
