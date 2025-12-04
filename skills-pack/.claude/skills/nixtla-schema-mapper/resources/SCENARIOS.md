# Common Scenarios

Real-world scenario patterns for Nixtla schema mapping.

## Scenario 1: Single Time Series (No unique_id)

**User**: "My CSV has just date and sales, no store IDs"

**Your response**:
```python
# For single series, create dummy unique_id
df_nixtla['unique_id'] = 'series_1'
df_nixtla['ds'] = pd.to_datetime(df['date'])
df_nixtla['y'] = df['sales']
```

## Scenario 2: Multiple ID Columns

**User**: "I have store_id AND product_id"

**Your response**:
```python
# Combine multiple IDs into single unique_id
df_nixtla['unique_id'] = (
    df['store_id'].astype(str) + '_' + df['product_id'].astype(str)
)
# Result: "store_1_product_A", "store_1_product_B", etc.
```

## Scenario 3: Timestamp in Multiple Columns

**User**: "Date is split across year, month, day columns"

**Your response**:
```python
# Combine into single timestamp
df_nixtla['ds'] = pd.to_datetime({
    'year': df['year'],
    'month': df['month'],
    'day': df['day']
})
```

## Scenario 4: Hierarchical Data

**User**: "I have national → regional → store hierarchy"

**Your response**:
```python
# Create separate series for each level
df_national = df.groupby('date').agg({'sales': 'sum'}).reset_index()
df_national['unique_id'] = 'national'

df_regional = df.groupby(['region', 'date']).agg({'sales': 'sum'}).reset_index()
df_regional['unique_id'] = 'region_' + df_regional['region']

df_store = df.copy()
df_store['unique_id'] = 'store_' + df_store['store_id']

# Combine all levels
df_nixtla = pd.concat([df_national, df_regional, df_store], ignore_index=True)
df_nixtla = df_nixtla.rename(columns={'date': 'ds', 'sales': 'y'})
```
