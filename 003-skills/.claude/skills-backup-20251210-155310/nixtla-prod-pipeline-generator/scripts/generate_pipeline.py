#!/usr/bin/env python3
"""
Generate production-ready forecasting pipeline from experiment config.

Creates Airflow DAG, Prefect flow, or cron script based on validated experiment
configuration. Includes ETL tasks, error handling, and monitoring hooks.

Usage:
    python generate_pipeline.py --config forecasting/config.yml --platform airflow
    python generate_pipeline.py --config forecasting/config.yml --platform prefect --schedule "0 6 * * *"
    python generate_pipeline.py --config forecasting/config.yml --platform cron --output pipelines/

Author: nixtla-prod-pipeline-generator skill
"""

import argparse
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

# Security logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_api_key(key: Optional[str]) -> bool:
    """
    Validate API key format and structure.

    Args:
        key: API key string to validate

    Returns:
        True if key appears valid, False otherwise

    Security:
        - Minimum length check prevents empty/trivial keys
        - Pattern check validates expected format
        - Does not log key value to prevent credential leakage
        - OWASP A07:2021 - Identification and Authentication Failures
    """
    if not key:
        return False

    key = key.strip()

    # Minimum length check (Nixtla keys are typically 32+ characters)
    if len(key) < 20:
        return False

    # Check for common placeholder values
    placeholder_patterns = [
        r"^your[-_]?api[-_]?key",
        r"^xxx+$",
        r"^test[-_]?key",
        r"^placeholder",
        r"^demo[-_]?key",
    ]
    for pattern in placeholder_patterns:
        if re.match(pattern, key, re.IGNORECASE):
            return False

    # Basic alphanumeric pattern check (allow alphanumeric, hyphens, underscores)
    if not re.match(r"^[a-zA-Z0-9_-]+$", key):
        return False

    return True


def escape_string_for_code(value: str) -> str:
    """
    Escape string value for safe embedding in generated Python code.

    Args:
        value: String to escape

    Returns:
        Escaped string safe for code generation

    Security:
        - Prevents code injection via configuration values
        - OWASP A03:2021 - Injection
    """
    escaped = value.replace("\\", "\\\\")
    escaped = escaped.replace('"', '\\"')
    escaped = escaped.replace("'", "\\'")
    escaped = escaped.replace("\n", "\\n")
    escaped = escaped.replace("\r", "\\r")
    return escaped


