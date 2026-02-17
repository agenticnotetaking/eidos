---
tldr: Extract learnings, tasks, and incoherences from a session export or file into structured snapshots
---

# /eidos:reflect

## Target

Sessions generate insights that get buried in conversation.
Reflect extracts them into structured files so they persist and can be acted on.

## Behaviour

- Args: file to reflect on (typically a session export or research file)
- Reads the file and identifies:
  - **Learnings** — insights worth preserving
  - **Tasks** — things that need doing
  - **Incoherences** — contradictions or unclear areas discovered
  - **Questions** — things worth investigating
- Presents findings via [[spec - numbered lists - structured selectable output]]
- User selects which items to externalise
- Creates appropriate files for selected items (learning, todo, incoherence, question prefixes)
- Commits created files

## Design

Reflect is the bridge between ephemeral conversation and persistent memory.
It should be used after significant sessions, especially those that explored new territory or made non-obvious decisions.

The numbered list presentation lets the user curate — not everything in a session deserves a file.

## Verification

- Extracts are accurate to the source material
- File types match the content (learnings aren't todos, etc.)
- Selected items produce correctly formatted files

## Interactions

- [[spec - externalise - persist insights beyond the conversation]] — reflect is the structured form of externalisation
- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — uses learning, todo, incoherence, question prefixes

## Mapping

> [[skills/reflect/reflect.md]]
