---
tldr: View and toggle eidos project settings
category: utility
---

# /eidos:config

View and toggle project settings.

## Usage

```
/eidos:config
/eidos:config <key>
```

## Instructions

### 1. Check Config

Read `.eidos-config.yaml` in the project root.

- **File missing or incomplete** (missing boolean keys): tell the user and offer to run `/eidos:init` to set up.
  If they accept, invoke `/eidos:init`. After init completes, continue to step 2.
  If they decline, stop — config can't be toggled without a complete file.
- **File complete:** continue to step 2.

Parse format: YAML key-value pairs.
- `key: true` = enabled
- `key: false` = disabled
- `key: value` = string value

### 2. Present Settings

Show all available settings with current values:

```
Eidos config (.eidos-config.yaml):

  git_workflow: true        # branch-per-task, commit-per-action, --no-ff merges
  status_reporting: true    # status report after each action
  skills_list: true         # skill listing in session start context
  specs_and_concepts: true  # spec/concept listing, open comments, future items at session start
  session_context: true     # session orientation: branches, todos, plans, recent memory

Toggle which? (e.g., "git_workflow" to disable it)
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
| `git_root` | _(omitted)_ | string | Relative path to parent `.git` directory (for nested projects) |
| `git_prefix` | _(omitted)_ | string | Branch name prefix (for nested projects) |

String keys are only present when explicitly set (e.g. via `/eidos:init` git detection flow).
The toggle interface applies to boolean keys only.

### 4. Apply Changes

When user selects items to toggle:
1. Flip the value (`true` ↔ `false`)
2. Write the updated `.eidos-config.yaml` file
3. Commit the change (if git_workflow is enabled)
4. Show updated state

### 5. Config File Format

When writing `.eidos-config.yaml`:

```yaml
git_workflow: true
status_reporting: true
skills_list: true
specs_and_concepts: true
session_context: true
```

Comments use `#` and are preserved when toggling values.
String keys appear below boolean keys, separated by a blank line:

```yaml
git_workflow: true
status_reporting: true

# nested project git
git_root: ../..
git_prefix: my-experiment
```

## Output

- Reads/writes: `.eidos-config.yaml`
- Shows current settings with toggle interface
