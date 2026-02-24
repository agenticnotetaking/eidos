# Eidos

Spec-driven development plugin for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

Markdown specs capture intent.
Code is a downstream manifestation of spec intent.
The relationship is bidirectional: specs shape code, code can update specs, and conflicts become human decisions.

## Why

Development intent lives in chat messages, commit messages, and the developer's head.
When an AI starts a new session, it sees code but not the reasoning behind it.

Eidos keeps intent in spec files alongside the code.
Specs describe what a system *should* be.
When spec and code drift apart, neither automatically wins — the human decides which to update.

## Three folders

```
project/
  eidos/     # what it SHOULD be (specs, claims)
  memory/    # how we got here (plans, decisions, sessions)
  src/       # what it IS (code)
```

Specs describe timeless intent.
Plans describe time-bound work.
Code is the result.

## How it works

### Green-field

Write a spec to capture what you want — behaviour, design, verification.
This can be manual or collaborative (`/eidos:spec` walks you through it).

Then push it into code:
```
/eidos:push my-feature-spec
```

Verify — with tests, manually, or both.
If something's off, update the spec, commit, push again.
`/eidos:push recent 1` picks up the latest spec change and its precise diff.
Repeat.

### Existing project

You already have the manifestation — mine it for intent:
```
/eidos:pull the auth module
```

Review the extracted spec, refine it, and iterate from there.
Now you have a spec to push against, drift-check, and evolve.

### Plans and memory

Multi-step work gets a plan:
```
/eidos:plan migrate the database layer
```

Plans live in `memory/`, persist across sessions, and track progress phase by phase.
Resume with `/eidos:plan-continue`.

Other procedural skills accumulate context the same way:
- `/eidos:research` — investigate external topics, document findings with sources
- `/eidos:observe` — capture testing issues mid-plan, update specs, inject tasks
- `/eidos:decision` — record architectural choices with options and rationale

### Externalise everything

AI "learning on the job" is just capturing ephemeral knowledge into files and composing them into session context.

That knowledge can be anywhere — your chat history, a coworker's head, legacy code nobody dares touch.
Eidos gives it all a place to land and a way to get loaded when it matters.

## Install

Requires [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

```bash
# Add marketplace
/plugin marketplace add agenticnotetaking/eidos

# Install plugin
/plugin install eidos@eidos
```

Then restart Claude and run `/eidos:init` inside any project to bootstrap the folder structure.

## Skills

Run `/eidos:help` for the full list. Highlights by category:

**Core loop** — sync between spec and code:

| Skill              | What it does                                      |
| ------------------ | ------------------------------------------------- |
| `/eidos:spec`      | Create a spec via structured Q&A                  |
| `/eidos:push`      | Implement code to match a spec                    |
| `/eidos:pull`      | Reverse-engineer a spec from existing code        |
| `/eidos:drift`     | Analyse divergence between specs and code         |
| `/eidos:sync`      | Bidirectional reconciliation                      |
| `/eidos:coherence` | Check specs against each other for contradictions |
| `/eidos:weave`     | Discover missing wiki links, prune stale ones     |

**Planning** — structured multi-step work:

| Skill                  | What it does                                 |
| ---------------------- | -------------------------------------------- |
| `/eidos:plan`          | Plan multi-step work with phases and actions |
| `/eidos:plan-continue` | Resume work on an existing plan              |
| `/eidos:research`      | Research a topic and document findings       |
| `/eidos:decision`      | Record a decision with options and rationale |
| `/eidos:brainstorm`    | Explore ideas around a topic                 |
| `/eidos:experiment`    | Log-based iterative exploration              |

**Observation** — understand what you have:

| Skill                 | What it does                             |
| --------------------- | ---------------------------------------- |
| `/eidos:observe`      | Capture testing issues mid-plan          |
| `/eidos:architecture` | Snapshot codebase structure              |
| `/eidos:code-review`  | Review code for quality and security     |
| `/eidos:reflect`      | Extract learnings from a session or file |

**Utility** — workflow glue:

| Skill             | What it does                               |
| ----------------- | ------------------------------------------ |
| `/eidos:todo`     | Create quick task files                    |
| `/eidos:done`     | End session with export and merge offer    |
| `/eidos:annotate` | Leave inline AI feedback for human review  |
| `/eidos:toclaude` | Persist behaviour corrections to CLAUDE.md |
| `/eidos:toeidos`  | Route insights into specs and claims       |

## The name

Eidos (εἶδος) — ancient Greek for "form" or "ideal form".

For Plato, eidos is the ideal that exists prior to any instance.
`/push` is Platonic: start with the ideal, make it real.
For Aristotle, eidos is the essence within particular things — discovered by studying concrete instances.
`/pull` is Aristotelian: start with code, extract intent.
The loop between them — spec meets reality, reality pushes back, spec evolves — is dialectical refinement.

## License

MIT
