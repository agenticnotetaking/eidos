#!/usr/bin/env python3
"""Extract sample frames from a scene mp4 at timing-aware positions.

Usage:
    python video_frames.py <scene.mp4> <output_dir> [--srt <path>] [--partials <dir>] [--no-partials]

Default sample positions:
    - 0.5s after scene start (clamped to [0, duration])
    - 0.5s before scene end (clamped to [0, duration])
    - Each subtitle line start (if --srt given or sibling srt exists)
    - Each animation boundary from manim's partial movie files (auto-detected)

Animation boundaries give "resting state between animations" frames — the state
after an animation finishes and before the next one starts. This catches layout
and overlap issues that subtitle-time sampling can miss.

Auto-detection looks for partials at:
    <mp4_dir>/videos/<mp4_stem>/*/partial_movie_files/<ClassName>/partial_movie_file_list.txt
Override with --partials <dir> (directory containing partial_movie_file_list.txt).
Disable with --no-partials.

Positions are deduplicated within 0.25s of each other.
Frames are saved as `<seconds_with_hundredths>s.png` (e.g. `02.50s.png`).
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

SRT_START_RE = re.compile(
    r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+\d{2}:\d{2}:\d{2},\d{3}'
)
PARTIAL_LIST_FILE_RE = re.compile(r"^file\s+'(?:file:)?(.+)'\s*$")

DEDUPE_WINDOW_SEC = 0.25
EDGE_OFFSET_SEC = 0.5
MIN_SAMPLE_SEC = 0.2  # avoid sampling exactly at t=0 before opening animations settle
BOUNDARY_BACKOFF_SEC = 0.05  # sample slightly before an animation ends to avoid the first frame of the next


def ffprobe_duration(mp4: Path) -> float:
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', str(mp4)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def parse_srt_starts(srt: Path) -> list[float]:
    starts = []
    for m in SRT_START_RE.finditer(srt.read_text()):
        h, mm, s, ms = m.groups()
        starts.append(int(h) * 3600 + int(mm) * 60 + int(s) + int(ms) / 1000)
    return starts


def locate_partials(mp4: Path) -> Path | None:
    """Find manim's partial_movie_files dir for this scene, if it exists.

    Searches <mp4_dir>/videos/<stem>/*/partial_movie_files/*/partial_movie_file_list.txt.
    Returns the directory containing the list file, or None.
    """
    videos_dir = mp4.parent / 'videos' / mp4.stem
    if not videos_dir.is_dir():
        return None
    matches = list(videos_dir.glob('*/partial_movie_files/*/partial_movie_file_list.txt'))
    if not matches:
        return None
    # Prefer the first match; warn if multiple
    if len(matches) > 1:
        print(f'note: multiple partials dirs found, using {matches[0].parent}', file=sys.stderr)
    return matches[0].parent


def parse_partial_list(partials_dir: Path) -> list[Path]:
    """Read partial_movie_file_list.txt and return ordered list of partial mp4 paths.

    The list file contains one `file '<path>'` line per partial, in playback order.
    Comment lines (starting with #) are skipped.
    """
    list_file = partials_dir / 'partial_movie_file_list.txt'
    if not list_file.is_file():
        return []
    paths: list[Path] = []
    for line in list_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = PARTIAL_LIST_FILE_RE.match(line)
        if not m:
            continue
        p = Path(m.group(1))
        if not p.is_absolute():
            p = partials_dir / p
        if p.is_file():
            paths.append(p)
    return paths


def animation_boundaries(partials_dir: Path) -> list[float]:
    """Cumulative timestamps of animation endings from manim partials.

    Returns a list of timestamps in seconds where animation N ends (= animation N+1
    starts). Excludes t=0 (before anything happens) but includes the scene's total.
    """
    partials = parse_partial_list(partials_dir)
    boundaries: list[float] = []
    cum = 0.0
    for p in partials:
        cum += ffprobe_duration(p)
        boundaries.append(cum)
    return boundaries


def sample_positions(
    duration: float,
    subtitle_starts: list[float],
    anim_boundaries: list[float],
) -> list[float]:
    positions: set[float] = set()
    # Edge samples, clamped
    positions.add(min(EDGE_OFFSET_SEC, duration / 2))
    positions.add(max(duration - EDGE_OFFSET_SEC, duration / 2))
    # Subtitle starts, clamped away from t=0 (opening animations haven't settled)
    for t in subtitle_starts:
        if 0 <= t <= duration:
            positions.add(max(t, MIN_SAMPLE_SEC))
    # Animation boundaries, backed off slightly so we sample the still frame just
    # before the next animation begins (rather than landing on the first frame of it)
    for t in anim_boundaries:
        t = t - BOUNDARY_BACKOFF_SEC
        if MIN_SAMPLE_SEC <= t <= duration:
            positions.add(t)
    # Sort and dedupe within DEDUPE_WINDOW_SEC
    ordered = sorted(positions)
    out: list[float] = []
    for t in ordered:
        if not out or t - out[-1] >= DEDUPE_WINDOW_SEC:
            out.append(t)
    return out


def extract_frame(mp4: Path, timestamp: float, out_png: Path) -> None:
    subprocess.run(
        ['ffmpeg', '-y', '-v', 'error',
         '-ss', f'{timestamp:.3f}', '-i', str(mp4),
         '-vframes', '1', '-q:v', '2', str(out_png)],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(description='Extract timing-aware sample frames from a scene mp4')
    parser.add_argument('mp4', help='Scene mp4 path')
    parser.add_argument('output_dir', help='Directory to write frames into (created if missing)')
    parser.add_argument('--srt', help='Optional companion srt file; subtitle-line starts become extra sample positions')
    parser.add_argument('--partials', help='Directory with partial_movie_file_list.txt (auto-detected if omitted)')
    parser.add_argument('--no-partials', action='store_true', help='Skip animation-boundary sampling')
    args = parser.parse_args()

    mp4 = Path(args.mp4)
    if not mp4.is_file():
        print(f'mp4 not found: {mp4}', file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    duration = ffprobe_duration(mp4)
    subtitle_starts = []
    if args.srt:
        srt = Path(args.srt)
        if srt.is_file():
            subtitle_starts = parse_srt_starts(srt)
        else:
            print(f'srt not found, ignoring: {srt}', file=sys.stderr)
    elif mp4.with_suffix('.srt').is_file():
        subtitle_starts = parse_srt_starts(mp4.with_suffix('.srt'))

    anim_boundaries: list[float] = []
    if not args.no_partials:
        partials_dir = Path(args.partials) if args.partials else locate_partials(mp4)
        if partials_dir and partials_dir.is_dir():
            anim_boundaries = animation_boundaries(partials_dir)
        elif args.partials:
            print(f'partials dir not found: {args.partials}', file=sys.stderr)

    positions = sample_positions(duration, subtitle_starts, anim_boundaries)
    for t in positions:
        out_png = out_dir / f'{t:05.2f}s.png'
        extract_frame(mp4, t, out_png)
        print(f'Wrote {out_png}')


if __name__ == '__main__':
    main()
