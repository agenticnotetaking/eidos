---
tldr: Persist images with a markdown companion that captures the essence
---

# Spec: Image Skill

> TL;DR: Drop an image, get a permanent copy and a markdown file that describes what it shows.

## Target

Images dropped into chat are ephemeral — they vanish when the session ends.
The observation-images convention copies them to `memory/`, but the image alone is opaque: unsearchable, unlinkable in wiki context, no textual description.

This skill adds a markdown companion that captures the essence of the image in words, making the content discoverable and useful across sessions.

## Behaviour

- User drops an image and invokes `/eidos:image` (or the skill is routed from context).
- AI examines the image and derives a short claim.
- Both the image and a markdown companion are written to `memory/`:
  - `image - <timestamp> - <claim>.<ext>` — the image file
  - `image - <timestamp> - <claim>.md` — the description
- The markdown file contains a wiki link to the image (with extension) and a prose description.
- Both files are committed together.

## Relationship to Observation Images

The observation-images feature (`inject/feature/observation-images.md`) is passive — it fires on any image in chat.
This skill is intentional and produces richer output.
When `/eidos:image` is invoked, it handles the full pipeline — observation-images doesn't need to also fire.

## Mapping

- `skills/image/image.md` — skill instructions
- `eidos/skills/spec - image skill - persist images with markdown companion.md` — this file
