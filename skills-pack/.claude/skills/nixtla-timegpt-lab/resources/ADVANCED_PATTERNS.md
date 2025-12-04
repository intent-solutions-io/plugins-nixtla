# Advanced Nixtla Forecasting Patterns

This document contains advanced TimeGPT and Nixtla library patterns. Reference from main SKILL.md when users need advanced features.

## Hierarchical Forecasting

If user mentions aggregation levels (e.g., national → regional → store):

```python
from hierarchicalforecast.core import HierarchicalReconciliation
from hierarchicalforecast.methods import BottomUp, TopDown

# Generate hierarchical reconciliation code
# Reference: https://nixtla.github.io/hierarchicalforecast/
```

## Probabilistic Forecasting

For uncertainty quantification:

```python
# StatsForecast: parametric intervals
sf.forecast(df, h=30, level=[80, 90])

# TimeGPT: conformal prediction
client.forecast(df, h=30, level=[80, 90])  # More robust intervals
```

## Transfer Learning (TimeGPT Fine-Tuning)

If user has domain-specific patterns:

```python
# Fine-tune TimeGPT on user's historical data
timegpt_fcst = client.forecast(
    df=df,
    h=30,
    finetune_steps=50,  # Adapt foundation model
    finetune_loss='mae'
)
```
