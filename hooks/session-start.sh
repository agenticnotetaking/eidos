#!/usr/bin/env bash
# Eidos session-start hook
# Composes context from core snippets, config-gated feature snippets, and dynamic project state.
# Silent when eidos/ is absent.

set -euo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$0")")}"
READ_CONFIG="$PLUGIN_ROOT/scripts/read_config.sh"

# Only activate if project has an eidos/ folder
if [ ! -d "eidos/" ]; then
    exit 0
fi

output=""

# --- Config completeness check ---
config_issue=""
if [ ! -f ".eidos-config.yaml" ]; then
    config_issue="missing"
else
    # Check if all known config keys are present
    missing_keys=""
    # Keys from feature snippets
    if [ -d "$PLUGIN_ROOT/inject/feature" ]; then
        for snippet in "$PLUGIN_ROOT/inject/feature/"*.md; do
            [ -f "$snippet" ] || continue
            basename_name=$(basename "$snippet" .md)
            config_key=$(echo "$basename_name" | tr '-' '_')
            if ! grep -qE "^${config_key}\s*:" ".eidos-config.yaml" 2>/dev/null; then
                missing_keys+="$config_key "
            fi
        done
    fi
    # Keys for dynamic sections
    for config_key in skills_list specs_and_concepts session_context; do
        if ! grep -qE "^${config_key}\s*:" ".eidos-config.yaml" 2>/dev/null; then
            missing_keys+="$config_key "
        fi
    done
    if [ -n "$missing_keys" ]; then
        config_issue="incomplete (missing: $missing_keys)"
    fi
fi

if [ -n "$config_issue" ]; then
    output+="**[eidos] Config $config_issue.** After the user's first message, tell them:\n"
    output+="EIDOS: Config $config_issue — run \`/eidos:init\` to set up.\n\n"
fi

# --- Core context (always loaded) ---
if [ -f "$PLUGIN_ROOT/inject/core.md" ]; then
    output+="$(cat "$PLUGIN_ROOT/inject/core.md")\n\n"
fi

# --- Feature snippets (config-gated) ---
if [ -d "$PLUGIN_ROOT/inject/feature" ]; then
    for snippet in "$PLUGIN_ROOT/inject/feature/"*.md; do
        [ -f "$snippet" ] || continue
        # Derive config key from filename: git-workflow.md → git_workflow
        basename=$(basename "$snippet" .md)
        config_key=$(echo "$basename" | tr '-' '_')
        enabled=$(bash "$READ_CONFIG" "$config_key" "true")
        if [ "$enabled" = "true" ]; then
            output+="$(cat "$snippet")\n\n"
        fi
    done
fi

# --- Dynamic: skill list from frontmatter (config-gated) ---
if [ "$(bash "$READ_CONFIG" "skills_list" "true")" = "true" ]; then
    skill_list=$(python3 "$PLUGIN_ROOT/scripts/skill_list.py" "$PLUGIN_ROOT" 2>/dev/null || true)
    if [ -n "$skill_list" ]; then
        output+="$skill_list\n\n"
    fi
fi

# --- Dynamic context: eidos state (config-gated) ---
if [ "$(bash "$READ_CONFIG" "specs_and_concepts" "true")" = "true" ]; then

    # Eidos concepts and specs
    concepts=$(find eidos/ -maxdepth 1 \( -name 'c - *.md' -o -name 'spec - *.md' \) -exec basename {} .md \; 2>/dev/null | sort)
    if [ -n "$concepts" ]; then
        output+="**[eidos] Specs and concepts:**\n"
        while IFS= read -r name; do
            output+="- [[$name]]\n"
        done <<< "$concepts"
        output+="\n"
    fi

    # WIP mode
    if [ -f "eidos/.WIP" ]; then
        output+="**[eidos] WIP mode** — partial spec coverage, unmapped code is expected.\n\n"
    fi

    # Future items summary
    items=$(python3 "$PLUGIN_ROOT/scripts/future_items.py" --path eidos/ 2>/dev/null || true)
    if [ -n "$items" ] && [ "$items" != "No future items found." ]; then
        planned=$(echo "$items" | grep -c '{[!]}' || true)
        aspirational=$(echo "$items" | grep -c '{[?]}' || true)
        output+="**[eidos] Future items:** $planned planned, $aspirational aspirational\n"
    fi

    # Recent eidos changes (last 3 commits touching eidos/)
    recent=$(git log --oneline -3 -- eidos/ 2>/dev/null || true)
    if [ -n "$recent" ]; then
        output+="\n**[eidos] Recent spec changes:**\n$recent\n"
    fi

