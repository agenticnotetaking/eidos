---
tldr: Extract and persist a claim from conversation context
category: core
---

# /eidos:claim

Capture a specific learning, principle, or convention as a claim file.
Claims are lightweight — a name, a sentence, and enough prose to be self-sufficient.

## Usage

```
/eidos:claim [topic or insight]
```

## Instructions

### 1. Identify the Claim

If the user gave a topic, use it.
If not, look at recent conversation — what was clarified, decided, or learned?
Ask only if the claim isn't clear from context.

The claim should be a **single, focused insight** — not a feature (that's a spec) or a task (that's a todo).
Good claims: principles, conventions, architectural decisions, naming rules, "we tried X and Y works better".

### 2. Gather Context

Quick scan for related artifacts:
- Existing claims in `eidos/` that overlap or relate
- Specs that might reference this claim
- Conversation context that motivated it

If a closely related claim already exists, surface it — the user may want to update rather than create.

### 3. Name the Claim

Filename: `c - <claim>.md` where `<claim>` is a prose sentence.
The name IS the claim — it should be readable and self-sufficient.
Check [[spec - naming - prefixes structure filenames as prefix claim pairs]] for conventions.

### 4. Write the Claim

Structure depends on complexity:

**Simple principle** (most claims):
```markdown
---
tldr: One-sentence summary
---

# [Claim as title]

[Prose — why this matters, when it applies, what it replaces or clarifies.]
[Wiki links to related specs or claims.]
```

**Complex convention** (when the claim has rules, examples, or interactions):
```markdown
---
tldr: One-sentence summary
---

# [Claim as title]

[Opening paragraph.]

## Convention / Behaviour

[Rules, patterns, examples.]

## Interactions

- [[related spec or claim]]
```

Only include sections that earn their place — most claims are 5-15 lines.

Write directly to `eidos/c - <claim>.md`.
Don't present a draft first — the user sees the diff and can request changes.
Commit immediately.

### 5. Offer Next Steps

```
Claim created: [[c - <claim>]]

Options:
1 - Weave wiki links into related specs with /eidos:weave
2 - Done
```

## Output

- Creates: `eidos/c - <claim>.md`
