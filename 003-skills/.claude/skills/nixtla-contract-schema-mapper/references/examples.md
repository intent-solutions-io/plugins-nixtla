## Examples

### Example 1: Basic Transformation

```bash
python {baseDir}/scripts/transform_data.py \
    --input polymarket_prices.csv \
    --id_col market_id \
    --date_col timestamp \
    --target_col last_price
```

**Output**:
```
Transformed data saved to: nixtla_data.csv

Transformation Summary:
  Series count: 15
  Total rows: 4500
  Date range: 2024-01-01 to 2024-06-30
  Value range: 0.0100 to 0.9900
```

### Example 2: With Visualization and Forecast

```bash
python {baseDir}/scripts/transform_data.py \
    --input election_contracts.csv \
    --id_col candidate_id \
    --date_col date \
    --target_col probability \
    --plot \
    --forecast
```
