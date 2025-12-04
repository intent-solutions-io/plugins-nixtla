# TimeGPT Fine-Tuning Advanced Features

## Advanced Fine-Tuning Parameters

### finetune_steps

Controls the number of training iterations:
```yaml
parameters:
  finetune_steps: 100  # Default
  # Increase for:
  # - Complex patterns
  # - Large datasets
  # - Better accuracy (may overfit)
  #
  # Decrease for:
  # - Simple patterns
  # - Small datasets
  # - Faster training
```

### finetune_loss

Objective function for optimization:
```yaml
parameters:
  finetune_loss: "mae"  # Mean Absolute Error (default)
  # Other options:
  # - "mse" - Mean Squared Error (penalizes large errors more)
  # - "mape" - Mean Absolute Percentage Error
  # - "smape" - Symmetric MAPE
```

## Multiple Dataset Handling

Fine-tune on hierarchical or multiple series:

```python
# Multiple related series
df = pd.DataFrame({
    'unique_id': ['store_1', 'store_1', 'store_2', 'store_2'],
    'ds': pd.date_range('2020-01-01', periods=2, freq='D').tolist() * 2,
    'y': [100, 110, 200, 220]
})

# TimeGPT learns patterns across all series
finetune_job = client.finetune(
    df=df,
    h=7,
    freq='D',
    model_name='multi-store-model'
)
```

## Time-Based vs Percentage Splits

### Time-Based Split (Recommended)
```yaml
data:
  split_strategy: "time"
  full_path: "data/sales.csv"
  train_end_date: "2023-12-31"
  val_start_date: "2024-01-01"
  val_end_date: "2024-06-30"
```

**Advantages**:
- Respects time series ordering
- Realistic production scenario
- Avoids data leakage

### Percentage Split
```yaml
data:
  split_strategy: "percentage"
  train_path: "data/sales_train.csv"
  val_path: "data/sales_val.csv"
```

**Use when**:
- Pre-split files already exist
- Custom split logic applied
- Non-temporal validation needed

## Custom Validation Strategies

### Expanding Window
Train on increasingly larger windows:
```python
# Window 1: 2020-2023
# Window 2: 2020-2024Q1
# Window 3: 2020-2024Q2
# Each window fine-tunes a new model
```

### Rolling Window
Fixed-size training window:
```python
# Window 1: 2021-2023
# Window 2: 2022-2024Q1
# Window 3: 2023-2024Q2
# Captures recent patterns only
```

## Integration with MLFlow

Track fine-tuning experiments:
```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("finetune_steps", finetune_steps)
    mlflow.log_param("model_name", model_name)

    # Fine-tune
    finetune_job = client.finetune(...)

    # Log metrics
    mlflow.log_metric("smape", metrics['smape'])
    mlflow.log_artifact(model_id_file)
```
