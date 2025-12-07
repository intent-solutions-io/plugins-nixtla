"""
Local test of BigQuery connector and Nixtla forecaster
"""
import sys
sys.path.insert(0, 'src')

from bigquery_connector import BigQueryConnector
from forecaster import NixtlaForecaster
import pandas as pd

print("=" * 60)
print("Testing Nixtla BigQuery Forecaster")
print("=" * 60)

# Test 1: Connect to BigQuery (use OUR project for billing)
print("\n1. Testing BigQuery Connector...")
try:
    connector = BigQueryConnector(project_id="nixtla-playground-01")
    print("✅ BigQuery client initialized")
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

# Test 2: Read Chicago taxi data - use wider date range
print("\n2. Reading Chicago taxi data (small sample)...")
print("   Source: bigquery-public-data")
print("   Billing: nixtla-playground-01")
try:
    df = connector.read_timeseries(
        dataset="chicago_taxi_trips",
        table="taxi_trips", 
        timestamp_col="trip_start_timestamp",
        value_col="trip_total",
        group_by="payment_type",
        where_clause="trip_start_timestamp BETWEEN '2023-01-01' AND '2023-01-31' AND trip_total > 0",
        limit=1000,
        source_project="bigquery-public-data"
    )
    print(f"✅ Read {len(df)} rows")
    print(f"✅ Unique series: {df['unique_id'].nunique()}")
    if len(df) > 0:
        print(f"\nPayment types: {df['unique_id'].unique().tolist()}")
        print(f"\nData types:\n{df.dtypes}")
        print(f"\nSample:")
        print(df.head())
        
        # Ensure ds is datetime
        df['ds'] = pd.to_datetime(df['ds'])
        print(f"\n✅ Converted 'ds' to datetime")
    else:
        print("❌ No data returned, check query")
        sys.exit(1)
except Exception as e:
    print(f"❌ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Run Nixtla forecasts
print("\n3. Running Nixtla statsforecast...")
try:
    forecaster = NixtlaForecaster()
    forecasts = forecaster.forecast(
        df=df,
        horizon=7,
        models=["AutoETS", "AutoTheta"],
        freq="D"
    )
    print(f"✅ Generated {len(forecasts)} forecast points")
    print(f"\nColumns: {forecasts.columns.tolist()}")
    print(f"\nSample forecasts:")
    print(forecasts.head(14))
except Exception as e:
    print(f"❌ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nPlugin verified:")
print("  ✅ BigQuery public data access")
print("  ✅ Nixtla statsforecast integration")
print("  ✅ AutoETS and AutoTheta models")
print("\nReady for deployment!")
