## Examples

### Example 1: Significant MASE degradation detected

**Input** (historical_metrics.csv):
```
model,MASE,sMAPE
model_A,1.2,0.15
```

**Input** (current_metrics.csv):
```
model,MASE,sMAPE
model_A,1.8,0.18
```

**Command**:
```bash
python scripts/validate_forecast.py --historical historical_metrics.csv --current current_metrics.csv
```

**Output** (validation_report.txt):
```
WARNING: Significant increase in MASE detected for model model_A.
```

**Interpretation**: Model A shows 50% increase in MASE (from 1.2 to 1.8), exceeding the default 20% threshold. This indicates forecast quality degradation requiring investigation.

### Example 2: Stable performance, no alerts

**Input** (historical_metrics.csv):
```
model,MASE,sMAPE
model_B,0.8,0.10
```

**Input** (current_metrics.csv):
```
model,MASE,sMAPE
model_B,0.85,0.11
```

**Command**:
```bash
python scripts/validate_forecast.py --historical historical_metrics.csv --current current_metrics.csv
```

**Output** (validation_report.txt):
```
Forecast validation passed. No significant degradation detected.
```

**Interpretation**: Model B shows only 6.25% increase in MASE and 10% increase in sMAPE, both below the 20% threshold. Performance is stable.

### Example 3: Multiple models with custom thresholds

**Command**:
```bash
python scripts/validate_forecast.py \
  --historical multi_model_historical.csv \
  --current multi_model_current.csv \
  --mase_threshold 0.3 \
  --smape_threshold 0.25
```

Uses more lenient thresholds (30% for MASE, 25% for sMAPE) suitable for volatile forecasts or experimental models.
