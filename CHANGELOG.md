# Changelog

All notable changes to Claude Code Plugins for Nixtla will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-11-30

### Summary
Documentation accuracy release - discovered and verified 3 working plugins (not 1), renumbered all docs chronologically starting from 001, and synchronized all version references.

### Changed
- **Working Plugin Count**: Updated from "1 working plugin" → "3 working plugins"
  - Baseline Lab (v0.8.0 → v1.1.0) - Production-ready
  - BigQuery Forecaster - Working demo (GCloud/Cloud Functions)
  - Search-to-Slack (v0.1.0) - MVP / Construction kit

- **Document Renumbering**: Complete chronological renumbering
  - Old: 010-078 (with gaps: no 015-022, 024-034, 036-049)
  - New: 001-035 (sequential, no gaps)
  - 6767 reference series preserved unchanged
  - 54 placeholder docs updated with new spec references

- **Version Synchronization**: All version references now aligned
  - VERSION file: 1.1.0
  - plugin.json: 1.1.0 (was out of sync at 0.7.0)
  - CHANGELOG: 1.1.0

### Added
- **Working Plugin Documentation**:
  - `plugins/nixtla-bigquery-forecaster/` - Full source, tests, README
  - `plugins/nixtla-search-to-slack/` - Full source, 6 test files, SETUP_GUIDE.md

- **Verification Audit**: `036-AA-AUDT-working-plugins-verification.md`
  - Documented all 3 working plugins with git references
  - Verified test suites, source code, documentation
  - Git commits: `4d4f679` (BigQuery), `0c27c23` (Search-to-Slack)

- **Documentation Organization Guide**: `000-docs/README.md` (350 lines)
  - Complete directory structure explanation
  - File naming convention guide (NNN-CC-ABCD format)
  - 6-doc standard per plugin documentation
  - Navigation tips and FAQ section
  - Version history tracking

### Updated
- **CLAUDE.md**: Now reflects 3 working plugins with full architecture details
- **Reference Updates**: All cross-references updated for new doc numbering
  - 035-PP-PROD business case references
  - global/000-EXECUTIVE-SUMMARY.md references
  - plugins/ placeholder doc references

- **README Tagline**: Changed to "Open playground for Claude Code plugins..."
  - Less restrictive positioning
  - Supports internal ops, open source, current customers, new markets
  - Reflects broader use cases beyond initial scope

### Fixed
- **Version Mismatch**: plugin.json was 0.7.0, VERSION was 1.0.0 (now both 1.1.0)
- **Plugin Count**: Documentation claimed 1 working plugin, but 3 exist
- **Doc Numbering Gaps**: Large gaps in 010-078 series eliminated

- **Documentation Links**: All 9 specified plugins now show 6 clickable docs in README
  - Each plugin displays: Business Case, PRD, Architecture, User Journey, Technical Spec, Status
  - Plus comprehensive spec link (12KB-59KB all-in-one document)
  - Total: 117 verified working links (63 in README + 54 internal cross-references)
  - Fixed user navigation: one click to any specific document type

### Documentation Metrics
- **Root docs**: 35 (001-035, sequential)
- **Reference docs**: 7 (6767 series)
- **Working plugins**: 3 (verified with tests)
- **Specified plugins**: 9 (full specs in 009-017)
- **Total plugins**: 12 (3 working + 9 specified)

---

## [1.0.0] - 2025-11-30

### Summary
Complete implementation of Enterprise Plugin README Standard v1.0. This milestone release restructures the entire repository documentation to provide clear navigation, standardized plugin documentation, and executive-ready materials for sponsor review.

### Changed
- **README.md**: Complete restructure with per-plugin sections
  - Added Quick Navigation table with 5 entry points
  - Added Portfolio Overview with status counts and categories
  - Created dedicated section for each of 10 plugins with full descriptions
  - Added Ideas & Backlog section for future concepts
  - Added Documentation Index explaining 6-doc standard
  - Each plugin section includes metadata, description, business value, and doc links
  - Total: 60 documentation links (10 plugins × 6 docs each)

- **Documentation Organization**: Restructured into global/, plugins/, and archive/ folders
  - `000-docs/global/` - 3 executive decision-making docs
  - `000-docs/plugins/` - 10 plugin folders with 6 docs each (60 files)
  - `000-docs/aar/` - 4 phase implementation AARs
  - Clear separation of concerns by audience and purpose

