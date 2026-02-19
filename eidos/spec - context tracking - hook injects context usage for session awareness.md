---
tldr: UserPromptSubmit hook injects context window usage percentage so Claude can plan around capacity
---

# Context Tracking

## Target

Claude has no built-in awareness of how much context window has been consumed.
Without this signal, it can start large tasks near the end of a session, hit the limit mid-work, and lose progress.
A hook that injects `[context used: X%]` on each user prompt gives Claude the data to plan proactively.

## Behaviour

- A `UserPromptSubmit` hook fires when the user sends a message
- The hook reads the session transcript JSONL (provided as `transcript_path` in hook input) and extracts token counts from the last assistant message's `usage` field
- Total context = `input_tokens` + `cache_creation_input_tokens` + `cache_read_input_tokens`, divided by `context_tracking_max`
- Output: plain text `[context used: X%]` to stdout — Claude Code injects non-JSON stdout as context alongside the user's message
- If no usage data is found, the hook exits silently (safe fallback)
- Gated by `context_tracking_max` config key — set to max token count (e.g. `200000`), `null` to disable
- Only activates when `eidos/` directory exists (standard eidos guard)

### Session Start Instruction

When `context_tracking_max` is set, a feature snippet injects guidance at session start:
- Claude is told to expect `[context used: X%]` updates
- Thresholds guide proactive behaviour:
  - Below 50%: normal operation
  - 50–70%: mention context level if the user is about to start a large task
  - Above 70%: suggest compacting or clearing before large tasks
  - Above 85%: strongly recommend compacting or starting a new session

## Design

### Hook Flow

```
User sends message → UserPromptSubmit hook fires
  → eidos/ exists?        → no   → exit 0
  → context_tracking_max? → null → exit 0
  → read transcript_path JSONL
    → find last assistant message with usage data
    → compute total tokens → percentage of context_tracking_max
  → percentage available?  → no   → exit 0
  → output plain text: [context used: X%]
  → Claude Code injects stdout as context alongside user message
```

### Why UserPromptSubmit, Not Stop

The Stop hook can only inject data via `{"decision": "block", "reason": "..."}`, which Claude Code surfaces as "Stop hook error" in the UI — wrong semantics for informational data.
`UserPromptSubmit` injects plain text stdout as context alongside the user's message — no blocking, no error labels.
(JSON `additionalContext` requires nesting in `hookSpecificOutput`; plain text stdout is simpler and equally effective.)
The timing shifts from "after each AI message" to "before each AI response" — functionally equivalent.

### Config Gating

- Hook script reads `context_tracking_max` via `read_config.sh` — the value is the max token count
- Feature snippet `inject/feature/context-tracking-max.md` maps to `context_tracking_max` config key automatically (filename hyphens → underscores)
- Session-start gating treats any non-null, non-false value as enabled (supports both booleans and numbers)
- Both the hook and the session start instruction are gated by the same key

## Verification

- Set `context_tracking_max: 200000` in `.eidos-config.yaml`
- Send a message — Claude should see `[context used: X%]` in its context
- Set `context_tracking_max: null` — no hook behaviour
- Remove `eidos/` directory — hook exits silently regardless of config

## Friction

- The transcript is scanned on every user message — may add latency on very long sessions
- Token count is an approximation; the actual context window budget includes overhead not captured in `usage` fields
- First message of a session has no prior assistant usage data — no percentage injected (expected)

## Interactions

- [[spec - config - toggleable project settings]] — `context_tracking_max` setting
- [[spec - session context - composable snippet based context injection]] — feature snippet follows the standard gating pattern
- [[spec - eidos - spec driven development loops]] — hooks are part of plugin infrastructure

## Mapping

> [[hooks/context-tracking.sh]]
> [[hooks/hooks.json]]
> [[inject/feature/context-tracking-max.md]]
