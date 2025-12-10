# Polymarket Analyst Scripts

Standalone Python scripts for analyzing Polymarket prediction market contracts with TimeGPT forecasting.

## Scripts Overview

### fetch_contract.py
Fetches contract metadata and historical price data from Polymarket API.

**Usage**:
```bash
python fetch_contract.py <condition_id> --days 30 --output contract_data.json
```

**Arguments**:
- `condition_id` - Polymarket contract ID (required)
- `--days` - Days of historical data (default: 30)
- `--output` - Output JSON file path (default: auto-generated)

**Output**: JSON file with contract metadata, question, volume, liquidity, and price history.

### transform_data.py
Transforms Polymarket data to Nixtla time series format (unique_id, ds, y).

**Usage**:
```bash
python transform_data.py contract_data.json --output nixtla_data.csv
```

**Arguments**:
- `input_file` - Contract data JSON from fetch_contract.py (required)
- `--output` - Output CSV file path (default: auto-generated)

**Output**: CSV with columns: unique_id, ds (datetime), y (price).

### forecast_contract.py
Generates TimeGPT forecasts with confidence intervals and visualizations.

**Usage**:
```bash
python forecast_contract.py nixtla_data.csv \
  --horizon 48 \
  --freq H \
  --output forecast_results
```

**Arguments**:
- `data_file` - Nixtla-formatted CSV (required)
- `--horizon` - Forecast periods (default: 24)
- `--freq` - Frequency: H (hourly), D (daily) (default: H)
- `--output` - Output file prefix (default: forecast)

**Output**:
- `{prefix}_forecast.csv` - Forecast with confidence intervals
- `{prefix}_plot.png` - Visualization
- `{prefix}_metadata.json` - Analysis and metadata

**Requires**: `NIXTLA_TIMEGPT_API_KEY` environment variable

### analyze_polymarket.py
Complete end-to-end pipeline combining all steps.

**Usage**:
```bash
python analyze_polymarket.py <condition_id> \
  --horizon 48 \
  --days 30 \
  --output-dir ./results
```

**Arguments**:
- `contract_id` - Polymarket contract ID (required)
- `--horizon` - Forecast periods (default: 24)
- `--days` - Days of historical data (default: 30)
- `--output-dir` - Output directory (default: current directory)

**Output**:
- `polymarket_{id}_historical.csv` - Historical data
- `polymarket_{id}_forecast.csv` - Forecasts
- `polymarket_{id}_plot.png` - Visualization
- `polymarket_{id}_analysis.json` - Complete analysis

## Requirements

```bash
pip install nixtla pandas requests matplotlib
```

**Environment Variables**:
- `NIXTLA_TIMEGPT_API_KEY` - Get at https://dashboard.nixtla.io

## Python Version

Requires Python 3.8+

## Example Workflows

### Quick Analysis (Single Command)
```bash
export NIXTLA_TIMEGPT_API_KEY='your-key'
python analyze_polymarket.py 0x1234abcd --horizon 48 --days 60
```

### Step-by-Step (Granular Control)
```bash
# Step 1: Fetch
python fetch_contract.py 0x1234abcd --days 30

# Step 2: Transform
python transform_data.py contract_1234abcd_data.json

# Step 3: Forecast
python forecast_contract.py contract_1234abcd_nixtla.csv --horizon 48
```

## Error Handling

All scripts include:
- Comprehensive argparse CLI
- Proper docstrings
- Error handling with informative messages
- Input validation
- Type hints for maintainability

## Architecture

- **fetch_contract.py**: API client (Polymarket CLOB + Gamma APIs)
- **transform_data.py**: ETL pipeline (JSON to Nixtla format)
- **forecast_contract.py**: ML forecasting (TimeGPT client)
- **analyze_polymarket.py**: Orchestrator (imports all modules)

Each script is standalone and can be used independently or as imported modules.
