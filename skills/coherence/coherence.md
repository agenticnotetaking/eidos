---
tldr: Check specs against each other for contradictions
category: core
---

# /eidos:coherence

Detect contradictions, orphaned links, and missing cross-references across the spec graph.
Drift checks spec vs code — coherence checks spec vs spec.

## Usage

```
/eidos:coherence
```

## Instructions

### 1. Gather All Specs

Read all `*.md` files in `eidos/`.
For each, extract:
- Claims from Behaviour sections (bullet points)
- Wiki links (all `[[...]]` references)
- Design patterns and architectural statements
- Interaction declarations

### 2. Check for Contradictions

Compare claims across specs:
- Does spec A say X while spec B says not-X?
- Do two specs define the same concept differently?
- Do interaction sections declare conflicting dependencies?

Flag anything that looks contradictory — false positives are acceptable, missed contradictions are not.
The human decides what's actually contradictory.

### 3. Check Wiki Links

For each `[[wiki-link]]` found:
1. Resolve to a file — does it exist?
2. If it points to another spec, does that spec reference back where expected?
3. Flag orphaned links (point to nothing) and one-directional references between specs that should be bidirectional

### 4. Check for Missing Cross-References

If specs A, B, and C all relate to the same domain (similar claims, overlapping mappings, shared terminology):
- Do they link to each other in their Interactions sections?
- Flag cases where related specs don't acknowledge each other

### 5. Detect CLAUDE.md Candidates

Look for claims that are general enough to be project-wide rules:
- Claims repeated across multiple specs
- Constraints that apply to all code, not just one feature
- Patterns that should be enforced globally

Suggest these as additions to CLAUDE.md.

### 6. Compile Report

Create `memory/coherence - <timestamp> - <claim>.md`:

```markdown
---
tldr: Coherence report — [scope description]
category: core
---

# Coherence: [scope description]

## Contradictions

- [spec A] claims X, [spec B] claims Y — these conflict because [reason]

## Orphaned Links

- [[target]] in [spec file:line] — file not found

## Missing Cross-References

- [spec A] and [spec B] both address [topic] but don't link to each other

## CLAUDE.md Candidates

- "[claim text]" appears in N specs — consider as project-wide rule

## Summary

- N specs analysed
- X contradictions found
- Y orphaned links
- Z missing cross-references
```

### 7. Present

Commit the coherence report.
Present findings via [[spec - numbered lists - structured selectable output]]:

```
Coherence check complete. N specs analysed.

1 - Contradiction: [spec A] vs [spec B] on [topic]
2 - Orphaned: [[link]] in [spec]
3 - Missing ref: [spec A] ↔ [spec B]
4 - CLAUDE.md candidate: "[claim]"

Which items to resolve?
```

For contradictions: open both specs and facilitate the user's decision.
For orphaned links: suggest fix (rename, remove, or create target).
For missing refs: suggest adding Interactions entries.

### 8. Resolve

Items can be worked through step by step — in-session or across sessions.
Append one of these at the end of each section:

- `**Resolved:**` — finding was fixed
- `**Rejected:**` — finding is not actually a problem (with reason)
- `**Deferred:**` — acknowledged but not acting now (with reason)

Never replace or remove the original finding — it's the record of what was detected.

```markdown
### 3. Some finding

[original finding text stays exactly as written]

**Resolved:** Fixed by updating X in commit abc1234.
```

The coherence report doubles as a working document and a historical record.
Use `/eidos:process` to work through findings systematically, or resolve items ad hoc.

## Output

- Creates: `memory/coherence - <timestamp> - <claim>.md`
- Read-only — never modifies specs automatically (the report itself is updated with resolutions)
