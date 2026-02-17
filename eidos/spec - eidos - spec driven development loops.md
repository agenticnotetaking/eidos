---
tldr: Spec-driven development plugin for Claude Code where markdown specs and code are bidirectional representations of the same system
---

# Eidos

Eidos (εἶδος — "ideal form") is a Claude Code plugin that makes markdown specs the source of truth for a project.
Code is a downstream manifestation of the spec.
The relationship is bidirectional:
specs shape code, code can update specs, and conflicts become human decisions.

## Target

Development is driven by intent, but intent gets lost.
It lives in chat messages, commit messages, abandoned docs, and the developer's head.
When an AI assistant starts a new session, it sees code but not the reasoning behind it.

Eidos gives intent a home.
Spec files describe what a system *should* be.
Code is one manifestation of that spec.
When they drift apart, neither automatically wins — the human decides which to update.

The workflow is:
{{please add some lines on why platonic and aristotelian, no context here yet}}
- **Spec → code** (Platonic direction): write what you want, then make it real
- **Code → spec** (Aristotelian direction): extract the implicit spec from existing code
- **Dialectical refinement**: spec meets reality, reality pushes back, spec evolves

## Behaviour

- Eidos specs are the intended source of truth, but may be stale — never blindly trust during conflict resolution
- Code and spec are two representations of the same system, kept in sync bidirectionally
- Conflicts between spec and code become decision prompts for the human
- The human focuses on decisions and intent, not implementation details
- Eidos is a Claude Code plugin, portable to any project via `--plugin-dir`
- `eidos/` (intentional) and `memory/` (procedural) coexist in a project without competing
- Spec files use [[wiki-links]] to form a relationship graph — meaning emerges from connections
- Spec granularity is user-chosen: per feature, per component, per whatever-feels-right — specs merge and split as needed
- `eidos/` allows arbitrary nesting by user choice, no forced structure
- Mapping pointers act as entry points into the source, not as an exhaustive index
- The plugin works incrementally — partial spec coverage is normal, not an error state
- [[c - the spec describes the full vision - versioning is for the procedural plan]]
- [[c - eidos is self contained - definitions do not rely on external systems]]
- [[c - specs emerge from discussions and serve as fixpoints not required reading]]
- [[spec - naming - prefixes structure filenames as prefix claim pairs]]

## Design

### Two Folders, Two Concerns

```
project/
  eidos/       # what it SHOULD be (intentional)
  memory/      # how we got here (procedural)
  src/         # what it IS (implementation)
```

- `eidos/` holds spec files — the ideal form of the system
- `memory/` holds procedural artifacts: plans, decisions, learnings, drift reports, observations
- The plugin creates files in both places depending on the operation:
  - `/eidos:pull` → creates or updates files in `eidos/`
  - `/eidos:drift` → creates report in `memory/`
  - `/eidos:push` → modifies code (and updates spec mappings if new files created)

### Spec File Format

See [[template - spec - sections and conventions for spec files]] for the full template.
Each spec file in `eidos/` follows this structure:

```markdown
---
tldr: Brief description of what this spec covers
---

# [Name]

## Target
What problem this targets, what is the goal.
Not every spec has a clear "problem" — sometimes it exists for aesthetics or other reasons.
Target covers both.

## Behaviour
How it behaves.
Include claims as bullet points here, with wiki links to claim-specs for the significant ones:
- When X happens, [[entering one build mode deactivates all others]]
- The system responds within 200ms
- Nested bullets for detail:
  - Sub-behaviour A
  - Sub-behaviour B

## Design
How it works.
Patterns, architecture, structure.

## Verification
How to verify this works.
Test scenarios, manual checks, acceptance criteria.

## Friction
Known pain points, rough edges, tradeoffs.

## Interactions
How this relates to other parts of the system or artifacts.
- Depends on [[save system]]
- Affects [[undo redo system]]

## Mapping
> [[src/components/BuildMode.tsx]]
> [[src/hooks/useBuildMode.ts]]
(Wiki links in blockquotes. Greppable. Entry points, not exhaustive.)

## Decisions
- [[decision - 2026-02-10-1400 - chose CSG over mesh booleans]]

## Future
{[!] planned item — will be implemented}
{[?] aspirational item — worth investigating}

## Notes
Anything else. Context, gotchas, open questions.
```

Not all sections required.
The format is a starting point — expect iteration.
`{[!]}` and `{[?]}` items can appear anywhere in the file, not just under Future.

### Templates

Many skills produce procedural output files in `memory/`.
Templates in `eidos/` define the structure of these outputs — they are the intentional form of procedural files.
A skill references its template, gathers context, and produces a timestamped file in `memory/` that follows the template's structure.

See [[spec - template - basis for output files]] for the template index and design rationale.

### Claims

Claims are verifiable statements about expected behaviour.
They start as bullet points within sections (especially Behaviour) and graduate to their own spec files when they are pressing enough, pointed enough, or referenced across multiple specs.

A claim as its own file might be named: [[each build mode is independent - entering one deactivates all others]]

These claim-specs can be lightweight — sometimes the name and the backlinks are the full signal.
They may use the spec template, but there's no template enforcement for claims.
They don't need all sections.

