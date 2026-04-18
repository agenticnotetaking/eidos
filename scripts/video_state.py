#!/usr/bin/env python3
"""Parse a video project outline.md's stage checklist and report progress.

Two formats are supported:

**Colocated (new):** per-section inline stage triplets under each scene.

    ## Pipeline status

    - [ ] Research
    - [x] Outline
    - [ ] Merge

    ## Sections

    ### 1. Section name

    - **About:** ...
    - **Scenes:**
      - [[scenes/01-slug]]
        - [x] md
        - [ ] code
        - [ ] render

**Flat (legacy):** a single `## Stages` block with nested wiki-links.

    ## Stages

    - [x] Research — [[research/notes]]
    - [x] Outline — this document
    - [ ] Scenes
      - [[scenes/01]]

The parser auto-detects which format the outline uses.
"""

import argparse
import json
import re
import sys
from pathlib import Path


SCENE_STAGES = ('md', 'code', 'render')

# Headings
PIPELINE_HEADING_RE = re.compile(r'^##+\s+Pipeline\s+status\s*$', re.I)
SECTIONS_HEADING_RE = re.compile(r'^##+\s+Sections\s*$', re.I)
STAGES_HEADING_RE = re.compile(r'^##+\s+Stages\s*$', re.I)
SECTION_HEADING_RE = re.compile(r'^###+\s+(?P<name>.+?)\s*$')
H2_RE = re.compile(r'^##\s+\S')  # any level-2 heading (new section — ends current block)

# Scene-list landmark
SCENES_BULLET_RE = re.compile(r'^\s*- \*\*Scenes:\*\*\s*$', re.I)
SCENE_LINK_RE = re.compile(r'^\s+- \[\[(?P<link>[^\]]+)\]\]\s*(?:—\s*\[\[[^\]]+\]\])?\s*$')

# Generic checkbox
CHECKBOX_RE = re.compile(r'^(?P<indent>\s*)- \[(?P<mark>[ xX])\]\s+(?P<rest>.+?)\s*$')
WIKILINK_RE = re.compile(r'\[\[(?P<link>[^\]]+)\]\]')

# Flat-format stage line (legacy)
STAGE_RE = re.compile(r'^- \[(?P<mark>[ xX])\]\s+(?P<name>\S+)(?:\s+[—-]\s+(?P<trail>.+))?$')
NESTED_LINK_RE = re.compile(r'^\s+- \[\[(?P<link>[^\]]+)\]\]')


def detect_format(text: str) -> str | None:
    if re.search(r'^##+\s+Pipeline\s+status\s*$', text, re.M | re.I):
        return 'colocated'
    if re.search(r'^##+\s+Stages\s*$', text, re.M | re.I):
        return 'flat'
    return None


def parse_flat(text: str) -> dict:
    lines = text.splitlines()
    in_stages = False
    stages = []
    current = None
    for line in lines:
        if STAGES_HEADING_RE.match(line):
            in_stages = True
            continue
        if in_stages and line.startswith('## '):
            break
        if not in_stages:
            continue
        m = STAGE_RE.match(line)
        if m:
            current = {
                'name': m.group('name'),
                'done': m.group('mark').lower() == 'x',
                'links': [lm.group('link') for lm in WIKILINK_RE.finditer(m.group('trail') or '')],
            }
            stages.append(current)
            continue
        nm = NESTED_LINK_RE.match(line)
        if nm and current is not None:
            current['links'].append(nm.group('link'))

    nxt = None
    for s in stages:
        if not s['done']:
            nxt = s['name']
            break

    return {
        'format': 'flat',
        'next': nxt,
        'stages': stages,
    }


