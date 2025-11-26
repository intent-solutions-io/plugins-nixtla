# Claude Code Plugins – Nixtla Baseline Lab

> Private, community-built Claude Code integration around Nixtla's statsforecast and TimeGPT for repeatable time series baseline experiments.

[![Private Repository](https://img.shields.io/badge/Repository-Private-red)](https://github.com/jeremylongshore/claude-code-plugins-nixtla)
[![Experimental](https://img.shields.io/badge/Status-Experimental-orange)](https://github.com/jeremylongshore/claude-code-plugins-nixtla)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> **Maintained by**: Intent Solutions (Jeremy Longshore)
> **Sponsored by**: Nixtla (Max Mergenthaler – early/enterprise supporter)
> **Status**: Experimental prototype | Private collaboration workspace

---

## What This Repo Is

This repository is a **developer sandbox** for building and testing Claude Code plugins on top of Nixtla's open-source time series stack.

**Key components**:

- **Nixtla Baseline Lab Plugin** – A Claude Code plugin that runs statsforecast baseline models (SeasonalNaive, AutoETS, AutoTheta) on M4 benchmark data or custom CSV files.
- **Metrics & Benchmarking** – Calculates sMAPE and MASE metrics, generates reproducible benchmark reports in Markdown format.
- **Repro Bundles** – Captures run configuration, library versions, and results for reproducibility.
- **GitHub Issue Draft Generator** – Helper tool to create pre-filled issue drafts for posting to `nixtla/statsforecast` (community plugin, not official Nixtla template).
- **Optional TimeGPT Showdown** – Opt-in comparison path for users with valid `NIXTLA_TIMEGPT_API_KEY` who want to compare baselines against Nixtla's TimeGPT foundation model on a small, controlled sample.

**What this enables**:

- CI-backed, reproducible statsforecast baseline experiments inside Claude Code.
- Easy capture of metrics, library versions, and run configurations for sharing with Nixtla maintainers or collaborators.
- A reference implementation showing how to integrate Nixtla OSS libraries into Claude Code plugins.

---

## What This Repo Is NOT

Set expectations clearly:

- **Not an official Nixtla product** – This is a community integration maintained by Intent Solutions, not by Nixtla. Nixtla is an early sponsor and collaborator, but this repo is not part of Nixtla's official tooling.
- **Not a production SLA or support commitment** – This is an experimental prototype intended for development, benchmarking, and reproducibility workflows. No guarantees about uptime, support, or maintenance timelines.
- **Not a guarantee of optimal performance** – The plugin runs statsforecast models with sensible defaults. It does not claim that any particular model or configuration will be optimal for all workloads. For production forecasting, consult Nixtla's official documentation and best practices.

**Framing**: This is a developer sandbox designed to make it easier for Nixtla users and maintainers to reproduce baseline behavior, share experiments, and collaborate on time series workflows inside Claude Code.

---

## Key Features (Phases 1–6)

The **Nixtla Baseline Lab** plugin currently supports:

### 1. Offline Statsforecast Baselines (Phases 1–3)

- **Models**: SeasonalNaive, AutoETS, AutoTheta from Nixtla's `statsforecast` library.
- **Datasets**:
  - **M4 Daily** subset (benchmark dataset via `datasetsforecast`).
  - **Custom CSV** files with columns `unique_id`, `ds`, `y`.
- **Metrics**: sMAPE (Symmetric Mean Absolute Percentage Error) and MASE (Mean Absolute Scaled Error).
- **Outputs**:
  - Metrics CSV (`results_*.csv`) with per-series, per-model metrics.
  - Human-readable summary file (`summary_*.txt`).

### 2. Benchmark Reports & Compatibility Info (Phase 4)

- **Benchmark Reports**: Markdown-formatted reports suitable for GitHub issues or documentation.
- **Compatibility Info**: Captures library versions (statsforecast, datasetsforecast, pandas, numpy) for reproducibility.
- **Version Introspection**: Auto-detects installed library versions to help with debugging and repro.

### 3. Repro Bundles & GitHub Issue Drafts (Phase 5)

- **Repro Bundle**:
  - `run_manifest.json` – Run configuration (dataset, horizon, models, freq, season_length).
  - `compat_info.json` – Library versions and environment details.
  - Metrics CSV, summary, and benchmark report (if generated).
- **GitHub Issue Draft Generator**:
  - MCP tool to create pre-filled Markdown issue drafts for `nixtla/statsforecast`.
  - Includes repro bundle details, making it easier to report questions or issues with full context.
  - **Note**: This is a community helper, not an official Nixtla issue template.

### 4. Optional TimeGPT Showdown (Phase 6)

- **Strictly Opt-In**: Disabled by default. Requires:
  - Explicit `include_timegpt=true` flag.
  - Valid `NIXTLA_TIMEGPT_API_KEY` environment variable.
- **Cost Control**: Limited to a small number of series (default 5, configurable via `timegpt_max_series`).
- **Graceful Degradation**: If TimeGPT is unavailable (missing key, SDK, or API error), the baseline run continues normally.
- **Showdown Report**: Text summary comparing TimeGPT forecasts to best statsforecast baseline on a limited sample (indicative, not conclusive).
- **Disclaimer**: This repo does not make any guarantees about TimeGPT availability, latency, or cost. Use Nixtla's official TimeGPT documentation as the source of truth.

---

## Quickstart (Offline / Statsforecast-Only)

**Safe default flow** (no API keys, no network calls, offline-only):

### 1. Clone and Setup

```bash
# Clone repo
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla

# Navigate to plugin
cd plugins/nixtla-baseline-lab

# Setup Python environment (creates .venv-nixtla-baseline)
./scripts/setup_nixtla_env.sh --venv

# Activate virtualenv
source .venv-nixtla-baseline/bin/activate

# Install plugin dependencies
pip install -r scripts/requirements.txt
```

### 2. Run Baseline Experiment

From Claude Code (after trusting the repo and installing the plugin):

```
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**What this does**:

- Loads M4 Daily dataset (subset of 5 series for quick demo).
- Runs SeasonalNaive, AutoETS, AutoTheta models with horizon=7.
- Calculates sMAPE and MASE metrics.
- Generates:
  - `results_M4_Daily_h7.csv` – Metrics table.
  - `summary_M4_Daily_h7.txt` – Human-readable summary.
  - `benchmark_report_M4_Daily_h7.md` – Markdown report.
  - `run_manifest.json` – Run configuration.
  - `compat_info.json` – Library versions.

**No API keys required. No network calls. Offline-only by default.**

### 3. Review Results

```bash
# View metrics
cat nixtla_baseline_m4_demo/results_M4_Daily_h7.csv

# View summary
cat nixtla_baseline_m4_demo/summary_M4_Daily_h7.txt

# View benchmark report
cat nixtla_baseline_m4_demo/benchmark_report_M4_Daily_h7.md
```

---

## Optional: TimeGPT Showdown (Opt-In Only)

**Requirements**:

1. Valid `NIXTLA_TIMEGPT_API_KEY` in your environment.
2. Explicit `include_timegpt=true` flag.
3. Understanding that this will make network calls to Nixtla's TimeGPT API and may incur costs.

**Example**:

```bash
# Set API key (never commit this!)
export NIXTLA_TIMEGPT_API_KEY="your-api-key-here"

# Run with TimeGPT showdown
/nixtla-baseline-m4 demo_preset=m4_daily_small include_timegpt=true timegpt_max_series=3
```

**What this does**:

- Runs statsforecast baselines as usual (offline).
- **Additionally**: Sends first 3 series to TimeGPT API for forecasts.
- Computes sMAPE and MASE for TimeGPT forecasts.
- Compares TimeGPT to best statsforecast baseline.
- Generates `timegpt_showdown_M4_Daily_h7.txt` with comparison summary.
- **Emphasis**: Results based on small sample (3 series) are **indicative, not conclusive**.

**Important Notes**:

- TimeGPT comparison is **optional** and has no impact on the default offline behavior.
- You are responsible for monitoring your TimeGPT API usage and costs.
- This repo makes no guarantees about TimeGPT availability, latency, or pricing.
- For official TimeGPT documentation, visit [docs.nixtla.io](https://docs.nixtla.io/).

---

## Repro Bundles & GitHub Issue Drafts

### Repro Bundle Structure

After running a baseline experiment, the output directory contains a **reproducibility bundle**:

```
nixtla_baseline_m4_demo/
├── results_M4_Daily_h7.csv          # Metrics (sMAPE, MASE per series/model)
├── summary_M4_Daily_h7.txt          # Human-readable summary
├── benchmark_report_M4_Daily_h7.md  # Markdown benchmark report
├── run_manifest.json                # Run configuration (dataset, horizon, models, etc.)
├── compat_info.json                 # Library versions (statsforecast, pandas, numpy)
└── timegpt_showdown_*.txt           # Optional TimeGPT comparison (if enabled)
```

**Purpose**: Makes it easy for Nixtla maintainers or collaborators to reproduce your exact run.

### GitHub Issue Draft Generator

The plugin includes an MCP tool to generate pre-filled GitHub issue drafts:

```
/nixtla-generate-issue-draft issue_type=question
```

**What this does**:

- Reads your repro bundle (metrics, manifest, compat info).
- Generates a Markdown file (`github_issue_draft.md`) with:
  - Issue template (question/bug/benchmark).
  - Complete benchmark results.
  - Run configuration and library versions.
  - Reproducibility information.

**How to use**:

1. Review `github_issue_draft.md`.
2. Fill in your specific question or description.
3. Post to [nixtla/statsforecast](https://github.com/Nixtla/statsforecast/issues) (manually – this is a draft generator, not an auto-poster).

**Note**: This is a **community helper tool**, not an official Nixtla issue template. Be respectful of maintainer time and include all reproducibility information from the draft.

---

## Nixtla & Sponsorship Context

**Nixtla** is an early and enterprise supporter of this experimental work.

- **Maintained by**: Intent Solutions (Jeremy Longshore) – not by Nixtla.
- **Sponsored by**: Nixtla (Max Mergenthaler) – provides guidance, feedback, and collaboration.
- **Purpose**: Make it easier for Nixtla users and maintainers to reproduce baseline behavior, share experiments, and collaborate on time series workflows inside Claude Code.

**This integration exists to**:

- Help developers run reproducible statsforecast experiments.
- Capture metrics, library versions, and run configurations for sharing with Nixtla maintainers.
- Demonstrate how Nixtla's OSS stack can integrate with Claude Code plugins.

**What this is NOT**:

- Not an official Nixtla product or endorsement.
- Not a replacement for Nixtla's official tooling or documentation.
- Not a production support commitment from Nixtla.

**For official Nixtla resources**:

- [Nixtla Documentation](https://docs.nixtla.io/)
- [statsforecast GitHub](https://github.com/Nixtla/statsforecast)
- [Nixtla Community Slack](https://join.slack.com/t/nixtlaworkspace/shared_invite/zt-135dssye9-fWTzMpv2WBthq8NK0Yvu6A)

---

## Documentation & Further Reading

### Plugin Documentation

- **[plugins/nixtla-baseline-lab/README.md](./plugins/nixtla-baseline-lab/README.md)** – Complete plugin manual with detailed setup, usage examples, and parameter documentation.

### Docs Site

- **[docs/index.md](./docs/index.md)** – Docs home page.
- **[docs/nixtla-baseline-lab.md](./docs/nixtla-baseline-lab.md)** – Plugin-level documentation.

### Architecture & Phase AARs (000-docs)

**Overview**:

- **[000-docs/6767-OD-OVRV-nixtla-baseline-lab-overview.md](./000-docs/6767-OD-OVRV-nixtla-baseline-lab-overview.md)** – High-level overview and phase summary.

**Architecture**:

- **[000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md](./000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md)** – Technical architecture and design decisions.
- **[000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md](./000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md)** – Implementation roadmap and phase breakdown.

**Phase After-Action Reports (AARs)**:

- **[015-AA-AACR-phase-01-structure-and-skeleton.md](./000-docs/015-AA-AACR-phase-01-structure-and-skeleton.md)** – Plugin scaffolding, marketplace setup.
- **[016-AA-AACR-phase-02-manifest-and-mcp.md](./000-docs/016-AA-AACR-phase-02-manifest-and-mcp.md)** – MCP server tools, JSON-RPC interface.
- **[017-AA-AACR-phase-03-mcp-baselines-nixtla-oss.md](./000-docs/017-AA-AACR-phase-03-mcp-baselines-nixtla-oss.md)** – Statsforecast baselines (SeasonalNaive, AutoETS, AutoTheta) + M4 integration.
- **[018-AA-AACR-phase-04-testing-and-skills.md](./000-docs/018-AA-AACR-phase-04-testing-and-skills.md)** – Golden task harness + AI skill for result interpretation.
- **[019-AA-AACR-phase-05-setup-and-validation.md](./000-docs/019-AA-AACR-phase-05-setup-and-validation.md)** – Setup script + dependency validation.
- **[020-AA-AACR-phase-06-ci-and-marketplace-hardening.md](./000-docs/020-AA-AACR-phase-06-ci-and-marketplace-hardening.md)** – GitHub Actions CI + marketplace finalization.
- **[021-AA-AACR-phase-07-visualization-csv-parametrization.md](./000-docs/021-AA-AACR-phase-07-visualization-csv-parametrization.md)** – Plot generation + custom CSV support.
- **[022-AA-AACR-phase-08-timegpt-showdown-and-evals.md](./000-docs/022-AA-AACR-phase-08-timegpt-showdown-and-evals.md)** – TimeGPT integration + showdown reports.
- **[032-AA-STAT-phase-06-timegpt-showdown-status.md](./000-docs/032-AA-STAT-phase-06-timegpt-showdown-status.md)** – Phase 6 status verification.
- **[033-AA-AACR-phase-06-timegpt-showdown.md](./000-docs/033-AA-AACR-phase-06-timegpt-showdown.md)** – Phase 6 AAR (optional TimeGPT showdown).

**Testing**:

- **[023-QA-TEST-nixtla-baseline-lab-test-coverage.md](./000-docs/023-QA-TEST-nixtla-baseline-lab-test-coverage.md)** – Comprehensive test coverage report.

---

## Repository Structure

```
claude-code-plugins-nixtla/
├── plugins/
│   └── nixtla-baseline-lab/        # Main plugin directory
│       ├── scripts/                # MCP server, TimeGPT client, setup
│       ├── skills/                 # AI skill for result interpretation
│       ├── tests/                  # Golden task harness
│       ├── data/                   # M4 dataset cache (auto-downloaded)
│       ├── README.md               # Plugin manual
│       └── manifest.json           # Plugin manifest
├── 000-docs/                       # Technical documentation
│   ├── 6767-OD-*.md               # Overview, architecture, planning
│   ├── 015-AA-AACR-*.md           # Phase AARs
│   └── 023-QA-TEST-*.md           # Test coverage
├── docs/                           # Docs site (MkDocs or similar)
│   ├── index.md                   # Docs home
│   └── nixtla-baseline-lab.md     # Plugin docs page
├── CLAUDE.md                       # Claude Code agent guidance
├── README.md                       # This file
└── LICENSE                         # MIT License
```

---

## Development Principles

**1. Respectful Integration**

- We build on top of Nixtla's OSS tools, not parallel to them.
- We focus on automation and reproducibility helpers, not replacement tooling.
- We acknowledge Nixtla's sophisticated existing infrastructure.

**2. Modest Framing**

- We avoid over-promising ("production-ready", "enterprise-grade", "guaranteed").
- We prefer "experimental", "prototype", "developer sandbox", "intended to help".
- We make no SLAs or support commitments.

**3. Technical Accuracy**

- We document what the plugin actually does, not what we hope it might do someday.
- We provide clear reproducibility information (library versions, run configurations).
- We emphasize offline-only default behavior and opt-in network paths.

**4. Human-Centered**

- We help developers reproduce experiments and share context with Nixtla maintainers.
- We provide draft templates and helpers, not automated posting bots.
- We require human review for all generated content (issue drafts, reports).

---

## Getting Started (Developer Setup)

### Prerequisites

- Python 3.12+
- Claude Code (latest version)
- Git

### Quick Setup

```bash
# Clone repo
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla

# Trust repo in Claude Code
# (Follow Claude Code prompts to trust the workspace)

# Navigate to plugin
cd plugins/nixtla-baseline-lab

# Setup environment
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate

# Install dependencies
pip install -r scripts/requirements.txt

# Run golden task (validation test)
python tests/run_baseline_m4_smoke.py
```

**Expected output**: All 5 validation checks pass (✓).

### CI Status

The plugin includes GitHub Actions CI that runs on every push/PR:

- Validates plugin manifest.
- Runs golden task harness (offline statsforecast baselines).
- Uploads test artifacts (7-day retention).

**CI remains offline-only** – No TimeGPT calls, no network dependencies.

---

## Collaboration

This is a **private workspace** for experimentation between Intent Solutions and Nixtla. We are:

- Prototyping reproducible baseline workflows before wider release.
- Validating integration patterns with real Nixtla codebases.
- Building community helpers that respect Nixtla's existing tooling.

**For questions or collaboration inquiries**:

- **Jeremy Longshore** (Intent Solutions): jeremy@intentsolutions.io | 251.213.1115
- **Max Mergenthaler** (Nixtla): max@nixtla.io

---

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## Acknowledgments

- **Nixtla Team**: For building world-class open-source time series forecasting tools and sponsoring this experimental integration work.
- **Max Mergenthaler**: For partnership, vision, and early/enterprise support.
- **Anthropic**: For Claude and the agent infrastructure that makes this possible.

---

**Maintained by**: Jeremy Longshore (Intent Solutions)
**Sponsored by**: Nixtla (Max Mergenthaler)
**Status**: Experimental Prototype | Private Collaboration
**Version**: 0.7.0 (Phase 7 – Docs Refresh)
