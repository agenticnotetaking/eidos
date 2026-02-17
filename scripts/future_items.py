#!/usr/bin/env python3
"""Extract {[!]} and {[?]} future items from eidos spec files."""

import argparse
import re
import sys
from pathlib import Path

PLANNED_RE = re.compile(r'\{\[!\]\s*(.+?)\s*\}')
ASPIRATIONAL_RE = re.compile(r'\{\[\?\]\s*(.+?)\s*\}')
INLINE_CODE_RE = re.compile(r'`[^`]+`')


def strip_inline_code(line: str) -> str:
    return INLINE_CODE_RE.sub('', line)


def find_items(path: Path):
    results = []
    for md in sorted(path.rglob('*.md')):
        rel = md.relative_to(path)
        lines = md.read_text().splitlines()
        in_code_block = False
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            cleaned = strip_inline_code(line)
            for m in PLANNED_RE.finditer(cleaned):
                results.append(('!', str(rel), i, m.group(1)))
            for m in ASPIRATIONAL_RE.finditer(cleaned):
                results.append(('?', str(rel), i, m.group(1)))
    return results


def main():
    parser = argparse.ArgumentParser(description='Extract future items from eidos files')
    parser.add_argument('--path', default='eidos/', help='Path to scan (default: eidos/)')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f'Path not found: {path}', file=sys.stderr)
        sys.exit(1)

    items = find_items(path)

    if args.format == 'json':
        import json
        print(json.dumps([
            {'type': t, 'file': f, 'line': l, 'description': d}
            for t, f, l, d in items
        ], indent=2))
    else:
        if not items:
            print('No future items found.')
            return
        current_file = None
        for typ, file, line, desc in items:
            if file != current_file:
                if current_file is not None:
                    print()
                print(f'{file}:')
                current_file = file
            marker = '{[!]}' if typ == '!' else '{[?]}'
            print(f'  L{line} {marker} {desc}')


if __name__ == '__main__':
    main()
