# Nixtla Baseline Lab – Product Overview

**Document ID**: 6767-OD-OVRV-nixtla-baseline-lab-product-overview
**Title**: Nixtla Baseline Lab Product Overview (Who/What/When/Where/Why)
**Status**: CURRENT
**Phase**: Production (v0.6.0)
**Related Docs**:
- Architecture: `6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`
- Plan: `6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`
- Phase AARs: `015-AA-AACR-*` through `022-AA-AACR-*`
- Test Coverage: `023-QA-TEST-nixtla-baseline-lab-test-coverage.md`

**Maintainer**: Jeremy Longshore (jeremy@intentsolutions.io)
**Collaboration**: Max Mergenthaler (Nixtla CEO)

---

## Executive Summary

The **Nixtla Baseline Lab** is a production-ready Claude Code plugin that brings Nixtla's open-source time series forecasting baselines (SeasonalNaive, AutoETS, AutoTheta) into Claude Code conversations. It runs reproducible benchmark experiments on M4 Daily datasets and custom CSVs, generates standardized metrics (sMAPE, MASE), and provides AI-powered interpretation. Optional TimeGPT integration enables quick baseline vs foundation model comparisons.

**Current Status**: ✅ **v0.6.0 RELEASED** (2025-11-25)

---

## Who: Target Users

### Primary Personas

**1. Nixtla CEO / Leadership**
- **Needs**: Quickly validate baseline performance without writing code
- **Use Case**: Check that OSS baselines are working correctly, optionally compare vs TimeGPT
- **Value**: Business confidence in baseline quality, directional insights for strategic decisions
- **Interaction**: Natural language commands + AI Skill interpretation

**2. Technical Collaborators (Data Scientists, ML Engineers)**
- **Needs**: Run reproducible baseline experiments with standardized evaluation
- **Use Case**: Benchmark custom datasets, validate model changes, compare approaches
- **Value**: Automated baseline generation, consistent methodology, CI validation
- **Interaction**: Commands + parameters + direct file outputs (CSV, plots, summaries)

**3. Nixtla Engineering Team**
- **Needs**: Ensure OSS baselines produce expected results on M4 benchmarks
- **Use Case**: CI validation, regression testing, golden task verification
- **Value**: Catch baseline degradation early, maintain quality standards
- **Interaction**: GitHub Actions CI, golden task harness, automated validation

**4. Plugin Developers / Reference Users**
- **Needs**: Learn Claude Code plugin patterns and best practices
- **Use Case**: Study comprehensive plugin implementation (Commands, Skills, Agents, MCP)
- **Value**: Working example with production-grade structure, documentation, testing
- **Interaction**: Code review, documentation study, pattern adaptation

---

## What: Product Capabilities

### Core Features (v0.6.0)

**1. Baseline Model Execution**
- **Models**: SeasonalNaive, AutoETS, AutoTheta (via `statsforecast`)
- **Datasets**: M4 Daily (4,227 series), custom CSV files
- **Metrics**: sMAPE (Symmetric Mean Absolute Percentage Error), MASE (Mean Absolute Scaled Error)
- **Output**: CSV with per-series metrics, summary TXT with aggregated results

**2. AI-Powered Interpretation**
- **Skill**: `nixtla-baseline-review` reads metrics and explains performance
- **Capability**: Identifies best model, explains why, highlights patterns
- **Interface**: Natural language questions → structured answers with context

**3. Custom Data Support**
- **Format**: CSV with required columns (`unique_id`, `ds`, `y`)
- **Flexibility**: Any frequency (daily, monthly, etc.), any number of series
- **Validation**: Schema checking, missing column detection, graceful errors

**4. Visualization (Optional)**
- **Format**: PNG forecast plots per series
- **Models**: Shows all three baseline forecasts + actual values
- **Dependency**: Matplotlib (installed by default, gracefully skipped if missing)

**5. TimeGPT Comparison (Optional)**
- **Integration**: Nixtla TimeGPT SDK (`nixtla>=0.5.0`, installed by default)
- **Feature Gating**: Opt-in via `include_timegpt` flag + `NIXTLA_TIMEGPT_API_KEY` env var
- **Output**: Showdown report comparing baseline best vs TimeGPT on small sample (3-5 series)
- **Cost Control**: Default `timegpt_max_series=5`, max=20 to cap API usage

**6. CI/CD Integration**
- **GitHub Actions**: Runs baseline tests on every push/PR to main
- **Golden Task**: 5-step validation harness (CSV schema, metrics ranges, summary content)
- **Artifacts**: Test results uploaded and retained for 7 days (even on failures)
- **Status**: Badge shows CI health

---

## When: Use Cases

### Primary Use Cases