Claims serve as:
- **Drift indicators** — check code against each claim
- **Acceptance criteria** — in plans, link to specific claims
- **Review criteria** — code review checks claims
- **Coherence anchors** — cross-spec coherence checks

### Mapping as Entry Points

Mappings use wiki links in blockquote format for greppability:
```
> [[src/components/BuildMode.tsx]]
```

Non-md wiki links require the file ending (e.g., `.tsx`, `.py`).

Mappings are **pointers**, not an exhaustive index.
During normal work, outdated or missing pointers get noticed and updated.
The mechanism for this is still open:
- Automatic update during push/pull operations
- User decision during session
- Noted in procedural files (plan, observation) and surfaced later

{[?] Determine the right mapping update mechanism through usage}

### Inline Markers

Inline markers for things not yet implemented:
- `{[!] description}` — planned, will be done (GID: TODO Priority)
- `{[?] description}` — aspirational, worth investigating (GID: TODO Unsure)

These can appear **anywhere** in a spec file — under Future, inline in Behaviour, in Design, wherever they're relevant.
The Future section is a collecting point for items that don't belong to a specific section.

Extracted by scripts, surfaced at session start, can become plan actions or push targets.
See [[spec - gid - semantic symbols for compressed notation]] for the notation system.

### Technical Code Direction

- `{>> description}` — inline technical hint for implementers

Used when a behaviour or design claim benefits from a code-level nudge:
```markdown
- Ghost preview is semi-transparent (50% opacity)
  - {>> depthWrite off to avoid z-fighting with placed buildings}
```

Not always needed — only when the technical detail encodes a decision or saves implementers from a known pitfall.
Test: could you swap the mechanism for a different one without changing the spec?
If yes, it's mechanism and probably doesn't need a `{>>`.
If no, it encodes a decision and belongs.

See [[c - pull climbs from code to intent not across from code to prose]] for the distinction between intent and mechanism in specs.

### .WIP Mode

A `.WIP` file in `eidos/` signals partial spec coverage.
This adjusts expectations:
- Unmapped code is expected, not flagged as an issue
- Drift reports focus only on what IS specified
- Encourages incremental adoption for existing projects

### Plugin Structure

```
eidos/                          # the plugin repo
  .claude-plugin/
    plugin.json                 # name: "eidos", defines namespace
  eidos/                        # eidos specs for eidos itself (bootstrapping)
  memory/                       # procedural files for eidos development
  skills/
    help/                       # each skill: <name>.md + SKILL.md symlink
    drift/
    pull/
    push/
    sync/
    coherence/
    weave/
    refine/
    plan/
    plan-continue/
    research/
    architecture/
    code-review/
    next/
    reflect/
    todo/
    done/
    info/
    options/
    summary/
    tomd/
    toscript/
    toskill/
    toclaude/
    toeidos/
    config/
  inject/
    core.md                     # always-loaded plugin rules
    feature/
      git-workflow.md           # config: git_workflow
      status-reporting.md       # config: status_reporting
  scripts/
    read_config.sh              # shared config reader (key → value from eidos/.config)
    recent_changes.py           # git-based recent change detection
    orphaned_mappings.py        # find mappings pointing to deleted files (used by drift)
    future_items.py             # extract {!} and {?} items
    outline_eidos.py            # heading extraction with line numbers
    open_comments.py            # find unresolved {{comments}} in eidos files
  hooks/
    hooks.json                  # hook configuration
    session-start.sh            # compose context from snippets + dynamic state
    pre-tool-use-branch-check.sh  # enforce branch rule (config-gated)
  CLAUDE.md                     # project-specific only (plugin rules live in inject/)
```

Skills use the symlink pattern: `help/help.md` is the named file, `help/SKILL.md` is a symlink for Claude Code discovery.
Skills are namespaced via `plugin.json`: `/eidos:drift`, `/eidos:pull`, `/eidos:push`, `/eidos:help`, etc.

### Core Workflow Loops

Two valid patterns, often interleaved:

**Formal loop (inventory-driven):**
```
eidos → drift → plan → code (Platonic: spec shapes code)
code → drift → eidos        (Aristotelian: code reveals spec)
```

**Organic loop (observation-driven):**
```
observe issue in program/artifact
  → adjust eidos file (manually or via chat)
  → commit
  → recent change is now discoverable
  → /eidos:push recent 1
  → code directly for small changes, or into a plan for larger changes
  → code
  → discoveries during implementation
  → discussion in chat
  → adjust eidos based on discoveries
```

During incoherence resolution, eidos is the *intended* source of truth but may be stale.
Neither direction automatically wins — conflicts become decision prompts.
Drift creates procedural files in `memory/` when decisions are needed, presenting them via numbered list for user selection.

### Commands

Each skill has its own spec in `eidos/skills/`:

**Core loop:**
- [[spec - help skill - usage guide listing all eidos skills]]
- [[spec - drift skill - read only analysis of spec vs code divergence]]
- [[spec - pull skill - reverse engineers spec from existing code]]
- [[spec - push skill - implements code to match spec]]
- [[spec - sync skill - bidirectional reconciliation with conflict surfacing]]
- [[spec - coherence skill - checks spec vs spec for contradictions]]
- [[spec - weave skill - discover missing links and prune stale ones]]
- [[spec - refine skill - processes inline comments via structured dialogue]]