### Added
- **Reference Documentation**
  - `000-docs/6767-OD-REF-enterprise-plugin-readme-standard.md` - Canonical standard definition
  - `000-docs/6767-OD-GUIDE-enterprise-plugin-implementation.md` - Implementation guide
  - `000-docs/6767-OD-STAT-enterprise-readme-standard-implementation.md` - Status tracking

- **Global Documentation** (`000-docs/global/`)
  - `000-EXECUTIVE-SUMMARY.md` - 1-page pitch for Max (Nixtla CEO)
  - `001-ENGAGEMENT-OPTIONS.md` - Evaluate/Pilot/Platform tiers with pricing/timelines
  - `002-DECISION-MATRIX.md` - Plugin prioritization scoring (9 plugins ranked)

- **Per-Plugin Documentation** (`000-docs/plugins/{slug}/`)
  - 60 total files (10 plugins × 6 standardized docs)
  - Each plugin has: Business Case, PRD, Architecture, User Journey, Technical Spec, Status
  - Baseline Lab (working plugin): 4 complete docs, 2 partial
  - 9 Specified plugins: Placeholder docs referencing comprehensive specs (future migration)

- **Implementation Documentation** (`000-docs/aar/`)
  - Phase 1 AAR: Foundation & directory structure
  - Phase 2 AAR: README compliance audit & gap fixes
  - Phase 3 AAR: Content quality review
  - Phase 4 AAR: Final verification & cleanup

- **Automation**
  - `scripts/new-plugin.sh` - Generate new plugin with 6-doc skeleton
  - `scripts/validate-docs.sh` - Verify documentation completeness

### Improved
- **Baseline Lab Documentation**: 5/6 docs complete with production quality
  - PRD (141 lines): Comprehensive requirements and user stories
  - Architecture (209 lines): System diagrams and integrations
  - User Journey (319 lines): Detailed persona and step-by-step guide
  - Technical Spec (352 lines): Full API reference and deployment
  - Business Case (94 lines): Complete ROI calculation
  - Status (99 lines): Current state tracking

- **Comprehensive Plugin Specs Preserved**: 051-059 series maintained as reference
  - High-quality specifications (200-500 lines each)
  - Serve as source material for future 6-doc conversions
  - Referenced by placeholder docs until migration complete

### Infrastructure
- **Version Management**: VERSION file at 1.0.0
- **Link Verification**: All 64 README documentation links verified
- **Demo Commands**: Verified setup script and requirements exist
- **Directory Structure**: Clean 3-tier organization (global/plugins/archive)

### Documentation Metrics
- **Total docs created**: 70+ files
- **README sections**: 14 (all required sections present)
- **Plugin documentation**: 60 files (100% coverage)
- **Global documentation**: 3 files (executive decision support)
- **Reference documentation**: 3 files (standard, guide, status)
- **Implementation AARs**: 4 files (full project audit trail)

### Quality Standards
- ✅ All README links verified (64/64 passing)
- ✅ Demo commands verified accurate
- ✅ Formatting consistent across all plugins
- ✅ No placeholder text in README
- ✅ Clear separation of working vs specified plugins
- ✅ Decision Matrix scores for plugin prioritization

### Migration Notes
- **Comprehensive specs (051-059)**: Kept as reference until content migration
- **Placeholder docs**: 9 plugins have placeholders referencing comprehensive specs
- **Future work**: Migrate top 3 priority plugins (Cost Optimizer, ROI Calculator, VS Benchmark) to full 6-doc format on-demand

## [0.8.0] - 2025-11-30

### Summary
Phase 8: Doc-Filing v3.0 Compliance - Complete directory restructuring, documentation consolidation, and plugin architecture specifications.

