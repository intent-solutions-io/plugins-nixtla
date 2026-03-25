## Examples

### Example 1: Daily Sales Forecast

```bash
python {baseDir}/scripts/generate_config.py \
    --data data/sales.csv \
    --target revenue \
    --horizon 30 \
    --freq D \
    --id_col store_id
```

Generates a config.yml with SeasonalNaive, AutoETS, and AutoARIMA as default models.

### Example 2: Hourly Energy Forecast

```bash
python {baseDir}/scripts/generate_config.py \
    --data data/energy.csv \
    --target consumption \
    --horizon 24 \
    --freq H
```
