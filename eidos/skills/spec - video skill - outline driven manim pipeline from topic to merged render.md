---
tldr: Staged skill that walks a topic to a merged manim video via research, outline, scenes, code, render, merge — with the outline doubling as the plan/state document
---

# /eidos:video

Turn a topic (or a pile of wiki-linked md) into a rendered manim explainer video through a fixed pipeline of stages.
Each stage produces md or code artifacts in a dedicated project folder; the outline doubles as a plan document that tracks stage progress via checkboxes and wiki-links to the artifacts each stage produces.

## Target

Making an explainer video is inherently multi-stage: research the topic, draft a script, design scenes, write animation code, render, then merge.
Done by hand, the stages lose continuity — notes live in one place, the script in another, the code elsewhere, and nothing tracks what's done.
Done by an AI without structure, the user loses the ability to steer between stages.

The video skill provides a single orchestrator that walks the full pipeline, pauses for review at each stage by default, and keeps all artifacts for a video together under one project folder.
The outline itself carries the progress state, so there's no separate `.state` file and resumption is just "re-read the outline."

## Behaviour

### Invocation

- `/eidos:video [topic]` — start a new video project
  - `topic` can be a plain string, a path to an md file, or a path to a folder of wiki-linked md
- `/eidos:video` (no args, inside an existing project folder) — detect the in-progress video project in cwd and resume at the first unchecked stage
- `--auto` flag skips all review pauses and runs the full pipeline through

### Stages

The pipeline runs in order. Each stage finishes by updating the outline's stage checklist and, unless `--auto`, pausing for review.

1. **Research** — collect background material
   - Read any user-provided md files; follow wiki-links transitively
   - Run WebSearch / WebFetch when coverage is insufficient
   - Ask 1–2 clarifying questions on focus and depth when the topic is broad
   - Write research notes into `<project>/research/*.md`
   - Skip entirely when the user-provided md already covers the topic

2. **Outline** — draft the script outline at `<project>/outline.md`
   - Sections with tldr, what it's about, key points to convey
   - Includes the stage checklist (see Design → Outline as state)

3. **Scenes** — write one scene description per scene into `<project>/scenes/NN-<name>.md`
   - Scene md describes: on-screen text (verbatim), visual elements, animations, style, subtitle lines, approximate duration
   - Descriptions may be precise ("red arrow from (0,0) to (1,2), 0.5s ease-in") or vague ("show how the gradient points uphill") — codegen fills gaps
   - Optional `## Continuity` section declares carried-over elements from the previous scene (see Design → Scene continuity)
   - Outline sections wiki-link to their scene md files inline under a per-section **Scenes:** bullet

4. **Code** — generate manim code per scene into `<project>/code/NN-<name>.py`
   - ManimCE (community edition); 1 scene md = 1 py file = 1 `Scene` subclass
   - Class name derived from the scene file (e.g. `01-intro.md` → `class SceneIntro(Scene)`)
   - When any scene declares `## Continuity`, extract shared construction into `<project>/code/_shared.py` and use `self.add(...)` on carried elements at frame 0 of the inheriting scene — see Design → Scene continuity

5. **Render** — run manim per scene into `<project>/renders/NN-<name>.mp4`
   - Emit a companion `NN-<name>.srt` per scene from the subtitle lines in the scene md
   - Extract sample frames into `<project>/renders/frames/NN-<name>/*.png` at timing-aware positions (scene start, scene end, each subtitle-line transition)
   - Visual review: the agent reads the frames and checks them against the scene description (text visible and correct, visuals reasonable, nothing cut off or overlapping, scene matches description)
   - Auto-iterate on render errors OR visual-review issues (bounded to N retries, e.g. 3) — parse stderr or note the visual defect, patch the py, re-run
   - If still failing after N tries, pause and ask the user, presenting the error and the sampled frames

6. **Merge** — concatenate scenes into `<project>/final.mp4` and `<project>/final.srt`
   - ffmpeg concat demuxer for mp4
   - SRT concatenation with cumulative offsets from scene durations
   - Also emits `<project>/final-sub.mp4` with the subtitles burned into the pixels — for players that don't auto-load external `.srt` (QuickTime, most share targets)

### Review and feedback

When paused, the skill presents the stage's artifact(s) and waits.
The user can give feedback in any of these ways — the skill accepts all three:

- **Edit md files directly** — skill re-reads on `continue`
- **Inline `{{comments}}`** — skill processes them per the eidos refine pattern, adjusts, and continues
- **Chat instructions** — skill applies, shows the diff, continues

The word `continue` (or equivalent acknowledgment) signals go-ahead without changes.

### Resume

- Re-invoking `/eidos:video` inside a folder that contains an `outline.md` detects the project and resumes at the first unchecked stage
- `scripts/video_state.py` handles both the colocated format (`## Pipeline status` + per-scene triplets) and the legacy flat format (`## Stages`) — see Design → Outline as state
- No separate state file — the outline carries the state

### Render failure and visual review