### Added
- **9 New Plugin Specifications** (050-060 series)
  - `050-PP-PROD-nixtla-plugin-opportunities-report.md` - Market analysis
  - `051-AT-ARCH-plugin-01-nixtla-cost-optimizer.md` - Cost optimization plugin
  - `052-AT-ARCH-plugin-02-nixtla-vs-statsforecast-benchmark.md` - Benchmark comparison
  - `053-AT-ARCH-plugin-03-nixtla-roi-calculator.md` - ROI calculator
  - `054-AT-ARCH-plugin-04-nixtla-airflow-operator.md` - Airflow integration
  - `055-AT-ARCH-plugin-05-nixtla-dbt-package.md` - dbt package
  - `056-AT-ARCH-plugin-06-nixtla-snowflake-adapter.md` - Snowflake adapter
  - `057-AT-ARCH-plugin-07-nixtla-anomaly-streaming-monitor.md` - Streaming monitor
  - `058-AT-ARCH-plugin-08-nixtla-migration-assistant.md` - Migration assistant
  - `059-AT-ARCH-plugin-09-nixtla-forecast-explainer.md` - Forecast explainer
  - `060-PP-PROD-nixtla-plugin-suite-master-summary.md` - Suite summary

- **Documentation Migrations** (061-076 series)
  - Migrated 6 files from `claudes-docs/` to `000-docs/` with proper numbering
  - Consolidated 10 root markdown files into `000-docs/`
  - Zero documentation loss with full git history preservation

### Changed
- **Doc-Filing v3.0 Compliance**
  - Renumbered duplicate documents (002-012 → 050-060)
  - Eliminated `claudes-docs/` directory
  - Consolidated root markdown files to `000-docs/`
  - 69 total documents now properly numbered in `000-docs/`

- **Plugin Structure Standardization**
  - Flattened `nixtla-baseline-lab/` test directories to `tests/`
  - Renamed `slash-commands/` to `commands/` for consistency
  - Archived 6,517 backup files to `archive/backups-20251108/`

### Documentation
- Phase 8 Audit: `036-AA-AUDT-directory-structure-audit-and-cleanup-plan.md`
- Cleanup script: `scripts/cleanup-doc-filing-v3.sh`

### Infrastructure
- Created `archive/` directory for historical backups
- Standardized plugin scaffold across all plugins
- Reduced root directory clutter (11 files → 7 standard files)

## [0.7.0] - 2025-11-26

### Summary
Phase 7: Docs Refresh - Complete documentation overhaul for the Nixtla Baseline Lab plugin with modest, technically accurate framing.

### Added
- **New Documentation Site Pages**
  - `docs/nixtla-baseline-lab.md` - Complete plugin documentation (423 lines)
  - `000-docs/6767-OD-OVRV-nixtla-baseline-lab-overview.md` - Technical overview (270 lines)

### Changed
- **Root README.md** - Complete rewrite (434 lines) with:
  - Modest framing: "experimental prototype", "developer sandbox"
  - Clear "what this is NOT" sections
  - Nixtla as source of truth for official documentation
  - Collaboration context (Intent Solutions maintains, Nixtla sponsors)
- **docs/index.md** - Updated with accurate plugin capabilities
- **CLAUDE.md** - Added "Current State Snapshot" section for AI assistants

### Documentation
- Updated all phase references (1-6 capabilities documented)
- Consistent versioning across all documentation
- Safety notes and disclaimers throughout

## [0.6.0] - 2025-11-25

### Summary
Phase 6: Optional TimeGPT Showdown - Strictly opt-in comparison mode against Nixtla's TimeGPT foundation model.

### Added
- **TimeGPT Showdown Mode** (opt-in only)
  - Requires explicit `include_timegpt=true` flag AND valid `NIXTLA_TIMEGPT_API_KEY`
  - Cost control via `timegpt_max_series` parameter (default 5)
  - Graceful degradation - TimeGPT failure doesn't break baseline run
  - Clear failure reasons (`missing_api_key`, `sdk_not_installed`, `api_error`)
  - `timegpt_showdown_*.txt` output with comparison summary

### Changed
- CI remains offline-only (no TimeGPT calls in automated tests)
- TimeGPT is strictly additive - baseline behavior unchanged

### Documentation
- Phase 6 AAR (`033-AA-AACR-phase-06-timegpt-showdown.md`)
- Phase 6 status verification (`032-AA-STAT-phase-06-timegpt-showdown-status.md`)

## [0.5.0] - 2025-11-24

### Summary
Phase 5: Setup & Validation - Reproducibility bundles and GitHub issue draft generation.

### Added
- **Reproducibility Bundles**
  - `run_manifest.json` - Complete run configuration
  - `compat_info.json` - Library versions (statsforecast, pandas, numpy, python)
