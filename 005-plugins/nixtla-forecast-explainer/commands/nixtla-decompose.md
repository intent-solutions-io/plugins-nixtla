# /nixtla-decompose

Run STL decomposition on time series data.

## Usage

```
/nixtla-decompose [data_path] [--period=7]
```

## Workflow

1. Load time series data
2. Run STL decomposition
3. Extract trend, seasonal, residual
4. Calculate component contributions
5. Generate visualization

## Parameters

- `data_path`: Path to time series CSV
- `--period`: Seasonal period (default: auto-detect)
- `--robust`: Use robust STL (default: true)

## Output

- Trend component
- Seasonal component
- Residual component
- Contribution percentages
- Visualization chart
