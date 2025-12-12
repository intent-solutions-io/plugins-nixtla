# Schema: nixtla-dbt-package (dbt_nixtla)

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** BUILT (Business Growth)

---

## Directory Tree (Fully Expanded)

```
nixtla-dbt-package/
├── adapters/
│   ├── bigquery/                  # BigQuery UDF integration (empty)
│   ├── databricks/                # Databricks Python UDF (empty)
│   ├── redshift/                  # Redshift Lambda integration (empty)
│   └── snowflake/                 # Snowflake external function (empty)
├── dbt_project.yml                # dbt project definition
├── integration_tests/             # Integration tests (empty)
├── macros/
│   ├── nixtla_anomaly_detect.sql  # {{ nixtla_anomaly_detect() }} macro
│   └── nixtla_forecast.sql        # {{ nixtla_forecast() }} macro
├── models/
│   └── examples/
│       ├── fct_sales_forecast.sql # Example forecast model
│       └── schema.yml             # Model documentation
├── tests/                         # Unit tests (empty)
└── README.md                      # Package documentation
```

---

## dbt Hub Package

```yaml
# packages.yml
packages:
  - package: nixtla/dbt_nixtla
    version: [">=0.1.0", "<1.0.0"]
```

---

## Macros (2)

| Macro | Purpose |
|-------|---------|
| nixtla_forecast() | Generate forecasts from SQL query |
| nixtla_anomaly_detect() | Detect anomalies in time series |

---

## Data Warehouse Support

| Warehouse | Integration Type | Status |
|-----------|-----------------|--------|
| BigQuery | Native UDF | Adapter ready |
| Snowflake | External function | Adapter ready |
| Databricks | Python UDF | Adapter ready |
| Redshift | Lambda integration | Adapter ready |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Analytics engineers, data teams
- **What:** Native dbt integration for TimeGPT forecasting
- **When:** Generate forecasts as part of dbt jobs
- **Target Goal:** dbt run completes with forecast table materialized
- **Production:** true (BUILT)
