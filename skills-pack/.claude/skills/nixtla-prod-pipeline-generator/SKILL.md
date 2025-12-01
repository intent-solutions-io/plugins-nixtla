---
name: nixtla-prod-pipeline-generator
description: "Transform experiment workflows into production-ready inference pipelines with orchestration"
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

## Core Behavior

### 1. Read Existing Experiment Setup

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

### 2. Gather Production Requirements

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

### 3. Generate Airflow DAG (Primary Implementation)

If user chooses Airflow, create `pipelines/timegpt_forecast_dag.py`:

```python
"""
TimeGPT Production Forecasting DAG

This DAG:
1. Extracts production data from source
2. Transforms to Nixtla schema (unique_id, ds, y)
3. Runs TimeGPT forecast (or fallback models)
4. Loads forecasts to destination
5. Monitors forecast quality

Generated by: nixtla-prod-pipeline-generator skill
"""

import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import yaml

# Environment variables (set in Airflow UI or docker-compose.yml)
NIXTLA_API_KEY = os.getenv('NIXTLA_API_KEY')
DATA_SOURCE = os.getenv('FORECAST_DATA_SOURCE', 'postgresql://...')
FORECAST_DEST = os.getenv('FORECAST_DESTINATION', 'postgresql://...')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')

# Load configuration
CONFIG_PATH = '/opt/airflow/dags/forecasting/config.yml'
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

horizon = config['forecast']['horizon']
freq = config['forecast']['frequency']

# DAG configuration
default_args = {
    'owner': 'forecasting-team',
    'depends_on_past': False,
    'email': ['alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(minutes=30),
}

dag = DAG(
    'timegpt_forecast_production',
    default_args=default_args,
    description='Production TimeGPT forecasting pipeline',
    schedule_interval='0 6 * * *',  # Daily at 6am UTC
    start_date=days_ago(1),
    catchup=False,
    tags=['forecasting', 'timegpt', 'production'],
)

def extract_production_data(**context):
    """Extract data from production source"""

    print(f"Extracting data from: {DATA_SOURCE}")

    # TODO: Implement actual extraction based on source type
    # For PostgreSQL:
    if DATA_SOURCE.startswith('postgresql://'):
        import psycopg2
        from sqlalchemy import create_engine

        engine = create_engine(DATA_SOURCE)

        # Extract last N days for context
        query = """
        SELECT
            unique_id,
            ds,
            y
        FROM sales
        WHERE ds >= CURRENT_DATE - INTERVAL '90 days'
        ORDER BY unique_id, ds
        """

        df = pd.read_sql(query, engine)

    # For BigQuery:
    elif DATA_SOURCE.startswith('bigquery://'):
        from google.cloud import bigquery

        client = bigquery.Client()

        query = """
        SELECT
            unique_id,
            ds,
            y
        FROM `project.dataset.table`
        WHERE ds >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
        ORDER BY unique_id, ds
        """

        df = client.query(query).to_dataframe()

    # For S3/GCS:
    elif DATA_SOURCE.startswith(('s3://', 'gs://')):
        df = pd.read_csv(DATA_SOURCE)

    else:
        raise ValueError(f"Unsupported data source: {DATA_SOURCE}")

    print(f"Extracted {len(df)} rows")
    print(f"Unique series: {df['unique_id'].nunique()}")
    print(f"Date range: {df['ds'].min()} to {df['ds'].max()}")

    # Save to XCom for next task
    ti = context['ti']
    ti.xcom_push(key='raw_data', value=df.to_json())

    return len(df)

def transform_to_nixtla_schema(**context):
    """Transform data to Nixtla schema (unique_id, ds, y)"""

    ti = context['ti']
    raw_data_json = ti.xcom_pull(key='raw_data', task_ids='extract')
    df = pd.read_json(raw_data_json)

    print("Validating Nixtla schema...")

    # Ensure required columns
    required_cols = ['unique_id', 'ds', 'y']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Missing required columns: {required_cols}")

    # Convert ds to datetime
    df['ds'] = pd.to_datetime(df['ds'])

    # Remove duplicates
    df = df.drop_duplicates(subset=['unique_id', 'ds'])

    # Sort by unique_id and ds
    df = df.sort_values(['unique_id', 'ds'])

    # Validate no missing values
    assert not df['y'].isna().any(), "Found missing values in target"

    print(f"✅ Schema validated: {len(df)} rows")

    ti.xcom_push(key='transformed_data', value=df.to_json())

    return len(df)

def run_timegpt_forecast(**context):
    """Run TimeGPT forecast (or fallback to baselines)"""

    ti = context['ti']
    data_json = ti.xcom_pull(key='transformed_data', task_ids='transform')
    df = pd.read_json(data_json)

    # Convert ds back to datetime (JSON serialization may change it)
    df['ds'] = pd.to_datetime(df['ds'])

    print(f"Running forecast with horizon={horizon}, freq={freq}")

    try:
        # Try TimeGPT first
        if NIXTLA_API_KEY:
            from nixtla import NixtlaClient

            client = NixtlaClient(api_key=NIXTLA_API_KEY)

            print("Running TimeGPT forecast...")
            forecast_df = client.forecast(
                df=df,
                h=horizon,
                freq=freq
            )

            forecast_df['model'] = 'TimeGPT'

        else:
            raise ValueError("NIXTLA_API_KEY not set, falling back to baselines")

    except Exception as e:
        print(f"TimeGPT failed: {e}")
        print("Falling back to StatsForecast baselines...")

        from statsforecast import StatsForecast
        from statsforecast.models import AutoETS, SeasonalNaive

        sf = StatsForecast(
            models=[AutoETS(season_length=7), SeasonalNaive(season_length=7)],
            freq=freq
        )

        sf.fit(df)
        forecast_df = sf.predict(h=horizon)

        # Use best performing model
        forecast_df['model'] = 'StatsForecast-AutoETS'

    # Add metadata
    forecast_df['forecast_date'] = datetime.now()
    forecast_df['environment'] = ENVIRONMENT
    forecast_df['horizon'] = horizon

    print(f"✅ Generated {len(forecast_df)} forecast rows")

    ti.xcom_push(key='forecasts', value=forecast_df.to_json())

    return len(forecast_df)

def load_forecasts_to_destination(**context):
    """Load forecasts to destination"""

    ti = context['ti']
    forecast_json = ti.xcom_pull(key='forecasts', task_ids='forecast')
    forecast_df = pd.read_json(forecast_json)

    print(f"Loading {len(forecast_df)} forecasts to: {FORECAST_DEST}")

    # TODO: Implement loading based on destination type
    if FORECAST_DEST.startswith('postgresql://'):
        from sqlalchemy import create_engine

        engine = create_engine(FORECAST_DEST)

        # Extract table name from connection string
        table = FORECAST_DEST.split('?table=')[1] if '?table=' in FORECAST_DEST else 'forecasts'

        # Append forecasts (or replace if needed)
        forecast_df.to_sql(
            table,
            engine,
            if_exists='append',
            index=False
        )

    elif FORECAST_DEST.startswith('bigquery://'):
        from google.cloud import bigquery

        client = bigquery.Client()

        # Extract table ID from connection string
        table_id = FORECAST_DEST.replace('bigquery://', '')

        # Load to BigQuery
        job = client.load_table_from_dataframe(forecast_df, table_id)
        job.result()  # Wait for completion

    elif FORECAST_DEST.startswith(('s3://', 'gs://')):
        # Write to cloud storage
        forecast_df.to_csv(FORECAST_DEST, index=False)

    else:
        raise ValueError(f"Unsupported destination: {FORECAST_DEST}")

    print(f"✅ Loaded forecasts successfully")

    return len(forecast_df)

def monitor_forecast_quality(**context):
    """Monitor forecast quality via backtesting"""

    from pipelines.monitoring import run_backtest_check

    ti = context['ti']
    data_json = ti.xcom_pull(key='transformed_data', task_ids='transform')
    df = pd.read_json(data_json)
    df['ds'] = pd.to_datetime(df['ds'])

    print("Running backtest to monitor quality...")

    # Backtest on last N periods
    backtest_results = run_backtest_check(df, horizon, freq)

    # Check if metrics are within acceptable range
    smape = backtest_results['smape']
    threshold = config.get('monitoring', {}).get('smape_threshold', 20.0)

    if smape > threshold:
        print(f"⚠️  WARNING: SMAPE {smape:.2f}% exceeds threshold {threshold}%")
        print("Consider retraining or investigating data quality issues")

        # Could send alert here
        # send_alert(f"Forecast quality degraded: SMAPE={smape:.2f}%")
    else:
        print(f"✅ Forecast quality OK: SMAPE={smape:.2f}%")

    return smape

# Define task dependencies
extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_production_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_to_nixtla_schema,
    dag=dag,
)

forecast_task = PythonOperator(
    task_id='forecast',
    python_callable=run_timegpt_forecast,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_forecasts_to_destination,
    dag=dag,
)

monitor_task = PythonOperator(
    task_id='monitor',
    python_callable=monitor_forecast_quality,
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> forecast_task >> load_task >> monitor_task
```

