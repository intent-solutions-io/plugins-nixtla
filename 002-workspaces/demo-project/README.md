# Nixtla Skills Pack - Demo Project

**End-to-end demonstration of Nixtla Claude Skills in action**

This minimal project demonstrates how the Nixtla Skills Pack accelerates forecasting workflows from data preparation through production deployment.

---

## What This Demo Shows

This demo simulates a real forecasting project:

1. **Data**: M4 Daily subset (5 series, 90 days history)
2. **Experiment**: Compare TimeGPT vs StatsForecast baselines
3. **Configuration**: Nixtla-standard `config.yml`
4. **Skills Integration**: How skills guide the workflow

**End-to-end flow**: Data → Experiment Setup → Forecasting → Results → Production Pipeline

---

## Quick Start

### 1. Install Nixtla Skills

```bash
# From repository root
cd packages/nixtla-claude-skills-installer
pip install -e .

# Install skills in this demo project
cd ../../demo-project
nixtla-skills init
```

### 2. Install Dependencies

```bash
pip install statsforecast nixtla pandas pyyaml

# Optional: Set TimeGPT API key for full demo
export NIXTLA_API_KEY='your-api-key-here'
```

### 3. Run Demo Experiment

```bash
python forecasting/run_experiment.py
```

**Expected output**:
```
Running M4 Daily Forecasting Experiment
=====================================

Loading data...
✓ Loaded 5 series, 90 days history

Running forecasts...
✓ StatsForecast AutoETS: SMAPE 12.3%
✓ StatsForecast SeasonalNaive: SMAPE 18.7%
(✓ TimeGPT: SMAPE 9.2% - if API key configured)

Best model: TimeGPT (9.2% SMAPE)
Saved results: forecasting/results/comparison.csv
```

---

## How Nixtla Skills Accelerate This Workflow

### Skill 1: nixtla-schema-mapper
**Without skill**: Manually write CSV parsing code  
**With skill**: "Map this CSV to Nixtla format" → generates transformation script

### Skill 2: nixtla-experiment-architect
**Without skill**: Write experiment harness from scratch  
**With skill**: "Set up forecasting experiment" → scaffolds config.yml and run_experiment.py

### Skill 3: nixtla-timegpt-lab (Mode Skill)
**Without skill**: Look up TimeGPT docs  
**With skill**: Ask questions in Nixtla-native language, get instant expert guidance

### Skill 4: nixtla-prod-pipeline-generator
**Without skill**: Write Airflow DAG from scratch  
**With skill**: "Turn this into production pipeline" → generates full Airflow DAG

---

## Demo Data

Sample: 5 M4 daily series, 90 days history, Nixtla format (unique_id, ds, y)

---

**Demo Version**: 0.4.0  
**Generated**: 2025-12-03 (Phase 4)
