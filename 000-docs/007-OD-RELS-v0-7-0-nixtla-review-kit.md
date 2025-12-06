# Nixtla Review Kit – v0.7.0 Release Overview

**Document ID**: 035-OD-RELS-v0-7-0-nixtla-review-kit
**Title**: Nixtla Baseline Lab v0.7.0 – Review Kit for Nixtla Engineers
**Category**: Release/Overview (OD-RELS)
**Status**: COMPLETE
**Classification**: Project-Specific
**Date**: 2025-11-26
**Owner**: Jeremy Longshore (jeremy@intentsolutions.io)

**Related Docs**:
- `024-AA-STAT-phase-01-already-complete.md` – Phase 1 status
- `025-AA-STAT-phase-02-metrics-already-complete.md` – Phase 2 status
- `026-AA-STAT-phase-03-implementation-status.md` – Phase 3 status
- `027-AA-AACR-phase-03-power-user-controls.md` – Phase 3 AAR
- `028-AA-STAT-phase-04-benchmark-compat-status.md` – Phase 4 status
- `029-AA-AACR-phase-04-benchmark-compatibility.md` – Phase 4 AAR
- `030-AA-STAT-phase-05-repro-bundle-status.md` – Phase 5 status
- `031-AA-AACR-phase-05-repro-bundle-github-issues.md` – Phase 5 AAR
- `032-AA-STAT-phase-06-timegpt-showdown-status.md` – Phase 6 status
- `033-AA-AACR-phase-06-timegpt-showdown.md` – Phase 6 AAR
- `034-AA-AACR-release-v0.7.0.md` – Release AAR
- `README.md` – Root repository documentation
- `docs/nixtla-baseline-lab.md` – Plugin documentation
- `plugins/nixtla-baseline-lab/README.md` – Plugin manual

---

## Executive Summary

The **Nixtla Baseline Lab v0.7.0** is an experimental, developer-focused Claude Code plugin that integrates Nixtla's open-source statsforecast library for reproducible time series baseline experiments. It provides:

- **Offline statsforecast baselines** (SeasonalNaive, AutoETS, AutoTheta) on M4 Daily or custom CSV data
- **Standard metrics** (sMAPE, MASE) with train/test splits
- **Reproducibility bundles** capturing run configuration and library versions
- **Optional TimeGPT comparison** (strictly opt-in, cost-controlled, graceful degradation)
- **GitHub issue draft generator** for community collaboration with `nixtla/statsforecast`

**What this is**:
- An **experimental workspace** for Nixtla engineers to reproduce baseline behavior
- A **developer sandbox** demonstrating Nixtla OSS integration patterns
- A **community helper** maintained by Intent Solutions, sponsored by Nixtla (Max Mergenthaler)

**What this is NOT**:
- ❌ Not an official Nixtla product or endorsement
- ❌ Not production-ready or enterprise-grade
- ❌ Not a guarantee of optimal performance for all workloads
- ❌ Not a replacement for Nixtla's official tooling or documentation

**Phases implemented**: Phases 1-7 (statsforecast baselines, metrics, power-user controls, benchmark reports, repro bundles, optional TimeGPT showdown, docs refresh)

---

## How a Nixtla Engineer Can Review This (2 Minutes)

### Prerequisites
- Linux/macOS machine with Python 3.9+
- Git installed
- No API keys required for offline baseline review

### Quick Review Path (Offline Baselines Only)

```bash
# 1. Clone repository
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla

# 2. Run offline baseline demo (no API keys needed)
./scripts/run_nixtla_review_baseline.sh
```

**What happens**:
1. Sets up Python virtualenv (if needed)
2. Installs statsforecast, datasetsforecast, pandas, numpy
3. Runs SeasonalNaive, AutoETS, AutoTheta on 5 M4 Daily series
4. Calculates sMAPE and MASE metrics
5. Generates CSV, summary, benchmark report, and repro bundle

**Where to find results**:
```
plugins/nixtla-baseline-lab/nixtla_baseline_m4_test/
├── results_M4_Daily_h7.csv           # Per-series, per-model metrics
├── summary_M4_Daily_h7.txt           # Human-readable summary
├── benchmark_report_M4_Daily_h7.md   # Markdown benchmark report
├── run_manifest.json                 # Run configuration (reproducibility)
└── compat_info.json                  # Library versions (statsforecast, pandas, numpy)
```

