---
tldr: Generate a manim explainer video through staged research → outline → scenes → code → render → merge, with the outline doubling as a plan/state document
category: utility
---

# /eidos:video

Turn a topic (or a folder of wiki-linked md) into a rendered manim video through a fixed pipeline.
Pauses after each stage for review by default.
Outline doubles as the plan/state document — wiki-linked checklist tracks progress.

Full design in [[spec - video skill - outline driven manim pipeline from topic to merged render]].

## Usage

```
/eidos:video [topic]              # start a new video project (topic = string, md file, or folder)
/eidos:video [topic] --auto       # run the full pipeline without review pauses
/eidos:video                      # resume the in-progress project in cwd
```

## Instructions

### Mode Detection

Parse flags from ARGUMENTS first: `--auto` sets autonomous mode for the rest of the run.

Decide mode from the remaining args and cwd:

| Remaining args                          | cwd state                           | Mode   | Target folder      |
| --------------------------------------- | ----------------------------------- | ------ | ------------------ |
| Path to a folder containing `outline.md` | —                                   | Resume | that folder        |
| Path to a file (.md)                     | —                                   | Start  | new under cwd      |
| A plain string (topic)                   | cwd has no `outline.md`             | Start  | new under cwd      |
| A plain string (topic)                   | cwd **is** a project (`outline.md`) | Resume | cwd, topic ignored, warn user |
| No args                                  | cwd has `outline.md`                | Resume | cwd                |
| No args                                  | cwd has no `outline.md`             | Error — needs a topic or an existing project |

In Resume Mode, verify the outline has either a `## Pipeline status` block (colocated format) or a legacy `## Stages` block by running `scripts/video_state.py <folder>`. If the script reports "no recognized stage structure", fall back to Start Mode and log why.

---

### Prereq Check

Before either mode, verify the environment can actually render.
Run these two checks in parallel:

```bash
command -v manim >/dev/null && manim --version 2>&1 | head -1
command -v ffmpeg >/dev/null && ffmpeg -version 2>&1 | head -1
```

**If `manim` is missing:**
- Ask the user (via AskUserQuestion) whether to install it
- Options: `Install with pip` / `Install with uv` (if `uv` is on PATH) / `Abort`
- On install, run the chosen command (`pip install manim` or `uv pip install manim`)
- Confirm by re-running `manim --version`
- If the user aborts, stop the skill with a clear message

**If `ffmpeg` is missing:**
- ffmpeg is system-level, not pip-installable — don't auto-install
- Show a short hint per platform: `brew install ffmpeg` (macOS), `apt install ffmpeg` (Debian/Ubuntu), `choco install ffmpeg` (Windows)
- Stop the skill with a clear message asking the user to install it and re-run

If both are present, continue to Start Mode or Resume Mode.

---

### Start Mode

1. **Create project folder** under `<cwd>/<video-name>/` with the layout:
   ```
   <video-name>/
     outline.md
     research/
     scenes/
     code/
     renders/
     final.mp4           # filled at merge
     final.srt           # filled at merge
   ```
   `<video-name>` follows the naming convention — prefix-claim, kebab-cased.
2. **Run the pipeline** — see Stages below.

---

### Resume Mode

1. Read `outline.md` in the detected project folder.
2. Invoke `scripts/video_state.py` to locate the first unchecked stage and summarise progress.
3. Resume from that stage.

---

### Stages

Run in order. After each stage completes:

1. **Update the outline's checkbox** — flip `[ ]` to `[x]` for the stage that just finished and append a wiki-link to the artifact on that line. Global stages (Research, Outline, Merge) update the top-level `## Pipeline status` block; per-scene stages (md, code, render) update the inline triplet under the scene's bullet in the relevant section.
2. **Report** — one-sentence summary of what was produced (filenames, counts)
3. **Pause for review** (unless `--auto`):
   - Present the primary artifact(s) — either surface the file paths or read them inline if small
   - If any `{{comments}}` exist in the artifacts, list them with locations
   - Wait for the user to give input (see Feedback Modes)
4. **Continue** — proceed to the next stage on `continue` / explicit go-ahead / any equivalent acknowledgment; otherwise apply the user's feedback and re-present the artifact before continuing

**1. Research** — collect background material

