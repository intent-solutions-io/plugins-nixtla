# Nixtla TimeGPT Lab - Advanced Patterns

This document contains advanced forecasting patterns including hierarchical forecasting, probabilistic forecasting, and TimeGPT fine-tuning.

## Hierarchical Forecasting

When users have data at multiple aggregation levels (e.g., national → regional → store), use hierarchical reconciliation:

```python
from hierarchicalforecast.core import HierarchicalReconciliation
from hierarchicalforecast.methods import BottomUp, TopDown, MinTrace

# Example: Product hierarchy (total → category → SKU)
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoETS

# Define hierarchy structure
hierarchy = {
    'total': ['electronics', 'clothing'],
    'electronics': ['laptops', 'phones'],
    'clothing': ['shirts', 'pants']
}

# Create hierarchical structure matrix
S = [[1, 1, 1, 1],           # total = sum of all
     [1, 1, 0, 0],           # electronics = laptops + phones
     [0, 0, 1, 1],           # clothing = shirts + pants
     [1, 0, 0, 0],           # laptops
     [0, 1, 0, 0],           # phones
     [0, 0, 1, 0],           # shirts
     [0, 0, 0, 1]]           # pants

# Generate base forecasts
sf = StatsForecast(models=[AutoETS()], freq='D')
base_forecasts = sf.forecast(df=hierarchical_df, h=30)

# Reconcile using MinTrace (optimal reconciliation)
reconciler = HierarchicalReconciliation(
    reconcilers=[
        BottomUp(),         # Simple: aggregate from bottom
        TopDown(),          # Simple: disaggregate from top
        MinTrace()          # Optimal: minimize trace of covariance
    ]
)

reconciled_forecasts = reconciler.reconcile(
    Y_hat_df=base_forecasts,
    S=S,
    tags={'total': ['total'], 'category': ['electronics', 'clothing']}
)
```

**When to use**:
- Multi-level aggregations (geography, product categories)
- Need coherent forecasts across levels
- Want to leverage information from all levels

**Reference**: https://nixtla.github.io/hierarchicalforecast/

## Probabilistic Forecasting

### StatsForecast Prediction Intervals

Parametric intervals based on model assumptions:

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA

sf = StatsForecast(
    models=[AutoETS(), AutoARIMA()],
    freq='D'
)

# Generate forecasts with 80% and 95% prediction intervals
forecasts = sf.forecast(
    df=df,
    h=30,
    level=[80, 95]  # Confidence levels
)

# Output columns: ds, AutoETS, AutoETS-lo-80, AutoETS-hi-80, AutoETS-lo-95, AutoETS-hi-95
print(forecasts.head())
```

### TimeGPT Conformal Prediction

Non-parametric intervals using conformal prediction (more robust):

```python
from nixtla import NixtlaClient
import os

client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))

# Conformal prediction intervals
timegpt_forecast = client.forecast(
    df=df,
    h=30,
    level=[80, 90, 95],  # Multiple confidence levels
    model='timegpt-1-long-horizon'  # Or timegpt-1
)

# Output includes: TimeGPT, TimeGPT-lo-80, TimeGPT-hi-80, etc.
# Conformal intervals are calibrated and distribution-free
```

**Advantages of conformal prediction**:
- No distributional assumptions
- Valid under distribution shift
- Calibrated coverage guarantees
- Works for any black-box model

### Quantile Forecasts

For asymmetric uncertainty or risk management:

```python
# TimeGPT quantile forecasts
quantile_forecast = client.forecast(
    df=df,
    h=30,
    quantiles=[0.1, 0.25, 0.5, 0.75, 0.9]  # Specific quantiles
)

# Useful for:
# - Inventory planning (safety stock at 95th percentile)
# - Revenue forecasting (conservative 10th percentile)
# - Capacity planning (peak demand at 90th percentile)
```

## TimeGPT Fine-Tuning (Transfer Learning)

Adapt the foundation model to domain-specific patterns:

```python
from nixtla import NixtlaClient

client = NixtlaClient()

# Fine-tune on user's historical data
finetuned_forecast = client.forecast(
    df=df,
    h=30,
    finetune_steps=50,      # Number of fine-tuning iterations
    finetune_loss='mae',    # Or 'mse', 'mape'
    level=[80, 90]
)

# Fine-tuning parameters:
# - finetune_steps: More steps = better adaptation (but slower)
#   - 10-20: Light adaptation
#   - 30-50: Standard fine-tuning
#   - 100+: Heavy domain adaptation
# - finetune_loss: Optimize for your metric
#   - 'mae': Balanced, robust to outliers
#   - 'mse': Penalize large errors more
#   - 'mape': Scale-free, good for business metrics
```

**When to use fine-tuning**:
- Domain-specific patterns not in general pre-training
- Recent regime changes (COVID, policy shifts)
- Proprietary business processes
- Better accuracy worth the compute cost

**Cost-benefit analysis**:
```python
# Standard TimeGPT (fast, good baseline)
standard = client.forecast(df=df, h=30)

# Fine-tuned TimeGPT (slower, potentially better)
finetuned = client.forecast(df=df, h=30, finetune_steps=50)

