#!/usr/bin/env bash
# Eidos session-start hook — per-unit dispatch.
#
# The harness caps each hook's output at 10K characters, so the full context
# cannot ship from a single hook. hooks.json registers one SessionStart entry
# per unit; each invocation emits exactly one budget-sized unit, gated by
# config where applicable. The harness concatenates the units into one block.
#
# Usage: session-start.sh <kind> [name]
#   preamble              truncation-recovery backstop + config-completeness notice
#   core <name>           inject/core/<name>.md (always loaded)
#   feature <name>        inject/feature/<name>.md (gated by <name>, - -> _)
#   dynamic <name>        computed section: mono | worktree
#                           | skills-list | specs-and-concepts | session-context
#   all (or no args)      every unit in injection order (for /eidos:debug-session-start)
#
# Silent when eidos/ is absent.

set -euo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$0")")}"
READ_CONFIG="$PLUGIN_ROOT/scripts/read_config.sh"

# Only activate if project has an eidos/ folder
[ -d "eidos/" ] || exit 0

KIND="${1:-all}"
NAME="${2:-}"

# gate <config_key> [default] — succeeds when the feature is enabled
gate() {
    local val
    val=$(bash "$READ_CONFIG" "$1" "${2:-true}")
    [ -n "$val" ] && [ "$val" != "false" ] && [ "$val" != "null" ]
}

emit_preamble() {
    local output=""
    output+="**IMPORTANT — read this first.**\n"
    output+="The eidos session-start context is injected as several blocks below. If any block shows a \"Full output saved to: <path>\" notice (i.e. it was truncated), READ that file in full before doing anything else — it holds eidos rules, skill routing, git workflow, and project state. With per-unit hooks this should not happen, but if it does, do not act on the truncated preview alone.\n\n"

    # Config completeness check
    local config_issue=""
    if [ ! -f ".eidos-config.yaml" ]; then
        config_issue="missing"
    else
        local missing_keys=""
        if [ -d "$PLUGIN_ROOT/inject/feature" ]; then
            for snippet in "$PLUGIN_ROOT/inject/feature/"*.md; do
                [ -f "$snippet" ] || continue
                local basename_name config_key
                basename_name=$(basename "$snippet" .md)
                config_key=$(echo "$basename_name" | tr '-' '_')
                if ! grep -qE "^${config_key}\s*:" ".eidos-config.yaml" 2>/dev/null; then
                    missing_keys+="$config_key "
                fi
            done
        fi
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
        output+="EIDOS: Config $config_issue — run \`/eidos:init\` to set up.\n"
    fi

    echo -e "$output"
}

emit_core() {
    local f="$PLUGIN_ROOT/inject/core/$NAME.md"
    if [ -f "$f" ]; then
        cat "$f"
    fi
}

emit_feature() {
    local f="$PLUGIN_ROOT/inject/feature/$NAME.md"
    [ -f "$f" ] || return 0
    local config_key
    config_key=$(echo "$NAME" | tr '-' '_')
    if gate "$config_key"; then
        cat "$f"
    fi
    return 0
}