Interpret the topic argument:
- **Plain string** (e.g. `gradient descent`) — no sources yet; default into clarifying questions and WebSearch
- **Path to an md file** — read it, follow `[[wiki-links]]` transitively within the same folder; these are the primary sources
- **Path to a folder** — treat every md in the folder (and its wiki-linked neighbours) as sources

Before searching the web, check for prior coverage:
- If the cwd is inside an eidos-managed project (`eidos/` or `memory/` directories above), grep those for the topic and read any hits

Ask 1–2 focused clarifying questions only when the topic is broad and the sources are thin. Skip when the user has clearly stated scope in the invocation or in provided md.

Emit notes into `<project>/research/*.md` — one file per coherent sub-topic, each with a `tldr` and a short body.
Use `<project>/research/summary.md` when all findings fit in one document.

Skip the research stage entirely when user-provided md already covers the topic — note "skipped: sources complete" in the outline's Research checkbox.

**2. Outline** — write `<project>/outline.md`

The outline is both the script blueprint and the pipeline state document. Global one-shot stages (Research, Outline, Merge) live in a `## Pipeline status` block near the top. Per-scene stages (md, code, render) live **inline** under each scene, colocated with the section that describes it.

Structure:

```markdown
---
tldr: One-sentence description of what this video covers
status: active
---

# <Video Title>

Short opening paragraph — why this video, who it's for, what they'll come away with.

## TLDR

One-paragraph summary of the full narrative arc.

## Pipeline status

- [ ] Research
- [ ] Outline
- [ ] Merge

(Scene-level progress is inline under each section below.)

## Sections

### 1. <Section name>

- **About:** what this section is about
- **Key points:** what must be conveyed
- **Scenes:**
  - [[scenes/01-<slug>]]
    - [ ] md
    - [ ] code
    - [ ] render

### 2. <Section name>

- **About:** ...
- **Scenes:**
  - [[scenes/02-<slug>]]
    - [ ] md
    - [ ] code
    - [ ] render
  - [[scenes/02b-<slug>]]
    - [ ] md
    - [ ] code
    - [ ] render
```

Multiple scenes per section are natural — list them as sibling bullets under `**Scenes:**`.

As each stage completes, flip its `[ ]` to `[x]` and append a wiki-link to the produced artifact on that line (e.g. `- [x] render → [[renders/01-<slug>.mp4]]`). `scripts/video_state.py` parses both the global pipeline block and the per-scene triplets and reports the first unchecked stage in doc order (Research → Outline → all scenes in section order, each as md → code → render → Merge).

**3. Scenes** — write `<project>/scenes/NN-<slug>.md` per scene

One scene md per scene, numbered sequentially (`01-`, `02-`, ...). Derive the slug from the scene's purpose (e.g. `01-intro`, `02-gradient-field`, `03-descent-step`).

Scene md template:

```markdown
---
tldr: One-sentence description of what this scene shows
---

# <Scene Title>

## About

One or two sentences on the scene's purpose and how it fits the narrative.

## Continuity

_Optional — include when this scene reuses visual elements from the previous scene, so the cut between them is seamless._

- From: [[scenes/NN-previous-slug]]
- Carries over (final state from previous scene):
  - Title "<text>" (top edge)
  - Axes at <layout description>
  - Curve in <color>, full opacity
  - Dot at x = <value>, yellow, with label `<label>`

Omit this section for standalone scenes — they start with a fresh canvas and entrance animations.

## On-screen text

Verbatim text that appears on screen (headings, labels, equations, captions).

## Visuals

Elements and layout — axes, objects, their positions and relationships.

## Animations

Entrances, transitions, highlights, what moves and when.

## Style

Colors, font sizes, pacing notes. Omit when defaults are fine.

## Subtitles

- `0.0s`: First line of narration subtitle
- `3.5s`: Second line
- `7.0s`: Third line

Subtitles drive the emitted `.srt` and the frame-sampling positions used for visual review. Each line's timing is the start; the end is the next line's start (or scene end for the last line).

## Duration

Approximate target length in seconds.
```

Descriptions may be precise or vague — codegen fills in tasteful defaults where scene md is silent.

Wiki-link each scene from the relevant outline section under its **Scenes:** bullet (see Outline stage for the exact inline structure).

**4. Code** — write `<project>/code/NN-<slug>.py` per scene

