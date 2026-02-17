---
tldr: Pattern for presenting structured information with selectable items using decimal notation
---

# Numbered Lists — structured selectable output

## Target

Skills that surface findings (coherence checks, drift reports, next items) need a consistent way to present results that the user can act on selectively.
A structured numbered format lets users reference specific items unambiguously.

## Behaviour

### Format

Top-level numbers for categories, decimal notation for items:

1 - Category Name
  - 1.1 - First item in category
  - 1.2 - Second item in category
2 - Another Category
  - 2.1 - Item in second category

Output as plain markdown, not in a code block.

### User Selection

After displaying the list, prompt:
```
Which items to act on? (e.g., "1.1, 2.3 optional comment")
```

User can respond with:
- Single item: `1.1`
- Multiple items: `1.1, 2.3, 3.2`
- Item with comment: `2.1 (add deadline)` or `2.1 - with extra context`

### Linking Results

When acting on a selection creates a file, add a wiki link under the original item:

```markdown
1 - Spec Contradictions
  - 1.1 - Auth spec conflicts with session spec
    - => [[decision - 2602101400 - chose session tokens over JWT]]
  - 1.2 - Build mode specs overlap
```

### Auto-Selection

When only one option exists, auto-select it:
```
Only one incomplete plan found: [[plan - 2602101030 - add user auth]]

Next action: Implement login endpoint
continue?
```

Don't auto-select for destructive actions or actions with significant side effects.

## Design

The decimal notation gives every item a stable reference.
Users can batch-select across categories.
The [[c - arrow prefix marks inline outcomes that emerged during execution|=>]] convention tracks what was done about each item.

## Verification

- Items are unambiguously referenceable by number
- Batch selection works across categories
- Acted-upon items get wiki links to resulting files

## Interactions

- [[spec - coherence skill - checks spec vs spec for contradictions]] — presents findings as numbered list
- [[spec - drift skill - read only analysis of spec vs code divergence]] — presents findings as numbered list
- [[spec - weave skill - discover missing links and prune stale ones]] — presents suggestions as numbered list
- [[c - arrow prefix marks inline outcomes that emerged during execution]] — acted-upon items use the arrow convention