- **GitHub Issue Draft Generator**
  - `generate_github_issue_draft` MCP tool
  - Pre-filled Markdown templates for `nixtla/statsforecast`
  - Includes benchmark results, run config, library versions
- **Setup Script**
  - `scripts/setup_nixtla_env.sh` with virtualenv support
  - Dependency validation

### Documentation
- Phase 5 AAR (`019-AA-AACR-phase-05-setup-and-validation.md`)

## [0.4.0] - 2025-11-24

### Summary
Phase 4: Testing & Skills - Golden task harness and AI skill for result interpretation.

### Added
- **Golden Task Harness**
  - `tests/run_baseline_m4_smoke.py` - 5-step validation test
  - CSV schema validation, metrics range checks, summary content validation
  - Exit code 0/1 for CI integration
- **AI Skill**
  - `skills/nixtla-baseline-review/` - Claude skill for interpreting results
  - Reads metrics CSV and summary files
  - Identifies best-performing models, explains sMAPE/MASE values
- **Benchmark Reports**
  - `benchmark_report_*.md` - Markdown format for GitHub issues
  - Dataset details, statsforecast version, average metrics table

### Documentation
- Phase 4 AAR (`018-AA-AACR-phase-04-testing-and-skills.md`)

## [0.3.0] - 2025-11-24

### Summary
Phase 3: MCP Baselines & Nixtla OSS - Core statsforecast integration with M4 benchmark support.

### Added
- **Statsforecast Integration**
  - SeasonalNaive, AutoETS, AutoTheta models from Nixtla's `statsforecast`
  - M4 Daily dataset loading via `datasetsforecast`
  - Train/test splits with configurable horizon
- **Metrics Calculation**
  - sMAPE (Symmetric Mean Absolute Percentage Error)
  - MASE (Mean Absolute Scaled Error)
  - Per-series, per-model metrics tables
- **Power-User Parameters**
  - `models` - Select specific models to run
  - `freq` - Data frequency (D, H, W, M)
  - `season_length` - Seasonal period
  - `demo_preset` - Quick demo configurations (e.g., `m4_daily_small`)
- **Output Files**
  - `results_*.csv` - Metrics per series/model
  - `summary_*.txt` - Human-readable summary

### Documentation
- Phase 3 AAR (`017-AA-AACR-phase-03-mcp-baselines-nixtla-oss.md`)

## [0.2.0] - 2025-11-23

### Summary
First working plugin implementation! The Nixtla Search-to-Slack Digest plugin demonstrates automated content discovery and curation for time-series practitioners.

### Added
- **First Working Plugin: nixtla-search-to-slack**
  - Complete MVP implementation with 7 Python modules (~1,500 lines)
  - Web search via SerpAPI for Nixtla/time-series content
  - GitHub search for Nixtla organization repositories
  - AI summaries using OpenAI or Anthropic
  - Slack publishing with Block Kit formatting
  - Comprehensive test suite with 5 test files (~800 lines)
  - Full documentation with honest "construction kit" positioning
  - Configuration-driven with YAML files
  - Environment-based secrets management

- **Documentation Enhancements**
  - 6767 canonical document reference sheet (010-DR-REFF)
  - Complete plugin development guide (006-DR-GUID)
  - Search-to-Slack architecture document (012-AT-ARCH)
  - MVP planning document with phases (011-PP-PLAN)
  - PR description template (013-OD-PRDESC)

- **Knowledge Base**
  - Complete understanding of Claude Code plugin architecture
  - Integration patterns from 254+ production plugins
  - Skill creation with 2025 schema compliance
  - Marketplace integration patterns

### Changed
- Documentation numbering fixed (sequential 001-013, no gaps)
- Enhanced plugin development understanding
- Repository now contains working code, not just concepts

### Infrastructure
- Python plugin structure with src/ layout
- YAML configuration system for sources and topics
- Environment variable management with .env.example
- pytest test framework with conftest.py fixtures
- Modular architecture for easy extension

## [0.1.0] - 2025-11-23

### Summary
- Initial release of Claude Code Plugins for Nixtla concept repository
- Three plugin concepts defined for potential Nixtla collaboration
- Complete infrastructure and documentation for future plugin development

### Added
- **Repository Infrastructure**
  - Initial repository structure with proper organization
  - Comprehensive CI/CD pipeline with GitHub Actions
  - GitHub Pages documentation site at https://jeremylongshore.github.io/claude-code-plugins-nixtla/
  - Complete plugin validation and testing infrastructure

