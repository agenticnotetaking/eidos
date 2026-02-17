#!/usr/bin/env python3
"""Find spec mappings that point to files which no longer exist."""

import argparse
import re
import sys
from pathlib import Path

MAPPING_RE = re.compile(r'^>\s*\[\[(.+?)\]\]')


def find_orphans(eidos_path: Path, project_root: Path):
    results = []
    for md in sorted(eidos_path.rglob('*.md')):
        rel = md.relative_to(eidos_path)
        lines = md.read_text().splitlines()
        in_mapping = False
        in_code_block = False

        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            stripped = line.strip()

            if stripped.lower() == '## mapping':
                in_mapping = True
                continue
            if in_mapping and stripped.startswith('## '):
                in_mapping = False
                continue

            if not in_mapping:
                continue

            m = MAPPING_RE.match(stripped)
            if not m:
                continue

            target = m.group(1)

            # skip wiki links to .md files (those are spec cross-references, not code mappings)
            if target.endswith('.md') or '.' not in target.split('/')[-1]:
                # directory reference or md file — check relative to project root
                target_path = project_root / target
            else:
                # code file reference
                target_path = project_root / target

            if not target_path.exists():
                results.append((str(rel), i, target, str(target_path)))

    return results


def main():
    parser = argparse.ArgumentParser(description='Find orphaned mappings in eidos specs')
    parser.add_argument('--eidos-path', default='eidos/', help='Path to eidos specs (default: eidos/)')
    parser.add_argument('--project-root', default='.', help='Project root for resolving mapping targets (default: .)')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()

    eidos_path = Path(args.eidos_path)
    project_root = Path(args.project_root)

    if not eidos_path.exists():
        print(f'Path not found: {eidos_path}', file=sys.stderr)
        sys.exit(1)

    orphans = find_orphans(eidos_path, project_root)

    if args.format == 'json':
        import json
        print(json.dumps([
            {'spec': s, 'line': l, 'target': t, 'resolved_path': r}
            for s, l, t, r in orphans
        ], indent=2))
    else:
        if not orphans:
            print('No orphaned mappings found.')
            return
        current_file = None
        for spec, line, target, resolved in orphans:
            if spec != current_file:
                if current_file is not None:
                    print()
                print(f'{spec}:')
                current_file = spec
            print(f'  L{line} > [[{target}]] — not found')


if __name__ == '__main__':
    main()