**Review checklist**:
- ✅ Check `summary_M4_Daily_h7.txt` – Does it show sMAPE/MASE for all 3 models?
- ✅ Check `results_M4_Daily_h7.csv` – Does it have columns for `unique_id`, `model`, `sMAPE`, `MASE`?
- ✅ Check `benchmark_report_M4_Daily_h7.md` – Is it formatted for GitHub?
- ✅ Check `run_manifest.json` – Does it capture horizon, models, freq, season_length?
- ✅ Check `compat_info.json` – Does it show statsforecast version?

### Optional TimeGPT Review Path (Requires API Key)

**COST WARNING**: This makes REAL TimeGPT API calls (limited to 3 series).

```bash
# 1. Set your TimeGPT API key
export NIXTLA_TIMEGPT_API_KEY="your-api-key-here"

# 2. Run TimeGPT showdown demo
./scripts/run_nixtla_review_timegpt.sh
```

**What happens**:
1. Checks for `NIXTLA_TIMEGPT_API_KEY` (exits gracefully if not set)
2. Installs `nixtla` SDK if not present
3. Runs statsforecast baselines + TimeGPT forecasts on 3 series
4. Compares TimeGPT vs best baseline (AutoETS/AutoTheta)
5. Generates showdown report

**Additional output**:
```
plugins/nixtla-baseline-lab/nixtla_baseline_m4_test/
└── timegpt_showdown_M4_Daily_h7.txt  # TimeGPT vs baseline comparison
```

**Review checklist**:
- ✅ Check `timegpt_showdown_M4_Daily_h7.txt` – Does it compare TimeGPT vs best baseline?
- ✅ Verify `run_manifest.json` includes `include_timegpt: true` and `timegpt_max_series: 3`
- ✅ Confirm showdown report has clear disclaimer about small sample size

---

## What This Shows

### Core Capabilities

1. **Statsforecast Integration**
   - Real Nixtla OSS models (SeasonalNaive, AutoETS, AutoTheta)
   - M4 Daily benchmark dataset loading via `datasetsforecast`
   - Custom CSV support (`unique_id`, `ds`, `y` columns)
   - Configurable parameters: `horizon`, `series_limit`, `freq`, `season_length`

2. **Metrics Pipeline**
   - sMAPE (Symmetric Mean Absolute Percentage Error): 0-200%, lower = better
   - MASE (Mean Absolute Scaled Error): <1.0 = better than naive, >1.0 = worse
   - Train/test splits with configurable horizon
   - Per-series, per-model granularity

3. **Reproducibility Artifacts**
   - `run_manifest.json` – Complete run configuration for exact reproduction
   - `compat_info.json` – Library versions (statsforecast, pandas, numpy, python)
   - Timestamp metadata for audit trails

4. **Benchmark Reports**
   - Markdown-formatted reports suitable for GitHub issues
   - Average metrics table (sorted by performance)
   - Highlights section with key insights
   - statsforecast version for reproducibility

5. **GitHub Issue Draft Generator**
   - MCP tool: `generate_github_issue_draft`
   - Creates pre-filled issue templates for `nixtla/statsforecast`
   - Includes benchmark results, run config, library versions
   - **Note**: Community helper, not official Nixtla template

