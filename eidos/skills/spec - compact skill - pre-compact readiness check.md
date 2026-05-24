---
tldr: Verify nothing is lost or stale before compacting or clearing a session
---

# /eidos:compact

## Target

Before compacting context or starting a new session, you need confidence that nothing is lost — plan is current, git is clean, no loose ends.
Done handles session-end ceremony (export, reflect, merge).
Compact is lighter: a read-only check that says "safe to go" or "fix these first".

## Behaviour

- Checks git status for uncommitted changes
- Checks active plan's Progress Log is current
- Flags in-progress actions missing completion notes
- Lists relevant open todos
- Reports verdict: clean or pending items

## Design

Almost entirely read-only — the one write is deleting this session's agent registration file (if any).
The registration describes an *active* agent; compact is the signal that the agent is winding down, so the file should not outlive the session.
Matching is by frontmatter `branch:` + `cwd:` — robust against context compaction forgetting the original UID.

The lightest possible "are we done?" signal.

Compact and done serve different moments:
- **compact** = "can I safely clear context?" (mid-flow checkpoint)
- **done** = "session is ending, wrap everything up" (full ceremony)

## Interactions

- [[spec - done skill - session end with export and merge]] — heavier session-end alternative
- [[spec - plan skill - structured plan for multi step work]] — checks plan currency
- [[spec - git workflow - branch per task with atomic commits]] — checks git cleanliness

## Mapping

> [[skills/compact/compact.md]]
