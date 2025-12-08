# Nixtla Baseline Lab – Overview

**Document ID**: 6767-OD-OVRV-nixtla-baseline-lab-overview
**Title**: Nixtla Baseline Lab Overview (Phases 1–6 Summary)
**Status**: CURRENT
**Phase**: Phase 7 (Docs Refresh) – v0.7.0
**Related Docs**:
- Architecture: `6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`
- Plan: `6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`
- Phase AARs: `015-AA-AACR-*` through `033-AA-AACR-*`
- Test Coverage: `023-QA-TEST-nixtla-baseline-lab-test-coverage.md`

**Maintainer**: Jeremy Longshore (Intent Solutions, jeremy@intentsolutions.io)
**Sponsor**: Max Mergenthaler (Nixtla, max@nixtla.io)

---

## Executive Summary

The **Nixtla Baseline Lab** is an experimental Claude Code plugin that integrates Nixtla's open-source statsforecast library for reproducible time series baseline experiments. It runs classical forecasting models (SeasonalNaive, AutoETS, AutoTheta) on M4 benchmark data or custom CSV files, calculates standard metrics (sMAPE, MASE), and generates structured reproducibility bundles.

**What this is**:

- A **developer sandbox** for building Claude Code plugins on top of Nixtla's OSS time series stack.
- An **experimental prototype** for reproducible baseline experiments inside Claude Code.
- A **community integration** maintained by Intent Solutions, sponsored by Nixtla.

**What this is NOT**:

- Not an official Nixtla product or endorsement.
- Not a production SLA or support commitment.
- Not a guarantee of optimal performance for all workloads.

**Current Status**: Phase 7 (Docs Refresh) – v0.7.0 (2025-11-26)

---

## Phases Summary (1–6)

The plugin has been developed through six implementation phases:

### Phase 1: Structure & Skeleton (015-AA-AACR)

- Plugin scaffolding and directory structure.
- Local marketplace setup (`.claude-plugin/marketplace.json`).
- Initial manifest and basic command structure.

### Phase 2: Manifest & MCP (016-AA-AACR)

- MCP server implementation (`scripts/nixtla_baseline_mcp.py`).
- JSON-RPC tool definitions (`run_baselines` tool).
- Basic test mode for validation.

### Phase 3: MCP Baselines & Nixtla OSS (017-AA-AACR)

- statsforecast integration (SeasonalNaive, AutoETS, AutoTheta).
- M4 Daily dataset loading via `datasetsforecast`.
- Metrics calculation (sMAPE, MASE) with train/test splits.
- CSV and summary file outputs.

### Phase 4: Testing & Skills (018-AA-AACR)

- Golden task harness (`tests/run_baseline_m4_smoke.py`).
- AI skill for result interpretation (`skills/nixtla-baseline-review/`).
- Benchmark reports (Markdown format).
- Compatibility info (library versions capture).

### Phase 5: Setup & Validation (019-AA-AACR)

- Setup script (`scripts/setup_nixtla_env.sh`).
- Dependency validation and virtualenv support.
- Repro bundles (`run_manifest.json`, `compat_info.json`).
- GitHub issue draft generator.

### Phase 6: CI & Marketplace Hardening (020-AA-AACR, 032-AA-STAT, 033-AA-AACR)

- GitHub Actions CI workflow (`.github/workflows/nixtla-baseline-lab-ci.yml`).
- Marketplace finalization and auto-discovery.
- Optional TimeGPT showdown (opt-in, disabled by default).
- Power-user parameters (`models`, `freq`, `season_length`, `demo_preset`).

**Additional Phases** (documented separately):

- Phase 7: Visualization + CSV parametrization (021-AA-AACR).
- Phase 8: TimeGPT showdown + evals (022-AA-AACR).

---

## Key Capabilities (Current)

### 1. Offline Statsforecast Baselines

- **Models**: SeasonalNaive, AutoETS, AutoTheta from Nixtla's `statsforecast`.
- **Datasets**: M4 Daily subset (via `datasetsforecast`), custom CSV files.
- **Metrics**: sMAPE, MASE per series/model.
- **Outputs**: Metrics CSV, summary TXT, benchmark report (Markdown).
- **Default Behavior**: Offline-only, no API keys required, no network calls.

### 2. Reproducibility Bundles

- **run_manifest.json**: Run configuration (dataset, horizon, models, freq, season_length).
- **compat_info.json**: Library versions (statsforecast, datasetsforecast, pandas, numpy).
- **Purpose**: Makes it easy for Nixtla maintainers or collaborators to reproduce exact run.

### 3. GitHub Issue Draft Generator

- **Tool**: `generate_github_issue_draft` (MCP tool).
- **Purpose**: Creates pre-filled Markdown issue drafts for `nixtla/statsforecast`.
- **Includes**: Benchmark results, run configuration, library versions.
- **Note**: Community helper, not official Nixtla template. User reviews and manually posts.

### 4. Optional TimeGPT Showdown

- **Strictly Opt-In**: Disabled by default. Requires `include_timegpt=true` AND valid `NIXTLA_TIMEGPT_API_KEY`.
- **Cost Control**: Limited to small number of series (default 5, configurable).
- **Graceful Degradation**: TimeGPT failure doesn't break baseline run.
- **Output**: Text showdown report comparing TimeGPT vs best statsforecast baseline.
- **Disclaimer**: Results based on small sample (3-5 series) are indicative, not conclusive.

### 5. CI Validation

- **GitHub Actions**: Runs golden task harness on every push/PR.
- **Golden Task**: 5-step validation (CSV schema, metrics ranges, summary content).
- **Artifacts**: Test results uploaded (7-day retention).
- **CI Behavior**: Offline-only (no TimeGPT calls, no network dependencies).

