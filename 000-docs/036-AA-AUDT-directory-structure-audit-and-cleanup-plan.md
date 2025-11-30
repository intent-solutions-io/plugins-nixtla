# Directory Structure Audit & Cleanup Plan
**Project**: Nixtla Claude Code Plugins
**Created**: 2025-11-30
**Status**: 🚨 CRITICAL - Multiple Doc-Filing v3.0 Violations
**Priority**: P0 - Immediate Cleanup Required

---

## Executive Summary

**Violations Identified**: 6 critical issues
**Total Files Affected**: 60+ documents
**Cleanup Complexity**: High
**Estimated Cleanup Time**: 2 hours
**Risk Level**: Low (backup-first strategy)

---

## CRITICAL VIOLATIONS

### ❌ Violation #1: claudes-docs/ Directory Exists

**Issue**: `claudes-docs/` directory violates Doc-Filing v3.0
**Location**: `/home/jeremy/000-projects/nixtla/claudes-docs/`
**Standard**: All documentation must be in `000-docs/`

**Files in claudes-docs/**:
```
claudes-docs/
├── claude-skills-implementation-summary.md
├── educational-overview-enhancement.md
├── free-search-providers-implementation.md
├── marketplace-implementation-summary.md
├── marketplace-setup-guide.md
└── nixtla-v020-release-session-summary.md
```

**Impact**: 6 files in wrong location
**Severity**: P0 - Critical

---

### ❌ Violation #2: Duplicate Document Numbers in 000-docs/

**Issue**: Multiple files share the same NNN prefix
**Standard**: Each NNN must be unique and chronological

**Duplicates Detected**:

```bash
# 002 appears TWICE:
002-AT-ARCH-plugin-architecture.md                      (Nov 23)
002-PP-PROD-nixtla-plugin-opportunities-report.md        (Nov 29)

# 003 appears TWICE:
003-AT-ARCH-plugin-01-nixtla-cost-optimizer.md           (Nov 30)
003-DR-META-document-standards.md                        (Nov 23)

# 004 appears THREE times:
004-AT-ARCH-plugin-02-nixtla-vs-statsforecast-benchmark.md (Nov 30)
004-RA-INTL-repo-audit-and-enhancements.md                 (Nov 23)

# 005 appears THREE times:
005-AT-ARCH-plugin-03-nixtla-roi-calculator.md            (Nov 30)
005-OD-RELS-v0-1-0-initial-release.md                     (Nov 23)

# 006 appears THREE times:
006-AT-ARCH-plugin-04-nixtla-airflow-operator.md          (Nov 30)
006-PP-PROD-nixtla-integration-requirements.md            (Nov 23)

# 007 appears THREE times:
007-AA-AUDT-appaudit-devops-playbook.md                   (Nov 23)
007-AT-ARCH-plugin-05-nixtla-dbt-package.md               (Nov 30)

# 008 appears THREE times:
008-AT-ARCH-plugin-06-nixtla-snowflake-adapter.md         (Nov 30)
008-DR-GUID-claude-code-plugin-development-guide.md       (Nov 23)

# 009 appears TWICE:
009-AT-ARCH-nixtla-plugin-marketplace-architecture.md     (Nov 23)
009-AT-ARCH-plugin-07-nixtla-anomaly-streaming-monitor.md (Nov 30)

# 010 appears TWICE:
010-AT-ARCH-plugin-08-nixtla-migration-assistant.md       (Nov 30)
010-DR-REFF-6767-canonical-document-reference-sheet.md    (Nov 23)

# 011 appears TWICE:
011-AT-ARCH-plugin-09-nixtla-forecast-explainer.md        (Nov 30)
011-PP-PLAN-nixtla-search-to-slack-mvp.md                 (Nov 23)

# 012 appears TWICE:
012-AT-ARCH-search-to-slack-plugin-construction.md        (Nov 23)
012-PP-PROD-nixtla-plugin-suite-master-summary.md         (Nov 30)
```

**Total Duplicates**: 24 conflicting files
**Impact**: Breaks chronological ordering
**Severity**: P0 - Critical

---

### ❌ Violation #3: 6767 Files Have Numeric IDs in Filenames (Pre-v3.0)

**Issue**: 6767 canonical files use old format with numeric IDs in filename
**Standard**: v3.0 requires `6767-CC-ABCD-description.ext` (NO numeric ID)

**Pre-v3.0 Files**:
```bash
6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md    (OK - no numeric ID)
6767-OD-OVRV-nixtla-baseline-lab-overview.md             (OK - no numeric ID)
6767-OD-OVRV-nixtla-baseline-lab-product-overview.md     (OK - no numeric ID)
6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md    (OK - no numeric ID)
```

**Status**: ✅ All 6767 files are v3.0 compliant (no violation here)

---

### ❌ Violation #4: Excessive Directory Nesting

**Issue**: Project has deep directory nesting violating "flat as possible" principle
**Standard**: Minimize directory depth

**Current Depth**: Up to 6-7 levels deep in some areas

**Examples of Excessive Nesting**:
```
/claude-code-plugins-plus/backups/skill-structure-cleanup-20251108-073936/plugins/skill-enhancers/search-to-slack/skills/skill-adapter/references/
│                                                                                                                                             └─── 7 levels deep!

/plugins/nixtla-baseline-lab/nixtla_baseline_csv_test/
/plugins/nixtla-baseline-lab/nixtla_baseline_m4_test/
/plugins/nixtla-baseline-lab/nixtla_test_custom/
│                            └─── Multiple test dirs that should be consolidated
```

**Impact**: Poor navigability, confusing structure
**Severity**: P1 - High

---

### ❌ Violation #5: Root-Level Markdown Clutter

**Issue**: Too many markdown files in project root
**Standard**: Keep root clean, move docs to 000-docs/

**Root-Level Markdown Files**:
```
ARCHITECTURE.md
CHANGELOG.md
CLAUDE.md
CODE_OF_CONDUCT.md
CONTRIBUTING.md
CONTRIBUTORS.md
DISCUSSIONS.md
EDUCATIONAL_RESOURCES.md
GCP-SETUP-COMPLETE.md
GITHUB_DESCRIPTION.txt
LICENSE
MARKETPLACE_SETUP.md
README.md
ROADMAP.md
SECURITY.md
SETUP-NIXTLA-PLAYGROUND.md
SUPPORT.md
```

**Acceptable in Root**:
- README.md (project entry point)
- CLAUDE.md (project instructions)
- CONTRIBUTING.md (GitHub standard)
- CODE_OF_CONDUCT.md (GitHub standard)
- LICENSE (GitHub standard)
- SECURITY.md (GitHub standard)

**Should Move to 000-docs/**:
- ARCHITECTURE.md
- ROADMAP.md
- EDUCATIONAL_RESOURCES.md
- GCP-SETUP-COMPLETE.md
- MARKETPLACE_SETUP.md
- SETUP-NIXTLA-PLAYGROUND.md
- CHANGELOG.md (or keep in root per convention)
- CONTRIBUTORS.md
- DISCUSSIONS.md
- SUPPORT.md
- GITHUB_DESCRIPTION.txt

**Impact**: Root directory clutter
**Severity**: P2 - Medium

---

### ❌ Violation #6: Inconsistent Plugin Structure

**Issue**: Plugins have inconsistent directory structures
**Standard**: Standardize plugin scaffolding

**Current Inconsistencies**:

```bash
# Plugin #1: nixtla-baseline-lab (complex structure)
plugins/nixtla-baseline-lab/
├── agents/
├── commands/
├── data/
├── nixtla_baseline_csv_test/        # Embedded test dirs (bad)
├── nixtla_baseline_m4_test/          # Should be in tests/
├── nixtla_test_custom/               # Should be in tests/
├── scripts/
├── skills/
└── tests/

# Plugin #2: nixtla-baseline-m4 (minimal structure)
plugins/nixtla-baseline-m4/
├── slash-commands/                   # Inconsistent: should be "commands"
└── src/

# Plugin #3: nixtla-bigquery-forecaster (standard structure)
plugins/nixtla-bigquery-forecaster/
├── 000-docs/                         # Has own docs (good)
└── src/

# Plugin #4: nixtla-search-to-slack (standard structure)
plugins/nixtla-search-to-slack/
├── config/
├── skills/
├── src/
└── tests/
```

**Impact**: Inconsistent development experience
**Severity**: P1 - High

---

## PROPOSED CLEANUP PLAN

### Phase 1: Document Renumbering (000-docs/)

**Goal**: Eliminate duplicate NNN numbers, maintain chronology

**Strategy**:
1. Identify "authoritative" version of each duplicate
2. Renumber newer plugin docs to 050-059 range (separate series)
3. Keep original docs in 001-049 range

**Renumbering Map**:

```bash
# Current duplicates → New numbers

# Original docs (KEEP original numbers):
002-AT-ARCH-plugin-architecture.md                 → KEEP
003-DR-META-document-standards.md                  → KEEP
004-RA-INTL-repo-audit-and-enhancements.md         → KEEP
005-OD-RELS-v0-1-0-initial-release.md              → KEEP
006-PP-PROD-nixtla-integration-requirements.md     → KEEP
007-AA-AUDT-appaudit-devops-playbook.md            → KEEP
008-DR-GUID-claude-code-plugin-development-guide.md → KEEP
009-AT-ARCH-nixtla-plugin-marketplace-architecture.md → KEEP
010-DR-REFF-6767-canonical-document-reference-sheet.md → KEEP
011-PP-PLAN-nixtla-search-to-slack-mvp.md          → KEEP
012-AT-ARCH-search-to-slack-plugin-construction.md → KEEP

# New plugin spec series (RENUMBER to 050-059):
002-PP-PROD-nixtla-plugin-opportunities-report.md  → 050-PP-PROD-nixtla-plugin-opportunities-report.md
003-AT-ARCH-plugin-01-nixtla-cost-optimizer.md     → 051-AT-ARCH-plugin-01-nixtla-cost-optimizer.md
004-AT-ARCH-plugin-02-nixtla-vs-statsforecast-benchmark.md → 052-AT-ARCH-plugin-02-nixtla-vs-statsforecast-benchmark.md
005-AT-ARCH-plugin-03-nixtla-roi-calculator.md     → 053-AT-ARCH-plugin-03-nixtla-roi-calculator.md
006-AT-ARCH-plugin-04-nixtla-airflow-operator.md   → 054-AT-ARCH-plugin-04-nixtla-airflow-operator.md
007-AT-ARCH-plugin-05-nixtla-dbt-package.md        → 055-AT-ARCH-plugin-05-nixtla-dbt-package.md
008-AT-ARCH-plugin-06-nixtla-snowflake-adapter.md  → 056-AT-ARCH-plugin-06-nixtla-snowflake-adapter.md
009-AT-ARCH-plugin-07-nixtla-anomaly-streaming-monitor.md → 057-AT-ARCH-plugin-07-nixtla-anomaly-streaming-monitor.md
010-AT-ARCH-plugin-08-nixtla-migration-assistant.md → 058-AT-ARCH-plugin-08-nixtla-migration-assistant.md
011-AT-ARCH-plugin-09-nixtla-forecast-explainer.md → 059-AT-ARCH-plugin-09-nixtla-forecast-explainer.md
012-PP-PROD-nixtla-plugin-suite-master-summary.md  → 060-PP-PROD-nixtla-plugin-suite-master-summary.md
```

**Result**: No more duplicate NNN numbers

---

### Phase 2: Migrate claudes-docs/ to 000-docs/

**Goal**: Eliminate claudes-docs/ directory

**Migration Map**:

```bash
# claudes-docs/ → 000-docs/ with proper naming

claudes-docs/claude-skills-implementation-summary.md
  → 000-docs/061-AA-SUMM-claude-skills-implementation-summary.md

claudes-docs/educational-overview-enhancement.md
  → 000-docs/062-UC-GUID-educational-overview-enhancement.md

claudes-docs/free-search-providers-implementation.md
  → 000-docs/063-DC-DEVN-free-search-providers-implementation.md

claudes-docs/marketplace-implementation-summary.md
  → 000-docs/064-AA-SUMM-marketplace-implementation-summary.md

claudes-docs/marketplace-setup-guide.md
  → 000-docs/065-DR-GUID-marketplace-setup-guide.md

claudes-docs/nixtla-v020-release-session-summary.md
  → 000-docs/066-OD-RELS-v0-2-0-release-session-summary.md
```

**After Migration**: Delete empty `claudes-docs/` directory

---

### Phase 3: Consolidate Root-Level Markdown Files

**Goal**: Move non-essential docs to 000-docs/

**Migration Map**:

```bash
# Keep in root (GitHub standards):
README.md                    → KEEP
CLAUDE.md                    → KEEP
CONTRIBUTING.md              → KEEP
CODE_OF_CONDUCT.md           → KEEP
LICENSE                      → KEEP
SECURITY.md                  → KEEP
CHANGELOG.md                 → KEEP (standard practice)

# Move to 000-docs/:
ARCHITECTURE.md              → 000-docs/067-AT-ARCH-project-architecture.md
ROADMAP.md                   → 000-docs/068-PP-RMAP-project-roadmap.md
EDUCATIONAL_RESOURCES.md     → 000-docs/069-UC-GUID-educational-resources.md
GCP-SETUP-COMPLETE.md        → 000-docs/070-OD-GUID-gcp-setup-complete.md
MARKETPLACE_SETUP.md         → 000-docs/071-DR-GUID-marketplace-setup.md
SETUP-NIXTLA-PLAYGROUND.md   → 000-docs/072-OD-GUID-nixtla-playground-setup.md
CONTRIBUTORS.md              → 000-docs/073-MC-MEMO-contributors.md
DISCUSSIONS.md               → 000-docs/074-MC-GUID-discussions-guide.md
SUPPORT.md                   → 000-docs/075-DR-GUID-support-guide.md
GITHUB_DESCRIPTION.txt       → 000-docs/076-MC-MEMO-github-description.txt
```

---

### Phase 4: Flatten Plugin Structure

**Goal**: Standardize all plugin directory structures

**Standard Plugin Scaffold**:

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json                  # Required manifest
├── commands/                        # Slash commands (markdown)
│   └── <command-name>.md
├── skills/                          # Agent skills
│   └── SKILL.md
├── mcp/                             # MCP server (TypeScript) - OPTIONAL
│   ├── server.json
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   └── dist/
├── src/                             # Python source code
│   ├── __init__.py
│   └── *.py
├── tests/                           # All tests (unit + integration)
│   └── test_*.py
├── config/                          # Configuration files - OPTIONAL
│   └── *.yaml
├── requirements.txt                 # Python dependencies
├── setup.sh                         # Installation script
└── README.md                        # Plugin documentation
```

**Cleanup Actions**:

```bash
# Plugin #1: nixtla-baseline-lab
# MOVE: nixtla_baseline_csv_test/ → tests/csv_test/
# MOVE: nixtla_baseline_m4_test/ → tests/m4_test/
# MOVE: nixtla_test_custom/ → tests/custom/
# REMOVE: data/ (if empty or move to tests/fixtures/)

# Plugin #2: nixtla-baseline-m4
# RENAME: slash-commands/ → commands/

# All plugins: Add .claude-plugin/ if missing
```

---

### Phase 5: Archive claude-code-plugins-plus/ Backups

**Goal**: Reduce clutter from old backups

**Strategy**: Move all backups to single archive directory

```bash
claude-code-plugins-plus/backups/
  → archive/backups-20251108/

# Or delete if no longer needed (after verification)
```

---

## FINAL TARGET STRUCTURE

### Root Level (Clean)

```
/home/jeremy/000-projects/nixtla/
├── .claude/
├── .claude-plugin/
├── .devcontainer/
├── .github/
├── .vscode/
├── 000-docs/                        # ✅ FLAT, all docs here
│   ├── 001-PP-PLAN-nixtla-collaboration-overview.md
│   ├── 002-AT-ARCH-plugin-architecture.md
│   ├── ...
│   ├── 050-PP-PROD-nixtla-plugin-opportunities-report.md
│   ├── 051-AT-ARCH-plugin-01-nixtla-cost-optimizer.md
│   ├── ...
│   ├── 060-PP-PROD-nixtla-plugin-suite-master-summary.md
│   ├── 061-AA-SUMM-claude-skills-implementation-summary.md
│   ├── ...
│   ├── 076-MC-MEMO-github-description.txt
│   └── 6767-*.md                    # Canonical standards
├── archive/                         # Old/deprecated materials
│   └── backups-20251108/
├── claude-code-plugins-plus/        # Plugin marketplace repo
│   ├── plugins/                     # 200+ marketplace plugins
│   ├── marketplace/                 # Website
│   ├── scripts/
│   └── README.md
├── docs/                            # MkDocs site (optional)
├── examples/                        # Usage examples
│   ├── mlforecast-automation/
│   ├── neuralforecast-deployment/
│   ├── statsforecast-pipeline/
│   └── timegpt-integration/
├── plugins/                         # ✅ STANDARDIZED structure
│   ├── nixtla-baseline-lab/
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── skills/
│   │   ├── src/
│   │   ├── tests/                   # ✅ All tests here
│   │   ├── requirements.txt
│   │   ├── setup.sh
│   │   └── README.md
│   ├── nixtla-baseline-m4/
│   │   ├── .claude-plugin/
│   │   ├── commands/                # ✅ RENAMED from slash-commands
│   │   ├── src/
│   │   └── README.md
│   ├── nixtla-bigquery-forecaster/
│   └── nixtla-search-to-slack/
├── scripts/                         # Build/deployment scripts
├── tests/                           # Project-level tests
├── README.md                        # ✅ KEEP in root
├── CLAUDE.md                        # ✅ KEEP in root
├── CONTRIBUTING.md                  # ✅ KEEP in root
├── CODE_OF_CONDUCT.md               # ✅ KEEP in root
├── LICENSE                          # ✅ KEEP in root
├── SECURITY.md                      # ✅ KEEP in root
├── CHANGELOG.md                     # ✅ KEEP in root
├── pyproject.toml
├── pytest.ini
├── requirements.txt
└── requirements-dev.txt
```

### Key Improvements

1. ✅ **Flat 000-docs/** - All docs in one place, no subdirectories
2. ✅ **No claudes-docs/** - Eliminated
3. ✅ **No duplicate NNN** - Unique chronological ordering
4. ✅ **Clean root** - Only essential files
5. ✅ **Standardized plugins/** - Consistent structure
6. ✅ **Archived backups** - Reduced clutter

---

## IMPLEMENTATION CHECKLIST

### Pre-Flight (Safety First)

- [ ] Create full backup: `tar -czf nixtla-backup-$(date +%Y%m%d-%H%M%S).tar.gz /home/jeremy/000-projects/nixtla/`
- [ ] Commit all current work: `git add -A && git commit -m "Pre-cleanup snapshot"`
- [ ] Create cleanup branch: `git checkout -b cleanup/doc-filing-v3-compliance`
- [ ] Document current state: `tree -L 3 > structure-before-cleanup.txt`

### Phase 1: Renumber Duplicate Docs (Priority: P0)

- [ ] Rename plugin spec series to 050-060 range
- [ ] Verify no conflicts remain
- [ ] Update any internal cross-references
- [ ] Git commit: `git commit -m "fix(docs): renumber plugin specs to 050-060 range"`

### Phase 2: Migrate claudes-docs/ (Priority: P0)

- [ ] Move 6 files to 000-docs/ with proper naming (061-066)
- [ ] Delete empty claudes-docs/ directory
- [ ] Git commit: `git commit -m "fix(docs): migrate claudes-docs to 000-docs per v3.0 standard"`

### Phase 3: Consolidate Root Markdown (Priority: P2)

- [ ] Move 10 markdown files to 000-docs/ (067-076)
- [ ] Update any scripts that reference old paths
- [ ] Git commit: `git commit -m "refactor(docs): consolidate root markdown into 000-docs"`

### Phase 4: Standardize Plugin Structure (Priority: P1)

- [ ] Flatten nixtla-baseline-lab test directories
- [ ] Rename slash-commands/ → commands/ in nixtla-baseline-m4
- [ ] Add .claude-plugin/ to all plugins
- [ ] Git commit: `git commit -m "refactor(plugins): standardize plugin directory structure"`

### Phase 5: Archive Old Backups (Priority: P2)

- [ ] Move backups to archive/backups-20251108/
- [ ] Git commit: `git commit -m "chore(archive): consolidate old plugin backups"`

### Post-Flight Validation

- [ ] Run: `find 000-docs/ -name "*.md" | sort | uniq -d` (verify no duplicates)
- [ ] Verify: No `claudes-docs/` directory exists
- [ ] Verify: All plugins have standardized structure
- [ ] Document final state: `tree -L 3 > structure-after-cleanup.txt`
- [ ] Create PR: "fix: achieve Doc-Filing v3.0 compliance"
- [ ] Merge to main after review

---

## RISK ASSESSMENT

### Low Risk

- Document renaming (Git preserves history)
- Directory consolidation (no code changes)
- File moves (Git tracks renames)

### Mitigation Strategies

1. **Full backup before any changes**
2. **Git branch for all cleanup work**
3. **Commit after each phase**
4. **Rollback plan: `git reset --hard` to pre-cleanup commit**

### Rollback Procedure

```bash
# If cleanup fails, rollback:
git checkout main
git branch -D cleanup/doc-filing-v3-compliance
git reset --hard <pre-cleanup-commit-sha>

# Restore from backup if needed:
tar -xzf nixtla-backup-YYYYMMDD-HHMMSS.tar.gz
```

---

## ESTIMATED TIMELINE

- **Phase 1 (Renumber)**: 20 minutes
- **Phase 2 (Migrate claudes-docs)**: 10 minutes
- **Phase 3 (Root consolidation)**: 15 minutes
- **Phase 4 (Plugin structure)**: 30 minutes
- **Phase 5 (Archive backups)**: 10 minutes
- **Validation**: 15 minutes

**Total**: ~100 minutes (1h 40m)

---

## SUCCESS CRITERIA

✅ No `claudes-docs/` directory exists
✅ No duplicate NNN numbers in `000-docs/`
✅ All docs follow `NNN-CC-ABCD-description.ext` format
✅ 6767 files follow `6767-CC-ABCD-description.ext` format (v3.0)
✅ Root directory contains <10 markdown files
✅ All plugins follow standardized structure
✅ Git history preserved for all renames/moves
✅ All tests pass after cleanup

---

**Next Action**: Execute Phase 1 (Renumber duplicate docs) after user approval

**Document Version**: 1.0.0
**Audit Date**: 2025-11-30
**Auditor**: Claude Code
**Standard**: Document Filing System v3.0
