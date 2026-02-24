---
tldr: File naming conventions using prefix-claim pairs with compact timestamps for procedural files
---

# Naming — prefixes structure filenames as prefix claim pairs

## Target

Files need to be discoverable by both humans and tools. The filename itself should communicate what the file is (prefix) and what it says (claim). When browsing a directory or reading a wiki link, the name should be enough to decide whether to open it.

## Behaviour

### General Pattern

All files follow: `<prefix> - <claim>.md`

- The prefix identifies what kind of file it is
- The claim is prose — a readable phrase capturing the main content
- Claims can be used directly in sentences when wiki-linked: "as stated in [[c - the spec describes the full vision - versioning is for the procedural plan]]"

Non-markdown files (images, diagrams) use the same pattern with their actual extension: `<prefix> - <yymmddhhmm> - <claim>.<ext>`
Wiki links to non-markdown files must include the extension: `[[observation - 2602242119 - layout bug on mobile.png]]`
See [[c - observation images persist visual context as named files]].

### Spec Files (intentional, in `eidos/`)

Spec files use `spec` as prefix, with an optional name segment:

```
spec - <claim>.md
spec - <name> - <claim>.md
```

The name segment groups related specs (e.g., skill names):

```
spec - drift - read only analysis of spec vs code divergence.md
spec - push - implements code to match spec.md
spec - naming - prefixes structure filenames as prefix claim pairs.md
```

Without name segment — for standalone specs:

```
spec refine loop uses double curly braces - creates refinement traces and adjusts spec.md
```

{[?] Should standalone specs still use the `spec -` prefix, or is the claim enough? Current practice is mixed.}

### Template Files (intentional, in `eidos/`)

Templates define the structure of procedural output files.
They use `template` as prefix with a name segment identifying what they template:

```
template - plan - structured phases with actions and progress tracking.md
template - decision - options and rationale for architectural choices.md
```

Templates are referenced by skills that produce procedural output.
See [[spec - template - basis for output files]] for the index and design rationale.

### Reference Files (intentional, in `eidos/`)

Reference docs capture external knowledge the project relies on but doesn't own.
They use `reference` as prefix:

```
reference - <claim>.md
```

Examples:

```
reference - DDD ubiquitous language grounds shared vocabulary.md
reference - Claude Code hooks execute shell commands on tool events.md
```

No timestamp — reference docs are stable, curated knowledge, not point-in-time snapshots.
See [[template - reference - curated external knowledge for project use]] for structure.

### Claim Files (intentional, in `eidos/`)

Claims that graduate to their own files use `c` as prefix:

```
c - the spec describes the full vision - versioning is for the procedural plan.md
c - eidos is self contained - definitions do not rely on external systems.md
c - each build mode is independent - entering one deactivates all others.md
```

The `c -` prefix identifies the file as a standalone claim.
Sometimes the name and the backlinks are the full signal.

### Procedural Files (in `memory/`)

Procedural files use a compact timestamp: `<prefix> - yymmddhhmm - <claim>.md`

```
refinement - 2602101418 - refine loop spec comment processing.md
drift - 2602101500 - building system divergence.md
solved - 2602122314 - document gid notation system.md
decision - 2602101400 - chose CSG over mesh booleans.md
```

Compact timestamp format: `yymmddhhmm` (10 digits, no separators)
- `26` = year, `02` = month, `10` = day, `14` = hour, `18` = minute
- Sorts chronologically in file browsers
- Shorter than `yyyy-mm-dd-hhmm` while remaining unambiguous

Procedural prefixes (timestamped):

