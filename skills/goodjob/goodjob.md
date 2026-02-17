---
tldr: Capture positive calibration with context
category: utility
---

# /eidos:goodjob

Capture a moment of good AI output with context, so future sessions can calibrate on what works.

## Usage

```
/eidos:goodjob [description of what was good]
```

## Instructions

### 1. Understand the Moment

Identify what was good — could be:
- A well-chosen framing or metaphor
- A structural insight or distinction
- Good taste in a design decision
- An approach that clicked
- Anything the human found valuable

If the description is brief, look back in the conversation for the full context.

### 2. Draft the Record

Capture three things:
- **What** — the output or idea itself (quote or paraphrase)
- **Context** — what we were working on, what prompted it
- **Why it worked** — what made this good (the human's words or inferred from their reaction)

Format:

```markdown
---
tldr: [brief description of what was good]
status: unprocessed
---

# Goodjob: [claim about what worked]

## What

[The output, idea, or moment — quoted or paraphrased]

## Context

[What we were working on, what question or task prompted this]

## Why It Worked

[What made this good — from the human's feedback or inferred]

# Goodjob: [next thing]
<!-- Just do this for all things in the session that worked well or got explicit postivive feedback from the human>
```

### 3. Present and Write

Show the draft to the user.
If approved, write to `memory/goodjob - <timestamp> - <claim>.md`.
Commit.

## Processing

Goodjob files start as `status: unprocessed`.
`/eidos:next` surfaces unprocessed goodjobs.
To process: run `/eidos:toeidos` on the goodjob file to extract the pattern into a claim, rule, or spec update, then set `status: processed`.

## Output

- Creates: `memory/goodjob - <timestamp> - <claim>.md`
- Status: `unprocessed` → `processed` (after pattern is extracted via `/eidos:toeidos`)