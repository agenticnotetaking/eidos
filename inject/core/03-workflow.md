## Skill Routing

When the user or a plan says to do something that matches an eidos skill, use that skill.
Don't fall back to built-in Claude Code behaviour or ad-hoc approaches when a skill exists for the job.
Always announce the matched skill before invoking: "This looks like X — invoking `/eidos:X`."
No need to ask for permission — just surface it clearly so the user can abort if needed.

**Skip detection when the user explicitly invokes a skill** (e.g. `/eidos:spec`, `/eidos:plan`).
The invocation IS the routing — don't match keywords on top of it.

Common triggers:
- "Plan this" → `/eidos:plan`
- "Research this" → `/eidos:research`
- "Deep dive on…" / "Go deep on…" / "Explore the landscape of…" → `/eidos:research-deep`
- "Continue deep research" / "Resume deep research" → `/eidos:research-deep continue`
- "Research this recursively" / "Branch out on…" / "Research tree for…" → `/eidos:research-recursive`
- "Continue recursive research" → `/eidos:research-recursive continue`
- "Document this external knowledge" → `/eidos:reference`
- "Spec this out" → `/eidos:spec`
- "We need to decide between…" → `/eidos:decision`
- "I found issues while testing" → `/eidos:observe`
- "Add a todo" → `/eidos:todo`
- "I wish it could…" / "Feature idea:" / "Wouldn't it be nice if…" → `/eidos:wish`
- "Let's brainstorm" → `/eidos:brainstorm`
- "Challenge this" / "Is this a good idea?" → `/eidos:challenge`
- "Is it safe to start a new session?" / "Anything left to do?" → `/eidos:compact`
- "Where are we?" / "What's the status?" / "How far along are we?" → `/eidos:status`
- "I'm working in subdir" / "Set mono focus" / "Which subdir am I in?" → `/eidos:mono`
- "Let me try some things" / "Let's experiment with…" / "I want to iterate on…" → `/eidos:experiment`
- [image dropped] / "Describe this image" / "Save this image" → `/eidos:image`
- "Review this plan" / "Check the plan before we start" → `/eidos:plan-review`
- "Make that a claim" → `/eidos:claim`
- "You're spiraling" → `/eidos:spiral`
- "Copy that" / "Clip that" / "Put that on the clipboard" → `/eidos:clip`
- "New worktree" / "Work on X in parallel" / "Create a worktree" → `/eidos:worktree`
- "Enable fail detection" / "Safe mode for commands" / "Verify before running" → `/eidos:faildetect`

## Plans

**IMPORTANT: Always read the plan template before working on any plan.**
The skills `/eidos:plan`, `/eidos:plan-continue`, and `/eidos:observe` already read it — don't read it twice.
Outside those skills, read [[template - plan - structured phases with actions and progress tracking]] yourself before touching a plan file.

When using `/eidos:plan`, create a plan file per the template — never use Claude Code's built-in plan mode instead.
Plans in `memory/` track multi-step work.
After each action: mark `[x]`, add `=>` notes for observations and created files, update Progress Log.
When the user reports testing issues during plan work, use `/eidos:observe` to structure them into numbered observations, update specs, and inject tasks.
Plans are best-effort: if an action proves wrong or underspecified during implementation, surface it and propose a plan edit, options, or `/eidos:research`/`/eidos:spec` — don't grind through a flawed action.

### Marking Actions Complete

An action is only `[x]` when every sub-bullet is satisfied.
If some sub-bullets are done and others aren't, the action stays `[ ]` — add `=>` notes for what's done and what remains.
Before marking `[x]`, check each sub-bullet against actual output (run it, look at it, test it).
The `=>` notes must account for every sub-bullet, not just describe what was built.
A partial implementation with `[x]` is worse than an honest `[ ]` with progress notes — it poisons the progress log.

## Externalise

Persist insights to files — don't let them stay only in chat.
Conversations are ephemeral; files outlast sessions and compound across them.
When in doubt, write it down — deleting an unnecessary file is easier than recreating lost context.
Destinations: specs in `eidos/`, inject snippets, procedural files in `memory/`, or inline `=>` notes in plans.
For work that accumulates context over time (research, large refactors, multi-source gathering), write progressively — create the file early and update it as you go.
Detail held only in context gets compressed or lost; detail written to a file is preserved.
See [[spec - externalise - persist insights beyond the conversation]].

When producing review items, observations, or findings that need human judgement: bias toward writing them to a file with feedback placeholders (`- [ ]`) rather than presenting in chat.
The file becomes the feedback surface — the human fills in responses at their own pace, across sessions if needed.
See [[c - bias toward artifacts as feedback surfaces over interactive dialogue]].

## Decisions

When work involves choosing between meaningful alternatives (architecture, tool choice, approach, trade-offs), suggest creating a decision file.
Lightweight choices (`=>` in plans) don't need this — the trigger is alternatives that were evaluated and a rationale that future-you would want.
Use `/eidos:decision` or create `memory/decision - <timestamp> - <claim>.md` following [[template - decision - options rationale and outcome]].

## Skills

Each skill lives in `skills/<name>/` with a descriptive main file (e.g. `weave.md`, `plan.md`).
`SKILL.md` is a symlink to the main file — it exists solely for Claude Code discovery.
The main file carries the proper name; `SKILL.md` is plumbing.
When creating a new skill: `ln -s <name>.md SKILL.md`.
Every skill gets a spec in `eidos/skills/spec - <name> skill - <claim>.md` — the skill file is the instructions, the spec is the intent and design rationale.
