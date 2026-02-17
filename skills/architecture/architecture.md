---
tldr: Snapshot codebase structure for reference
category: observation
---

# /eidos:architecture

Snapshot the current codebase structure and architectural patterns.
Act as a **documentarian, not an evaluator** — document what exists without suggesting improvements.

## Usage

```
/eidos:architecture [scope]
```

Scope: directory path, module name, or "full" (default: full).

## Instructions

### 1. Gather Information

For full snapshots, document each of these:

**Git State**
- Current branch and commit
- Recent significant commits
- Active branches

**Directory Structure**
- Top-level organisation
- Key directories and their purposes
- File counts / size indicators where useful

**Tech Stack**
- Languages and frameworks
- Key dependencies
- Build tools

**Module Breakdown**
- Major components / modules
- How they connect
- Data flow patterns (API calls, stores, events)

**Entry Points**
- Where execution begins
- Key configuration files
- Environment requirements

For scoped queries, document only what's relevant to the scope.

### 2. Identify Patterns

- State management approach
- Routing / navigation
- Testing patterns
- Build / deployment setup

### 3. Create Architecture File

Create `memory/architecture - <timestamp> - <claim>.md`:

```markdown
---
tldr: [Brief scope description]
category: observation
---

# Architecture: [Scope]

## Git State

- **Branch:** `main`
- **Commit:** `abc1234` — "Recent commit message"
- **Active branches:** feature/x, bugfix/y

## Directory Structure

project/
  src/
    components/    # UI components
    services/      # Business logic
    utils/         # Shared utilities
  tests/
  config/

## Tech Stack

- **Language:** TypeScript 5.x
- **Framework:** React 18
- **Build:** Vite
- **Key deps:** react-query, zustand, tailwind

## Modules

### [Module Name]
[Description, files involved, how it works]

### [Module Name]
[Description, files involved, how it works]

## Entry Points

- `src/main.tsx` — Application bootstrap
- `vite.config.ts` — Build configuration

## Patterns

[Architectural patterns identified in the codebase]

## Notes

[Deviations, oddities, technical debt observed]
```

The claim should describe what was documented:
- `architecture - 2602141030 - full codebase snapshot.md`
- `architecture - 2602141030 - authentication flow.md`

### 4. Follow-up Questions

If the user asks follow-up questions about the same architecture:
1. **Append to existing file** rather than creating a new one
2. Add a new section with timestamp

```markdown
## Follow-up: How does session refresh work?
_Added: 2602141130_

[Answer to the follow-up question]
```

### 5. Commit and Present

Commit the file.
Present a summary and link to related specs if they exist.

## Output

- Creates: `memory/architecture - <timestamp> - <claim>.md`

## When to Use

- Onboarding to a new codebase
- After major refactors or architectural changes
- Before starting significant new work
- Periodic snapshots for historical reference
- Answering "how does X work?" questions
