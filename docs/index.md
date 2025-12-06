# Claude Code Plugins – Nixtla Baseline Lab Documentation

**Maintained by**: Intent Solutions (Jeremy Longshore)
**Sponsored by**: Nixtla (Max Mergenthaler – early/enterprise supporter)

> **Status**: Experimental prototype for reproducible statsforecast baseline experiments inside Claude Code.

---

## Welcome

This site documents a **Claude Code plugin workspace** built around Nixtla's time series forecasting tools. The primary component is the **Nixtla Baseline Lab** plugin, which enables reproducible baseline experiments using Nixtla's statsforecast library, with optional TimeGPT comparison paths.

**What this enables**:

- Run statsforecast baselines (SeasonalNaive, AutoETS, AutoTheta) on M4 benchmark data or custom CSV inside Claude Code.
- Calculate standard metrics (sMAPE, MASE) with reproducible outputs.
- Generate benchmark reports and repro bundles for sharing with Nixtla maintainers or collaborators.
- Optionally compare baselines against TimeGPT on a small, controlled sample (opt-in only).

**What this is NOT**:

- Not an official Nixtla product or endorsement.
- Not a production SLA or support commitment.
- Not a guarantee of optimal performance for all workloads.

---

## Who This Is For

This plugin workspace is intended for:

- **Developers familiar with Nixtla OSS** (statsforecast, TimeGPT, datasetsforecast) who want to automate baseline experiments inside Claude Code.
- **People evaluating Claude Code plugins** as a way to integrate time series workflows into their development environment.
- **Nixtla maintainers and engineers** who want a concrete, reproducible repro for baseline experiments or questions.
- **Plugin developers** looking for reference implementations of Claude Code MCP servers, skills, and tools.

**Not for**:

- Users expecting production-ready, enterprise-grade forecasting infrastructure with SLAs.
- Teams needing official Nixtla support or guarantees.

---

## Main Workflows

The Nixtla Baseline Lab plugin supports three core workflows:

### 1. Offline Statsforecast Baselines

**What it does**: Runs statsforecast models (SeasonalNaive, AutoETS, AutoTheta) on M4 Daily benchmark data or custom CSV files, calculates sMAPE and MASE metrics, and generates reproducible outputs.

**Key features**:

- No API keys required (offline-only by default).
- Configurable parameters: horizon, series_limit, models, freq, season_length.
- Demo presets for quick testing (e.g., `demo_preset=m4_daily_small`).

**Outputs**:

- Metrics CSV (`results_*.csv`)
- Human-readable summary (`summary_*.txt`)
- Markdown benchmark report (`benchmark_report_*.md`)

### 2. Repro Bundles & Benchmark Reports

**What it does**: Captures run configuration, library versions, and results in a structured bundle for reproducibility.

**Key features**:

- `run_manifest.json` – Run configuration (dataset, horizon, models, etc.)
- `compat_info.json` – Library versions (statsforecast, pandas, numpy)
- GitHub issue draft generator – Creates pre-filled Markdown drafts for `nixtla/statsforecast` (community helper, not official template)

**Use case**: Share complete reproducibility context with Nixtla maintainers or collaborators when asking questions or reporting issues.

### 3. Optional TimeGPT Showdown

**What it does**: Compares statsforecast baselines against Nixtla's TimeGPT foundation model on a small, controlled sample.

**Key features**:

- **Strictly opt-in** – Disabled by default, requires `include_timegpt=true` flag AND valid `NIXTLA_TIMEGPT_API_KEY`.
- **Cost control** – Limited to small number of series (default 5, configurable).
- **Graceful degradation** – TimeGPT failure doesn't break baseline run.

**Outputs**:

- `timegpt_showdown_*.txt` – Text comparison summary (TimeGPT vs best baseline)
- TimeGPT metadata in `run_manifest.json`

**Important notes**:

- Results based on small sample (3-5 series) are **indicative, not conclusive**.
- You are responsible for monitoring TimeGPT API usage and costs.
- This repo makes no guarantees about TimeGPT availability, latency, or pricing.

---

## Key Pages

### Plugin Documentation

- **[Nixtla Baseline Lab Plugin](nixtla-baseline-lab.md)** – Complete plugin overview, capabilities, and usage patterns.
- **[Plugin Manual (GitHub)](https://github.com/intent-solutions-io/plugins-nixtla/tree/main/plugins/nixtla-baseline-lab/README.md)** – Detailed setup, parameters, and examples.

### Repository Documentation

- **[Root README (GitHub)](https://github.com/intent-solutions-io/plugins-nixtla)** – Repository overview, quickstart, and collaboration context.
- **[Architecture Docs (000-docs)](https://github.com/intent-solutions-io/plugins-nixtla/tree/main/000-docs)** – Technical architecture, planning, and phase AARs.

---

## Quick Links

**Getting Started**:

- [Quickstart Guide](../README.md#quickstart-offline--statsforecast-only) – Run your first baseline in 5 minutes.
- [Developer Setup](../README.md#getting-started-developer-setup) – Full environment setup for contributors.

**Technical Details**:

- [Plugin Capabilities](nixtla-baseline-lab.md#core-capabilities) – What the plugin can do (Phases 1-6).
- [TimeGPT Showdown](nixtla-baseline-lab.md#optional-timegpt-showdown) – How the opt-in comparison works.

**Collaboration**:

- [Nixtla & Sponsorship Context](../README.md#nixtla--sponsorship-context) – Relationship between Intent Solutions and Nixtla.
- [Contact Information](../README.md#collaboration) – How to reach maintainers and sponsors.

---

## About This Project

**What it is**:

- A **developer sandbox** for building Claude Code plugins on top of Nixtla's OSS time series stack.
- An **experimental prototype** for reproducible baseline experiments inside Claude Code.
- A **reference implementation** showing how to integrate Nixtla libraries with Claude Code plugins.

**What it is NOT**:

- Not an official Nixtla product.
- Not a production SLA or support commitment.
- Not a guarantee of optimal performance for all workloads.

**Maintained by**: [Intent Solutions](https://intentsolutions.io) (Jeremy Longshore)
**Sponsored by**: [Nixtla](https://nixtla.io) (Max Mergenthaler – early/enterprise supporter)

**For questions or collaboration**:

- **Jeremy Longshore**: jeremy@intentsolutions.io | 251.213.1115
- **Max Mergenthaler**: max@nixtla.io

---

## Official Nixtla Resources

For official Nixtla documentation, support, and resources:

- [Nixtla Documentation](https://docs.nixtla.io/)
- [statsforecast GitHub](https://github.com/Nixtla/statsforecast)
- [TimeGPT Documentation](https://docs.nixtla.io/docs/getting-started-timegpt)
- [Nixtla Community Slack](https://join.slack.com/t/nixtlaworkspace/shared_invite/zt-135dssye9-fWTzMpv2WBthq8NK0Yvu6A)

---

*This is a community integration maintained by Intent Solutions. For official Nixtla products and support, visit [nixtla.io](https://nixtla.io).*
