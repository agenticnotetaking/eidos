#!/usr/bin/env python3
"""Extract heading structure with line numbers from eidos spec files."""

import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)')


def extract_headings(md: Path):
    lines = md.read_text().splitlines()
    headings = []
    in_code_block = False

    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            headings.append((i, level, text))

    return headings


def extract_outline(path: Path):
    results = []

    if path.is_file():
        headings = extract_headings(path)
        if headings:
            results.append((path.name, headings))
    else:
        for md in sorted(path.rglob('*.md')):
            rel = md.relative_to(path)
            headings = extract_headings(md)
            if headings:
                results.append((str(rel), headings))

    return results


def main():
    parser = argparse.ArgumentParser(description='Extract heading outlines from eidos files')
    parser.add_argument('--path', default='eidos/', help='Path to scan (default: eidos/)')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--max-depth', type=int, default=6, help='Maximum heading depth to show (default: 6)')
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f'Path not found: {path}', file=sys.stderr)
        sys.exit(1)

    outlines = extract_outline(path)

    if args.format == 'json':
        import json
        print(json.dumps([
            {
                'file': f,
                'headings': [
                    {'line': l, 'level': lv, 'text': t}
                    for l, lv, t in hs
                    if lv <= args.max_depth
                ]
            }
            for f, hs in outlines
        ], indent=2))
    else:
        if not outlines:
            print('No headings found.')
            return
        for file, headings in outlines:
            print(f'{file}:')
            for line, level, text in headings:
                if level > args.max_depth:
                    continue
                indent = '  ' * (level - 1)
                print(f'  L{line} {indent}{text}')
            print()


if __name__ == '__main__':
    main()
