# TimeGPT Fine-Tuning Usage Scenarios

## Scenario 1: Fine-Tune on Sales Data

**User request**: "I want to fine-tune TimeGPT on my sales data"

**Workflow**:

1. **Gather requirements**:
   ```
   Questions:
   1. Dataset path? → "data/sales.csv"
   2. Is it in Nixtla format (unique_id, ds, y)? → "No, needs transformation"
   3. Forecast horizon? → "14 days"
   4. Frequency? → "D" (daily)
   5. Fine-tune model name? → "sales-daily-v1"
   6. Train/validation split? → "Time-based: train on 2020-2023, validate on 2024"
   ```

2. **Transform data** (if needed):
   - Invoke `nixtla-schema-mapper` to transform data to Nixtla format
   - Validate required columns: `unique_id`, `ds`, `y`

3. **Extend config**:
   - Add `fine_tune:` section to `forecasting/config.yml`
   - Set model_name: "sales-daily-v1"
   - Configure time-based split

4. **Generate files**:
   - `forecasting/timegpt_finetune_job.py` - Fine-tuning job script
   - `forecasting/experiments.py` - Comparison experiments

5. **Run workflow**:
   ```bash
   python forecasting/timegpt_finetune_job.py
   python forecasting/experiments.py
   ```

**Expected output**:
- Fine-tuned model ID saved to artifacts
- Comparison table showing zero-shot vs fine-tuned vs baselines
- SMAPE/MASE/MAE metrics for each model

---

## Scenario 2: Compare Fine-Tuned vs Baselines

**User request**: "Compare my fine-tuned TimeGPT model with StatsForecast baselines"

**Workflow**:

1. **Check for existing fine-tuned model**:
   - Look for `forecasting/artifacts/timegpt_finetune/finetune_model_id.txt`
   - If not found, run fine-tuning first

2. **Load fine-tuned model ID**:
   ```python
   model_id = Path('forecasting/artifacts/timegpt_finetune/finetune_model_id.txt').read_text().strip()
   ```

3. **Run comparison experiments**:
   - TimeGPT zero-shot (baseline)
   - TimeGPT fine-tuned (using model_id)
   - AutoETS, AutoARIMA, AutoTheta

4. **Generate comparison table**:
   ```
   Model                   MAE    SMAPE    MASE
   ================================================
   TimeGPT Zero-Shot      0.452   12.3%   0.89
   TimeGPT Fine-Tuned     0.398   10.8%   0.76  ← Best
   AutoETS                0.512   14.1%   1.02
   AutoARIMA              0.489   13.5%   0.95
   AutoTheta              0.501   13.9%   0.98
   ```

5. **Interpret results**:
   - Fine-tuned model shows 12% improvement over zero-shot
   - Fine-tuned model outperforms all baselines
   - Recommendation: Use fine-tuned model for production

---

## Scenario 3: TimeGPT Not Available (Setup Mode)

**User request**: "Fine-tune TimeGPT on my data" (but `nixtla` package not installed)

**Workflow**:

1. **Detect missing dependencies**:
   ```python
   try:
       from nixtla import NixtlaClient
   except ImportError:
       timegpt_available = False
   ```

2. **Generate scaffold with TODOs**:
   ```python
   # TODO: Install nixtla package
   # pip install nixtla

   # TODO: Set your TimeGPT API key
   # export NIXTLA_API_KEY='your-api-key-here'
   # Get API key from: https://dashboard.nixtla.io
   ```

3. **Provide setup instructions**:
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

4. **Still generate all files**:
   - Create `config.yml` with fine-tune section
   - Create `timegpt_finetune_job.py` with TODOs and error handling
   - Create comparison script structure
   - User can complete setup and run later

**User experience**:
- Gets complete scaffold code immediately
- Clear setup instructions with links
- Can complete TODOs at their own pace
- No errors when running scripts (graceful degradation)

---

