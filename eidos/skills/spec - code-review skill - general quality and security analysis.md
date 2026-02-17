---
tldr: General code review for quality, security, and maintainability — independent of eidos specs
---

# /eidos:code-review

## Target

Spec-aware code review is handled by [[spec - drift skill - read only analysis of spec vs code divergence]] in focused mode (`/eidos:drift [files]`).
This skill covers general code quality: bugs, security issues, maintainability, patterns.
It works in any codebase regardless of spec coverage.

## Behaviour

- Args: file paths, directory, or "recent" for recently changed files
- No argument: ask what to review
- Analyses code for:
  - Bugs and logic errors
  - Security vulnerabilities (OWASP top 10, injection, auth issues)
  - Maintainability concerns (complexity, naming, dead code)
  - Pattern consistency (does this code follow the rest of the codebase?)
- Creates `memory/codereview - <timestamp> - <claim>.md`
- Includes Executive Summary with Health Rating (Good / Fair / Needs Attention)
- Includes Pattern Analysis (positive patterns, concerning patterns, inconsistencies)
- Presents findings via [[spec - numbered lists - structured selectable output]] for selective action
- When user selects items to fix: fix the issue, then update the review file with a link to the fix commit

## Design

Distinct from `/eidos:drift [files]` (spec-aware) — this is general-purpose.
When both spec-aware and general review are wanted, run both.

### Severity Levels

- **Critical** — bugs, security issues that need immediate attention
- **Warning** — patterns that will cause problems later
- **Note** — style, naming, minor improvements

### Finding Structure

Each finding should include: Location (file:line), Issue, Risk/Observation, and Recommendation.

### Health Rating

- **Good** — no critical issues, few warnings, codebase follows good practices
- **Fair** — no critical issues but multiple warnings, or inconsistent patterns
- **Needs Attention** — has critical issues, or many warnings suggesting systemic problems

## Verification

- Catches known bugs in test code
- Security findings are actionable, not false positives
- Findings are grouped by severity

## Interactions

- [[spec - drift skill - read only analysis of spec vs code divergence]] — drift focused mode is the spec-aware complement
- [[spec - architecture skill - snapshot codebase structure and relationships]] — architecture context helps identify pattern violations

## Mapping

> [[skills/code-review/code-review.md]]
