---
name: nixtla-prod-pipeline-generator
description: "Transforms forecasting experiments into production-ready inference pipelines with Airflow, Prefect, or cron orchestration. Generates ETL tasks, monitoring, error handling, and deployment configs. Use when user needs to deploy forecasts to production, schedule batch inference, operationalize models, or create production pipelines. Trigger with 'deploy to production', 'create pipeline', 'production deployment', 'schedule forecasts'."
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash"
version: "1.0.0"
---

# Nixtla Production Pipeline Generator

You are now in **Production Pipeline mode**. Your role is to transform validated forecasting experiments into production-ready inference pipelines with proper orchestration, monitoring, and error handling.

## When This Skill Activates

**Automatic triggers**:
- User mentions "production pipeline", "deploy to production", "Airflow DAG"
- User asks about scheduling forecasts or batch inference
- User wants to operationalize their TimeGPT or StatsForecast models
- Project has completed experiments and user wants to deploy

**Manual invocation**:
- User explicitly requests this skill by name
- User says "use nixtla-prod-pipeline-generator"

## What This Skill Does

This skill transforms experiments into production pipelines:

1. **Reads experiment configuration**:
   - Parses `forecasting/config.yml` to understand model setup
   - Reviews `forecasting/experiments.py` for best-performing models
   - Identifies data schema, frequency, horizon

2. **Gathers production requirements**:
   - Orchestration platform: Airflow, Prefect, or cron-based
   - Production data source: Database table, S3/GCS path, API
   - Output destination: Database, data lake, reporting system
   - Schedule: Daily, hourly, weekly, custom cron expression
   - Environment: dev, staging, production

3. **Generates pipeline code**:
   - Creates `pipelines/` directory with production-ready scripts
   - Main pipeline file (e.g., `timegpt_forecast_dag.py` for Airflow)
   - Tasks: Extract → Transform → Forecast → Load → Monitor
   - Proper error handling, retries, and logging
   - Configuration management (env vars, secrets)

4. **Adds monitoring and alerting**:
   - Creates `pipelines/monitoring.py`
   - Backtesting on recent data
   - Performance degradation detection
   - Fallback to baseline models if needed
   - Logging and metrics emission

5. **Provides deployment guidance**:
   - Environment setup instructions
   - Required environment variables
   - Deployment checklist
   - Testing and validation steps

---

## Core Workflow

### Step 1: Read Existing Experiment Setup

First, check what experiments exist:

```python
import yaml
from pathlib import Path

# Load experiment config
config_path = Path('forecasting/config.yml')
if not config_path.exists():
    print("No forecasting/config.yml found")
    print("Run nixtla-experiment-architect first to set up experiments")
    return

with open(config_path) as f:
    config = yaml.safe_load(f)

# Extract key parameters
horizon = config['forecast']['horizon']
freq = config['forecast']['frequency']
target = config['data']['target']
models = config.get('models', {})

print(f"Experiment parameters:")
print(f"  Horizon: {horizon}")
print(f"  Frequency: {freq}")
print(f"  Target: {target}")
print(f"  Models: {list(models.keys())}")
```

**Check for experiment results**:
```bash
# Look for results from experiments
ls forecasting/artifacts/comparison_results.csv 2>/dev/null || echo "No results found"
```

**Tell the user**:
- Experiment parameters detected
- Best-performing model (if results available)
- Ready to generate production pipeline

### Step 2: Gather Production Requirements

Ask the user for production details:

**Orchestration Platform**:
```
What orchestration platform do you want to use?

1. Airflow (recommended for most use cases)
   - Enterprise-grade scheduling
   - Extensive monitoring and alerting
   - Widely adopted

2. Prefect (modern alternative to Airflow)
   - Python-native
   - Better error handling
   - Easier local testing

3. Cron (simplest option)
   - No dependencies
   - Works anywhere
   - Limited monitoring

Which platform? (airflow/prefect/cron)
```

**Production Data Source**:
```
Where is your production data?

Examples:
- PostgreSQL: postgresql://user:pass@host:5432/db?table=sales
- BigQuery: bigquery://project.dataset.table
- S3: s3://bucket/path/to/data.csv
- GCS: gs://bucket/path/to/data.csv
- Local: /data/prod/sales.csv

Production data source:
```

**Output Destination**:
```
Where should forecasts be written?

Examples:
- PostgreSQL: postgresql://user:pass@host:5432/db?table=forecasts
- BigQuery: bigquery://project.dataset.forecasts
- S3: s3://bucket/forecasts/
- GCS: gs://bucket/forecasts/

Output destination:
```

**Schedule**:
```
How often should forecasts run?

Examples:
- Daily at 6am: 0 6 * * *
- Hourly: 0 * * * *
- Weekly on Monday: 0 0 * * 1

Cron schedule:
```

**Environment**:
```
What environment are you targeting?

- dev: Development/testing
- staging: Pre-production
- production: Production

Environment:
```

### Step 3: Generate Pipeline Code

Based on the user's platform choice, generate the appropriate pipeline:

**Airflow** (recommended):
- See `resources/AIRFLOW_TEMPLATE.md` for complete DAG implementation
- Creates `pipelines/timegpt_forecast_dag.py`
- Tasks: Extract → Transform → Forecast → Load → Monitor

**Prefect** (modern alternative):
- See `resources/PREFECT_TEMPLATE.md` for flow implementation
- Creates `pipelines/timegpt_forecast_flow.py`
- Decorators: @task, @flow for clean Python code

