# Troubleshooting

Common issues and solutions for Nixtla experiment setup.

## Issue: "Frequency cannot be inferred"

**Solution**: Explicitly set `freq` in config.yml:
```yaml
forecast:
  freq: "D"  # Daily, or "H", "M", "W", etc.
```

## Issue: "Seasonal length too large"

**Solution**: Reduce `season_length` to match available data:
```yaml
forecast:
  season_length: 7  # For weekly pattern (not 365 for yearly)
```

## Issue: Cross-validation fails with "Not enough data"

**Solution**: Reduce `n_windows` or increase `step_size`:
```yaml
cv:
  n_windows: 2       # Fewer windows
  step_size: 14      # Larger steps
```

## Issue: "No module named 'statsforecast'"

**Solution**: Add installation instructions to experiments.py:
```python
"""
Install required packages:
    pip install statsforecast mlforecast nixtla utilsforecast pyyaml
"""
```
