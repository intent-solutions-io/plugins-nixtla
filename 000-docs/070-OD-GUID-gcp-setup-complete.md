# ✅ GCP Setup Complete - Nixtla Playground

**Project Created**: `nixtla-playground-01`
**Date**: 2025-11-29
**Status**: Ready for deployment

---

## 📋 Summary

Successfully created and configured Google Cloud project for Nixtla BigQuery Forecaster plugin with:
- ✅ Project: `nixtla-playground-01`
- ✅ Billing: Linked to My Billing Account
- ✅ APIs: 8 services enabled
- ✅ Service Account: `nixtla-github-deployer`
- ✅ IAM Roles: 6 permissions granted
- ✅ Workload Identity Federation: Configured (keyless GitHub Actions)

---

## 🔑 GitHub Secrets Configuration

Go to: https://github.com/jeremylongshore/claude-code-plugins-nixtla/settings/secrets/actions

Click **"New repository secret"** and add these **4 secrets**:

### 1. `GCP_PROJECT_ID`
```
nixtla-playground-01
```

### 2. `GCP_SA_EMAIL`
```
nixtla-github-deployer@nixtla-playground-01.iam.gserviceaccount.com
```

### 3. `GCP_WORKLOAD_IDENTITY_PROVIDER`
```
projects/859338910722/locations/global/workloadIdentityPools/github-pool/providers/github-provider
```

### 4. `NIXTLA_TIMEGPT_API_KEY`
```
nixak-JNfT4z4JQb9uK3gdAyiWYWSBELdt6iW0PmE0Sy3k8ETAInJkFSPp4gOfyAZrENcGOsKyTqfDmuLghVq9
```

---

## 🚀 Next Steps

### 1. Configure GitHub Secrets (5 minutes)
Add the 4 secrets above to GitHub repository settings.

### 2. Commit & Push to Deploy (Automatic)
```bash
cd /home/jeremy/000-projects/nixtla

# Add new plugin files
git add plugins/nixtla-bigquery-forecaster/
git add .github/workflows/deploy-bigquery-forecaster.yml

# Commit
git commit -m "feat: add Nixtla BigQuery Forecaster with Cloud Functions deployment"

# Push to trigger deployment
git push origin main
```

### 3. Monitor Deployment
- Go to: https://github.com/jeremylongshore/claude-code-plugins-nixtla/actions
- Watch the **"Deploy Nixtla BigQuery Forecaster"** workflow
- Green checkmark = successful deployment

### 4. Get Cloud Function URL
```bash
gcloud functions describe nixtla-bigquery-forecast \
  --region=us-central1 \
  --project=nixtla-playground-01 \
  --gen2 \
  --format="value(serviceConfig.uri)"
```

