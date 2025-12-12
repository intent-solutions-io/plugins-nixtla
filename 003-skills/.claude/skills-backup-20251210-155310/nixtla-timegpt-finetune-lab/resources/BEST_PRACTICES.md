# TimeGPT Fine-Tuning Best Practices

## 1. Start with Zero-Shot Baseline

**Always establish baseline performance first**:

```python
# Step 1: Run zero-shot TimeGPT
zeroshot_forecast = client.forecast(df=train_df, h=horizon, freq=freq)
zeroshot_metrics = calculate_metrics(test_df, zeroshot_forecast)

print(f"Zero-shot SMAPE: {zeroshot_metrics['smape']}")

# Decision framework:
# - If SMAPE < 10%: Zero-shot is excellent, fine-tuning may not help
# - If SMAPE 10-15%: Fine-tuning likely provides marginal improvement
# - If SMAPE > 15%: Fine-tuning has good potential for improvement
```

**Why**:
- Avoid unnecessary fine-tuning costs
- Set realistic improvement expectations
- Understand what zero-shot already captures

---

## 2. Use Representative Validation Data

**Good validation split**:
```python
# Time-based split preserves temporal ordering
train_end = '2023-12-31'
val_start = '2024-01-01'
val_end = '2024-03-31'

train_df = df[df['ds'] <= train_end]
val_df = df[(df['ds'] >= val_start) & (df['ds'] <= val_end)]
```

**Bad validation split**:
```python
# Random split breaks temporal structure
train_df = df.sample(frac=0.8)  # Don't do this for time series
```

**Validation period guidelines**:
- At least 2x the forecast horizon
- Includes similar patterns to training (same seasons, events)
- Recent enough to be relevant (last 6-12 months)
- Not too far in future (avoid regime shifts)

---

## 3. Track Fine-Tuning Experiments

**Create experiment tracking system**:

```python
# experiments_log.csv
experiment_id, model_name, finetune_steps, finetune_loss, train_smape, val_smape, test_smape, timestamp
exp_001, sales-v1, 100, mae, 8.5, 12.3, 12.8, 2024-01-15
exp_002, sales-v2, 200, mse, 7.2, 11.5, 11.9, 2024-01-16
exp_003, sales-v3, 200, mae, 7.8, 10.8, 11.2, 2024-01-17  # Best
```

**Track key information**:
- Model name and version
- Fine-tuning parameters (steps, loss)
- Performance metrics (train/val/test)
- Data characteristics (volume, date range)
- Timestamp and experiment notes

**Benefits**:
- Compare experiments objectively
- Identify best configurations
- Avoid repeating failed experiments
- Document improvement over time

---

## 4. Version Fine-Tuned Models

**Use semantic versioning**:

```yaml
# Versioning scheme: {dataset}-{horizon}-v{version}
model_name: "sales-daily-v1"
model_name: "sales-daily-v2"  # After parameter tuning
model_name: "sales-weekly-v1"  # Different horizon

# In production
production_model: "sales-daily-v2"
candidate_model: "sales-daily-v3"
```

**Tag models with metadata**:
```yaml
# finetune_metadata.yml
model_name: "sales-daily-v2"
finetune_id: "ft-abc123xyz"
created_at: "2024-01-17T10:30:00Z"
dataset_version: "2024-01-15"
train_period: "2020-01-01 to 2023-12-31"
val_period: "2024-01-01 to 2024-03-31"
horizon: 14
freq: "D"
finetune_steps: 200
finetune_loss: "mse"
performance:
  train_smape: 7.8
  val_smape: 10.8
  test_smape: 11.2
status: "production"
```

---

## 5. Monitor Production Performance

**Set up continuous evaluation**:

```python
# production_monitoring.py
def evaluate_production_model(model_id, lookback_days=30):
    """
    Evaluate production model on recent data
    """
    # Get recent actuals
    end_date = datetime.now()
    start_date = end_date - timedelta(days=lookback_days)

    actuals = fetch_actuals(start_date, end_date)

    # Get forecasts that were made
    forecasts = fetch_forecasts(start_date, end_date, model_id)

    # Calculate realized metrics
    metrics = calculate_metrics(actuals, forecasts)

    # Alert if performance degrades
    if metrics['smape'] > THRESHOLD:
        send_alert(f"Model {model_id} SMAPE: {metrics['smape']} exceeds threshold")

    return metrics

# Run daily
schedule.every().day.at("08:00").do(evaluate_production_model, model_id="ft-abc123xyz")
```

**Monitor for**:
- Performance degradation over time
- Regime shifts in data patterns
- Seasonal changes affecting accuracy
- Data quality issues

**Retrain triggers**:
- SMAPE increases by 20% from baseline
- New seasonal patterns emerge
- Quarterly or semi-annual schedule
- Significant business changes

---

## 6. Cost Awareness

**Understand fine-tuning costs**:

