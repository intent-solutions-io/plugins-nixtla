---
name: nixtla-roi
description: Calculate TimeGPT ROI for enterprise customers
---

# /nixtla-roi

Calculate TimeGPT ROI for enterprise customers.

## Usage

```
/nixtla-roi
```

## Workflow

1. Gather current forecasting costs (tools, FTE, infrastructure)
2. Estimate TimeGPT usage based on volume
3. Calculate 3-year TCO comparison
4. Generate executive summary report

## Parameters

Interactive wizard collects:
- Current tool costs (Prophet, ARIMA, custom ML)
- Data scientist FTE allocation
- Infrastructure costs (compute, storage)
- Forecast volume (series × frequency)

## Output

- ROI percentage and payback period
- Executive PDF summary
- Detailed cost breakdown
- Salesforce-ready export
