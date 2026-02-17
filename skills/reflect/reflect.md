---
tldr: Extract learnings from session or file
category: observation
---

# /eidos:reflect

Extract learnings, tasks, and incoherences from a file.

## Usage

```
/eidos:reflect [file]
```

## Instructions

### 1. Read the Source

Read the target file (session export, research, or any file with insights to extract).

### 2. Identify Extractables

Categorise findings:
- **Learnings** — insights worth preserving (`learning -` prefix)
- **Tasks** — things that need doing (`todo -` prefix)
- **Incoherences** — contradictions discovered (`incoherence -` prefix)
- **Questions** — things worth investigating (`question -` prefix)

### 3. Present for Selection

Use [[spec - numbered lists - structured selectable output]] format:

```
1 - Learnings
  - 1.1 - Session tokens are simpler than JWT for our use case
  - 1.2 - Rate limiting should be middleware, not per-endpoint
2 - Tasks
  - 2.1 - Audit existing error handling for consistency
3 - Incoherences
  - 3.1 - Auth spec says stateless but session spec assumes state
4 - Questions
  - 4.1 - Should we support multiple simultaneous sessions?

Which items to externalise? (e.g., "1.1, 2.1, 3.1")
```

### 4. Create Files

For each selected item, create the appropriate file:
- `memory/learning - <claim>.md`
- `memory/todo - <timestamp> - <claim>.md`
- `memory/incoherence - <claim>.md`
- `memory/question - <claim>.md`

Commit all created files together.

### 5. Update Source

Add `=>` wiki links in the numbered list snapshot to track what was created:

```
  - 1.1 - Session tokens are simpler than JWT
    - => [[learning - session tokens simpler than JWT for single server]]
```

## Output

- Creates: files with appropriate prefixes in `memory/`
- Creates: `memory/reflect - <timestamp> - <claim>.md` (the snapshot)
