# ERCOT Grid Forecasting Prototype

48-hour electricity load forecasting for the Texas (ERCOT) grid using Nixtla's statsforecast and TimeGPT.

**Part of**: [121-AA-REPT Energy Grid Forecasting Opportunity Research](../../000-docs/121-AA-REPT-energy-grid-forecasting-opportunity-research.md)

## Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run (statsforecast only - no API key needed)
python ercot_grid_forecast.py

# Run with TimeGPT (optional)
export NIXTLA_TIMEGPT_API_KEY='your-key'
python ercot_grid_forecast.py
```

## What It Does

1. **Loads** clean ERCOT data from Nixtla's S3 bucket
2. **Splits** into train/test (last 48h holdout)
3. **Runs** statsforecast models:
   - SeasonalNaive (baseline)
   - MSTL (multi-seasonal decomposition)
   - AutoETS (exponential smoothing)
4. **Runs** TimeGPT (if API key set)
5. **Evaluates** MAE, RMSE, MAPE
6. **Plots** forecasts vs actuals

## Outputs

- `sf_forecasts.csv` - Statsforecast predictions
- `evaluation_results.csv` - Model metrics
- `forecast_plot.png` - Visualization

## Data Source

Uses Nixtla's pre-cleaned ERCOT dataset:
```
https://datasets-nixtla.s3.amazonaws.com/ERCOT-clean.csv
```

Original source: [ERCOT Grid Information](http://www.ercot.com/gridinfo/load/load_hist)

## Next Steps

- [ ] Add geo-visualization overlay (transmission map)
- [ ] Multi-region comparison (ERCOT zones)
- [ ] Real-time data ingestion
- [ ] Congestion prediction layer
