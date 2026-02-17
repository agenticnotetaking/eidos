---
tldr: Create new skill from conversation
category: utility
---

# /eidos:toskill

Turn a discovered pattern into a reusable skill.

## Usage

```
/eidos:toskill [name]
```

## Instructions

1. If no name provided, ask what the skill should do
2. Extract the pattern from conversation
3. Create `skills/<name>/<name>.md` with:
   - tldr in frontmatter
   - Skill heading with `# /eidos:<name>`
   - Usage section
   - Instructions section
   - Output section
4. Create `skills/<name>/SKILL.md` symlink → `<name>.md`
5. Ask if a spec should also be created in `eidos/skills/`
6. Commit all files

## Output

- Creates: `skills/<name>/<name>.md` + SKILL.md symlink
- Optionally creates: `eidos/skills/spec - <name> - <claim>.md`
