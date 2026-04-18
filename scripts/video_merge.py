#!/usr/bin/env python3
"""Merge per-scene mp4 + srt files into final.mp4 + final.srt (+ final-sub.mp4).

Usage:
    python video_merge.py <project_dir>

Expects:
    <project_dir>/renders/NN-*.mp4   # per-scene renders (sorted by NN prefix)
    <project_dir>/renders/NN-*.srt   # optional per-scene subtitles

Produces:
    <project_dir>/final.mp4          # silent, no burned subtitles
    <project_dir>/final.srt          # only if any .srt files exist
    <project_dir>/final-sub.mp4      # only if final.srt exists — subtitles burned in
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SRT_TIME_RE = re.compile(r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})')


def ffprobe_duration(mp4: Path) -> float:
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', str(mp4)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def ms_to_srt(ms: int) -> str:
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def srt_to_ms(h: str, m: str, s: str, ms: str) -> int:
    return int(h) * 3600_000 + int(m) * 60_000 + int(s) * 1000 + int(ms)


def shift_srt(srt_text: str, offset_ms: int, start_index: int) -> tuple[str, int]:
    """Return (shifted srt text, next index)."""
    lines = srt_text.splitlines()
    out = []
    idx = start_index
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().isdigit():
            out.append(str(idx))
            idx += 1
            i += 1
            continue
        m = SRT_TIME_RE.match(line.strip())
        if m:
            a = srt_to_ms(*m.group(1, 2, 3, 4)) + offset_ms
            b = srt_to_ms(*m.group(5, 6, 7, 8)) + offset_ms
            out.append(f'{ms_to_srt(a)} --> {ms_to_srt(b)}')
            i += 1
            continue
        out.append(line)
        i += 1
    # ensure trailing blank line between blocks
    result = '\n'.join(out).rstrip() + '\n'
    return result, idx


def concat_mp4(scene_mp4s: list[Path], final: Path) -> None:
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
        list_path = Path(f.name)
        for mp4 in scene_mp4s:
            # escape single quotes per ffmpeg concat spec
            escaped = str(mp4.resolve()).replace("'", r"'\''")
            f.write(f"file '{escaped}'\n")
    try:
        subprocess.run(
            ['ffmpeg', '-y', '-f', 'concat', '-safe', '0',
             '-i', str(list_path), '-c', 'copy', str(final)],
            check=True,
        )
    finally:
        list_path.unlink(missing_ok=True)


def burn_subtitles(project: Path, final_mp4: Path, final_srt: Path, out_mp4: Path) -> None:
    """Produce a copy of final.mp4 with final.srt burned into the pixels."""
    subprocess.run(
        ['ffmpeg', '-y', '-v', 'error',
         '-i', final_mp4.name,
         '-vf', f'subtitles={final_srt.name}',
         '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
         out_mp4.name],
        check=True,
        cwd=str(project),
    )


def merge_srt(scenes: list[tuple[Path, float]], final: Path) -> bool:
    """scenes: list of (scene_mp4, duration). Merge sibling .srt by offsetting."""
    blocks = []
    idx = 1
    offset_ms = 0
    any_srt = False
    for mp4, dur in scenes:
        srt = mp4.with_suffix('.srt')
        if srt.is_file():
            any_srt = True
            shifted, idx = shift_srt(srt.read_text(), offset_ms, idx)
            blocks.append(shifted.rstrip())
        offset_ms += int(round(dur * 1000))
    if not any_srt:
        return False
    final.write_text('\n\n'.join(blocks) + '\n')
    return True


def main():
    parser = argparse.ArgumentParser(description='Merge per-scene mp4 + srt into final output')
    parser.add_argument('project', help='Project directory (contains renders/)')
    args = parser.parse_args()

    project = Path(args.project)
    renders = project / 'renders'
    if not renders.is_dir():
        print(f'renders/ not found in {project}', file=sys.stderr)
        sys.exit(1)

    scene_mp4s = sorted(p for p in renders.glob('*.mp4') if p.is_file())
    if not scene_mp4s:
        print(f'No scene mp4s in {renders}', file=sys.stderr)
        sys.exit(1)

    durations = [ffprobe_duration(p) for p in scene_mp4s]
    scenes = list(zip(scene_mp4s, durations))

    final_mp4 = project / 'final.mp4'
    concat_mp4(scene_mp4s, final_mp4)
    print(f'Wrote {final_mp4}')

    final_srt = project / 'final.srt'
    if merge_srt(scenes, final_srt):
        print(f'Wrote {final_srt}')
        final_sub_mp4 = project / 'final-sub.mp4'
        burn_subtitles(project, final_mp4, final_srt, final_sub_mp4)
        print(f'Wrote {final_sub_mp4}')
    else:
        print('No per-scene .srt files found; skipped final.srt and final-sub.mp4')


if __name__ == '__main__':
    main()
