---
name: nixtla-airflow-dag
description: Generate production-ready Airflow DAG for TimeGPT forecasting
---

# /nixtla-airflow-dag

Generate production-ready Airflow DAG for TimeGPT forecasting.

## Usage

```
/nixtla-airflow-dag [dag_name] [--schedule=@daily] [--source=bigquery]
```

## Workflow

1. Gather DAG requirements
2. Configure data source connection
3. Generate DAG Python file
4. Add monitoring and alerting
5. Create deployment instructions

## Parameters

- `dag_name`: Name of the DAG
- `--schedule`: Airflow schedule (default: @daily)
- `--source`: Data source (bigquery, snowflake, postgres, s3)
- `--alert-email`: Email for failure alerts

## Output

- Complete DAG Python file
- Connection configuration
- Deployment guide
- Test instructions
