---
name: nixtla-explain-analyst
description: 'Analyze and explain TimeGPT forecast results in plain English. Generates
  executive summaries with driver analysis.

  Use when stakeholders need forecast explanations, board presentations, or compliance
  documentation.

  Trigger with "explain forecast", "why is the forecast", "forecast narrative".

  '
allowed-tools: Read,Glob,Grep
version: 1.1.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
compatible-with: claude-code
tags: [nixtla, timegpt, forecasting, explainability, reporting]
---

# Nixtla Explain Analyst

## Overview

Generate plain-English explanations of TimeGPT forecasts for non-technical stakeholders, with a short executive narrative plus driver-oriented analysis.

## Prerequisites

- A forecast output artifact to explain (CSV/JSON/markdown), or a path under the plugin workspace containing results.
- If using TimeGPT outputs: access to the TimeGPT run metadata used to generate the forecast.

## Instructions

1. Locate the forecast results file(s) and any run metadata (model, horizon, frequency, training window).
2. Summarize forecast context: what is being forecast, horizon, and any known events/holidays/regressors.
3. Explain forecast shape using: baseline level, trend direction, seasonal pattern (if present), and uncertainty.
4. Provide driver analysis at the level supported by available data. Do not fabricate causal drivers — restrict to observable signals.
5. Produce a stakeholder-ready narrative plus a short technical appendix (assumptions + limitations).
6. Validate output by cross-referencing stated metrics against source data. Flag any discrepancies.

## Output

Select the output format that matches the audience:
- **Executive**: 1-page summary for C-level (default)
- **Technical**: Detailed analysis for data science teams
- **Compliance**: SOX/Basel III documentation format

## Error Handling

- If only point forecasts are available, state that uncertainty intervals are unavailable and recommend generating prediction intervals.
- If inputs are missing (no horizon/freq), request the minimum details required to interpret results.
- If drivers/regressors are not provided, restrict “drivers” to observable components (trend/seasonality/outliers).

## Examples

**User**: “Explain the Q4 forecast for the board presentation.”

**Response structure**:
- Executive summary (3–6 bullets)
- What changed vs last quarter (trend/seasonality)
- Key risks and uncertainty
- Assumptions and limitations (what was/wasn’t modeled)

## Resources

- Plugin docs and outputs under `005-plugins/nixtla-forecast-explainer/`
- TimeGPT API docs: https://docs.nixtla.io/docs/getting-started-timegpt
- Nixtla forecast explanation guide: https://docs.nixtla.io/
