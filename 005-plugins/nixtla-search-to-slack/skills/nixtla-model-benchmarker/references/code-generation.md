# Code Generation Process

When generating a benchmark comparison, use the complete benchmark script template at:

**Template location**: `{baseDir}/assets/templates/benchmark_template.py`

## Template Structure

The template provides a complete `NixtlaBenchmark` class with methods:

```python
class NixtlaBenchmark:
    def load_data(filepath) -> train, test          # Split data 80/20
    def benchmark_timegpt(train, horizon, freq)     # TimeGPT forecasting
    def benchmark_statsforecast(train, h, freq)     # Statistical models
    def benchmark_mlforecast(train, h, freq)        # ML models
    def benchmark_neuralforecast(train, h, freq)    # Neural networks
    def calculate_metrics(y_true, y_pred, model)    # MAE, RMSE, MAPE, SMAPE
    def run_full_benchmark(data_path, h, freq)      # Run all benchmarks
    def plot_comparison(results_df, save_path)      # Visualize results
```

## Key Configuration Points

When generating the benchmark script, customize these parameters:

```python
# In main() function:
DATA_PATH = "data/timeseries.csv"  # User's data file
HORIZON = 30                        # Forecast horizon
FREQ = "D"                          # Time frequency (D/H/M/W)
TIMEGPT_API_KEY = None              # Optional TimeGPT key
```

## Model-Specific Tuning

**StatsForecast**: Adjust `season_length` based on data frequency
```python
models = [
    AutoARIMA(season_length=7),  # Weekly seasonality
    AutoETS(season_length=7),
    AutoTheta(season_length=7)
]
```

**MLForecast**: Configure lags based on temporal patterns
```python
mlf = MLForecast(
    models=[RandomForestRegressor(), lgb.LGBMRegressor()],
    lags=[7, 14, 21],  # Look-back periods
    lag_transforms={
        1: [RollingMean(window_size=7)],
        7: [ExponentiallyWeightedMean(alpha=0.3)]
    }
)
```

**NeuralForecast**: Set `input_size` and `max_steps` for training
```python
models = [
    NHITS(h=horizon, input_size=horizon * 2, max_steps=100),
    NBEATS(h=horizon, input_size=horizon * 2, max_steps=100)
]
```

## Workflow

1. **Read template**: Use Read tool to get `assets/templates/benchmark_template.py`
2. **Customize parameters**: Update DATA_PATH, HORIZON, FREQ based on user requirements
3. **Adjust models**: Modify season_length, lags, or neural network parameters if user specifies
4. **Write script**: Save customized benchmark to desired location
5. **Explain usage**: Provide instructions for running and interpreting results

## Output Files

The benchmark script generates:
- `benchmark_results.csv` - Metrics table sorted by RMSE
- `benchmark_comparison.png` - 4-panel visualization (MAE, RMSE, MAPE, execution time)

## Required Dependencies

```bash
pip install nixtla statsforecast mlforecast neuralforecast \
            scikit-learn lightgbm pandas matplotlib seaborn
```

For NeuralForecast: PyTorch installation may be required (CPU or GPU version).
