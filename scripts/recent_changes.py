#!/usr/bin/env python3
"""Show recently changed files in eidos/ and code via git log."""

import argparse
import subprocess
import sys
from pathlib import Path


def git_changed_files(days=None, commits=None):
    cmd = ['git', 'log', '--name-only', '--pretty=format:']
    if days is not None:
        cmd.append(f'--since={days} days ago')
    elif commits is not None:
        cmd.append(f'-{commits}')
    else:
        cmd.append('--since=7 days ago')

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'git error: {result.stderr.strip()}', file=sys.stderr)
        sys.exit(1)

    files = set()
    for line in result.stdout.splitlines():
        line = line.strip()
        if line:
            files.add(line)
    return sorted(files)


def categorise(files):
    eidos_files = []
    code_files = []
    memory_files = []
    other_files = []

    for f in files:
        if f.startswith('eidos/'):
            eidos_files.append(f)
        elif f.startswith('memory/'):
            memory_files.append(f)
        elif f.startswith('scripts/') or f.startswith('hooks/') or f.startswith('skills/'):
            code_files.append(f)
        elif not f.startswith('.'):
            code_files.append(f)
        else:
            other_files.append(f)

    return eidos_files, code_files, memory_files, other_files


def main():
    parser = argparse.ArgumentParser(description='Show recently changed files')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--days', type=int, help='Show changes from last N days')
    group.add_argument('--commits', type=int, help='Show changes from last N commits')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()

    files = git_changed_files(days=args.days, commits=args.commits)

    if args.format == 'json':
        import json
        eidos, code, memory, other = categorise(files)
        print(json.dumps({
            'eidos': eidos,
            'code': code,
            'memory': memory,
            'other': other,
        }, indent=2))
    else:
        if not files:
            scope = f'last {args.days} days' if args.days is not None else f'last {args.commits} commits' if args.commits is not None else 'last 7 days'
            print(f'No changes found ({scope}).')
            return

        eidos, code, memory, other = categorise(files)

        if eidos:
            print('eidos/ (specs):')
            for f in eidos:
                print(f'  {f}')

        if code:
            if eidos:
                print()
            print('code:')
            for f in code:
                print(f'  {f}')

        if memory:
            if eidos or code:
                print()
            print('memory/ (procedural):')
            for f in memory:
                print(f'  {f}')


if __name__ == '__main__':
    main()
