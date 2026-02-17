# Eidos

Spec-driven development plugin for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

Markdown specs are the source of truth.
Code is a downstream manifestation of spec intent.
The relationship is bidirectional: specs shape code, code can update specs, and conflicts become human decisions.

## Install

```bash
/plugin marketplace add agenticnotetaking/eidos
/plugin install eidos@eidos
```

Then **restart claude** and run `/eidos:init` inside any project to bootstrap the folder structure.

## How it works

Three folders:

- `eidos/` — what the system **should** be (specs, claims, templates)
- `memory/` — how we got here (plans, decisions, sessions)
- `src/` (or project code) — what it **is**

Two workflow loops:

- **Top-down:** spec → push ( → plan ) → code
- **Bottom-up:** code → pull ( → plan ) → spec
- **Sync** drift and coherence checks

## Skills

Run `/eidos:help` for a full list. Some highlights:

| Skill             | What it does                                 |
| ----------------- | -------------------------------------------- |
| `/eidos:spec`     | Create a spec via structured Q&A             |
| `/eidos:plan`     | Plan multi-step work                         |
| `/eidos:drift`    | Analyse divergence between specs and code    |
| `/eidos:push`     | Implement code to match a spec               |
| `/eidos:pull`     | Reverse-engineer a spec from existing code   |
| `/eidos:sync`     | Bidirectional reconciliation                 |
| `/eidos:observe`  | Capture testing issues mid-plan              |
| `/eidos:research` | Research a topic and document findings       |
| `/eidos:decision` | Record a decision with options and rationale |

## License

MIT
