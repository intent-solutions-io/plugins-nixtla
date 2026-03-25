## Examples

### Example 1: Detect outliers in website traffic

**Input** (`traffic.csv`):
```csv
unique_id,ds,y
website_1,2024-01-01,1000
website_1,2024-01-02,1050
website_1,2024-01-03,300
website_1,2024-01-04,980
```

**Command**:
```bash
python {baseDir}/scripts/detect_anomalies.py --input traffic.csv
```

**Output** (anomalies.csv):
```csv
unique_id,ds,y,anomaly_type
website_1,2024-01-03,300,outlier
```

### Example 2: Identify trend break in sales data

**Input** (`sales.csv`):
```csv
unique_id,ds,y
store_1,2023-12-28,50
store_1,2023-12-29,55
store_1,2023-12-30,60
store_1,2023-12-31,150
store_1,2024-01-01,145
```

**Command**:
```bash
python {baseDir}/scripts/detect_anomalies.py -i sales.csv -o sales_anomalies.csv
```

**Output**: Detects trend break at 2023-12-31
