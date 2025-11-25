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

## Installation

### From the Dev Marketplace

From the repository root:

```bash
# Start Claude Code
claude

# In Claude Code, add the local marketplace:
/plugin marketplace add ./

# Install the plugin:
/plugin install nixtla-baseline-lab@nixtla-dev-marketplace
```

## Automated Nixtla OSS Setup

After installing the plugin, use the automated setup command to prepare your Python environment:

```
/nixtla-baseline-setup
```

**What this does**:
1. Checks that Python 3 and pip are available
2. Offers choice: current environment or dedicated virtualenv
3. Installs Nixtla OSS dependencies from `scripts/requirements.txt`:
   - `statsforecast` (≥1.5.0) - Classical forecasting methods
   - `datasetsforecast` (≥0.0.8) - M4 benchmark datasets
   - `pandas` (≥2.0.0) and `numpy` (≥1.24.0) - Data processing
4. Verifies imports work correctly
5. Reports ready status

**Runtime**: 1-2 minutes (downloads ~200MB of packages)

**Recommended**: Use the virtualenv option for isolated testing

## Zero-to-First-Forecast

Get your first baseline forecast in < 5 minutes:

1. **Install the plugin** (see Installation above)

2. **Run automated setup** in Claude Code:
   ```
   /nixtla-baseline-setup
   ```

   Choose "dedicated virtualenv" when prompted (recommended).

3. **Run a small baseline experiment**:
   ```
   /nixtla-baseline-m4 horizon=7 series_limit=5
   ```

   This will:
   - Load 5 series from M4 Daily dataset (~95MB download on first run)
   - Run SeasonalNaive, AutoETS, AutoTheta models
   - Forecast 7 days ahead
   - Write results to `nixtla_baseline_m4/` directory

4. **Analyze the results** by asking Claude:
   ```
   Which baseline model performed best in that run?
   ```

   Claude will use the `NixtlaBaselineReview` skill to interpret metrics and provide analysis.

**Expected Runtime**:
- First run: ~60 seconds (includes M4 data download)
- Subsequent runs: ~30 seconds (uses cached data)

**Expected Output Files**:
- `nixtla_baseline_m4/results_M4_Daily_h7.csv` - Full metrics table (15 rows)
- `nixtla_baseline_m4/summary_M4_Daily_h7.txt` - Human-readable summary

## Proof It Works (Actual Results)

We validated the plugin with a real test run on November 25, 2025:

**Test Command**: `python3 scripts/nixtla_baseline_mcp.py test`

**Configuration**: 5 series from M4 Daily, horizon=7 days

**Results** (averages across 5 series):

| Model | Avg sMAPE | Avg MASE | Winner |
|-------|-----------|----------|--------|
| **AutoETS** | **0.77%** | **0.422** | ✅ |
| AutoTheta | 0.85% | 0.454 | |
| SeasonalNaive | 1.49% | 0.898 | |

**Key Findings**:
- **AutoETS won on both metrics**: Lowest sMAPE (0.77%) and lowest MASE (0.422)
- All models performed well: sMAPE < 1.5% is excellent for this benchmark
- MASE < 1.0 means AutoETS and AutoTheta beat the naive seasonal baseline
- Runtime: ~50 seconds (includes data loading and metric calculation)

**What these metrics mean**:
- **sMAPE (Symmetric Mean Absolute Percentage Error)**: 0.77% means predictions are typically within 0.77% of actual values. Lower is better. Range: 0-200%.
- **MASE (Mean Absolute Scaled Error)**: 0.422 means AutoETS is 58% better than a naive seasonal forecast. < 1.0 beats the baseline.

This demonstrates that the plugin works end-to-end and produces valid, competitive forecasting results on public benchmarks.

## Troubleshooting

### Environment Setup Issues

**Problem**: `/nixtla-baseline-setup` fails with "python3: command not found"

**Solution**: Install Python 3.8+
- Ubuntu/Debian: `sudo apt-get install python3 python3-pip`
- macOS: `brew install python3`
- Verify: `python3 --version`

