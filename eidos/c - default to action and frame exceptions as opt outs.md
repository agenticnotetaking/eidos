---
tldr: Framing "skip when trivial" produces better agent behaviour than "do when complex"
---

# Default to action and frame exceptions as opt-outs

When instructing an agent to conditionally perform an action, the framing determines which way it errs.

"Do X for complex cases" → agent defaults to skipping, errs on the side of not doing it.
"Only skip X for very simple cases" → agent defaults to doing it, errs on the side of action.

Both describe the same rule, but the default differs.
For actions that are cheap to do and costly to miss, frame the exception as an opt-out.
