## Examples

### Example 1: StatsForecast M4 Daily Demo

```bash
python {baseDir}/scripts/generate_demo_notebook.py \
    --library statsforecast \
    --dataset m4-daily \
    --models AutoETS,AutoARIMA,SeasonalNaive \
    --horizon 14 \
    --output demo_statsforecast_m4_daily.ipynb
```

**Generated notebook includes**:
```python
# Import libraries
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA, SeasonalNaive
import pandas as pd
import matplotlib.pyplot as plt

# Load M4 Daily data
df = pd.read_csv('m4_daily_sample.csv')
print(f"Loaded {len(df)} rows, {df['unique_id'].nunique()} series")

# Configure models
sf = StatsForecast(
    models=[AutoETS(), AutoARIMA(), SeasonalNaive(season_length=7)],
    freq='D',
    n_jobs=-1
)

# Generate forecasts
forecasts = sf.forecast(df=df, h=14)

# Evaluate
from statsforecast.utils import calculate_metrics
metrics = calculate_metrics(df, forecasts, metrics=['smape', 'mase'])
print(metrics)

# Visualize
sf.plot(df, forecasts)
plt.show()
```

### Example 2: MLForecast with Exogenous Features

```bash
python {baseDir}/scripts/generate_demo_notebook.py \
    --library mlforecast \
    --dataset retail-sales \
    --models LightGBM,XGBoost \
    --features lag,rolling_mean,date_features \
    --output demo_mlforecast_retail.ipynb
```

**Generated notebook features**:
- Lag features (1, 7, 14 days)
- Rolling statistics (mean, std, min, max)
- Date features (day of week, month, is_weekend)
- LightGBM and XGBoost model comparison
- Feature importance plots

### Example 3: TimeGPT API Demo

```bash
python {baseDir}/scripts/generate_demo_notebook.py \
    --library timegpt \
    --dataset custom \
    --api-key $NIXTLA_API_KEY \
    --horizon 30 \
    --confidence-levels 80,90,95 \
    --output demo_timegpt_api.ipynb
```

**Generated notebook demonstrates**:
- TimeGPT API client initialization
- Data upload and validation
- Forecast generation with confidence intervals
- Probabilistic forecasting
- Anomaly detection integration

### Example 4: Batch Generate All Three Libraries

```bash
for library in statsforecast mlforecast timegpt; do
    python {baseDir}/scripts/generate_demo_notebook.py \
        --library $library \
        --dataset m4-hourly \
        --output "demo_${library}_m4_hourly.ipynb"
done
```

### Example 5: Custom Template with Branding

```bash
python {baseDir}/scripts/generate_demo_notebook.py \
    --library statsforecast \
    --dataset m4-weekly \
    --template {baseDir}/assets/templates/custom_branded_template.ipynb \
    --logo company_logo.png \
    --output demo_branded.ipynb
```
