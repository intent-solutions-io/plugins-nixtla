# Nixtla Playground Setup Guide

**Goal**: Deploy Nixtla BigQuery Forecaster to Google Cloud with GitHub Actions

**Time**: 15-20 minutes

---

## Prerequisites

✅ You have:
- Google Cloud account with billing enabled
- GitHub account (you own `intent-solutions-io/plugins-nixtla`)
- gcloud CLI installed
- TimeGPT API key from Max

---

## Step-by-Step Setup

### Step 1: Run GCP Setup Script (10 minutes)

This script creates the "Nixtla Playground" GCP project and configures everything.

```bash
cd /home/jeremy/000-projects/nixtla

# Run setup script
./scripts/setup-gcp-nixtla-playground.sh
```

**What it does**:
1. ✅ Creates GCP project `nixtla-playground-XXXXXX`
2. ✅ Enables BigQuery, Cloud Functions, Cloud Run APIs
3. ✅ Creates service account `nixtla-github-deployer`
4. ✅ Sets up Workload Identity Federation (keyless GitHub Actions)
5. ✅ Configures IAM permissions
6. ✅ Outputs GitHub secrets to configure

**You'll be prompted for**:
- Billing account ID (choose one from the list shown)

**Script output**: At the end, you'll see the GitHub secrets you need to add.

---

### Step 2: Configure GitHub Secrets (5 minutes)

Go to: https://github.com/intent-solutions-io/plugins-nixtla/settings/secrets/actions

Click **"New repository secret"** and add these 4 secrets:

#### Secret 1: `GCP_PROJECT_ID`
```
nixtla-playground-XXXXXX
```
(Get this from script output)

#### Secret 2: `GCP_SA_EMAIL`
```
nixtla-github-deployer@nixtla-playground-XXXXXX.iam.gserviceaccount.com
```
(Get this from script output)

#### Secret 3: `GCP_WORKLOAD_IDENTITY_PROVIDER`
```
projects/123456789/locations/global/workloadIdentityPools/github-pool/providers/github-provider
```
(Get this from script output)

#### Secret 4: `NIXTLA_TIMEGPT_API_KEY`
```
nixak-JNfT4z4JQb9uK3gdAyiWYWSBELdt6iW0PmE0Sy3k8ETAInJkFSPp4gOfyAZrENcGOsKyTqfDmuLghVq9
```
(TimeGPT API key from Max)

---

### Step 3: Deploy to Cloud (Automatic)

Once GitHub secrets are configured:

```bash
# Commit and push the new plugin
git add plugins/nixtla-bigquery-forecaster
git add .github/workflows/deploy-bigquery-forecaster.yml
git commit -m "feat: add Nixtla BigQuery Forecaster plugin with GCP deployment"
git push origin main
```

**What happens**:
1. GitHub Actions workflow triggers automatically
2. Authenticates with GCP via Workload Identity (no keys!)
3. Deploys Cloud Function to `nixtla-playground-XXXXXX`
4. Runs test to verify deployment

**Check deployment**:
- Go to: https://github.com/intent-solutions-io/plugins-nixtla/actions
- Watch the workflow run
- Green checkmark = successful deployment

---

## Verify Setup

### Test Local Plugin

```bash
cd /home/jeremy/000-projects/nixtla

# Source GCP config
source nixtla-playground-config.env

# Test BigQuery connector
cd plugins/nixtla-bigquery-forecaster
python src/bigquery_connector.py
```

### Test Cloud Function

```bash
# Get Cloud Function URL
FUNCTION_URL=$(gcloud functions describe nixtla-bigquery-forecast \
  --region=us-central1 \
  --format="value(serviceConfig.uri)")

# Test with curl
curl -X POST "${FUNCTION_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "bigquery-public-data",
    "dataset": "chicago_taxi_trips",
    "table": "taxi_trips",
    "timestamp_col": "trip_start_timestamp",
    "value_col": "trip_total",
    "group_by": "payment_type",
    "horizon": 7,
    "limit": 1000
  }'
```

---

## Troubleshooting

### "Billing account required"

Make sure you've linked a billing account in Step 1:
```bash
gcloud billing accounts list
gcloud billing projects link nixtla-playground-XXXXXX --billing-account=XXXXXX
```

### "API not enabled"

Re-run the API enable commands:
```bash
gcloud services enable bigquery.googleapis.com --project=nixtla-playground-XXXXXX
```

### "GitHub Actions authentication failed"

Check that GitHub secrets are set correctly:
- Go to repo settings → Secrets and variables → Actions
- Verify all 4 secrets are present
- Re-run the workflow

---

## What You've Built

✅ **GCP Project**: `nixtla-playground-XXXXXX`
✅ **BigQuery**: Ready to query public datasets
✅ **Cloud Function**: Serverless Nixtla forecasting endpoint
✅ **GitHub Actions**: Automatic deployment on push
✅ **Workload Identity**: Keyless authentication (no JSON keys!)

---

## Next Steps

1. **Test the plugin in Claude Code**:
   ```
   /nixtla-bigquery-forecast project_id=bigquery-public-data ...
   ```

2. **Show Max the demo**:
   - Pull 100k+ rows from BigQuery
   - Run statsforecast baselines
   - Compare with TimeGPT
   - Write forecasts back to BigQuery

3. **Iterate based on feedback**:
   - Add more models
   - Improve error handling
   - Add visualizations

---

## Resources

- **GCP Console**: https://console.cloud.google.com/home/dashboard?project=nixtla-playground-XXXXXX
- **GitHub Actions**: https://github.com/intent-solutions-io/plugins-nixtla/actions
- **BigQuery**: https://console.cloud.google.com/bigquery?project=nixtla-playground-XXXXXX

---

**Questions?** jeremy@intentsolutions.io

**Sponsor**: Max Mergenthaler (Nixtla) - max@nixtla.io