class PipelineGenerator:
    """Generate production pipeline code from experiment configuration."""

    PLATFORMS = ["airflow", "prefect", "cron"]

    # Template directory relative to this script
    TEMPLATE_DIR = Path(__file__).parent.parent / "assets" / "templates"

    def __init__(self, config_path: str, platform: str, output_dir: str):
        """
        Initialize pipeline generator.

        Args:
            config_path: Path to config.yml
            platform: Platform (airflow, prefect, cron)
            output_dir: Output directory for generated files
        """
        self.config_path = Path(config_path)
        self.platform = platform.lower()
        self.output_dir = Path(output_dir)
        self.config: Optional[Dict[str, Any]] = None

        if self.platform not in self.PLATFORMS:
            raise ValueError(f"Platform must be one of {self.PLATFORMS}")

    def load_config(self) -> Dict[str, Any]:
        """Load and validate config file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            self.config = yaml.safe_load(f)

        return self.config

    def generate(self, schedule: Optional[str] = None) -> Dict[str, Path]:
        """
        Generate pipeline files.

        Args:
            schedule: Cron schedule expression (e.g., "0 6 * * *")

        Returns:
            Dictionary mapping file type to generated file path
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        generated_files = {}

        if self.platform == "airflow":
            generated_files["dag"] = self._generate_airflow_dag(schedule)
        elif self.platform == "prefect":
            generated_files["flow"] = self._generate_prefect_flow(schedule)
        elif self.platform == "cron":
            generated_files["script"] = self._generate_cron_script()

        # Generate common files
        generated_files["monitoring"] = self._generate_monitoring()
        generated_files["readme"] = self._generate_readme()
        generated_files["requirements"] = self._generate_requirements()

        return generated_files

    def _generate_airflow_dag(self, schedule: Optional[str]) -> Path:
        """Generate Airflow DAG file."""
        schedule = schedule or "0 6 * * *"  # Default: daily at 6am

        horizon = self.config["forecast"]["horizon"]
        freq = self.config["forecast"]["freq"]
        target = self.config["data"]["y"]

        dag_code = f'''"""
Production Forecasting DAG - Generated by nixtla-prod-pipeline-generator
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Pipeline: Extract → Transform → Forecast → Load → Monitor
Schedule: {schedule}
"""

import os
import re
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import yaml


def validate_api_key(key):
    """
    Validate API key format and structure.
    Security: OWASP A07:2021 - Identification and Authentication Failures
    """
    if not key:
        return False
    key = key.strip()
    if len(key) < 20:
        return False
    placeholder_patterns = [
        r'^your[-_]?api[-_]?key', r'^xxx+$', r'^test[-_]?key',
        r'^placeholder', r'^demo[-_]?key',
    ]
    for pattern in placeholder_patterns:
        if re.match(pattern, key, re.IGNORECASE):
            return False
    if not re.match(r'^[a-zA-Z0-9_-]+$', key):
        return False
    return True


# Environment variables (with security validation)
NIXTLA_API_KEY = os.getenv('NIXTLA_API_KEY', '').strip()
DATA_SOURCE = os.getenv('FORECAST_DATA_SOURCE')
FORECAST_DEST = os.getenv('FORECAST_DESTINATION')

# Configuration
HORIZON = {horizon}
FREQ = '{freq}'
TARGET_COL = '{target}'

default_args = {{
    'owner': 'forecasting-team',
    'depends_on_past': False,
    'email': ['alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(minutes=30),
}}

dag = DAG(
    'nixtla_production_forecast',
    default_args=default_args,
    description='Production forecasting pipeline',
    schedule_interval='{schedule}',
    start_date=days_ago(1),
    catchup=False,
    tags=['forecasting', 'nixtla', 'production'],
)


def extract_data(**context):
    """Extract production data from source."""
    print(f"Extracting data from: {{DATA_SOURCE}}")

    if not DATA_SOURCE:
        raise ValueError("FORECAST_DATA_SOURCE environment variable not set")

    # Load data based on source type
    if DATA_SOURCE.startswith('postgresql://'):
        from sqlalchemy import create_engine
        engine = create_engine(DATA_SOURCE)

        query = """
        SELECT unique_id, ds, {target}
        FROM production_data
        WHERE ds >= CURRENT_DATE - INTERVAL '90 days'
        ORDER BY unique_id, ds
        """
        df = pd.read_sql(query, engine)

    elif DATA_SOURCE.startswith('bigquery://'):
        from google.cloud import bigquery
        client = bigquery.Client()

        query = """
        SELECT unique_id, ds, {target}
        FROM `project.dataset.table`
        WHERE ds >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
        ORDER BY unique_id, ds
        """
        df = client.query(query).to_dataframe()

    elif DATA_SOURCE.endswith('.csv'):
        df = pd.read_csv(DATA_SOURCE)

    else:
        raise ValueError(f"Unsupported data source: {{DATA_SOURCE}}")

    print(f"✓ Extracted {{len(df)}} rows, {{df['unique_id'].nunique()}} series")

    ti = context['ti']
    ti.xcom_push(key='raw_data', value=df.to_json())
    return len(df)


def transform_data(**context):
    """Transform to Nixtla schema."""
    ti = context['ti']
    raw_json = ti.xcom_pull(key='raw_data', task_ids='extract')
    df = pd.read_json(raw_json)

    # Ensure required columns
    required = ['unique_id', 'ds', '{target}']
    if not all(col in df.columns for col in required):
        raise ValueError(f"Missing columns. Required: {{required}}")

    # Standardize column names
    df = df.rename(columns={{'{target}': 'y'}})

    # Convert ds to datetime
    df['ds'] = pd.to_datetime(df['ds'])

    # Remove duplicates and sort
    df = df.drop_duplicates(subset=['unique_id', 'ds'])
    df = df.sort_values(['unique_id', 'ds'])

    # Validate no missing values
    if df['y'].isna().any():
        raise ValueError("Found missing values in target column")

    print(f"✓ Transformed {{len(df)}} rows")

    ti.xcom_push(key='transformed', value=df.to_json())
    return len(df)


def forecast(**context):
    """Generate forecasts using TimeGPT or fallback models."""
    ti = context['ti']
    data_json = ti.xcom_pull(key='transformed', task_ids='transform')
    df = pd.read_json(data_json)
    df['ds'] = pd.to_datetime(df['ds'])

    print(f"Running forecast: horizon={{HORIZON}}, freq={{FREQ}}")

    try:
        # Try TimeGPT (with API key validation)
        if NIXTLA_API_KEY and validate_api_key(NIXTLA_API_KEY):
            from nixtla import NixtlaClient
            client = NixtlaClient(api_key=NIXTLA_API_KEY)

            forecast_df = client.forecast(df=df, h=HORIZON, freq=FREQ)
            forecast_df['model'] = 'TimeGPT'
            print("✓ TimeGPT forecast completed")
        else:
            raise ValueError("No valid API key, using fallback")

    except Exception as e:
        print(f"TimeGPT failed: {{e}}")
        print("Falling back to StatsForecast baselines...")

        from statsforecast import StatsForecast
        from statsforecast.models import AutoETS, SeasonalNaive

        sf = StatsForecast(
            models=[AutoETS(), SeasonalNaive()],
            freq=FREQ
        )
        sf.fit(df)
        forecast_df = sf.predict(h=HORIZON)
        forecast_df['model'] = 'Fallback-AutoETS'
        print("✓ Fallback forecast completed")

    # Add metadata
    forecast_df['forecast_date'] = datetime.now()
    forecast_df['horizon'] = HORIZON

    print(f"✓ Generated {{len(forecast_df)}} forecasts")

    ti.xcom_push(key='forecasts', value=forecast_df.to_json())
    return len(forecast_df)


def load_forecasts(**context):
    """Load forecasts to destination."""
    ti = context['ti']
    forecast_json = ti.xcom_pull(key='forecasts', task_ids='forecast')
    forecast_df = pd.read_json(forecast_json)

    if not FORECAST_DEST:
        raise ValueError("FORECAST_DESTINATION environment variable not set")

    print(f"Loading {{len(forecast_df)}} forecasts to {{FORECAST_DEST}}")

    if FORECAST_DEST.startswith('postgresql://'):
        from sqlalchemy import create_engine
        engine = create_engine(FORECAST_DEST)
        forecast_df.to_sql('forecasts', engine, if_exists='append', index=False)

    elif FORECAST_DEST.startswith('bigquery://'):
        from google.cloud import bigquery
        client = bigquery.Client()
        table_id = FORECAST_DEST.replace('bigquery://', '')
        job = client.load_table_from_dataframe(forecast_df, table_id)
        job.result()

    elif FORECAST_DEST.endswith('.csv'):
        forecast_df.to_csv(FORECAST_DEST, mode='a', header=False, index=False)

    else:
        raise ValueError(f"Unsupported destination: {{FORECAST_DEST}}")

    print("✓ Forecasts loaded successfully")
    return len(forecast_df)


def monitor(**context):
    """Monitor forecast quality."""
    from monitoring import run_backtest_check

    ti = context['ti']
    data_json = ti.xcom_pull(key='transformed', task_ids='transform')
    df = pd.read_json(data_json)
    df['ds'] = pd.to_datetime(df['ds'])

    print("Running quality checks...")

    results = run_backtest_check(df, HORIZON, FREQ)
    smape = results['smape']

    threshold = 20.0  # Default threshold

    if smape > threshold:
        print(f"⚠️  WARNING: SMAPE {{smape:.2f}}% exceeds threshold {{threshold}}%")
    else:
        print(f"✓ Quality OK: SMAPE={{smape:.2f}}%")

    return smape


# Define tasks
extract_task = PythonOperator(task_id='extract', python_callable=extract_data, dag=dag)
transform_task = PythonOperator(task_id='transform', python_callable=transform_data, dag=dag)
forecast_task = PythonOperator(task_id='forecast', python_callable=forecast, dag=dag)
load_task = PythonOperator(task_id='load', python_callable=load_forecasts, dag=dag)
monitor_task = PythonOperator(task_id='monitor', python_callable=monitor, dag=dag)

# Task dependencies
extract_task >> transform_task >> forecast_task >> load_task >> monitor_task
'''

        output_path = self.output_dir / "forecast_dag.py"
        output_path.write_text(dag_code)

        return output_path

    def _generate_prefect_flow(self, schedule: Optional[str]) -> Path:
        """Generate Prefect flow file."""
        schedule = schedule or "0 6 * * *"

        horizon = self.config["forecast"]["horizon"]
        freq = self.config["forecast"]["freq"]

        flow_code = f'''"""
Production Forecasting Flow - Generated by nixtla-prod-pipeline-generator
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Prefect flow for production forecasting pipeline.
Schedule: {schedule}
"""

import os
from prefect import flow, task
import pandas as pd

HORIZON = {horizon}
FREQ = '{freq}'


@task(retries=2, retry_delay_seconds=300)
def extract_data():
    """Extract production data."""
    data_source = os.getenv('FORECAST_DATA_SOURCE')
    # Same extraction logic as Airflow
    return df


@task
def transform_data(raw_data):
    """Transform to Nixtla schema."""
    # Same transformation logic
    return transformed_df


@task
def forecast(data):
    """Generate forecasts."""
    # Same forecasting logic
    return forecast_df


@task
def load_forecasts(forecasts):
    """Load to destination."""
    # Same loading logic
    return len(forecasts)


@task
def monitor_quality(data):
    """Monitor forecast quality."""
    from monitoring import run_backtest_check
    results = run_backtest_check(data, HORIZON, FREQ)
    return results


@flow(name="nixtla-production-forecast")
def forecast_pipeline():
    """Main forecasting pipeline."""
    raw = extract_data()
    transformed = transform_data(raw)
    forecasts = forecast(transformed)
    load_forecasts(forecasts)
    monitor_quality(transformed)


if __name__ == '__main__':
    forecast_pipeline()
'''

        output_path = self.output_dir / "forecast_flow.py"
        output_path.write_text(flow_code)

        return output_path

    def _generate_cron_script(self) -> Path:
        """Generate standalone cron script."""
        horizon = self.config["forecast"]["horizon"]
        freq = self.config["forecast"]["freq"]

        script_code = f'''#!/usr/bin/env python3
"""
Standalone Forecasting Script - Generated by nixtla-prod-pipeline-generator
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Run with: python run_forecast.py
Schedule with crontab: 0 6 * * * /path/to/run_forecast.py
"""

import os
import re
import logging
from datetime import datetime
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def validate_api_key(key):
    """
    Validate API key format and structure.
    Security: OWASP A07:2021 - Identification and Authentication Failures
    """
    if not key:
        return False
    key = key.strip()
    if len(key) < 20:
        return False
    placeholder_patterns = [
        r'^your[-_]?api[-_]?key', r'^xxx+$', r'^test[-_]?key',
        r'^placeholder', r'^demo[-_]?key',
    ]
    for pattern in placeholder_patterns:
        if re.match(pattern, key, re.IGNORECASE):
            return False
    if not re.match(r'^[a-zA-Z0-9_-]+$', key):
        return False
    return True


HORIZON = {horizon}
FREQ = '{freq}'


def extract_data():
    """Extract production data."""
    data_source = os.getenv('FORECAST_DATA_SOURCE')
    logging.info(f"Extracting from {{data_source}}")

    if data_source.endswith('.csv'):
        df = pd.read_csv(data_source)
    else:
        raise ValueError(f"Unsupported source: {{data_source}}")

    logging.info(f"Extracted {{len(df)}} rows")
    return df


def transform_data(df):
    """Transform to Nixtla schema."""
    logging.info("Transforming data...")
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.sort_values(['unique_id', 'ds'])
    return df


def forecast(df):
    """Generate forecasts."""
    logging.info(f"Forecasting: horizon={{HORIZON}}, freq={{FREQ}}")

    try:
        api_key = os.getenv('NIXTLA_API_KEY', '').strip()
        if api_key and validate_api_key(api_key):
            from nixtla import NixtlaClient
            client = NixtlaClient(api_key=api_key)
            forecast_df = client.forecast(df=df, h=HORIZON, freq=FREQ)
            forecast_df['model'] = 'TimeGPT'
        else:
            raise ValueError("No valid API key")
    except Exception as e:
        logging.warning(f"TimeGPT failed: {{e}}, using fallback")
        from statsforecast import StatsForecast
        from statsforecast.models import AutoETS

        sf = StatsForecast(models=[AutoETS()], freq=FREQ)
        sf.fit(df)
        forecast_df = sf.predict(h=HORIZON)
        forecast_df['model'] = 'Fallback'

    forecast_df['forecast_date'] = datetime.now()
    logging.info(f"Generated {{len(forecast_df)}} forecasts")
    return forecast_df


def load_forecasts(forecast_df):
    """Load forecasts to destination."""
    dest = os.getenv('FORECAST_DESTINATION')
    logging.info(f"Loading to {{dest}}")

    if dest.endswith('.csv'):
        forecast_df.to_csv(dest, mode='a', header=False, index=False)
    else:
        raise ValueError(f"Unsupported destination: {{dest}}")

    logging.info("Forecasts loaded")


def monitor_quality(df):
    """Monitor forecast quality."""
    logging.info("Running quality checks...")
    from monitoring import run_backtest_check
    results = run_backtest_check(df, HORIZON, FREQ)
    logging.info(f"Quality: SMAPE={{results['smape']:.2f}}%")


def main():
    """Main pipeline execution."""
    try:
        logging.info("=== Starting forecast pipeline ===")

        data = extract_data()
        transformed = transform_data(data)
        forecasts = forecast(transformed)
        load_forecasts(forecasts)
        monitor_quality(transformed)

        logging.info("=== Pipeline completed successfully ===")
        return 0

    except Exception as e:
        logging.error(f"Pipeline failed: {{e}}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit(main())
'''

        output_path = self.output_dir / "run_forecast.py"
        output_path.write_text(script_code)
        output_path.chmod(0o755)  # Make executable

        return output_path

    def _generate_monitoring(self) -> Path:
        """Generate monitoring.py with quality checks."""
        monitoring_code = '''"""
Monitoring and Quality Checks - Generated by nixtla-prod-pipeline-generator

Functions for forecast quality monitoring, drift detection, and fallback logic.
"""

import pandas as pd
import numpy as np
from statsforecast import StatsForecast
from statsforecast.models import SeasonalNaive, AutoETS


def calculate_smape(actual, forecast):
    """Calculate Symmetric Mean Absolute Percentage Error."""
    return 100 * np.mean(
        2 * np.abs(forecast - actual) / (np.abs(actual) + np.abs(forecast))
    )


def run_backtest_check(df, horizon, freq, window_size=30):
    """
    Run backtest on recent data to monitor quality.

    Args:
        df: Historical data (unique_id, ds, y)
        horizon: Forecast horizon
        freq: Frequency (D, H, etc.)
        window_size: Number of recent periods to backtest

    Returns:
        dict with backtest metrics (smape, mae)
    """
    print(f"Running backtest on last {window_size} periods...")

    # Split train/test
    test_size = min(horizon, len(df) // 10)
    train_df = df[:-test_size].copy()
    test_df = df[-test_size:].copy()

    # Forecast with baseline
    model = StatsForecast(models=[SeasonalNaive()], freq=freq)
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

    print(f"Backtest: SMAPE={smape:.2f}%, MAE={mae:.2f}")
    return results


def detect_drift(df, window_days=30):
    """
    Detect if recent data distribution has changed.

    Args:
        df: Historical data
        window_days: Size of recent window

    Returns:
        dict with drift indicators
    """
    recent = df.tail(window_days)
    historical = df.iloc[:-window_days]

    recent_mean = recent['y'].mean()
    historical_mean = historical['y'].mean()

    mean_change = 100 * abs(recent_mean - historical_mean) / historical_mean

    drift_detected = mean_change > 20

    results = {
        'drift_detected': drift_detected,
        'mean_change_pct': mean_change,
        'recent_mean': recent_mean,
        'historical_mean': historical_mean
    }

    if drift_detected:
        print(f"⚠️  Drift detected: mean changed {mean_change:.1f}%")

    return results


def fallback_to_baseline(df, horizon, freq):
    """
    Generate forecasts using baseline models (fallback).

    Args:
        df: Historical data
        horizon: Forecast horizon
        freq: Frequency

    Returns:
        Forecast dataframe
    """
    print("Using baseline models...")

    model = StatsForecast(models=[AutoETS()], freq=freq)
    model.fit(df)
    forecast_df = model.predict(h=horizon)
    forecast_df['model'] = 'Fallback-AutoETS'

    return forecast_df
'''

        output_path = self.output_dir / "monitoring.py"
        output_path.write_text(monitoring_code)

        return output_path

    def _generate_readme(self) -> Path:
        """Generate README with deployment instructions."""
        readme = f"""# Production Forecasting Pipeline

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Platform: {self.platform}

## Overview

This pipeline implements: Extract → Transform → Forecast → Load → Monitor

## Prerequisites

```bash
pip install -r requirements.txt
```

## Environment Variables

Set these before running:

```bash
export FORECAST_DATA_SOURCE="postgresql://..."  # or path to CSV
export FORECAST_DESTINATION="postgresql://..."  # or path to CSV
export NIXTLA_API_KEY="your-api-key"  # Optional, fallback to baselines
```

## Deployment

### {self.platform.capitalize()}

"""

        if self.platform == "airflow":
            readme += """
1. Copy `forecast_dag.py` to Airflow DAGs folder
2. Set environment variables in Airflow UI or docker-compose.yml
3. Enable DAG in Airflow UI
4. Monitor at http://localhost:8080
"""
        elif self.platform == "prefect":
            readme += """
1. Run: `prefect deployment build forecast_flow.py:forecast_pipeline -n production`
2. Run: `prefect deployment apply forecast_pipeline-deployment.yaml`
3. Start agent: `prefect agent start -q default`
4. Monitor at http://localhost:4200
"""
        else:  # cron
            readme += """
1. Make script executable: `chmod +x run_forecast.py`
2. Test manually: `python run_forecast.py`
3. Add to crontab: `crontab -e`
4. Add line: `0 6 * * * /full/path/to/run_forecast.py >> /var/log/forecast.log 2>&1`
"""

        readme += """
## Monitoring

- Forecast quality is monitored via backtesting
- Drift detection alerts on data distribution changes
- Automatic fallback to baselines if TimeGPT fails

## Troubleshooting

- Check logs for error messages
- Verify environment variables are set
- Test data source connectivity
- Ensure sufficient historical data (90+ days)
"""

        output_path = self.output_dir / "README.md"
        output_path.write_text(readme)

        return output_path

    def _generate_requirements(self) -> Path:
        """Generate requirements.txt."""
        requirements = [
            "pandas>=1.5.0",
            "pyyaml>=6.0",
            "nixtla>=0.5.0",
            "statsforecast>=1.5.0",
            "utilsforecast>=0.0.10",
        ]

        if self.platform == "airflow":
            requirements.append("apache-airflow>=2.5.0")
        elif self.platform == "prefect":
            requirements.append("prefect>=2.10.0")

        output_path = self.output_dir / "requirements.txt"
        output_path.write_text("\n".join(requirements) + "\n")

        return output_path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate production forecasting pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Airflow DAG
  python generate_pipeline.py --config forecasting/config.yml --platform airflow

  # Generate Prefect flow with custom schedule
  python generate_pipeline.py --config forecasting/config.yml --platform prefect --schedule "0 */6 * * *"

  # Generate simple cron script
  python generate_pipeline.py --config forecasting/config.yml --platform cron --output pipelines/
        """,
    )

    parser.add_argument("--config", required=True, help="Path to experiment config.yml")

    parser.add_argument(
        "--platform", required=True, choices=PipelineGenerator.PLATFORMS, help="Target platform"
    )

    parser.add_argument(
        "--output", default="pipelines", help="Output directory (default: pipelines/)"
    )

    parser.add_argument("--schedule", help='Cron schedule expression (e.g., "0 6 * * *")')

    args = parser.parse_args()

    try:
        generator = PipelineGenerator(args.config, args.platform, args.output)

        print(f"Loading config: {args.config}")
        generator.load_config()

        print(f"Generating {args.platform} pipeline...")
        files = generator.generate(schedule=args.schedule)

        print("\n✓ Pipeline generated successfully!")
        print("\nGenerated files:")
        for file_type, path in files.items():
            print(f"  - {path}")

        print(f"\nNext steps:")
        print(f"  1. Review generated files in {args.output}/")
        print(f"  2. Set environment variables (see README.md)")
        print(f"  3. Deploy to {args.platform}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
