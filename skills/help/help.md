---
tldr: List all eidos skills with descriptions
category: core
---

# /eidos:help

List available eidos commands, explain the workflow, and offer interactive guidance.

## Usage

```
/eidos:help
```

## Instructions

### 1. List Skills

Read all SKILL.md files in `${CLAUDE_PLUGIN_ROOT}/skills/`.
For each, extract `tldr` and `category` from YAML frontmatter.

Group by `category` in this order: core, planning, observation, utility.
Present as a formatted list:

```
Eidos — spec-driven development for Claude Code

Core Loop:
  /eidos:<name>   <tldr>
  ...

Planning:
  ...

Observation:
  ...

Utility:
  ...
```

### 2. How It Works

After the skill list, always show a brief workflow overview:

```
How it works:

  eidos/     what it SHOULD be (specs, intent)
  memory/    how we got here (plans, decisions, research)
  src/       what it IS (code)

Eidos keeps specs and code in sync bidirectionally:

  Spec → Code    Write what you want, then make it real (/push)
  Code → Spec    Extract intent from existing code (/pull)
  The Loop       Edit spec → push → test → adjust spec → repeat

Specs are markdown files with wiki links forming a relationship graph.
Leave {{comments}} in specs for AI-assisted refinement (/refine).
Plans in memory/ persist across sessions and track multi-step work.
```

### 3. Offer Guidance

After the overview, ask:

```
Want help figuring out where to start?
```

If the user declines, stop here.

If the user accepts, have a short interactive conversation to understand their situation:

- **What are they working on?** New project, existing codebase, or exploring eidos itself?
- **What's their goal?** Capture intent, improve documentation, plan a feature, understand code?
- **What exists already?** Any specs in `eidos/`? Any plans in `memory/`?

Based on their answers, suggest a concrete starting path with specific skills.

#### Example starting paths

**New project, starting from ideas:**
> Dump your notes into `eidos/seed.md` — doesn't have to be clean.
> Then `/eidos:spec` turns them into a proper spec.
> Review it, leave `{{comments}}` on anything that's off, run `/eidos:refine`.
> When you're ready to build: `/eidos:plan` for big work, `/eidos:push` for direct implementation.

**Existing project, no specs yet:**
> `/eidos:pull` extracts a spec from your code — pick a feature or component to start with.
> Read the generated spec, leave `{{comments}}`, `/eidos:refine` to iterate.
> Now you have a spec you can evolve. Edit it, `/eidos:push` the changes back.

**Mid-project, specs exist:**
> `/eidos:drift` shows where specs and code have diverged.
> `/eidos:next` shows open items across plans, todos, and specs.
> `/eidos:coherence` checks specs against each other for contradictions.

**Just exploring:**
> Read [[spec - eidos - spec driven development loops]] for the full design.
> Try `/eidos:pull` on a small piece of code to see what a spec looks like.
> The workflow clicks once you've done one push-pull cycle.

These are examples — adapt to what the user actually tells you.
The goal is a short, useful conversation that ends with a clear next action.