**1. Validating Nixtla OSS Baselines**
- **Trigger**: After library updates, model changes, or dependency upgrades
- **Process**: Run `/nixtla-baseline-m4` → Check CI green → Review metrics
- **Outcome**: Confidence that baselines produce expected M4 Daily results

**2. Sanity-Checking Custom Time Series**
- **Trigger**: New dataset acquisition, data pipeline changes
- **Process**: Export to CSV → Run with `--dataset-type csv --csv-path <path>`
- **Outcome**: Quick assessment of baseline performance vs M4 standards

**3. Baseline vs TimeGPT Comparison**
- **Trigger**: Evaluating whether TimeGPT adds value for specific use case
- **Process**: Run with `--include-timegpt` → Read showdown report → Assess directional insights
- **Outcome**: Small-sample comparison (not comprehensive benchmark) for decision-making

**4. CI Regression Testing**
- **Trigger**: Every push/PR to main branch
- **Process**: GitHub Actions runs golden task automatically
- **Outcome**: Early detection of baseline degradation or breaking changes

**5. Educational / Demo**
- **Trigger**: Teaching forecasting concepts, demonstrating Nixtla tools
- **Process**: Run baseline with plots → Show AI interpretation → Explain metrics
- **Outcome**: Visual + narrative understanding of baseline forecasting

---

## Where: Deployment Context

### Runtime Environment

**Claude Code Integration**:
- **Platform**: Claude Code desktop application (macOS, Windows, Linux)
- **Installation**: Local marketplace (`nixtla-dev-marketplace`) defined in `.claude-plugin/marketplace.json`
- **Discovery**: Automatic when repo is trusted in Claude Code
- **Execution**: In-process Python execution via MCP server

**Python Environment**:
- **Virtualenv**: `.venv-nixtla-baseline` (isolated dependencies)
- **Python Version**: 3.10+ (tested on 3.12)
- **Dependencies**: statsforecast, datasetsforecast, pandas, numpy, matplotlib, nixtla
- **Setup**: `setup_nixtla_env.sh` script or manual `pip install -r requirements.txt`

**File System**:
- **Plugin Location**: `plugins/nixtla-baseline-lab/`
- **Data Cache**: `plugins/nixtla-baseline-lab/data/` (M4 datasets downloaded once)
- **Output**: User-specified directory (default: `nixtla_baseline_m4_test/`)
- **Artifacts**: CSV, TXT, optional PNG plots, showdown reports

### CI/CD Environment

**GitHub Actions**:
- **Runner**: `ubuntu-latest` (Python 3.12)
- **Triggers**: Push to main, PR to main (paths: `plugins/nixtla-baseline-lab/**`)
- **Steps**: Setup Python → Install deps → Run MCP test → Run golden task → Upload artifacts
- **Caching**: Pip cache for faster dependency installation
- **Artifacts**: `nixtla-baseline-test-results` (7-day retention)

**Supported Platforms**:
- **Primary**: Ubuntu/Linux (CI + primary development)
- **Recommended**: macOS (full testing)
- **Supported**: Windows via WSL (not tested in CI)

---

## Why: Business & Technical Rationale

### Business Rationale

**1. CEO Confidence in OSS Baselines**
- **Problem**: Hard to quickly verify that Nixtla OSS baselines work correctly
- **Solution**: One-command execution + AI explanation of results
- **Impact**: Leadership can validate quality without engineering deep-dive

**2. Standardized Evaluation Methodology**
- **Problem**: Inconsistent baseline evaluation across projects/teams
- **Solution**: Reproducible workflow with standardized metrics (sMAPE, MASE) on M4
- **Impact**: Apples-to-apples comparisons, consistent quality standards

**3. TimeGPT Positioning**
- **Problem**: Need directional insights on TimeGPT value vs baselines
- **Solution**: Small-sample showdown reports with clear disclaimers
- **Impact**: Informed conversations with customers/partners about when TimeGPT adds value

**4. Reference Implementation**
- **Problem**: Plugin ecosystem needs production-quality examples
- **Solution**: Comprehensive demo of all Claude Code plugin capabilities
- **Impact**: Faster plugin adoption, higher quality community plugins

### Technical Rationale

**1. Automation of Repetitive Tasks**
- **Problem**: Running baseline benchmarks is tedious, error-prone
- **Solution**: Automated workflow with CI validation
- **Impact**: Engineers focus on research/modeling, not manual benchmarking

**2. Early Regression Detection**
- **Problem**: Baseline degradation discovered late in development cycle
- **Solution**: Golden task harness runs on every push/PR
- **Impact**: Catch issues immediately, maintain quality baseline

**3. Reproducibility**
- **Problem**: Hard to reproduce baseline results across machines/setups
- **Solution**: Virtualenv isolation + pinned dependencies + setup script
- **Impact**: Consistent results regardless of environment