---

**Problem**: `pip install` fails with "externally-managed-environment"

**Solution**: Use the virtualenv option
- Re-run: `/nixtla-baseline-setup` and choose "dedicated virtualenv"
- This creates an isolated environment at `plugins/nixtla-baseline-lab/.venv-nixtla-baseline/`

---

**Problem**: Corporate firewall blocks package downloads

**Solution**: Configure proxy or use trusted hosts
```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
# Or use trusted host flag:
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r scripts/requirements.txt
```

### Baseline Execution Issues

**Problem**: `/nixtla-baseline-m4` times out after 5 minutes

**Solution**: Increase MCP timeout in `.mcp.json`
```json
{
  "mcpServers": {
    "nixtla-baseline-mcp": {
      "timeout": 600000
    }
  }
}
```

---

**Problem**: First run is slow (> 2 minutes)

**Expected behavior**: M4 Daily dataset downloads automatically (~95MB)
- This only happens once
- Subsequent runs use cached data from `plugins/nixtla-baseline-lab/data/`
- Try smaller `series_limit` for faster testing: `horizon=7 series_limit=3`

---

**Problem**: Results show very high sMAPE (> 50%)

**Check**:
1. Is `horizon` reasonable for the data frequency? (Daily data: try horizon=7 or horizon=14)
2. Is `series_limit` too high, including difficult series? (Try `series_limit=5` first)
3. Check the summary file for per-model averages
4. Verify data was downloaded correctly: `ls -lh plugins/nixtla-baseline-lab/data/m4/datasets/`

---

**Problem**: "ModuleNotFoundError: No module named 'statsforecast'"

**Solution**: Re-run setup
```bash
cd plugins/nixtla-baseline-lab
source .venv-nixtla-baseline/bin/activate  # If using virtualenv
pip install -r scripts/requirements.txt
```

### Skill Issues

**Problem**: Skill doesn't activate when asking about results

**Check**:
1. Results files exist: `ls nixtla_baseline_m4/results_*.csv`
2. Ask explicitly: "Use the nixtla-baseline-review skill to analyze the last baseline run"
3. Check `.claude/skills/nixtla-baseline-review/SKILL.md` exists (project-level mirror)

---

**Problem**: Skill shows errors reading files

**Solution**: Verify file permissions
```bash
ls -la nixtla_baseline_m4/
# Files should be readable (rw-r--r--)
chmod 644 nixtla_baseline_m4/*.csv nixtla_baseline_m4/*.txt
```

### Getting Help

If issues persist:
1. Check logs in the MCP server output
2. Run standalone test: `python3 scripts/nixtla_baseline_mcp.py test`
3. Review Phase 5 AAR: `000-docs/019-AA-AACR-phase-05-setup-and-validation.md`
4. Contact: jeremy@intentsolutions.io

## Status

**Current Phase**: Phase 5 - Automated setup and local validation ✅

**Capabilities**:
- ✅ Automated Nixtla OSS setup with `/nixtla-baseline-setup` command
- ✅ Run baseline forecasts on M4 Daily benchmark
- ✅ Calculate sMAPE and MASE metrics
- ✅ AI-powered result interpretation via Skills
- ✅ Strategic analysis via analyst agent
- ✅ Local dev marketplace for easy installation
- ✅ Validated on real machine with actual results captured

**Validation Status**:
- ✅ Setup script runs cleanly on Ubuntu with Python 3.12
- ✅ MCP server executes baseline models successfully
- ✅ Results match expected schema and metric ranges
- ✅ Golden task validated against actual behavior
- ✅ Ready for Max (Nixtla CEO) demo

## License

MIT License - see repository root LICENSE file.

## Contact

- **Technical Lead**: Jeremy Longshore (jeremy@intentsolutions.io)
- **Nixtla Collaboration**: Max Mergenthaler (max@nixtla.io)
- **Repository**: https://github.com/jeremylongshore/claude-code-plugins-nixtla

---

**Version**: 0.3.0 (Phase 5)
**Last Updated**: 2025-11-25