emit_dynamic() {
    local output=""
    case "$NAME" in
        mono)
            gate mono_focus || return 0
            local MONO_READ repo_root mono_subpath
            MONO_READ="$PLUGIN_ROOT/scripts/mono_read.sh"
            repo_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
            mono_subpath=$(bash "$MONO_READ" "$repo_root" 2>/dev/null || true)
            if [ -n "$mono_subpath" ]; then
                output+="## Mono Focus\n\n"
                output+="**IMPORTANT:** You are in repo \`$repo_root\` but the user is currently working in \`$repo_root/$mono_subpath\`.\n"
                output+="Prefer file operations, commands, and navigation relative to \`$mono_subpath\`.\n\n"
                output+="**Say this at the very start of your first response (before anything else):**\n\n"
                output+="> Mono focus: **$mono_subpath** (\`$repo_root/$mono_subpath\`)\n"
            fi
            ;;
        worktree)
            gate worktrees || return 0
            local worktree_count
            worktree_count=$(git worktree list 2>/dev/null | wc -l | tr -d ' ')
            if [ "$worktree_count" -gt 1 ]; then
                local main_worktree current_dir
                main_worktree=$(git worktree list --porcelain 2>/dev/null | head -1 | sed 's/^worktree //')
                current_dir=$(pwd)
                if [ "$current_dir" != "$main_worktree" ]; then
                    local current_branch
                    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
                    output+="## Worktree\n\n"
                    output+="**Say this at the very start of your first response (before anything else):**\n\n"
                    output+="> Worktree: **$current_branch** (\`$current_dir\`)\n\n"
                fi
                local other_worktrees=""
                while IFS= read -r line; do
                    local wt_path wt_branch
                    wt_path=$(echo "$line" | awk '{print $1}')
                    wt_branch=$(echo "$line" | awk '{print $3}' | sed 's/\[//;s/\]//')
                    if [ "$wt_path" != "$current_dir" ]; then
                        if [ "$wt_path" = "$main_worktree" ]; then
                            other_worktrees+="  $wt_path    $wt_branch    (main worktree)\n"
                        else
                            local ahead
                            ahead=$(git rev-list --count main.."$wt_branch" 2>/dev/null || echo "?")
                            other_worktrees+="  $wt_path    $wt_branch    ($ahead commits ahead)\n"
                        fi
                    fi
                done < <(git worktree list 2>/dev/null)
                if [ -n "$other_worktrees" ]; then
                    if [ "$current_dir" != "$main_worktree" ]; then
                        output+="Other worktrees:\n$other_worktrees"
                    else
                        output+="**[session] Active worktrees:**\n$other_worktrees"
                    fi
                fi
            fi
            ;;
        skills-list)
            gate skills_list || return 0
            local skill_list
            skill_list=$(python3 "$PLUGIN_ROOT/scripts/skill_list.py" "$PLUGIN_ROOT" 2>/dev/null || true)
            [ -n "$skill_list" ] && output+="$skill_list"
            ;;
        specs-and-concepts)
            gate specs_and_concepts || return 0
            local concepts
            concepts=$(find eidos/ -maxdepth 1 \( -name 'c - *.md' -o -name 'spec - *.md' \) -exec basename {} .md \; 2>/dev/null | sort)
            if [ -n "$concepts" ]; then
                output+="**[eidos] Specs and concepts:**\n"
                while IFS= read -r name; do
                    output+="- [[$name]]\n"
                done <<< "$concepts"
                output+="\n"
            fi
            if [ -f "eidos/.WIP" ]; then
                output+="**[eidos] WIP mode** — partial spec coverage, unmapped code is expected.\n\n"
            fi
            local items
            items=$(python3 "$PLUGIN_ROOT/scripts/future_items.py" --path eidos/ 2>/dev/null || true)
            if [ -n "$items" ] && [ "$items" != "No future items found." ]; then
                local planned aspirational
                planned=$(echo "$items" | grep -c '{[!]}' || true)
                aspirational=$(echo "$items" | grep -c '{[?]}' || true)
                output+="**[eidos] Future items:** $planned planned, $aspirational aspirational\n"
            fi
            local recent
            recent=$(git log --oneline -3 -- eidos/ 2>/dev/null || true)
            if [ -n "$recent" ]; then
                output+="\n**[eidos] Recent spec changes:**\n$recent\n"
            fi
            ;;
        session-context)
            gate session_context || return 0
            local branches
            branches=$(git branch --sort=-committerdate --format='%(refname:short)' 2>/dev/null | head -5)
            if [ -n "$branches" ]; then
                output+="**[session] Recent branches:**\n"
                while IFS= read -r branch; do
                    output+="- \`$branch\`\n"
                done <<< "$branches"
            fi
            local todos
            todos=$(find memory/ -maxdepth 1 -name 'todo - *.md' 2>/dev/null | sort -r)
            if [ -n "$todos" ]; then
                output+="\n**[session] Open todos:**\n"
                while IFS= read -r todo; do
                    output+="- [[$(basename "$todo" .md)]]\n"
                done <<< "$todos"
            fi
            local wishes
            wishes=$(find memory/ -maxdepth 1 -name 'wish - *.md' 2>/dev/null | sort -r)
            if [ -n "$wishes" ]; then
                output+="\n**[session] Open wishes:**\n"
                while IFS= read -r wish; do
                    output+="- [[$(basename "$wish" .md)]]\n"
                done <<< "$wishes"
            fi
            local plans
            plans=$(find memory/ -maxdepth 1 -name 'plan - *.md' 2>/dev/null | sort -r)
            if [ -n "$plans" ]; then
                local open_plans=""
                while IFS= read -r plan; do
                    if grep -q '\- \[ \]' "$plan" 2>/dev/null; then
                        open_plans+="- [[$(basename "$plan" .md)]]\n"
                    fi
                done <<< "$plans"
                [ -n "$open_plans" ] && output+="\n**[session] Open plans:**\n$open_plans"
            fi
            local last_session
            last_session=$(find memory/ -maxdepth 1 -name 'session - *.md' 2>/dev/null | sort -r | head -1)
            if [ -n "$last_session" ]; then
                local session_name session_ts stale_note=""
                session_name=$(basename "$last_session" .md)
                session_ts=$(echo "$session_name" | sed -n 's/^session - \([0-9]\{10\}\) - .*/\1/p')
                if [ -n "$session_ts" ]; then
                    local yy mm dd hh mi session_epoch now_epoch age_days
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
            local recent_memory
            recent_memory=$(find memory/ -maxdepth 1 -name '*.md' \
                ! -name 'session - *' ! -name 'todo - *' ! -name 'wish - *' ! -name 'plan - *' ! -name 'human.md' \
                -mtime -7 2>/dev/null | sort -r | head -10)
            if [ -n "$recent_memory" ]; then
                output+="\n**[session] Recent memory (7d):**\n"
                while IFS= read -r mfile; do
                    output+="- [[$(basename "$mfile" .md)]]\n"
                done <<< "$recent_memory"
            fi
            ;;
        *) return 0 ;;
    esac
    if [ -n "$output" ]; then
        echo -e "$output"
    fi
    return 0
}

# Emit every unit in injection order (debugging / inspection).
emit_all() {
    local f
    "$0" preamble
    for f in "$PLUGIN_ROOT"/inject/core/*.md; do
        [ -f "$f" ] || continue
        "$0" core "$(basename "$f" .md)"
    done
    "$0" dynamic mono
    "$0" dynamic worktree
    for f in "$PLUGIN_ROOT"/inject/feature/*.md; do
        [ -f "$f" ] || continue
        "$0" feature "$(basename "$f" .md)"
    done
    "$0" dynamic skills-list
    "$0" dynamic specs-and-concepts
    "$0" dynamic session-context
}

case "$KIND" in
    preamble) emit_preamble ;;
    core)     emit_core ;;
    feature)  emit_feature ;;
    dynamic)  emit_dynamic ;;
    all)      emit_all ;;
    *)        exit 0 ;;
esac
