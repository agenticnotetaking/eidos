---
tldr: Agent calls /eidos:ping <name> <type> <tldr> to surface session status to the human via native OS notifications
---

# Ping — agent surfaces status via OS notification

## Target

When the human steps away from a long session — or runs several in parallel — they have no signal that the agent has stopped, finished, or is blocked.
Watching N terminals doesn't scale.
Pings give the agent a one-line out-of-band channel to the human: "I'm done", "I have a question", "I hit a wall".
Native OS notifications and a clickable popover surface the message without the human having to look at the terminal.

## Behaviour

- Agent calls `/eidos:ping <name> <type> <tldr>` to fire a notification
  - `<name>` — short context label like `auth-refactor` or `add-foo-page`. Agent picks based on current task; can change mid-session as work shifts. Two agents on the same branch use different names so the human can tell their pings apart.
  - `<type>` — one of `done`, `question`, `step`, `fail`. Open-ended: agent may use another short token if the situation calls for it.
  - `<tldr>` — ~5 word summary of what just happened
- Notification format: title is `[<name>] <type>`, body is `<tldr>`
- The skill is a thin wrapper over `scripts/ping.sh` — the agent (or any tool) can also call the script directly for speed
- Agent uses pings deliberately, not constantly:
  - Always ping on `done` — the agent is stopping and the human should know
  - Always ping on `question` / `fail` — the agent is blocked on the human
  - `step` only when the human asked to be informed after each milestone, or when a phase wraps with something a human should see
  - When running autonomously, do **not** surface speculative observations — only ping when input or a decision is genuinely needed
- Gated by `ping_macos` config key — a path string. Empty / unset means the user hasn't opted in (silent no-op). Set to a built `eidos-ping-app` binary path means full ping flow.
- Only activates when `eidos/` directory exists (standard eidos guard)

## Design

### Skill and Script

```
skills/ping/ping.md             # invoked as /eidos:ping
scripts/ping.sh                 # gate + jsonl write + NC entry + lazy launch
inject/feature/ping-macos.md    # session-start instruction when ping_macos is set
.repos.yaml                     # ping_macos: <repo URL> for missing-binary install hint
```

The skill parses the three arguments and calls the script.
The script handles all OS-level work and decides when to defer to the external menubar app.

### Opt-in via External Companion App

The actual menubar UI (toast under the icon, popover, click-to-refocus) lives in a separate repository — see `.repos.yaml` for `ping_macos`. The eidos plugin doesn't ship Swift sources or a build artifact: macOS-only code stays out of the plugin so Linux/Windows users (and macOS users uninterested in the feature) aren't burdened.

`ping.sh` runs in three modes depending on `ping_macos`:
- **Empty** — exit 0 silently. Default for everyone.
- **Set, binary present** — write JSONL queue record, fire NC notification, launch the binary if not already running.
- **Set, binary missing** — write JSONL, fire NC, then print a one-line stderr message naming the install repo (read from `.repos.yaml`) so the user can complete setup.

### macOS Notification (always fires when opted in)

```
osascript display notification "<tldr>" with title "[<name>] <type>" sound name "Glass"
```

This is complementary to the menubar popover: the NC entry persists in the sidebar for review, and the Glass sound is audible regardless of banner suppression.

### Queue Protocol

Path: `~/Library/Application Support/eidos/pings.jsonl`. Append-only JSON Lines, one record per ping with fields `ts`, `name`, `type`, `tldr`, `host_app`, `cwd`, `source_pid`. The script trims to the last 1000 records before each append. The companion app is responsible for tailing this queue.

The `host_app` field is determined by walking up the process tree (`lsof -d txt`) to find the first ancestor process running from a `.app` bundle. The `cwd` is `$PWD` at script invocation. Both are used by the menubar app to identify and refocus the right window when several windows of the same host are open.

### Config Gating

- `ping_macos: ""` (default empty) — opt-in
- Feature snippet `inject/feature/ping-macos.md` injects a session-start reminder. Filename hyphens convert to underscores in the session-start hook (`hooks/session-start.sh`), so `ping-macos.md` ↔ `ping_macos` config key automatically.

### Argument Parsing

The script takes `<name> <type>` as positional args 1–2 and treats `$3..$N` as the tldr (joined with spaces).

## Verification

- Unset `ping_macos`: `/eidos:ping foo done test` → exit 0 silently. No queue record, no notification, no app launch.
- Set `ping_macos` to a missing path: `/eidos:ping foo done test` → JSONL appended, NC entry fires, stderr names the install repo from `.repos.yaml`.
- Set `ping_macos` to a built binary: `/eidos:ping foo done test` → toast under menubar icon, badge increments, popover lists recent pings on click; **Open** activates the right host window and switches to its Space.
- Linux / Windows: `/eidos:ping foo done test` → exit 0, message about platform not yet supported.

## Friction

- Explicit-only means a forgotten ping is a silent ping. Stop-hook auto-fire is tracked in Future.
- macOS suppresses NC banners under Do Not Disturb / Focus; the menubar popover bypasses this.
- Title-based window matching needs Screen Recording permission for the companion app.

## Interactions

- [[spec - config - toggleable project settings]] — adds the `ping_macos` key (string path)
- [[spec - session context - composable snippet based context injection]] — feature snippet follows the standard gating pattern

## Mapping

> [[skills/ping/ping.md]]
> [[scripts/ping.sh]]
> [[inject/feature/ping-macos.md]]
> [[.repos.yaml]]

## Future

{[!] Linux companion via `notify-send` (libnotify-bin) — opt-in via `ping_linux: <path>`}
{[!] Windows companion via PowerShell NotifyIcon — opt-in via `ping_windows: <path>`}
{[?] Stop-hook auto-fire when the agent didn't ping explicitly during the turn — catches forgotten pings}
{[?] Notification-hook auto-fire mapping Claude Code's permission/idle prompts to `question` pings — gated separately, can be noisy}
{[?] Sound / urgency hint per type (e.g. `fail` uses a different sound, `done` uses the default)}
