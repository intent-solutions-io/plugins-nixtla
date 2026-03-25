## Error Handling

**Error: Input file not found**
- Verify file path with `ls -la`
- Check current directory and use absolute paths

**Error: Missing required columns**
- Ensure CSV has `unique_id`, `ds`, `y` columns
- Verify column names match exactly (case-sensitive)

**Error: Insufficient data points**
- Need at least 30 data points per contract for reliable correlations
- Verify data has sufficient time-series history

**Error: Invalid data format**
- Check that `y` values are numeric (not strings)
- Ensure dates are parseable (ISO format recommended)
- Remove or handle missing values

**Error: Insufficient contracts**
- Need at least 2 contracts for correlation analysis
- Verify `unique_id` column has multiple distinct values
