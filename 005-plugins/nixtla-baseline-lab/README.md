# Nixtla Baseline Lab

Statistical forecasting benchmark plugin for Claude Code. Runs AutoETS, AutoTheta, and SeasonalNaive on M4 competition data. Returns sMAPE and MASE metrics.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
python tests/run_baseline_m4_smoke.py
```

**Expected output:** `GOLDEN TASK PASSED` (~30 seconds)

---

## What It Does

| Input | Output |
|-------|--------|
| M4 benchmark data (or your CSV) | sMAPE, MASE metrics per model |

**Models included:**
- AutoETS (exponential smoothing)
- AutoTheta (theta method)
- SeasonalNaive (baseline benchmark)

**No API keys required.** Uses Nixtla's open-source `statsforecast` library.

---

## Plugin Structure

```
nixtla-baseline-lab/
│
├── README.md                  # This file
├── QUICKSTART.md              # 4-line setup guide
│
├── agents/
│   └── nixtla-baseline-analyst.md    # AI agent for result interpretation
│
├── commands/
│   ├── nixtla-baseline-m4.md         # /nixtla-baseline-m4 slash command
│   └── nixtla-baseline-setup.md      # /nixtla-baseline-setup slash command
│
├── data/
│   └── m4/
│       ├── M4-Daily.csv              # 4,227 daily series
│       ├── M4-Hourly.csv             # 414 hourly series
│       ├── M4-Monthly.csv            # 48,000 monthly series
│       └── M4-Weekly.csv             # 359 weekly series
│
├── scripts/
│   ├── nixtla_baseline_mcp.py        # MCP server (4 tools)
│   ├── timegpt_client.py             # TimeGPT API wrapper (optional)
│   ├── requirements.txt              # Python dependencies
│   └── setup_nixtla_env.sh           # Environment setup script
│
├── skills/
│   └── nixtla-baseline-review/
│       ├── SKILL.md                  # Claude skill definition
│       └── resources/                # Reference documentation
│
└── tests/
    ├── run_baseline_m4_smoke.py      # Main smoke test
    ├── golden_tasks/                 # Production test definitions
    ├── csv_test/                     # Custom CSV testing
    ├── custom/                       # User test scenarios
    ├── m4_test/                      # Full M4 tests
    └── data/                         # Test fixtures
```

---

## MCP Server Tools

The `scripts/nixtla_baseline_mcp.py` exposes 4 tools to Claude Code:

| Tool | Purpose |
|------|---------|
| `run_baselines` | Execute forecasting models on data |
| `get_nixtla_compatibility_info` | Check installed library versions |
| `generate_benchmark_report` | Create markdown report from CSV |
| `generate_github_issue_draft` | Generate bug report template |

---

## Sample Results

Running on M4 Daily (5 series, 7-day horizon):

| Model | sMAPE | MASE |
|-------|-------|------|
| AutoETS | 0.77% | 0.422 |
| AutoTheta | 0.85% | 0.454 |
| SeasonalNaive | 1.49% | 0.898 |

**Interpretation:**
- sMAPE < 2% = excellent accuracy
- MASE < 1.0 = beats naive baseline

---

## Using Your Own Data

CSV format required:

```csv
unique_id,ds,y
store_001,2024-01-01,100
store_001,2024-01-02,105
store_001,2024-01-03,98
```

Run:
```bash
python scripts/nixtla_baseline_mcp.py --data your_file.csv --horizon 7
```

---

## Claude Code Integration

In Claude Code, use slash commands:

```
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

Or ask Claude to analyze results:
```
"Review these baseline forecasting results and tell me which model performed best"
```

---

## Dependencies

```
statsforecast>=1.5.0
datasetsforecast>=0.0.8
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
nixtla>=0.5.0  # Optional, for TimeGPT comparison
```

---

## Troubleshooting

**"Module not found"**
```bash
pip install -r scripts/requirements.txt
```

**"Data file not found"**
```bash
ls data/m4/  # Check M4 files exist
```

**Smoke test fails**
```bash
# Check Python version (3.10+ required)
python3 --version

# Reinstall deps
pip install --force-reinstall -r scripts/requirements.txt
```

---

## Files Generated

After running smoke test:

```
nixtla_baseline_m4_test/
├── results_M4_Daily_h7.csv    # Per-series metrics
└── summary_M4_Daily_h7.txt    # Averaged results
```

---

## Requirements

- Python 3.10+
- ~2GB RAM
- No API keys (statsforecast is open source)

---

## License

Internal PoC - Nixtla + Intent Solutions collaboration.