ManimCE conventions:
- `from manim import *` at the top
- One `Scene` subclass per file (1:1:1 mapping: scene md → py file → Scene class)
- Class name is derived from the scene's slug, camel-cased (e.g. `01-gradient-field.md` → `class GradientField(Scene)`)
- Use `construct(self)` as the animation entry point
- Prefer idioms that render reliably: `Text`, `MathTex`, `Axes`, `Arrow`, `Circle`, `Square`, `VGroup`, `Create`, `Write`, `FadeIn`, `Transform`, `ReplacementTransform`
- Use `self.wait(n)` to hold frames; match total timing roughly to the scene's declared duration
- Default to a dark background (ManimCE default)

Translate the scene md into code:
- **On-screen text** → `Text` / `MathTex` mobjects with `self.play(Write(...))` or `FadeIn`
- **Visuals** → positioned shapes and `Axes`; layout via `.to_edge`, `.next_to`, `.shift`, `.move_to`
- **Animations** → `self.play(...)` with `run_time=` matched to subtitle spacing when possible
- **Subtitles** → NOT rendered inside the video (subtitles live in the emitted `.srt`). The scene's on-screen text is separate from subtitles.
- **Style** → apply color/scale/font where declared; otherwise pick tasteful defaults

**Match declared duration.** Manim renders for however long `self.play(...)` + `self.wait(...)` calls add up to — not for the declared scene duration. After all animations, add a trailing `self.wait(...)` so total runtime ≥ the scene md's `## Duration`. Budget with a few tenths of a second of slack; under-running is worse than over-running because subtitles declared past the end get truncated.

**Frame bounds.** Manim's default frame is 14.22 wide × 8.00 tall. Wide horizontal layouts with labels on both sides (`topic → [boxes] → final.mp4`) can run past the edges. Mitigations:
- Scale the group down: `group.scale(0.85)` or tighter
- Tighten `buff` on `VGroup.arrange(...)` and `.next_to(...)`
- Use shorter labels, or stack side labels above/below instead of left/right
- For any layout wider than ~12 units, explicitly verify extremes (leftmost and rightmost mobjects) sit inside `[-7, 7]` via `.get_left().x` / `.get_right().x`

**Subtitle safe zone.** Burned-in subtitles in the merged `final-sub.mp4` sit at the bottom of the frame. Reserve **the bottom ~1.2 units** (y from -4.0 to -2.8) as empty space — no titles, labels, footers, or diagram elements there. Anything placed with `.to_edge(DOWN, buff=0.4)` or smaller will be overwritten by subtitles. Use `.to_edge(DOWN, buff=1.4)` or larger for any text intended to remain visible, and avoid shifting visual groups below y ≈ -2.8.

**Layout symmetry.** When side-by-side groups flank a divider or central element, verify both groups have comparable breathing room to the divider. `VGroup.arrange(DOWN, aligned_edge=LEFT)` anchors the group's bounding-box center but leaves the anchored edge at an asymmetric position relative to other objects. Prefer `.move_to(<point>, aligned_edge=<edge>)` to pin the inside edge of each group at a known offset from the divider, producing matching gaps on both sides.

**Continuity.** When a scene's md declares a `## Continuity` section, its rendered first frame must match the previous scene's rendered last frame so the ffmpeg concat cut is invisible. Pattern:

- Extract shared construction into `<project>/code/_shared.py` — a module of pure constructor functions (`build_title()`, `build_axes()`, `build_curve(axes, color=BLUE_B, opacity=1.0)`, plus any math functions like `f(x)`, `fprime(x)`). Constructors must be deterministic (no unseeded RNG, no timestamps) so both scenes produce pixel-identical output.
- Each scene that declares continuity imports from `_shared` and constructs the carried elements in `construct()`. Then — before any `self.play(...)` — calls `self.add(...)` to place them on frame 0 at their final state from the previous scene:

  ```python
  from manim import *
  from _shared import build_title, build_axes, build_curve, f

  class GradientArrow(Scene):
      def construct(self):
          # carried from the previous scene — no animation, placed on frame 0
          title = build_title()
          axes = build_axes()
          curve = build_curve(axes)
          x0 = -2
          dot = Dot(axes.c2p(x0, f(x0)), radius=0.09, color=YELLOW)
          dot_label = MathTex("x_0", font_size=32, color=YELLOW).next_to(dot, LEFT, buff=0.15)
          self.add(title, axes, curve, dot, dot_label)

          # new animations for this scene begin here
          self.play(GrowArrow(grad_arrow), ...)
  ```

