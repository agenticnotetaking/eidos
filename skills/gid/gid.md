---
tldr: Compress text to GID notation or decompress GID back to full text
category: utility
---

# /eidos:gid

Bidirectional translation between prose and GID (General Idea Distillation) notation.
Two modes: **compress** (prose → GID) and **decompress** (GID → prose).

## Usage

```
/eidos:gid compress <source>    # prose → GID
/eidos:gid write <source>       # alias for compress

/eidos:gid decompress <source>  # GID → prose
/eidos:gid read <source>        # alias for decompress
```

Source can be: a file path, multiple file paths, a URL, or inline text in the conversation.

## Instructions

### Reference

Before processing, internalise the full GID symbol table and conventions from [[spec - gid skill - semantic symbols for compressed notation]].
The **full** symbol set applies here, not just the eidos subset.

Key principles:
- Each symbol extracts the goal/aim/kind of an idea, removing the words that would otherwise express it
- Tree nesting groups related ideas under general parents — deeper = more specific
- The first character(s) of each line signal the kind of content
- Compression is lossy by design — favour scan-speed over completeness
- Implicit context during writing may not be present during reading — balance compression with recoverability

### Compress Mode

1. **Read the source** — file(s), URL content, or inline text
2. **Identify structure** — find the main topics, subtopics, claims, questions, examples, etc.
3. **Map to GID symbols** — for each unit of meaning, identify which GID symbol captures its kind:
   - Is it a claim? → `^`
   - A question? → `?`
   - An example? → `§`
   - A definition? → `:=`
   - Important? → `!` or `!!`
   - A goal? → `0`
   - A problem? → `S`
   - A solution? → `=`
   - A follow/consequence? → `->` or `=>`
   - A reason? → `<-`
   - A counter-point? → `<`
   - Pros/cons? → `+` / `-`
   - A source reference? → `//`
   - A todo? → `[ ]` (with variants `[!]`, `[?]`, `[x]`, etc.)
   - A note? → `>` or `.` for side-notes
   - An idea? → `°`
   - A condition? → `x`
4. **Build the tree** — nest related points under their parents, using indentation (2 spaces per level)
5. **Compress inline** — use `{..}` for inline branches, `|` to chain symbols, `_` for continuation
6. **Remove redundant words** — the symbol already carries the meaning; strip linguistic scaffolding like "this is an example of", "the reason is", "it's important that"

#### Compression Guidelines

- **Top level** = main topics or goals (`0`, `>`, `^`)
- **Second level** = supporting points, explanations, conditions
- **Third level+** = details, examples, sources, todos
- Chain symbols with `|` when a point has multiple aspects: `//|@ Peters` (source + person)
- Use `{..}` for brief inline asides that don't warrant their own line
- Use `_` when a point continues on the next line
- Tags `{TAG}` for categorisation, abbreviations `[AB]~` for recurring terms
- Don't over-compress: if a point would be unrecoverable without its original context, keep more words

#### Output

Write the result to `<source-basename>.gid` (or `<name>.gid` for inline/URL input).
If the source is a single file `notes.md`, output to `notes.gid` in the same directory.
If the user specifies a different output path, use that.

### Decompress Mode

1. **Read the GID source** — file or inline text
2. **Parse the tree** — follow indentation to reconstruct the hierarchy
3. **Resolve symbols** — expand each GID symbol back to natural language:
   - `^` → "[Author] claims that..." or "Claim: ..."
   - `?` → "Question: ..." or "Is it true that...?"
   - `§` → "For example, ..."
   - `:=` → "[Term] is defined as ..."
   - `!` → "Important: ..."
   - `0` → "Goal: ..." or "The aim is ..."
   - `S` → "Problem: ..."
   - `=` → "Solution: ..."
   - `->` → "This leads to ..."
   - `=>` → "Therefore, ..." or "Conclusion: ..."
   - `<-` → "The reason is ..."
   - `<` → "On the other hand, ..." or "Alternatively, ..."
   - `+` → "Pro: ..." or "Advantage: ..."
   - `-` → "Con: ..." or "Disadvantage: ..."
   - `//` → "Source: ..."
   - `[ ]` variants → "TODO: ..." with appropriate status
   - `>` → (just the note text)
   - `°` → "Idea: ..."
   - `x` → "Condition: ..." or "When ..."
   - `@` → person name
   - `d` → date
   - `v` → location
3. **Reconstruct prose** — turn the tree back into flowing paragraphs or structured sections
   - Respect the hierarchy: top-level points become paragraphs or section headers
   - Nested points become sentences within those paragraphs
   - Inline branches `{..}` become parenthetical remarks or footnotes
   - Chained symbols `|` get expanded to their respective meanings
4. **Preserve intent** — decompress recovers meaning, not the original text verbatim. The output should be clear, readable prose that captures what the GID notes encode.

#### Output

Write the result to `<source-basename>.md` (or present inline if the source was inline).
If the source is `notes.gid`, output to `notes.md` in the same directory.
If the user specifies a different output path, use that.

## Notes

- Compression quality depends on the source material — highly structured text compresses better than conversational prose
- Decompression is inherently interpretive — GID symbols are intentionally vague, so the expansion involves judgement calls
- Round-tripping (compress → decompress) will not reproduce the original text, but should preserve the core meaning
- When uncertain about a symbol mapping during compression, prefer the more general symbol and keep more words
- The `.gid` extension is a convention — the content is plain text with GID notation
