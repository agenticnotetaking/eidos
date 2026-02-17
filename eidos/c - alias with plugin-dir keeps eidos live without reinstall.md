---
tldr: Shell alias with --plugin-dir loads eidos live from source — always current, no install step
---

# Alias with plugin-dir keeps eidos live without reinstall

## The Problem

`claude plugin add` copies the plugin into a cache.
Changes to eidos don't propagate — you have to re-run the install after every edit.
During active development this defeats the purpose.

Symlinking into `~/.claude/plugins/` doesn't work — that directory is a cache managed by `claude plugin add`, not a scan directory.
Unregistered directories there are ignored.

## The Solution

A shell alias that always includes `--plugin-dir`:

```bash
alias cc='claude --plugin-dir /path/to/eidos'
```

Add to `.zshrc` or `.bashrc`.

This gives both:
- **Always current** — loads from the live eidos directory every session
- **No install step** — no `claude plugin add`, no cache staleness
- **Works everywhere** — any project gets eidos commands automatically

## Behaviour

- Changes to skill files, scripts, and hooks take effect on the **next session start**, not mid-session
- The session-start hook only activates if the target project has an `eidos/` folder — silent otherwise
- Within the eidos project itself, `.claude-plugin/plugin.json` at the project root is auto-detected — the alias is for other projects
- Multiple `--plugin-dir` flags can be chained if needed

## Friction

- If the eidos repo moves, the alias path breaks — update it
- Mid-session changes require restarting the session to take effect
- The alias overrides the bare `claude` command — use a distinct alias name (e.g., `cc`) to keep both available
