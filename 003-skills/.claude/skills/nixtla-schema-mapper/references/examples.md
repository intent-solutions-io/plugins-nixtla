## Examples

### Example 1: CSV Transformation

```bash
python {baseDir}/scripts/generate_transform.py \
    --input sales.csv \
    --id_col product_id \
    --date_col timestamp \
    --target_col revenue
```

**Generated code**:
```python
def to_nixtla_schema(path="sales.csv"):
    df = pd.read_csv(path)
    df = df.rename(columns={
        'product_id': 'unique_id',
        'timestamp': 'ds',
        'revenue': 'y'
    })
    df['ds'] = pd.to_datetime(df['ds'])
    return df[['unique_id', 'ds', 'y']]
```

### Example 2: SQL Source

```bash
python {baseDir}/scripts/generate_transform.py \
    --sql "SELECT * FROM daily_sales" \
    --connection postgresql://localhost/db \
    --id_col store_id \
    --date_col sale_date \
    --target_col amount
```
