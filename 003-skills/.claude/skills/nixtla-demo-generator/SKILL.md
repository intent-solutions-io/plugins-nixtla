---
name: nixtla-demo-generator
description: "Generate production-ready Jupyter notebooks showcasing Nixtla forecasting workflows for statsforecast, mlforecast, and TimeGPT. Use when creating demos, building examples, or showcasing forecasting capabilities. Trigger with 'generate demo notebook', 'create Jupyter demo', or 'build forecasting example'."
allowed-tools: "Write,Read,Glob,Bash(python:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, jupyter, demo]
---

# Nixtla Demo Generator

Generate interactive, production-ready Jupyter notebooks that showcase Nixtla forecasting workflows with complete data pipelines, model training, evaluation, and visualization.

## Overview

This skill creates high-quality demonstration notebooks:

- **Three library support**: StatsForecast, MLForecast, TimeGPT
- **Complete workflows**: Data loading, preprocessing, model training, forecasting, evaluation, visualization
- **Production patterns**: Best practices, error handling, performance optimization
- **Instant demos**: Ready for Nixtla CEO presentations, customer POCs, and documentation
- **Customizable templates**: Modify for specific use cases and datasets

## Prerequisites

**Required**:
- Python 3.8+
- Jupyter notebook (`pip install jupyter`)
- At least one Nixtla library:
  - `statsforecast` - Statistical models (ARIMA, ETS, etc.)
  - `mlforecast` - Machine learning models (LightGBM, XGBoost)
  - `nixtla` - TimeGPT API access

**Optional**:
- `NIXTLA_API_KEY`: For TimeGPT demos
- Sample datasets (M4, custom time series)

**Installation**:
```bash
pip install jupyter statsforecast mlforecast nixtla pandas matplotlib
```

## Instructions

### Step 1: Choose Library

Select which Nixtla library to demonstrate:
```bash
# Options: statsforecast, mlforecast, timegpt
export DEMO_LIBRARY=statsforecast
```

### Step 2: Generate Notebook

Run the generator script:
```bash
python {baseDir}/scripts/generate_demo_notebook.py \
    --library statsforecast \
    --dataset m4-daily \
    --output demo_statsforecast_m4.ipynb
```

### Step 3: Customize (Optional)

Edit the generated notebook to:
- Add custom datasets
- Modify model configurations
- Adjust visualizations
- Include domain-specific context

### Step 4: Execute Notebook

Run the generated notebook:
```bash
jupyter notebook demo_statsforecast_m4.ipynb
```

Or execute non-interactively:
```bash
jupyter nbconvert --to notebook --execute demo_statsforecast_m4.ipynb
```

### Step 5: Export Results

Export to various formats:
```bash
# HTML for sharing
jupyter nbconvert --to html demo_statsforecast_m4.ipynb

# PDF for presentations
jupyter nbconvert --to pdf demo_statsforecast_m4.ipynb

# Python script for automation
jupyter nbconvert --to python demo_statsforecast_m4.ipynb
```

## Output

- **[library]_demo.ipynb**: Complete Jupyter notebook with:
  - Introduction and setup
  - Data loading and exploration
  - Model configuration
  - Training and forecasting
  - Evaluation metrics (SMAPE, MASE, MAE)
  - Visualizations (forecasts, residuals, comparisons)
  - Next steps and resources

## Error Handling

1. **Error**: `ModuleNotFoundError: No module named 'statsforecast'`
   **Solution**: Install required library: `pip install statsforecast mlforecast nixtla`

2. **Error**: `NIXTLA_API_KEY not set` (TimeGPT demos)
   **Solution**: Export API key: `export NIXTLA_API_KEY=your_key` or skip TimeGPT demo

3. **Error**: `Dataset file not found`
   **Solution**: Use `--generate-sample-data` flag to create synthetic dataset

4. **Error**: `nbformat.validator.ValidationError`
   **Solution**: Check Jupyter version compatibility: `pip install --upgrade jupyter nbformat`

5. **Error**: `Kernel died while executing notebook`
   **Solution**: Reduce dataset size or increase memory allocation

## Examples

See [examples](references/examples.md) for detailed usage patterns.

## Resources

- **StatsForecast Docs**: https://nixtla.github.io/statsforecast/
- **MLForecast Docs**: https://nixtla.github.io/mlforecast/
- **TimeGPT Docs**: https://docs.nixtla.io/
- **Jupyter Tutorial**: https://jupyter.org/try
- **M4 Competition**: https://github.com/Mcompetitions/M4-methods

**Related Skills**:
- `nixtla-timegpt-lab`: Interactive TimeGPT experimentation
- `nixtla-experiment-architect`: Multi-model experiment design
- `nixtla-schema-mapper`: Data transformation for Nixtla format

**Scripts**:
- `{baseDir}/scripts/generate_demo_notebook.py`: Main notebook generator
- `{baseDir}/assets/templates/statsforecast_template.ipynb`: StatsForecast base template
- `{baseDir}/assets/templates/mlforecast_template.ipynb`: MLForecast base template
- `{baseDir}/assets/templates/timegpt_template.ipynb`: TimeGPT base template