**Tell the user**:
- "Created `pipelines/timegpt_forecast_dag.py` (Airflow DAG)"
- Show task flow: Extract → Transform → Forecast → Load → Monitor
- Explain configuration via environment variables
- Provide deployment instructions

### 4. Generate Monitoring Module

Create `pipelines/monitoring.py`:

```python
"""
Forecast Monitoring and Quality Checks

Functions:
- run_backtest_check: Backtest on recent data to monitor quality
- detect_drift: Detect data distribution changes
- check_anomalies: Flag unusual forecast values
- fallback_to_baseline: Use simpler models if TimeGPT fails

Generated by: nixtla-prod-pipeline-generator skill
"""

import pandas as pd
import numpy as np
from statsforecast import StatsForecast
from statsforecast.models import SeasonalNaive
import yaml

def calculate_smape(actual, forecast):
    """Calculate Symmetric Mean Absolute Percentage Error"""
    return 100 * np.mean(2 * np.abs(forecast - actual) / (np.abs(actual) + np.abs(forecast)))

def run_backtest_check(df, horizon, freq, window_size=30):
    """
    Run backtest on recent data to monitor forecast quality

    Args:
        df: Historical data (unique_id, ds, y)
        horizon: Forecast horizon
        freq: Frequency (D, H, etc.)
        window_size: Number of recent periods to backtest

    Returns:
        dict with backtest metrics
    """

    print(f"Running backtest on last {window_size} periods...")

    # Split into train/test
    test_size = horizon
    train_df = df[:-test_size].copy()
    test_df = df[-test_size:].copy()

    # Generate forecasts using baseline (SeasonalNaive for monitoring)
    model = StatsForecast(
        models=[SeasonalNaive(season_length=7)],
        freq=freq
    )

    model.fit(train_df)
    forecast_df = model.predict(h=test_size)

    # Calculate metrics
    actual = test_df['y'].values
    forecast = forecast_df['SeasonalNaive'].values

    smape = calculate_smape(actual, forecast)
    mae = np.mean(np.abs(actual - forecast))

    results = {
        'smape': smape,
        'mae': mae,
        'test_size': test_size,
        'train_size': len(train_df)
    }

    print(f"Backtest results: SMAPE={smape:.2f}%, MAE={mae:.2f}")

    return results

def detect_drift(df, window_days=30):
    """
    Detect if recent data distribution has changed

    Args:
        df: Historical data
        window_days: Size of recent window to compare

    Returns:
        dict with drift indicators
    """

    # Calculate statistics for recent vs. historical
    recent_df = df.tail(window_days)
    historical_df = df.iloc[:-window_days]

    recent_mean = recent_df['y'].mean()
    historical_mean = historical_df['y'].mean()

    recent_std = recent_df['y'].std()
    historical_std = historical_df['y'].std()

    # Detect significant changes
    mean_change_pct = 100 * abs(recent_mean - historical_mean) / historical_mean
    std_change_pct = 100 * abs(recent_std - historical_std) / historical_std

    drift_detected = mean_change_pct > 20 or std_change_pct > 30

    results = {
        'drift_detected': drift_detected,
        'mean_change_pct': mean_change_pct,
        'std_change_pct': std_change_pct,
        'recent_mean': recent_mean,
        'historical_mean': historical_mean
    }

    if drift_detected:
        print(f"⚠️  Drift detected: mean changed {mean_change_pct:.1f}%, std changed {std_change_pct:.1f}%")

    return results

def check_anomalies(forecast_df, threshold=3):
    """
    Flag unusual forecast values (outliers)

    Args:
        forecast_df: Forecast dataframe
        threshold: Number of std deviations for outlier detection

    Returns:
        dict with anomaly flags
    """

    # Assuming forecast column is named based on model
    forecast_col = [col for col in forecast_df.columns if col not in ['unique_id', 'ds']][0]

    forecasts = forecast_df[forecast_col].values

    mean = np.mean(forecasts)
    std = np.std(forecasts)

    # Flag values beyond threshold
    anomalies = np.abs(forecasts - mean) > (threshold * std)
    anomaly_count = np.sum(anomalies)

    if anomaly_count > 0:
        print(f"⚠️  Found {anomaly_count} anomalous forecasts (>{threshold} std from mean)")

    return {
        'anomaly_count': anomaly_count,
        'anomaly_indices': np.where(anomalies)[0].tolist(),
        'mean': mean,
        'std': std
    }

def fallback_to_baseline(df, horizon, freq):
    """
    Generate forecasts using baseline models (fallback when TimeGPT fails)

    Args:
        df: Historical data
        horizon: Forecast horizon
        freq: Frequency

    Returns:
        Forecast dataframe
    """

    print("Using baseline models for forecast...")

    from statsforecast.models import AutoETS, SeasonalNaive

    model = StatsForecast(
        models=[
            AutoETS(season_length=7),
            SeasonalNaive(season_length=7)
        ],
        freq=freq
    )

    model.fit(df)
    forecast_df = model.predict(h=horizon)

    # Use AutoETS as primary fallback
    forecast_df['forecast'] = forecast_df['AutoETS']
    forecast_df['model'] = 'Fallback-AutoETS'

    return forecast_df[['unique_id', 'ds', 'forecast', 'model']]
```

