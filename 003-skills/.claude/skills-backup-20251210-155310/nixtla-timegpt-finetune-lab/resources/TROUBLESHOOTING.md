# TimeGPT Fine-Tuning Troubleshooting

## Issue 1: Fine-Tuning Job Fails Immediately

**Symptoms**:
- Job returns 'failed' status within seconds
- Error message in API response

**Common causes**:

### 1. Data format errors
```python
# Check for required columns
required_cols = ['unique_id', 'ds', 'y']
missing = [col for col in required_cols if col not in df.columns]
if missing:
    print(f"Missing columns: {missing}")

# Check for null values
print(df.isnull().sum())

# Check data types
print(df.dtypes)
# ds should be datetime, y should be numeric
```

**Fix**:
- Ensure `ds` column is datetime format
- Ensure `y` column is numeric (float/int)
- Remove or impute null values

### 2. Insufficient data
**Minimum requirements**:
- At least 100 observations per series
- At least 2x the forecast horizon

**Fix**:
```python
# Check data volume
print(f"Total rows: {len(df)}")
for uid in df['unique_id'].unique():
    series_len = len(df[df['unique_id'] == uid])
    print(f"{uid}: {series_len} observations")

# If insufficient, collect more data or reduce horizon
```

### 3. Invalid API key
```bash
# Test API key
export NIXTLA_API_KEY='your-key-here'
python -c "from nixtla import NixtlaClient; client = NixtlaClient(); print('API key valid')"
```

**Fix**:
- Get valid API key from https://dashboard.nixtla.io
- Check for typos in environment variable

---

## Issue 2: Fine-Tuning Takes Too Long

**Symptoms**:
- Job runs for 30+ minutes
- Status remains 'training' for extended period

**Common causes**:

### 1. Large dataset
- Fine-tuning time scales with data volume
- 10,000+ rows can take 20-40 minutes

**Solutions**:
```python
# Option 1: Sample data for faster iteration
df_sample = df.sample(frac=0.5, random_state=42)

# Option 2: Reduce finetune_steps
finetune_steps = 50  # Down from 100

# Option 3: Use time-based subset
df_recent = df[df['ds'] >= '2023-01-01']
```

### 2. Network issues
- Intermittent connection can slow monitoring

**Fix**:
- Use longer polling intervals
- Add retry logic with exponential backoff

---

## Issue 3: Fine-Tuned Model Not Better Than Zero-Shot

**Symptoms**:
- Fine-tuned SMAPE similar to or worse than zero-shot
- No accuracy improvement despite successful training

**Diagnostic steps**:

### 1. Check validation data
```python
# Is validation data representative?
train_stats = train_df['y'].describe()
val_stats = val_df['y'].describe()
print("Train stats:", train_stats)
print("Val stats:", val_stats)

# Check for distribution shift
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
train_df['y'].hist(bins=50, alpha=0.5, label='Train')
plt.subplot(1, 2, 2)
val_df['y'].hist(bins=50, alpha=0.5, label='Val')
plt.legend()
```