- Update the previous scene's code **alongside** the new one if needed: the previous scene must also use the `_shared` constructors (with the same end-state parameters) so both renders converge to the same pixels. If scene N doesn't already use `_shared`, refactor it as part of generating scene N+1's code.
- **Staleness rule.** Any change to scene N's md or code invalidates the code of every downstream scene declaring continuity from N. Re-run Code (and Render) for the invalidated chain. Treat this the same way as any mid-pipeline feedback that requires downstream re-work.
- **Scenes without continuity** use the standard fresh-start pattern (entrance animations, empty first frame) — no `_shared.py` involvement. `_shared.py` is only created when at least one scene declares continuity.

If scene md is vague, fill in defaults that match the declared **Duration** and **Key points** of the parent outline section.

**5. Render** — produce `<project>/renders/NN-<slug>.mp4` + `.srt` per scene

For each scene, in order:

1. **Render the mp4.** Invoke ManimCE, then move the output into the flat `renders/` layout:

   ```bash
   manim render -ql --media_dir <project>/renders --output_file NN-<slug>.mp4 \
       <project>/code/NN-<slug>.py <ClassName>
   mv <project>/renders/videos/NN-<slug>/*/NN-<slug>.mp4 <project>/renders/NN-<slug>.mp4
   ```

   After all scenes are rendered, clean up manim's scaffolding:
   ```bash
   rm -rf <project>/renders/videos <project>/renders/images <project>/renders/texts
   ```

   Use `-qm` or `-qh` for final verification runs; `-ql` (low quality) during initial iteration.

2. **Measure actual duration.** Read the rendered mp4's duration with `ffprobe` — it won't exactly match the scene md's declared duration:
   ```bash
   ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 <project>/renders/NN-<slug>.mp4
   ```

3. **Emit subtitles, clamped to actual duration.** From the scene md's **Subtitles** section, write `<project>/renders/NN-<slug>.srt`. Each subtitle line's start is taken from the scene md; its end is the next line's start (or the actual scene duration for the last line). **Clamp every subtitle end to `min(declared_end, actual_duration)`** and drop any subtitle whose start is ≥ the actual duration. This prevents overlap at scene boundaries in the merged `final.srt`.

4. **Extract frames for visual review.**

   ```bash
   python scripts/video_frames.py \
       <project>/renders/NN-<slug>.mp4 \
       <project>/renders/frames/NN-<slug>/
   ```

   The script auto-picks up:
   - The sibling `.srt` for subtitle-aware sampling.
   - Manim's `partial_movie_files/<ClassName>/` dir for **animation-boundary sampling** — one frame per resting state between animations. This catches layout and overlap issues that subtitle-time sampling alone misses (the scene's final composed state appears well before the scene ends, but asymmetric spacing or elements introduced mid-animation are only visible at the right boundary). Do not delete `renders/videos/` per-scene — the cleanup at line 293 only runs after all scenes have had their frames extracted.

5. **Review the frames.** Read **every** extracted frame, not just the end-of-scene frame. For each, check:
   - Is the on-screen text from the scene md present and legible?
   - Are the declared visual elements present and in frame?
   - Does the layout match the scene description — **including symmetry and breathing room**? Columns should have comparable margins to any dividers or edges; side-by-side groups should not crowd each other while the opposite side has slack.
   - Are there obvious glitches — cut-off objects, overlapping text, elements off-screen?
   - Does any frame show an element that appears at a bad position mid-build (e.g., a label that lands before its anchor moves into place)?