- On manim stderr, the skill diagnoses and patches the scene's py file
- On successful render, the skill samples frames and inspects them against the scene description; a failed visual check is treated the same as a render error for iteration purposes
- Bounded at N retries per scene (default 3), combining render errors and visual-review failures in the same budget
- On exhaustion: pause, present the error (or the flagged frame + reason) and last attempted fix, ask the user to intervene (manual edit, retry anyway, skip the scene, or accept as-is)

## Design

### Project folder layout

The skill creates a new folder under the current project root for each video:

```
<cwd>/<video-name>/
  outline.md                  # script + stage checklist + wiki-links to artifacts
  research/
    *.md                      # research notes
  scenes/
    01-<name>.md              # scene descriptions
    02-<name>.md
  code/
    01-<name>.py              # ManimCE Scene subclasses
    02-<name>.py
  renders/
    01-<name>.mp4             # per-scene renders
    01-<name>.srt             # per-scene subtitles
    02-<name>.mp4
    02-<name>.srt
    frames/
      01-<name>/              # sampled frames for visual review
        00.00s.png
        02.50s.png
        ...
      02-<name>/
        ...
  final.mp4                   # merged video, no burned subtitles
  final.srt                   # merged subtitles (sidecar)
  final-sub.mp4               # merged video with subtitles burned in (only when final.srt exists)
```

Flat root plus subfolders by artifact type.
No `.state` file — the outline serves that role.
`<video-name>` is derived from the topic using the standard prefix-claim naming convention.

### Outline as state

The outline document is the single source of truth for script content AND pipeline progress.
Global one-shot stages (Research, Outline, Merge) live in a `## Pipeline status` block near the top.
Per-scene stages (md, code, render) are inline under each scene in each section — colocated with the section that describes it, so a reader sees both narrative and progress for a section in one place.

```markdown
## Pipeline status

- [x] Research — [[research/concept-overview]]
- [x] Outline — this document
- [ ] Merge

## Sections

### 1. Intro

- **About:** ...
- **Scenes:**
  - [[scenes/01-intro]]
    - [x] md
    - [x] code
    - [x] render → [[renders/01-intro.mp4]]

### 2. Gradient field

- **About:** ...
- **Scenes:**
  - [[scenes/02-gradient-field]]
    - [x] md
    - [ ] code
    - [ ] render
```

Benefits:
- Resumption is trivial: read outline via `scripts/video_state.py`, find the first unchecked stage, continue from there
- The outline visually reflects "how far along" each section is, not just the aggregate
- Multiple scenes per section are natural — sibling bullets under one section's **Scenes:** list
- Wiki-links make every artifact discoverable from the single entry point

**Back-compat.** The legacy flat `## Stages` block (single top-level checklist for Research/Outline/Scenes/Code/Render/Merge with wiki-links nested as children) is still parsed by `video_state.py`. Existing projects don't need to migrate.

### Scene md structure

Each scene md captures what the scene should be, at whatever precision suits the user:

- **About** — one or two sentences on the scene's purpose
- **On-screen text** — verbatim strings that appear
- **Visuals** — elements and layout
- **Animations** — entrances, transitions, highlights
- **Style** — colors, font sizes, pacing notes
- **Subtitles** — lines with optional per-line durations or timestamps
- **Duration** — approximate target length

Any of these can be vague.
Codegen fills in tasteful defaults where the scene md is silent.

### Subtitles

- Scene md declares subtitle lines; each line has either an explicit timing or an implicit duration estimate
- Render stage emits a per-scene `.srt` alongside the mp4 using those timings
- Merge stage concatenates all per-scene `.srt` files with cumulative offsets drawn from measured scene durations

### ManimCE codegen

- One `.py` per scene, one `Scene` subclass per `.py`
- Class name derived from the scene file's claim portion (stripped of separators, camel-cased)
- Import idioms and API conventions follow ManimCE as of the current stable release

### Scene continuity

Adjacent scenes often share visual elements — a curve that reappears, a title that stays on screen, axes used in every step of a walkthrough. A naive codegen rebuilds those elements from scratch in each scene with entrance animations (`Write`, `Create`, `FadeIn`), so the viewer sees scene N end with everything drawn and scene N+1 start with an empty canvas that fades the elements back in — a visible discontinuity at the join.

Continuity solves this with a **"final frame equals first frame"** trick:

- Each scene's md can declare an optional `## Continuity` section naming the previous scene and listing the carried-over elements with their final state from that scene
- Shared construction moves into `<project>/code/_shared.py` — a module of pure, deterministic constructor functions (no unseeded RNG, no timestamps)
- Both the scene that produces the final state and the scene that inherits it use the same `_shared` helpers, so pixel output is identical
- The inheriting scene's `construct()` uses `self.add(...)` (not `self.play(...)`) on the carried elements before starting any new animations — this places them on frame 0 at the same positions they occupied on the last frame of the previous scene
- ffmpeg concat does a hard cut between mp4s; because both frames are pixel-identical for the shared content, the cut is visually invisible

**Staleness rule.** Changing scene N's md or code invalidates every downstream scene declaring continuity from N — they must be regenerated and re-rendered.

