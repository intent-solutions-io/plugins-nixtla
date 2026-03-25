## Examples

### Example 1: Holiday impact on sales

**Input (data.csv)**:
```csv
unique_id,ds,y
store_1,2024-01-01,100
store_1,2024-01-02,120
store_1,2024-01-03,115
```

**Input (holidays.csv)**:
```csv
ds,holiday
2024-01-01,1
2024-01-02,0
2024-01-03,0
2024-01-04,0
```

**Command**:
```bash
python {baseDir}/scripts/integrate_exogenous.py \
  --input data.csv \
  --exogenous holidays.csv \
  --horizon 7 \
  --freq D
```

**Output (forecast_exogenous.csv)**:
```csv
unique_id,ds,TimeGPT,TimeGPT-lo-90,TimeGPT-hi-90
store_1,2024-01-04,125,110,140
store_1,2024-01-05,128,113,143
```

### Example 2: Weather affecting demand

**Input (data.csv)**:
```csv
unique_id,ds,y
grid_1,2024-01-01 00:00,5000
grid_1,2024-01-01 01:00,5100
```

**Input (weather.csv)**:
```csv
ds,temperature
2024-01-01 00:00,10
2024-01-01 01:00,8
2024-01-01 02:00,7
```

**Command**:
```bash
python {baseDir}/scripts/integrate_exogenous.py \
  --input data.csv \
  --exogenous weather.csv \
  --horizon 24 \
  --freq H
```

**Output**: Hourly forecast incorporating temperature trends.
