#!/usr/bin/env bash
# Eidos ping — agent surfaces session status to the human via OS notification.
# Usage: ping.sh <name> <type> <tldr...>
#
# Opt-in via `ping_macos: <path-to-eidos-ping-app>` in .eidos-config.yaml.
# When unset (the default), this script is a silent no-op so Linux / Windows
# users and macOS users who haven't installed the companion app aren't burdened.
#
# When set: writes a JSONL record to ~/Library/Application Support/eidos/pings.jsonl
# (consumed by the eidos-ping menubar app), and fires a Notification Center
# entry as a complementary persistent / audible surface.
#
# Companion app source: see ping_macos in .repos.yaml.
# See [[spec - ping skill - agent surfaces status via os notification]].

set -euo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"
READ_CONFIG="$PLUGIN_ROOT/scripts/read_config.sh"

# eidos guard — only activate when the project uses eidos
if [ ! -d "eidos/" ]; then
    exit 0
fi

# Opt-in gate — empty / unset means the user hasn't installed the companion.
binary_path=$(bash "$READ_CONFIG" "ping_macos" "")
if [ -z "$binary_path" ]; then
    exit 0
fi
# Expand leading tilde
binary_path="${binary_path/#\~/$HOME}"

if [ "$#" -lt 3 ]; then
    echo "usage: ping.sh <name> <type> <tldr...>" >&2
    exit 1
fi

name="$1"
type="$2"
shift 2
tldr="$*"

# AppleScript string-literal escaping: backslash first, then double quote
escape_as() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    printf '%s' "$s"
}

case "$(uname -s)" in
    Darwin)
        # Walk up the process tree to find the host app bundle (Terminal,
        # iTerm, Code, Cursor, etc.). The aggregator's "Open" button uses
        # this to refocus the agent's host app.
        host_app=""
        pid=$PPID
        steps=0
        while [ -n "$pid" ] && [ "$pid" != "1" ] && [ "$steps" -lt 30 ]; do
            exe=$(lsof -a -p "$pid" -d txt -Fn 2>/dev/null | awk '/^n/ {sub(/^n/, ""); print; exit}')
            if [[ "$exe" =~ /([^/]+)\.app/ ]]; then
                host_app="${BASH_REMATCH[1]}"
                break
            fi
            pid=$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' ')
            steps=$((steps + 1))
        done

        # Append a JSON Lines record to the shared queue. Python handles the
        # JSON escaping so the record is always well-formed.
        queue_dir="$HOME/Library/Application Support/eidos"
        mkdir -p "$queue_dir"
        queue_file="$queue_dir/pings.jsonl"

        # Soft cap: trim to the last 1000 records before appending so the
        # archive doesn't grow unbounded. The aggregator keeps its own
        # in-memory ring for the visible history.
        if [ -f "$queue_file" ]; then
            line_count=$(wc -l < "$queue_file" | tr -d ' ')
            if [ "$line_count" -gt 1000 ]; then
                tail -n 1000 "$queue_file" > "$queue_file.tmp" && mv "$queue_file.tmp" "$queue_file"
            fi
        fi

        python3 -c '
import json, sys, datetime
record = {
    "ts": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "name": sys.argv[1],
    "type": sys.argv[2],
    "tldr": sys.argv[3],
    "host_app": sys.argv[4],
    "cwd": sys.argv[5],
    "source_pid": int(sys.argv[6]),
}
print(json.dumps(record))
' "$name" "$type" "$tldr" "$host_app" "$PWD" "$$" >> "$queue_file"

        # Lazy-launch the configured menubar aggregator. If the binary is
        # missing at the configured path, fall through with a friendly stderr
        # message naming the install repo from .repos.yaml. The JSONL record
        # is already written, and the NC entry below will still fire.
        if ! pgrep -x eidos-ping-app >/dev/null 2>&1; then
            if [ -x "$binary_path" ]; then
                nohup "$binary_path" >/dev/null 2>&1 &
                disown 2>/dev/null || true
            else
                repo_url=$(grep -E "^ping_macos:" "$PLUGIN_ROOT/.repos.yaml" 2>/dev/null \
                    | sed 's/^ping_macos:[[:space:]]*//')
                echo "ping: ping_macos is set to '$binary_path' but no executable found there." >&2
                if [ -n "$repo_url" ]; then
                    echo "ping: install eidos-ping from: $repo_url" >&2
                fi
            fi
        fi

        # Notification Center entry — persistent record reviewable via the NC
        # sidebar, audible cue via Glass sound. Complementary to the popover.
        title="[$name] $type"
        title_esc=$(escape_as "$title")
        tldr_esc=$(escape_as "$tldr")
        osascript <<APPLESCRIPT
display notification "$tldr_esc" with title "$title_esc" sound name "Glass"
APPLESCRIPT
        ;;
    *)
        echo "ping: platform $(uname -s) not yet supported (macOS only in v1)" >&2
        exit 0
        ;;
esac
