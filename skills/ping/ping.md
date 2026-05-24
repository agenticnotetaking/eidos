---
tldr: Surface session status to the human via a native OS notification
category: utility
---

# /eidos:ping

Send a short out-of-band signal to the human — "I'm done", "I have a question", "I hit a wall" — as a native OS notification.
The agent picks the moment; the human gets a popup without watching the terminal.

## Setup (macOS, opt-in)

This skill is a no-op until the human has installed the **eidos-ping** menubar app and pointed at it in `.eidos-config.yaml`:

```yaml
ping_macos: /path/to/eidos-ping/bin/eidos-ping-app
```

Source repo: see `.repos.yaml` (`ping_macos` entry). Without setup, `/eidos:ping` exits silently — no jsonl record, no notification, no popover.

## Usage

```
/eidos:ping <name> <type> <tldr>
```

- `<name>` — short context label for what this session is working on (e.g. `auth-refactor`, `add-foo-page`). Pick based on current task; change mid-session as work shifts. Two agents on the same branch should use different names so the human can tell their pings apart.
- `<type>` — one of `done`, `question`, `step`, `fail`. Open-ended; another short token is fine if the situation calls for it.
- `<tldr>` — ~5-word summary of what just happened.

Notification format: title is `[<name>] <type>`, body is `<tldr>`.

## When to Ping

- **`done`** — task complete, agent is stopping. Always ping.
- **`question`** — blocked on a decision or clarification. Always ping.
- **`fail`** — hit a real blocker that can't be resolved without the human (test failure, missing creds, etc.). Always ping.
- **`step`** — only when the human asked to be informed after each milestone, or a phase wraps with something a human should see.

When running autonomously, **do not** ping speculative observations — only surface when input or a decision is genuinely needed.

## Instructions

1. Validate three arguments are present. If not, ask the user what to ping.
2. Call the script:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/scripts/ping.sh <name> <type> <tldr>
   ```
3. The script handles the `ping_macos` opt-in gate, JSONL queue write, NC notification, and lazy-launch of the aggregator.
4. Confirm briefly in the response: `[<name>] <type> — <tldr>`.

## Output

- macOS, configured: queue record + NC entry + toast/popover via the menubar app.
- macOS, unconfigured: silent no-op.
- Linux/Windows: silent no-op (an opt-in companion app for those platforms is future work).