fi

# --- Session orientation (config-gated) ---
if [ "$(bash "$READ_CONFIG" "session_context" "true")" = "true" ]; then

# Recent branches (last 5)
branches=$(git branch --sort=-committerdate --format='%(refname:short)' 2>/dev/null | head -5)
if [ -n "$branches" ]; then
    output+="\n**[session] Recent branches:**\n"
    while IFS= read -r branch; do
        output+="- \`$branch\`\n"
    done <<< "$branches"
fi

# Open todos
todos=$(find memory/ -maxdepth 1 -name 'todo - *.md' 2>/dev/null | sort -r)
if [ -n "$todos" ]; then
    output+="\n**[session] Open todos:**\n"
    while IFS= read -r todo; do
        name=$(basename "$todo" .md)
        output+="- [[$name]]\n"
    done <<< "$todos"
fi

# Open plans (with unchecked items)
plans=$(find memory/ -maxdepth 1 -name 'plan - *.md' 2>/dev/null | sort -r)
if [ -n "$plans" ]; then
    open_plans=""
    while IFS= read -r plan; do
        if grep -q '\- \[ \]' "$plan" 2>/dev/null; then
            name=$(basename "$plan" .md)
            open_plans+="- [[$name]]\n"
        fi
    done <<< "$plans"
    if [ -n "$open_plans" ]; then
        output+="\n**[session] Open plans:**\n$open_plans"
    fi
fi

# Last session file (most recent by filename sort)
last_session=$(find memory/ -maxdepth 1 -name 'session - *.md' 2>/dev/null | sort -r | head -1)
if [ -n "$last_session" ]; then
    session_name=$(basename "$last_session" .md)
    # Extract timestamp from filename (prefix - yymmddhhmm - claim)
    session_ts=$(echo "$session_name" | sed -n 's/^session - \([0-9]\{10\}\) - .*/\1/p')
    stale_note=""
    if [ -n "$session_ts" ]; then
        yy="${session_ts:0:2}"; mm="${session_ts:2:2}"; dd="${session_ts:4:2}"
        hh="${session_ts:6:2}"; mi="${session_ts:8:2}"
        session_epoch=$(date -j -f "%Y%m%d%H%M" "20${yy}${mm}${dd}${hh}${mi}" +%s 2>/dev/null || echo "0")
        now_epoch=$(date +%s)
        age_days=$(( (now_epoch - session_epoch) / 86400 ))
        if [ "$age_days" -gt 7 ]; then
            stale_note=" _(${age_days} days old — may not reflect recent work)_"
        fi
    fi
    output+="\n**[session] Last session:** [[$session_name]]${stale_note}\n"
fi

# Recent memory files (last 7 days, excluding session/todo/plan already shown)
recent_memory=$(find memory/ -maxdepth 1 -name '*.md' \
    ! -name 'session - *' ! -name 'todo - *' ! -name 'plan - *' ! -name 'human.md' \
    -mtime -7 2>/dev/null | sort -r | head -10)
if [ -n "$recent_memory" ]; then
    output+="\n**[session] Recent memory (7d):**\n"
    while IFS= read -r mfile; do
        name=$(basename "$mfile" .md)
        output+="- [[$name]]\n"
    done <<< "$recent_memory"
fi

fi  # end session_context gate

if [ -n "$output" ]; then
    echo -e "$output"
fi
