---
tldr: Create todo files quickly
category: utility
---

# /eidos:todo

Quickly capture a task.

## Usage

```
/eidos:todo [description]
```

## Instructions

1. If no description provided, ask what needs doing
2. Create `memory/todo - <timestamp> - <claim>.md`:

```markdown
---
tldr: [description]
category: utility
---

# Todo: [description]

[Optional context, links to related specs or files]
```

3. Commit immediately

When a todo is completed, rename from `todo -` to `solved -` (preserving timestamp and claim), update wiki links, and commit.

## Output

- Creates: `memory/todo - <timestamp> - <claim>.md`
