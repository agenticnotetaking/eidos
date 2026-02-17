# Status Reporting

After completing an action, report:

1. **Branch** — name and commit count
2. **Recent commits** — hash, message, files changed
3. **Summary** — what was done

Format: nested bullet lists, not tables.
File paths as clickable links: `[filename](<relative/path>)` (angle brackets for paths with spaces).

```
**Branch:** `task/my-feature` (2 commits)
- `abc1234` Add new feature
  - [feature.md](<memory/feature.md>)
- `def5678` Fix related issue
  - [feature.md](<memory/feature.md>)

**Summary:** Added feature and fixed related issue.
```

After the status report, preview the next step:
```
**Next:** [brief description]
continue?
```
