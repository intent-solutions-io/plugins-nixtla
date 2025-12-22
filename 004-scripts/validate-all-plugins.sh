#!/usr/bin/env bash
#
# Comprehensive Plugin Validation Script
# Validates all plugins in the repository or a specific plugin directory
#

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Determine target directory
TARGET_DIR="${1:-.}"

validate_markdown_frontmatter() {
    local md_file="$1"
    local errors=0

    if ! head -1 "$md_file" | grep -q "^---$"; then
        print_error "Missing frontmatter in $md_file"
        return 1
    fi

    local fm_block
    fm_block="$(awk 'NR==1{next} /^---$/{exit} {print}' "$md_file")"
    if [ -z "$(echo "$fm_block" | tr -d '[:space:]')" ]; then
        print_error "Empty frontmatter block in $md_file"
        errors=$((errors + 1))
    fi

    local fm_name
    fm_name="$(echo "$fm_block" | awk -F': ' '$1=="name"{print substr($0, index($0,$2))}' | head -1 | xargs || true)"
    if [ -z "$fm_name" ]; then
        print_error "Frontmatter missing required field 'name' in $md_file"
        errors=$((errors + 1))
    fi

    local fm_desc
    fm_desc="$(echo "$fm_block" | awk -F': ' '$1=="description"{print substr($0, index($0,$2))}' | head -1 | xargs || true)"
    if [ -z "$fm_desc" ]; then
        print_error "Frontmatter missing required field 'description' in $md_file"
        errors=$((errors + 1))
    fi

    return $errors
}

validate_plugin_json() {
    local plugin_json="$1"

    if [ ! -f "$plugin_json" ]; then
        print_error "plugin.json not found at $plugin_json"
        return 1
    fi

    # Check JSON syntax
    if ! jq empty "$plugin_json" 2>/dev/null; then
        print_error "Invalid JSON syntax in $plugin_json"
        return 1
    fi

    # Validate required fields
    local errors=0

    if ! jq -e '.name' "$plugin_json" > /dev/null 2>&1; then
        print_error "Missing 'name' field in $plugin_json"
        errors=$((errors + 1))
    fi

    if ! jq -e '.version' "$plugin_json" > /dev/null 2>&1; then
        print_error "Missing 'version' field in $plugin_json"
        errors=$((errors + 1))
    fi

    if ! jq -e '.description' "$plugin_json" > /dev/null 2>&1; then
        print_error "Missing 'description' field in $plugin_json"
        errors=$((errors + 1))
    fi

    if ! jq -e '.author.name' "$plugin_json" > /dev/null 2>&1; then
        print_error "Missing 'author.name' field in $plugin_json"
        errors=$((errors + 1))
    fi

    # Validate version format (semantic versioning)
    if [ "$errors" -eq 0 ]; then
        local version=$(jq -r '.version' "$plugin_json")
        if ! echo "$version" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$'; then
            print_error "Invalid version format: $version (expected semantic versioning)"
            errors=$((errors + 1))
        fi
    fi

    return $errors
}

