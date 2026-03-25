# Uncertainty Quantifier Examples

## Example 1: Sales Forecast with 90% Confidence

**Input (forecast.csv)**:
```csv
unique_id,ds,y,StatsForecast
store_1,2024-01-01,100,95
store_1,2024-01-02,120,115
store_1,2024-01-03,110,112
```

**Command**:
```bash
python {baseDir}/scripts/quantify_uncertainty.py \
  --input forecast.csv \
  --confidence 0.90 \
  --method quantile
```

**Output (forecast_with_uncertainty.csv)**:
```csv
unique_id,ds,y,StatsForecast,lower_bound_90,upper_bound_90
store_1,2024-01-01,100,95.0,85.0,105.0
store_1,2024-01-02,120,115.0,105.0,125.0
store_1,2024-01-03,110,112.0,102.0,122.0
```

## Example 2: Energy Demand Forecast with 95% Confidence

**Input (data.csv)**: Hourly energy grid data spanning January 2024 with columns unique_id, ds, y.

**Commands**:
```bash
# Step 1: Generate forecasts from historical data
python {baseDir}/scripts/generate_forecasts.py \
  --input data.csv \
  --output forecast.csv

# Step 2: Quantify uncertainty using jackknife+ method
python {baseDir}/scripts/quantify_uncertainty.py \
  --input forecast.csv \
  --confidence 0.95 \
  --method jackknife+
```

**Output**: Forecast with 95% prediction intervals suitable for risk-aware energy planning and capacity reserve allocation.

## Example 3: Complete End-to-End Workflow

Demonstrate the full pipeline from raw historical data to uncertainty-quantified forecasts.

```bash
# Generate point forecasts from historical sales data
python {baseDir}/scripts/generate_forecasts.py \
  --input sales_history.csv \
  --output sales_forecast.csv

# Quantify uncertainty with 90% confidence using quantile method
python {baseDir}/scripts/quantify_uncertainty.py \
  --input sales_forecast.csv \
  --confidence 0.90 \
  --method quantile \
  --forecast_col StatsForecast

# Review generated outputs:
# - forecast_with_uncertainty.csv (data with prediction intervals)
# - uncertainty_plot.png (visualization with confidence bands)
# - calibration_metrics.json (coverage and interval width metrics)
```
