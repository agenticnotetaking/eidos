---
tldr: The pattern of leaving comments in spec files, processing them via structured Q&A, and updating
---

# Spec refine loop uses double curly braces — creates refinement traces and adjusts spec

## Target

Specs drift from the author's actual thinking. As you read a spec, you notice things that are wrong, unclear, or missing. You need a lightweight way to mark those spots, then process them in a structured conversation that results in both a refinement trace and an updated spec.

This is the pattern of iterative spec refinement through human-AI dialogue.

## Behaviour

- The human leaves `{{comments}}` inline in spec files at the point where they apply
- The AI leaves `{{AI ...}}` annotations via `/eidos:annotate` (see [[spec - annotate - ai inline feedback for human review]])
- Comments can be corrections, questions, ideas, disagreements, or additions
- `/eidos:refine` reads the file, extracts all `{{comments}}`, and presents structured questions grouped logically (using letter+number format like A, B1, B2, C...)
- The human answers — can be brief, can redirect, can say "correct"
- A refinement file is created with the verbatim Q&A
  - The refinement links to the spec file it was processing
  - The spec does NOT link back to the refinement (discoverable via backlink lookup, avoids spec bloat)
- The spec file is updated with the outcomes of all resolved comments
- Unresolved items remain as `{{comments}}` or become `{[?] ...}` future items
- Comments are committed to git (by the user or before refine runs) but are temporary — they should be resolved

## Design

### Comment Syntax

Double curly braces mark inline comments in spec files:

```markdown
## Behaviour
How users interact with this.
{{this section is too vague, needs specific steps}}

The system responds within 200ms.
{{where does this number come from? is it a claim or aspiration?}}
```

Comments can appear anywhere. They are inline — tied to the context where they appear.

When a spec file contains double curly braces as literal examples (like this spec does), the `*` prefix is the convention for collision avoidance.
To reference the `{{` syntax without triggering detection, use `\{{` (backslash escape) or wrap in backticks/code blocks.

`{{AI ...}}` markers follow the same rules — temporary, inline, resolved by refine.
The `AI` prefix distinguishes authorship so refine can present them differently (AI explains reasoning, human decides).

Comment prefixes follow [[spec - gid - semantic symbols for compressed notation]].

### Unresolved Comment Discovery

`{{comments}}` are temporary and must be resolved. The script [[c - open comment discovery - script to find unresolved refinement comments]] scans eidos files for unresolved comments and surfaces them. `/eidos:next` uses this script to surface open comments as actionable items.

### Session Example

A refine session looks like this. The AI extracts comments, groups them logically, and presents structured questions:

```
### A. Rename section heading

*Line 12*

You commented: {{this should be called Target not Intent}}

No question — applying the rename.

### B1. Claim granularity

*Lines 24-26*

You commented: {{claims should start as bullets but graduate to own files}}

Question: Does every significant claim get its own file, or only ones referenced
across multiple specs?

### B2. Claim file format

*Line 30*

You commented: {{no template enforcement for claims}}

Related to B1 — claim files can use the spec template but don't have to.
Confirming.

### C. Missing section

*Line 40*

You commented: {{need a Friction section here}}

Question: Should Friction always appear in the template, or only when relevant?
```

The human answers each item. Clear directives get confirmed; ambiguous items get questions. The AI creates a refinement file with verbatim Q&A, then updates the spec.

### Processing Flow

```
human edits spec, leaves {{comments}}
  → commits comments
  → /eidos:refine [file(s)]
  → AI reads file, extracts {{comments}}
  → AI groups questions logically (A, B1, B2, C...)
  → presents to human
  → human answers
  → refinement file created in memory/
  → spec file updated with resolved outcomes
  → unresolved items become {[?]} or (rarely) stay as {{comments}}
```

### Refinement File

Created in `memory/` (procedural, not intentional):
```markdown
---
tldr: Q&A from refining [spec name]
---

# Refinement: [Claim about what was refined]

Context: [[spec name]]

---

## A. [Topic]

**Question:**
[AI's question, verbatim]

**Answer:**
[Human's answer, verbatim]

---

## B1. [Sub-topic]
...
```

The refinement links to the spec. The spec does not link back — the refinement is discoverable via backlink lookup, keeping the spec clean.

### Skill Behaviour

The skill should:
- Accept one or more file paths
- Extract all `{{comments}}` with their surrounding context (a few lines before/after)
- Group related comments together
- Present questions that address the comments but also probe for connected issues
- After answers: create refinement file, update spec, commit both

{[?] Should the skill auto-commit after processing, or leave that to the user?}
{[?] Can multiple spec files be processed in one pass, or one at a time?}

## Verification

- Processing a spec with 5+ comments produces a coherent, grouped Q&A session
- The refinement file captures verbatim answers
- The updated spec has all comments resolved or converted to `{[?]}` items (unless explicitly skipped or asked to keep for now)
- Collision avoidance with `*` prefix works when spec contains `{{` as examples

## Mapping

(no implementation yet — this spec was created before the skill)

## Interactions

- The refinement file type uses the `refinement` prefix in `memory/`
- [[spec - eidos - spec driven development loops]] main spec uses this pattern for its own refinement (bootstrapping)
- [[c - open comment discovery - script to find unresolved refinement comments]] — finds comments that need refining
- [[c - eidos is self contained - definitions do not rely on external systems]]

## Future

{[?] Detect `{{comments}}` at session start and offer to refine them}
{[?] Auto-extract potential claims from the Q&A into their own files}

## Notes

- This pattern was discovered while building eidos — the first spec refinement sessions used exactly this flow before it was codified.
- The `/eidos:refine` skill is a downstream artifact of this spec — an example of the eidos philosophy in action: spec first, implementation follows.