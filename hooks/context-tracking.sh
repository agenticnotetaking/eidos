#!/usr/bin/env bash
# Eidos context tracking — injects [context used: X%] on each user prompt.
# Gated by context_tracking_max config key (value = max tokens, null = disabled).

set -euo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$0")")}"
READ_CONFIG="$PLUGIN_ROOT/scripts/read_config.sh"

# Only activate if project has an eidos/ folder
if [ ! -d "eidos/" ]; then
    exit 0
fi

# Check config — value is max token count, empty/null/false = disabled
max_tokens=$(bash "$READ_CONFIG" "context_tracking_max" "")
if [ -z "$max_tokens" ] || [ "$max_tokens" = "null" ] || [ "$max_tokens" = "false" ]; then
    exit 0
fi

input=$(cat)

# Read transcript and compute context usage percentage
pct=$(python3 -c "
import json, sys, os

data = json.loads(sys.stdin.read())

transcript = data.get('transcript_path', '')
if not transcript or not os.path.isfile(transcript):
    sys.exit(0)

last_usage = None
with open(transcript) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg = entry.get('message', {})
        if msg.get('role') == 'assistant' and 'usage' in msg:
            last_usage = msg['usage']

if not last_usage:
    sys.exit(0)

total = (
    last_usage.get('input_tokens', 0)
    + last_usage.get('cache_creation_input_tokens', 0)
    + last_usage.get('cache_read_input_tokens', 0)
)

max_tok = int(${max_tokens})
if total > 0 and max_tok > 0:
    print(int(total * 100 / max_tok))
" <<< "$input" 2>/dev/null) || exit 0

if [ -n "$pct" ]; then
    echo "[context used: ${pct}%]"
fi
