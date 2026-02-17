---
tldr: GID defines semantic symbols that reduce linguistic overhead — eidos inline markers are instances of GID notation
source: https://github.com/ltOgt/GID
---

# GID — General Idea Distillation

GID defines a collection of semantic symbols that can be easily typed on most keyboards.
These symbols extract the goal/aim/kind of an idea, reducing the linguistic overhead needed for its expression.
This is helpful for both storing and retrieving information quickly.

Eidos inline markers (`{[!]}`, `{[?]}`, `{>>}`, `=>`) are instances of GID notation, wrapped in eidos-specific syntax.

## Target

Writing captures thinking, but the overhead of full prose slows both capture and retrieval.
Meetings move fast, ideas are fleeting, and reconnecting with notes later requires scanning dense text.

GID addresses this by:
- Compressing repeated semantic patterns (question, claim, example, ...) into single symbols
- Making the *kind* of each point visible at a glance via its leading symbol
- Supporting tree-structured nesting that allows progressive scanning from general to specific

## Behaviour

GID is made up of three components that build upon each other:
1. **Semantic Symbols** — shorthand for their rough meaning
2. **Semantic Compression** — extracting the goal/aim/kind of a note into a matching symbol, removing the words that would otherwise express it
3. **Level of Detail Hierarchy** — nesting notes into a tree structure where each level adds specificity to its parent

### Symbols

The associated meaning of each symbol is decidedly vague, balancing specificity with flexibility.
There is some overlap between symbols — utilization varies by context.

```
>       Note
.       Side-Note
(..)    Relativation, side-note

<       Counter-Point, Alternative
^       Claim
°       Idea

?       Question
:       Explanation
:=      Definition
^=      Equal Meaning
~       Maybe / Approximation / Like
/       opposite, difference
§       Example
¬       not  (AltGr+6)
!=      not

i       Info (some importance)
!       Important
!!      Very Important

0       Goal/Aim/Focus
S       Error / Problem
=       Solution
x       Condition

->      Follow
=>      Conclusion
<-      Reason

1)      Enumeration
--      Option / Type
+       Pro
-       Contra

//      (internet) source
$       Command-example
>>      Code-example
::      Code-output
|-      (Sub-)Directory

E       parent
e       is element of parent
00      overview

*       reference
#       Inner-Document Reference
{TAG}   Tag
[AB]~   Abbreviation

d       Date
v       Location
@       Person

**      Comment
_       Continued on next line
|       Chain symbols
{..}    Inline side branch / Comment

[ ]     TODO
[x]     TODO - Done
[*]     TODO - Active
[?]     TODO - Unsure
[!]     TODO - Priority
[p]     TODO - Postponed
[~]     TODO - Partly Finished / On Hold
[-]     TODO - Closed / Deprecated
```

### Compression

By extracting some part of an idea into a symbol, you can remove all words that would otherwise be needed to specify that part.

Take for example the note:
```
Peters claims that trees can walk when no one is looking (not sure if that is true).
```
which compresses to:
```
^ Trees can walk when no one is looking {//|@ Peters} {? true}
```

### Level of Detail

