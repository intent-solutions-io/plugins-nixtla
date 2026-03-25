# Model Selector Examples

## Example 1: Short Seasonal Data

**Input** (7 observations):
```csv
unique_id,ds,y
product_1,2023-01-01,10
product_1,2023-01-02,12
product_1,2023-01-03,15
product_1,2023-01-04,13
product_1,2023-01-05,16
product_1,2023-01-06,18
product_1,2023-01-07,20
```

**Command**: `{baseDir}/scripts/model_selector.py --input short_data.csv`

**Output**:
- **model_selection.txt**: "StatsForecast selected due to short data length (<30 observations)."
- **forecast.csv**: 14-period forecasts from AutoETS and AutoARIMA

## Example 2: Long Non-Seasonal Data

**Input** (365+ observations):
```csv
unique_id,ds,y
location_1,2020-01-01,100
location_1,2020-01-02,102
location_1,2020-01-03,105
... (365+ rows)
```

**Command**: `{baseDir}/scripts/model_selector.py --input long_data.csv --horizon 30 --visualize`

**Output**:
- **model_selection.txt**: "TimeGPT selected due to long data length and lack of clear seasonality."
- **forecast.csv**: 30-period TimeGPT forecasts
- **time_series_plot.png**: Input data visualization

## Example 3: Multi-Series Data with Missing Values

**Input** (multiple series with gaps):
```csv
unique_id,ds,y
store_1,2023-01-01,100
store_1,2023-01-02,
store_1,2023-01-03,105
store_2,2023-01-01,200
store_2,2023-01-02,210
store_2,2023-01-03,205
```

**Command**: `{baseDir}/scripts/model_selector.py --input multi_series.csv --horizon 7`

**Output**:
- **model_selection.txt**: "StatsForecast selected due to missing values detected in target variable."
- **forecast.csv**: 7-period forecasts for each series using AutoETS and AutoARIMA
