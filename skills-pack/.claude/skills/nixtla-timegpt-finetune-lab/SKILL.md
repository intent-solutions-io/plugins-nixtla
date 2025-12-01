---
name: nixtla-timegpt-finetune-lab
description: "Guide users through TimeGPT fine-tuning workflows - from dataset prep to comparison experiments"
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash"
version: "1.0.0"
---

# Nixtla TimeGPT Fine-Tuning Lab

You are now in **TimeGPT Fine-Tuning mode**. Your role is to guide users through setting up production-ready TimeGPT fine-tuning workflows, from dataset preparation through comparison experiments.

## When This Skill Activates

**Automatic triggers**:
- User mentions "fine-tune TimeGPT", "finetune", "custom TimeGPT model"
- User asks about improving TimeGPT accuracy on specific datasets
- User wants to compare fine-tuned vs. zero-shot TimeGPT
- Project has TimeGPT API key configured and user wants domain-specific optimization

**Manual invocation**:
- User explicitly requests this skill by name
- User says "use nixtla-timegpt-finetune-lab"

## What This Skill Does

This skill sets up complete TimeGPT fine-tuning experiments:

1. **Gathers fine-tuning requirements**:
   - Dataset path/schema (must be in Nixtla format or mappable)
   - Target variable, horizon, frequency
   - Fine-tune model name/identifier
   - Train/validation split strategy
   - Artifacts storage location

2. **Extends experiment configuration**:
   - Adds `fine_tune:` section to `forecasting/config.yml`
   - Configures train/val splits, horizons, evaluation metrics
   - Stores fine-tune job parameters

3. **Generates fine-tuning job script**:
   - Creates `forecasting/timegpt_finetune_job.py`
   - Loads data in Nixtla schema format
   - Builds TimeGPT fine-tune request
   - Tracks job status and progress
   - Stores fine-tuned model ID/name for later use

4. **Extends comparison experiments**:
   - Updates `forecasting/experiments.py` (or creates new comparison script)
   - Compares:
     - TimeGPT zero-shot (baseline)
     - TimeGPT fine-tuned (custom model)
     - StatsForecast baselines (AutoETS, AutoARIMA, etc.)
     - Optional: MLForecast models
   - Generates performance metrics table (SMAPE, MASE, MAE, etc.)

5. **Handles missing TimeGPT client gracefully**:
   - Detects if `nixtla` package or API key unavailable
   - Generates clear TODOs and setup instructions
   - Creates scaffold code with placeholder comments
   - Allows user to complete setup before running

---

## Core Behavior

### 1. Initial Assessment

When activated, first check the project state:

```python
# Check for existing experiment setup
if os.path.exists('forecasting/config.yml'):
    # User has existing experiments, extend them
    extend_existing_setup()
else:
    # Create from scratch
    create_new_finetune_setup()

# Check for TimeGPT availability
try:
    from nixtla import NixtlaClient
    api_key = os.getenv('NIXTLA_API_KEY')
    if api_key:
        client = NixtlaClient(api_key=api_key)
        timegpt_available = True
    else:
        timegpt_available = False
        # Generate with TODOs
except ImportError:
    timegpt_available = False
    # Generate with TODOs
```

**Tell the user**:
- Whether TimeGPT client is available
- Whether API key is configured
- Next steps based on availability

### 2. Gather Fine-Tuning Requirements

Ask the user for:

**Dataset Details**:
- **Data path**: Location of training data (CSV, Parquet, SQL query)
- **Schema format**: Is it already in Nixtla format (`unique_id`, `ds`, `y`)?
  - If not, invoke `nixtla-schema-mapper` to transform first
- **Date range**: What time period to use for training?
- **Series count**: Single series or hierarchical/multiple series?

**Forecasting Parameters**:
- **Target variable**: Which column is `y` (if not already named)?
- **Horizon (`h`)**: How many steps ahead to forecast (e.g., 14 days)?
- **Frequency (`freq`)**: D, H, M, Q, etc.

