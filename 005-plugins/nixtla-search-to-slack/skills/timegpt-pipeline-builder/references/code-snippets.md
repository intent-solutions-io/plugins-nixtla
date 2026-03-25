# Code Snippets and Template Reference

## Template Reference

Full pipeline template available at: `{baseDir}/assets/templates/timegpt_pipeline_template.py`

The template includes:
- Complete `TimeGPTForecaster` class with data validation, forecasting, visualization
- Advanced features: multi-series forecasting, external regressors, cross-validation
- Production-ready error handling, logging, and configuration management
- Main execution function with summary statistics

## Basic Usage

```python
# Initialize forecaster
forecaster = TimeGPTForecaster()

# Run complete pipeline
forecast = forecaster.run_pipeline(
    data_path="data/timeseries.csv",
    horizon=30,
    freq="D",
    plot=True,
    output_path="output/forecast.csv"
)
```

## Multi-Series Forecasting

```python
# Data must have 'unique_id', 'ds', 'y' columns
forecast = forecaster.forecast_multiple_series(
    df=multi_series_df,
    horizon=14,
    freq="D"
)
```

## With External Regressors

```python
# Provide future regressor values
forecast = forecaster.forecast_with_regressors(
    df=historical_df,
    horizon=7,
    X_future=future_regressors_df,
    freq="D"
)
```

## Cross-Validation

```python
# Backtesting with time-series cross-validation
metrics = forecaster.cross_validate(
    df=data,
    horizon=14,
    n_windows=5
)
```

## Code Generation Workflow

1. **Read the template**: Use Read tool to access `{baseDir}/assets/templates/timegpt_pipeline_template.py`
2. **Customize for user**: Adapt template based on gathered requirements
3. **Generate supporting files**:
   - `requirements.txt` with dependencies
   - `README.md` with setup instructions
   - `.env.example` for API keys
   - Example data format (CSV structure)

## Template Customization Guide

When customizing the template:
- Update `DATA_PATH`, `HORIZON`, `FREQ` in `main()` function
- Adjust frequency in `load_data()` date range check
- Modify confidence interval levels in `forecast()` method
- Add custom validation rules in `load_data()` if needed
- Include additional methods for advanced features (multi-series, regressors, CV)
