---
tldr: CLAUDE.md as a compact entrypoint — TLDRs and critical rules inline, detail linked via wiki links to specs
---

# Progressive Disclosure — compact entrypoint with linked detail

## Target

The AI reads CLAUDE.md every session.
If it's too long, important rules drown in detail.
If it's too short, the AI misses critical context.
Progressive disclosure solves this: the entrypoint is compact and scannable, with links to full specs for depth.

## Behaviour

- CLAUDE.md is the single file loaded at session start
- Each concern gets a short section: TLDR + critical rules + wiki link to the full spec
- Rules that fit in one line go inline; anything longer links out
- The AI follows wiki links when working in a relevant area, not upfront
- This keeps the context window focused on what matters now

## Design

### Structure Pattern

Each section in CLAUDE.md follows:

```markdown
## [Concern]

[One-paragraph TLDR or inline rules]
See [[spec - concern - full claim]] for detail.
```

For critical rules that must always be followed:

```markdown
## Critical: [Rule]

[The rule, stated completely in 1-3 lines]
```

Critical rules are inline because they can't be missed.
Everything else links out.

### What Goes Inline vs Linked

**Inline (in CLAUDE.md):**
- Hard rules with no exceptions (always do X, never do Y)
- Identity statements (what the project is)
- The skill inventory (scannable list)

**Linked (in specs):**
- How rules work in detail
- Design rationale
- Examples and edge cases
- Verification criteria

### Session Start Flow

1. AI reads CLAUDE.md (automatic)
2. AI has enough context to begin working
3. When touching a specific area, AI follows the wiki link to the relevant spec
4. Spec provides full detail for that area

## Verification

- CLAUDE.md is readable in under 2 minutes
- No critical rule requires following a link to understand
- Every spec is reachable from CLAUDE.md within one link
- AI behaviour doesn't degrade when specs aren't read upfront

## Interactions

- [[spec - eidos - spec driven development loops]] — CLAUDE.md is part of the plugin structure
- [[spec - config - toggleable project settings]] — config may affect which sections appear
