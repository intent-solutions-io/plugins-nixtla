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
        ((errors++))
    fi

    if ! jq -e '.version' "$plugin_json" > /dev/null 2>&1; then
        print_error "Missing 'version' field in $plugin_json"
        ((errors++))
    fi

    if ! jq -e '.description' "$plugin_json" > /dev/null 2>&1; then
        print_error "Missing 'description' field in $plugin_json"
        ((errors++))
    fi

    if ! jq -e '.author' "$plugin_json" > /dev/null 2>&1; then
        print_error "Missing 'author' field in $plugin_json"
        ((errors++))
    fi

    # Validate version format (semantic versioning)
    if [ "$errors" -eq 0 ]; then
        local version=$(jq -r '.version' "$plugin_json")
        if ! echo "$version" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$'; then
            print_error "Invalid version format: $version (expected semantic versioning)"
            ((errors++))
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
        ((errors++))
    fi

    # Check for README.md
    if [ ! -f "$plugin_dir/README.md" ]; then
        print_error "README.md not found in $plugin_dir"
        ((errors++))
    fi

    # Check for LICENSE
    if [ ! -f "$plugin_dir/LICENSE" ]; then
        print_warn "LICENSE file not found in $plugin_dir (recommended)"
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
        ((errors++))
    fi

    # Validate markdown files in commands/agents
    for cmd_file in "$plugin_dir"/commands/*.md 2>/dev/null; do
        if [ -f "$cmd_file" ]; then
            if ! head -1 "$cmd_file" | grep -q "^---$"; then
                print_error "Missing frontmatter in $cmd_file"
                ((errors++))
            fi
        fi
    done

    for agent_file in "$plugin_dir"/agents/*.md 2>/dev/null; do
        if [ -f "$agent_file" ]; then
            if ! head -1 "$agent_file" | grep -q "^---$"; then
                print_error "Missing frontmatter in $agent_file"
                ((errors++))
            fi
        fi
    done

    # Validate skills
    if [ -d "$plugin_dir/skills" ]; then
        for skill_dir in "$plugin_dir"/skills/*/; do
            if [ -d "$skill_dir" ]; then
                local skill_file="$skill_dir/SKILL.md"
                if [ ! -f "$skill_file" ]; then
                    print_error "SKILL.md not found in $skill_dir"
                    ((errors++))
                else
                    if ! head -1 "$skill_file" | grep -q "^---$"; then
                        print_error "Missing frontmatter in $skill_file"
                        ((errors++))
                    fi
                fi
            fi
        done
    fi

    return $errors
}

# Main validation logic
main() {
    local total_errors=0
    local plugins_validated=0

    print_info "Starting plugin validation..."

    # Find all plugin directories
    if [ -d "$TARGET_DIR/plugins" ]; then
        for category in "$TARGET_DIR"/plugins/*/; do
            if [ -d "$category" ]; then
                for plugin in "$category"*/; do
                    if [ -d "$plugin/.claude-plugin" ]; then
                        validate_plugin_structure "$plugin" || ((total_errors++))
                        ((plugins_validated++))
                    fi
                done
            fi
        done
    elif [ -d "$TARGET_DIR/.claude-plugin" ]; then
        # Single plugin directory
        validate_plugin_structure "$TARGET_DIR" || ((total_errors++))
        ((plugins_validated++))
    else
        print_warn "No plugins found to validate"
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