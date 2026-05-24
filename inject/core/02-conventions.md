## Handle Renames

Wiki links break when filenames change.
Always: `git mv` → update all `[[wiki links]]` → verify no broken links remain.

## Keep Names and TL;DRs Current

When a spec's content changes substantially, check whether the filename claim and TL;DR still reflect the actual content.
If they've drifted, update them — a misleading name or summary is worse than a missing one.
This applies to renames (`git mv` + wiki link updates) and to TL;DR lines inside the file.

## Context Includes TL;DRs

When adding rules to inject snippets or feature files that link to specs, include enough inline summary to act on without reading the linked file.
Specs are for rationale and edge cases — injected context should be self-sufficient for 90% of work.

## Brevity

Every sentence should earn its place — if removing it doesn't lose meaning, remove it.
Provide as much context as needed, but as little as possible.
Brevity is not terseness — terseness drops information; brevity earns every word.
See [[c - brevity - as much as needed but as little as possible]].

## "Should Have Happened" = Documentation Gap

When the user says something "should have happened" (missed expectation):
1. Fix the immediate issue
2. Check if a rule exists but was ambiguous → clarify it
3. If no rule existed → add one (context file, spec, or claim)

Corrective feedback implies a documentation improvement — that improvement is part of the fix, not optional cleanup.

## Questions vs Work

If the user is asking a question, just answer it — don't make file changes.
Only edit files when the task is clearly work (implementing, fixing, creating).
When uncertain, answer first, then offer to do the work as a follow-up.

## Markdown Styling

Prefer starting every sentence on a new line.
(Unless there are e.g. multiple sentences in brackets. Like here.)

## Numbered Lists

When presenting findings or options the user can act on selectively, use decimal notation:
top-level numbers for categories, decimals for items (1.1, 1.2, etc.).
After the list, prompt: `Which items to act on? (e.g., "1.1, 2.3")`
When only one option exists, auto-select it — unless the action is destructive.
Acted-upon items get `=>` wiki links to resulting files.
See [[spec - numbered lists - structured selectable output]].

## Seed Files

Any templated file (spec, plan, research, decision, etc.) can have `status: seed` in frontmatter.
A seed contains raw context — notes, links, brain dumps — that doesn't follow the template yet.
Seeds are valid input to skills: the skill uses the seed content as pre-answered context and structures it into template-compliant form.
See [[c - seed status marks files with unstructured context awaiting template compliance]].

## Naming

Files follow `prefix - claim.md` with prose claims.
Procedural files in `memory/` use compact timestamps: `prefix - yymmddhhmm - claim.md`.
When a `todo` is completed, rename to `solved` with updated timestamp: `git mv "memory/todo - ..." "memory/solved - yymmddhhmm - claim.md"` and update any wiki links.
**Always run `date '+%y%m%d%H%M'` to get the actual current time before creating any timestamped filename.**
Never guess or infer the time from conversation context — it's frequently wrong.
See [[spec - naming - prefixes structure filenames as prefix claim pairs]].