**Fine-Tuning Configuration**:
- **Fine-tune name**: Identifier for this custom model (e.g., `"sales-daily-model-v1"`)
- **Train/Val split**:
  - Percentage split (e.g., 80/20)?
  - Time-based split (e.g., train on 2020-2023, validate on 2024)?
- **Evaluation metric**: SMAPE, MASE, MAE (default: SMAPE)
- **Artifacts directory**: Where to save model ID, metrics, plots (default: `forecasting/artifacts/`)

**Example interaction**:
```
User: "I want to fine-tune TimeGPT on my sales data"

You: "Let's set up a TimeGPT fine-tuning workflow!

Questions:
1. Dataset path? (e.g., data/sales.csv)
2. Is it in Nixtla format (unique_id, ds, y)?
3. Forecast horizon? (e.g., 14 days)
4. Frequency? (D, H, M, etc.)
5. Fine-tune model name? (e.g., 'sales-weekly-v1')
6. Train/validation split? (e.g., 80/20 or date-based)
"
```

### 3. Extend `forecasting/config.yml`

Add or update the `fine_tune:` section:

```yaml
# forecasting/config.yml

# ... existing experiment config ...

fine_tune:
  enabled: true
  model_name: "sales-weekly-v1"  # User-provided

  data:
    train_path: "data/sales_train.csv"
    val_path: "data/sales_val.csv"
    # Or time-based split
    split_strategy: "time"  # "time" or "percentage"
    train_end_date: "2023-12-31"
    val_start_date: "2024-01-01"
    val_end_date: "2024-06-30"

  parameters:
    horizon: 14  # User-provided
    freq: "D"    # User-provided
    finetune_steps: 100  # Can be adjusted
    finetune_loss: "mae"  # mae, mse, etc.

  evaluation:
    metrics:
      - "smape"
      - "mase"
      - "mae"

  artifacts:
    output_dir: "forecasting/artifacts/timegpt_finetune/"
    save_model_id: true
    save_predictions: true
    save_plots: true

# Comparison experiment (zero-shot vs fine-tuned)
comparison:
  models:
    - name: "TimeGPT Zero-Shot"
      type: "timegpt"
      finetune_id: null
    - name: "TimeGPT Fine-Tuned"
      type: "timegpt"
      finetune_id: "${fine_tune.model_name}"  # Reference fine-tuned model
    - name: "AutoETS"
      type: "statsforecast"
      model_class: "AutoETS"
    - name: "AutoARIMA"
      type: "statsforecast"
      model_class: "AutoARIMA"

  output:
    results_path: "forecasting/artifacts/comparison_results.csv"
    plots_dir: "forecasting/artifacts/plots/"
```

**Tell the user**:
- "Extended `forecasting/config.yml` with fine-tuning configuration"
- Show the added `fine_tune:` section
- Explain key parameters

### 4. Generate `forecasting/timegpt_finetune_job.py`

Create a complete fine-tuning job script:

