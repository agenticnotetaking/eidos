#!/usr/bin/env bash
# Read a config value from .eidos-config.yaml (YAML format)
# Usage: read_config.sh <key> [default]
# Returns the value for the key, or default if key absent or file missing.
#
# Format:
#   git_workflow: true
#   status_reporting: false
#   git_root: ../..
#   git_prefix: my-experiment

CONFIG_FILE=".eidos-config.yaml"
KEY="$1"
DEFAULT="${2-true}"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "$DEFAULT"
    exit 0
fi

# Find line matching key: value (ignoring comments and inline comments)
LINE=$(grep -E "^${KEY}\s*:" "$CONFIG_FILE" 2>/dev/null | head -1)

if [ -z "$LINE" ]; then
    echo "$DEFAULT"
    exit 0
fi

# Extract value after the colon, trim whitespace and inline comments
VALUE=$(echo "$LINE" | sed 's/^[^:]*:\s*//' | sed 's/\s*#.*//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

if [ -z "$VALUE" ]; then
    echo "$DEFAULT"
    exit 0
fi

echo "$VALUE"
