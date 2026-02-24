---
tldr: Bootstrap eidos folder structure for a new project
category: utility
---

# /eidos:init

Bootstrap the eidos folder structure in the current project.

## Usage

```
/eidos:init
```

## Instructions

### 1. Check and Create Folders

Create each target, reporting what was created vs what already existed:

| Target | Purpose |
|--------|---------|
| `eidos/` | Spec root — what the system should be |
| `memory/` | Procedural artifacts — how we got here |

For each:
- **Missing:** create the directory, report "created"
- **Exists:** report "already exists", continue

### 2. Create Seed File

Copy `copy/seed.md` (from the plugin directory) to `eidos/seed.md` if it does not exist.
If it exists, report "already exists".

### 3. Create Human Scratchpad

Copy `copy/human.md` (from the plugin directory) to `memory/human.md` if it does not exist.
If it exists, report "already exists".

### 4. Create or Complete Config

Check `.eidos-config.yaml`:

- **Missing:** create it with all default settings, report "created"
- **Exists but incomplete** (missing boolean keys): append missing keys with their defaults, report "updated (added: key1, key2)"
- **Complete:** report "already exists"

Default settings (with `#` comments above each key):

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

Use the format from [[skills/config/config.md]] §5.
When appending, preserve existing values and comments — only add what's missing.

### 5. Git Detection

After creating the config, check for a `.git` directory in the working directory.

**`.git` found locally:** skip this step — git is available.

**No `.git` found:** present options:

```
No .git found in this directory.

1 - Create fresh repository (git init here)
2 - Find parent (walk ancestor directories for .git)
3 - Disable git (set git_workflow: false)
```

**Option 1 — Create fresh:**
- Run `git init` in the working directory
- Continue to report/commit as normal

**Option 2 — Find parent:**
- Walk ancestor directories looking for `.git`
- If found, calculate relative path from cwd to the directory containing `.git`
- Ask whether branch names should use a prefix:
  ```
  Found .git at <path>.

  Branch prefix? (e.g. "my-experiment" → my-experiment/task/feature)
  Leave empty for no prefix.
  ```
- Write to `.eidos-config.yaml`:
  - `git_root: <relative-path>` (e.g. `../..`)
  - `git_prefix: <prefix>` (only if non-empty)
- If `.git` not found in any ancestor, fall back to offering options 1 and 3

**Option 3 — Disable git:**
- Set `git_workflow: false` in `.eidos-config.yaml`
- Skip the commit step

### 6. Report

Show what was created, what already existed, and git status:

```
Eidos initialised:

- eidos/              created
- eidos/seed.md       created
- memory/             already exists
- memory/human.md     created
- .eidos-config.yaml  created | updated (added: ...) | already exists
- git:                using parent repo (../../) with prefix "my-experiment"
```

Git line variants:
- `git: local .git found` — normal case
- `git: created fresh repository` — option 1
- `git: using parent repo (<path>) with prefix "<prefix>"` — option 2 with prefix
- `git: using parent repo (<path>)` — option 2 without prefix
- `git: disabled` — option 3

### 7. Commit

If git_workflow is enabled (or no config existed before init), commit all created files in a single commit.

## Output

- Creates: `eidos/`, `eidos/seed.md`, `memory/`, `memory/human.md`, `.eidos-config.yaml`
- Reports creation status for each target
