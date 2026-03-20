---
tldr: A seed file has the right name and prefix but contains raw context instead of template-compliant structure
---

# Seed Status

Any templated file (spec, plan, research, decision, reference, pull) can start as a seed.

A seed file:
- Has the correct prefix and naming (`spec - ...`, `plan - ...`, etc.)
- Contains `status: seed` in frontmatter
- Holds raw context — notes, links, brain dumps, copied content, conversation excerpts
- Does not follow its template's section structure
- Signals "this exists as intent/context but isn't structured yet"

## Why Seeds Exist

Sometimes context arrives before structure.
You know what a spec should be about, you have links and notes, but you're not ready to think through sections.
A seed captures that context in the right place with the right name, without forcing premature structure.

Seeds are better than not writing anything — the context is externalised and discoverable, even if unstructured.

## How Skills Handle Seeds

When a skill encounters a file with `status: seed`:
- **Don't reject it** — seeds are valid input
- **Offer to structure it** — use the seed's content as input to the skill's normal flow
- The seed content becomes context for Q&A, not something to preserve verbatim
- After structuring, update `status: seed` to the appropriate status (`active`, or remove for specs)

Examples:
- `/eidos:spec` given a seed spec → uses the raw content as answers to gather-context, skips questions the seed already covers
- `/eidos:plan` given a seed plan → uses the context to draft phases and actions
- `/eidos:push` given a seed spec → flags that the spec needs structuring before implementation
