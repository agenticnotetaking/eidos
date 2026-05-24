---
tldr: When searching a markdown corpus, disclose the cheapest informative layer first — file names, then tldr frontmatter, then heading outlines — and read full files only when a cheaper layer points there. An optional technique, not a default ritual.
---

# Progressive Disclosure — surface summaries before reading full files

## Target

Finding relevant information across a markdown corpus (`eidos/`, `memory/`, or any docs folder) by reading whole files eagerly is expensive: it burns context and buries the relevant passage in noise.
Progressive disclosure is the habit of reading the *cheapest* informative layer first and escalating only when it points somewhere specific.

This is a **technique to reach for**, not a rule that runs every time — see [[#When to use it]].

## Behaviour

### The disclosure ladder

Cheapest to most expensive; stop as soon as you have what you need:

1. **File listing** — eidos filenames are `prefix - claim` (see [[spec - naming - prefixes structure filenames as prefix claim pairs]]), so the name already states the claim. Listing a folder is often enough to locate the right file.
2. **Frontmatter `tldr`** — templated files carry a one-line `tldr:`. Batch-grep it (`grep -m1 '^tldr:'` across candidates) for a one-line summary of each without opening it.
3. **Heading outline** — `scripts/outline_eidos.py --path <file-or-dir>` prints heading structure with line numbers (text or JSON), so you see a file's shape and jump to the relevant section. Best for large files or batch outlines.
4. **Targeted read** — read only the file or line range the cheaper layers pointed at (e.g. `Read` with an offset taken from the outline's line numbers).

### When to use it

Reach for the ladder when:
- scanning an **unfamiliar or large** markdown corpus where relevance is uncertain,
- context budget is tight, or
- a sub-agent is doing a broad search and should report conclusions, not file dumps.

**Skip it — read directly — when:**
- you already know the target file,
- the corpus is small, or
- you need the full content anyway (the ladder would just add round-trips).

## Design

The eidos corpus is deliberately structured so each layer is informative on its own: claim-filenames, `tldr` frontmatter, section headings, and the wiki-link graph all act as summaries.
Progressive disclosure is the retrieval counterpart to that structure — it exists to *exploit* those affordances, which a generic file search wouldn't know to use (that the filename is a claim, or that every templated file has a greppable `tldr`).

It is intentionally optional.
Capable agents — and the harness's own search tooling — already explore cheaply by default; mandating a fixed list → frontmatter → headings → read ritual on every lookup would add round-trips and override depth-calibration that is usually better made in context.
The value here is *documenting the corpus-specific shortcuts so they are available* — especially to a spawned search sub-agent that lacks the session's context — not imposing a checklist.

The session-start specs/concepts index (file names plus their implicit claims, injected by the session-start hook) is itself an instance of progressive disclosure: it surfaces the cheapest layer up front, so deeper reads are by choice.

## Verification

- A broad search over `eidos/`/`memory/` can locate the relevant file from names + `tldr`s without reading full bodies
- `outline_eidos.py` returns headings + line numbers for a file or a directory
- The technique is documented as optional — no `core/` rule mandates it
- Skipping the ladder for a known target is explicitly sanctioned, not a violation

## Interactions

- [[spec - naming - prefixes structure filenames as prefix claim pairs]] — claim-filenames are the first (cheapest) disclosure layer
- [[spec - session context - composable snippet based context injection]] — the injected specs/concepts index is progressive disclosure at session start
- [[spec - externalise - persist insights beyond the conversation]] — the corpus worth disclosing exists because insights get written down

## Mapping

> [[scripts/outline_eidos.py]]
