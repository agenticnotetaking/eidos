---
tldr: Review code for quality, security, and maintainability
category: observation
---

# /eidos:code-review

General-purpose code review — independent of eidos specs.

## Usage

```
/eidos:code-review [scope]
```

Scope options:
- `path/to/dir` — review specific directory
- `path/to/file.ts` — review specific file
- `recent` — review files changed in recent commits
- No argument — ask what to review

## Instructions

### 1. Determine Scope

- Specific files/directories: review those
- `recent`: use git to find recently changed files
- No argument: ask what to review

### 2. Analyse

For each file, check:

**Critical (fix now):**
- Logic errors and bugs
- Security vulnerabilities (injection, auth bypass, data exposure)
- Race conditions, resource leaks

**Warning (fix soon):**
- Error handling gaps
- Complexity that invites bugs
- Missing validation at system boundaries

**Note (consider):**
- Naming and readability
- Dead code or unused imports
- Pattern inconsistency with rest of codebase

### 3. Identify Patterns

Look for:
- **Positive patterns** — good practices being followed consistently
- **Concerning patterns** — anti-patterns or bad habits spreading
- **Inconsistencies** — mixed approaches to the same problem

### 4. Create Review File

Create `memory/codereview - <timestamp> - <claim>.md`:

```markdown
---
tldr: [Brief scope description]
category: observation
---

# Code Review: [Scope]

## Executive Summary

**Health Rating:** [Good / Fair / Needs Attention]

**Key Findings:**
- [1-3 sentence summary of most important findings]

## Critical

1 - [Finding title]
  - **Location:** `file.ts:42`
  - **Issue:** [Description of the problem]
  - **Risk:** [What could go wrong]
  - **Recommendation:** [How to fix]

## Warnings

2 - [Finding title]
  - **Location:** `file.ts:100`
  - **Issue:** [Description]
  - **Recommendation:** [How to address]

## Notes

3 - [Finding title]
  - **Location:** `file.ts`
  - **Observation:** [What could be better]
  - **Suggestion:** [Improvement idea]

## Pattern Analysis

### Positive Patterns
- [Pattern observed and where it's used well]

### Concerning Patterns
- [Anti-pattern and examples]

### Inconsistencies
- [Mixed approaches to same problem]

## Summary

- **Files reviewed:** X
- **Critical issues:** Y
- **Warnings:** Z
- **Notes:** W

Which items would you like to address?
```

Use [[spec - numbered lists - structured selectable output]] format for findings within each section.

The claim should summarise findings:
- `codereview - 2602141030 - 2 critical issues in auth module.md`
- `codereview - 2602141030 - healthy codebase minor suggestions.md`

### 5. Health Rating Guide

- **Good** — no critical issues, few warnings, codebase follows good practices
- **Fair** — no critical issues but multiple warnings, or inconsistent patterns
- **Needs Attention** — has critical issues, or many warnings suggesting systemic problems

### 6. Present for Action

Show findings grouped by severity.
Offer to fix selected items.

### 7. Acting on Findings

When user selects items to address:
1. Fix the issue
2. Update the review file showing the fix:

```markdown
1 - SQL injection in user query
  - **Location:** `db.ts:42`
  - **Issue:** User input concatenated into SQL
  - **Fixed:** commit `abc1234` — converted to parameterised query
```

## Output

- Creates: `memory/codereview - <timestamp> - <claim>.md`

## When to Use

- Before major releases
- After acquiring or inheriting a codebase
- Periodic quality checks
- Before significant refactoring
- When onboarding to understand code quality