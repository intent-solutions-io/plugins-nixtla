#!/usr/bin/env bash
#
# Doc-Filing v3.0 Compliance Cleanup Script
# ===========================================
#
# Purpose: Restructure nixtla project to comply with Document Filing System v3.0
# Reference: /home/jeremy/002-command-bible/DOCUMENT-FILING-STANDARD-v3.0.md
# Audit Report: 000-docs/036-AA-AUDT-directory-structure-audit-and-cleanup-plan.md
#
# Safety: Creates backup, uses Git branching, validates each phase
#

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="/home/jeremy/000-projects/nixtla"
cd "$PROJECT_ROOT"

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Header
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Nixtla Doc-Filing v3.0 Compliance Cleanup"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Pre-flight checks
log "Running pre-flight checks..."

# Check if in git repo
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    error "Not a git repository!"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    warning "You have uncommitted changes!"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create backup
log "Creating full backup..."
BACKUP_FILE="nixtla-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf "/tmp/$BACKUP_FILE" "$PROJECT_ROOT" 2>/dev/null || true
log "Backup created: /tmp/$BACKUP_FILE"

# Document current state
log "Documenting current structure..."
tree -L 3 -I 'node_modules|.venv|__pycache__|.git' > "structure-before-cleanup.txt" 2>/dev/null || {
    warning "tree command not available, skipping structure documentation"
}

# Create cleanup branch
log "Creating cleanup branch..."
BRANCH_NAME="cleanup/doc-filing-v3-compliance-$(date +%Y%m%d)"
git checkout -b "$BRANCH_NAME" || {
    warning "Branch already exists, using existing branch"
    git checkout "$BRANCH_NAME"
}

log "Working on branch: $BRANCH_NAME"
echo ""

# ============================================================================
# PHASE 1: Renumber Duplicate Docs (Priority: P0)
# ============================================================================

echo "─────────────────────────────────────────────────────────────"
log "Phase 1: Renumbering duplicate docs to 050-060 range..."
echo "─────────────────────────────────────────────────────────────"
echo ""

cd "$PROJECT_ROOT/000-docs"

# Renumber plugin spec series (002-012 duplicates → 050-060)
declare -A RENUMBER_MAP=(
    ["002-PP-PROD-nixtla-plugin-opportunities-report.md"]="050-PP-PROD-nixtla-plugin-opportunities-report.md"
    ["003-AT-ARCH-plugin-01-nixtla-cost-optimizer.md"]="051-AT-ARCH-plugin-01-nixtla-cost-optimizer.md"
    ["004-AT-ARCH-plugin-02-nixtla-vs-statsforecast-benchmark.md"]="052-AT-ARCH-plugin-02-nixtla-vs-statsforecast-benchmark.md"
    ["005-AT-ARCH-plugin-03-nixtla-roi-calculator.md"]="053-AT-ARCH-plugin-03-nixtla-roi-calculator.md"
    ["006-AT-ARCH-plugin-04-nixtla-airflow-operator.md"]="054-AT-ARCH-plugin-04-nixtla-airflow-operator.md"
    ["007-AT-ARCH-plugin-05-nixtla-dbt-package.md"]="055-AT-ARCH-plugin-05-nixtla-dbt-package.md"
    ["008-AT-ARCH-plugin-06-nixtla-snowflake-adapter.md"]="056-AT-ARCH-plugin-06-nixtla-snowflake-adapter.md"
    ["009-AT-ARCH-plugin-07-nixtla-anomaly-streaming-monitor.md"]="057-AT-ARCH-plugin-07-nixtla-anomaly-streaming-monitor.md"
    ["010-AT-ARCH-plugin-08-nixtla-migration-assistant.md"]="058-AT-ARCH-plugin-08-nixtla-migration-assistant.md"
    ["011-AT-ARCH-plugin-09-nixtla-forecast-explainer.md"]="059-AT-ARCH-plugin-09-nixtla-forecast-explainer.md"
    ["012-PP-PROD-nixtla-plugin-suite-master-summary.md"]="060-PP-PROD-nixtla-plugin-suite-master-summary.md"
)

for OLD_NAME in "${!RENUMBER_MAP[@]}"; do
    NEW_NAME="${RENUMBER_MAP[$OLD_NAME]}"

    if [ -f "$OLD_NAME" ]; then
        info "Renaming: $OLD_NAME → $NEW_NAME"
        git mv "$OLD_NAME" "$NEW_NAME"
    else
        warning "File not found: $OLD_NAME (skipping)"
    fi
done

log "Phase 1 complete: Plugin specs renumbered to 050-060 range"
git commit -m "fix(docs): renumber plugin specs to 050-060 range per Doc-Filing v3.0" || {
    warning "No changes to commit in Phase 1"
}
echo ""

# ============================================================================
# PHASE 2: Migrate claudes-docs/ to 000-docs/ (Priority: P0)
# ============================================================================

echo "─────────────────────────────────────────────────────────────"
log "Phase 2: Migrating claudes-docs/ to 000-docs/..."
echo "─────────────────────────────────────────────────────────────"
echo ""

