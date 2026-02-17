---
tldr: Reverse-engineer eidos specs from existing code (Aristotelian direction)
---

# /eidos:pull

## Target

Existing code embeds implicit specs — patterns, contracts, behaviours — that aren't written down. Pull extracts these into eidos spec files, bringing code-first knowledge into the intentional layer.

## Behaviour

- Args: file paths, query, `recent [N]`, `plan [name]`, `recursive [target]`
- Analyzes target code: structure, patterns, implicit contracts, naming conventions
- If spec exists (found via mapping search):
  - Presents diff between existing spec and what code implies
  - Decision prompt: update spec, keep spec, or merge
- If no spec exists:
  - Creates new spec using the template
  - Presents draft to user before writing
- Auto-populates: Target (inferred), Behaviour with claims (extracted), Design (patterns), Mapping
- Created specs go in `eidos/`
- If scope is too broad (many files, multiple unrelated concerns, or `recursive` argument): does an overview pull first, then creates a plan for subsection pulls
- Multi-pass mode produces an overview pull doc and a plan — subsection pulls happen later via `/eidos:plan-continue`

## Design

Pull is the Aristotelian direction: discovering the form by examining its instances.

### Scope escalation

When the target is too broad for a single pull pass, the skill escalates to multi-pass mode:
overview first, then a plan for subsection pulls.
This avoids producing a single spec too broad to be useful, and avoids context exhaustion on complex targets.

Triggers: `recursive` argument, many files across unrelated concerns, scope too broad for one spec, or scope well-defined but too nuanced for one session.
The plan follows [[template - plan - structured phases with actions and progress tracking]] and work continues via `/eidos:plan-continue`.

### Climb, don't translate

Pull must climb *up* from code to intent, not translate *across* from code to prose.
See [[c - pull climbs from code to intent not across from code to prose]].

Describing what the code does is `/eidos:architecture`'s job (descriptive, horizontal).
Pull's job is extracting what the system *should* do — the intent that the code is one possible implementation of.

The question pull answers: "what would someone need to know to re-implement this differently?"
Not: "what does this code do?"

### Two-phase approach

1. **Collect** — targeted read of the relevant files.
   Extract the bits that matter, filter noise.
   Many files may only have a small percentage of relevant code for the question at hand — collecting distils this.
   Produces a working artifact: `memory/pull - <timestamp> - <claim>.md`.
   Only skip the pull file for very simple pulls (one or two focused files, narrow scope).
   See [[c - default to action and frame exceptions as opt outs]].
2. **Climb** — from collected material, abstract up to intent.
   What behaviour does this code serve?
   What design decisions does it encode?
   Produce the spec.

### Technicals in output

Specs are primarily behaviour and design — not implementation detail.
But technicals that encode design decisions belong.
Technicals that are pure mechanism don't.

When a behaviour claim benefits from a code-level hint, use `{>>` inline:
```markdown
- Drag feels responsive even with complex shapes
  - {>> don't rebuild mesh on every pointer event — throttle to once per frame}
```

### Other

The `recent [N]` argument uses `recent_changes.py` to find recently changed code files as pull targets.
This supports the organic workflow: code changes happened, now pull the implicit spec updates.

The `plan` argument reads a completed plan's `=>` notes and git history to find implementation files changed during that plan.
This supports the end-of-plan workflow: plan is done, now capture what was built as specs.
Excludes `memory/`, `eidos/`, and `inject/` — only implementation code is pulled.

When a spec already exists, pull does NOT auto-overwrite.
It shows what the code implies vs what the spec says, and the human decides.
This respects the principle that neither code nor spec automatically wins.

{[?] How much context should pull gather — just the target files, or also their imports and callers?}
{[?] Should pull detect which existing spec a file maps to, or require the user to specify?}

## Verification

- Pulling on well-structured code produces a readable, accurate draft spec
- Pulling on code with an existing spec surfaces meaningful differences
- The decision prompt is clear about what would change
- `recent` argument correctly scopes to recently changed files
- `recursive` argument triggers multi-pass mode: overview pull + plan for subsections
- Auto-detected broad scope triggers the same escalation without explicit `recursive`

## Interactions

- Inverse of [[spec - push skill - implements code to match spec]]
- [[spec - drift skill - read only analysis of spec vs code divergence]] often precedes pull — drift identifies what needs pulling
- [[spec - sync skill - bidirectional reconciliation with conflict surfacing]] combines pull and push in one pass

## Mapping

> [[skills/pull/pull.md]]
> [[scripts/recent_changes.py]]