## Scenario 4: Multiple Series Fine-Tuning

**User request**: "Fine-tune TimeGPT on hierarchical sales data (multiple stores)"

**Workflow**:

1. **Validate data format**:
   ```python
   # Check for multiple unique_id values
   unique_ids = df['unique_id'].unique()
   print(f"Found {len(unique_ids)} series: {unique_ids}")
   ```

2. **Configure fine-tuning**:
   - Same workflow as single series
   - TimeGPT automatically handles multiple series
   - Ensure sufficient data per series (100+ observations recommended)

3. **Adjust validation strategy**:
   - Per-series validation
   - Aggregate metrics across all series
   - Identify best/worst performing series

4. **Generate comparison by series**:
   ```
   Series       Model                   MAE    SMAPE
   ===================================================
   store_001    TimeGPT Fine-Tuned     0.389   10.2%
   store_001    TimeGPT Zero-Shot      0.456   12.8%

   store_002    TimeGPT Fine-Tuned     0.412   11.1%
   store_002    TimeGPT Zero-Shot      0.501   13.9%
   ```

---

## Scenario 5: Cost-Benefit Analysis

**User request**: "Is fine-tuning worth it for my use case?"

**Decision framework**:

### Fine-tune when:
- Domain-specific data patterns (e.g., specialized industry)
- Zero-shot SMAPE > 15% (room for improvement)
- Have sufficient training data (100+ observations per series)
- Forecast accuracy directly impacts business value
- Budget allows for API costs

### Skip fine-tuning when:
- Zero-shot SMAPE < 10% (already excellent)
- Limited training data (< 100 observations)
- Simple seasonal patterns (StatsForecast sufficient)
- Cost-sensitive use cases
- Quick proof-of-concept needed

### Calculate ROI:

```python
# Fine-tuning costs
finetune_cost = 100  # API credits

# Inference costs
zeroshot_cost_per_call = 0.01
finetuned_cost_per_call = 0.015  # Usually slightly higher

# Forecast volume
calls_per_month = 1000

# Accuracy improvement value
# e.g., 10% SMAPE reduction = $500/month in better decisions
accuracy_value = 500

# ROI calculation
monthly_extra_cost = calls_per_month * (finetuned_cost_per_call - zeroshot_cost_per_call)
monthly_roi = accuracy_value - monthly_extra_cost - (finetune_cost / 12)
```

**Recommendation**:
- If `monthly_roi > 0`: Fine-tune is worthwhile
- If `monthly_roi < 0`: Use zero-shot or StatsForecast

---

## Scenario 6: Iterative Fine-Tuning

**User request**: "My fine-tuned model isn't better than zero-shot. What should I try?"

**Troubleshooting steps**:

1. **Check data quality**:
   - Sufficient volume? (100+ observations recommended)
   - Clean data? (no outliers, missing values)
   - Representative validation set?

2. **Adjust fine-tuning parameters**:
   ```yaml
   parameters:
     finetune_steps: 200  # Increase from 100
     finetune_loss: "mse"  # Try different loss function
   ```

3. **Try different validation splits**:
   - Time-based split (train on older data, validate on recent)
   - Ensure validation period has similar patterns to test period

4. **Compare metrics carefully**:
   - Is fine-tuned better on some metrics but not others?
   - Check per-series performance (may excel on some series)

5. **Consider alternatives**:
   - Maybe zero-shot is genuinely better for this dataset
   - StatsForecast baselines might be more appropriate
   - Data might not have learnable patterns beyond what zero-shot captures

**Example iteration**:
```
Iteration 1: finetune_steps=100, loss=mae → SMAPE: 12.8%
Iteration 2: finetune_steps=200, loss=mse → SMAPE: 11.5%  ← Better
Iteration 3: finetune_steps=300, loss=mse → SMAPE: 11.4%  ← Marginal
→ Use Iteration 2 (diminishing returns after 200 steps)
```