cd "$PROJECT_ROOT"

if [ -d "claudes-docs" ]; then
    # Migration map
    declare -A CLAUDE_DOCS_MAP=(
        ["claudes-docs/claude-skills-implementation-summary.md"]="000-docs/061-AA-SUMM-claude-skills-implementation-summary.md"
        ["claudes-docs/educational-overview-enhancement.md"]="000-docs/062-UC-GUID-educational-overview-enhancement.md"
        ["claudes-docs/free-search-providers-implementation.md"]="000-docs/063-DC-DEVN-free-search-providers-implementation.md"
        ["claudes-docs/marketplace-implementation-summary.md"]="000-docs/064-AA-SUMM-marketplace-implementation-summary.md"
        ["claudes-docs/marketplace-setup-guide.md"]="000-docs/065-DR-GUID-marketplace-setup-guide.md"
        ["claudes-docs/nixtla-v020-release-session-summary.md"]="000-docs/066-OD-RELS-v0-2-0-release-session-summary.md"
    )

    for OLD_PATH in "${!CLAUDE_DOCS_MAP[@]}"; do
        NEW_PATH="${CLAUDE_DOCS_MAP[$OLD_PATH]}"

        if [ -f "$OLD_PATH" ]; then
            info "Moving: $OLD_PATH → $NEW_PATH"
            git mv "$OLD_PATH" "$NEW_PATH"
        else
            warning "File not found: $OLD_PATH (skipping)"
        fi
    done

    # Remove empty claudes-docs directory
    if [ -d "claudes-docs" ] && [ -z "$(ls -A claudes-docs)" ]; then
        info "Removing empty claudes-docs/ directory"
        rmdir "claudes-docs"
    fi

    log "Phase 2 complete: claudes-docs/ migrated to 000-docs/"
    git commit -m "fix(docs): migrate claudes-docs to 000-docs per Doc-Filing v3.0" || {
        warning "No changes to commit in Phase 2"
    }
else
    warning "claudes-docs/ directory not found (already cleaned?)"
fi
echo ""

# ============================================================================
# PHASE 3: Consolidate Root-Level Markdown Files (Priority: P2)
# ============================================================================

echo "─────────────────────────────────────────────────────────────"
log "Phase 3: Consolidating root markdown files to 000-docs/..."
echo "─────────────────────────────────────────────────────────────"
echo ""

cd "$PROJECT_ROOT"

# Root markdown migration map
declare -A ROOT_DOCS_MAP=(
    ["ARCHITECTURE.md"]="000-docs/067-AT-ARCH-project-architecture.md"
    ["ROADMAP.md"]="000-docs/068-PP-RMAP-project-roadmap.md"
    ["EDUCATIONAL_RESOURCES.md"]="000-docs/069-UC-GUID-educational-resources.md"
    ["GCP-SETUP-COMPLETE.md"]="000-docs/070-OD-GUID-gcp-setup-complete.md"
    ["MARKETPLACE_SETUP.md"]="000-docs/071-DR-GUID-marketplace-setup.md"
    ["SETUP-NIXTLA-PLAYGROUND.md"]="000-docs/072-OD-GUID-nixtla-playground-setup.md"
    ["CONTRIBUTORS.md"]="000-docs/073-MC-MEMO-contributors.md"
    ["DISCUSSIONS.md"]="000-docs/074-MC-GUID-discussions-guide.md"
    ["SUPPORT.md"]="000-docs/075-DR-GUID-support-guide.md"
    ["GITHUB_DESCRIPTION.txt"]="000-docs/076-MC-MEMO-github-description.txt"
)

for OLD_PATH in "${!ROOT_DOCS_MAP[@]}"; do
    NEW_PATH="${ROOT_DOCS_MAP[$OLD_PATH]}"

    if [ -f "$OLD_PATH" ]; then
        info "Moving: $OLD_PATH → $NEW_PATH"
        git mv "$OLD_PATH" "$NEW_PATH"
    else
        warning "File not found: $OLD_PATH (skipping)"
    fi
done

log "Phase 3 complete: Root markdown files consolidated"
git commit -m "refactor(docs): consolidate root markdown into 000-docs" || {
    warning "No changes to commit in Phase 3"
}
echo ""

# ============================================================================
# PHASE 4: Standardize Plugin Structure (Priority: P1)
# ============================================================================

echo "─────────────────────────────────────────────────────────────"
log "Phase 4: Standardizing plugin directory structure..."
echo "─────────────────────────────────────────────────────────────"
echo ""

cd "$PROJECT_ROOT/plugins"

