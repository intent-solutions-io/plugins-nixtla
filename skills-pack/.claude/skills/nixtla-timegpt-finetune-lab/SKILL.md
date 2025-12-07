---
name: nixtla-timegpt-finetune-lab
description: "Enables TimeGPT model fine-tuning on custom datasets with Nixtla SDK. Guides dataset preparation, job submission, status monitoring, model comparison, and accuracy benchmarking. Use when user needs TimeGPT fine-tuning, custom model training, domain-specific optimization, or zero-shot vs fine-tuned comparison. Trigger with 'fine-tune TimeGPT', 'train custom model', 'optimize TimeGPT accuracy', 'compare fine-tuned models'."
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

Create a complete fine-tuning job script with:
- Data loading and validation
- Job submission to TimeGPT API
- Status monitoring until completion
- Model ID persistence for later use

**Core structure** (condensed for brevity):
```python
# TimeGPT Fine-Tuning Job Script
from nixtla import NixtlaClient
import yaml, pandas as pd

# Load config
config = yaml.safe_load(open('forecasting/config.yml'))
client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))

# Load training data (time-based or percentage split)
train_df, val_df = load_training_data()

# Submit fine-tune job
finetune_job = client.finetune(
    df=train_df,
    h=horizon,
    freq=freq,
    model_name=model_name,
    finetune_steps=100,
    finetune_loss='mae'
)

# Monitor status until completed
status = monitor_finetune_status(finetune_job)

# Save model ID
save_finetune_results(finetune_job, status)
```

**For full implementation**, see `resources/TEMPLATES/timegpt_finetune_job_full.py`

**Tell the user**:
- "Created `forecasting/timegpt_finetune_job.py`"
- Explain the workflow (load data → submit job → monitor → save model ID)
- Provide run command: `python forecasting/timegpt_finetune_job.py`

### 5. Update Comparison Experiments

Add fine-tuned model comparison to `forecasting/experiments.py`:

**Core additions** (condensed):
```python
# Load fine-tuned model ID
def load_finetuned_model_id():
    model_id_file = Path('forecasting/artifacts/timegpt_finetune/finetune_model_id.txt')
    return model_id_file.read_text().strip() if model_id_file.exists() else None

# Run forecast with fine-tuned model
def run_timegpt_finetuned_forecast(df, horizon, freq):
    model_id = load_finetuned_model_id()
    return client.forecast(df=df, h=horizon, freq=freq, finetune_id=model_id)

# Compare: zero-shot vs fine-tuned vs baselines
results = [
    {'model': 'TimeGPT Zero-Shot', **metrics_zeroshot},
    {'model': 'TimeGPT Fine-Tuned', **metrics_finetuned},
    {'model': 'AutoETS', **metrics_autoets},
]
```

**For full code**, see `resources/TEMPLATES/experiments_finetune_comparison.py`

**Tell the user**:
- "Updated `forecasting/experiments.py` to compare zero-shot vs fine-tuned TimeGPT"
- Explain metrics: SMAPE, MASE, MAE

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

## Usage Examples

For detailed examples and scenarios, see `resources/SCENARIOS.md`:
- Example 1: Fine-tune on sales data
- Example 2: Compare fine-tuned vs baselines
- Example 3: TimeGPT not available (setup instructions)

---

## Troubleshooting

For common issues and solutions, see `resources/TROUBLESHOOTING.md`:
- Issue 1: Fine-tuning job fails immediately
- Issue 2: Data format errors
- Issue 3: Fine-tuning takes too long
- Issue 4: Fine-tuned model not better than zero-shot

---

## Advanced Features

For advanced fine-tuning configurations, see `resources/ADVANCED_FEATURES.md`:
- Advanced fine-tuning parameters (finetune_steps, finetune_loss)
- Multiple dataset handling
- Time-based vs percentage splits
- Custom validation strategies

---

## Best Practices

For workflow best practices, see `resources/BEST_PRACTICES.md`:
- Start with zero-shot baseline
- Use representative validation data
- Track fine-tuning experiments
- Version fine-tuned models
- Monitor production performance
- Cost awareness

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