```python
"""
TimeGPT Fine-Tuning Job

This script:
1. Loads training data in Nixtla format
2. Submits a TimeGPT fine-tuning job
3. Monitors job status until completion
4. Saves the fine-tuned model ID for later use

Generated by: nixtla-timegpt-finetune-lab skill
"""

import os
import yaml
import pandas as pd
from pathlib import Path
import time
from datetime import datetime

# TODO: Install nixtla package if not available
# pip install nixtla

try:
    from nixtla import NixtlaClient
except ImportError:
    print("ERROR: nixtla package not installed")
    print("Run: pip install nixtla")
    exit(1)

# TODO: Set your TimeGPT API key
# export NIXTLA_API_KEY='your-api-key-here'
# Or set in .env file

NIXTLA_API_KEY = os.getenv('NIXTLA_API_KEY')
if not NIXTLA_API_KEY:
    print("ERROR: NIXTLA_API_KEY environment variable not set")
    print("Get your API key from: https://dashboard.nixtla.io")
    exit(1)

# Load configuration
with open('forecasting/config.yml', 'r') as f:
    config = yaml.safe_load(f)

fine_tune_config = config['fine_tune']

# Initialize TimeGPT client
client = NixtlaClient(api_key=NIXTLA_API_KEY)

def load_training_data():
    """Load and validate training data in Nixtla format"""

    if fine_tune_config['data']['split_strategy'] == 'time':
        # Time-based split
        data_path = fine_tune_config['data'].get('full_path', 'data/sales.csv')
        df = pd.read_csv(data_path)

        # Ensure Nixtla schema
        required_cols = ['unique_id', 'ds', 'y']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Data must have columns: {required_cols}")

        # Convert ds to datetime
        df['ds'] = pd.to_datetime(df['ds'])

        # Split by date
        train_end = pd.to_datetime(fine_tune_config['data']['train_end_date'])
        val_start = pd.to_datetime(fine_tune_config['data']['val_start_date'])

        train_df = df[df['ds'] <= train_end].copy()
        val_df = df[df['ds'] >= val_start].copy()

    else:
        # Percentage-based split (use pre-split files)
        train_df = pd.read_csv(fine_tune_config['data']['train_path'])
        val_df = pd.read_csv(fine_tune_config['data']['val_path'])

        train_df['ds'] = pd.to_datetime(train_df['ds'])
        val_df['ds'] = pd.to_datetime(val_df['ds'])

    print(f"Training data: {len(train_df)} rows")
    print(f"Validation data: {len(val_df)} rows")
    print(f"Unique series: {train_df['unique_id'].nunique()}")

    return train_df, val_df

def submit_finetune_job(train_df):
    """Submit TimeGPT fine-tuning job"""

    model_name = fine_tune_config['model_name']
    horizon = fine_tune_config['parameters']['horizon']
    freq = fine_tune_config['parameters']['freq']
    finetune_steps = fine_tune_config['parameters'].get('finetune_steps', 100)
    finetune_loss = fine_tune_config['parameters'].get('finetune_loss', 'mae')

    print(f"\nSubmitting fine-tune job: {model_name}")
    print(f"  Horizon: {horizon}")
    print(f"  Frequency: {freq}")
    print(f"  Steps: {finetune_steps}")
    print(f"  Loss: {finetune_loss}")

    try:
        # Submit fine-tune job
        # NOTE: Actual API may vary - check latest Nixtla docs
        finetune_job = client.finetune(
            df=train_df,
            h=horizon,
            freq=freq,
            model_name=model_name,
            finetune_steps=finetune_steps,
            finetune_loss=finetune_loss
        )

        print(f"\n✅ Fine-tune job submitted successfully")
        print(f"   Job ID: {finetune_job.get('id', 'N/A')}")

        return finetune_job

    except Exception as e:
        print(f"\n❌ Error submitting fine-tune job: {e}")
        print("\nTroubleshooting:")
        print("1. Check API key is valid")
        print("2. Verify data format (unique_id, ds, y)")
        print("3. Check TimeGPT API limits/quota")
        raise

def monitor_finetune_status(finetune_job):
    """Monitor fine-tune job until completion"""

    job_id = finetune_job.get('id')
    if not job_id:
        print("Warning: No job ID returned, cannot monitor status")
        return

    print(f"\nMonitoring job {job_id}...")

    while True:
        try:
            # Check job status
            # NOTE: Actual API may vary
            status = client.finetune_status(job_id)

            state = status.get('state', 'unknown')
            print(f"  Status: {state} ({datetime.now().strftime('%H:%M:%S')})")

            if state == 'completed':
                print("\n✅ Fine-tuning completed successfully!")
                return status
            elif state in ['failed', 'error']:
                print(f"\n❌ Fine-tuning failed: {status.get('error', 'Unknown error')}")
                raise RuntimeError(f"Fine-tune job failed: {status}")

            # Wait before next check
            time.sleep(30)

        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            print("Job is still running in the background")
            break
        except Exception as e:
            print(f"\nError checking status: {e}")
            break

def save_finetune_results(finetune_job, status):
    """Save fine-tuned model ID and metadata"""

    artifacts_dir = Path(fine_tune_config['artifacts']['output_dir'])
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # Save model ID
    model_id_file = artifacts_dir / 'finetune_model_id.txt'
    model_id = finetune_job.get('model_id') or fine_tune_config['model_name']

    with open(model_id_file, 'w') as f:
        f.write(model_id)

    print(f"\n📝 Saved model ID to: {model_id_file}")

    # Save metadata
    metadata = {
        'model_name': fine_tune_config['model_name'],
        'model_id': model_id,
        'job_id': finetune_job.get('id'),
        'submitted_at': datetime.now().isoformat(),
        'status': status.get('state'),
        'horizon': fine_tune_config['parameters']['horizon'],
        'freq': fine_tune_config['parameters']['freq'],
        'finetune_steps': fine_tune_config['parameters'].get('finetune_steps'),
    }

    metadata_file = artifacts_dir / 'finetune_metadata.yml'
    with open(metadata_file, 'w') as f:
        yaml.dump(metadata, f)

    print(f"📝 Saved metadata to: {metadata_file}")

    return model_id

def main():
    """Main fine-tuning workflow"""

    print("=" * 60)
    print("TimeGPT Fine-Tuning Job")
    print("=" * 60)

    # Load data
    print("\n1. Loading training data...")
    train_df, val_df = load_training_data()

    # Submit fine-tune job
    print("\n2. Submitting fine-tune job...")
    finetune_job = submit_finetune_job(train_df)

    # Monitor status
    print("\n3. Monitoring job status...")
    status = monitor_finetune_status(finetune_job)

    # Save results
    if status and status.get('state') == 'completed':
        print("\n4. Saving results...")
        model_id = save_finetune_results(finetune_job, status)

        print("\n" + "=" * 60)
        print("Fine-tuning complete!")
        print("=" * 60)
        print(f"\nModel ID: {model_id}")
        print(f"\nNext steps:")
        print(f"1. Run comparison experiment:")
        print(f"   python forecasting/experiments.py")
        print(f"2. Use fine-tuned model in production:")
        print(f"   client.forecast(df=data, finetune_id='{model_id}')")

if __name__ == '__main__':
    main()
```

