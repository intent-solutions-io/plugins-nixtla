---
name: nixtla-explain
description: Generate plain-English explanation of TimeGPT forecasts
---

# /nixtla-explain

Generate plain-English explanation of TimeGPT forecasts.

## Usage

```
/nixtla-explain [forecast_data] [--format=executive] [--output=pdf]
```

## Workflow

1. Load forecast results
2. Run STL decomposition
3. Identify trend/seasonal drivers
4. Calculate contribution percentages
5. Generate narrative explanation
6. Export report

## Parameters

- `forecast_data`: Path to forecast results
- `--format`: Report format (executive, technical, compliance)
- `--output`: Output type (pdf, html, pptx, md)
- `--audience`: Target audience for language level

## Output

- Plain-English explanation
- STL decomposition chart
- Driver contribution breakdown
- Risk factors and confidence
- Board-ready PDF/PPTX
