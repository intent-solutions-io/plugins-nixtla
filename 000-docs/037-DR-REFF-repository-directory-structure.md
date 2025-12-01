# Repository Directory Structure Reference

**Document ID**: 037-DR-REFF-repository-directory-structure.md
**Created**: 2025-11-30
**Purpose**: Visual reference for complete repository structure
**For**: Developers, contributors, and documentation readers

---

## ASCII Directory Tree

```
nixtla/                                    Root repository folder
│
├── README.md                              ⭐ Main showcase for Max (Nixtla CEO)
├── CHANGELOG.md                           📝 Version history (v1.1.0)
├── CLAUDE.md                              🤖 Claude Code guidance
├── VERSION                                🏷️  Current version: 1.1.0
│
├── 000-docs/                              📚 ALL DOCUMENTATION (142 files)
│   ├── README.md                          🗺️  Organization guide (YOU ARE HERE!)
│   ├── RESTRUCTURE-SUMMARY.md             Summary of v1.1.0 restructure
│   ├── 037-DR-REFF-repository-directory-structure.md  ← THIS DOCUMENT
│   │
│   ├── Root-Level Docs (001-036)         Chronological project documents
│   │   ├── 001-DR-REFF-*.md              Reference materials
│   │   ├── 002-005-PP-PLAN-*.md          Planning documents
│   │   ├── 006-QA-TEST-*.md              Testing documentation
│   │   ├── 007-008-OD-*.md               Overview/release docs
│   │   ├── 009-017-AT-ARCH-plugin-*.md   ⭐ 9 COMPREHENSIVE PLUGIN SPECS
│   │   │   ├── 009-AT-ARCH-plugin-01-nixtla-cost-optimizer.md (59KB)
│   │   │   ├── 010-AT-ARCH-plugin-02-nixtla-vs-statsforecast-benchmark.md (23KB)
│   │   │   ├── 011-AT-ARCH-plugin-03-nixtla-roi-calculator.md (22KB)
│   │   │   ├── 012-AT-ARCH-plugin-04-nixtla-airflow-operator.md (19KB)
│   │   │   ├── 013-AT-ARCH-plugin-05-nixtla-dbt-package.md (12KB)
│   │   │   ├── 014-AT-ARCH-plugin-06-nixtla-snowflake-adapter.md (12KB)
│   │   │   ├── 015-AT-ARCH-plugin-07-nixtla-anomaly-streaming-monitor.md (42KB)
│   │   │   ├── 016-AT-ARCH-plugin-08-nixtla-migration-assistant.md (37KB)
│   │   │   └── 017-AT-ARCH-plugin-09-nixtla-forecast-explainer.md (40KB)
│   │   ├── 018-PP-PROD-*.md              Product summaries
│   │   ├── 019-033-*.md                  Various specs/guides/overviews
│   │   ├── 034-OD-RELS-*.md              v0.8.0 release AAR
│   │   ├── 035-PP-PROD-*.md              💰 Business case for Max
│   │   └── 036-AA-AUDT-*.md              Working plugins verification
│   │
│   ├── 6767-OD-* Series (7 files)        📜 CANONICAL REFERENCE DOCS
│   │   ├── 6767-OD-REF-enterprise-plugin-readme-standard.md
│   │   ├── 6767-OD-GUIDE-enterprise-plugin-implementation.md
│   │   ├── 6767-OD-STAT-enterprise-readme-standard-implementation.md
│   │   ├── 6767-OD-OVRV-nixtla-baseline-lab-overview.md
│   │   ├── 6767-OD-OVRV-nixtla-baseline-lab-product-overview.md
│   │   ├── 6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md
│   │   └── 6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md
│   │
│   ├── global/                            👔 EXECUTIVE DOCS (3 files)
│   │   ├── 000-EXECUTIVE-SUMMARY.md      📊 1-page pitch for Max
│   │   ├── 001-ENGAGEMENT-OPTIONS.md     💼 Evaluate/Pilot/Platform tiers
│   │   └── 002-DECISION-MATRIX.md        🎯 Plugin prioritization scoring
│   │
│   ├── aar/                               📖 AFTER-ACTION REPORTS (4 files)
│   │   ├── 2025-11-30-phase-1-foundation-aar.md
│   │   ├── 2025-11-30-phase-2-readme-compliance-aar.md
│   │   ├── 2025-11-30-phase-3-content-review-aar.md
│   │   └── 2025-11-30-phase-4-final-verification-aar.md
│   │
│   ├── plugins/                           🔌 PER-PLUGIN DOCS (60 files)
│   │   │                                  Each plugin has 6 standardized docs:
│   │   │                                  01-BUSINESS-CASE, 02-PRD, 03-ARCHITECTURE,
│   │   │                                  04-USER-JOURNEY, 05-TECHNICAL-SPEC, 06-STATUS
│   │   │
│   │   ├── nixtla-baseline-lab/          ✅ WORKING (6 docs)
│   │   │   ├── 01-BUSINESS-CASE.md       💰 ROI analysis
│   │   │   ├── 02-PRD.md                 📋 Requirements
│   │   │   ├── 03-ARCHITECTURE.md        🏗️  System design
│   │   │   ├── 04-USER-JOURNEY.md        🚶 User experience
│   │   │   ├── 05-TECHNICAL-SPEC.md      🔧 Implementation
│   │   │   └── 06-STATUS.md              📊 Current state
│   │   │
│   │   ├── nixtla-cost-optimizer/        📋 SPECIFIED (6 docs)
│   │   ├── nixtla-migration-assistant/   📋 SPECIFIED (6 docs)
│   │   ├── nixtla-forecast-explainer/    📋 SPECIFIED (6 docs)
│   │   ├── nixtla-vs-statsforecast-benchmark/  📋 SPECIFIED (6 docs)
│   │   ├── nixtla-roi-calculator/        📋 SPECIFIED (6 docs)
│   │   ├── nixtla-airflow-operator/      📋 SPECIFIED (6 docs)
│   │   ├── nixtla-dbt-package/           📋 SPECIFIED (6 docs)
│   │   ├── nixtla-snowflake-adapter/     📋 SPECIFIED (6 docs)
│   │   └── nixtla-anomaly-streaming-monitor/  📋 SPECIFIED (6 docs)
│   │
│   └── archive/                           🗄️  Historical/deprecated docs
│
├── plugins/                               🔌 PLUGIN SOURCE CODE (3 working)
│   │
│   ├── nixtla-baseline-lab/              ✅ v1.1.0 - PRODUCTION READY
│   │   ├── .claude-plugin/               🤖 Plugin metadata
│   │   │   └── plugin.json               Version, description, author
│   │   │
│   │   ├── commands/                     ⌨️  Slash commands
│   │   │   └── nixtla-baseline-m4.md     /nixtla-baseline-m4 definition
│   │   │
│   │   ├── skills/                       🧠 AI Skills (auto-triggered)
│   │   │   └── nixtla-baseline-review/   Skill adapter + prompts
│   │   │
│   │   ├── scripts/                      🐍 Python backend
│   │   │   ├── mcp_server.py             MCP server implementation
│   │   │   ├── run_baseline_m4.py        Core forecasting logic
│   │   │   ├── requirements.txt          Python dependencies
│   │   │   └── setup_nixtla_env.sh       Environment setup
│   │   │
│   │   ├── tests/                        🧪 Test suite
│   │   │   └── run_baseline_m4_smoke.py  Golden task validation
│   │   │
│   │   └── README.md                     📖 Plugin user manual
│   │
│   ├── nixtla-bigquery-forecaster/       ✅ WORKING DEMO
│   │   ├── .github/                      🔄 CI/CD workflows
│   │   │   └── workflows/
│   │   │       └── deploy.yml            GitHub Actions deployment
│   │   │
│   │   ├── src/                          💻 Python source
│   │   │   ├── main.py                   Cloud Functions entry point
│   │   │   └── forecaster.py             Forecasting logic
│   │   │
│   │   ├── test_local.py                 Local testing script
│   │   └── README.md                     Setup and usage guide
│   │
│   └── nixtla-search-to-slack/           ✅ v0.1.0 - MVP / CONSTRUCTION KIT
│       ├── src/                          💻 Python source
│       │   └── nixtla_search_to_slack/   Main package
│       │       ├── search.py             SerpAPI integration
│       │       ├── summarize.py          AI summarization
│       │       └── slack.py              Slack posting
│       │
│       ├── tests/                        🧪 Comprehensive test suite (6 files)
│       │   ├── test_search.py
│       │   ├── test_summarize.py
│       │   ├── test_slack.py
│       │   ├── test_integration.py
│       │   ├── test_config.py
│       │   └── test_cli.py
│       │
│       ├── SETUP_GUIDE.md                📖 Comprehensive setup (24KB)
│       └── README.md                     Plugin overview
│
├── templates/                             📝 PLUGIN SCAFFOLDING TEMPLATES (6 files)
│   ├── 01-BUSINESS-CASE-TEMPLATE.md      Template for business case docs
│   ├── 02-PRD-TEMPLATE.md                Template for PRDs
│   ├── 03-ARCHITECTURE-TEMPLATE.md       Template for architecture docs
│   ├── 04-USER-JOURNEY-TEMPLATE.md       Template for user journeys
│   ├── 05-TECHNICAL-SPEC-TEMPLATE.md     Template for technical specs
│   └── 06-STATUS-TEMPLATE.md             Template for status tracking
│
├── scripts/                               🛠️  REPOSITORY UTILITIES (4 files)
│   ├── new-plugin.sh                     Scaffold new plugin structure
│   ├── validate-docs.sh                  Verify documentation completeness
│   ├── run_nixtla_review_baseline.sh     2-minute demo script
│   └── cleanup-doc-filing-v3.sh          Doc-Filing v3.0 compliance
│
├── .github/                               🔄 CI/CD CONFIGURATION
│   └── workflows/                         GitHub Actions workflows
│       └── (various CI/CD pipelines)
│
├── .claude/                               🤖 CLAUDE CODE CONFIGURATION
│   └── commands/                          Custom slash commands
│       └── nixtla-release.md              /nixtla-release command definition
│
└── archive/                               🗄️  OLD BACKUPS
    └── backups-20251108/                  Historical plugin backups
```

