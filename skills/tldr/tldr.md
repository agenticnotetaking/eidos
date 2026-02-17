---
tldr: Ultra-short summary of a topic, file, or set of files
category: observation
---

# /eidos:tldr

Get the gist fast.
Bullet-point summary — as short as possible without losing core ideas.

## Usage

```
/eidos:tldr [target]           — default granularity (minimal)
/eidos:tldr [target] detailed  — more granularity, still concise
```

Target can be a file path, glob pattern, topic name, spec, or "this conversation".

## Instructions

1. Read the target (file, files, spec, or conversation)
2. Distill to **5–10 bullet points** at default granularity
   - Each bullet: one core idea, one line
   - If the source genuinely needs more bullets to avoid losing meaning, go up to ~15
   - With `detailed` arg: allow more bullets, sub-bullets for nuance, but still earn every line
3. Output directly in chat — no file created
4. Use this structure:

```
**TL;DR: [target name]**

- [core idea 1]
- [core idea 2]
- ...
```

## Principles

- Default to **fewer bullets, not more** — the user wants the gist, not a rewrite
- Each bullet should stand alone — no "see above" or forward references
- Prefer concrete over abstract ("uses wiki links for cross-referencing" over "has a linking system")
- If the target is multiple files, give one unified summary, not per-file summaries (unless the user asks)
- Skip boilerplate, imports, config — focus on what the thing *does* and *why*

## Output

- No files created — purely informational
- Displayed directly in chat
