---
tldr: View and toggle eidos project settings
category: utility
---

# /eidos:config

View and change project settings.

## Usage

```
/eidos:config
/eidos:config <key>
```

## Instructions

### 1. Check Config

Read `.eidos-config.yaml` in the project root.

- **File missing or incomplete** (missing keys): tell the user and offer to run `/eidos:init` to set up.
  If they accept, invoke `/eidos:init`. After init completes, continue to step 2.
  If they decline, stop — config can't be changed without a complete file.
- **File complete:** continue to step 2.

Parse format: YAML key-value pairs.
- `key: true` / `key: false` = boolean
- `key: 200000` = numeric value
- `key: null` = explicitly disabled/unset
- `key: value` = string value

### 2. Present Settings

Show all available settings with current values:

```
Eidos config (.eidos-config.yaml):

  git_workflow: true              # branch-per-task, commit-per-action, --no-ff merges
  status_reporting: true          # status report after each action
  skills_list: true               # eidos skill listing in session start context
  specs_and_concepts: true        # spec/concept listing, future items at session start
  session_context: true           # session orientation: branches, todos, plans, recent memory
  context_tracking_max: 200000    # max tokens for context window tracking (null to disable)
  mono_focus: true                # mono-repo sub-part focus injection at session start
  observation_images: true        # persist pasted images as named observation files in memory/

Change which? (e.g., "git_workflow", "context_tracking_max 100000")
```

If a specific key was provided as argument, show only that setting and its description.

### 3. Available Settings

| Key | Default | Type | Description |
|-----|---------|------|-------------|
| `git_workflow` | `true` | bool | Branch-per-task, commit-per-action, --no-ff merges |
| `status_reporting` | `true` | bool | Status report after each action (branch, commits, summary) |
| `skills_list` | `true` | bool | Skill listing in session start context |
| `specs_and_concepts` | `true` | bool | Spec/concept listing, open comments, future items at session start |
| `session_context` | `true` | bool | Session orientation: branches, todos, plans, recent memory |
| `context_tracking_max` | `200000` | int/null | Max tokens for context tracking; `null` to disable |
| `mono_focus` | `true` | bool | Mono-repo sub-part focus injection at session start (reads external mapping) |
| `observation_images` | `true` | bool | Persist pasted images as named observation files in `memory/` |
| `git_root` | _(omitted)_ | string | Relative path to parent `.git` directory (for nested projects) |
| `git_prefix` | _(omitted)_ | string | Branch name prefix (for nested projects) |

String keys are only present when explicitly set (e.g. via `/eidos:init` git detection flow).

### 4. Apply Changes

How changes work depends on the setting type:

- **Boolean keys:** toggle (`true` ↔ `false`). Just the key name is enough.
- **Numeric/nullable keys:** user provides a value. E.g. `context_tracking_max 100000` or `context_tracking_max null`.
  If user provides just the key name, ask for the new value.
- **String keys:** user provides a value. E.g. `git_prefix my-project`.

Steps:
1. Apply the new value
2. Write the updated `.eidos-config.yaml` file
3. Commit the change (if git_workflow is enabled)
4. Show updated state

### 5. Config File Format

When writing `.eidos-config.yaml`, each setting gets a `#` comment on the line above:

```yaml
# branch-per-task, commit-per-action, --no-ff merges
git_workflow: true
# status report after each action
status_reporting: true
# eidos skill listing in session start context
skills_list: true
# spec/concept listing, future items at session start
specs_and_concepts: true
# session orientation: branches, todos, plans, recent memory
session_context: true
# max tokens for context window tracking (null to disable), used to warn about compaction early
context_tracking_max: 200000
# mono-repo sub-part focus injection at session start
mono_focus: true
# persist pasted images as named observation files in memory/
observation_images: true
```

Comments are preserved when changing values.
String keys appear below other keys, separated by a blank line:

```yaml
# persist pasted images as named observation files in memory/
observation_images: true

# nested project git
git_root: ../..
git_prefix: my-experiment
```

## Output

- Reads/writes: `.eidos-config.yaml`
- Shows current settings with change interface