### 5. Test Deployment
```bash
# Example: Forecast Chicago taxi trips by payment type
curl -X POST "FUNCTION_URL" \
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

## 🏗️ Infrastructure Details

### GCP Project
- **Project ID**: `nixtla-playground-01`
- **Project Number**: `859338910722`
- **Project Name**: Nixtla Playground
- **Region**: us-central1

### Enabled APIs
1. BigQuery API (`bigquery.googleapis.com`)
2. Cloud Functions API (`cloudfunctions.googleapis.com`)
3. Cloud Build API (`cloudbuild.googleapis.com`)
4. Cloud Run API (`run.googleapis.com`)
5. Artifact Registry API (`artifactregistry.googleapis.com`)
6. IAM Credentials API (`iamcredentials.googleapis.com`)
7. Cloud Resource Manager API (`cloudresourcemanager.googleapis.com`)
8. IAM API (`iam.googleapis.com`)

### Service Account
- **Name**: `nixtla-github-deployer`
- **Email**: `nixtla-github-deployer@nixtla-playground-01.iam.gserviceaccount.com`

### IAM Roles Granted
1. `roles/cloudfunctions.admin` - Deploy and manage Cloud Functions
2. `roles/run.admin` - Manage Cloud Run services
3. `roles/bigquery.admin` - Full BigQuery access
4. `roles/iam.serviceAccountUser` - Use service accounts
5. `roles/artifactregistry.admin` - Manage container images
6. `roles/storage.admin` - Cloud Storage access

### Workload Identity Federation
- **Pool**: `github-pool`
- **Provider**: `github-provider`
- **Repository**: `jeremylongshore/claude-code-plugins-nixtla`
- **Authentication**: Keyless (no JSON keys required)

---

## 📊 Cost Estimate

**Monthly cost estimate** (with moderate usage):

| Service | Usage | Cost |
|---------|-------|------|
| Cloud Functions | 1M invocations, 2GB RAM | ~$5 |
| BigQuery | 10 GB processed/month | ~$0.50 |
| Cloud Storage | 1 GB storage | ~$0.02 |
| **Total** | | **~$5.50/month** |

**Free tier includes**:
- 2M Cloud Function invocations/month
- 10 GB BigQuery storage
- 1 TB BigQuery queries/month

**For demo purposes**: Should stay within free tier limits.

---

## 🔗 Quick Links

- **GCP Console**: https://console.cloud.google.com/home/dashboard?project=nixtla-playground-01
- **BigQuery**: https://console.cloud.google.com/bigquery?project=nixtla-playground-01
- **Cloud Functions**: https://console.cloud.google.com/functions?project=nixtla-playground-01
- **GitHub Actions**: https://github.com/jeremylongshore/claude-code-plugins-nixtla/actions
- **GitHub Secrets**: https://github.com/jeremylongshore/claude-code-plugins-nixtla/settings/secrets/actions

---

## 🎯 Demo Datasets to Try

### 1. Chicago Taxi Trips (Recommended)
- **Project**: `bigquery-public-data`
- **Dataset**: `chicago_taxi_trips`
- **Table**: `taxi_trips`
- **Size**: 200M+ trips
- **Use Case**: Forecast demand by payment type or company

### 2. Bitcoin Transactions
- **Project**: `bigquery-public-data`
- **Dataset**: `crypto_bitcoin`
- **Table**: `transactions`
- **Size**: 500M+ transactions
- **Use Case**: Forecast transaction volume patterns

### 3. COVID-19 Data
- **Project**: `bigquery-public-data`
- **Dataset**: `covid19_open_data`
- **Table**: `covid19_open_data`
- **Size**: 1M+ records
- **Use Case**: Forecast cases by country

---

## 📝 Local Development

To use this project locally:

```bash
# Source the config
source nixtla-playground-config.env

# Set GCP project
gcloud config set project nixtla-playground-01

# Test BigQuery connector
cd plugins/nixtla-bigquery-forecaster
python src/bigquery_connector.py
```

---

## ⚠️ Important Notes

1. **No JSON Keys**: This setup uses Workload Identity Federation (keyless authentication)
2. **GitHub Only**: Deployment triggers automatically on push to `main` branch
3. **Public Function**: The Cloud Function is publicly accessible (allow-unauthenticated)
4. **API Key Security**: TimeGPT API key is stored as GitHub secret (encrypted)

---

## 🛟 Troubleshooting

### Deployment fails with "API not enabled"
```bash
gcloud services enable bigquery.googleapis.com --project=nixtla-playground-01
```

### GitHub Actions authentication failed
- Verify all 4 GitHub secrets are set correctly
- Check repository name matches: `jeremylongshore/claude-code-plugins-nixtla`
- Re-run the workflow

### Function deployment timeout
- Check Cloud Build logs: https://console.cloud.google.com/cloud-build/builds?project=nixtla-playground-01
- Increase timeout in workflow (default: 540s)

---

**Setup complete!** Ready to configure GitHub secrets and deploy.

**Configuration saved**: `nixtla-playground-config.env`
