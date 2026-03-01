---
tldr: Persist an image with a markdown companion that captures its essence
category: utility
---

# /eidos:image

Persist a dropped image with a markdown file that describes what the image shows.

## Usage

```
/eidos:image
```

User drops an image into chat (or has just dropped one).

## Instructions

1. **Look at the image.** Understand what it shows — a UI, a diagram, a sketch, an error, a photo, whatever it is.
2. Run `date '+%y%m%d%H%M'` to get the current timestamp.
3. Derive a short claim from the image content (what it *is*, not what it's *for*).
4. Determine the image extension from the source path (`.png`, `.jpg`, `.webp`, etc.).
5. **Copy the image** from its temp/cache path to `memory/`:
   `memory/image - <timestamp> - <claim>.<ext>`
6. **Create the markdown companion** at `memory/image - <timestamp> - <claim>.md`:

```markdown
---
tldr: [one-line description]
---

# [claim]

[[image - <timestamp> - <claim>.<ext>]]

[Description of what the image shows — layout, key elements, relationships, text, colours, whatever matters.
Write enough that someone who can't see the image gets the essential information.
Don't over-describe — capture the essence, not every pixel.]
```

7. Commit both files together.
8. If a plan or experiment is active, add an `=> [[image - <timestamp> - <claim>.md]]` reference in the relevant action.

## Notes

- The markdown file is the primary artifact — it's searchable, linkable, and carries context the image alone doesn't.
- The image file uses a wiki link with extension since it's non-markdown: `[[image - ... .png]]`.
- If the user provides context about what the image is for, weave that into the description.
- This skill supersedes the passive observation-images convention when explicitly invoked — it does everything observation-images does plus the markdown companion.

## Output

- Creates: `memory/image - <timestamp> - <claim>.<ext>` (the image)
- Creates: `memory/image - <timestamp> - <claim>.md` (the description)