**Fix**:
- Ensure validation period has similar patterns to training
- Avoid seasonal mismatches (e.g., don't train on summer, validate on winter)

### 2. Try different loss functions
```yaml
# In config.yml
parameters:
  finetune_loss: "mse"  # Try: mae, mse, rmse
```

**Rule of thumb**:
- Use `mae` for stable data with few outliers
- Use `mse` for data with important large deviations
- Use `rmse` as middle ground

### 3. Adjust fine-tuning steps
```yaml
parameters:
  finetune_steps: 200  # Increase from default 100
```

**Guidelines**:
- Small datasets (< 1000 rows): 50-100 steps
- Medium datasets (1000-10000 rows): 100-200 steps
- Large datasets (> 10000 rows): 200-500 steps

### 4. Check for overfitting
```python
# Compare train vs validation performance
train_forecast = client.forecast(df=train_df, h=horizon, finetune_id=model_id)
train_metrics = calculate_metrics(train_df, train_forecast)

val_forecast = client.forecast(df=train_df, h=horizon, finetune_id=model_id)
val_metrics = calculate_metrics(val_df, val_forecast)

print(f"Train SMAPE: {train_metrics['smape']}")
print(f"Val SMAPE: {val_metrics['smape']}")

# If train_smape << val_smape: overfitting
# Solution: reduce finetune_steps or add regularization
```

---

## Issue 4: Model ID Not Saved Correctly

**Symptoms**:
- Comparison script can't find fine-tuned model ID
- File exists but is empty or corrupted

**Fix**:

```python
# Robust model ID saving
def save_finetune_results(config, finetune_job, status):
    output_dir = Path(config['artifacts']['output_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)

    model_id_file = output_dir / 'finetune_model_id.txt'
    model_id = finetune_job.get('finetune_id', '')

    if not model_id:
        raise ValueError("No finetune_id in API response")

    # Atomic write
    temp_file = model_id_file.with_suffix('.tmp')
    temp_file.write_text(model_id)
    temp_file.rename(model_id_file)

    print(f"Saved model ID: {model_id}")

    # Verify
    saved_id = model_id_file.read_text().strip()
    assert saved_id == model_id, "Model ID verification failed"
```

---

## Issue 5: API Rate Limiting

**Symptoms**:
- Job submission fails with rate limit error
- "Too many requests" message

**Fix**:

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3):
    """Decorator for exponential backoff on rate limits"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if 'rate limit' in str(e).lower():
                        wait_time = 2 ** attempt  # 1s, 2s, 4s
                        print(f"Rate limited. Waiting {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise
            raise Exception(f"Max retries ({max_retries}) exceeded")
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def submit_finetune_job(client, config, train_df):
    return client.finetune(df=train_df, ...)
```

---

## Issue 6: Memory Errors with Large Datasets

**Symptoms**:
- Python crashes with MemoryError
- System runs out of RAM during fine-tuning

**Fix**:

```python
# Option 1: Use chunked data loading
def load_training_data_chunked(path, chunk_size=10000):
    chunks = pd.read_csv(path, chunksize=chunk_size)
    df = pd.concat([chunk for chunk in chunks])
    return df

# Option 2: Optimize data types
def optimize_dtypes(df):
    # Use smaller integer types
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    # Use float32 instead of float64
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = df[col].astype('float32')

    return df

# Option 3: Sample data
df_sample = df.sample(n=50000, random_state=42)
```

---

## Issue 7: Fine-Tuning Monitoring Timeout

**Symptoms**:
- Monitoring script times out before job completes
- Job is still running but script exits

**Fix**:

```python
def monitor_finetune_status(client, finetune_id, timeout_minutes=120):
    """Extended timeout for large datasets"""
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60

    # Save state periodically
    state_file = Path('finetune_monitoring_state.json')

    while True:
        elapsed = time.time() - start_time

        try:
            status = client.get_finetune_status(finetune_id)
            current_status = status.get('status', 'unknown')

            # Save state
            state = {
                'finetune_id': finetune_id,
                'status': current_status,
                'elapsed_seconds': elapsed,
                'last_check': time.time()
            }
            state_file.write_text(json.dumps(state))

            if current_status in ['completed', 'failed']:
                return current_status

            time.sleep(120)  # 2 minute intervals

        except KeyboardInterrupt:
            print(f"Monitoring interrupted. Resume with:")
            print(f"python resume_monitoring.py {finetune_id}")
            raise
```

---

## Debug Checklist

Before opening a support ticket, verify:

- [ ] Data is in correct Nixtla format (unique_id, ds, y)
- [ ] API key is valid and has credits
- [ ] Dataset has sufficient volume (100+ observations)
- [ ] No null values in required columns
- [ ] `ds` column is datetime type
- [ ] `y` column is numeric type
- [ ] Validation data is representative of training data
- [ ] Network connection is stable
- [ ] Sufficient memory available
- [ ] Fine-tuning parameters are reasonable (steps, loss)

**Get help**:
- Check Nixtla documentation: https://docs.nixtla.io
- Join Slack community: https://join.slack.com/t/nixtlaworkspace/...
- Open GitHub issue: https://github.com/Nixtla/nixtla/issues
