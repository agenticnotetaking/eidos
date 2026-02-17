---
tldr: Reverse-engineer eidos spec from existing code
category: core
---

# /eidos:pull

Extract the implicit spec from existing code into eidos spec files (Aristotelian direction: code → spec).

## Usage

```
/eidos:pull [file ...]           # pull spec from specific files
/eidos:pull recent [N]           # pull from recently changed code files
/eidos:pull plan [plan-name]     # pull from files changed during a plan
/eidos:pull recursive [target]   # force multi-pass mode: overview first, then plan for subsections
```

## Instructions

### 1. Identify Targets

- **File paths** → use those files directly
- **`recent [N]`** → run `${CLAUDE_PLUGIN_ROOT}/scripts/recent_changes.py --commits N`, use the code files (not eidos/ files)
- **`plan [name]`** → find the plan file in `memory/` (by name match, or most recently completed if no name given), then:
  1. Read the plan's `=>` notes for created/modified files
  2. Use `git log` on the plan's branch (from merge commit or branch name) to find all changed code files
  3. Exclude `memory/`, `eidos/`, and `inject/` files — only pull from implementation code
  4. Present the file list for confirmation before proceeding
- If no args, ask the user what to pull from

### 2. Assess Scope

Before diving in, gauge the breadth of the target:

- **How many files?** — a handful vs dozens
- **How many distinct concerns?** — one feature vs an entire subsystem
- **How deep?** — focused behaviour vs cross-cutting architecture

**Triggers for multi-pass mode** (any of these):
- `recursive` argument was used
- Target spans many files across multiple unrelated concerns
- The scope would produce a spec too broad to be useful as a single document
- The scope is well defined but its still too complex to pull in a single session (e.g. extremely nuanced)

**If multi-pass triggers:**

1. **Overview pull** — skim all targets, produce a high-level pull doc that maps the territory:
   - What are the major subsections/concerns?
   - How do they relate to each other?
   - What existing specs already cover parts of this?
   - The intent sketch stays at overview level — broad strokes, not per-concern detail
2. **Create a plan** via `/eidos:plan` using [[template - plan - structured phases with actions and progress tracking]]
   - File: `memory/plan - <timestamp> - pull subsections for <claim>.md`
   - One action per subsection, each a focused pull of that concern
   - Present the plan to the user for approval
   - Work proceeds via `/eidos:plan-continue`
3. **Stop here** — the overview pull doc and plan are the output. Don't proceed to subsection pulls in the same pass.

**If scope is manageable:** continue to step 3 as normal.

### 3. Check for Existing Specs

For each target file:
1. Search all spec Mapping sections (`> [[...]]`) for references to the target
2. Also search for specs whose name relates to the target's domain

If a matching spec exists, note it — this becomes an update, not a creation.

### 4. Collect — Extract Relevant Code

Read each target file thoroughly.
The goal is to distil what matters — many files may only have a small percentage of relevant code for targeted spec requests (e.g. some behaviour or feature we want to spec may have a footprint in many files in the implementation).

Write the collected material to `memory/pull - <timestamp> - <claim>.md` using [[template - pull - collected code material with intent sketch]].
Only skip the pull file for very simple pulls (one or two focused files, narrow scope) — when in doubt, create the file.

Organise by logical concern, not per-file — one concern often spans multiple files.
The template's sections (Collected Material, Patterns, Dependencies) guide what to extract.

### 5. Climb — Abstract to Intent

Fill in the template's **Intent Sketch** section.
See [[c - pull climbs from code to intent not across from code to prose]].

Each bullet should survive a complete rewrite of the implementation.
The question: "what would someone need to know to re-implement this differently?"

Climbing guidelines for the spec draft:
- **Behaviour claims** should describe what a user experiences, not how the code achieves it
- **Design** should capture decisions, rationale, and visual preferences, not algorithms (unless those are relevant to the previous points in rare cases)
- **Technicals** that encode design decisions can use `{>>` inline hints:
  ```markdown
  - Drag feels responsive even with complex shapes
    - {>> don't rebuild mesh on every pointer event — throttle to once per frame}
  ```
- Pure mechanism (specific API calls, internal variable names) does not belong in the spec

### 6. Draft the Spec

#### New Spec (no existing spec found)

Create a draft following the spec template from [[spec - eidos - spec driven development loops]]:

```markdown
---
tldr: [brief description]
category: core
---

# [Name]

## Target
[Inferred from code analysis]

## Behaviour
- [Extracted claims as bullet points]

## Design
[Patterns and architecture observed]

## Interactions
- [Dependencies and effects]

## Mapping
> [[target-file.ext]]
```

#### Existing Spec Update

Show a diff-style comparison:
- What the spec currently says vs what the code implies
- New claims the code introduces
- Claims the code no longer upholds
- Mapping additions needed

### 7. Present for Decision

#### New Spec

```
Pull complete. Draft spec for [target]:

[show draft]

Options:
1 - Create spec as shown
2 - Adjust before creating
3 - Discard
```

#### Existing Spec Update

```
Pull found differences between code and spec:

[show comparison]

Options:
1 - Update spec to match code
2 - Keep spec as-is (code should be fixed instead → /eidos:push)
3 - Merge selectively
4 - Discard
```

Per [[c - agency in implementation not direction - surface reasoning for human steering]], never auto-update — present reasoning and let the human decide.

### 8. Execute

If approved:
- Write the new spec file to `eidos/` or update the existing one
- Commit

## Output

**Single-pass mode:**
- Working material: `memory/pull - <timestamp> - <claim>.md`
- Creates or updates: spec file(s) in `eidos/`

**Multi-pass mode (recursive):**
- Overview pull doc: `memory/pull - <timestamp> - <claim> overview.md`
- Plan for subsections: `memory/plan - <timestamp> - pull subsections for <claim>.md`
- Subsection pulls and specs are produced later via `/eidos:plan-continue`
