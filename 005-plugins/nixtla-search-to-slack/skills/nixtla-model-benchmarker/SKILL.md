---
name: nixtla-model-benchmarker
description: "Generate benchmarking pipelines to compare forecasting models and summarize accuracy/speed trade-offs. Use when evaluating TimeGPT vs StatsForecast/MLForecast/NeuralForecast on a dataset. Trigger with \"benchmark models\", \"compare TimeGPT vs StatsForecast\", or \"model selection\"."
allowed-tools: Write,Read,Bash(python:*),Glob
version: 1.1.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
compatible-with: claude-code
tags: [nixtla, benchmarking, forecasting, model-selection, time-series]
---

# Nixtla Model Benchmarker

## Overview

Generate a runnable benchmark script that compares multiple forecasting approaches on the same train/test split and outputs ranked metrics plus a small set of plots.

## Prerequisites

- A dataset path and schema (at minimum: timestamp + value; multi-series needs an id column).
- Optional: an API key if benchmarking TimeGPT.

## Instructions

1. Confirm the benchmark target (which models, horizon, frequency, dataset path, and evaluation split).
2. Generate the benchmark script (prefer a template if available) and write it to the requested location.
3. Include clear run instructions and explain how to interpret results.

## Core Mission

Answer: **"Which Nixtla model is best for this data?"**

Compare across dimensions:
- **Accuracy**: MAE, RMSE, MAPE, SMAPE
- **Speed**: Training and inference time
- **Scalability**: Performance with large datasets
- **Interpretability**: Model explainability
- **Ease of use**: Setup and configuration complexity

For detailed model descriptions, see [models reference](references/models.md).

## Best Practices

1. **Fair comparison**: Use the same data split for all models
2. **Multiple metrics**: Avoid relying on a single accuracy measure
3. **Consider speed**: Training time matters in production
4. **Document trade-offs**: Explain pros/cons of each model
5. **Statistical significance**: Mention confidence intervals if possible
6. **Real-world context**: Consider deployment constraints (API costs, GPU requirements)
7. **Reproducibility**: Set random seeds for consistency
8. **Data requirements**: Ensure sufficient history for training (minimum 2x horizon)

## Output

- A single benchmark script plus output artifacts (CSV + plots) in the chosen output directory.

## Error Handling

- If required dependencies are missing, output the exact `pip install ...` command.
- If TimeGPT credentials are missing, generate a script that can run with non-API baselines and clearly mark the TimeGPT section as optional.

## Examples

- "Benchmark TimeGPT vs StatsForecast on this CSV and rank by sMAPE."
- "Create a comparison script for 30-day horizon daily data."

For full worked scenarios, see [scenarios reference](references/scenarios.md).

## Resources

- Code generation process and template details: [code-generation reference](references/code-generation.md)
- Model details (TimeGPT, StatsForecast, MLForecast, NeuralForecast): [models reference](references/models.md)
- User scenarios and example interactions: [scenarios reference](references/scenarios.md)
- Prefer templates under `{baseDir}/assets/templates/` for consistent benchmark structure.
