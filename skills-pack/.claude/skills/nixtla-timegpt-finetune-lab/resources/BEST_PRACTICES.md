# TimeGPT Fine-Tuning Best Practices

## 1. Start with Zero-Shot Baseline

Always benchmark TimeGPT zero-shot before fine-tuning:
- Establishes performance floor
- Determines if fine-tuning is worth the effort
- Simple datasets may not need fine-tuning

## 2. Use Representative Validation Data

Fine-tuning quality depends on good train/val split:
- Time-based split (not random!) for time series
- Validation period should match production use case
- Include edge cases and seasonality patterns

## 3. Track Fine-Tuning Experiments

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

## 4. Version Your Fine-Tuned Models

Use descriptive model names with versions:
- ✅ `sales-daily-v1`, `sales-daily-v2`
- ❌ `model1`, `temp`, `final`

## 5. Monitor Production Performance

Fine-tuned models can drift over time:
- Regularly backtest on recent data
- Compare vs. baselines periodically
- Re-fine-tune when performance degrades

## 6. Cost Awareness

Fine-tuning and fine-tuned inference may have different pricing:
- Check TimeGPT pricing for fine-tuning jobs
- Compare cost vs. accuracy improvement
- Consider baselines for cost-sensitive use cases

## When to Use Fine-Tuning

✅ Use when:
- Domain-specific data patterns
- Need better accuracy than zero-shot
- Have sufficient training data (100+ observations)
- Cost justifies accuracy improvement

❌ Skip when:
- Zero-shot already meets requirements
- Limited training data
- Simple seasonal patterns (StatsForecast sufficient)
- Cost-sensitive use cases