---

## Repository Metrics

| Category | Count | Details |
|----------|-------|---------|
| **Total Documentation** | 142 files | All in `000-docs/` |
| **Root Docs** | 35 files | 001-035 series (sequential, no gaps) |
| **Reference Docs** | 7 files | 6767 series (canonical standards) |
| **Executive Docs** | 3 files | `global/` folder |
| **After-Action Reports** | 4 files | `aar/` folder |
| **Per-Plugin Docs** | 60 files | 10 plugins × 6 docs each |
| **Comprehensive Specs** | 9 files | 009-017 series (12KB-59KB each) |
| **Working Plugins** | 3 | Baseline Lab, BigQuery, Search-to-Slack |
| **Specified Plugins** | 9 | Full specs ready to build |
| **Total Plugins** | 12 | 3 working + 9 specified |
| **Verified Links** | 117 | All tested and working |

---

## File Naming Convention

All numbered docs follow: `NNN-CC-ABCD-description.md`

**NNN** = Sequential number (001-035, no gaps)
**CC** = Category Code:
- `DR` - Documentation Reference
- `PP` - Planning & Product
- `AT` - Architecture & Technical
- `AA` - Audits & After-Action Reports
- `OD` - Overview & Documentation
- `QA` - Quality Assurance & Testing

**ABCD** = Type Code (varies by category)