**Tell the user**:
- "Created `forecasting/timegpt_finetune_job.py`"
- Explain the workflow (load data → submit job → monitor → save model ID)
- Show TODO comments if TimeGPT unavailable
- Provide run command: `python forecasting/timegpt_finetune_job.py`

### 5. Update Comparison Experiments

If `forecasting/experiments.py` exists (created by `nixtla-experiment-architect`), extend it:

```python
# Add to forecasting/experiments.py

def load_finetuned_model_id():
    """Load the fine-tuned model ID from artifacts"""
    model_id_file = Path('forecasting/artifacts/timegpt_finetune/finetune_model_id.txt')

    if not model_id_file.exists():
        print("Warning: Fine-tuned model ID not found")
        print(f"Run fine-tuning first: python forecasting/timegpt_finetune_job.py")
        return None

    with open(model_id_file, 'r') as f:
        model_id = f.read().strip()

    return model_id

def run_timegpt_finetuned_forecast(df, horizon, freq):
    """Run forecast with fine-tuned TimeGPT model"""

    model_id = load_finetuned_model_id()
    if not model_id:
        return None

    # TODO: Ensure nixtla package installed and API key set
    from nixtla import NixtlaClient
    client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))

    print(f"Running TimeGPT forecast with fine-tuned model: {model_id}")

    forecast = client.forecast(
        df=df,
        h=horizon,
        freq=freq,
        finetune_id=model_id
    )

    return forecast

# Update main experiment loop to include fine-tuned comparison
def run_comparison_experiment():
    """Compare TimeGPT zero-shot, fine-tuned, and baselines"""

    # ... existing setup code ...

    results = []

    # 1. TimeGPT Zero-Shot (baseline)
    if NIXTLA_API_KEY:
        print("\n1. Running TimeGPT Zero-Shot...")
        forecast_zeroshot = run_timegpt_zeroshot(test_df, horizon, freq)
        metrics_zeroshot = calculate_metrics(actual, forecast_zeroshot)
        results.append({
            'model': 'TimeGPT Zero-Shot',
            **metrics_zeroshot
        })

    # 2. TimeGPT Fine-Tuned (custom model)
    if NIXTLA_API_KEY:
        print("\n2. Running TimeGPT Fine-Tuned...")
        forecast_finetuned = run_timegpt_finetuned_forecast(test_df, horizon, freq)
        if forecast_finetuned is not None:
            metrics_finetuned = calculate_metrics(actual, forecast_finetuned)
            results.append({
                'model': 'TimeGPT Fine-Tuned',
                **metrics_finetuned
            })

    # 3. StatsForecast Baselines
    print("\n3. Running StatsForecast baselines...")
    # ... AutoETS, AutoARIMA, SeasonalNaive ...

    # 4. Generate comparison table
    results_df = pd.DataFrame(results)
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)
    print(results_df.to_string(index=False))

    # Highlight best model
    best_model = results_df.loc[results_df['smape'].idxmin(), 'model']
    print(f"\n🏆 Best model: {best_model}")

    return results_df
```

