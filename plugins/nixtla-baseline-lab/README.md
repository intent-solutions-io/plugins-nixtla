# Nixtla Baseline Lab – Claude Code Plugin

## What This Is

**Nixtla Baseline Lab** is a Claude Code plugin that runs Nixtla-style baseline time series forecasting models on public benchmark datasets (M4) directly inside your editor conversations.

This plugin demonstrates how to:
- Execute baseline forecasting workflows (SeasonalNaive, AutoETS, AutoTheta)
- Analyze model performance with AI-powered interpretation
- Generate reproducible benchmark results
- Integrate Nixtla's open-source forecasting stack into development workflows

## Who This Is For

This is an **internal Proof of Concept (PoC)** developed through collaboration between:
- **Nixtla** - Time series forecasting platform and research team
- **Intent Solutions** - AI/ML engineering and agent architecture

The plugin serves as a reference implementation for integrating Nixtla workflows into Claude Code, with patterns designed to scale to production agent systems.

## Data & Libraries

### Nixtla Open-Source Tools

This plugin uses Nixtla's open-source forecasting libraries:

- **`statsforecast`** - Classical statistical forecasting methods
  - SeasonalNaive (baseline benchmark)
  - AutoETS (exponential smoothing state space)
  - AutoTheta (Theta method with optimization)

- **`datasetsforecast`** - Benchmark time series datasets
  - M4 Competition datasets (Daily, Monthly, Quarterly, Yearly)
  - Standard evaluation utilities

### Public Benchmark Data Only

**Important**: This PoC uses **public benchmark datasets only**:
- M4 Daily dataset (starting point)
- No Nixtla customer data
- No production TimeGPT infrastructure
- No proprietary or sensitive time series

Future phases may integrate TimeGPT API for comparative analysis, but initial development focuses on reproducible open-source workflows.

## Plugin Components

This plugin demonstrates all major Claude Code plugin capabilities:

- **Commands** - `/nixtla-baseline-m4` slash command for running baseline models
- **Agents** - `nixtla-baseline-analyst` subagent for expert result interpretation
- **Skills** - `NixtlaBaselineReview` model-invoked capability for metric analysis
- **MCP Tools** - Local MCP server exposing `run_baselines` forecasting tool

## Documentation

For complete technical details, see the canonical 6767 documentation:

- **Architecture**: [`000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`](../../000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md)
  - Plugin structure and component design
  - Code examples for all components
  - Data flow and integration patterns
  - Testing and debugging workflows

- **Planning**: [`000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`](../../000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md)
  - Goals, non-goals, and scope
  - Phase-by-phase implementation plan
  - Success metrics and validation strategy
  - Future extension roadmap

## Status

**Current Phase**: Phase 1 - Repository structure and plugin skeleton

This README will be expanded in future phases to include:
- Setup and installation instructions
- How to enable the plugin in Claude Code
- How to run `/nixtla-baseline-m4` command
- Example workflows and outputs
- Troubleshooting guide

## License

MIT License - see repository root LICENSE file.

## Contact

- **Technical Lead**: Jeremy Longshore (jeremy@intentsolutions.io)
- **Nixtla Collaboration**: Max Mergenthaler (max@nixtla.io)
- **Repository**: https://github.com/jeremylongshore/claude-code-plugins-nixtla

---

**Version**: 0.1.0 (Phase 1)
**Last Updated**: 2025-11-24
