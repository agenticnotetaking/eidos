#!/usr/bin/env python3
"""Find unresolved {{comments}} in eidos spec files."""

import argparse
import re
import sys
from pathlib import Path

COMMENT_OPEN = re.compile(r'\{\{')
COMMENT_CLOSE = re.compile(r'\}\}')
INLINE_CODE_RE = re.compile(r'`[^`]+`')
ESCAPED_COMMENT_RE = re.compile(r'\\{{.*?}}|\\{{')


def strip_inline_code(line: str) -> str:
    return INLINE_CODE_RE.sub('', line)


def strip_escaped_comments(line: str) -> str:
    """Remove \\{{ patterns so they aren't detected as open comments."""
    return ESCAPED_COMMENT_RE.sub('', line)


def find_comments(paths: list[Path], exclude: set[str] | None = None):
    exclude = exclude or set()
    results = []
    for path in paths:
        if not path.exists():
            continue
        for md in sorted(path.rglob('*.md')):
            if md.name in exclude:
                continue
            rel = md.relative_to(Path.cwd()) if md.is_relative_to(Path.cwd()) else md
            lines = md.read_text().splitlines()
            in_code_block = False
            in_comment = False
            comment_start = 0
            comment_lines = []

            for i, line in enumerate(lines, 1):
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue

                cleaned = strip_escaped_comments(strip_inline_code(line))

                if not in_comment:
                    if COMMENT_OPEN.search(cleaned):
                        in_comment = True
                        comment_start = i
                        comment_lines = [line]
                        remainder = cleaned.split('{{', 1)[1] if '{{' in cleaned else ''
                        if COMMENT_CLOSE.search(remainder):
                            text = '\n'.join(comment_lines)
                            text = re.sub(r'\{\{[*]?\s*', '', text)
                            text = re.sub(r'\s*\}\}', '', text)
                            results.append((str(rel), comment_start, text.strip()))
                            in_comment = False
                            comment_lines = []
                else:
                    comment_lines.append(line)
                    if COMMENT_CLOSE.search(line):
                        text = '\n'.join(comment_lines)
                        text = re.sub(r'\{\{[*]?\s*', '', text)
                        text = re.sub(r'\s*\}\}', '', text)
                        results.append((str(rel), comment_start, text.strip()))
                        in_comment = False
                        comment_lines = []

            if in_comment and comment_lines:
                text = '\n'.join(comment_lines)
                text = re.sub(r'\{\{[*]?\s*', '', text)
                results.append((str(rel), comment_start, text.strip()))

    return results


def main():
    parser = argparse.ArgumentParser(description='Find unresolved {{comments}} in eidos files')
    parser.add_argument('--path', nargs='+', default=['eidos/'], help='Paths to scan (default: eidos/)')
    parser.add_argument('--exclude', nargs='*', default=['human.md'], help='Filenames to skip (default: human.md)')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--cap', type=int, default=0, help='Max entries to show (0 = unlimited)')
    args = parser.parse_args()

    paths = [Path(p) for p in args.path]
    missing = [p for p in paths if not p.exists()]
    if missing:
        for p in missing:
            print(f'Path not found: {p}', file=sys.stderr)
        sys.exit(1)

    comments = find_comments(paths, exclude=set(args.exclude or []))

    if args.format == 'json':
        import json
        output = comments[:args.cap] if args.cap else comments
        print(json.dumps([
            {'file': f, 'line': l, 'text': t}
            for f, l, t in output
        ], indent=2))
    else:
        if not comments:
            print('No open comments found.')
            return
        cap = args.cap if args.cap else len(comments)
        shown = comments[:cap]
        current_file = None
        for file, line, text in shown:
            if file != current_file:
                if current_file is not None:
                    print()
                print(f'{file}:')
                current_file = file
            preview = text.split('\n')[0][:80]
            if len(text) > 80 or '\n' in text:
                preview += '...'
            print(f'  L{line} {preview}')
        remaining = len(comments) - len(shown)
        if remaining > 0:
            remaining_files = len(set(f for f, _, _ in comments[cap:]))
            print(f'\n{remaining} more in {remaining_files} file{"s" if remaining_files != 1 else ""}')


if __name__ == '__main__':
    main()
