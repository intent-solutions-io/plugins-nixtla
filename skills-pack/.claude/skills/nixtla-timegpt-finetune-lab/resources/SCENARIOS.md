# TimeGPT Fine-Tuning Scenarios

## Example 1: Fine-Tune on Sales Data

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

## Example 2: Compare Fine-Tuned vs Baselines

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

## Example 3: TimeGPT Not Available

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