- **Documentation & Learning**
  - Three detailed plugin concepts with technical specifications
  - Educational resources linking to 254 production plugins from main marketplace
  - Issue templates for collaboration (Plugin Idea, Bug Report, Collaboration Request, Documentation)
  - Discussion guidelines for community engagement
  - Comprehensive README with clear positioning as Intent Solutions io work

- **Plugin Concepts**
  - TimeGPT Quickstart Pipeline Builder specification
  - Nixtla Bench Harness Generator specification
  - Forecast Service Template Builder (FastAPI) specification
  - Mermaid flowchart diagrams for each plugin concept

- **Security & Compliance**
  - Security warnings on all code examples
  - Environment variable handling for API keys
  - Audit trail documentation (101-RA-INTL-repo-audit)
  - CodeQL v3 security scanning

### Fixed
- CI/CD pipeline failures (CodeQL action v2 → v3)
- Missing test files for pytest
- Repository description and GitHub Pages visibility
- Removed misleading claims about existing plugins

### Infrastructure
- Python requirements.txt and requirements-dev.txt
- pytest.ini configuration
- GitHub Actions workflows (CI, plugin validation, security scanning)
- Document filing system v3.0 implementation

## [1.0.0] - 2025-01-01 (Planned)

### Added
- First stable release
- Production-ready TimeGPT deployer plugin
- Production-ready forecast validator plugin
- Complete test coverage (>90%)
- Comprehensive documentation
- Multi-cloud deployment support (AWS, Azure, GCP)
- Integration with Nixtla API ecosystem
- Command-line interface for natural language commands
- Plugin marketplace integration

### Features
- **TimeGPT Deployer**
  - Deploy models to any cloud platform
  - Automatic rollback on failure
  - Real-time status monitoring
  - Multi-region support

- **Forecast Validator**
  - Cross-model validation
  - Statistical metrics computation
  - Visual comparison reports
  - Performance benchmarking

### Infrastructure
- Docker containerization
- Kubernetes deployment manifests
- Terraform modules for cloud resources
- GitHub Actions for CI/CD

### Documentation
- User guide
- Developer documentation
- API reference
- Architecture documentation
- Contributing guidelines

## Version History

### Versioning Scheme

We use Semantic Versioning (SemVer):
- **MAJOR** version: Incompatible API changes
- **MINOR** version: Add functionality in backward-compatible manner
- **PATCH** version: Backward-compatible bug fixes

### Pre-release Versions

- **Alpha** (0.x.x): Early development, unstable API
- **Beta** (0.9.x): Feature complete, testing phase
- **Release Candidate** (1.0.0-rc.x): Final testing before stable release

## Upgrade Guide

### From 0.x to 1.0

When upgrading from pre-release versions to 1.0:

1. **Update plugin manifests**: The plugin.json schema has changed
2. **Migrate configuration**: New configuration format
3. **Update commands**: Some command syntax has changed

```bash
# Before (0.x)
/deploy-timegpt --production

# After (1.0)
/deploy-timegpt --env production --region us-central1
```

### Breaking Changes

Breaking changes will be documented here with migration guides.

## Release Process

1. **Feature Freeze**: 2 weeks before release
2. **Release Candidate**: 1 week before release
3. **Testing Period**: 5 days minimum
4. **Documentation Update**: Must be complete before release
5. **Release**: First Tuesday of the month

## How to Contribute

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details on:
- Submitting changes
- Commit message format
- Pull request process
- Release notes requirements

## Release Notes Template

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features added

### Changed
- Changes in existing functionality

### Deprecated
- Features marked for removal

### Removed
- Features removed

### Fixed
- Bug fixes

### Security
- Security vulnerability fixes
```

## Archive

Older versions and their changelogs can be found in the [releases page](https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases).

---

**Maintained by**: Jeremy Longshore (jeremy@intentsolutions.io)
**Repository**: [claude-code-plugins-nixtla](https://github.com/jeremylongshore/claude-code-plugins-nixtla)

[Unreleased]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.8.0
[0.7.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.7.0
[0.6.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.6.0
[0.5.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.5.0
[0.4.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.4.0
[0.3.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.3.0
[0.2.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.2.0
[0.1.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.1.0