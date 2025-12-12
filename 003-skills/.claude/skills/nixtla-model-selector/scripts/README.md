# Nixtla Model Selector Scripts

Automated forecasting model selection and execution scripts.

## model_selector.py

Comprehensive script that handles the complete model selection workflow:

1. **load_and_analyze_data()** - Loads CSV, validates schema, infers frequency
2. **select_model()** - Analyzes data characteristics and selects optimal model
3. **execute_forecast()** - Runs StatsForecast or TimeGPT
4. **generate_output()** - Saves forecasts and selection report

### Usage

```bash
# Basic usage
python model_selector.py --input data.csv

# Custom output and horizon
python model_selector.py --input data.csv --output results.csv --horizon 30

# With visualization
python model_selector.py --input data.csv --visualize

# Full options
python model_selector.py --input data.csv \
    --output forecast.csv \
    --selection-output model_selection.txt \
    --horizon 14 \
    --visualize
```

### Arguments

- `--input`: Path to input CSV (required)
- `--output`: Path to output forecast CSV (default: forecast.csv)
- `--selection-output`: Path to model selection report (default: model_selection.txt)
- `--horizon`: Forecast horizon in periods (default: 14)
- `--visualize`: Generate time series plot

### Requirements

```bash
pip install statsforecast nixtla pandas matplotlib statsmodels
```

### Environment Variables

- `NIXTLA_TIMEGPT_API_KEY`: Required if TimeGPT is selected

### Exit Codes

- `0`: Success
- `1`: File not found
- `2`: Invalid data format
- `3`: Unexpected error

## Input Data Format

CSV file with required columns:
- `unique_id`: Series identifier
- `ds`: Timestamp (datetime parseable)
- `y`: Observation values (numeric)

Example:
```csv
unique_id,ds,y
product_1,2023-01-01,100
product_1,2023-01-02,102
product_1,2023-01-03,105
```

## Output Files

### forecast.csv
Predictions in long format with columns:
- `unique_id`: Series identifier
- `ds`: Forecast timestamp
- `model`: Model name (AutoETS, AutoARIMA, or TimeGPT)
- `yhat`: Predicted value

### model_selection.txt
Selection report containing:
- Selected model name
- Selection reason with data characteristics
- Number of forecast records generated

### time_series_plot.png (optional)
Visualization of input time series data when `--visualize` flag is used.
