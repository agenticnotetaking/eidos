---
tldr: Stop spiraling and hand off to the user with actionable next steps
category: utility
---

# /eidos:spiral

The user is telling you that you're spiraling — repeatedly trying things that aren't working, whether that's terminal commands, code fixes, or debugging attempts.

## Instructions

1. **Stop immediately.** Do not retry, try another variation, or make another speculative attempt.
2. **Summarise** what you were trying to do, what you tried, and what went wrong (briefly).
3. **Hand off** using whichever approach fits the situation:

### Terminal / environment failures
- **Pasteable command:** give the user a command they can run in their own terminal, then share the output with you.
- **Diagnostic script:** write a small script that includes debugging output (env vars, paths, versions, error details), make it executable, and ask the user to run it and paste back the results.

### Code / bug fix failures
- **Logging:** suggest adding targeted logging to narrow the cause — specify exactly where and what to log.
- **Debug overlay:** in UI contexts, suggest a togglable debug overlay that encodes diagnostic info (state tooltips, debug panel, visible bounding boxes).
- **Isolation script:** suggest a small standalone script or test that reproduces the issue outside the full system.

### General
- **Present options:** if multiple approaches exist, list them and ask the user which to try.
- **Ask for help:** describe what information you'd need to make progress and ask the user to provide it.

4. **Wait** for the user's response before continuing.

## Example handoffs

**Pasteable command:**
> Could you run this and paste the output?
> ```
> node -e "console.log(process.env.PATH)" && which npx && npx --version
> ```

**Diagnostic script:**
> I wrote `debug-build.sh` — could you run it?
> ```
> chmod +x debug-build.sh && ./debug-build.sh
> ```
> It checks toolchain versions and prints the failing step with verbose output.

**Logging suggestion:**
> I've tried X and Y but can't tell where it breaks.
> Can I add a `console.log` in `handleSubmit` at line 45 to print the form state before validation?

**Presenting options:**
> I've tried the obvious fix and it didn't work. I see three possible causes:
> 1. State race condition in the effect
> 2. Stale closure over the callback
> 3. Missing dependency in the memo
> Which should I dig into first?
