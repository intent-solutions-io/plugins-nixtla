# Nixtla Airflow Operator

Generate production-ready Airflow DAGs for TimeGPT forecasting.

## Features

- **DAG Generation**: Production-ready Python DAG files
- **Multiple Sources**: BigQuery, Snowflake, Postgres, S3
- **Monitoring**: Built-in alerting and retries
- **Testing**: Auto-generated test files

## Quick Start

```bash
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-airflow-dag my_forecast_dag --schedule=@daily --source=bigquery
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `generate_dag` | Generate Airflow DAG Python file |
| `validate_dag` | Validate DAG syntax |
| `configure_connection` | Set up data source connection |
| `generate_tests` | Create DAG test file |

## License

Proprietary - Intent Solutions
