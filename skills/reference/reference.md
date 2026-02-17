---
tldr: Capture or research external concepts the project relies on
category: observation
---

# /eidos:reference

Curate external knowledge that the project depends on but doesn't own.

## Usage

```
/eidos:reference [concept or topic]
```

## Instructions

### 1. Clarify the Concept

If the topic is broad, use AskUserQuestion to narrow scope:
- What specific concept or technology?
- How does the project use it?
- How deep should we go?

If the concept is already clear, proceed.

### 2. Check for Existing References

Search `eidos/` for existing reference docs on this topic.
If one exists, offer to update it rather than creating a duplicate.

### 3. Determine Mode

Two modes based on what the user provides:

**Research mode** (default): The user names a concept — investigate it.
- Search web for authoritative sources, documentation, key explanations
- Search codebase and eidos/memory for how it's already used
- Gather enough to write a useful reference

**Capture mode**: The user provides content or context — structure it.
- User has the knowledge already (from conversation, docs they've read, experience)
- Structure it into the template format
- Ask clarifying questions to fill gaps

### 4. Distil into Project Terms

Read the template: [[template - reference - curated external knowledge for project use]]

Write the reference in the project's own words:
- **What It Is** — core definition tuned to project usage, not a Wikipedia entry
- **Key Points** — the 20% that covers 80%, project-relevant gotchas
- **How We Use It** — concrete connections to specs, code, decisions (wiki links)
- **Sources** — where to go for deeper reading

The reference should be self-sufficient for daily use.
Sources are for verification and deep dives, not required reading.

### 5. Ask Before Writing

Before creating the file, present a brief outline:
- Proposed filename claim
- Key points that will be covered
- Any connections to existing specs

Get confirmation, then create.

### 6. Create Reference File

Create `eidos/reference - <claim>.md` following the template.
Commit immediately.

### 7. Present and Offer Next Steps

```
Reference created: [[reference - <claim>]]

Options:
1 - Link from relevant specs (update How We Use It / Interactions sections)
2 - Research deeper on [specific aspect]
3 - Done for now
```

## Output

- Creates: `eidos/reference - <claim>.md`
- Location: `eidos/` (intentional, timeless)
- No timestamp (stable knowledge, not point-in-time)
