---
tldr: Find precise domain names for vaguely referenced concepts
category: core
---

# /eidos:true-name

Establish ubiquitous language — replace vague references with precise, canonical domain names and propagate everywhere.

See [[c - ubiquitous language - shared vocabulary across specs code and conversation]].
When the same concept has three names, nobody is sure they're talking about the same thing.
When it has one true name, communication becomes precise and specs become navigable.

## Usage

```
/eidos:true-name <vague reference or concept>
```

Examples:
- `/eidos:true-name "the thing that tracks plan progress"`
- `/eidos:true-name "that config toggle mechanism"`
- `/eidos:true-name rename phase-gate → phase-checkpoint`

## Instructions

### 1. Understand the Target

Parse the input:
- **Discovery mode** — a vague description or concept that needs naming (e.g., "the thing that X")
- **Rename mode** — an existing name that should be replaced (e.g., "rename X → Y" or "X should be called Y")

If the input is ambiguous, ask: "What are you pointing at?"

### 2. Survey Current Usage (Discovery Mode)

Search for how the concept is currently referenced:

```bash
# In specs — filenames and content
grep -ri '<related terms>' eidos/
grep -ri '<related terms>' memory/

# In code
grep -ri '<related terms>' src/ skills/ scripts/ hooks/

# In recent conversations (session exports)
grep -ri '<related terms>' memory/session\ -\ *.md
```

Collect:
- Every name, description, or reference used for this concept
- Where each appears (file + line)
- Which representations are most common

### 3. Propose a True Name

A true name should be:
- **Domain-native** — uses the language of the problem, not the implementation ("phase" not "step-container")
- **Precise** — names what it *is*, not what it's *near* or what it *does sometimes*
- **Stable** — won't need renaming as the concept evolves
- **Self-evident** — someone unfamiliar can guess the meaning
- **Consistent** — fits the existing naming patterns in the project

Present the proposal:

```
## Current references
- "progress tracker" in spec - planning (3×)
- "status section" in plan template (1×)
- `updateProgress()` in code (2×)

## Proposed true name: `progress-log`

Rationale: It's a log (append-only, timestamped entries), not a tracker
(which implies computed state). "Progress log" matches how it's actually
used in plan files.

Alternatives considered:
- `activity-log` — too generic, doesn't convey plan-specific scope
- `progress-tracker` — implies computed state, but it's just entries

Apply this name? (y / suggest alternative)
```

If the user suggests an alternative, evaluate it against the same criteria and confirm.

### 4. Propagate the Name

Once confirmed, propagate systematically:

**Spec filenames** (if the concept is a spec or claim):
```bash
git mv "eidos/old - name.md" "eidos/new - name.md"
```
Then update all `[[wiki links]]` referencing the old name.

**Spec content:**
- Replace the old term in prose, headings, and TL;DRs
- Check that the claim in the filename still matches content

**Code identifiers** (if applicable and the user confirms):
- Variable names, function names, class names
- Comments referencing the old term

**Plan and memory files:**
- Update references in active plans
- Don't rewrite historical files (sessions, solved) — they're records of what *was*

Commit after each logical unit (filenames, then content, then code).

### 5. Rename Mode

When the input is explicitly "rename X → Y":
- Skip discovery — the user already knows the true name
- Go straight to surveying where X appears
- Show the propagation plan (which files, which references)
- Confirm, then propagate

### 6. Report

```
## True name applied: `progress-log`

Renamed:
- [spec - progress log - ...](<eidos/spec - progress log - ...md>)
  - was: spec - progress tracker - ...

Updated references:
- [plan template](<eidos/template - plan - ...md>) — 2 occurrences
- [planning spec](<eidos/spec - planning - ...md>) — 3 occurrences
- [scripts/progress.py](<scripts/progress.py>) — 1 occurrence

No changes (historical):
- memory/session - ... (3 files reference old name, preserved as-is)
```

## Output

- Renames: spec/claim files via `git mv`
- Updates: wiki links, prose, and optionally code identifiers
- Does not modify: historical memory files (sessions, solved items)