- `architecture` — `/eidos:architecture` — `architecture - 2602141030 - full codebase snapshot.md`
- `brainstorm` — `/eidos:brainstorm` — `brainstorm - 2602101400 - alternative auth approaches.md`
- `bug` — manual — `bug - 2602101500 - login fails on expired token.md`
- `codereview` — `/eidos:code-review` — `codereview - 2602141030 - 2 critical issues in auth module.md`
- `coherence` — `/eidos:coherence` — `coherence - 2602101500 - spec graph contradictions.md`
- `decision` — `/eidos:decision` — `decision - 2602101400 - chose CSG over mesh booleans.md`
- `drift` — `/eidos:drift` — `drift - 2602101500 - building system divergence.md`
- `experiment` — `/eidos:experiment` — `experiment - 2602141030 - iterating on drag feel.md`
- `goal` — manual — `goal - 2602101400 - ship v1 by end of month.md`
- `goodjob` — `/eidos:goodjob` — `goodjob - 2602141030 - well chosen auth framing.md`
- `incoherence` — `/eidos:reflect` — `incoherence - 2602101500 - auth spec contradicts session spec.md`
- `learning` — `/eidos:reflect` — `learning - 2602101500 - rate limiting belongs in middleware.md`
- `meta` — `/eidos:meta` — `meta - 2602141030 - pull output abstraction level.md`
- `next` — `/eidos:next` — `next - 2602141030 - aggregated actionable items.md`
- `observation` — manual — `observation - 2602101500 - users confused by settings page.md`
- `pickmeup` — `/eidos:pickmeup` — `pickmeup - 2602141030 - last 3 days activity.md`
- `plan` — `/eidos:plan` — `plan - 2602101614 - migrate to new auth system.md`
- `proposal` — manual — `proposal - 2602101400 - switch to event sourcing.md`
- `pull` — `/eidos:pull` — `pull - 2602101418 - extracted spec from auth module.md`
- `push` — `/eidos:push` — `push - 2602101500 - implement auth spec claims.md`
- `reflect` — `/eidos:reflect` — `reflect - 2602141030 - session learnings snapshot.md`
- `refinement` — `/eidos:refine` — `refinement - 2602101418 - refine loop spec comment processing.md`
- `research` — `/eidos:research` — `research - 2602101400 - comparing auth token strategies.md`
- `review` — manual — `review - 2602101500 - sprint retrospective findings.md`
- `session` — `/eidos:tomd` — `session - 2602141030 - auth implementation session.md`
- `solved` — renamed `todo` — `solved - 2602122314 - document gid notation system.md`
- `summary` — `/eidos:summary` — `summary - 2602141030 - auth module overview.md`
- `sync` — `/eidos:sync` — `sync - 2602141030 - reconciled auth specs and code.md`
- `todo` — `/eidos:todo` — `todo - 2602101400 - audit error handling consistency.md`
- `weave` — `/eidos:weave` — `weave - 2602141030 - suggested links.md`

Non-timestamped prefixes (in `memory/`): idea, problem, question

`solved` is a renamed `todo` — when a todo is complete, rename from `todo -` to `solved -` (preserving timestamp and claim).

### Nesting

`eidos/` allows arbitrary nesting by user choice:

```
eidos/
  eidos.md
  skills/
    spec - drift - read only analysis of spec vs code divergence.md
    spec - push - implements code to match spec.md
  building/
    spec - building tools - csg based construction.md
    each build mode is independent - entering one deactivates all others.md
```

`memory/` is flat — no nesting.

## Design

### Why Prose Claims

When claims are written as prose, they can be:
- Used directly in sentences when wiki-linking
- Understood at a glance without opening the file
- Linked naturally: "as described in [[spec - drift skill - read only analysis of spec vs code divergence]]"

Avoid keyword-style names:
- Good: `spec - drift - read only analysis of spec vs code divergence.md`
- Avoid: `spec - drift - overview.md`

### Why Compact Timestamps

Procedural files are point-in-time snapshots. The timestamp in the name:
- Provides chronological sorting in file browsers
- Makes each file unique even with similar claims
- Is derivable from git, but convenient to have in the name for human browsing

The compact `yymmddhhmm` format saves characters while remaining readable with practice (use bash `date` to get the actual date).

### Wiki Link Implications

Since filenames ARE wiki links, renaming a file breaks links. See the rename workflow in CLAUDE.md.

## Verification

- All files follow the prefix-claim pattern
- Spec files in eidos/ use `spec -` prefix or bare claim names
- Procedural files in memory/ use compact timestamps
- Wiki links match filenames exactly

## Interactions

- [[spec - eidos - spec driven development loops]] — naming applies to all files in both eidos/ and memory/
- [[c - eidos is self contained - definitions do not rely on external systems]] — naming conventions are defined here, not inherited from external systems
