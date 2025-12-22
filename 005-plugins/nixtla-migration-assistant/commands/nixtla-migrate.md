---
name: nixtla-migrate
description: Migrate legacy forecasting code to Nixtla
---

# /nixtla-migrate

Migrate legacy forecasting code to Nixtla.

## Usage

```
/nixtla-migrate [source_path] [--target=timegpt] [--execute]
```

## Workflow

1. Analyze source code (AST parsing)
2. Detect library patterns (Prophet, statsmodels)
3. Generate migration plan
4. Transform data format
5. Generate Nixtla equivalent code
6. Run accuracy comparison
7. Execute migration (optional)

## Parameters

- `source_path`: Path to legacy forecasting code
- `--target`: Target library (timegpt, statsforecast)
- `--analyze-only`: Only analyze, no code generation
- `--execute`: Apply changes (default: dry-run)

## Supported Sources

- Prophet
- statsmodels (ARIMA, ETS)
- sklearn time series
- pandas rolling forecasts

## Output

- Migration analysis report
- Generated Nixtla code
- Accuracy comparison
- Rollback instructions
