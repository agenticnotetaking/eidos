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

**You can test:** open the dashboard, check the new widget renders
with live data. Try resizing the browser — layout should not break.
```

At phase boundaries (or when meaningful changes landed), include a **"You can test:"** section with concrete manual verification steps derived from what was actually built.
Focus on things that need human eyes — flows, visual behaviour, interactions.
Skip this section if the phase was purely structural (specs, config, refactoring with full test coverage).

After the status report, preview the next step:
```
**Next:** [brief description]
continue?
```

**IMPORTANT: Phase boundaries are mandatory checkpoints.**
After completing the last action of a plan phase, give the status report and **wait for explicit user confirmation** before starting the next phase.
Never continue into the next phase without go-ahead.
