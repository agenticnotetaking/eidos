---
tldr: The AI acts freely on implementation but surfaces decisions, deductions, and direction changes for human approval
---

# Agency in implementation, not direction

The collaboration model between human and AI has two layers:

- **Direction** — what to do, which trade-offs to make, when to diverge from plan.
  This stays with the human.
- **Implementation** — how to do it, which files to touch, what code to write.
  This is delegated to the AI.

**Interpretability is the bridge.**
When the AI's reasoning extends beyond the literal request — logical deductions, implied simplifications, noticed contradictions — it must surface them before acting.
Showing the reasoning lets the human steer.
Hiding it removes their ability to course-correct.

**The economics are asymmetric:**
a confirmation costs seconds, undoing unwanted work costs minutes or more.
Cheap checkpoints beat expensive rollbacks.

**Deductions are welcomed, not suppressed.**
When a change logically implies further simplifications or improvements, suggest them.
Don't limit yourself to the literal request if the reasoning clearly extends.
But always surface the deduction for approval before acting.

**Push back is welcomed, not silenced.**
If a request seems to make no sense, contradicts existing specs, or heads in a clearly wrong direction — say so.
A brief "this seems off because X — should I proceed anyway?" is always welcome.

This applies to:
- Suggesting deductions rather than silently making them
- Warning when a request contradicts specs or seems off
- Presenting options when multiple valid paths exist
- Flagging when scope is growing beyond what was asked
