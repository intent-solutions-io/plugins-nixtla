---
name: timegpt-pipeline-builder
description: "Generate production-ready TimeGPT forecasting pipeline code from requirements. Use when scaffolding a pipeline with validation, logging, visualization, and repeatable runs. Trigger with \"create TimeGPT pipeline\", \"build TimeGPT integration\", or \"generate forecast code\"."
allowed-tools: Write,Read,Bash(python:*),Glob,Grep
version: 1.1.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
compatible-with: claude-code
tags: [nixtla, timegpt, pipeline, code-generation, forecasting]
---

# TimeGPT Pipeline Builder

## Overview

Generate a runnable, production-oriented pipeline skeleton (config, validation, forecasting call, output persistence, and optional plots) based on a short set of user requirements.

## Prerequisites

- A dataset source and schema (single-series or multi-series).
- A TimeGPT API key if the pipeline must run end-to-end against the API.

## Instructions

1. Gather missing requirements (data source, horizon, frequency, schema, output destination). See [requirements gathering](references/requirements-gathering.md) for the full checklist.
2. Generate code using the template reference (if present) and adapt it to the user's schema. See [code snippets](references/code-snippets.md) for template details and usage patterns.
3. Include setup/run instructions plus a short "customization points" checklist.

## Pipeline Components

Generate pipelines with these standard components:

1. **Setup and Imports** - All required libraries
2. **Configuration Management** - API keys, paths, parameters
3. **Data Loading and Validation** - CSV/database loading with validation
4. **TimeGPT Client Initialization** - Secure API key handling
5. **Forecasting Execution** - Core forecasting logic
6. **Results Processing** - Save and analyze results
7. **Visualization** - Optional plotting with confidence intervals
8. **Error Handling** - Try-except blocks with informative messages
9. **Logging** - Track pipeline execution for debugging

## Best Practices

1. **Error handling**: Try-except blocks with informative messages
2. **Logging**: Track pipeline execution for debugging
3. **Input validation**: Check data format, missing values, duplicates
4. **Type hints**: Make code maintainable
5. **Docstrings**: Explain function purpose and parameters
6. **PEP 8 compliance**: Clean, readable Python

## Output

- A complete Python module plus supporting files (`requirements.txt`, `.env.example`, minimal README instructions).

## Error Handling

- If credentials are missing, generate a pipeline that fails fast with a clear error and points to `.env.example`.
- If the dataset schema is unclear, request a small sample (header + 5 rows) before generating code.

## Examples

- "Create a TimeGPT pipeline for daily sales with 30-day horizon."
- "Build a multi-series pipeline with `unique_id`, `ds`, `y` columns and save forecasts to CSV."

## Resources

- Requirements gathering checklist: [requirements-gathering](references/requirements-gathering.md)
- Code snippets and template reference: [code-snippets](references/code-snippets.md)
- Prefer templates under `{baseDir}/assets/templates/` when available.
