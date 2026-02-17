---
tldr: Template for plan files — phases, actions, progress log, and learnings
---

# Plan Template

Output path: `memory/plan - <timestamp> - <claim>.md`

```markdown
---
tldr: Brief description what the plan is about (may need to be updated on larger shifts)
status: active
---

# Plan: [Brief description]

## Context

<!-- Link to related artifacts if they exist -->
- Spec: [[spec - ...]]
- Goal: [[goal - ...]]

## Phases

### Phase 1 - [Name] - status: open

1. [ ] First action
   - planning notes go here before starting
2. [ ] Second action
3. [ ] Third action

### Phase 2 - [Name] - status: open

1. [ ] First action
2. [ ] ...

<!-- Observations go inside phases — see Field Reference. -->

## Verification

[How to verify the plan is complete — tests, behaviour checks, acceptance criteria]

## Adjustments

<!-- Plans evolve. Document changes with timestamps. -->

## Progress Log

<!-- Timestamped entries tracking work done. Updated after every action. -->
```

## Field Reference

**Frontmatter:**
- `status` — `open`, `active`, `paused`, `completed`, `abandoned`

**Phases:**
- Split work into logical groups
- Each phase has its own status
- Actions are atomic — one action, one commit
- Use `[x]` for done, `[ ]` for pending, `[p]` for postponed
- `[x]` means every sub-bullet is satisfied — verify each against actual output before marking done
- Partial completion stays `[ ]` with `=>` notes for what's done and what remains
- `[p]` means intentionally deferred — add `=>` note with reason. Postponed actions are skipped by `/eidos:next` and `/eidos:plan-continue`

**Action sub-notes:**
Actions can have nested bullet points for context.
Notes added before starting are plain bullets.
Notes added during or after implementation use `=>` prefix to mark them as observations:

```
1. [ ] Research auth approaches
   - check JWT vs session tokens
   - look at existing middleware

2. [x] Implement login endpoint
   - use bcrypt for password hashing
   - => session tokens chosen over JWT — simpler for our case
   - => [[spec - auth - session based authentication]] created
   - => found existing rate limiter in utils/rateLimit.ts
```

The `=>` makes it easy to see what was planned vs what emerged.
Created files are tracked inline with `=>` rather than in a separate section.

**Observations:**
- Structured findings from testing or reviewing the running system
- Added via `/eidos:observe` — typically after a phase completes and the user tests the result
- Live inside the phase they relate to, as a sub-section after the actions:

```
### Phase 2 - Panel view - status: done

1. [x] Focus column
   ...

#### Observations (from YYMMDDHHMM user testing)

##### P2-O1 — Line numbers should be per-line, not per-block — FIXED

**Was:** only block elements got line numbers.
**Fix:** recursive AST walk annotates list items too.
**Verify:** each `<li>` renders its own line number.

##### P2-O2 — Scroll indicator lags behind scroll

**Was:** CSS transition on viewport indicator.
**Expected:** immediate response to scroll.
```

- Numbered per-phase: P1-O1, P2-O1, etc. — keeps references local and unambiguous
- Each observation has: short title, Was/Expected (or Was/Fix/Verify), optional Impact and Spec notes
- Mark `FIXED` in the title when resolved
- Implementation tasks reference observations: `[ ] Fix P2-O1 — line numbers per-line`
- Tasks go in the same phase (if it's still open) or a new phase after current

**Adjustments:**
- Timestamped entries when the plan changes
- Brief reason for the change
- Don't delete history — add to it

**Progress Log:**
- Updated after every completed action (this is part of the action, not optional cleanup)
- The plan is the persistent record — chat is ephemeral
- Without progress log updates, the next session has no idea what happened
- Brief timestamped entries — detail lives inline under the action itself