```python
# Example cost calculation (hypothetical rates)
FINETUNE_COST = 100  # API credits per fine-tuning job
INFERENCE_COST_ZEROSHOT = 0.01  # Per forecast
INFERENCE_COST_FINETUNED = 0.015  # Per forecast (may be higher)

# Calculate monthly cost
forecasts_per_month = 1000
monthly_inference_cost = forecasts_per_month * INFERENCE_COST_FINETUNED

# Amortize fine-tune cost (retrain quarterly)
monthly_finetune_cost = FINETUNE_COST / 3

total_monthly_cost = monthly_inference_cost + monthly_finetune_cost
print(f"Total monthly cost: ${total_monthly_cost}")
```

**Cost optimization strategies**:

1. **Batch forecasts**:
   ```python
   # Instead of 1000 individual calls
   forecast = client.forecast(df=all_series, h=horizon)

   # Use batch API (if available)
   forecasts = client.batch_forecast(df=all_series, h=horizon)
   ```

2. **Cache forecasts**:
   ```python
   # Cache forecasts that don't change frequently
   cache_key = f"{model_id}_{series_id}_{forecast_date}"
   if cache_key in forecast_cache:
       return forecast_cache[cache_key]
   else:
       forecast = client.forecast(...)
       forecast_cache[cache_key] = forecast
   ```

3. **Use fine-tuning selectively**:
   - Fine-tune only for critical series
   - Use zero-shot for less important series
   - Hybrid approach saves costs while maintaining quality

---

## 7. Data Quality First

**Pre-fine-tuning data validation**:

```python
def validate_training_data(df, horizon):
    """
    Comprehensive data validation before fine-tuning
    """
    issues = []

    # Check volume
    if len(df) < 100:
        issues.append(f"Insufficient data: {len(df)} rows (minimum: 100)")

    # Check completeness
    null_counts = df.isnull().sum()
    if null_counts.any():
        issues.append(f"Null values found: {null_counts[null_counts > 0]}")

    # Check temporal coverage
    min_date = df['ds'].min()
    max_date = df['ds'].max()
    date_range = (max_date - min_date).days
    if date_range < horizon * 10:
        issues.append(f"Insufficient temporal coverage: {date_range} days")

    # Check for outliers
    q1 = df['y'].quantile(0.25)
    q3 = df['y'].quantile(0.75)
    iqr = q3 - q1
    outliers = df[(df['y'] < q1 - 3*iqr) | (df['y'] > q3 + 3*iqr)]
    if len(outliers) > len(df) * 0.05:
        issues.append(f"High outlier rate: {len(outliers)/len(df):.1%}")

    # Check stationarity (basic check)
    mean_first_half = df[:len(df)//2]['y'].mean()
    mean_second_half = df[len(df)//2:]['y'].mean()
    if abs(mean_first_half - mean_second_half) / mean_first_half > 0.5:
        issues.append("Non-stationary data detected (mean shift > 50%)")

    return issues

# Use before fine-tuning
issues = validate_training_data(train_df, horizon=14)
if issues:
    print("Data quality issues:")
    for issue in issues:
        print(f"  - {issue}")
    print("\nResolve issues before fine-tuning")
```

---

## 8. Document Everything

**Create runbook for each fine-tuned model** with:
- Model purpose and ownership
- Training/validation data details
- Performance metrics and baselines
- Configuration parameters
- Usage examples
- Monitoring thresholds
- Known issues
- Change history

See `resources/templates/` for runbook template.

---

## 9. Test Before Production Deployment

**Staging validation**:

```python
def staging_validation(model_id, test_datasets):
    """
    Validate model on multiple test scenarios before production
    """
    results = []

    for test_name, test_df in test_datasets.items():
        forecast = client.forecast(
            df=test_df,
            h=horizon,
            freq=freq,
            finetune_id=model_id
        )

        metrics = calculate_metrics(test_df, forecast)
        results.append({
            'test_scenario': test_name,
            **metrics
        })

    # All tests must pass thresholds
    for result in results:
        if result['smape'] > MAX_ACCEPTABLE_SMAPE:
            raise ValueError(f"Model failed on {result['test_scenario']}")

    return results

# Define test scenarios
test_datasets = {
    'recent_data': df_recent,
    'seasonal_peaks': df_seasonal,
    'low_volume': df_low_volume,
    'high_volume': df_high_volume
}

staging_validation(model_id='ft-abc123xyz', test_datasets=test_datasets)
```

---

## 10. Incremental Improvement

**Iterative fine-tuning workflow**:

```
Baseline (Zero-shot) → SMAPE: 15.2%
    ↓
Experiment 1: finetune_steps=100, loss=mae → SMAPE: 13.8%  (✓ 9% improvement)
    ↓
Experiment 2: finetune_steps=200, loss=mae → SMAPE: 12.5%  (✓ 9% improvement)
    ↓
Experiment 3: finetune_steps=200, loss=mse → SMAPE: 11.8%  (✓ 6% improvement)
    ↓
Experiment 4: finetune_steps=300, loss=mse → SMAPE: 11.6%  (2% improvement, diminishing returns)
    ↓
Production Model: Experiment 3 (best ROI)
```

**Guidelines**:
- Make one change at a time
- Document what worked and what didn't
- Stop when improvements become marginal (< 5%)
- Consider cost vs. accuracy tradeoff