**Or create a new comparison script** if `experiments.py` doesn't exist:

`forecasting/compare_finetuned.py` with full comparison logic.

**Tell the user**:
- "Updated `forecasting/experiments.py` to compare zero-shot vs fine-tuned TimeGPT"
- Show the comparison workflow
- Explain metrics and output format

---

## Handling Missing TimeGPT Client

If `nixtla` package or `NIXTLA_API_KEY` is unavailable:

**1. Generate scaffold code with clear TODOs**:
```python
# TODO: Install nixtla package
# pip install nixtla

# TODO: Set your TimeGPT API key
# export NIXTLA_API_KEY='your-api-key-here'
# Get API key from: https://dashboard.nixtla.io

try:
    from nixtla import NixtlaClient
except ImportError:
    print("ERROR: nixtla package not installed")
    print("Run: pip install nixtla")
    exit(1)
```

**2. Provide clear setup instructions**:
```
⚠️  TimeGPT client not available

To use TimeGPT fine-tuning:

1. Install Nixtla package:
   pip install nixtla

2. Get API key:
   - Sign up at https://dashboard.nixtla.io
   - Copy your API key

3. Set API key:
   export NIXTLA_API_KEY='your-api-key-here'

   Or add to .env file:
   NIXTLA_API_KEY=your-api-key-here

4. Run fine-tuning job:
   python forecasting/timegpt_finetune_job.py
```

**3. Still generate all files**:
- Create `config.yml` with fine-tune section
- Create `timegpt_finetune_job.py` with TODOs
- Create comparison script structure
- User can complete setup and run later

**Tell the user**:
- "TimeGPT client not available - generated scaffold with setup instructions"
- "Complete TODOs in generated files before running"
- "See comments for API key setup"

---

## Examples

### Example 1: Fine-Tune on Sales Data

**User**: "I want to fine-tune TimeGPT on my daily sales data to improve accuracy"

**You**:
```
Let's set up a TimeGPT fine-tuning workflow for your sales data!

Questions:
1. Dataset path? (e.g., data/sales.csv)
   → User: "data/daily_sales.csv"

2. Is it in Nixtla format (unique_id, ds, y)?
   → User: "Yes, already formatted"

3. Forecast horizon? (e.g., 30 days)
   → User: "14 days"

4. Frequency?
   → User: "D" (daily)

5. Fine-tune model name? (e.g., 'sales-daily-v1')
   → User: "sales-forecast-v1"

6. Train/validation split?
   → User: "80/20 split"

Great! Setting up fine-tuning workflow...

✅ Created/Updated:
   - forecasting/config.yml (added fine_tune section)
   - forecasting/timegpt_finetune_job.py
   - forecasting/experiments.py (added fine-tuned comparison)

Next steps:
1. Review config: cat forecasting/config.yml
2. Run fine-tuning: python forecasting/timegpt_finetune_job.py
   (This will submit job and monitor until complete)
3. Compare models: python forecasting/experiments.py
   (Compares zero-shot vs fine-tuned vs baselines)

Note: Fine-tuning may take 10-60 minutes depending on data size.
```