# Plugin 1: nixtla-baseline-lab (flatten test directories)
if [ -d "nixtla-baseline-lab" ]; then
    cd "nixtla-baseline-lab"
    info "Standardizing nixtla-baseline-lab structure..."

    # Create tests/ if it doesn't exist
    [ ! -d "tests" ] && mkdir -p "tests"

    # Move test directories
    if [ -d "nixtla_baseline_csv_test" ]; then
        info "Moving nixtla_baseline_csv_test → tests/csv_test"
        git mv "nixtla_baseline_csv_test" "tests/csv_test" || mv "nixtla_baseline_csv_test" "tests/csv_test"
    fi

    if [ -d "nixtla_baseline_m4_test" ]; then
        info "Moving nixtla_baseline_m4_test → tests/m4_test"
        git mv "nixtla_baseline_m4_test" "tests/m4_test" || mv "nixtla_baseline_m4_test" "tests/m4_test"
    fi

    if [ -d "nixtla_test_custom" ]; then
        info "Moving nixtla_test_custom → tests/custom"
        git mv "nixtla_test_custom" "tests/custom" || mv "nixtla_test_custom" "tests/custom"
    fi

    cd "$PROJECT_ROOT/plugins"
fi

# Plugin 2: nixtla-baseline-m4 (rename slash-commands → commands)
if [ -d "nixtla-baseline-m4/slash-commands" ]; then
    info "Renaming slash-commands → commands in nixtla-baseline-m4"
    cd "nixtla-baseline-m4"
    git mv "slash-commands" "commands" || mv "slash-commands" "commands"
    cd "$PROJECT_ROOT/plugins"
fi

log "Phase 4 complete: Plugin structures standardized"
git add -A
git commit -m "refactor(plugins): standardize plugin directory structure" || {
    warning "No changes to commit in Phase 4"
}
echo ""

# ============================================================================
# PHASE 5: Archive Old Backups (Priority: P2)
# ============================================================================

echo "─────────────────────────────────────────────────────────────"
log "Phase 5: Archiving old backups..."
echo "─────────────────────────────────────────────────────────────"
echo ""

cd "$PROJECT_ROOT"

if [ -d "claude-code-plugins-plus/backups" ]; then
    # Create archive directory
    mkdir -p "archive"

    info "Moving backups to archive/backups-20251108/"
    git mv "claude-code-plugins-plus/backups" "archive/backups-20251108" || {
        mv "claude-code-plugins-plus/backups" "archive/backups-20251108"
    }

    log "Phase 5 complete: Backups archived"
    git add -A
    git commit -m "chore(archive): consolidate old plugin backups" || {
        warning "No changes to commit in Phase 5"
    }
else
    warning "Backups directory not found (already archived?)"
fi
echo ""

# ============================================================================
# POST-FLIGHT VALIDATION
# ============================================================================

echo "─────────────────────────────────────────────────────────────"
log "Running post-flight validation..."
echo "─────────────────────────────────────────────────────────────"
echo ""

cd "$PROJECT_ROOT"

# Check for duplicate NNN numbers
info "Checking for duplicate document numbers..."
DUPLICATES=$(find 000-docs/ -name "[0-9][0-9][0-9]-*.md" | sed 's/.*\/\([0-9][0-9][0-9]\)-.*/\1/' | sort | uniq -d)
if [ -n "$DUPLICATES" ]; then
    error "Duplicate document numbers found:"
    echo "$DUPLICATES"
else
    log "✅ No duplicate document numbers"
fi

# Check if claudes-docs exists
if [ -d "claudes-docs" ]; then
    error "❌ claudes-docs/ directory still exists!"
else
    log "✅ claudes-docs/ directory removed"
fi

# Document final state
info "Documenting final structure..."
tree -L 3 -I 'node_modules|.venv|__pycache__|.git' > "structure-after-cleanup.txt" 2>/dev/null || {
    warning "tree command not available, skipping structure documentation"
}

# Count files in 000-docs
DOC_COUNT=$(find 000-docs/ -maxdepth 1 -name "*.md" | wc -l)
log "Total documents in 000-docs/: $DOC_COUNT"

# Count root markdown files (excluding standard GitHub files)
ROOT_MD_COUNT=$(find . -maxdepth 1 -name "*.md" ! -name "README.md" ! -name "CLAUDE.md" ! -name "CONTRIBUTING.md" ! -name "CODE_OF_CONDUCT.md" ! -name "SECURITY.md" ! -name "CHANGELOG.md" | wc -l)
log "Non-standard markdown files in root: $ROOT_MD_COUNT"

echo ""
echo "═══════════════════════════════════════════════════════════════"
log "CLEANUP COMPLETE!"
echo "═══════════════════════════════════════════════════════════════"
echo ""

info "Summary:"
echo "  - Branch: $BRANCH_NAME"
echo "  - Backup: /tmp/$BACKUP_FILE"
echo "  - Phases completed: 5/5"
echo ""

info "Next steps:"
echo "  1. Review changes: git diff main..$BRANCH_NAME"
echo "  2. Review structure: cat structure-after-cleanup.txt"
echo "  3. Run tests: pytest (if applicable)"
echo "  4. Merge to main: git checkout main && git merge $BRANCH_NAME"
echo ""

info "To rollback:"
echo "  git checkout main"
echo "  git branch -D $BRANCH_NAME"
echo "  tar -xzf /tmp/$BACKUP_FILE"
echo ""

log "All cleanup phases completed successfully! 🎉"
