# Quickstart

**Requires**: GCP credentials with BigQuery access

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Authenticate (one of these)
gcloud auth application-default login          # Personal
export GOOGLE_APPLICATION_CREDENTIALS=key.json # Service account

# Run test
python scripts/test_local.py
```

**Expected output:** `ALL TESTS PASSED!`

## What It Does

Queries BigQuery public data (Chicago taxi trips) → runs statsforecast → returns forecasts.

## GCP Requirements

- Project: `nixtla-playground-01` (or your own)
- APIs enabled: BigQuery API
- Permissions: `bigquery.jobs.create`, `bigquery.tables.getData`

## Test Without GCP

Can't run locally without credentials. The Cloud Function deploys via GitHub Actions with Workload Identity Federation.

## Files

```
nixtla-bigquery-forecaster/
├── src/
│   ├── main.py              # Cloud Function entry
│   ├── bigquery_connector.py
│   └── forecaster.py
├── scripts/
│   └── test_local.py        # Local test
├── requirements.txt
└── README.md
```
