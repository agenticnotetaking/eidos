---
tldr: Bidirectional translation between prose and GID notation — compress to .gid or decompress back to prose
---

# /eidos:gid

## Target

Dense notes are hard to scan; verbose prose is slow to write.
GID notation compresses text by extracting the kind of each idea into a symbol, making structure visible at a glance.
But GID is hard to read cold — decompression recovers the prose when needed.

This skill makes GID usable as an active format, not just a reference.

## Behaviour

- Two modes: `compress` (prose → GID) and `decompress` (GID → prose)
- Aliases: `write` = compress, `read` = decompress
- Accepts files, multiple files, URLs, or inline text
- Uses the **full** GID symbol set, not just the eidos subset
- Compress outputs to `<basename>.gid`; decompress outputs to `<basename>.md`
- User can override output path

See [[spec - gid - semantic symbols for compressed notation]] for the full symbol table, compression rules, and tree nesting conventions.

## Design

The skill is a direct application of GID's three components:
1. **Symbols** — map each unit of meaning to its GID symbol
2. **Compression** — strip words the symbol already carries
3. **Tree nesting** — group related points under parents, indent 2 spaces per level

### Compress

- Identify structure in the source (topics, claims, questions, examples, ...)
- Map each to the matching GID symbol
- Build a tree with top-level = main topics, deeper = more specific
- Use `{..}` for inline asides, `|` to chain symbols, `_` for continuation
- When uncertain, keep more words — recoverability over maximum compression

### Decompress

- Parse the tree via indentation
- Expand each GID symbol to natural language
- Reconstruct flowing prose or structured sections
- Preserve intent, not original wording — decompression is interpretive

### Round-trip

Compress → decompress will not reproduce the original text.
It should preserve the core meaning and structure.
This is by design — GID symbols are intentionally vague.

## Verification

- Compressing a 400-line spec produces a readable .gid file at roughly 50% size
- Decompressing that .gid file recovers all key claims and structure
- Symbols are used correctly (not just `>` for everything)
- Tree depth matches the source's conceptual hierarchy

## Interactions

- [[spec - gid - semantic symbols for compressed notation]] — the notation system (delegates all symbol definitions and conventions here)

## Mapping

> [[skills/gid/gid.md]]