6. **Optional TimeGPT Showdown**
   - **Strictly opt-in** (requires explicit flag + API key)
   - Cost-controlled (default 5 series, configurable)
   - Graceful degradation (TimeGPT failure doesn't break baseline run)
   - Clear disclaimers about small sample size

### Power-User Parameters

The plugin supports fine-grained control:

```python
# Example MCP tool call structure
run_baselines(
    dataset_type="m4",           # or "csv"
    horizon=7,                   # forecast horizon
    series_limit=5,              # number of series to process
    models=["AutoETS", "AutoTheta"],  # select specific models
    freq="D",                    # data frequency (D, H, W, M)
    season_length=7,             # seasonal period
    demo_preset="m4_daily_small",  # quick demo config
    include_timegpt=False,       # opt-in TimeGPT comparison
    timegpt_max_series=5         # cost control
)
```

### CI/CD Integration

- **GitHub Actions workflow** (`.github/workflows/nixtla-baseline-lab-ci.yml`)
- Runs golden task harness on every push/PR
- 5-step validation (CSV schema, metrics ranges, summary content)
- **CI remains offline-only** (no TimeGPT calls, no network dependencies)

---

## What This Does Not Promise

This repository is an **experimental, community-built integration**. It makes **no guarantees** about:

### Not Promised
- ❌ Production readiness or enterprise-grade quality
- ❌ SLAs or uptime guarantees
- ❌ Long-term maintenance commitments
- ❌ Official Nixtla support or endorsement
- ❌ Optimal performance for all workloads
- ❌ TimeGPT availability, latency, or cost guarantees

### Nixtla Remains the Source of Truth

For official information, always refer to Nixtla:

- **statsforecast behavior**: [nixtlaverse.nixtla.io/statsforecast](https://nixtlaverse.nixtla.io/statsforecast/)
- **TimeGPT documentation**: [docs.nixtla.io](https://docs.nixtla.io/)
- **Model selection best practices**: [nixtla.io/blog](https://www.nixtla.io/blog)
- **Pricing and policies**: [dashboard.nixtla.io](https://dashboard.nixtla.io/)

This plugin is intended to **help developers reproduce baseline behavior**, not to replace Nixtla's official tooling or documentation.

---

## Use Cases for Nixtla Engineers

### 1. Reproducing Baseline Behavior

**Scenario**: User reports unexpected statsforecast results on M4 Daily data.

**Workflow**:
1. User runs this plugin and generates repro bundle
2. User shares `run_manifest.json` + `compat_info.json` + `results_*.csv`
3. Nixtla engineer can reproduce exact setup:
   - Same statsforecast version
   - Same M4 subset
   - Same horizon, freq, season_length
4. Engineer confirms or debugs behavior

### 2. Benchmark Comparison

**Scenario**: Nixtla wants to test statsforecast improvements on M4 benchmarks.

**Workflow**:
1. Run baseline with current statsforecast version
2. Upgrade statsforecast
3. Run baseline again with same config
4. Compare `results_*.csv` files to see metric improvements
5. Repro bundles provide exact configurations for both runs

### 3. TimeGPT Validation (Optional)

**Scenario**: Nixtla wants to validate TimeGPT improvements on small sample.

**Workflow**:
1. Run `scripts/run_nixtla_review_timegpt.sh` with API key
2. Review `timegpt_showdown_*.txt` comparison
3. Check if TimeGPT beats baselines on sample
4. **Remember**: 3-5 series is indicative, not conclusive

### 4. Community Issue Triage

**Scenario**: Community member asks "Why is AutoETS better than AutoTheta on my data?"

**Workflow**:
1. User runs plugin on their CSV data
2. User generates GitHub issue draft with `generate_github_issue_draft` tool
3. Issue draft includes:
   - Complete metrics CSV
   - Statsforecast version
   - Run configuration
   - Library versions
4. Nixtla engineer can reproduce or debug with complete context

---

## Architecture Overview

### Components

```
nixtla-baseline-lab/
├── scripts/
│   ├── nixtla_baseline_mcp.py       # MCP server (JSON-RPC tools)
│   ├── requirements.txt             # Python dependencies
│   └── setup_nixtla_env.sh          # Virtualenv setup
├── skills/
│   └── nixtla-baseline-review/      # AI skill for result interpretation
├── tests/
│   └── run_baseline_m4_smoke.py     # Golden task harness (5 validations)
├── .claude-plugin/
│   └── plugin.json                  # Plugin manifest (v0.7.0)
└── README.md                        # Plugin manual
```

### MCP Tools Exposed

1. **`run_baselines`** – Core baseline experiment runner
2. **`generate_benchmark_report`** – Create Markdown benchmark reports
3. **`generate_github_issue_draft`** – Create pre-filled issue templates

### AI Skill

- **Name**: `nixtla-baseline-review`
- **Purpose**: Claude interprets baseline results
- **Capabilities**:
  - Reads metrics CSV and summary files
  - Identifies best-performing models
  - Explains sMAPE/MASE values in human terms
  - Provides recommendations based on results
  - Handles TimeGPT showdown interpretation (when enabled)

---

## Development Workflow

### For Nixtla Engineers Contributing

If you want to modify or extend this plugin:

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla

# 2. Set up development environment
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# 3. Make changes to scripts/nixtla_baseline_mcp.py

# 4. Test changes
python scripts/nixtla_baseline_mcp.py test

# 5. Run golden task harness
cd tests && python run_baseline_m4_smoke.py

# 6. Commit and push
git add .
git commit -m "feat(baseline-lab): add new feature"
git push origin feature-branch
```

### CI/CD Pipeline

All changes trigger:
1. Plugin manifest validation
2. Golden task harness (5-step validation)
3. Artifact upload (test results, 7-day retention)
4. **No TimeGPT calls in CI** (offline-only validation)

---

## Version History

| Version | Date | Phase | Summary |
|---------|------|-------|---------|
| 0.1.0 | 2025-11-23 | Phase 1-2 | Initial scaffolding, Search-to-Slack plugin |
| 0.2.0 | 2025-11-23 | Phase 2 | First working Search-to-Slack plugin |
| 0.3.0 | 2025-11-24 | Phase 3 | Core statsforecast integration, M4 benchmarks |
| 0.4.0 | 2025-11-24 | Phase 4 | Golden task, AI skill, benchmark reports |
| 0.5.0 | 2025-11-24 | Phase 5 | Repro bundles, GitHub issue draft generator |
| 0.6.0 | 2025-11-25 | Phase 6 | Optional TimeGPT showdown (opt-in) |
| **0.7.0** | **2025-11-26** | **Phase 7** | **Docs refresh, Nixtla Review Kit** |

---

## Collaboration Context

**Maintained by**: [Intent Solutions](https://intentsolutions.io) (Jeremy Longshore)
**Sponsored by**: [Nixtla](https://nixtla.io) (Max Mergenthaler – early/enterprise supporter)

**Relationship**:
- Nixtla is an early and enterprise supporter of this experimental work
- This plugin is maintained by Intent Solutions, not by Nixtla
- This is a community integration, not an official Nixtla product

**For questions or collaboration**:
- **Jeremy Longshore**: jeremy@intentsolutions.io | 251.213.1115
- **Max Mergenthaler**: max@nixtla.io

---

## Next Steps for Reviewers

### If You're a Nixtla Engineer

1. **Quick smoke test** (2 minutes):
   ```bash
   ./scripts/run_nixtla_review_baseline.sh
   ```

2. **Review outputs**:
   - Check summary for sanity (sMAPE < 20%, MASE < 2.0)
   - Confirm CSV has all expected columns
   - Verify repro bundle captures config + versions

3. **Optional TimeGPT test** (if curious):
   ```bash
   export NIXTLA_TIMEGPT_API_KEY="..."
   ./scripts/run_nixtla_review_timegpt.sh
   ```

4. **Provide feedback**:
   - Is this useful for reproducing statsforecast issues?
   - Are the repro bundles sufficient for debugging?
   - Any missing features or metrics?

### If You're Max (Sponsor)

This v0.7.0 release packages Phases 1-7 as a **lightweight review artifact** for Nixtla engineers. Key achievements:

- ✅ Statsforecast baselines work offline (no API keys)
- ✅ Repro bundles capture exact configurations
- ✅ TimeGPT showdown is strictly opt-in with cost control
- ✅ Documentation is modest and technically accurate
- ✅ CI/CD validates offline behavior only
- ✅ Two helper scripts for easy review

No action required unless you want to test the review scripts yourself.

---

## FAQ

### Q: Is this production-ready?
**A**: No. This is an experimental workspace for reproducible experiments. Use Nixtla's official SDKs for production.

### Q: Does this require API keys?
**A**: No for offline baselines. Yes (optional) for TimeGPT showdown.

### Q: Will TimeGPT calls happen automatically?
**A**: No. TimeGPT requires explicit `include_timegpt=true` flag AND valid API key. Default is offline-only.

### Q: Can I use custom data?
**A**: Yes. Provide CSV with `unique_id`, `ds`, `y` columns. See plugin README for details.

### Q: Who supports this?
**A**: Community-maintained by Intent Solutions. For official Nixtla support, use official channels.

### Q: Can I modify this?
**A**: Yes! Fork, modify, contribute. MIT license. See `CONTRIBUTING.md` for guidelines.

---

**End of Nixtla Review Kit**

*Timestamp: 2025-11-26*
*Version: v0.7.0*
*Maintained by: Jeremy Longshore (Intent Solutions)*
*Sponsored by: Max Mergenthaler (Nixtla)*
