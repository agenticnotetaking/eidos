# Pings

You can surface session status to the human via a native OS notification using `/eidos:ping <name> <type> <tldr>`.

This requires the **eidos-ping** menubar app to be installed and `ping_macos` to point at the binary in `.eidos-config.yaml`. See `.repos.yaml` for the source repo.

- `<name>` — short context label (e.g. `auth-refactor`). Pick based on current task; rename mid-session if work shifts. Two agents on the same branch use different names.
- `<type>` — `done`, `question`, `step`, `fail` (or another short token if the situation calls for it).
- `<tldr>` — ~5-word summary.

When to ping:
- **`done`** — task complete, you're stopping. Always ping.
- **`question`** / **`fail`** — blocked on the human. Always ping.
- **`step`** — only when the human asked to be informed after each milestone, or a phase wraps with something a human should see.

When running autonomously, **do not** ping speculative observations — only surface when input or a decision is genuinely needed.
