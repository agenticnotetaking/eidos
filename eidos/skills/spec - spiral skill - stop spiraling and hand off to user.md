---
tldr: User-triggered circuit breaker when the AI spirals on any kind of repeated failure
---

# /eidos:spiral

## Target

The AI sometimes spirals — retrying terminal commands, making speculative code fixes, or cycling through debugging attempts that aren't converging.
This burns context and makes no progress.

The debugging strategy rule in core inject tells the AI to notice this and hand off proactively.
But sometimes it doesn't — this skill is the user's manual trigger for the same behaviour.

## Behaviour

- Immediately stops retrying
- Summarises what was attempted and what failed
- Hands off to the user with approach appropriate to the situation:
  - Terminal failures → pasteable command or diagnostic script
  - Code/bug failures → logging, debug overlay, or isolation script
  - General → present options or ask what information is needed
- Waits for the user's response before continuing

## Design

This is a circuit breaker, not a workflow.
It should be fast — no file creation, no ceremony.
The user says "spiral" and the AI shifts from doing to asking.

The core inject rule is the proactive version (AI notices itself spiraling).
This skill is the reactive version (user notices and intervenes).

## Interactions

- Debugging Strategy (core inject) — proactive counterpart
- [[c - agency in implementation not direction - surface reasoning for human steering]] — user steering the AI out of a loop

## Mapping

> [[skills/spiral/spiral.md]]