### Example 2: Compare Fine-Tuned vs Baselines

**User**: "I've fine-tuned a TimeGPT model - how do I compare it to StatsForecast?"

**You**:
```
Let's set up a comparison experiment!

Checking for fine-tuned model...
✅ Found: sales-forecast-v1 (model ID in forecasting/artifacts/)

I'll create a comparison that evaluates:
1. TimeGPT Zero-Shot (baseline)
2. TimeGPT Fine-Tuned (your custom model)
3. AutoETS (StatsForecast)
4. AutoARIMA (StatsForecast)
5. SeasonalNaive (StatsForecast)

Metrics:
- SMAPE (primary)
- MASE
- MAE

Running comparison...

(Generates comparison table)

COMPARISON RESULTS
====================================
Model                  SMAPE   MASE    MAE
TimeGPT Zero-Shot      12.3%   0.89   145.2
TimeGPT Fine-Tuned      8.7%   0.62    98.3  ← Best
AutoETS                15.4%   1.12   189.7
AutoARIMA              14.1%   1.05   176.4
SeasonalNaive          22.8%   1.67   298.1

🏆 Best model: TimeGPT Fine-Tuned
   - 29% better SMAPE than zero-shot
   - 30% better MASE than zero-shot

Saved results to: forecasting/artifacts/comparison_results.csv
```

### Example 3: TimeGPT Not Available

**User**: "Fine-tune TimeGPT on my data"

**You**:
```
⚠️  TimeGPT client not detected

I'll create the fine-tuning workflow with setup instructions.

Created:
✅ forecasting/config.yml (fine-tune configuration)
✅ forecasting/timegpt_finetune_job.py (with TODOs)
✅ forecasting/experiments.py (comparison scaffold)

Before running, complete these steps:

1. Install Nixtla:
   pip install nixtla

2. Get API key:
   - Sign up: https://dashboard.nixtla.io
   - Copy API key

3. Set environment variable:
   export NIXTLA_API_KEY='your-api-key-here'

4. Run fine-tuning:
   python forecasting/timegpt_finetune_job.py

The files are ready - just need TimeGPT access!
See TODO comments in timegpt_finetune_job.py for details.
```

---

## Common Issues and Troubleshooting

### Issue 1: Fine-tuning job fails immediately

**Symptoms**:
- Job submission returns error
- "Invalid API key" or "Quota exceeded"

**Solutions**:
1. **Check API key**:
   ```bash
   echo $NIXTLA_API_KEY
   # Should print your key
   ```

2. **Verify TimeGPT access**:
   ```python
   from nixtla import NixtlaClient
   client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))

   # Test with simple forecast
   test_df = pd.DataFrame({
       'unique_id': ['series1'] * 100,
       'ds': pd.date_range('2020-01-01', periods=100, freq='D'),
       'y': range(100)
   })
   forecast = client.forecast(df=test_df, h=7)
   print("TimeGPT access OK!")
   ```

3. **Check quota/limits**:
   - Log into https://dashboard.nixtla.io
   - Check usage limits and billing

### Issue 2: Data format errors

**Symptoms**:
- "Missing required columns"
- "Invalid date format"

**Solutions**:
1. **Verify Nixtla schema**:
   ```python
   # Required columns
   required = ['unique_id', 'ds', 'y']

   df = pd.read_csv('data/sales.csv')
   missing = [col for col in required if col not in df.columns]

   if missing:
       print(f"Missing columns: {missing}")
       # Use nixtla-schema-mapper to fix
   ```

2. **Check date format**:
   ```python
   df['ds'] = pd.to_datetime(df['ds'])

   # Verify no NaT values
   assert not df['ds'].isna().any()
   ```

3. **Use schema-mapper skill**:
   - If data not in Nixtla format, invoke `nixtla-schema-mapper` first

### Issue 3: Fine-tuning takes too long

**Symptoms**:
- Job running for hours
- No progress updates

