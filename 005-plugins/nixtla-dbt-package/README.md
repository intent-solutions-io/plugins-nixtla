# dbt_nixtla

Native dbt package for TimeGPT forecasting.

## Installation

Add to your `packages.yml`:

```yaml
packages:
  - package: nixtla/dbt_nixtla
    version: [">=0.1.0", "<1.0.0"]
```

Then run:

```bash
dbt deps
```

## Configuration

Add to your `dbt_project.yml`:

```yaml
vars:
  nixtla_api_key: "{{ env_var('NIXTLA_API_KEY') }}"
  default_horizon: 14
  default_freq: 'D'
  confidence_levels: [80, 90, 95]
```

## Macros

### nixtla_forecast

Generate forecasts from time series data:

```sql
{{ nixtla_forecast(
    source_table='my_data',
    timestamp_col='ds',
    value_col='y',
    group_by_col='unique_id',
    horizon=30,
    freq='D'
) }}
```

### nixtla_anomaly_detect

Detect anomalies in time series:

```sql
{{ nixtla_anomaly_detect(
    source_table='my_data',
    timestamp_col='ds',
    value_col='y',
    level=95
) }}
```

## Supported Warehouses

| Warehouse | Status | Integration |
|-----------|--------|-------------|
| BigQuery | ✅ Phase 1 | Native UDF |
| Snowflake | ✅ Phase 1 | Native App |
| Databricks | ✅ Phase 1 | Python UDF |
| Redshift | 🔜 Phase 2 | Lambda |

## Example Model

See `models/examples/fct_sales_forecast.sql` for a complete example.

## License

Proprietary - Intent Solutions
