# Baseline Lab - User Journey

**Plugin:** nixtla-baseline-lab
**Last Updated:** 2025-11-30

---

## Persona

**Name:** "Engineer Emma"
**Role:** Machine Learning Engineer at Nixtla
**Company Type:** Time series forecasting platform
**Technical Level:** Advanced (Python, forecasting, data science)
**Goal:** Quickly validate statsforecast baseline performance on M4 data to debug a customer issue

---

## Prerequisites

Before using this plugin, ensure:

- [x] Claude Code is installed and running
- [x] Python 3.10+ is available on your system
- [x] Git repository is cloned locally
- [x] (Optional) Nixtla API key for TimeGPT comparison

---

## Journey Overview

```
Setup → Run Baseline → Review Results → Share Findings → Success!
```

---

## Step-by-Step Journey

### Step 1: Initial Setup

**User wants to:** Set up the Nixtla Baseline Lab plugin for the first time

**User does:**
```bash
# Clone the repository
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla/plugins/nixtla-baseline-lab

# Run automated setup
./scripts/setup_nixtla_env.sh --venv
```

**System responds:**
```
🔧 Nixtla Baseline Lab - Environment Setup

Checking Python...
✅ Python 3.12.3 detected

Creating virtual environment...
✅ Virtual environment created at .venv-nixtla-baseline/

Installing dependencies...
✅ statsforecast 1.7.10 installed
✅ datasetsforecast 0.0.8 installed
✅ nixtla 0.6.2 installed (optional TimeGPT)

Setup complete! 🎉

Next steps:
1. Activate: source .venv-nixtla-baseline/bin/activate
2. Try it: /nixtla-baseline-m4 demo_preset=m4_daily_small
```

**User sees:**
Environment is ready, dependencies installed, clear next steps

**Next:** Activate the virtual environment and try the plugin

---

### Step 2: Run First Baseline Benchmark

**User wants to:** Run a quick baseline benchmark to see how the plugin works

**User does:**
```bash
# Activate virtual environment
source .venv-nixtla-baseline/bin/activate

# Start Claude Code
claude
```

Then in Claude Code:
```
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**System responds:**
```
Running Nixtla Baseline Lab benchmark...

📊 Dataset: M4 Daily (Small subset)
   - Series count: 4,227
   - Forecast horizon: 14 days

🔄 Running baseline models:
   ✅ SeasonalNaive completed (12s)
   ✅ AutoETS completed (45s)
   ✅ AutoTheta completed (28s)

📈 Metrics calculated:
   - sMAPE (Symmetric Mean Absolute Percentage Error)
   - MASE (Mean Absolute Scaled Error)

✅ Results saved:
   - Metrics CSV: nixtla_baseline_m4_20251130_143022.csv
   - Reproducibility bundle: repro_bundle_20251130_143022.txt

Total runtime: 90 seconds
```

**User sees:**
- Progress indicators for each model
- Clear metrics output
- File locations for results
- Total execution time

**Next:** Review the results and metrics

---

### Step 3: Review Results

**User wants to:** Understand the benchmark metrics and model performance

**User does:**
Open the generated CSV or ask Claude to interpret:
```
Can you explain these baseline results?
```

**System responds (via Nixtla Baseline Review skill):**
```
📊 M4 Daily Baseline Analysis

Model Performance Rankings (by sMAPE):
1. AutoETS: 12.3% (best)
2. AutoTheta: 13.1%
3. SeasonalNaive: 15.7%

Key Insights:
✅ AutoETS performs best - recommends using for production baselines
⚠️ SeasonalNaive shows 27% higher error - expected for this dataset
📈 All models within reasonable M4 Daily benchmarks

Reproducibility:
- statsforecast version: 1.7.10
- Dataset: M4 Daily (4,227 series)
- Config saved in: repro_bundle_20251130_143022.txt
```

**User sees:**
Human-readable interpretation, actionable insights, reproducibility info

**Next:** Use findings to debug customer issue or create GitHub issue

---

### Step 4: Create GitHub Issue (Optional)

**User wants to:** Report a potential bug with full reproducibility context

**User does:**
```
Can you create a GitHub issue draft for this benchmark?
```

**System responds:**
```markdown
# Baseline Benchmark Results - M4 Daily

## Summary
Ran baseline benchmarks on M4 Daily dataset with the following results:

## Metrics
| Model | sMAPE | MASE |
|-------|-------|------|
| AutoETS | 12.3% | 0.85 |
| AutoTheta | 13.1% | 0.92 |
| SeasonalNaive | 15.7% | 1.14 |

## Reproducibility
- **statsforecast**: 1.7.10
- **datasetsforecast**: 0.0.8
- **Dataset**: M4 Daily (4,227 series)
- **Forecast horizon**: 14 days
- **Date**: 2025-11-30

