---
name: nixtla-explain-analyst
description: 'Analyze and explain TimeGPT forecast results in plain English. Generates
  executive summaries with driver analysis.

  Use when stakeholders need forecast explanations, board presentations, or compliance
  documentation.

  Trigger with "explain forecast", "why is the forecast", "forecast narrative".

  '
allowed-tools: Read,Glob,Grep
version: 1.0.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
---

# Nixtla Explain Analyst

## Purpose

Generate plain-English explanations of TimeGPT forecasts for non-technical stakeholders.

## Capabilities

1. **STL Decomposition**: Break forecasts into trend, seasonal, residual
2. **Driver Analysis**: Identify and quantify forecast drivers
3. **Narrative Generation**: Create executive summaries
4. **Report Export**: PDF, HTML, PowerPoint formats

## Instructions

1. Load the forecast data from the specified path
2. Run STL decomposition to identify components
3. Calculate driver contributions
4. Generate appropriate narrative for audience
5. Export report in requested format

## Output Formats

- **Executive**: 1-page summary for C-level
- **Technical**: Detailed analysis for data science
- **Compliance**: SOX/Basel III documentation

## Example

```
User: Explain the Q4 forecast for the board presentation