def parse_colocated(text: str) -> dict:
    lines = text.splitlines()
    global_stages: list[dict] = []
    sections: list[dict] = []

    mode: str | None = None  # 'pipeline' | 'sections' | None
    current_section = None
    current_scene = None
    in_scenes_list = False
    scene_indent: int | None = None  # indent of the scene-link bullets within a section's Scenes list

    for line in lines:
        if PIPELINE_HEADING_RE.match(line):
            mode = 'pipeline'
            continue
        if SECTIONS_HEADING_RE.match(line):
            mode = 'sections'
            current_section = None
            current_scene = None
            in_scenes_list = False
            continue
        # Any other H2 closes the current mode
        if H2_RE.match(line) and not (PIPELINE_HEADING_RE.match(line) or SECTIONS_HEADING_RE.match(line)):
            mode = None
            continue

        if mode == 'pipeline':
            m = CHECKBOX_RE.match(line)
            if m and not m.group('indent'):
                rest = m.group('rest')
                tm = re.match(r'^(?P<name>\S+)(?:\s+[—-]\s+(?P<trail>.+))?$', rest)
                if tm:
                    stage_name = tm.group('name')
                    trail = tm.group('trail') or ''
                else:
                    stage_name = rest.strip()
                    trail = ''
                global_stages.append({
                    'name': stage_name,
                    'done': m.group('mark').lower() == 'x',
                    'links': [lm.group('link') for lm in WIKILINK_RE.finditer(trail)],
                })
            continue

        if mode == 'sections':
            sm = SECTION_HEADING_RE.match(line)
            if sm:
                current_section = {
                    'name': sm.group('name').strip(),
                    'scenes': [],
                }
                sections.append(current_section)
                current_scene = None
                in_scenes_list = False
                scene_indent = None
                continue

            if current_section is None:
                continue

            if SCENES_BULLET_RE.match(line):
                in_scenes_list = True
                current_scene = None
                scene_indent = None
                continue

            if in_scenes_list:
                link_m = SCENE_LINK_RE.match(line)
                if link_m:
                    current_scene = {
                        'link': link_m.group('link'),
                        'md': False,
                        'code': False,
                        'render': False,
                    }
                    current_section['scenes'].append(current_scene)
                    scene_indent = len(line) - len(line.lstrip(' '))
                    continue

                cb_m = CHECKBOX_RE.match(line)
                if cb_m and current_scene is not None:
                    rest = cb_m.group('rest').strip()
                    first_token = rest.split(maxsplit=1)[0].lower() if rest else ''
                    if first_token in SCENE_STAGES:
                        current_scene[first_token] = cb_m.group('mark').lower() == 'x'
                        links = [lm.group('link') for lm in WIKILINK_RE.finditer(rest)]
                        if links:
                            key = f'{first_token}_links'
                            current_scene.setdefault(key, []).extend(links)
                    continue

                # Non-list / non-checkbox line at a shallower indent ends the scenes list
                stripped = line.rstrip()
                if stripped and not stripped.startswith((' ', '\t', '-')):
                    in_scenes_list = False

    nxt = _next_colocated(global_stages, sections)

    return {
        'format': 'colocated',
        'next': nxt,
        'global_stages': global_stages,
        'sections': sections,
    }


def _next_colocated(global_stages: list[dict], sections: list[dict]) -> dict | None:
    def find(name):
        for s in global_stages:
            if s['name'].lower() == name.lower():
                return s
        return None

    research = find('Research')
    outline = find('Outline')
    merge = find('Merge')

    if research is not None and not research['done']:
        return {'kind': 'global', 'name': research['name']}
    if outline is not None and not outline['done']:
        return {'kind': 'global', 'name': outline['name']}

    for section in sections:
        for scene in section['scenes']:
            for stage in SCENE_STAGES:
                if not scene[stage]:
                    return {
                        'kind': 'scene-stage',
                        'section': section['name'],
                        'scene': scene['link'],
                        'stage': stage,
                    }

    if merge is not None and not merge['done']:
        return {'kind': 'global', 'name': merge['name']}

    return None


def parse_outline(path: Path) -> dict | None:
    text = path.read_text()
    fmt = detect_format(text)
    if fmt == 'colocated':
        return parse_colocated(text)
    if fmt == 'flat':
        return parse_flat(text)
    return None


def render_text(result: dict) -> str:
    out: list[str] = []
    if result['format'] == 'flat':
        for s in result['stages']:
            mark = '[x]' if s['done'] else '[ ]'
            trail = ''
            if s['links']:
                trail = ' — ' + ', '.join(s['links'])
            out.append(f'{mark} {s["name"]}{trail}')
        out.append('')
        nxt = result['next']
        out.append(f'Next: {nxt}' if nxt else 'All stages complete.')
    else:
        for s in result['global_stages']:
            mark = '[x]' if s['done'] else '[ ]'
            trail = ''
            if s['links']:
                trail = ' — ' + ', '.join(s['links'])
            out.append(f'{mark} {s["name"]}{trail}')
        out.append('')
        for section in result['sections']:
            out.append(f"### {section['name']}")
            for scene in section['scenes']:
                out.append(f"  [[{scene['link']}]]")
                for stage in SCENE_STAGES:
                    mark = '[x]' if scene[stage] else '[ ]'
                    out.append(f"    {mark} {stage}")
            out.append('')
        nxt = result['next']
        if nxt is None:
            out.append('All stages complete.')
        elif nxt['kind'] == 'global':
            out.append(f"Next: {nxt['name']}")
        else:
            out.append(f"Next: {nxt['stage']} of {nxt['scene']} (section: {nxt['section']})")
    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser(description='Parse a video outline stage checklist')
    parser.add_argument('outline', help='Path to outline.md (or project dir containing outline.md)')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()

    p = Path(args.outline)
    if p.is_dir():
        p = p / 'outline.md'
    if not p.is_file():
        print(f'outline.md not found: {p}', file=sys.stderr)
        sys.exit(1)

    result = parse_outline(p)
    if result is None:
        print(f'No recognized stage structure in {p} — expected "## Pipeline status" or "## Stages"', file=sys.stderr)
        sys.exit(2)

    if args.format == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(render_text(result))


if __name__ == '__main__':
    main()
