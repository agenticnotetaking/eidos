#!/usr/bin/env python3
"""Generate formatted skill list from SKILL.md frontmatter."""

import sys
from pathlib import Path

CATEGORY_ORDER = ["core", "planning", "observation", "utility"]
CATEGORY_LABELS = {
    "core": "Core Loop",
    "planning": "Planning",
    "observation": "Observation",
    "utility": "Utility",
}


def extract_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter fields from a skill file."""
    fields = {}
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return fields
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def main():
    plugin_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    skills_dir = plugin_root / "skills"

    if not skills_dir.is_dir():
        return

    # Collect skills grouped by category
    categories: dict[str, list[tuple[str, str]]] = {c: [] for c in CATEGORY_ORDER}

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        # Resolve symlink to get the actual file
        target = skill_md.resolve()
        if not target.exists():
            continue
        name = skill_md.parent.name
        fm = extract_frontmatter(target)
        tldr = fm.get("tldr", "")
        category = fm.get("category", "utility")
        if category in categories:
            categories[category].append((name, tldr))
        else:
            categories.setdefault("utility", []).append((name, tldr))

    # Format output
    lines = ["## Skills", ""]
    for cat in CATEGORY_ORDER:
        skills = categories.get(cat, [])
        if not skills:
            continue
        label = CATEGORY_LABELS.get(cat, cat.title())
        lines.append(f"### {label}")
        for name, tldr in skills:
            lines.append(f"- `/eidos:{name}` — {tldr}")
        lines.append("")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