**Examples**:
- `001-DR-REFF-6767-canonical-document-reference-sheet.md`
- `009-AT-ARCH-plugin-01-nixtla-cost-optimizer.md`
- `035-PP-PROD-nixtla-plugin-business-case.md`

---

## Navigation Guide

### For Max (Nixtla CEO)

**Start Here**:
1. `README.md` ⭐ (Repository overview)
2. `000-docs/global/000-EXECUTIVE-SUMMARY.md` 📊 (1-page pitch)
3. `000-docs/035-PP-PROD-nixtla-plugin-business-case.md` 💰 (Full business case)

### For Engineers

**Plugin Development**:
1. `000-docs/009-017-AT-ARCH-plugin-*.md` (9 comprehensive specs)
2. `plugins/nixtla-baseline-lab/` (Production reference implementation)
3. `templates/` (Scaffolding templates)
4. `scripts/new-plugin.sh` (Create new plugin)

### For Documentation Contributors

**Understanding Organization**:
1. `000-docs/README.md` 🗺️ (Organization guide)
2. `000-docs/037-DR-REFF-repository-directory-structure.md` (This document)
3. `000-docs/6767-OD-REF-enterprise-plugin-readme-standard.md` (Standards)

---

## Quick Commands

```bash
# View directory structure
tree -L 2 -I 'node_modules|.venv*|__pycache__'

# Find all markdown files
find 000-docs/ -name "*.md" -type f

# Count documentation files
find 000-docs/ -name "*.md" -type f | wc -l

# Validate documentation completeness
./scripts/validate-docs.sh

# Create new plugin
./scripts/new-plugin.sh my-plugin "My Plugin" efficiency
```

---

## Directory Purpose Summary

| Directory | Purpose | Audience |
|-----------|---------|----------|
| `000-docs/` | All documentation | Everyone |
| `000-docs/global/` | Executive materials | Decision makers |
| `000-docs/aar/` | Implementation history | Project managers |
| `000-docs/plugins/` | Per-plugin docs | Engineers, Max |
| `000-docs/archive/` | Historical docs | Reference only |
| `plugins/` | Working plugin code | Engineers |
| `templates/` | New plugin templates | Plugin developers |
| `scripts/` | Build/validate tools | DevOps, engineers |
| `.claude/` | Claude Code config | Claude Code users |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2025-11-30 | Doc renumbering, 3 working plugins, organization guide |
| 1.0.0 | 2025-11-30 | Enterprise Plugin README Standard implementation |
| 0.8.0 | 2025-11-30 | Doc-Filing v3.0 compliance |

---

## Related Documents

- [Organization Guide](README.md) - How everything is organized
- [Business Case](035-PP-PROD-nixtla-plugin-business-case.md) - ROI analysis for Max
- [Executive Summary](global/000-EXECUTIVE-SUMMARY.md) - 1-page pitch
- [Plugin Specs](009-AT-ARCH-plugin-01-nixtla-cost-optimizer.md) - Start of 9 comprehensive specs

---

**Last Updated**: 2025-11-30
**Maintained By**: Intent Solutions (Claude Code)
**For**: Nixtla Plugin Showcase Repository