**Tell the user**:
- "Created `pipelines/monitoring.py` with quality checks"
- Explain backtest, drift detection, anomaly detection
- Show fallback mechanism

### 5. Generate Deployment Documentation

Create `pipelines/README.md`:

```markdown
# Production Forecasting Pipeline

Automated TimeGPT forecasting pipeline with monitoring and fallback.

## Architecture

```
[Data Source] → Extract → Transform → Forecast → Load → Monitor → [Destination]
                                        ↓
                                  (Fallback to
                                   baselines)
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Required
export NIXTLA_API_KEY='your-api-key'
export FORECAST_DATA_SOURCE='postgresql://...'
export FORECAST_DESTINATION='postgresql://...'

# Optional
export ENVIRONMENT='production'  # dev/staging/production
```

### 3. Deploy to Airflow

```bash
# Copy DAG to Airflow dags folder
cp pipelines/timegpt_forecast_dag.py /opt/airflow/dags/

# Copy monitoring module
cp pipelines/monitoring.py /opt/airflow/dags/pipelines/

# Copy config
cp forecasting/config.yml /opt/airflow/dags/forecasting/

# Restart Airflow
docker-compose restart airflow-scheduler
```

## Testing

Test pipeline locally before deploying:

```python
# Test extract
python -c "from timegpt_forecast_dag import extract_production_data; extract_production_data()"