validate_plugin_structure() {
    local plugin_dir="$1"
    local plugin_name=$(basename "$plugin_dir")
    local errors=0

    print_info "Validating plugin: $plugin_name"

    # Check for plugin.json
    if ! validate_plugin_json "$plugin_dir/.claude-plugin/plugin.json"; then
        errors=$((errors + 1))
    fi

    # Check manifest name matches directory
    if [ -f "$plugin_dir/.claude-plugin/plugin.json" ]; then
        local manifest_name
        manifest_name=$(jq -r '.name // empty' "$plugin_dir/.claude-plugin/plugin.json" 2>/dev/null || true)
        if [ -n "$manifest_name" ] && [ "$manifest_name" != "$plugin_name" ]; then
            print_error "plugin.json name '$manifest_name' does not match directory '$plugin_name'"
            errors=$((errors + 1))
        fi
    fi

    # Check for README.md
    if [ ! -f "$plugin_dir/README.md" ]; then
        print_error "README.md not found in $plugin_dir"
        errors=$((errors + 1))
    fi

    # Check for at least one component directory
    local has_component=false
    for component in commands agents skills hooks scripts mcp; do
        if [ -d "$plugin_dir/$component" ]; then
            print_info "  Found component: $component"
            has_component=true
        fi
    done

    if [ "$has_component" = false ]; then
        print_error "No component directories found (need at least one of: commands, agents, skills, hooks, scripts, mcp)"
        errors=$((errors + 1))
    fi

    # Validate markdown files in commands/agents
    local had_nullglob=0
    if shopt -q nullglob; then had_nullglob=1; fi
    shopt -s nullglob

    for cmd_file in "$plugin_dir"/commands/*.md; do
        if [ -f "$cmd_file" ]; then
            validate_markdown_frontmatter "$cmd_file" || errors=$((errors + 1))
        fi
    done

    for agent_file in "$plugin_dir"/agents/*.md; do
        if [ -f "$agent_file" ]; then
            validate_markdown_frontmatter "$agent_file" || errors=$((errors + 1))
        fi
    done

    if [ "$had_nullglob" -eq 0 ]; then
        shopt -u nullglob
    fi

    # Validate skills
    if [ -d "$plugin_dir/skills" ]; then
        for skill_dir in "$plugin_dir"/skills/*/; do
            if [ -d "$skill_dir" ]; then
                local skill_file="$skill_dir/SKILL.md"
                if [ ! -f "$skill_file" ]; then
                    print_error "SKILL.md not found in $skill_dir"
                    errors=$((errors + 1))
                else
                    if ! head -1 "$skill_file" | grep -q "^---$"; then
                        print_error "Missing frontmatter in $skill_file"
                        errors=$((errors + 1))
                    fi
                fi
            fi
        done
    fi

    # Validate hooks.json if hooks/ exists
    if [ -d "$plugin_dir/hooks" ]; then
        local hooks_json="$plugin_dir/hooks/hooks.json"
        if [ ! -f "$hooks_json" ]; then
            print_error "hooks/ exists but hooks.json not found in $plugin_dir/hooks"
            errors=$((errors + 1))
        else
            if ! jq empty "$hooks_json" 2>/dev/null; then
                print_error "Invalid JSON syntax in $hooks_json"
                errors=$((errors + 1))
            fi
        fi
    fi

    return $errors
}

# Main validation logic
main() {
    local total_errors=0
    local plugins_validated=0

    print_info "Starting plugin validation..."

    # Find plugin directories
    local plugins_root=""
    if [ -d "$TARGET_DIR/005-plugins" ]; then
        plugins_root="$TARGET_DIR/005-plugins"
    elif [ -d "$TARGET_DIR" ] && [ "$(basename "$TARGET_DIR")" = "005-plugins" ]; then
        plugins_root="$TARGET_DIR"
    fi

    if [ -n "$plugins_root" ]; then
        for plugin in "$plugins_root"/*/; do
            if [ -d "$plugin/.claude-plugin" ]; then
                validate_plugin_structure "${plugin%/}" || total_errors=$((total_errors + 1))
                plugins_validated=$((plugins_validated + 1))
            fi
        done
    elif [ -d "$TARGET_DIR/.claude-plugin" ]; then
        validate_plugin_structure "$TARGET_DIR" || total_errors=$((total_errors + 1))
        plugins_validated=$((plugins_validated + 1))
    else
        print_warn "No plugins found to validate (expected 005-plugins/* or a plugin directory with .claude-plugin/)"
    fi

    echo ""
    if [ "$total_errors" -eq 0 ]; then
        print_info "Validation complete: $plugins_validated plugin(s) validated successfully"
        exit 0
    else
        print_error "Validation failed: $total_errors error(s) found"
        exit 1
    fi
}

main "$@"
