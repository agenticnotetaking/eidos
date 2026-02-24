#!/bin/bash
# PreToolUse hook - Enforces "not on main" rule for Edit/Write operations
# Exit code 2 blocks the operation and shows stderr to Claude
# Respects git_workflow config — disabled = no enforcement

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$0")")}"

# Check if git_workflow is enabled
ENABLED=$(bash "$PLUGIN_ROOT/scripts/read_config.sh" "git_workflow" "true")
if [[ "$ENABLED" != "true" ]]; then
    exit 0
fi

# Read JSON input from stdin
INPUT=$(cat)

# Extract tool name
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Only check Edit and Write tools
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
    exit 0
fi

# Extract file path from tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Allow writes to files outside the repo or gitignored files
if [[ -n "$FILE_PATH" ]]; then
    REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
    if [[ -z "$REPO_ROOT" ]] || [[ "$FILE_PATH" != "$REPO_ROOT"* ]]; then
        exit 0
    fi
    if git check-ignore -q "$FILE_PATH" 2>/dev/null; then
        exit 0
    fi
fi

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
    echo "BLOCKED: Cannot edit files on '$BRANCH' branch. Create a task branch first: git checkout -b task/<description>" >&2
    exit 2
fi

exit 0