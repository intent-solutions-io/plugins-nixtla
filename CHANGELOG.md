# Changelog

All notable changes to Claude Code Plugins for Nixtla will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/compare/v0.7.0...HEAD
[0.7.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.7.0
[0.6.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.6.0
[0.5.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.5.0
[0.4.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.4.0
[0.3.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.3.0
[0.2.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.2.0
[0.1.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.1.0