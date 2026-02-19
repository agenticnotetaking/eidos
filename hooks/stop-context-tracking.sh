#!/usr/bin/env bash
# Eidos stop hook — injects [context used: X%] after each AI message.
# Gated by context_tracking config key.

set -euo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$0")")}"
READ_CONFIG="$PLUGIN_ROOT/scripts/read_config.sh"

# Only activate if project has an eidos/ folder
if [ ! -d "eidos/" ]; then
    exit 0
fi

# Check config
if [ "$(bash "$READ_CONFIG" "context_tracking" "true")" != "true" ]; then
    exit 0
fi

input=$(cat)

# Parse JSON with python3 (available everywhere, jq often isn't)
eval "$(python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
sa = str(data.get('stop_hook_active', False)).lower()
pct = data.get('context_window', {}).get('used_percentage', '')
if pct != '':
    pct = str(int(float(pct)))
print(f'stop_active={sa}')
print(f'pct={pct}')
" <<< "$input" 2>/dev/null)" || exit 0

# Prevent infinite loop: if stop hook already active, allow stop
if [ "$stop_active" = "true" ]; then
    exit 0
fi

if [ -n "$pct" ]; then
    echo "{\"decision\": \"block\", \"reason\": \"[context used: ${pct}%]\"}"
fi