**4. Graceful Degradation**
- **Problem**: Optional features (plots, TimeGPT) should not break core functionality
- **Solution**: Feature gating with clear status codes (`ok`, `skipped_no_api_key`, `error`)
- **Impact**: Reliable core experience, predictable failure modes

---

## User Journey: Zero to First Forecast

### Step-by-Step Walkthrough

**1. Initial Setup** (5 minutes)
```bash
# Clone repo
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla

# Open in Claude Code and trust folder
# (Marketplace auto-discovers from .claude-plugin/marketplace.json)
```

**2. Install Plugin** (30 seconds)
```
# In Claude Code chat
/plugin install nixtla-baseline-lab@nixtla-dev-marketplace
```

**3. Setup Environment** (2 minutes)
```
# In Claude Code chat
/nixtla-baseline-setup

# Or manually
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
```

**4. Run First Baseline** (30 seconds)
```
# In Claude Code chat
/nixtla-baseline-m4 horizon=7 series_limit=5

# Output: CSV + summary created in nixtla_baseline_m4_test/
```

**5. AI Interpretation** (10 seconds)
```
# Ask the Skill
Which baseline model performed best overall and why?

# AI reads CSV and summary, explains:
# "AutoETS performed best with avg sMAPE 0.77% vs SeasonalNaive 1.49%..."
```

**6. Optional: Custom Data** (add-on)
```
# Prepare your CSV with columns: unique_id, ds, y
/nixtla-baseline-m4 --dataset-type csv --csv-path /path/to/data.csv --horizon 5 --series-limit 10
```

**7. Optional: TimeGPT Comparison** (add-on)
```bash
# Set API key
export NIXTLA_TIMEGPT_API_KEY="your-key"

# Run with TimeGPT
/nixtla-baseline-m4 --include-timegpt --timegpt-max-series 3

# Review showdown report: timegpt_showdown_M4_Daily_h7.txt
```

**Total Time**: 5-10 minutes from clone to results (first run, including setup).

---

## Success Criteria (What "Done" Looks Like)

### Phase 8 Completion Criteria (v0.6.0) ✅

- ✅ **Baseline Models**: SeasonalNaive, AutoETS, AutoTheta run on M4 Daily
- ✅ **Custom CSV Support**: Accept user-provided time series with validation
- ✅ **Visualization**: Optional PNG plots with matplotlib
- ✅ **TimeGPT Integration**: Optional comparison with graceful degradation
- ✅ **AI Skill**: Interprets metrics and explains best model
- ✅ **Golden Task**: 5-step validation harness passes on every push
- ✅ **CI/CD**: GitHub Actions runs tests, uploads artifacts
- ✅ **Documentation**: README, AARs, test coverage, this product overview
- ✅ **Version**: 0.6.0 released with all features stable

### Quality Gates

**CI Must Pass**:
- Baseline MCP test produces valid CSV + summary
- Golden task harness validates schema, metrics ranges, summary content
- No TimeGPT failures (gracefully skips if no API key)
- Artifacts uploaded even on failures

**Manual Validation**:
- TimeGPT comparison works with valid API key
- Plots generate correctly when enabled
- Custom CSV support handles various formats
- Error messages are clear and actionable

---

## Future Directions (Post v0.6.0)

**Phase 9 Candidates** (Not Yet Planned):
- **Confidence Intervals**: Bootstrap or prediction intervals for forecasts
- **Larger Benchmarks**: Full M4 comparison (not just Daily subset)
- **Model Ensembling**: Combine baseline + TimeGPT forecasts
- **Automated Reporting**: Generate PDF/HTML reports
- **More Models**: MLForecast, NeuralForecast integration

**Longer-Term Vision**:
- Integration with broader "Bob for Nixtla" agentic system
- Specialist agents (Backtest QA, TimeGPT Runner, CI Triage, Doc Sync)
- Production TimeGPT infrastructure integration
- Multi-repo Nixtlaverse coordination

---

## Key Stakeholders

**Primary Decision Maker**: Max Mergenthaler (Nixtla CEO)
**Implementation Lead**: Jeremy Longshore (Intent Solutions)
**Technical Collaboration**: Nixtla Engineering Team
**Users**: Nixtla leadership, data science teams, technical collaborators

---

## Contact & Support

**Questions**: jeremy@intentsolutions.io or max@nixtla.io
**Issues**: GitHub Issues on `intent-solutions-io/plugins-nixtla`
**Documentation**: `plugins/nixtla-baseline-lab/README.md` (plugin manual)

---

**Product Overview Status**: ✅ **CURRENT** (v0.6.0)
**Last Updated**: 2025-11-25
**Next Review**: Post-Phase 9 (if/when planned)
