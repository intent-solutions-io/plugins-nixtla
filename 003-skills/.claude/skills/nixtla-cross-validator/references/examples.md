## Examples

### Example 1: Cross-validating TimeGPT on daily sales

**Input**:
```csv
unique_id,ds,y
store_1,2023-01-01,10
store_1,2023-01-02,12
store_1,2023-01-03,15
...
store_1,2023-12-31,20
```

**Command**:
```bash
python {baseDir}/scripts/cross_validate.py \
  --input sales.csv \
  --model timegpt \
  --window 30 \
  --folds 4 \
  --freq D
```

**Output**:
```csv
fold,unique_id,ds,y,y_hat
1,store_1,2023-11-01,18,17.5
1,store_1,2023-11-02,20,19.2
...
```

### Example 2: Cross-validating ARIMA on monthly demand

**Input**:
```csv
unique_id,ds,y
product_1,2020-01-01,100
product_1,2020-02-01,110
...
product_1,2023-12-01,125
```

**Command**:
```bash
python {baseDir}/scripts/cross_validate.py \
  --input demand.csv \
  --model arima \
  --window 6 \
  --folds 3 \
  --freq M
```

**Output**:
```json
{
 "MAE": 5.2,
 "RMSE": 7.1
}
```