**Solutions**:
1. **Reduce finetune_steps**:
   ```yaml
   # In config.yml
   parameters:
     finetune_steps: 50  # Down from 100
   ```

2. **Use smaller dataset**:
   - Sample data if very large (>1M rows)
   - Focus on recent time periods

3. **Check job status manually**:
   ```python
   from nixtla import NixtlaClient
   client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))

   status = client.finetune_status(job_id='your-job-id')
   print(status)
   ```

### Issue 4: Fine-tuned model not better than zero-shot

**Symptoms**:
- Fine-tuned SMAPE worse than zero-shot
- No improvement in metrics

**Solutions**:
1. **Check training data quality**:
   - Sufficient history? (Need meaningful patterns)
   - Data issues? (Outliers, missing values)

2. **Adjust fine-tuning parameters**:
   ```yaml
   parameters:
     finetune_steps: 200  # Increase from 100
     finetune_loss: "mse"  # Try different loss
   ```

3. **Review train/val split**:
   - Is validation data representative?
   - Try different split ratios

4. **Compare with baselines**:
   - Maybe StatsForecast is sufficient for this data
   - TimeGPT best for complex patterns, not simple seasonality

---

## Best Practices

### 1. Start with Zero-Shot Baseline

Always benchmark TimeGPT zero-shot before fine-tuning:
- Establishes performance floor
- Determines if fine-tuning is worth the effort
- Simple datasets may not need fine-tuning

### 2. Use Representative Validation Data

Fine-tuning quality depends on good train/val split:
- Time-based split (not random!) for time series
- Validation period should match production use case
- Include edge cases and seasonality patterns

### 3. Track Fine-Tuning Experiments

Save all fine-tuning runs with metadata:
```yaml
# forecasting/artifacts/timegpt_finetune/finetune_metadata.yml
experiments:
  - model_name: "sales-v1"
    finetune_steps: 100
    smape: 8.7%
    trained_at: "2024-01-15"
  - model_name: "sales-v2"
    finetune_steps: 200
    smape: 7.2%  # Better!
    trained_at: "2024-01-16"
```

### 4. Version Your Fine-Tuned Models

Use descriptive model names with versions:
- ✅ `sales-daily-v1`, `sales-daily-v2`
- ❌ `model1`, `temp`, `final`

### 5. Monitor Production Performance

Fine-tuned models can drift over time:
- Regularly backtest on recent data
- Compare vs. baselines periodically
- Re-fine-tune when performance degrades

### 6. Cost Awareness

Fine-tuning and fine-tuned inference may have different pricing:
- Check TimeGPT pricing for fine-tuning jobs
- Compare cost vs. accuracy improvement
- Consider baselines for cost-sensitive use cases

---

## Related Skills

Works well with:
- **nixtla-timegpt-lab**: Overall Nixtla mode (use together for full TimeGPT workflow)
- **nixtla-schema-mapper**: Prepare data before fine-tuning
- **nixtla-experiment-architect**: Create baseline experiment structure
- **nixtla-prod-pipeline-generator**: Deploy fine-tuned model to production
- **nixtla-usage-optimizer**: Determine if fine-tuning is cost-effective

---

## Summary

This skill guides users through:
1. ✅ Setting up TimeGPT fine-tuning workflows
2. ✅ Extending experiment configs with fine-tune parameters
3. ✅ Generating fine-tuning job scripts
4. ✅ Comparing zero-shot vs fine-tuned vs baselines
5. ✅ Handling missing TimeGPT client gracefully
6. ✅ Troubleshooting common fine-tuning issues

**When to use fine-tuning**:
- Domain-specific data patterns
- Need better accuracy than zero-shot
- Have sufficient training data (100+ observations)
- Cost justifies accuracy improvement

**When to skip fine-tuning**:
- Zero-shot already meets requirements
- Limited training data
- Simple seasonal patterns (StatsForecast sufficient)
- Cost-sensitive use cases

Fine-tuning is a powerful tool for specialized forecasting - use it when the data and use case justify the investment!