# Test transform
python -c "from timegpt_forecast_dag import transform_to_nixtla_schema; transform_to_nixtla_schema()"

# Test forecast
python -c "from timegpt_forecast_dag import run_timegpt_forecast; run_timegpt_forecast()"
```

## Monitoring

Pipeline emits logs and metrics at each step:
- Extract: Row count, date range
- Transform: Schema validation
- Forecast: Model used (TimeGPT or fallback)
- Load: Rows written
- Monitor: SMAPE, drift detection

### Alerts

Configure alerts in Airflow UI for:
- Task failures (automatic retry 2x)
- Forecast quality degradation (SMAPE > threshold)
- Data drift detection

## Troubleshooting

### TimeGPT API errors
- Check API key: `echo $NIXTLA_API_KEY`
- Verify quota: https://dashboard.nixtla.io
- Pipeline will fallback to StatsForecast baselines

### Data source connection errors
- Verify connection string
- Check network access from Airflow
- Test connection: `python -c "import sqlalchemy; engine = sqlalchemy.create_engine('$FORECAST_DATA_SOURCE'); engine.connect()"`

### Forecast quality issues
- Check backtest metrics in monitoring step
- Review data for anomalies or drift
- Consider retraining fine-tuned models
```

**Tell the user**:
- "Created `pipelines/README.md` with deployment guide"
- Highlight setup steps, testing, monitoring
- Provide troubleshooting guidance