## Configuration
See attached: repro_bundle_20251130_143022.txt

## Expected Behavior
[User fills in expected behavior]

## Actual Behavior
[User fills in observed behavior]
```

**User sees:**
GitHub-ready issue template with complete context

**Success!** User has validated baseline performance, gathered reproducibility info, and can now share findings with the team or create detailed bug reports.

---

## Complete Example

### Scenario
Emma needs to validate that a customer's reported statsforecast issue is reproducible on standard M4 data before escalating to the research team.

### Full Walkthrough

```bash
# Terminal setup
cd ~/nixtla-plugin-showcase/plugins/nixtla-baseline-lab
source .venv-nixtla-baseline/bin/activate
claude

# In Claude Code session:
```

**Emma:** I need to run baseline benchmarks on M4 Daily to validate a customer issue.

**Claude:** I'll help you run the Nixtla Baseline Lab benchmark. Let me use the plugin.

*Claude invokes /nixtla-baseline-m4 demo_preset=m4_daily_small*

**Output:**
```
Running Nixtla Baseline Lab benchmark...
📊 Dataset: M4 Daily (Small - 4,227 series)
✅ SeasonalNaive: sMAPE 15.7%, MASE 1.14
✅ AutoETS: sMAPE 12.3%, MASE 0.85
✅ AutoTheta: sMAPE 13.1%, MASE 0.92

Results saved:
- nixtla_baseline_m4_20251130_143022.csv
- repro_bundle_20251130_143022.txt

Total runtime: 90 seconds
```

**Emma:** Can you interpret these results and tell me if AutoETS performance is normal?

**Claude (via Nixtla Baseline Review skill):**
```
✅ AutoETS performance (sMAPE 12.3%) is within expected range for M4 Daily.
   Baseline benchmarks typically show 11-14% sMAPE on this dataset.

✅ Model ranking is standard (AutoETS > AutoTheta > SeasonalNaive).

✅ Your results are reproducible - repro bundle contains:
   - statsforecast 1.7.10
   - M4 Daily (4,227 series)
   - Configuration snapshot

Recommendation: These baseline results look normal. If customer is seeing
significantly different metrics, check their library versions and dataset.
```

**Emma:** Perfect! This confirms the customer issue is likely version-specific. I'll create a GitHub issue with this repro bundle.

**Result:** Emma validated baseline performance in 90 seconds, got expert interpretation, and now has full reproducibility context for the GitHub issue.

---

## Error Scenarios

| Scenario | What User Sees | What Went Wrong | How to Fix |
|----------|---------------|-----------------|------------|
| Missing dependencies | `ModuleNotFoundError: No module named 'statsforecast'` | Python environment not set up | Run `./scripts/setup_nixtla_env.sh --venv` |
| Wrong Python version | `Error: Python 3.10+ required` | Python too old | Install Python 3.10+ or use pyenv |
| TimeGPT API key missing | `Warning: TimeGPT comparison skipped (no API key)` | `NIXTLA_TIMEGPT_API_KEY` not set | Set API key in `.env` file (opt-in feature) |
| Out of memory | `MemoryError` during model execution | Dataset too large for available RAM | Use smaller preset: `demo_preset=m4_daily_small` |
| Invalid preset | `Error: Unknown preset 'typo'` | Typo in demo_preset parameter | Valid: m4_daily_small, m4_weekly_full, etc. |

---

## Tips & Best Practices

1. **Start Small:** Use `demo_preset=m4_daily_small` for first runs (faster, lower memory)
2. **Virtual Environment:** Always use the dedicated venv to avoid version conflicts
3. **Save Repro Bundles:** Keep reproducibility bundles for all benchmarks (valuable for debugging)
4. **TimeGPT is Optional:** Baseline mode is zero-cost and fully offline
5. **Check Runtime:** M4 Daily Small ~90s, M4 Daily Full ~10 min

---

## FAQ

**Q: Can I use custom datasets?**
A: Not yet. v0.8.0 only supports M4 benchmark datasets. Custom data support planned for future releases.

**Q: Does this cost money?**
A: No. Baseline mode (statsforecast only) is free and offline. TimeGPT comparison is opt-in and requires Nixtla API credits.

**Q: Can I run this in CI/CD?**
A: Yes, but it's designed for interactive use. See GitHub Actions integration docs for automated benchmarking.

**Q: How do I update the plugin?**
A: `cd plugins/nixtla-baseline-lab && git pull && pip install -U -r scripts/requirements.txt`

**Q: Where are results saved?**
A: Current working directory. Files are named with timestamps for uniqueness.

**Q: Can I use this on Windows?**
A: Setup script is Bash. For Windows, manually create venv and install from requirements.txt.
