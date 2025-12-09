# TimeGPT Lab Environment Setup

**Purpose**: Configure local development environment for TimeGPT API experimentation and workflow development.

**Last Updated**: 2025-12-08

## Prerequisites

- **Python**: 3.9+ (recommended: 3.10 or 3.11)
- **Git**: For cloning and version control
- **API Access**: Valid Nixtla TimeGPT API key (obtain from [Nixtla dashboard](https://dashboard.nixtla.io/))

## Installation Steps

### 1. Python Environment

We recommend using a virtual environment to isolate TimeGPT lab dependencies:

```bash
# From repository root
cd 002-workspaces/timegpt-lab

# Create virtual environment
python3 -m venv .venv-timegpt

# Activate (Linux/Mac)
source .venv-timegpt/bin/activate

# Activate (Windows)
.venv-timegpt\Scripts\activate
```

### 2. Install TimeGPT Dependencies

TimeGPT lab requires the Nixtla SDK and supporting libraries:

```bash
# Install core TimeGPT dependencies
pip install nixtla>=0.5.0 utilsforecast pandas>=1.5.0

# Optional: Install additional forecasting libraries for comparison
pip install statsforecast mlforecast
```

**Note**: If the repository root has a `pyproject.toml` or `requirements.txt` that already includes these dependencies, you can install from there instead:

```bash
# From repository root
pip install -e .
```

### 3. Set Environment Variables

TimeGPT requires an API key. **Never commit this key to git**.

#### Option A: Local Shell Export (Session-Only)

```bash
export NIXTLA_TIMEGPT_API_KEY="your_api_key_here"
export NIXTLA_ENV="dev"  # Optional: dev, demo, prod
```

Add to your `~/.bashrc` or `~/.zshrc` for persistence across sessions.

#### Option B: Local .env File (Recommended for Development)

1. Copy the example file:

```bash
cp .env.example .env
```

2. Edit `.env` with your actual API key:

```dotenv
NIXTLA_TIMEGPT_API_KEY=your_actual_api_key_here
NIXTLA_ENV=dev
```

3. Load the `.env` file before running scripts:

```bash
# Using python-dotenv
pip install python-dotenv

# In your scripts:
from dotenv import load_dotenv
load_dotenv()
```

**Important**: `.env` is gitignored and will NOT be committed.

### 4. Verify Installation

Run the environment validation script:

```bash
python scripts/validate_env.py
```

Expected output on success:

```
✓ Python 3.10.x (supported)
✓ NIXTLA_TIMEGPT_API_KEY environment variable present
✓ nixtla package installed (version 0.5.x)
✓ utilsforecast package installed
✓ pandas package installed

Environment validation: PASSED
```

If validation fails, review error messages and ensure all steps above were completed.

## Common Issues

### ImportError: No module named 'nixtla'

**Solution**: Install dependencies:

```bash
pip install nixtla utilsforecast pandas
```

### Environment variable NIXTLA_TIMEGPT_API_KEY not set

**Solution**: Set the environment variable using one of the methods above. Verify with:

```bash
echo $NIXTLA_TIMEGPT_API_KEY  # Should print your key (or first few chars)
```

### Python version < 3.9

**Solution**: Upgrade Python. TimeGPT requires Python 3.9+.

```bash
python --version  # Check current version
```

## Running the Smoke Test

Once your environment is validated, test your TimeGPT setup with the smoke test script:

```bash
# From the lab root (002-workspaces/timegpt-lab)
python scripts/timegpt_smoke_test.py
```

### What to Expect

**On Success**:

```
✓ TimeGPT Smoke Test: PASSED

Summary:
  Input series: 2
  Forecast horizon: 14 days
  Output: reports/timegpt_smoke_forecast.csv
```

The script will:
- Load the sample dataset (`data/timegpt_smoke_sample.csv`)
- Make ONE TimeGPT API forecast call (14-day horizon)
- Save forecast results to `reports/timegpt_smoke_forecast.csv`

**On Authentication Error**:

```
ERROR: TimeGPT API Call Failed
This appears to be an authentication error.
Please verify your API key is valid
```

**Fix**: Double-check your `NIXTLA_TIMEGPT_API_KEY` value at https://dashboard.nixtla.io/

**On Missing Dataset**:

```
ERROR: Dataset Not Found
Expected dataset at: data/timegpt_smoke_sample.csv
```

**Fix**: Ensure you're running from the correct directory and the dataset file exists.

### Cost & Limits

The smoke test is designed to be minimal and safe:
- **Dataset size**: 2 time series, 90 timestamps each (~180 rows)
- **API calls**: Exactly ONE forecast call
- **Horizon**: 14 days (small forecast window)
- **Frequency**: Daily (standard, no advanced features)

**Important**: Run this test manually, not in a tight loop. It makes a real API call that may incur costs based on your TimeGPT plan.

## Running TimeGPT Experiments

After validating your environment and smoke test, you can run config-driven experiments using the experiment harness.

### Experiment Harness Overview

The experiment harness (`scripts/run_experiment.py`) runs multiple TimeGPT forecasting experiments defined in `experiments/timegpt_experiments.json`. Each experiment:
- Uses the same sample dataset (`data/timegpt_smoke_sample.csv`)
- Makes ONE TimeGPT API call
- Computes metrics (MAE, SMAPE) against a holdout period
- Tracks runtime and generates reports

### Running Experiments

```bash
# From the lab root (002-workspaces/timegpt-lab)
python scripts/run_experiment.py
```

### What to Expect

**On Success**:

```
✓ Experiment Harness: COMPLETE

Summary:
  Experiments run: 2
  Series processed: 2
  Total results: 4

Reports:
  - reports/timegpt_experiments_results.csv
  - reports/timegpt_experiments_summary.md
```

The script will:
- Load experiment configs from `experiments/timegpt_experiments.json`
- Run each enabled experiment sequentially
- Generate detailed CSV metrics (per-series, per-experiment)
- Generate human-readable Markdown summary with insights

### Understanding Experiment Config

The config file `experiments/timegpt_experiments.json` defines experiments:

```json
{
  "experiments": [
    {
      "name": "timegpt_baseline_14d",
      "description": "14-day forecast...",
      "enabled": true,
      "horizon": 14,
      "eval_window": 14,
      "frequency": "D"
    }
  ]
}
```

**Key fields**:
- `name`: Unique experiment identifier
- `enabled`: Set to `false` to disable without deleting
- `horizon`: Number of steps to forecast
- `eval_window`: Number of final points used as holdout for metrics
- `frequency`: Time frequency (`"D"` = daily, `"M"` = monthly, etc.)

### Adding/Modifying Experiments

1. **Add a new experiment**: Copy an existing experiment block, change `name` and parameters
2. **Disable an experiment**: Set `"enabled": false`
3. **Change horizon**: Adjust `horizon` and `eval_window` values
4. **Re-run**: Execute `python scripts/run_experiment.py` to apply changes

### Cost & Limits (Experiments)

The experiment harness is designed for controlled cost:
- **Dataset size**: Reuses tiny sample (2 series, 90 days, 180 rows)
- **API calls per run**: ONE call per enabled experiment
- **Default config**: 2 enabled experiments = 2 API calls total
- **Horizons**: Small (7-28 days by default)

**Important**: Each enabled experiment makes ONE real API call. Disable experiments you don't need to reduce costs.

### Interpreting Results

**CSV Report** (`reports/timegpt_experiments_results.csv`):
- One row per (experiment, series) combination
- Columns: `experiment_name`, `unique_id`, `horizon`, `eval_window`, `mae`, `smape`, `runtime_seconds`
- Use for detailed analysis or further processing

**Markdown Summary** (`reports/timegpt_experiments_summary.md`):
- Human-readable summary of all experiments
- Per-experiment metrics tables
- Comparative analysis across experiments
- Insights (e.g., which experiment has lowest error)

**Metrics**:
- **MAE (Mean Absolute Error)**: Average absolute difference between forecast and actual values (lower is better)
- **SMAPE (Symmetric MAPE)**: Percentage error metric (0-200 scale, lower is better)

### Example Workflow

1. **Baseline run**: Run default config (14d + 28d experiments)
2. **Review results**: Check `reports/timegpt_experiments_summary.md`
3. **Iterate**: Add new experiment with different horizon, re-run
4. **Compare**: Review comparative analysis to see which horizon performs best
5. **Optimize**: Disable poorly-performing experiments, focus on promising configs

## Next Steps

Once your environment is validated and experiments are running:

1. **Review experiment results**: Examine `reports/timegpt_experiments_summary.md` for insights
2. **Iterate on configs**: Add/modify experiments in `experiments/timegpt_experiments.json`
3. **Compare TimeGPT vs baselines**: Design experiments comparing TimeGPT with StatsForecast models
4. **Create custom datasets**: Add your own time series data to `data/`

## Security Reminders

- **Never commit** `.env` or any file containing `NIXTLA_TIMEGPT_API_KEY`
- **Never share** API keys in logs, screenshots, or documentation
- **Rotate keys** if accidentally exposed
- **Use read-only keys** for experimentation when available

## References

- Nixtla TimeGPT Documentation: https://docs.nixtla.io/
- Nixtla SDK (nixtla package): https://github.com/Nixtla/nixtla
- Repository standards: `{baseDir}/002-workspaces/.directory-standards.md`

---

**Maintained by**: TimeGPT Lab Team
**Contact**: jeremy@intentsolutions.io
