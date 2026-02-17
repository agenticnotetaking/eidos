---
tldr: AI leaves inline {{AI ...}} annotations in files for the human to review and resolve
---

# Annotate — AI inline feedback for human review

## Target

The human can leave `{{comments}}` for the AI to process via `/eidos:refine`.
The reverse direction is missing: the AI has observations about a file but no lightweight way to leave them inline for the human.

Reports (drift, code-review) are useful but disconnected from context.
Inline annotations let the AI point at the exact spot and say "this seems off" — the human reviews in-place.

## Behaviour

- `/eidos:annotate` reads target files and leaves `{{AI ...}}` comments inline at relevant points
- The scope and focus of annotations is driven by context parameters (see Usage)
- Annotations are suggestions, not directives — the AI has no authority to change content
- Each annotation should be self-contained: a reader shouldn't need to look elsewhere to understand the point
- Annotations are temporary — they exist to be processed and removed, same as `{{comments}}`
- `/eidos:refine` recognises `{{AI ...}}` markers and can process them alongside human `{{comments}}`

## Design

### Marker Syntax

`{{AI` prefix distinguishes AI annotations from human comments:

```markdown
## Behaviour
- Users can export data in CSV format
  {{AI this contradicts the Design section which says JSON only}}

- Response time under 100ms
  {{AI ? where does this target come from — no benchmark or rationale}}
```

GID prefixes work inside `{{AI ...}}` the same way as in `{{...}}`:
- `{{AI ? ...}}` — question
- `{{AI ! ...}}` — important observation
- `{{AI ^ ...}}` — claim/correction
- `{{AI > ...}}` — suggestion

Without a prefix, the annotation is a general observation.

### Processing Flow

```
/eidos:annotate [file(s)] [--focus ...]
  → AI reads file(s)
  → AI analyses based on focus
  → AI inserts {{AI ...}} at relevant points
  → commits annotated file
  → human reviews annotations in-place
  → human can:
    - resolve directly (edit the file)
    - add own {{response}} next to {{AI ...}}
    - run /eidos:refine to process both
```

### Focus Parameters

Annotations without focus risk being noisy.
The `--focus` parameter constrains what the AI looks for:

- `--focus coherence` — contradictions within the file or against linked specs
- `--focus clarity` — vague claims, missing specificity, ambiguous language
- `--focus gaps` — missing sections, uncovered edge cases, absent rationale
- `--focus stale` — claims that may no longer match the codebase
- No focus → AI uses judgement, but should err toward fewer, higher-signal annotations

### Annotation Density

Less is more.
Each annotation should earn its place — if removing it doesn't lose a meaningful observation, remove it.
Target: 3-7 annotations for a typical spec file.
A file with 20 annotations is noise, not feedback.

### Interaction with Refine

`/eidos:refine` already processes `{{comments}}`.
With annotate, refine gains a second marker type:

- `{{comment}}` — human feedback, AI asks questions to resolve
- `{{AI observation}}` — AI feedback, presented to human for decision

During refine, `{{AI ...}}` items are presented differently:
- The AI explains its reasoning (why it flagged this)
- The human decides: agree (AI applies fix), disagree (remove annotation), or discuss

## Interactions

- [[c - spec refine loop uses double curly braces - creates refinement traces and adjusts spec]] — annotate is the reverse direction
- [[spec - gid - semantic symbols for compressed notation]] — GID prefixes work inside `{{AI ...}}`
- [[c - agency in implementation not direction - surface reasoning for human steering]] — annotations are suggestions, human decides

## Mapping

> [[skills/refine/refine.md]]
> [[skills/annotate/annotate.md]]

## Future

{[?] Should annotate work on code files too, or only eidos specs?}
{[?] Could drift/coherence/code-review deposit `{{AI ...}}` annotations instead of (or alongside) reports?}