Nesting notes into a tree structure is the core idea behind [outliners](https://en.wikipedia.org/wiki/Outliner).
Similar to the outline found in a book, writing in a tree allows you to group multiple aspects of an idea under a more general common point.
Like a book's chapter/section/subsection hierarchy, this structure allows you to scan on a high level before going deeper into the details of the topic you're currently interested in.

If your text editor supports it, you can also collapse sub-trees, hiding information not relevant at the moment.

This parsability is further improved by integrating semantic compression via symbols, since the very first character of each point gives a hint to its content.

Example — same claim, two levels of nesting:

```
^ Trees can walk when no one is looking
  //|@ Peters

  [!] check other sources to confirm
```

or, more decomposed:

```
^ Trees can walk _
  x no one is looking
  //|@ Peters

  ? is this true
    [!] check other sources
```

The degree to which you split larger ideas into nested branches is up to you.
Keep in mind that a very high degree of nesting and compression can make it harder to reconnect with your intended meaning at a later time, since the ambiguity of the symbols might not have enough explicit context to be resolved easily.
Your implicit context during writing might not be present later.

## Design

### Benefits

#### Storage Speed

Similar to [stenography](https://en.wikipedia.org/wiki/Shorthand), reducing the amount of characters needed significantly improves writing speed.
This is useful when the subject of your notes is moving quickly — meetings, lectures, calls, interviews, fleeting ideas.
When your notes can keep up with the content, you miss less of it.

The tree structure also helps: during fast-moving sections, briefly touch on each point and move on.
The structure is already present, and current implicit context can be made explicit by filling in the gaps once a pause presents itself.

#### Retrieval Speed

Both symbol compression and deep nesting help with targeted retrieval.
The tree structure lets you prune large chunks during search — scan the top level, identify relevant branches, exclude the rest, then recurse deeper.

Additionally, scanning symbols at the start of each line lets you dismiss entire sub-trees without reading their content.
(E.g. a sub-tree branching from an example might be irrelevant when looking for a definition.)

#### Active Structuring

When not in a hurry, thinking carefully about structure and symbol utilization deepens understanding.
Reasoning about what can be omitted and how it can best be nested is essentially preparing a simple explanation for your future self.

#### Multithreading

With interleaving subjects (lecture returning to a previous point, stream of consciousness), the tree structure allows quickly locating each thread by flowing down from general parents, guided by indicating symbols.
New information can be included at the right point easily.

#### Transmission

For ideas requiring continued thought across sessions, GID captures the mental state at the point of interruption.
The multitude of open tasks/thoughts/questions that accumulate during any project can be offloaded in a structured and iterative manner (adding detail as you go).
This captures the highly connected nature of thoughts with a little less loss via a lower-dimensional tree, compared to linear text.

Useful when leaving work for the weekend, or before bed with the intention of continuing in the next session.

### Eidos Adaptation

Eidos inline markers are instances of GID notation, wrapped in eidos-specific syntax.
The curly brace wrapper `{ }` is the eidos framing; the content inside follows GID.

#### Active Subset

The following GID symbols are currently used in eidos:

| GID Symbol | Eidos Syntax | Meaning in Eidos | Context |
|---|---|---|---|
| `[!]` | `{[!] ...}` | Planned — will be implemented | Spec markers, anywhere in file |
| `[?]` | `{[?] ...}` | Aspirational — worth investigating | Spec markers, anywhere in file |
| `>>` | `{>> ...}` | Technical hint for implementers | Design/Behaviour sections |
| `=>` | `=>` (bare) | Inline outcome that emerged during execution | Plans, action lists |
| `[p]` | `[p]` (bare) | Postponed — intentionally deferred action | Plans, action lists |
| `{{ }}` | `{{...}}` | Inline refinement comment — human (temporary) | Spec files |
| `{{ }}` | `{{AI ...}}` | Inline annotation — AI (temporary) | Spec files, via `/eidos:annotate` |

GID symbols inside `{{ }}` comments work as prefixes:
- `{{? is this the right approach}}` — question
- `{{! this needs to change}}` — important
- `{{^ this is actually X}}` — claim/correction
- `{{* collision avoidance prefix}}` — special eidos convention, not GID

The subset can expand as usage demands — the full symbol table is the reference.

#### Marker Syntax Rules

- `{<GID> description}` — single-brace markers are persistent (stay in the spec)
- `{{<optional GID prefix> comment}}` — double-brace markers are temporary (resolved by `/eidos:refine`)
- `=>` is used bare (no wrapping) as an inline outcome prefix in plans and action lists

## Verification

- All eidos files use `{[!]}` / `{[?]}` syntax 
- `scripts/future_items.py` correctly parses the new syntax
- Session-start hook surfaces future items with new markers
- The full GID symbol table is documented and referenceable

## Interactions

- [[c - spec refine loop uses double curly braces - creates refinement traces and adjusts spec]] — `{{ }}` comments can use GID prefixes
- [[spec - eidos - spec driven development loops]] — inline markers section references this spec
- [[template - spec - sections and conventions for spec files]] — marker syntax in template
- [[c - arrow prefix marks inline outcomes that emerged during execution]] — `=>` as GID instance

## Mapping

> [[scripts/future_items.py]]

## Future

{[?] Expand active subset as usage patterns emerge — candidates: `^` for claims, `S` for problems, `=` for solutions}
{[?] GID-aware syntax highlighting for eidos files}

## Notes

GID was developed independently of eidos, in the context of part-time work, university lectures, and unstructured thinking sessions.
The eidos adaptation is a narrow projection — it uses a small subset of GID symbols within eidos-specific marker syntax.
The full system remains available for personal note-taking outside of eidos.