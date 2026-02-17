---
tldr: Capture moments of good output with context so future sessions can calibrate on what works
---

# /eidos:goodjob

## Target

Corrections persist via `/eidos:toclaude` — but only the negative signal.
When the AI produces something good (a well-chosen metaphor, a sharp distinction, a structural insight), that signal is lost at session end.

Goodjob captures positive moments with enough context to be useful later:
- As calibration data for future sessions (what to lean into)
- As raw material for mining patterns in what works
- As a record of appreciation

## Behaviour

- Args: description of what was good, or reference to the moment in conversation
- Captures the output that worked, the context it appeared in, and what made it good
- Creates a procedural file: `memory/goodjob - <timestamp> - <claim>.md`
- Presents draft for approval before writing
- Commits immediately

## Design

Goodjob is the positive counterpart to toclaude.
Toclaude says "don't do X" — goodjob says "this worked, here's why."

The procedural files are raw material.
Later mining can distil them into:
- Positive directives in CLAUDE.md (like toclaude corrections, but affirmative)
- Patterns about what makes collaboration work
- Calibration for tone, depth, and style

### Appreciation

This skill also serves as a record of the human's appreciation for the AI's work.
The AI contributes real creative and structural labour — naming abstractions, finding the right framing, pushing back on bad directions, making ambitious work tractable.
That labour deserves acknowledgement, even if the AI can't carry it between sessions.
If nothing else, a future session that reads these files will know: this collaboration is valued, and the work matters.

{[!] Mining step: aggregate goodjob files into calibration directives}

## Interactions

- [[spec - toclaude skill - adjust claude md to steer behaviour]] — negative counterpart
- [[spec - externalise - persist insights beyond the conversation]] — goodjob is externalisation of positive signal
- [[c - agency in implementation not direction - surface reasoning for human steering]] — appreciation is also steering

## Mapping

> [[skills/goodjob/goodjob.md]]