---

## Handling Different Orchestration Platforms

### Prefect (Alternative)

If user chooses Prefect, generate similar structure but with Prefect syntax:

```python
from prefect import flow, task
from prefect.deployments import DeploymentSpec
from prefect.flow_runners import SubprocessFlowRunner

@task(retries=2, retry_delay_seconds=300)
def extract_data():
    # Same extraction logic
    pass

@task
def transform_data(raw_data):
    # Same transformation logic
    pass

@task
def forecast(transformed_data):
    # Same forecasting logic
    pass

@task
def load_forecasts(forecasts):
    # Same loading logic
    pass

@task
def monitor_quality(data, forecasts):
    # Same monitoring logic
    pass

@flow(name="timegpt-forecast-production")
def timegpt_forecast_pipeline():
    raw_data = extract_data()
    transformed = transform_data(raw_data)
    forecasts = forecast(transformed)
    load_forecasts(forecasts)
    monitor_quality(transformed, forecasts)

# Deployment
DeploymentSpec(
    flow=timegpt_forecast_pipeline,
    name="production",
    schedule="0 6 * * *",  # Daily at 6am
    flow_runner=SubprocessFlowRunner(),
    tags=["forecasting", "production"]
)
```

### Cron (Simplest Option)

If user chooses cron, generate standalone script:

```python
#!/usr/bin/env python3
"""
Standalone forecasting script for cron

Run with: python pipelines/run_forecast.py
Schedule with crontab: 0 6 * * * python /path/to/run_forecast.py
"""

import logging

logging.basicConfig(level=logging.INFO)

def main():
    try:
        # Extract
        logging.info("Extracting data...")
        data = extract_production_data()

        # Transform
        logging.info("Transforming data...")
        transformed = transform_to_nixtla_schema(data)

        # Forecast
        logging.info("Running forecast...")
        forecasts = run_timegpt_forecast(transformed)

        # Load
        logging.info("Loading forecasts...")
        load_forecasts_to_destination(forecasts)

        # Monitor
        logging.info("Monitoring quality...")
        monitor_forecast_quality(transformed, forecasts)

        logging.info("✅ Pipeline completed successfully")

    except Exception as e:
        logging.error(f"❌ Pipeline failed: {e}")
        raise

if __name__ == '__main__':
    main()
```

---

## Examples

### Example 1: Generate Airflow Pipeline

**User**: "Turn my experiments into a production Airflow pipeline"

