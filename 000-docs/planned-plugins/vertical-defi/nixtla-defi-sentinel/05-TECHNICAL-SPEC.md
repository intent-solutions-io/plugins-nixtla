# Nixtla DeFi Sentinel - Technical Specification

**Plugin ID:** nixtla-defi-sentinel
**Category:** Growth - New Market Entry
**Created:** 2025-12-02
**Status:** Specified
**Version:** 1.0

---

## Executive Summary

This document provides detailed technical specifications for **Nixtla DeFi Sentinel**, including API contracts, data schemas, algorithms, and implementation details. This spec is intended for engineering teams implementing the system.

**Specification Scope:**
- REST API endpoints with request/response schemas
- Database schemas (PostgreSQL, InfluxDB)
- Anomaly detection algorithm implementation
- MCP server protocol implementation
- Claude Code plugin structure
- Integration specifications (Slack, Email, Webhooks)
- Security implementation details
- Performance requirements and optimization strategies

---

## Table of Contents

1. [API Specification](#api-specification)
2. [Data Models & Schemas](#data-models--schemas)
3. [Anomaly Detection Algorithm](#anomaly-detection-algorithm)
4. [MCP Server Implementation](#mcp-server-implementation)
5. [Claude Code Plugin](#claude-code-plugin)
6. [Integration Specifications](#integration-specifications)
7. [Security Implementation](#security-implementation)
8. [Performance & Optimization](#performance--optimization)
9. [Testing Strategy](#testing-strategy)
10. [Deployment Specifications](#deployment-specifications)

---

## API Specification

### Base URL
- **Production**: `https://api.nixtla-defi-sentinel.com/v1`
- **Staging**: `https://api-staging.nixtla-defi-sentinel.com/v1`
- **Local Dev**: `http://localhost:8000/v1`

### Authentication
All requests require `Authorization` header with API key:
```
Authorization: Bearer nixtla_sk_live_abc123...
```

### Common Response Codes

| Code | Meaning | Response Body |
|------|---------|---------------|
| 200 | Success | JSON with data |
| 201 | Created | JSON with created resource |
| 400 | Bad Request | `{"error": "Invalid parameter: ...", "code": "INVALID_PARAM"}` |
| 401 | Unauthorized | `{"error": "Invalid API key", "code": "INVALID_API_KEY"}` |
| 403 | Forbidden | `{"error": "Insufficient permissions", "code": "FORBIDDEN"}` |
| 404 | Not Found | `{"error": "Resource not found", "code": "NOT_FOUND"}` |
| 429 | Rate Limited | `{"error": "Rate limit exceeded", "code": "RATE_LIMIT", "retry_after": 60}` |
| 500 | Server Error | `{"error": "Internal server error", "code": "SERVER_ERROR"}` |

---

### Endpoints

#### 1. Contracts

##### `GET /contracts`
List all monitored contracts for authenticated user.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `chain` | string | No | all | Filter by chain: `ethereum`, `bsc`, `base`, `all` |
| `status` | string | No | all | Filter by status: `active`, `paused`, `all` |
| `limit` | integer | No | 50 | Results per page (max 100) |
| `offset` | integer | No | 0 | Pagination offset |

**Response:**
```json
{
  "data": [
    {
      "contract_id": "ctr_abc123",
      "address": "0x1234567890abcdef1234567890abcdef12345678",
      "chain": "ethereum",
      "label": "Uniswap V3: USDC/ETH Pool",
      "monitoring_enabled": true,
      "created_at": "2025-12-01T10:30:00Z",
      "last_checked_at": "2025-12-02T15:45:32Z",
      "metrics": {
        "tvl": 1250000.50,
        "transaction_count_24h": 3421,
        "anomaly_count_30d": 5
      }
    }
  ],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "total": 127
  }
}
```

---

##### `POST /contracts`
Add a new contract to monitor.

**Request Body:**
```json
{
  "address": "0x1234567890abcdef1234567890abcdef12345678",
  "chain": "ethereum",
  "label": "Uniswap V3: USDC/ETH Pool",
  "monitoring_enabled": true,
  "alert_thresholds": {
    "tvl_drop_percent": 10,
    "tx_volume_spike_stddev": 3,
    "gas_anomaly_threshold": 2
  }
}
```

**Validation Rules:**
- `address`: Must be valid Ethereum address (0x + 40 hex chars)
- `chain`: Must be one of: `ethereum`, `bsc`, `base`
- `label`: Optional, max 100 characters
- `alert_thresholds`: Optional, uses defaults if not provided

**Response:** `201 Created`
```json
{
  "contract_id": "ctr_abc123",
  "address": "0x1234567890abcdef1234567890abcdef12345678",
  "chain": "ethereum",
  "label": "Uniswap V3: USDC/ETH Pool",
  "monitoring_enabled": true,
  "created_at": "2025-12-02T16:00:00Z",
  "message": "Contract added successfully. Monitoring will begin within 60 seconds."
}
```

**Error Cases:**
- `400 INVALID_ADDRESS`: Address is not valid hex format
- `400 CONTRACT_NOT_FOUND`: Contract does not exist on specified chain
- `409 ALREADY_MONITORED`: Contract is already being monitored by this customer
- `403 TIER_LIMIT_EXCEEDED`: Customer tier allows max 5 contracts, already monitoring 5

---

##### `GET /contracts/{contract_id}`
Get detailed information about a specific contract.

**Path Parameters:**
- `contract_id`: UUID of the contract

**Response:**
```json
{
  "contract_id": "ctr_abc123",
  "address": "0x1234567890abcdef1234567890abcdef12345678",
  "chain": "ethereum",
  "label": "Uniswap V3: USDC/ETH Pool",
  "monitoring_enabled": true,
  "created_at": "2025-12-01T10:30:00Z",
  "last_checked_at": "2025-12-02T15:45:32Z",
  "metrics": {
    "current": {
      "tvl": 1250000.50,
      "transaction_count": 3421,
      "gas_used": 125000000,
      "unique_users": 847
    },
    "24h_change": {
      "tvl_percent": -2.5,
      "transaction_count_percent": 15.3,
      "gas_used_percent": -5.1
    }
  },
  "alert_thresholds": {
    "tvl_drop_percent": 10,
    "tx_volume_spike_stddev": 3,
    "gas_anomaly_threshold": 2
  },
  "anomaly_summary": {
    "last_7_days": 2,
    "last_30_days": 5,
    "last_anomaly_at": "2025-12-01T08:15:00Z"
  }
}
```

---

##### `PUT /contracts/{contract_id}`
Update contract monitoring settings.

**Request Body:**
```json
{
  "label": "Uniswap V3: USDC/ETH Pool (Updated Label)",
  "monitoring_enabled": false,
  "alert_thresholds": {
    "tvl_drop_percent": 15
  }
}
```

**Response:** `200 OK`
```json
{
  "contract_id": "ctr_abc123",
  "message": "Contract updated successfully"
}
```

---

##### `DELETE /contracts/{contract_id}`
Stop monitoring a contract (soft delete).

**Response:** `200 OK`
```json
{
  "message": "Contract removed from monitoring. Historical data retained for 90 days."
}
```

---

#### 2. Metrics

##### `GET /contracts/{contract_id}/metrics`
Fetch time-series metrics for a contract.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `metric` | string | Yes | - | Metric name: `tvl`, `transaction_count`, `gas_used`, `unique_users` |
| `start_time` | ISO8601 | No | 24h ago | Start of time range |
| `end_time` | ISO8601 | No | now | End of time range |
| `resolution` | string | No | auto | Data resolution: `1min`, `5min`, `1hour`, `1day`, `auto` |

**Response:**
```json
{
  "contract_id": "ctr_abc123",
  "metric": "tvl",
  "resolution": "5min",
  "data_points": [
    {
      "timestamp": "2025-12-02T15:00:00Z",
      "value": 1250000.50,
      "anomaly": false
    },
    {
      "timestamp": "2025-12-02T15:05:00Z",
      "value": 1248500.25,
      "anomaly": false
    },
    {
      "timestamp": "2025-12-02T15:10:00Z",
      "value": 1125000.00,
      "anomaly": true,
      "anomaly_score": 0.92,
      "anomaly_type": "sudden_drop"
    }
  ],
  "time_range": {
    "start": "2025-12-02T00:00:00Z",
    "end": "2025-12-02T16:00:00Z"
  },
  "statistics": {
    "min": 1125000.00,
    "max": 1250000.50,
    "mean": 1230500.25,
    "stddev": 15230.75
  }
}
```

---

#### 3. Anomalies

##### `GET /anomalies`
List detected anomalies across all monitored contracts.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `contract_id` | UUID | No | all | Filter by contract |
| `severity` | string | No | all | Filter by severity: `critical`, `high`, `medium`, `low`, `all` |
| `start_time` | ISO8601 | No | 7d ago | Start of time range |
| `end_time` | ISO8601 | No | now | End of time range |
| `limit` | integer | No | 50 | Results per page |
| `offset` | integer | No | 0 | Pagination offset |

**Response:**
```json
{
  "data": [
    {
      "anomaly_id": "ano_xyz789",
      "contract_id": "ctr_abc123",
      "contract_address": "0x1234...5678",
      "chain": "ethereum",
      "metric": "tvl",
      "anomaly_type": "sudden_drop",
      "severity": "critical",
      "detected_at": "2025-12-02T15:10:00Z",
      "metric_value": 1125000.00,
      "expected_value": 1250000.00,
      "confidence_score": 0.92,
      "description": "TVL dropped 10% in 5 minutes (expected: $1.25M, actual: $1.12M)",
      "context": {
        "similar_to": "Balancer exploit (Nov 2025)",
        "historical_pattern": "This pattern preceded 3 past exploits",
        "other_protocols": "No similar anomalies detected in other DEXes"
      },
      "alert_sent": true,
      "acknowledged_at": "2025-12-02T15:12:00Z",
      "resolved_at": null
    }
  ],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "total": 127
  }
}
```

---

##### `POST /anomalies/{anomaly_id}/acknowledge`
Mark an anomaly as acknowledged.

**Request Body:**
```json
{
  "notes": "False positive: Expected TVL drop due to scheduled withdrawal",
  "feedback": "false_positive"
}
```

**Response:** `200 OK`
```json
{
  "anomaly_id": "ano_xyz789",
  "acknowledged_at": "2025-12-02T15:12:00Z",
  "acknowledged_by": "user@example.com",
  "message": "Anomaly acknowledged. Feedback recorded for model improvement."
}
```

---

##### `POST /anomalies/{anomaly_id}/resolve`
Mark an anomaly as resolved.

**Request Body:**
```json
{
  "resolution": "confirmed_exploit",
  "notes": "Reentrancy attack confirmed. Contract paused at 15:15 UTC.",
  "incident_report_url": "https://..."
}
```

**Response:** `200 OK`
```json
{
  "anomaly_id": "ano_xyz789",
  "resolved_at": "2025-12-02T15:20:00Z",
  "message": "Anomaly resolved"
}
```

---

#### 4. Alerts

##### `GET /alerts`
List alert delivery history.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | string | No | all | Filter by status: `pending`, `sent`, `failed`, `all` |
| `channel` | string | No | all | Filter by channel: `slack`, `email`, `sms`, `webhook`, `all` |
| `limit` | integer | No | 50 | Results per page |
| `offset` | integer | No | 0 | Pagination offset |

**Response:**
```json
{
  "data": [
    {
      "alert_id": "alt_123",
      "anomaly_id": "ano_xyz789",
      "channel": "slack",
      "destination": "https://hooks.slack.com/services/...",
      "status": "sent",
      "created_at": "2025-12-02T15:10:05Z",
      "sent_at": "2025-12-02T15:10:07Z",
      "delivery_latency_ms": 2340
    }
  ],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "total": 543
  }
}
```

---

#### 5. Configuration

##### `GET /config/notification-channels`
List configured notification channels.

**Response:**
```json
{
  "channels": [
    {
      "channel_id": "ch_abc",
      "type": "slack",
      "destination": "https://hooks.slack.com/services/...",
      "enabled": true,
      "min_severity": "medium",
      "created_at": "2025-12-01T10:00:00Z"
    },
    {
      "channel_id": "ch_def",
      "type": "email",
      "destination": "security@example.com",
      "enabled": true,
      "min_severity": "high",
      "created_at": "2025-12-01T10:00:00Z"
    }
  ]
}
```

---

##### `POST /config/notification-channels`
Add a new notification channel.

**Request Body:**
```json
{
  "type": "slack",
  "destination": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX",
  "enabled": true,
  "min_severity": "medium"
}
```

**Validation:**
- `type`: Must be one of: `slack`, `email`, `discord`, `sms`, `webhook`
- `destination`: Format validated based on type (URL, email, phone)
- `min_severity`: Must be one of: `critical`, `high`, `medium`, `low`

**Response:** `201 Created`
```json
{
  "channel_id": "ch_abc",
  "message": "Notification channel added successfully. Test alert sent."
}
```

---

##### `DELETE /config/notification-channels/{channel_id}`
Remove a notification channel.

**Response:** `200 OK`
```json
{
  "message": "Notification channel removed"
}
```

---

#### 6. Reports

##### `GET /reports/roi`
Generate ROI report for specified time period.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_date` | date | No | 30d ago | Start of report period |
| `end_date` | date | No | today | End of report period |

**Response:**
```json
{
  "report_period": {
    "start": "2025-11-02",
    "end": "2025-12-02"
  },
  "summary": {
    "total_contracts_monitored": 15,
    "total_anomalies_detected": 47,
    "critical_anomalies": 5,
    "false_positive_rate": 0.12,
    "estimated_losses_prevented": 350000.00,
    "engineering_hours_saved": 240
  },
  "cost_analysis": {
    "subscription_cost": 5000.00,
    "api_usage_cost": 127.50,
    "total_cost": 5127.50,
    "roi_multiplier": 68.3,
    "break_even_date": "2025-11-05"
  },
  "anomaly_breakdown": [
    {
      "anomaly_type": "tvl_drop",
      "count": 8,
      "avg_severity": "high",
      "estimated_loss_prevented": 150000.00
    },
    {
      "anomaly_type": "gas_spike",
      "count": 12,
      "avg_severity": "medium",
      "estimated_loss_prevented": 50000.00
    }
  ]
}
```

---

## Data Models & Schemas

### PostgreSQL Schema

#### `customers` Table
```sql
CREATE TABLE customers (
  customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  api_key TEXT UNIQUE NOT NULL, -- SHA-256 hashed
  tier TEXT NOT NULL DEFAULT 'starter', -- starter, professional, enterprise
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  suspended_at TIMESTAMPTZ,
  metadata JSONB DEFAULT '{}'::jsonb,

  CONSTRAINT tier_check CHECK (tier IN ('starter', 'professional', 'enterprise'))
);

CREATE INDEX idx_customers_api_key ON customers (api_key);
CREATE INDEX idx_customers_email ON customers (email);
```

---

#### `contracts` Table
```sql
CREATE TABLE contracts (
  contract_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
  address TEXT NOT NULL,
  chain TEXT NOT NULL,
  label TEXT,
  monitoring_enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_checked_at TIMESTAMPTZ,
  deleted_at TIMESTAMPTZ, -- Soft delete

  CONSTRAINT chain_check CHECK (chain IN ('ethereum', 'bsc', 'base')),
  UNIQUE(customer_id, address, chain)
);

CREATE INDEX idx_contracts_customer ON contracts (customer_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_contracts_address_chain ON contracts (address, chain) WHERE deleted_at IS NULL;
```

---

#### `thresholds` Table
```sql
CREATE TABLE thresholds (
  threshold_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contract_id UUID NOT NULL REFERENCES contracts(contract_id) ON DELETE CASCADE,
  metric_name TEXT NOT NULL,
  anomaly_type TEXT NOT NULL,
  threshold_value NUMERIC,
  severity TEXT NOT NULL DEFAULT 'medium',
  enabled BOOLEAN NOT NULL DEFAULT TRUE,

  CONSTRAINT severity_check CHECK (severity IN ('critical', 'high', 'medium', 'low')),
  UNIQUE(contract_id, metric_name, anomaly_type)
);

CREATE INDEX idx_thresholds_contract ON thresholds (contract_id) WHERE enabled = TRUE;
```

---

#### `anomalies` Table
```sql
CREATE TABLE anomalies (
  anomaly_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contract_id UUID NOT NULL REFERENCES contracts(contract_id) ON DELETE CASCADE,
  metric_name TEXT NOT NULL,
  anomaly_type TEXT NOT NULL,
  severity TEXT NOT NULL,
  detected_at TIMESTAMPTZ NOT NULL,
  metric_value NUMERIC NOT NULL,
  expected_value NUMERIC,
  confidence_score NUMERIC NOT NULL, -- 0.0 to 1.0
  description TEXT,
  context JSONB DEFAULT '{}'::jsonb,
  alert_sent BOOLEAN NOT NULL DEFAULT FALSE,
  acknowledged_at TIMESTAMPTZ,
  acknowledged_by TEXT,
  resolved_at TIMESTAMPTZ,
  resolution TEXT,
  feedback TEXT, -- false_positive, confirmed_exploit, expected_behavior

  CONSTRAINT severity_check CHECK (severity IN ('critical', 'high', 'medium', 'low')),
  CONSTRAINT confidence_check CHECK (confidence_score BETWEEN 0 AND 1)
);

-- Partition by month for performance
CREATE INDEX idx_anomalies_contract_detected ON anomalies (contract_id, detected_at DESC);
CREATE INDEX idx_anomalies_severity ON anomalies (severity, detected_at DESC) WHERE resolved_at IS NULL;
```

---

#### `alerts` Table
```sql
CREATE TABLE alerts (
  alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  anomaly_id UUID NOT NULL REFERENCES anomalies(anomaly_id) ON DELETE CASCADE,
  channel_id UUID NOT NULL REFERENCES notification_channels(channel_id),
  status TEXT NOT NULL DEFAULT 'pending', -- pending, sent, failed
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  sent_at TIMESTAMPTZ,
  failed_at TIMESTAMPTZ,
  error_message TEXT,
  delivery_latency_ms INTEGER,
  retry_count INTEGER NOT NULL DEFAULT 0,

  CONSTRAINT status_check CHECK (status IN ('pending', 'sent', 'failed'))
);

CREATE INDEX idx_alerts_anomaly ON alerts (anomaly_id);
CREATE INDEX idx_alerts_status ON alerts (status, created_at) WHERE status = 'pending';
```

---

#### `notification_channels` Table
```sql
CREATE TABLE notification_channels (
  channel_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
  channel_type TEXT NOT NULL,
  destination TEXT NOT NULL, -- URL, email, phone number
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  min_severity TEXT NOT NULL DEFAULT 'medium',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_used_at TIMESTAMPTZ,

  CONSTRAINT channel_type_check CHECK (channel_type IN ('slack', 'email', 'discord', 'sms', 'webhook')),
  CONSTRAINT severity_check CHECK (min_severity IN ('critical', 'high', 'medium', 'low'))
);

CREATE INDEX idx_channels_customer ON notification_channels (customer_id) WHERE enabled = TRUE;
```

---

### InfluxDB Schema

**Database:** `defi_sentinel_metrics`

**Measurement:** `contract_metrics`

**Tags:**
- `contract_id` (UUID)
- `address` (Ethereum address)
- `chain` (ethereum, bsc, base)
- `metric_type` (tvl, transaction_count, gas_used, unique_users, etc.)

**Fields:**
- `value` (float64) - The metric value
- `anomaly` (boolean) - Whether this data point is an anomaly
- `anomaly_score` (float64, optional) - Confidence score if anomaly=true

**Retention Policy:**
- Raw data: 30 days (full resolution)
- Downsampled (5min avg): 90 days
- Downsampled (1hour avg): 1 year
- Downsampled (1day avg): 5 years

**Example InfluxQL Query:**
```sql
SELECT value, anomaly
FROM contract_metrics
WHERE contract_id = 'ctr_abc123'
  AND metric_type = 'tvl'
  AND time >= now() - 24h
ORDER BY time DESC
```

**Continuous Query (Downsampling):**
```sql
CREATE CONTINUOUS QUERY cq_5min_avg ON defi_sentinel_metrics
BEGIN
  SELECT mean(value) AS value
  INTO contract_metrics_5min
  FROM contract_metrics
  GROUP BY time(5m), contract_id, address, chain, metric_type
END;
```

---

## Anomaly Detection Algorithm

### Overview

Nixtla DeFi Sentinel uses a **hybrid approach**:
1. **Primary**: TimeGPT API (Nixtla's foundation model)
2. **Fallback**: StatsForecast models (AutoETS, MSTL)
3. **Post-processing**: Threshold-based filtering and severity scoring

### TimeGPT Anomaly Detection

**Input Preparation:**
```python
import pandas as pd
from nixtla import NixtlaClient

# Fetch last 1,000 data points (approx 3.5 days at 5-minute resolution)
df = fetch_metrics(
    contract_id='ctr_abc123',
    metric='tvl',
    hours=84  # 3.5 days
)

# Format for TimeGPT
df_timegpt = df[['timestamp', 'value']].rename(columns={
    'timestamp': 'ds',
    'value': 'y'
})
```

**TimeGPT API Call:**
```python
client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))

# Detect anomalies with 80% and 95% confidence intervals
result = client.detect_anomalies(
    df=df_timegpt,
    time_col='ds',
    target_col='y',
    freq='5min',
    level=[80, 95]
)
```

**Response Structure:**
```python
# result DataFrame columns:
# - ds: timestamp
# - y: actual value
# - TimeGPT: forecasted value
# - TimeGPT-lo-80: lower bound (80% CI)
# - TimeGPT-hi-80: upper bound (80% CI)
# - TimeGPT-lo-95: lower bound (95% CI)
# - TimeGPT-hi-95: upper bound (95% CI)
```

**Anomaly Identification Logic:**
```python
def identify_anomalies(result, confidence_level=95):
    """
    Identify anomalies where actual value falls outside confidence intervals.
    """
    lo_col = f'TimeGPT-lo-{confidence_level}'
    hi_col = f'TimeGPT-hi-{confidence_level}'

    result['anomaly'] = (
        (result['y'] > result[hi_col]) |  # Upper anomaly
        (result['y'] < result[lo_col])    # Lower anomaly
    )

    # Calculate anomaly score (how far outside bounds)
    result['anomaly_score'] = result.apply(lambda row:
        calculate_anomaly_score(
            value=row['y'],
            lower_bound=row[lo_col],
            upper_bound=row[hi_col]
        ) if row['anomaly'] else 0.0,
        axis=1
    )

    return result[result['anomaly']]

def calculate_anomaly_score(value, lower_bound, upper_bound):
    """
    Score from 0.0 (barely outside bounds) to 1.0 (extremely anomalous).
    """
    interval_width = upper_bound - lower_bound

    if value > upper_bound:
        distance = value - upper_bound
    else:  # value < lower_bound
        distance = lower_bound - value

    # Normalize: 1 interval width = 0.5 score, 2 widths = 0.75, etc.
    score = 1 - (1 / (1 + distance / interval_width))
    return min(score, 1.0)
```

---

### StatsForecast Fallback

**When to Use Fallback:**
- TimeGPT API returns 429 (rate limit)
- TimeGPT API returns 5xx (server error)
- TimeGPT API latency > 30 seconds
- Customer on Starter tier (uses StatsForecast by default)

**Implementation:**
```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, MSTL
import numpy as np

def detect_anomalies_statsforecast(df):
    """
    Fallback anomaly detection using StatsForecast models.
    """
    # Train models on historical data
    sf = StatsForecast(
        models=[
            AutoETS(season_length=12),  # 12 × 5min = 1 hour seasonality
            MSTL(season_length=[12, 288])  # 1 hour + 1 day seasonality
        ],
        freq='5min'
    )

    # Fit on first 90% of data
    train_size = int(len(df) * 0.9)
    train_df = df[:train_size]
    test_df = df[train_size:]

    sf.fit(train_df)

    # Forecast on test set
    forecast = sf.predict(h=len(test_df))

    # Simple Z-score anomaly detection on residuals
    residuals = test_df['value'] - forecast['AutoETS'].values
    z_scores = np.abs((residuals - residuals.mean()) / residuals.std())

    test_df['anomaly'] = z_scores > 3  # 3 standard deviations
    test_df['anomaly_score'] = np.minimum(z_scores / 5, 1.0)  # Normalize to 0-1

    return test_df[test_df['anomaly']]
```

---

### Severity Scoring

Once anomalies are detected, assign severity based on:
1. **Anomaly Score** (from TimeGPT/StatsForecast)
2. **Metric Type** (TVL drop is more critical than gas spike)
3. **Magnitude** (10% TVL drop vs 50% TVL drop)
4. **Context** (similar to known exploits?)

**Algorithm:**
```python
def calculate_severity(
    anomaly_score: float,
    metric: str,
    value: float,
    expected_value: float,
    historical_context: dict
) -> str:
    """
    Calculate severity: critical, high, medium, low
    """
    # Base score from model
    score = anomaly_score

    # Weight by metric type
    metric_weights = {
        'tvl': 1.5,
        'transaction_count': 1.0,
        'gas_used': 0.8,
        'unique_users': 0.7
    }
    score *= metric_weights.get(metric, 1.0)

    # Weight by magnitude
    percent_change = abs((value - expected_value) / expected_value)
    if percent_change > 0.5:  # >50% change
        score *= 1.5
    elif percent_change > 0.2:  # >20% change
        score *= 1.2

    # Weight by historical context
    if historical_context.get('similar_to_exploit'):
        score *= 1.3

    # Assign severity
    if score >= 0.9:
        return 'critical'
    elif score >= 0.7:
        return 'high'
    elif score >= 0.5:
        return 'medium'
    else:
        return 'low'
```

---

### Anomaly Type Classification

After detecting an anomaly, classify the type:

| Type | Definition | Example |
|------|-----------|---------|
| `sudden_drop` | Metric drops >10% in <10 minutes | TVL: $1M → $850K in 5 minutes |
| `sudden_spike` | Metric spikes >3 stddev in <10 minutes | Gas usage: 50K → 500K in 1 block |
| `gradual_drain` | Metric decreases steadily over 1-6 hours | TVL: $1M → $500K over 3 hours |
| `unusual_pattern` | Pattern doesn't match historical trends | Transaction count spikes at 3 AM (usually low) |
| `sustained_anomaly` | Anomaly persists for >1 hour | Gas usage 2x normal for 3 hours |

**Classification Logic:**
```python
def classify_anomaly_type(
    metric_name: str,
    value: float,
    expected_value: float,
    duration_minutes: int,
    recent_values: list
) -> str:
    """
    Classify the anomaly type based on patterns.
    """
    percent_change = (value - expected_value) / expected_value

    # Sudden drops/spikes (fast changes)
    if duration_minutes <= 10:
        if percent_change < -0.10:
            return 'sudden_drop'
        elif percent_change > 0.30:
            return 'sudden_spike'

    # Gradual drains (slow changes)
    if duration_minutes >= 60 and duration_minutes <= 360:
        if percent_change < -0.20:
            return 'gradual_drain'

    # Sustained anomalies (long-lasting)
    if duration_minutes > 60:
        return 'sustained_anomaly'

    # Default: unusual pattern
    return 'unusual_pattern'
```

---

## MCP Server Implementation

### MCP Protocol Overview

The Model Context Protocol (MCP) is Claude's standard for exposing tools and resources to AI assistants.

**MCP Server Responsibilities:**
1. Expose tools (functions Claude can call)
2. Validate inputs
3. Execute tool logic (call Sentinel API)
4. Return structured responses

---

### MCP Server File Structure

```
plugins/nixtla-defi-sentinel/
├── scripts/
│   └── mcp_server.py          # Main MCP server
├── commands/
│   └── nixtla-defi-monitor.md # Slash command definition
└── skills/
    └── nixtla-defi-sentinel/
        ├── SKILL.md           # Skill definition
        └── templates/
            └── incident_report.md
```

---

### `mcp_server.py` Implementation

```python
#!/usr/bin/env python3
"""
Nixtla DeFi Sentinel - MCP Server

Exposes tools for monitoring DeFi contracts via Claude Code.
"""

import os
import sys
from typing import Any, Dict, List
from mcp.server import MCPServer, Tool, ToolResult
from nixtla_defi_sentinel_client import SentinelClient

# Initialize MCP server
server = MCPServer(name="nixtla-defi-sentinel")

# Initialize Sentinel API client
API_KEY = os.getenv("NIXTLA_SENTINEL_API_KEY")
sentinel = SentinelClient(api_key=API_KEY)


@server.tool(
    name="monitor_contract",
    description="Start monitoring a DeFi contract for anomalies",
    parameters={
        "address": {
            "type": "string",
            "description": "Contract address (0x...)",
            "required": True
        },
        "chain": {
            "type": "string",
            "description": "Blockchain: ethereum, bsc, or base",
            "required": True,
            "enum": ["ethereum", "bsc", "base"]
        },
        "label": {
            "type": "string",
            "description": "Human-readable label (e.g., 'Uniswap USDC/ETH')",
            "required": False
        }
    }
)
def monitor_contract(address: str, chain: str, label: str = None) -> ToolResult:
    """
    Add a contract to monitoring.
    """
    try:
        # Call Sentinel API
        response = sentinel.add_contract(
            address=address,
            chain=chain,
            label=label
        )

        return ToolResult(
            success=True,
            content=f"✅ Contract {address} added to monitoring on {chain}. "
                    f"Monitoring will begin within 60 seconds.\n\n"
                    f"Contract ID: {response['contract_id']}"
        )

    except Exception as e:
        return ToolResult(
            success=False,
            content=f"❌ Failed to add contract: {str(e)}"
        )


@server.tool(
    name="get_contract_status",
    description="Get current metrics and recent anomalies for a contract",
    parameters={
        "address": {
            "type": "string",
            "description": "Contract address (0x...)",
            "required": True
        },
        "chain": {
            "type": "string",
            "description": "Blockchain: ethereum, bsc, or base",
            "required": True,
            "enum": ["ethereum", "bsc", "base"]
        }
    }
)
def get_contract_status(address: str, chain: str) -> ToolResult:
    """
    Fetch current status and recent anomalies for a contract.
    """
    try:
        # Get contract details
        contract = sentinel.get_contract_by_address(address, chain)

        # Get recent anomalies (last 24 hours)
        anomalies = sentinel.get_anomalies(
            contract_id=contract['contract_id'],
            hours=24
        )

        # Format response
        status_text = f"📊 **Contract Status**: {contract['label'] or address}\n\n"
        status_text += f"**Chain**: {chain}\n"
        status_text += f"**Monitoring**: {'✅ Enabled' if contract['monitoring_enabled'] else '❌ Paused'}\n\n"

        status_text += "**Current Metrics** (last updated: {}):\n".format(
            contract['last_checked_at']
        )
        metrics = contract['metrics']['current']
        status_text += f"- TVL: ${metrics['tvl']:,.2f}\n"
        status_text += f"- Transactions (24h): {metrics['transaction_count']:,}\n"
        status_text += f"- Gas Used: {metrics['gas_used']:,}\n\n"

        if anomalies:
            status_text += f"**⚠️ Recent Anomalies** ({len(anomalies)} in last 24h):\n"
            for ano in anomalies[:5]:  # Show up to 5
                status_text += f"- **{ano['severity'].upper()}**: {ano['description']}\n"
                status_text += f"  Detected: {ano['detected_at']}\n"
        else:
            status_text += "**✅ No anomalies detected in last 24 hours**\n"

        return ToolResult(success=True, content=status_text)

    except Exception as e:
        return ToolResult(
            success=False,
            content=f"❌ Failed to fetch contract status: {str(e)}"
        )


@server.tool(
    name="analyze_exploit_risk",
    description="Run comprehensive risk assessment on a contract",
    parameters={
        "address": {
            "type": "string",
            "description": "Contract address (0x...)",
            "required": True
        },
        "chain": {
            "type": "string",
            "description": "Blockchain: ethereum, bsc, or base",
            "required": True,
            "enum": ["ethereum", "bsc", "base"]
        }
    }
)
def analyze_exploit_risk(address: str, chain: str) -> ToolResult:
    """
    Perform deep analysis of exploit risk.
    """
    try:
        # Get historical metrics (last 7 days)
        metrics = sentinel.get_metrics(
            address=address,
            chain=chain,
            metric='tvl',
            days=7
        )

        # Get anomaly history (last 30 days)
        anomalies = sentinel.get_anomalies(
            address=address,
            chain=chain,
            days=30
        )

        # Calculate risk score
        risk_analysis = sentinel.analyze_risk(
            address=address,
            chain=chain
        )

        # Format report
        report = f"🔍 **Exploit Risk Analysis**: {address}\n\n"
        report += f"**Overall Risk Score**: {risk_analysis['risk_score']}/100\n"
        report += f"**Risk Level**: {risk_analysis['risk_level']}\n\n"

        report += "**Risk Factors**:\n"
        for factor in risk_analysis['risk_factors']:
            report += f"- {factor['name']}: {factor['score']}/10 ({factor['description']})\n"

        report += f"\n**Anomaly History** (last 30 days): {len(anomalies)} anomalies\n"
        report += f"- Critical: {sum(1 for a in anomalies if a['severity'] == 'critical')}\n"
        report += f"- High: {sum(1 for a in anomalies if a['severity'] == 'high')}\n"

        report += f"\n**Recommendations**:\n"
        for rec in risk_analysis['recommendations']:
            report += f"- {rec}\n"

        return ToolResult(success=True, content=report)

    except Exception as e:
        return ToolResult(
            success=False,
            content=f"❌ Failed to analyze exploit risk: {str(e)}"
        )


@server.tool(
    name="generate_security_report",
    description="Generate PDF security report for a contract",
    parameters={
        "address": {
            "type": "string",
            "description": "Contract address (0x...)",
            "required": True
        },
        "chain": {
            "type": "string",
            "description": "Blockchain: ethereum, bsc, or base",
            "required": True,
            "enum": ["ethereum", "bsc", "base"]
        },
        "days": {
            "type": "integer",
            "description": "Number of days to include in report",
            "required": False,
            "default": 30
        }
    }
)
def generate_security_report(address: str, chain: str, days: int = 30) -> ToolResult:
    """
    Generate comprehensive security report (PDF).
    """
    try:
        # Request report generation (async)
        response = sentinel.generate_report(
            address=address,
            chain=chain,
            days=days,
            format='pdf'
        )

        report_url = response['report_url']

        return ToolResult(
            success=True,
            content=f"📄 **Security Report Generated**\n\n"
                    f"Report covers {days} days of monitoring for contract {address}.\n\n"
                    f"Download: {report_url}\n\n"
                    f"Report includes:\n"
                    f"- Anomaly timeline with severity breakdown\n"
                    f"- Metric trends (TVL, transactions, gas usage)\n"
                    f"- Risk assessment and recommendations\n"
                    f"- Comparison to similar protocols"
        )

    except Exception as e:
        return ToolResult(
            success=False,
            content=f"❌ Failed to generate report: {str(e)}"
        )


if __name__ == "__main__":
    server.run()
```

---

### Slash Command Definition

**File:** `commands/nixtla-defi-monitor.md`

```markdown
description: Monitor a DeFi contract for security anomalies using Nixtla's TimeGPT

---

You are a DeFi security analyst using **Nixtla DeFi Sentinel**, an AI-powered anomaly detection system.

# User Request
The user wants to monitor this contract:
- **Address**: {{contract}}
- **Chain**: {{chain}}

# Your Task
1. Use the `monitor_contract` tool to add this contract to monitoring
2. Use the `get_contract_status` tool to fetch current metrics and recent anomalies
3. Use the `analyze_exploit_risk` tool to perform a comprehensive risk assessment

# Output Format
Provide a clear, structured report with:
- Contract details (address, chain, label)
- Current metrics (TVL, transaction count, etc.)
- Recent anomalies (if any)
- Exploit risk score and recommendations

Be concise but thorough. If anomalies are detected, explain their significance and suggest next steps.
```

---

## Claude Code Plugin

### Skill Definition

**File:** `skills-pack/.claude/skills/nixtla-defi-sentinel/SKILL.md`

```markdown
---
name: nixtla-defi-sentinel
description: AI-powered DeFi security monitoring with anomaly detection
type: utility
autoActivate: true
activationPatterns:
  - "\\b0x[a-fA-F0-9]{40}\\b"  # Ethereum addresses
  - "\\b(exploit|hack|reentrancy|flash loan|rug pull)\\b"  # Security terms
  - "\\b(TVL|total value locked|liquidity pool)\\b"  # DeFi terms
capabilities:
  - Detect smart contract anomalies in real-time
  - Analyze exploit risk for DeFi protocols
  - Generate security reports with AI-powered insights
  - Monitor TVL, transaction patterns, and gas usage
---

# Nixtla DeFi Sentinel Skill

You are now a **DeFi Security Analyst** powered by Nixtla's TimeGPT anomaly detection.

## Your Capabilities
- **Real-time Monitoring**: Detect exploits before they cause major damage
- **Risk Assessment**: Analyze contract risk using historical data
- **Incident Response**: Generate forensic reports for post-mortems
- **Predictive Alerts**: Forecast potential exploits using time-series forecasting

## Available Tools
Use the MCP tools from `nixtla-defi-sentinel` server:
- `monitor_contract(address, chain, label)` - Start monitoring a contract
- `get_contract_status(address, chain)` - Fetch current metrics and anomalies
- `analyze_exploit_risk(address, chain)` - Comprehensive risk assessment
- `generate_security_report(address, chain, days)` - Generate PDF report

## Analysis Framework
When analyzing a contract:
1. **Context**: What type of protocol is this? (DEX, lending, bridge)
2. **Metrics**: Review TVL, transaction volume, gas usage
3. **Anomalies**: Identify any unusual patterns in last 24-48 hours
4. **Risk**: Calculate exploit risk score based on historical data
5. **Recommendations**: Suggest monitoring thresholds and incident response steps

## Common Exploit Patterns to Watch For
- **Sudden TVL drops** (>10% in <10 minutes): Likely reentrancy or flash loan attack
- **Gas usage spikes**: Possible MEV attack or contract spamming
- **Unusual transaction patterns**: Suspicious fund movements to new addresses
- **Gradual TVL drain**: Slow exploit or economic attack

## Response Style
- Be direct and actionable
- Use severity labels: 🔴 Critical, 🟠 High, 🟡 Medium, 🟢 Low
- Provide context: Compare to known exploits (Balancer, Curve, etc.)
- Quantify risk: "85% confidence this is a real threat"
```

---

## Integration Specifications

### Slack Integration

**Webhook Format:**
```json
POST https://hooks.slack.com/services/T00000000/B00000000/XXXX

{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🚨 CRITICAL: TVL Drop Detected"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Contract:*\n0x1234...5678"
        },
        {
          "type": "mrkdwn",
          "text": "*Chain:*\nEthereum"
        },
        {
          "type": "mrkdwn",
          "text": "*Anomaly:*\nSudden TVL Drop"
        },
        {
          "type": "mrkdwn",
          "text": "*Severity:*\nCritical"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "TVL dropped from *$1,250,000* to *$1,125,000* in 5 minutes (-10%).\n\n*Context*: Similar pattern to Balancer exploit (Nov 2025)."
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View Dashboard"
          },
          "url": "https://dashboard.nixtla-defi-sentinel.com/contracts/ctr_abc123"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Acknowledge"
          },
          "url": "https://dashboard.nixtla-defi-sentinel.com/anomalies/ano_xyz789/acknowledge"
        }
      ]
    }
  ]
}
```

---

### Email Integration (SendGrid)

**Template:**
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; }
    .alert-critical { background-color: #ffebee; border-left: 4px solid #d32f2f; padding: 15px; }
    .alert-high { background-color: #fff3e0; border-left: 4px solid #f57c00; padding: 15px; }
    .metric { font-size: 24px; font-weight: bold; }
  </style>
</head>
<body>
  <h1>🚨 Critical Alert: TVL Drop Detected</h1>

  <div class="alert-critical">
    <h2>Contract: 0x1234...5678 (Ethereum)</h2>
    <p><strong>Anomaly Type:</strong> Sudden TVL Drop</p>
    <p><strong>Severity:</strong> Critical</p>
    <p><strong>Detected At:</strong> 2025-12-02 15:10:00 UTC</p>
  </div>

  <h3>Details</h3>
  <table>
    <tr>
      <td>TVL Before:</td>
      <td class="metric">$1,250,000</td>
    </tr>
    <tr>
      <td>TVL After:</td>
      <td class="metric">$1,125,000</td>
    </tr>
    <tr>
      <td>Change:</td>
      <td class="metric" style="color: #d32f2f;">-10%</td>
    </tr>
  </table>

  <h3>Context</h3>
  <p>This pattern is similar to the Balancer exploit (November 2025). Recommend immediate investigation.</p>

  <p><a href="https://dashboard.nixtla-defi-sentinel.com/contracts/ctr_abc123" style="background-color: #1976d2; color: white; padding: 10px 20px; text-decoration: none;">View Dashboard</a></p>

  <hr>
  <p style="color: #666; font-size: 12px;">
    Powered by <a href="https://nixtla.io">Nixtla DeFi Sentinel</a><br>
    To adjust alert settings, visit your <a href="https://dashboard.nixtla-defi-sentinel.com/settings">notification preferences</a>.
  </p>
</body>
</html>
```

---

## Security Implementation

### API Key Management

**Key Generation:**
```python
import secrets
import hashlib

def generate_api_key():
    """
    Generate API key with format: nixtla_sk_{env}_{random}
    """
    env = 'live'  # or 'test'
    random_part = secrets.token_urlsafe(32)
    key = f"nixtla_sk_{env}_{random_part}"

    # Hash for storage (SHA-256)
    key_hash = hashlib.sha256(key.encode()).hexdigest()

    return key, key_hash
```

**Key Validation Middleware (FastAPI):**
```python
from fastapi import Header, HTTPException
import hashlib

async def validate_api_key(authorization: str = Header(...)):
    """
    Validate API key from Authorization header.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization format")

    api_key = authorization[7:]  # Remove "Bearer "

    # Hash incoming key
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    # Look up in database
    customer = await db.get_customer_by_api_key(key_hash)
    if not customer:
        raise HTTPException(401, "Invalid API key")

    if customer['suspended_at']:
        raise HTTPException(403, "Account suspended")

    return customer
```

---

### Rate Limiting (Redis)

**Implementation:**
```python
import redis
from datetime import datetime, timedelta

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def check_rate_limit(customer_id: str, limit: int = 1000, window_seconds: int = 3600):
    """
    Token bucket rate limiting: 1,000 requests per hour.
    """
    key = f"rate_limit:{customer_id}"
    current_time = datetime.utcnow()

    # Increment request count
    count = redis_client.incr(key)

    # Set expiration on first request
    if count == 1:
        redis_client.expire(key, window_seconds)

    if count > limit:
        ttl = redis_client.ttl(key)
        raise HTTPException(
            429,
            detail=f"Rate limit exceeded. Try again in {ttl} seconds.",
            headers={"Retry-After": str(ttl)}
        )

    return count
```

---

## Performance & Optimization

### Database Indexing Strategy

**PostgreSQL Indexes:**
```sql
-- Customers table
CREATE INDEX idx_customers_api_key ON customers (api_key);
CREATE INDEX idx_customers_email ON customers (email);

-- Contracts table
CREATE INDEX idx_contracts_customer ON contracts (customer_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_contracts_address_chain ON contracts (address, chain) WHERE deleted_at IS NULL;

-- Anomalies table (most queried)
CREATE INDEX idx_anomalies_contract_detected ON anomalies (contract_id, detected_at DESC);
CREATE INDEX idx_anomalies_severity ON anomalies (severity, detected_at DESC) WHERE resolved_at IS NULL;
CREATE INDEX idx_anomalies_resolved ON anomalies (contract_id, resolved_at) WHERE resolved_at IS NOT NULL;

-- Alerts table
CREATE INDEX idx_alerts_anomaly ON alerts (anomaly_id);
CREATE INDEX idx_alerts_status ON alerts (status, created_at) WHERE status = 'pending';
```

**InfluxDB Continuous Queries:**
```sql
-- Downsample to 5-minute averages
CREATE CONTINUOUS QUERY cq_5min_avg ON defi_sentinel_metrics
BEGIN
  SELECT mean(value) AS value
  INTO contract_metrics_5min
  FROM contract_metrics
  GROUP BY time(5m), contract_id, metric_type
END;

-- Downsample to 1-hour averages
CREATE CONTINUOUS QUERY cq_1hour_avg ON defi_sentinel_metrics
BEGIN
  SELECT mean(value) AS value
  INTO contract_metrics_1hour
  FROM contract_metrics_5min
  GROUP BY time(1h), contract_id, metric_type
END;
```

---

### Caching Strategy

**Redis Caching (FastAPI):**
```python
import json
from functools import wraps

def cache_result(ttl_seconds: int = 60):
    """
    Decorator to cache function results in Redis.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and args
            cache_key = f"cache:{func.__name__}:{json.dumps(args)}:{json.dumps(kwargs)}"

            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute function
            result = await func(*args, **kwargs)

            # Store in cache
            redis_client.setex(cache_key, ttl_seconds, json.dumps(result))

            return result
        return wrapper
    return decorator


@cache_result(ttl_seconds=300)  # Cache for 5 minutes
async def get_contract_metrics(contract_id: str, metric: str, hours: int = 24):
    """
    Fetch metrics from InfluxDB (cached).
    """
    query = f"""
    SELECT value, anomaly
    FROM contract_metrics
    WHERE contract_id = '{contract_id}'
      AND metric_type = '{metric}'
      AND time >= now() - {hours}h
    ORDER BY time DESC
    """
    return await influxdb_client.query(query)
```

---

## Testing Strategy

### Unit Tests

**Example: Test Anomaly Detection Algorithm**
```python
import pytest
from nixtla_defi_sentinel.anomaly_detection import identify_anomalies

def test_identify_anomalies_upper_bound():
    """
    Test that values above upper confidence bound are flagged as anomalies.
    """
    # Mock TimeGPT response
    mock_result = pd.DataFrame({
        'ds': ['2025-12-02 15:00:00', '2025-12-02 15:05:00'],
        'y': [1250000, 1500000],  # Second value is anomalous
        'TimeGPT': [1250000, 1250000],
        'TimeGPT-lo-95': [1200000, 1200000],
        'TimeGPT-hi-95': [1300000, 1300000]
    })

    anomalies = identify_anomalies(mock_result, confidence_level=95)

    assert len(anomalies) == 1
    assert anomalies.iloc[0]['y'] == 1500000
    assert anomalies.iloc[0]['anomaly_score'] > 0.5


def test_calculate_severity_critical():
    """
    Test that large TVL drops are classified as critical.
    """
    severity = calculate_severity(
        anomaly_score=0.95,
        metric='tvl',
        value=500000,
        expected_value=1000000,
        historical_context={'similar_to_exploit': True}
    )

    assert severity == 'critical'
```

---

### Integration Tests

**Example: Test API Endpoint**
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_contract_success():
    """
    Test POST /contracts endpoint with valid data.
    """
    response = client.post(
        "/v1/contracts",
        json={
            "address": "0x1234567890abcdef1234567890abcdef12345678",
            "chain": "ethereum",
            "label": "Test Contract"
        },
        headers={"Authorization": "Bearer nixtla_sk_test_abc123"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data['address'] == "0x1234567890abcdef1234567890abcdef12345678"
    assert data['chain'] == "ethereum"
    assert 'contract_id' in data


def test_add_contract_invalid_address():
    """
    Test POST /contracts with invalid Ethereum address.
    """
    response = client.post(
        "/v1/contracts",
        json={
            "address": "invalid_address",
            "chain": "ethereum"
        },
        headers={"Authorization": "Bearer nixtla_sk_test_abc123"}
    )

    assert response.status_code == 400
    assert "INVALID_ADDRESS" in response.json()['code']
```

---

### End-to-End Tests

**Golden Task: Monitor Contract + Detect Anomaly**
```python
import pytest
import time

def test_end_to_end_monitoring():
    """
    Test full workflow: Add contract → Ingest metrics → Detect anomaly → Send alert.
    """
    # 1. Add contract
    response = client.post("/v1/contracts", json={
        "address": "0xtest123",
        "chain": "ethereum"
    })
    contract_id = response.json()['contract_id']

    # 2. Simulate blockchain metrics ingestion
    simulate_blockchain_metrics(contract_id, tvl=[1000000, 1000000, 500000])  # Last value is anomaly

    # 3. Wait for anomaly detection (should run within 60 seconds)
    time.sleep(60)

    # 4. Check anomalies endpoint
    response = client.get(f"/v1/anomalies?contract_id={contract_id}")
    anomalies = response.json()['data']

    assert len(anomalies) == 1
    assert anomalies[0]['severity'] in ['critical', 'high']

    # 5. Check alert was sent
    response = client.get(f"/v1/alerts?anomaly_id={anomalies[0]['anomaly_id']}")
    alerts = response.json()['data']

    assert len(alerts) > 0
    assert alerts[0]['status'] == 'sent'
```

---

## Deployment Specifications

### Docker Configuration

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - INFLUXDB_URL=${INFLUXDB_URL}
      - REDIS_URL=${REDIS_URL}
      - NIXTLA_API_KEY=${NIXTLA_API_KEY}
    depends_on:
      - postgres
      - influxdb
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: defi_sentinel
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  influxdb:
    image: influxdb:2.7
    environment:
      INFLUXDB_DB: defi_sentinel_metrics
      INFLUXDB_ADMIN_PASSWORD: ${INFLUXDB_PASSWORD}
    volumes:
      - influxdb_data:/var/lib/influxdb2
    ports:
      - "8086:8086"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru

volumes:
  postgres_data:
  influxdb_data:
```

---

### Cloud Run Deployment (GCP)

**Deploy Command:**
```bash
gcloud run deploy nixtla-defi-sentinel-api \
  --image gcr.io/nixtla-defi-sentinel/api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 2 \
  --max-instances 10 \
  --min-instances 1 \
  --set-env-vars DATABASE_URL=${DATABASE_URL},INFLUXDB_URL=${INFLUXDB_URL} \
  --set-secrets NIXTLA_API_KEY=nixtla-api-key:latest
```

---

## Conclusion

This technical specification provides all implementation details required to build **Nixtla DeFi Sentinel**. Key technical decisions:

1. **API-First**: RESTful API with OpenAPI documentation
2. **Hybrid Anomaly Detection**: TimeGPT (primary) + StatsForecast (fallback)
3. **Multi-Tenant**: PostgreSQL for config, InfluxDB for time-series metrics
4. **MCP Protocol**: Native Claude Code integration
5. **Cloud-Native**: Containerized, serverless-ready, horizontally scalable

**Next Steps:**
1. Implement MVP API (Endpoints 1-3: Contracts, Metrics, Anomalies)
2. Build anomaly detection pipeline (TimeGPT integration)
3. Create MCP server (4 tools: monitor, status, analyze, report)
4. Deploy to staging (GCP Cloud Run)
5. Beta test with 5 customers

---

**Prepared by:** Intent Solutions
**For:** Nixtla (Max Mergenthaler)
**Date:** 2025-12-02
**Version:** 1.0
