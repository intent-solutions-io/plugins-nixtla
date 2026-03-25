## Examples

### Example 1: Forecast 50 Daily Contracts

```bash
python {baseDir}/scripts/batch_forecast.py contracts.csv \
    --horizon 14 \
    --freq D \
    --batch-size 10 \
    --output-dir forecasts/
```

**Output**:
```
Batch Forecast Complete
Series forecasted: 50/50
Success rate: 100.0%
```

### Example 2: Hourly Portfolio with Aggregation

```bash
python {baseDir}/scripts/batch_forecast.py portfolio.csv \
    --horizon 24 \
    --freq H \
    --aggregate \
    --output-dir portfolio_forecasts/
```
