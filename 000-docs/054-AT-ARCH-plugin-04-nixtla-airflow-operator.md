# Plugin #4: Nixtla Airflow Operator
**Technical Architecture & Implementation Specification**

**Created**: 2025-11-30
**Status**: Design Phase
**Priority**: Tier 2 (INTEGRATION WIN)
**Addresses**: Integration Tax (Friction #4)

---

## Executive Summary

### What It Is
A production-grade Apache Airflow operator (`NixtlaForecastOperator`) that natively integrates Nixtla TimeGPT forecasting into DAGs with automatic retry logic, authentication handling, and dependency management.

### Why It Exists
Nixtla's CRO sees this friction:
> "Users must rely on generic PythonOperator to call Nixtla SDK, managing authentication and dependencies manually. This 'glue code tax' slows adoption."

**This plugin makes Nixtla a first-class citizen in Airflow workflows.**

### Who It's For
- **Data engineering teams** running production forecast pipelines
- **MLOps engineers** orchestrating forecasting workflows
- **Analytics teams** scheduling recurring forecasts
- **Platform teams** standardizing forecasting infrastructure

---

## Architecture Overview

### Component Stack

```
┌─────────────────────────────────────────────────────────────┐
│  AIRFLOW DAG                                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  from airflow_providers_nixtla import                │  │
│  │      NixtlaForecastOperator                          │  │
│  │                                                       │  │
│  │  forecast_task = NixtlaForecastOperator(            │  │
│  │      task_id='daily_forecast',                      │  │
│  │      dataset='bigquery.sales',                      │  │
│  │      horizon=30,                                     │  │
│  │      nixtla_conn_id='nixtla_api'                    │  │
│  │  )                                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  AIRFLOW PROVIDER PACKAGE                                   │
│  airflow-providers-nixtla                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Operators:                                           │  │
│  │  ├─ NixtlaForecastOperator                          │  │
│  │  ├─ NixtlaAnomalyOperator                           │  │
│  │  └─ NixtlaCrossValidationOperator                   │  │
│  │                                                       │  │
│  │  Hooks:                                              │  │
│  │  └─ NixtlaHook (handles auth, retries)             │  │
│  │                                                       │  │
│  │  Sensors:                                            │  │
│  │  └─ NixtlaJobSensor (async job polling)            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  NIXTLA API / DATA SOURCES                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │ TimeGPT API │  │  BigQuery   │  │  Snowflake       │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Plugin Type
**Airflow Provider Package** (Pure Python)

### Components

1. **Airflow Operators** (3)
   - `NixtlaForecastOperator` - Run forecasts
   - `NixtlaAnomalyOperator` - Detect anomalies
   - `NixtlaCrossValidationOperator` - Backtest models

2. **Airflow Hooks** (1)
   - `NixtlaHook` - Handle API authentication and retries

3. **Airflow Sensors** (1)
   - `NixtlaJobSensor` - Poll async jobs

4. **No MCP Server** - Pure Airflow integration

---

## API Keys & User Requirements

### Required
- **NIXTLA_API_KEY** - Stored in Airflow Connections
- **Airflow 2.5.0+** - Provider requires modern Airflow

### User Requirements

#### Minimum
- Apache Airflow running (2.5.0+)
- Python 3.10+
- Access to Airflow Connections UI (for API key config)

#### Recommended
- BigQuery or Snowflake integration
- Airflow on Kubernetes (for scalability)
- Monitoring (Prometheus/Grafana)

---

## Installation Process

### setup.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Installing Nixtla Airflow Provider..."

# Install provider package
pip install apache-airflow-providers-nixtla

# Configure Airflow connection
echo "⚙️  Configuring Airflow connection..."

# Option 1: CLI (if available)
if command -v airflow &> /dev/null; then
    airflow connections add nixtla_api \
        --conn-type http \
        --conn-host https://api.nixtla.io \
        --conn-password "nixak-YOUR_API_KEY_HERE"

    echo "✅ Airflow connection 'nixtla_api' created"
else
    echo "⚠️  Airflow CLI not found"
    echo "   Add connection manually in Airflow UI:"
    echo "   Admin > Connections > Add Connection"
    echo "   - Conn Id: nixtla_api"
    echo "   - Conn Type: HTTP"
    echo "   - Host: https://api.nixtla.io"
    echo "   - Password: YOUR_NIXTLA_API_KEY"
fi

echo "✅ Installation complete!"
echo ""
echo "Example DAG:"
echo "  from airflow_providers_nixtla import NixtlaForecastOperator"
echo "  forecast = NixtlaForecastOperator(task_id='forecast', ...)"
```

---

## Code Implementation

### Directory Structure

```
airflow-providers-nixtla/
├── setup.py                          # Package setup
├── README.md
├── LICENSE
├── airflow_providers_nixtla/
│   ├── __init__.py
│   ├── operators/
│   │   ├── __init__.py
│   │   ├── forecast.py               # NixtlaForecastOperator
│   │   ├── anomaly.py                # NixtlaAnomalyOperator
│   │   └── cross_validation.py       # NixtlaCrossValidationOperator
│   ├── hooks/
│   │   ├── __init__.py
│   │   └── nixtla.py                 # NixtlaHook
│   ├── sensors/
│   │   ├── __init__.py
│   │   └── job.py                    # NixtlaJobSensor
│   └── utils/
│       └── data_connectors.py        # BigQuery/Snowflake helpers
├── tests/
│   ├── operators/
│   ├── hooks/
│   └── sensors/
└── example_dags/
    ├── daily_forecast.py
    ├── anomaly_detection.py
    └── backtest_validation.py
```

### Core Implementation

#### operators/forecast.py

```python
"""
NixtlaForecastOperator - Production-grade Airflow operator
"""
from typing import Any, Dict, Optional, List
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from airflow_providers_nixtla.hooks.nixtla import NixtlaHook


class NixtlaForecastOperator(BaseOperator):
    """
    Run Nixtla TimeGPT forecasts in Airflow DAG

    :param dataset: Source dataset (table ref, query, or DataFrame)
    :param horizon: Forecast horizon
    :param models: List of models to use (default: ['TimeGPT'])
    :param freq: Frequency ('D', 'H', 'M', etc.)
    :param output_table: Where to write forecasts
    :param nixtla_conn_id: Airflow connection ID for Nixtla API

    Example:
        forecast_task = NixtlaForecastOperator(
            task_id='daily_sales_forecast',
            dataset='bigquery.analytics.sales',
            horizon=30,
            freq='D',
            output_table='forecasts.daily_sales',
            nixtla_conn_id='nixtla_api'
        )
    """

    template_fields = ('dataset', 'output_table', 'execution_date')
    ui_color = '#4A90E2'
    ui_fgcolor = '#FFFFFF'

    @apply_defaults
    def __init__(
        self,
        dataset: str,
        horizon: int,
        models: Optional[List[str]] = None,
        freq: str = 'D',
        output_table: Optional[str] = None,
        nixtla_conn_id: str = 'nixtla_api',
        level: Optional[List[int]] = None,
        finetune_steps: Optional[int] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.dataset = dataset
        self.horizon = horizon
        self.models = models or ['TimeGPT']
        self.freq = freq
        self.output_table = output_table
        self.nixtla_conn_id = nixtla_conn_id
        self.level = level or [80, 90, 95]
        self.finetune_steps = finetune_steps

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute forecast task"""
        self.log.info(f"Starting Nixtla forecast for {self.dataset}")

        # Initialize hook
        hook = NixtlaHook(nixtla_conn_id=self.nixtla_conn_id)

        # Load data
        self.log.info(f"Loading data from {self.dataset}")
        df = hook.load_data(self.dataset)

        self.log.info(f"Loaded {len(df)} rows, {df['unique_id'].nunique()} series")

        # Run forecast
        self.log.info(f"Running forecast with horizon={self.horizon}")
        forecasts = hook.forecast(
            df=df,
            horizon=self.horizon,
            freq=self.freq,
            level=self.level,
            finetune_steps=self.finetune_steps
        )

        self.log.info(f"Generated {len(forecasts)} forecast points")

        # Write results
        if self.output_table:
            self.log.info(f"Writing forecasts to {self.output_table}")
            hook.write_forecasts(forecasts, self.output_table)

        # Push to XCom for downstream tasks
        return {
            'forecast_count': len(forecasts),
            'series_count': df['unique_id'].nunique(),
            'output_table': self.output_table
        }
```

#### hooks/nixtla.py

```python
"""
NixtlaHook - Handle Nixtla API authentication and operations
"""
from typing import Optional, Dict, Any, List
import pandas as pd
from airflow.hooks.base import BaseHook
from nixtla import NixtlaClient


class NixtlaHook(BaseHook):
    """
    Interact with Nixtla TimeGPT API

    Handles:
    - API authentication
    - Retry logic
    - Data loading from various sources
    - Forecast execution
    - Result writing
    """

    conn_name_attr = 'nixtla_conn_id'
    default_conn_name = 'nixtla_api'
    conn_type = 'http'
    hook_name = 'Nixtla'

    def __init__(self, nixtla_conn_id: str = default_conn_name):
        super().__init__()
        self.nixtla_conn_id = nixtla_conn_id
        self._client = None

    def get_conn(self) -> NixtlaClient:
        """Get authenticated Nixtla client"""
        if self._client is None:
            # Get connection details from Airflow
            conn = self.get_connection(self.nixtla_conn_id)
            api_key = conn.password

            self._client = NixtlaClient(api_key=api_key)
            self.log.info("Nixtla client initialized")

        return self._client

    def forecast(
        self,
        df: pd.DataFrame,
        horizon: int,
        freq: str = 'D',
        level: Optional[List[int]] = None,
        finetune_steps: Optional[int] = None
    ) -> pd.DataFrame:
        """Run forecast via TimeGPT API"""
        client = self.get_conn()

        try:
            forecasts = client.forecast(
                df=df,
                h=horizon,
                freq=freq,
                level=level or [80, 90, 95],
                finetune_steps=finetune_steps
            )

            self.log.info(f"Forecast successful: {len(forecasts)} points")
            return forecasts

        except Exception as e:
            self.log.error(f"Forecast failed: {e}")
            raise

    def load_data(self, source: str) -> pd.DataFrame:
        """
        Load data from various sources

        Supports:
        - BigQuery: 'bigquery.project.dataset.table'
        - Snowflake: 'snowflake.database.schema.table'
        - SQL query: 'query: SELECT ...'
        - Local file: 'file:/path/to/data.csv'
        """
        if source.startswith('bigquery.'):
            return self._load_from_bigquery(source)
        elif source.startswith('snowflake.'):
            return self._load_from_snowflake(source)
        elif source.startswith('query:'):
            return self._load_from_query(source[6:].strip())
        elif source.startswith('file:'):
            return pd.read_csv(source[5:])
        else:
            raise ValueError(f"Unsupported data source: {source}")

    def _load_from_bigquery(self, table_ref: str) -> pd.DataFrame:
        """Load from BigQuery"""
        from google.cloud import bigquery

        # Parse: bigquery.project.dataset.table
        parts = table_ref.split('.')
        if len(parts) != 4:
            raise ValueError(f"Invalid BigQuery ref: {table_ref}")

        _, project, dataset, table = parts
        full_ref = f"{project}.{dataset}.{table}"

        client = bigquery.Client(project=project)
        query = f"SELECT * FROM `{full_ref}`"

        self.log.info(f"Loading from BigQuery: {full_ref}")
        df = client.query(query).to_dataframe()

        return df

    def write_forecasts(self, forecasts: pd.DataFrame, destination: str):
        """Write forecasts to destination"""
        if destination.startswith('bigquery.'):
            self._write_to_bigquery(forecasts, destination)
        elif destination.startswith('snowflake.'):
            self._write_to_snowflake(forecasts, destination)
        else:
            raise ValueError(f"Unsupported destination: {destination}")
```

---

## Example DAG

```python
"""
Example Airflow DAG using Nixtla operators
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow_providers_nixtla.operators.forecast import NixtlaForecastOperator
from airflow_providers_nixtla.operators.anomaly import NixtlaAnomalyOperator


default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 11, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_sales_forecast',
    default_args=default_args,
    description='Daily sales forecasting with Nixtla TimeGPT',
    schedule_interval='0 6 * * *',  # 6 AM daily
    catchup=False,
    tags=['forecasting', 'nixtla', 'sales'],
) as dag:

    # Task 1: Run forecast
    forecast_task = NixtlaForecastOperator(
        task_id='forecast_sales',
        dataset='bigquery.analytics.sales_history',
        horizon=30,
        freq='D',
        level=[80, 90, 95],
        output_table='forecasts.daily_sales',
        nixtla_conn_id='nixtla_api'
    )

    # Task 2: Detect anomalies
    anomaly_task = NixtlaAnomalyOperator(
        task_id='detect_anomalies',
        dataset='bigquery.analytics.sales_history',
        threshold=3.0,
        output_table='anomalies.daily_sales',
        nixtla_conn_id='nixtla_api'
    )

    # Task 3: Notify team
    def notify_completion(**context):
        forecast_results = context['task_instance'].xcom_pull(task_ids='forecast_sales')
        print(f"Forecast complete: {forecast_results['forecast_count']} points")

    notify_task = PythonOperator(
        task_id='notify_completion',
        python_callable=notify_completion,
        provide_context=True
    )

    # DAG dependencies
    [forecast_task, anomaly_task] >> notify_task
```

---

## User Journey

### Journey 1: Migrate from PythonOperator

**Persona**: Carlos, Data Engineer
**Goal**: Replace brittle PythonOperator with native Nixtla operator
**Context**: Has 10 DAGs using PythonOperator + manual Nixtla SDK calls

**Before (PythonOperator)**:
```python
def run_forecast(**context):
    import os
    import pandas as pd
    from nixtla import NixtlaClient
    from google.cloud import bigquery

    # Manual setup
    api_key = os.getenv('NIXTLA_API_KEY')
    client = NixtlaClient(api_key=api_key)

    # Manual data loading
    bq_client = bigquery.Client()
    query = "SELECT * FROM analytics.sales"
    df = bq_client.query(query).to_dataframe()

    # Manual forecast
    forecasts = client.forecast(df=df, h=30, freq='D')

    # Manual writing
    forecasts.to_gbq('forecasts.sales', if_exists='replace')

forecast_task = PythonOperator(
    task_id='forecast',
    python_callable=run_forecast
)
```

**After (NixtlaForecastOperator)**:
```python
forecast_task = NixtlaForecastOperator(
    task_id='forecast',
    dataset='bigquery.analytics.sales',
    horizon=30,
    output_table='forecasts.sales',
    nixtla_conn_id='nixtla_api'
)
```

**Outcome**: Reduced from 20 lines to 5 lines. Added automatic retries, connection pooling, and monitoring.

---

## Dependencies

```txt
# requirements.txt
apache-airflow>=2.5.0
nixtla>=0.7.1
pandas>=2.0.0
google-cloud-bigquery>=3.10.0  # Optional
snowflake-connector-python>=3.0.0  # Optional
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-30
**Language**: Pure Python (No TypeScript)