# Compare accuracy on validation set
from utilsforecast.losses import mae
print(f"Standard MAE: {mae(y_true, standard['TimeGPT'])}")
print(f"Fine-tuned MAE: {mae(y_true, finetuned['TimeGPT'])}")
```

## Exogenous Variables (Future Regressors)

Incorporate known future information:

```python
# Historical data with exogenous variables
df_train = pd.DataFrame({
    'unique_id': ['store_1'] * 100,
    'ds': pd.date_range('2024-01-01', periods=100),
    'y': [100, 105, ...],           # Sales
    'price': [10.99, 9.99, ...],    # Price (known)
    'promotion': [0, 1, ...],       # Promotion flag (known)
    'temperature': [20, 22, ...]    # Weather (known for forecast)
})

# Future exogenous values (must be provided for forecast horizon)
df_future = pd.DataFrame({
    'unique_id': ['store_1'] * 30,
    'ds': pd.date_range('2024-04-11', periods=30),
    'price': [10.99] * 30,          # Planned future prices
    'promotion': [0, 0, 1, ...],    # Scheduled promotions
    'temperature': [25, 26, ...]    # Weather forecast
})

# StatsForecast with exogenous variables
from statsforecast.models import AutoARIMA
sf = StatsForecast(models=[AutoARIMA()], freq='D')
sf.fit(df_train)
forecasts = sf.predict(h=30, X_df=df_future)

# TimeGPT with exogenous variables
timegpt_forecast = client.forecast(
    df=df_train,
    X_df=df_future,  # Future exogenous values
    h=30
)
```

**Common exogenous variables**:
- **Calendar**: holidays, day of week, month (automatically handled by MLForecast)
- **Known future**: promotions, pricing, ad spend
- **Forecasted**: weather, economic indicators (use with caution)

## Anomaly Detection and Cleaning

Remove anomalies before forecasting:

```python
from statsforecast import StatsForecast
from statsforecast.models import MSTL

# Decompose series to detect anomalies
mstl = StatsForecast(models=[MSTL(season_length=[7, 365])], freq='D')
decomposition = mstl.forecast(df=df, h=1)

# Identify anomalies (residuals > 3 std dev)
residuals = df['y'] - decomposition['MSTL']
threshold = 3 * residuals.std()
anomalies = abs(residuals) > threshold

# Clean data
df_clean = df.copy()
df_clean.loc[anomalies, 'y'] = decomposition.loc[anomalies, 'MSTL']

# Forecast on cleaned data
sf = StatsForecast(models=[AutoETS()], freq='D')
forecasts = sf.forecast(df=df_clean, h=30)
```

## Ensemble Methods

Combine multiple models for robustness:

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA, AutoTheta

# Generate forecasts from multiple models
models = [AutoETS(), AutoARIMA(), AutoTheta()]
sf = StatsForecast(models=models, freq='D')
sf.fit(df)
forecasts = sf.predict(h=30)

# Simple average ensemble
forecasts['Ensemble'] = forecasts[[
    'AutoETS', 'AutoARIMA', 'AutoTheta'
]].mean(axis=1)

# Weighted ensemble (based on CV performance)
weights = {'AutoETS': 0.4, 'AutoARIMA': 0.3, 'AutoTheta': 0.3}
forecasts['WeightedEnsemble'] = (
    forecasts['AutoETS'] * weights['AutoETS'] +
    forecasts['AutoARIMA'] * weights['AutoARIMA'] +
    forecasts['AutoTheta'] * weights['AutoTheta']
)

# Median ensemble (robust to outliers)
forecasts['MedianEnsemble'] = forecasts[[
    'AutoETS', 'AutoARIMA', 'AutoTheta'
]].median(axis=1)
```

## Long-Horizon Forecasting

For forecasts beyond typical horizons:

```python
# Use TimeGPT long-horizon model
client = NixtlaClient()

long_forecast = client.forecast(
    df=df,
    h=365,  # 1 year ahead
    model='timegpt-1-long-horizon',  # Optimized for long horizons
    level=[80, 90]
)

# Alternative: Recursive StatsForecast with seasonal models
from statsforecast.models import MSTL, AutoTheta

sf = StatsForecast(
    models=[
        MSTL(season_length=[7, 365]),  # Multiple seasonalities
        AutoTheta(season_length=7, decomposition_type='multiplicative')
    ],
    freq='D'
)

long_forecasts = sf.forecast(df=df, h=365)
```

## Multi-Series at Scale

Forecast thousands of series efficiently:

```python
# Use parallel processing
sf = StatsForecast(
    models=[AutoETS(), AutoARIMA()],
    freq='D',
    n_jobs=-1  # Use all CPU cores
)

# For very large datasets, use batch processing
unique_ids = df['unique_id'].unique()
batch_size = 1000

all_forecasts = []
for i in range(0, len(unique_ids), batch_size):
    batch_ids = unique_ids[i:i+batch_size]
    df_batch = df[df['unique_id'].isin(batch_ids)]

    sf.fit(df_batch)
    forecasts_batch = sf.predict(h=30)
    all_forecasts.append(forecasts_batch)

forecasts = pd.concat(all_forecasts)
```

## Reference Links

- **HierarchicalForecast**: https://nixtla.github.io/hierarchicalforecast/
- **TimeGPT Fine-Tuning**: https://docs.nixtla.io/docs/tutorials-finetuning
- **Conformal Prediction**: https://docs.nixtla.io/docs/tutorials-prediction_intervals
- **StatsForecast Models**: https://nixtla.github.io/statsforecast/models.html