Scenes without a `## Continuity` section keep the standard fresh-start pattern. `_shared.py` is only generated when at least one scene opts in.

### Render iteration

Per scene, during the render stage:
```
manim render <code>.py <ClassName>
  stderr parsed
    on error → patch py → retry (bounded)
    on success → next scene
  bound exhausted → pause, ask user
```

### Visual review

Manim correctness is hard to verify from code alone, but the skill controls the timing of everything on screen, so it can extract frames at meaningful moments and inspect them.

- After a scene renders, ffmpeg extracts frames at timing-aware positions:
  - Scene start (shortly after `t=0` to let the opening animation settle)
  - Scene end (shortly before the final frame)
  - Each subtitle-line transition (using the declared subtitle timings)
- Frames land in `<project>/renders/frames/NN-<name>/<timestamp>s.png`
- The agent reads the frames (multimodal) and checks them against the scene md — on-screen text correct and legible, visual elements present and in bounds, layout matches the description, no obvious glitches
- Any flagged frame plus a brief reason is treated identically to a stderr error for the retry loop
- During the render-stage pause, the frame grid is surfaced to the user alongside the mp4 — they can see what the agent saw

Visual review is bounded by the model's interpretation of the frames; it catches gross failures (blank scenes, cut-off text, wrong content) reliably but may miss subtle aesthetic issues.

### Merge

- ffmpeg concat demuxer joins the per-scene mp4 files
- Subtitle concatenation walks scene durations to compute offsets and rewrite timestamps

## Verification

- `/eidos:video quantum-tunneling` with no sources produces a complete project tree (research, outline, scenes, code, renders, final.mp4, final.srt)
- `/eidos:video ./notes/entropy/` with a folder of wiki-linked md skips research when coverage is sufficient
- Pausing and editing the outline between stages is reflected in downstream stages (e.g., adding a section regenerates the relevant scenes)
- Re-invoking `/eidos:video` in an existing project folder resumes at the first unchecked stage
- `{{comments}}` added to a scene md during the scenes-stage pause are processed on continue and the scene is rewritten
- A scene with deliberately broken Python triggers bounded auto-iteration and then asks the user when the bound is exceeded
- A scene that renders but produces off-screen or missing elements is caught by visual review and triggers iteration within the same retry budget
- `--auto` runs end-to-end without stopping

## Friction

- ManimCE install and system deps (ffmpeg, LaTeX for some mobjects) are non-trivial — the skill assumes they're available
- Subtitle timing without TTS is an estimate; per-line durations may drift from actual render timing
- Large research or long outlines can balloon context — intermediate summaries may be needed
- Codegen quality is bounded by scene description specificity; vague scenes produce generic defaults
- Render time per scene is real wall-clock — full-pipeline autorun can be slow
- Visual review is bounded by the model's interpretation of still frames — subtle errors or motion-dependent glitches may slip through
- The outline-as-state convention breaks if the user renames or moves artifacts without updating the outline

## Interactions

- Depends on [[spec - naming - prefixes structure filenames as prefix claim pairs]] — file naming for project folder, scenes, code, renders
- Relates to [[spec - plan skill - structured plan for multi step work]] — the outline's stage checklist mirrors the plan structure
- Relates to [[spec - refine skill - processes inline comments via structured dialogue]] — `{{comments}}` handling during review pauses
- Relates to [[spec - research skill - investigate and document findings with sources]] — research stage pattern
- Relates to [[spec - options skill - present structured choices for user decision]] — for the "multiple retries failed, what now?" prompt

## Mapping

> [[skills/video/video.md]]

## Future

{[!] `--auto` flag to run the full pipeline without pauses}
{[?] TTS integration for accurate subtitle timing and optional audio track}
{[?] Style presets (3b1b look, scientific diagram, pastel explainer) applied across all scenes}
{[?] Shared setup module for common imports/helpers across a project's scenes}
{[?] Outline regeneration trigger when research reveals major gaps mid-pipeline}
{[?] Scene preview at low quality before committing to full render}
{[?] Configurable manim flavor (ManimCE vs 3b1b) per project}
{[?] Video-level (not frame-level) visual review once multimodal video input is widely available}
{[?] Adaptive frame sampling — more frames where the scene description declares complex animations}
{[?] Strengthen codegen duration-match guidance from "a few tenths of slack" to a concrete "declared + 0.5s" default — first-pass tends to undershoot (surfaced during gradient-descent verification)}
{[?] Codegen prompt should address clustered-point label collisions — alternating label directions or label-only-keyframes (distinct from edge clipping)}
{[?] Optional `--crossfade DURATION` flag on `video_merge.py` for scenes without content continuity — uses ffmpeg `xfade` filter at non-continuity joins; default stays pure concat for the crispness continuity requires}

## Notes

The outline-as-state design was chosen in preference to a separate `.state` file so the user has one document to read to understand both the artifact (the script) and the progress.
The same structure makes the outline valuable as a standalone deliverable even when the video never gets rendered.
