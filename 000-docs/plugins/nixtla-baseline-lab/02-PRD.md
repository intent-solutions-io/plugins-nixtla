# Baseline Lab - Product Requirements Document

**Plugin:** nixtla-baseline-lab
**Version:** 0.8.0
**Status:** Working
**Last Updated:** 2025-11-30

---

## Overview

Nixtla Baseline Lab is a Claude Code plugin that runs statsforecast baseline models on M4 benchmark data, generating reproducibility bundles for customer issue debugging and model validation.

---

## Goals & Non-Goals

### Goals
- [x] Enable one-command execution of baseline benchmarks (M4 datasets)
- [x] Generate human-readable metric summaries (sMAPE, MASE)
- [x] Create reproducibility bundles (versions, configs, data)
- [x] Provide GitHub-ready issue draft templates
- [x] Support optional TimeGPT comparison mode
- [x] Deliver results in <2 minutes for small datasets

### Non-Goals (Explicitly Out of Scope)
- [ ] Custom model training or fine-tuning
- [ ] Real-time forecasting on production data
- [ ] Multi-variate forecasting (single-series only for v0.8)
- [ ] Automated model deployment to production
- [ ] Integration with proprietary Nixtla infrastructure

---

## User Stories

| ID | As a... | I want to... | So that... | Priority |
|----|---------|--------------|------------|----------|
| US-01 | Nixtla Engineer | Run baseline benchmarks with one command | I can quickly validate statsforecast behavior | 🔴 Must |
| US-02 | Support Engineer | Generate complete repro bundles | I can debug customer issues with full context | 🔴 Must |
| US-03 | Data Scientist | Compare baseline vs TimeGPT results | I can demonstrate TimeGPT value-add | 🟡 Should |
| US-04 | Developer | See human-readable metric interpretations | I understand model performance without deep expertise | 🟡 Should |
| US-05 | Contributor | Create GitHub issues with benchmark data | I can report bugs with complete reproducibility | 🟡 Should |

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-01 | Support M4 Daily, Weekly, Monthly, Quarterly, Yearly datasets | 🔴 Must | Baseline Lab v0.8 |
| FR-02 | Run AutoETS, AutoTheta, SeasonalNaive models | 🔴 Must | Core statsforecast baselines |
| FR-03 | Calculate sMAPE and MASE metrics | 🔴 Must | Standard M4 evaluation |
| FR-04 | Generate metrics CSV with per-model results | 🔴 Must | Data export |
| FR-05 | Create reproducibility bundle (versions + config) | 🔴 Must | Issue debugging |
| FR-06 | Optional TimeGPT comparison mode | 🟡 Should | Cost-controlled, opt-in |
| FR-07 | GitHub issue draft generation | 🟡 Should | Streamline bug reporting |
| FR-08 | AI-powered metric interpretation | 🟡 Should | Nixtla Baseline Review skill |

### Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-01 | Performance (M4 Daily Small) | < 2 min | Wall-clock time |
| NFR-02 | Test Coverage | > 65% | pytest --cov |
| NFR-03 | Reproducibility | 100% | Same data + versions = same results |
| NFR-04 | API Cost (baseline mode) | $0 | Fully offline statsforecast |
| NFR-05 | Setup Time | < 5 min | From clone to first run |

---

## Success Metrics

| Metric | Target | Measurement Method | Timeline |
|--------|--------|-------------------|----------|
| Time saved per issue | 2-4 hours → 5 min | Manual tracking | Monthly |
| Engineer adoption | 80% of team | Usage logs | 90 days |
| Issue resolution speed | 2-3 days → 1 day | GitHub analytics | Quarterly |
| Repro bundle quality | 95% complete | Manual review | Per issue |

---

## Scope

### MVP (Phase 1-6) ✅ Complete
- M4 dataset integration
- StatsForecast baseline models
- Metrics calculation (sMAPE, MASE)
- CSV export
- Reproducibility bundles
- MCP server + slash command

### Phase 7 (Visualization) ✅ Complete
- Human-readable summaries
- GitHub issue drafts
- Agent skill for metric interpretation

### Phase 8 (TimeGPT Showdown) ✅ Complete
- Optional TimeGPT comparison
- Cost controls (opt-in only)
- Comparative analysis

### Future (Out of Scope for v0.8)
- Additional benchmark datasets (Electricity, Tourism, M3)
- Multi-variate forecasting
- Custom model configuration UI
- Automated CI/CD integration for continuous benchmarking

---

## Dependencies

| Dependency | Type | Owner | Status |
|------------|------|-------|--------|
| statsforecast ≥1.5.0 | Technical | Nixtla OSS | ✅ Stable |
| datasetsforecast | Technical | Nixtla OSS | ✅ Stable |
| nixtla SDK (TimeGPT) | Technical | Nixtla | ✅ Stable (opt-in) |
| Claude Code MCP framework | Technical | Anthropic | ✅ Stable |

---

## Open Questions

| Question | Owner | Due Date | Resolution |
|----------|-------|----------|------------|
| Expand to M3 datasets? | Nixtla Team | Q1 2026 | Pending feedback |
| Add MLForecast models? | Nixtla Team | Q1 2026 | Pending feedback |
| Production deployment strategy? | Intent Solutions | Q1 2026 | Awaiting engagement decision |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.8.0 | 2025-11-26 | TimeGPT comparison mode, opt-in cost controls |
| 0.7.0 | 2025-11-25 | Reproducibility bundles, GitHub issue drafts |
| 0.6.0 | 2025-11-24 | CI/CD pipeline, marketplace hardening |
| 0.1.0 | 2025-11-23 | Initial MVP with M4 Daily baseline |
