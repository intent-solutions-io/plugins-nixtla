# Quick Start Guide for Max - Nixtla BigQuery Forecaster

**Document**: 002-DR-QREF-max-quick-start-guide.md
**Created**: 2025-11-29
**For**: Max (Nixtla CEO)
**Purpose**: Get the demo running in < 5 minutes

---

## 🎯 What You're About to See

**The Demo**: Nixtla OSS models (AutoETS, AutoTheta) running on Google BigQuery public data, forecasting Chicago taxi trips by payment type, deployed as a Cloud Function.

**The Pitch**: Replace Google's expensive Timeseries Insights API (~$150/month) with Nixtla OSS models (~$10/month). Same results, 90% cost savings.

---

## ✅ Prerequisites Checklist

Before starting, make sure you have:
- [ ] GitHub account access to `intent-solutions-io/plugins-nixtla`
- [ ] TimeGPT API key (already have: `nixak-...`)
- [ ] 5 minutes

That's it! No GCP account needed on your end. Jeremy set everything up.

---

## 🚀 Step 1: Configure GitHub Secrets (2 minutes)

Go to: https://github.com/intent-solutions-io/plugins-nixtla/settings/secrets/actions

Add these **4 secrets** (copy-paste from below):

### Secret 1: `GCP_PROJECT_ID`
```
nixtla-playground-01
```

### Secret 2: `GCP_SA_EMAIL`
```
nixtla-github-deployer@nixtla-playground-01.iam.gserviceaccount.com
```

### Secret 3: `GCP_WORKLOAD_IDENTITY_PROVIDER`
```
projects/859338910722/locations/global/workloadIdentityPools/github-pool/providers/github-provider
```

### Secret 4: `NIXTLA_TIMEGPT_API_KEY`
```
nixak-JNfT4z4JQb9uK3gdAyiWYWSBELdt6iW0PmE0Sy3k8ETAInJkFSPp4gOfyAZrENcGOsKyTqfDmuLghVq9
```

---

## 📦 Step 2: Trigger Deployment (1 minute)

**Option A - Let Jeremy do it:**
Tell Jeremy "push the BigQuery forecaster to main" and he'll trigger the deployment.

**Option B - Do it yourself (if you have push access):**
```bash
git add .
git commit -m "feat: deploy Nixtla BigQuery Forecaster"
git push origin main
```

---

## 👀 Step 3: Watch Deployment (2 minutes)

Go to: https://github.com/intent-solutions-io/plugins-nixtla/actions

You'll see **"Deploy Nixtla BigQuery Forecaster"** workflow running.

**What's happening**:
1. ✅ Authenticate with GCP (keyless, using Workload Identity)
2. ✅ Deploy Cloud Function with Nixtla models
3. ✅ Run test with Chicago taxi data
4. ✅ Green checkmark = success

**Typical deployment time**: 90-120 seconds

---

## 🧪 Step 4: Test the Demo

Once deployment succeeds, the workflow outputs a **Function URL**.

### Example Test Command

```bash
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
    "limit": 1000,
    "models": ["AutoETS", "AutoTheta"]
  }'
```

### What This Does

1. Queries **BigQuery public dataset** (Chicago taxi trips)
2. Groups by **payment type** (Cash, Credit Card, etc.)
3. Runs **AutoETS and AutoTheta** forecasts
4. Predicts **next 7 days**
5. Returns JSON with forecasts

---

## 📊 Expected Output

```json
{
  "status": "success",
  "metadata": {
    "source_table": "bigquery-public-data.chicago_taxi_trips.taxi_trips",
    "rows_read": 1000,
    "unique_series": 4,
    "horizon": 7,
    "models_used": ["AutoETS", "AutoTheta"],
    "forecast_points_generated": 56
  },
  "forecasts": [
    {
      "unique_id": "Cash",
      "ds": "2025-11-30",
      "AutoETS": 12.45,
      "AutoTheta": 12.38
    },
    ...
  ]
}
```

---

## 🎯 Demo Talking Points for Max

### 1. Cost Savings
- **Google Timeseries Insights**: ~$150/month
- **Nixtla OSS on Cloud Functions**: ~$10/month
- **Savings**: 90%

### 2. Transparency
- **Google**: Black-box proprietary models
- **Nixtla**: Open source AutoETS, AutoTheta, SeasonalNaive
- **Value**: Full visibility into forecasting methodology

### 3. Flexibility
- **Google**: Fixed API, limited customization
- **Nixtla**: Swap models, tune parameters, add custom logic
- **Value**: Adapt to specific use cases

### 4. Integration
- **Works with**: BigQuery (already used by enterprises)
- **No lock-in**: Can run anywhere (Cloud Functions, Cloud Run, local)
- **Value**: Enterprise-friendly architecture

### 5. Scale
- **Cloud Functions**: Auto-scales with demand
- **BigQuery**: Handles petabyte-scale data
- **Value**: Production-ready from day one

---

## 🔍 Optional: Add TimeGPT Comparison

Want to show TimeGPT vs OSS models side-by-side?

Add `"include_timegpt": true` to the test payload:

```json
{
  "project_id": "bigquery-public-data",
  "dataset": "chicago_taxi_trips",
  "table": "taxi_trips",
  "timestamp_col": "trip_start_timestamp",
  "value_col": "trip_total",
  "group_by": "payment_type",
  "horizon": 7,
  "limit": 1000,
  "models": ["AutoETS", "AutoTheta"],
  "include_timegpt": true
}
```

**Result**: Forecast output includes TimeGPT column alongside OSS models.

---

## 🛠️ Troubleshooting

### Deployment fails with "API not enabled"
- **Solution**: APIs are already enabled, re-run workflow

### GitHub Actions authentication failed
- **Solution**: Double-check all 4 secrets are set correctly
- **Note**: No trailing spaces in secret values

### Function timeout
- **Solution**: Reduce `limit` parameter (try 500 instead of 1000)

### "No data found"
- **Solution**: Check `where_clause` isn't too restrictive
- **Default**: No where clause = all available data

---

## 📱 Quick Links

- **GCP Console**: https://console.cloud.google.com/home/dashboard?project=nixtla-playground-01
- **Cloud Functions**: https://console.cloud.google.com/functions?project=nixtla-playground-01
- **BigQuery**: https://console.cloud.google.com/bigquery?project=nixtla-playground-01
- **GitHub Actions**: https://github.com/intent-solutions-io/plugins-nixtla/actions
- **GitHub Secrets**: https://github.com/intent-solutions-io/plugins-nixtla/settings/secrets/actions

---

## ⏱️ Timeline Summary

| Step | Time | Status |
|------|------|--------|
| Configure GitHub secrets | 2 min | ⏳ Pending |
| Trigger deployment | 1 min | ⏳ Pending |
| Watch deployment | 2 min | ⏳ Pending |
| Test demo | 1 min | ⏳ Pending |
| **Total** | **< 5 min** | |

---

## 💡 Next Steps After Demo

1. **Try different datasets**:
   - Bitcoin transactions
   - COVID-19 data
   - Your own BigQuery tables

2. **Customize models**:
   - Add more statsforecast models
   - Tune hyperparameters
   - Compare against TimeGPT

3. **Productionize**:
   - Add authentication
   - Implement caching
   - Set up monitoring

4. **Scale**:
   - Process millions of rows
   - Multi-region deployment
   - Add batch processing

---

**Ready?** Start with Step 1: Configure GitHub secrets. The whole demo runs in < 5 minutes.

**Questions?** jeremy@intentsolutions.io
