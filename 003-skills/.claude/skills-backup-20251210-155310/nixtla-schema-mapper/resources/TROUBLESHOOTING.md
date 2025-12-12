# Troubleshooting

Common issues and solutions for Nixtla schema mapping.

## Issue: "Cannot infer frequency"

**Solution**: Add explicit frequency to schema contract and transformation code.

## Issue: "Exogenous variables have different granularity"

**Example**: Daily sales but monthly promotions.

**Solution**: Forward-fill or interpolate:
```python
# Forward-fill monthly promotions to daily
df_nixtla['promotion'] = df_nixtla.groupby('unique_id')['promotion'].ffill()
```

## Issue: "Too many unique_id values (thousands)"

**Solution**: Filter or aggregate:
```python
# Keep only top 100 series by total sales
top_series = (
    df.groupby('unique_id')['y']
    .sum()
    .nlargest(100)
    .index
)
df_nixtla = df_nixtla[df_nixtla['unique_id'].isin(top_series)]
```