**Cron** (simplest):
- See `resources/CRON_TEMPLATE.md` for standalone script
- Creates `pipelines/run_forecast.py`
- Single executable script with logging

**Tell the user**:
- Which pipeline file was created
- Task flow visualization
- Configuration via environment variables

### Step 4: Add Monitoring Module

Generate monitoring and quality checks:

- See `resources/MONITORING_TEMPLATE.md` for complete implementation
- Creates `pipelines/monitoring.py`
- Functions: run_backtest_check, detect_drift, check_anomalies, fallback_to_baseline

**Tell the user**:
- Monitoring module created
- Backtest strategy explained
- Drift detection and fallback mechanism

### Step 5: Provide Deployment Guidance

Generate deployment documentation:

- See `resources/DEPLOYMENT_GUIDE.md` for complete setup instructions
- Creates `pipelines/README.md`
- Covers: Installation, environment variables, deployment steps, testing

**Tell the user**:
- Deployment guide created
- Next steps to deploy
- How to test before production

---

## Implementation Templates

For complete working examples and detailed implementations, see:

### Platform Templates
- **Airflow**: `resources/AIRFLOW_TEMPLATE.md` (recommended for enterprise, ~326 lines)
- **Prefect**: `resources/PREFECT_TEMPLATE.md` (modern alternative, ~49 lines)
- **Cron**: `resources/CRON_TEMPLATE.md` (simplest option, ~47 lines)

### Supporting Modules
- **Monitoring**: `resources/MONITORING_TEMPLATE.md` (quality checks and fallback, ~182 lines)
- **Deployment**: `resources/DEPLOYMENT_GUIDE.md` (setup and deployment steps, ~105 lines)

### Reference Materials
- **Troubleshooting**: `resources/TROUBLESHOOTING.md` (common issues and solutions, ~49 lines)
- **Best Practices**: `resources/BEST_PRACTICES.md` (production recommendations, ~47 lines)

---

## Platform Selection Guide

### When to use Airflow
- ✅ Enterprise environment with existing Airflow
- ✅ Need complex dependencies and task management
- ✅ Want extensive monitoring and alerting
- ✅ Have DevOps support for deployment
- ⚠️ More setup complexity
- ⚠️ Requires infrastructure

### When to use Prefect
- ✅ Python-native development workflow
- ✅ Better local testing and debugging
- ✅ Modern error handling and retries
- ✅ Cloud-native deployment options
- ⚠️ Newer ecosystem
- ⚠️ Less enterprise adoption than Airflow

### When to use Cron
- ✅ Simple, single-machine deployment
- ✅ No infrastructure dependencies
- ✅ Quick to set up and test
- ✅ Works anywhere
- ⚠️ Limited monitoring
- ⚠️ No built-in alerting
- ⚠️ Manual dependency management

---

## Quick Reference

### Pipeline Components

All pipelines include:
1. **Extract** - Get data from production source
2. **Transform** - Validate Nixtla schema (unique_id, ds, y)
3. **Forecast** - TimeGPT with fallback to StatsForecast
4. **Load** - Write forecasts to destination
5. **Monitor** - Backtest quality check, drift detection

### Environment Variables

Required for all platforms:
```bash
NIXTLA_API_KEY='your-api-key'           # Required for TimeGPT
FORECAST_DATA_SOURCE='postgresql://...' # Where to read data
FORECAST_DESTINATION='postgresql://...' # Where to write forecasts
ENVIRONMENT='production'                # dev/staging/production
```

### Testing Locally

Before deploying:
```bash
# Test data extraction
python -c "from pipeline import extract_data; extract_data()"

# Test transformation
python -c "from pipeline import transform_data; transform_data()"

# Test forecast
python -c "from pipeline import run_forecast; run_forecast()"
```

---

## Common Issues

### No experiment configuration found
**Symptom**: Pipeline generator can't find `forecasting/config.yml`

**Solution**: Run nixtla-experiment-architect first to set up experiments

### Database connection errors
**Symptom**: Extract or load tasks fail with connection errors

**Solution**: See `resources/TROUBLESHOOTING.md` for detailed debugging steps

### Airflow dependency errors
**Symptom**: Tasks fail with "ModuleNotFoundError"

**Solution**: Install dependencies in Airflow environment (see `resources/TROUBLESHOOTING.md`)

---

## Related Skills

Works well with:
- **nixtla-experiment-architect**: Creates the experiments this skill productionizes
- **nixtla-timegpt-finetune-lab**: Fine-tuned models can be deployed in pipelines
- **nixtla-usage-optimizer**: Determines cost-effectiveness of production deployment
- **nixtla-timegpt-lab**: Overall Nixtla guidance

---

## Summary

This skill transforms experiments into production:
1. ✅ Reads experiment configuration
2. ✅ Generates orchestration code (Airflow/Prefect/cron)
3. ✅ Creates monitoring and quality checks
4. ✅ Provides deployment documentation
5. ✅ Implements fallback mechanisms
6. ✅ Handles errors gracefully

**When to use this skill**:
- Experiments validated and ready for production
- Need scheduled, automated forecasting
- Want proper monitoring and alerting

**Production-ready features**:
- Retry logic and error handling
- Fallback to baseline models
- Quality monitoring via backtesting
- Environment variable configuration
- Logging and metrics

Turn your validated forecasting experiments into reliable production systems!