---

## Target Users

**Intended for**:

- Developers familiar with Nixtla OSS (statsforecast, TimeGPT) who want to automate baseline experiments inside Claude Code.
- Nixtla maintainers/engineers who want reproducible repro for baseline experiments or questions.
- Plugin developers looking for reference implementations of Claude Code MCP servers, skills, and tools.

**Not intended for**:

- Users expecting production-ready, enterprise-grade forecasting infrastructure with SLAs.
- Teams needing official Nixtla support or guarantees.

---

## Use Cases

**Primary workflows**:

1. **Offline Baseline Experiments**: Run statsforecast models on M4/custom CSV, calculate metrics, generate reports.
2. **Reproducibility Sharing**: Capture run configuration + library versions + results in structured bundle for sharing with Nixtla maintainers.
3. **Optional TimeGPT Comparison**: Compare baselines vs TimeGPT on small, controlled sample (opt-in only).

**Example commands**:

```
# Quick demo (offline, 5 series, horizon=7)
/nixtla-baseline-m4 demo_preset=m4_daily_small

# Custom configuration
/nixtla-baseline-m4 horizon=14 series_limit=50 freq=D season_length=7

# With custom CSV
/nixtla-baseline-m4 dataset_type=csv csv_path=/path/to/data.csv horizon=7

# Generate GitHub issue draft
/nixtla-generate-issue-draft issue_type=question

# Optional TimeGPT showdown (requires API key)
/nixtla-baseline-m4 demo_preset=m4_daily_small include_timegpt=true timegpt_max_series=3
```

---

## Documentation Pointers

### User-Facing Docs

- **[Root README](../README.md)**: Repository overview, quickstart, collaboration context.
- **[Plugin Manual](../plugins/nixtla-baseline-lab/README.md)**: Complete user guide with detailed setup, parameters, and examples.

### Technical Docs (000-docs)

**Architecture & Planning**:

- `6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md` – Technical architecture.
- `6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md` – Implementation roadmap.

**Phase AARs** (After-Action Reports):

- `015-AA-AACR-phase-01-structure-and-skeleton.md` – Phase 1.
- `016-AA-AACR-phase-02-manifest-and-mcp.md` – Phase 2.
- `017-AA-AACR-phase-03-mcp-baselines-nixtla-oss.md` – Phase 3.
- `018-AA-AACR-phase-04-testing-and-skills.md` – Phase 4.
- `019-AA-AACR-phase-05-setup-and-validation.md` – Phase 5.
- `020-AA-AACR-phase-06-ci-and-marketplace-hardening.md` – Phase 6.
- `021-AA-AACR-phase-07-visualization-csv-parametrization.md` – Phase 7.
- `022-AA-AACR-phase-08-timegpt-showdown-and-evals.md` – Phase 8.
- `032-AA-STAT-phase-06-timegpt-showdown-status.md` – Phase 6 status verification.
- `033-AA-AACR-phase-06-timegpt-showdown.md` – Phase 6 AAR (TimeGPT showdown).

**Testing**:

- `023-QA-TEST-nixtla-baseline-lab-test-coverage.md` – Test coverage report.

---

## Collaboration Context

**Maintained by**: [Intent Solutions](https://intentsolutions.io) (Jeremy Longshore)
**Sponsored by**: [Nixtla](https://nixtla.io) (Max Mergenthaler – early/enterprise supporter)

**Relationship**:

- Nixtla is an early and enterprise supporter of this experimental work.
- This plugin is maintained by Intent Solutions, not by Nixtla.
- This is a community integration, not an official Nixtla product.

**Purpose**:

- Make it easier for Nixtla users and maintainers to reproduce baseline behavior.
- Capture metrics, library versions, and run configurations for sharing.
- Demonstrate how Nixtla's OSS stack can integrate with Claude Code plugins.

**For questions or collaboration**:

- **Jeremy Longshore**: jeremy@intentsolutions.io | 251.213.1115
- **Max Mergenthaler**: max@nixtla.io

---

## Safety & Scope Notes

**What to emphasize**:

- **Experimental** – This is a prototype for development and benchmarking, not a production system.
- **Community Integration** – Maintained by Intent Solutions, not by Nixtla.
- **Offline-Only Default** – No API keys required, no network calls unless explicitly opted in.
- **Modest Framing** – Avoid "production-ready", "enterprise-grade", "guaranteed". Prefer "experimental", "prototype", "developer sandbox", "intended to help".

**Nixtla as Source of Truth**:

- For official statsforecast behavior: [statsforecast docs](https://nixtlaverse.nixtla.io/statsforecast/)
- For TimeGPT documentation and pricing: [docs.nixtla.io](https://docs.nixtla.io/)
- For model selection and best practices: [Nixtla blog and tutorials](https://www.nixtla.io/blog)

**This plugin does NOT**:

- Make any guarantees about TimeGPT availability, latency, or cost.
- Promise SLAs or production support.
- Replace Nixtla's official tooling or documentation.

---

## Version History

- **v0.1.0** – Initial scaffold and MCP server (Phases 1-2).
- **v0.2.0** – Statsforecast baselines + metrics (Phase 3).
- **v0.3.0** – Golden task + AI skill (Phase 4).
- **v0.4.0** – Setup script + repro bundles (Phase 5).
- **v0.5.0** – CI + marketplace (Phase 6).
- **v0.6.0** – Visualization + CSV support (Phase 7).
- **v0.6.1** – TimeGPT showdown (Phase 8).
- **v0.7.0** – Docs refresh (Phase 7, current).

---

**End of Overview**

This document provides a compact summary of the Nixtla Baseline Lab plugin as of Phase 7 (v0.7.0). For detailed implementation notes, see the individual phase AARs listed above.