**Planning:**
- [[spec - planning - structured intent between spec and code]] — the conceptual mode
- [[spec - plan skill - structured plan for multi step work]]
- [[spec - plan-continue skill - resume work on existing plan]]

**Observation:**
- [[spec - research skill - investigate and document findings with sources]]
- [[spec - architecture skill - snapshot codebase structure and relationships]]
- [[spec - code-review skill - general quality and security analysis]]
- [[spec - next skill - aggregate actionable items across project]]
- [[spec - reflect skill - extract learnings from session or file]]

**Utility:**
- [[spec - todo skill - quick task creation in memory]]
- [[spec - done skill - session end with export and merge]]
- [[spec - info skill - request more context before proceeding]]
- [[spec - options skill - present structured choices for user decision]]
- [[spec - summary skill - generate structured summary of file or session]]
- [[spec - tomd skill - export conversation to markdown]]
- [[spec - toscript skill - export code to script file]]
- [[spec - toskill skill - create new skill from conversation]]
- [[spec - toclaude skill - adjust claude md to steer behaviour]]
- [[spec - toeidos skill - routes insights into specs and claims]]
- [[spec - config - toggleable project settings]]

### Scripts

Python scripts for context gathering and analysis:

- **`recent_changes.py`** — `--days N` or `--commits N`, shows changed files in both eidos/ and code
- **`orphaned_mappings.py`** — find mappings pointing to files that no longer exist (used within drift, not standalone)
- **`future_items.py`** — extract `{[!]}` and `{[?]}` from all eidos files, grouped by file with line numbers
- **`outline_eidos.py`** — heading extraction with line numbers from eidos files
- **`open_comments.py`** — find unresolved `{{comments}}` across eidos files (see [[c - open comment discovery - script to find unresolved refinement comments]])

### Session Hook

On session start:
- Detect `eidos/` folder presence
- If absent: stay silent, don't interfere
- If present, inject context:
  - Recent changes (via `recent_changes.py`)
  - `{!}` planned items (via `future_items.py`)
  - Unresolved `{{comments}}` (via `open_comments.py`)
  - Incomplete plans in `memory/` (unchecked actions)
  - `.WIP` state if present
  - Config settings from `eidos/.config`

### PreToolUse Hook

On Edit/Write of files referenced in spec mappings:
- Surface relevant spec as context (advisory, not blocking — exit 0)
- Helps the AI stay aligned with spec intent during implementation

## Verification

- `/eidos:pull` on existing code produces reasonable spec drafts
- `/eidos:push` from spec produces matching code changes
- `/eidos:drift` on real specs detects actual divergence
- Claim verification checklist is usable and accurate
- Session hook injects useful context without noise
- Plugin installs and namespaces correctly in target projects
- Both workflow loops (formal and organic) feel natural in practice

## Friction

- Bootstrapping: eidos doesn't exist yet, so early spec refinement is manual
- Claims as files may proliferate — need good backlink tooling to navigate
- Mapping staleness: pointers will go stale, mechanism for updating still open
- Context window: large eidos/ folders may overwhelm the AI — scripts must pre-filter

## Interactions

- Coexists with `memory/` — complementary, not competing
- [[c - spec refine loop uses double curly braces - creates refinement traces and adjusts spec]] — the pattern for iterative spec refinement
- Wiki links between specs form a navigable graph of intent

## Mapping

> [[.claude-plugin/plugin.json]]
> [[inject/]]
> [[skills/]]
> [[scripts/]]
> [[hooks/]]
> [[CLAUDE.md]]

## Decisions

(none yet — this is the initial spec)

## Future

{[!] More output templates — decision, drift report, research, goal, session}
{[!] PreToolUse hook — surface relevant spec on Edit/Write of mapped files (advisory, not blocking)}
{[!] State & intent commands: decision, goal — linked to eidos specs}
{[!] Observation & verification commands: observation, research, info}
{[?] Auto-deduction to CLAUDE.md — detect general expectations in specs that should be project-wide rules}
{[?] Design integration — link to images, JSON, or design system references in specs}
{[?] Replace or subsume mono — eidos as the foundation, mono patterns refined on top}

## Research Todos

- [ ] Mine mono's `/drift` and `/consistency` skills in detail — closest patterns to `/eidos:drift` and `/eidos:coherence`
- [ ] Mine mono's session-start hook and scripts — pattern for eidos session hook
- [ ] Look at how VTT features would map to spec files — validate format on a real project
- [ ] Test Claude Code plugin mechanics end-to-end — confirm namespacing, hooks, `${CLAUDE_PLUGIN_ROOT}`
- [ ] Review mono skill patterns broadly — identify gold-standard skills and known issues

## Notes

This spec was created as part of bootstrapping eidos: using eidos's own spec-driven approach to build eidos.
The initial spec files were created manually.
As the tool matures, it will maintain its own specs.
