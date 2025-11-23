# Changelog

All notable changes to Claude Code Plugins for Nixtla will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v0.1.0
[1.0.0]: https://github.com/jeremylongshore/claude-code-plugins-nixtla/releases/tag/v1.0.0