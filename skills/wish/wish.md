---
tldr: Capture feature requests that aren't yet specced
category: utility
---

# /eidos:wish

Quickly capture a feature idea or request — something you want the system to do eventually, but that doesn't need a spec or plan yet.

## Usage

```
/eidos:wish [description]
```

## Instructions

1. If no description provided, ask what the wish is
2. Run `date '+%y%m%d%H%M'` to get the current timestamp
3. Create `memory/wish - <timestamp> - <claim>.md`:

```markdown
---
tldr: [description]
---

# Wish: [description]

[Optional context — motivation, rough ideas, links to related specs or features]
```

4. Commit immediately

When a wish gets specced out, rename from `wish -` to `specced -` (preserving timestamp and claim), update wiki links, and commit.
Link to the resulting spec with an `=>` note.

## Output

- Creates: `memory/wish - <timestamp> - <claim>.md`