6. **Iterate on failure.** Both render errors (non-zero exit / manim stderr) and visual-review issues count toward the same retry budget (default: 3 per scene).
   - Diagnose the cause, patch the py file, re-run from step 1
   - On retry, re-run ffprobe (step 2), re-emit srt (step 3), re-extract frames (step 4), re-review (step 5)
   - On retry-budget exhaustion, pause even when `--auto` is set, and present:
     - The last error output (stderr text) **or** the flagged frame with a short explanation of what failed
     - The last attempted fix (diff of the py file's most recent patch)
     - A concrete choice to the user via options:
       - `Edit manually` — user edits the py file directly in their editor, says `continue` to re-render once
       - `Retry anyway` — one more attempt past the bound (useful when a fix was nearly right)
       - `Skip the scene` — exclude this scene from the merge; note the skip in the outline's Render checkbox with a `{[?]}` marker
       - `Accept as-is` — keep the last successful render (or the current broken render if there is no successful prior), move on

After **each scene** renders successfully, update the outline's per-scene inline triplet: flip `- [ ] render` to `- [x] render → [[renders/NN-<slug>.mp4]]` under that scene's bullet. Same pattern for the `md` and `code` stages when they complete. There is no flat `## Stages` block to update in the colocated format — the per-scene triplets are the state. Use `scripts/video_state.py` to verify the next unchecked stage is what you expect before and after each update.

**6. Merge** — produce `<project>/final.mp4` + `<project>/final.srt`

Invoke the merge script:

```bash
python scripts/video_merge.py <project>
```

- ffmpeg concat demuxer joins per-scene mp4 files in lexical order (NN prefix ensures scene order)
- Per-scene `.srt` files are concatenated with cumulative offsets (from ffprobe durations) and globally renumbered
- If no `.srt` files exist, `final.srt` is skipped (not an error)
- When a `final.srt` is produced, the script also writes `final-sub.mp4` — a subtitles-burned copy suitable for players that don't auto-load external `.srt` files (e.g. QuickTime, some share/upload targets). `final.mp4` stays clean for players that soft-load `.srt`.

After the script succeeds, update the outline's top-level `## Pipeline status` block — flip `- [ ] Merge` to `- [x] Merge — [[final.mp4]], [[final.srt]], [[final-sub.mp4]]` (omit `final.srt` / `final-sub.mp4` when no subtitles were produced).

---

### Render Failure and Visual Review

- On manim stderr, diagnose and patch the scene's py, re-run
- On successful render, invoke `scripts/video_frames.py` to sample frames, read them, check against the scene md
- Visual-review failures count toward the same retry budget as stderr errors (default bound: 3)
- On exhaustion, pause and present the error or flagged frame to the user

_(Detailed iteration logic: Phase 3 action 5 + Phase 5 action 4.)_

---

### Feedback Modes

At each pause, accept any of — in practice the user will mix them freely:

- **Direct md edits** — the user opens artifacts in their editor, makes changes, then says `continue`. Re-read the affected files before proceeding and fold any changes into downstream stages (e.g. a new scene added to the outline spawns a new scene md in the Scenes stage).
- **Inline `{{comments}}`** — the user drops `{{double-curly}}` markers into the artifact. On `continue`, process them per the refine pattern: replace each comment with the edit it implies, show a diff, wait for acknowledgment if changes are substantive.
- **Chat instructions** — the user types feedback in chat. Apply the change to the artifact, show a diff, continue.

Explicit `continue` / `go` / `ok` / similar acknowledgments with no changes mean "proceed as-is." Don't ask for permission when the user has clearly already approved.

### Auto Mode

With `--auto` in ARGUMENTS, the skill runs end-to-end without review pauses between stages. Specifically:

- Stages still update the outline checklist and emit the same artifacts
- No "pause and wait" step after each stage — just continue to the next
- Render failures still auto-iterate within the retry bound
- On retry-bound exhaustion, the skill **still surfaces to the user** — `--auto` silences planned pauses, not errors

This mode is for runs where the user trusts the pipeline end-to-end (e.g., after a review run on the same topic).

---

## Scripts

- `scripts/video_state.py` — parse outline stage checklist, report next unchecked
- `scripts/video_merge.py` — ffmpeg concat + SRT offset math
- `scripts/video_frames.py` — timing-aware frame extraction

_(Implemented in Phase 2.)_

## Output

Creates a project folder under `<cwd>/<video-name>/` containing:
- `outline.md` (script + stage checklist)
- `research/*.md` (optional)
- `scenes/*.md` (scene descriptions)
- `code/*.py` (ManimCE Scene subclasses)
- `renders/*.mp4`, `renders/*.srt`, `renders/frames/*/`
- `final.mp4`, `final.srt`