**You**:
```
Let's generate a production pipeline!

Reading experiment configuration...
✅ Found: forecasting/config.yml
   - Horizon: 14 days
   - Frequency: D (daily)
   - Best model: TimeGPT (SMAPE: 8.7%)

Questions:
1. Production data source?
   → User: "postgresql://prod-db:5432/sales?table=daily_sales"

2. Forecast destination?
   → User: "postgresql://prod-db:5432/forecasts?table=forecasts"

3. Schedule (cron)?
   → User: "0 6 * * *" (daily at 6am)

4. Environment?
   → User: "production"

Generating Airflow pipeline...

✅ Created:
   - pipelines/timegpt_forecast_dag.py (Airflow DAG)
   - pipelines/monitoring.py (quality checks)
   - pipelines/README.md (deployment guide)

Pipeline tasks:
1. Extract → Get data from PostgreSQL
2. Transform → Validate Nixtla schema
3. Forecast → TimeGPT (fallback to AutoETS)
4. Load → Write forecasts to PostgreSQL
5. Monitor → Backtest quality check

Environment variables needed:
- NIXTLA_API_KEY
- FORECAST_DATA_SOURCE (default: postgresql://...)
- FORECAST_DESTINATION (default: postgresql://...)

Next steps:
1. Review pipeline: cat pipelines/timegpt_forecast_dag.py
2. Set env vars in Airflow UI
3. Deploy: cp pipelines/* /opt/airflow/dags/
4. Enable DAG in Airflow UI
```

### Example 2: Cron-Based Pipeline

**User**: "I just want a simple cron job, no Airflow"

**You**:
```
Generating cron-based pipeline...

✅ Created:
   - pipelines/run_forecast.py (standalone script)
   - pipelines/monitoring.py (quality checks)
   - pipelines/README.md (setup guide)

To schedule with cron:

1. Make script executable:
   chmod +x pipelines/run_forecast.py

2. Add to crontab:
   crontab -e

   # Add this line:
   0 6 * * * /usr/bin/python3 /path/to/pipelines/run_forecast.py >> /var/log/forecast.log 2>&1

3. Set environment variables in crontab:
   NIXTLA_API_KEY=your-key
   FORECAST_DATA_SOURCE=postgresql://...
   FORECAST_DESTINATION=postgresql://...

The script will run daily at 6am and log to /var/log/forecast.log
```

---

## Common Issues and Troubleshooting

### Issue 1: No experiment configuration found

**Symptom**: Pipeline generator can't find `forecasting/config.yml`

**Solution**:
```
Run nixtla-experiment-architect first to set up experiments:

1. "Set up a forecasting experiment"
2. Complete experiment setup
3. Run this skill again
```

### Issue 2: Database connection errors

**Symptom**: Extract or load tasks fail with connection errors

**Solution**:
```python
# Test connection strings
import sqlalchemy

# Test source
engine = sqlalchemy.create_engine(os.getenv('FORECAST_DATA_SOURCE'))
engine.connect()  # Should not raise error

# Test destination
engine = sqlalchemy.create_engine(os.getenv('FORECAST_DESTINATION'))
engine.connect()  # Should not raise error
```

### Issue 3: Airflow can't import dependencies

**Symptom**: Tasks fail with "ModuleNotFoundError"

**Solution**:
```
Install dependencies in Airflow environment:

# If using Docker:
docker exec -it airflow-worker pip install nixtla statsforecast

# Or add to requirements.txt and rebuild
echo "nixtla" >> requirements.txt
echo "statsforecast" >> requirements.txt
docker-compose build
```

---

## Best Practices

### 1. Start with Staging Environment

Test pipelines in staging before production:
```yaml
# config.yml
environments:
  staging:
    data_source: "postgresql://staging-db/..."
    destination: "postgresql://staging-db/..."
  production:
    data_source: "postgresql://prod-db/..."
    destination: "postgresql://prod-db/..."
```

### 2. Implement Proper Logging

All tasks should log key metrics:
```python
logging.info(f"Extracted {row_count} rows")
logging.info(f"Forecast SMAPE: {smape:.2f}%")
logging.warning(f"Drift detected: {drift_pct:.1f}% change")
```

### 3. Configure Alerts

Set up alerts for failures and quality issues:
- Airflow: email_on_failure in DAG config
- Prefect: Automation rules
- Cron: Pipe errors to monitoring system

### 4. Version Control Pipeline Code

Treat pipeline code as production code:
```bash
git add pipelines/
git commit -m "feat(pipelines): add TimeGPT production pipeline"
git push
```

### 5. Monitor Costs

TimeGPT API calls cost money:
- Track API usage via Nixtla dashboard
- Implement fallback to free baselines
- Set budget alerts

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
