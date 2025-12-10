# Nixtla DeFi Sentinel - System Architecture

**Plugin ID:** nixtla-defi-sentinel
**Category:** Growth - New Market Entry
**Created:** 2025-12-02
**Status:** Specified
**Version:** 1.0

---

## Executive Summary

This document defines the technical architecture for **Nixtla DeFi Sentinel**, an AI-native security monitoring platform that uses time-series forecasting and anomaly detection to protect DeFi protocols from exploits.

**Architecture Philosophy:**
- **Cloud-native**: Serverless where possible, containerized for control
- **Event-driven**: Blockchain events trigger real-time processing pipelines
- **AI-first**: TimeGPT and StatsForecast at the core of threat detection
- **Multi-tenant**: Shared infrastructure with isolated customer data
- **API-centric**: All components communicate via well-defined APIs

**Key Design Decisions:**
- Serverless data ingestion (Cloud Functions/Lambda)
- Managed time-series database (InfluxDB Cloud or TimescaleDB)
- TimeGPT API for anomaly detection with StatsForecast fallback
- PostgreSQL for configuration and alerting metadata
- Redis for caching and rate limiting
- MCP server for Claude Code plugin integration

---

## Table of Contents

1. [System Context](#system-context)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Technology Stack](#technology-stack)
5. [Integration Architecture](#integration-architecture)
6. [Scalability & Performance](#scalability--performance)
7. [Security Architecture](#security-architecture)
8. [Deployment Architecture](#deployment-architecture)
9. [Monitoring & Observability](#monitoring--observability)
10. [Future Architecture Evolution](#future-architecture-evolution)

---

## System Context

### Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      External Systems                           │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Ethereum    │  │     BSC      │  │    Base      │          │
│  │  RPC Nodes   │  │  RPC Nodes   │  │  RPC Nodes   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                  │
└─────────┼──────────────────┼──────────────────┼──────────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Nixtla DeFi Sentinel Platform                    │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Data Ingestion Layer                         │  │
│  │  (Blockchain Listeners, Event Parsers, Data Normalizers) │  │
│  └───────────────────────┬───────────────────────────────────┘  │
│                          │                                       │
│                          ▼                                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Time-Series Storage                          │  │
│  │  (InfluxDB / TimescaleDB - Raw blockchain metrics)       │  │
│  └───────────────────────┬───────────────────────────────────┘  │
│                          │                                       │
│                          ▼                                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Anomaly Detection Engine                     │  │
│  │  (TimeGPT API + StatsForecast Models)                    │  │
│  └───────────────────────┬───────────────────────────────────┘  │
│                          │                                       │
│                          ▼                                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Alerting & Notification Layer                │  │
│  │  (Slack, Email, Discord, SMS, Webhook)                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Web Dashboard (React + TypeScript)           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Claude Code Plugin (MCP Server)              │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      External Services                           │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Nixtla      │  │   SendGrid   │  │    Twilio    │          │
│  │  TimeGPT API │  │   (Email)    │  │    (SMS)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### System Boundaries

**In Scope:**
- Real-time blockchain data ingestion
- Time-series storage and retrieval
- Anomaly detection using Nixtla models
- Alert generation and delivery
- Web dashboard for visualization
- Claude Code plugin for developer workflows

**Out of Scope (External Dependencies):**
- Blockchain infrastructure (rely on RPC providers)
- Email/SMS delivery (use SendGrid, Twilio)
- Static code analysis (use auditor integrations)
- Incident response (customer responsibility)

---

## Component Architecture

### High-Level Components

```
┌──────────────────────────────────────────────────────────────┐
│                    Frontend Layer                            │
├──────────────────────────────────────────────────────────────┤
│  - Web Dashboard (React + TypeScript)                        │
│  - Claude Code Plugin (MCP Client)                           │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    API Gateway Layer                         │
├──────────────────────────────────────────────────────────────┤
│  - REST API (FastAPI)                                        │
│  - MCP Server (Model Context Protocol)                      │
│  - Authentication & Authorization (JWT)                      │
│  - Rate Limiting (Redis)                                     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
├──────────────────────────────────────────────────────────────┤
│  - Contract Monitor Service                                  │
│  - Anomaly Detection Service                                 │
│  - Alert Manager Service                                     │
│  - Configuration Service                                     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
├──────────────────────────────────────────────────────────────┤
│  - Time-Series DB (InfluxDB / TimescaleDB)                  │
│  - Relational DB (PostgreSQL)                               │
│  - Cache (Redis)                                            │
│  - Object Storage (S3 / GCS)                                │
└──────────────────────────────────────────────────────────────┘
```

### Detailed Component Breakdown

#### 1. Data Ingestion Layer

**1.1 Blockchain Listener Service**
- **Purpose**: Subscribe to blockchain events in real-time
- **Technology**: Node.js with ethers.js / web3.py
- **Deployment**: Cloud Functions (GCP) / Lambda (AWS)
- **Triggers**:
  - New block events (every 12 seconds)
  - Contract event logs (Transfer, Swap, Deposit, Withdraw)
  - Pending transaction pool monitoring
- **Output**: Raw blockchain events → Event Queue (Pub/Sub / SQS)

**1.2 Event Parser Service**
- **Purpose**: Decode and normalize blockchain events
- **Technology**: Python with web3.py + custom ABI decoders
- **Deployment**: Cloud Run (GCP) / ECS Fargate (AWS)
- **Input**: Raw events from Event Queue
- **Output**: Normalized metrics → Time-Series DB

**1.3 Metrics Calculator Service**
- **Purpose**: Compute derived metrics (TVL, APY, risk scores)
- **Technology**: Python with pandas + numpy
- **Deployment**: Scheduled Cloud Functions (every 1 minute)
- **Calculations**:
  - TVL = Sum of all token balances × prices
  - Transaction velocity = Count of transactions per time window
  - Gas anomaly score = Current gas usage / historical average
  - Fund flow risk = Large transfers to new addresses

#### 2. Anomaly Detection Engine

**2.1 TimeGPT Anomaly Detector**
- **Purpose**: Primary anomaly detection using Nixtla TimeGPT
- **Technology**: Python with Nixtla SDK
- **Deployment**: Cloud Run with GPU support (optional)
- **Input**: Time-series metrics from InfluxDB/TimescaleDB
- **Process**:
  1. Fetch last 1,000 data points for each metric
  2. Call TimeGPT API with `detect_anomalies=True`
  3. Apply custom thresholds (configurable per customer)
  4. Score anomalies (0-100 severity)
- **Output**: Anomaly events → Alert Manager

**2.2 StatsForecast Fallback Detector**
- **Purpose**: Backup anomaly detection when TimeGPT unavailable
- **Technology**: Python with statsforecast library
- **Deployment**: Same container as TimeGPT detector
- **Models**: AutoETS, AutoTheta, MSTL (Multiple Seasonal Trend Loess)
- **Fallback Logic**:
  - If TimeGPT API returns 429 (rate limit) → use StatsForecast
  - If TimeGPT API returns 5xx (server error) → use StatsForecast
  - If TimeGPT latency > 30s → use StatsForecast

**2.3 Forecast Service (Phase 2)**
- **Purpose**: Predict future metric values to provide early warnings
- **Technology**: Python with Nixtla SDK
- **Deployment**: Scheduled batch jobs (every 5 minutes)
- **Process**:
  1. Fetch last 7 days of metrics
  2. Generate 1-hour ahead forecast with 80% confidence intervals
  3. Compare forecast to real-time values
  4. Trigger alert if real value exceeds upper confidence bound

#### 3. Alerting & Notification Layer

**3.1 Alert Manager Service**
- **Purpose**: Centralized alert routing and delivery
- **Technology**: Python with FastAPI + Celery (async task queue)
- **Deployment**: Cloud Run + Cloud Tasks (GCP) / ECS + SQS (AWS)
- **Features**:
  - Alert deduplication (same anomaly within 5 minutes)
  - Severity-based routing (critical → SMS, warning → email)
  - Alert aggregation (batch similar alerts)
  - Retry logic with exponential backoff

**3.2 Notification Channels**
- **Slack**: Webhook integration with rich message formatting
- **Email**: SendGrid API with HTML templates
- **Discord**: Webhook with embed formatting
- **SMS**: Twilio API for critical alerts only
- **Webhook**: Custom HTTP POST for integrations (PagerDuty, Opsgenie)

**3.3 Alert Storage & History**
- **Database**: PostgreSQL `alerts` table
- **Schema**:
  ```sql
  CREATE TABLE alerts (
    alert_id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    contract_address TEXT NOT NULL,
    anomaly_type TEXT NOT NULL,
    severity TEXT NOT NULL, -- critical, high, medium, low
    metric_name TEXT NOT NULL,
    metric_value NUMERIC,
    expected_value NUMERIC,
    confidence_score NUMERIC,
    triggered_at TIMESTAMPTZ NOT NULL,
    delivered_at TIMESTAMPTZ,
    acknowledged_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    metadata JSONB
  );
  ```

#### 4. Web Dashboard

**4.1 Frontend Application**
- **Technology**: React 18 + TypeScript + Vite
- **UI Library**: Tailwind CSS + shadcn/ui components
- **State Management**: Zustand + React Query
- **Charting**: Recharts or Plotly.js for time-series visualization
- **Deployment**: Static hosting (Vercel, Netlify, Firebase Hosting)

**4.2 Dashboard Features**
- **Contract Overview**: List of monitored contracts with status badges
- **Real-Time Metrics**: Live charts for TVL, transactions, gas usage
- **Anomaly Timeline**: Historical anomalies with severity indicators
- **Alert Feed**: Real-time alert notifications
- **Configuration Panel**: Add/remove contracts, set thresholds

**4.3 Backend API (REST)**
- **Technology**: Python with FastAPI
- **Endpoints**:
  - `GET /api/v1/contracts` - List monitored contracts
  - `GET /api/v1/contracts/{address}/metrics` - Fetch time-series data
  - `GET /api/v1/alerts?status=active` - Fetch alerts
  - `POST /api/v1/contracts` - Add new contract to monitor
  - `PUT /api/v1/contracts/{address}/thresholds` - Update alert thresholds
  - `DELETE /api/v1/contracts/{address}` - Stop monitoring contract

#### 5. Claude Code Plugin (MCP Server)

**5.1 MCP Server Implementation**
- **Technology**: Python with MCP SDK
- **Location**: `005-plugins/nixtla-defi-sentinel/scripts/mcp_server.py`
- **Tools Exposed**:
  - `monitor_contract(address, chain)` - Start monitoring a DeFi contract
  - `get_contract_status(address)` - Fetch current metrics and anomalies
  - `analyze_exploit_risk(address)` - Run comprehensive risk assessment
  - `generate_security_report(address)` - Create PDF report with findings

**5.2 Slash Command**
- **Location**: `005-plugins/nixtla-defi-sentinel/commands/nixtla-defi-monitor.md`
- **Usage**: `/nixtla-defi-monitor contract=0x123... chain=ethereum`
- **Prompt**: Activates Claude as DeFi security analyst, runs full analysis

**5.3 AI Skill**
- **Location**: `003-skills/.claude/skills/nixtla-defi-sentinel/`
- **Trigger**: Automatic when Claude detects blockchain addresses or DeFi terms
- **Capabilities**:
  - Explain anomaly types (sudden TVL drop, gas spike, etc.)
  - Suggest mitigation strategies
  - Generate incident reports
  - Compare against historical exploits (SCONE-bench dataset)

#### 6. Configuration & Metadata Storage

**6.1 PostgreSQL Schema**

```sql
-- Customers (multi-tenant)
CREATE TABLE customers (
  customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  api_key TEXT UNIQUE NOT NULL,
  tier TEXT NOT NULL DEFAULT 'starter', -- starter, professional, enterprise
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  suspended_at TIMESTAMPTZ
);

-- Monitored contracts
CREATE TABLE contracts (
  contract_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL REFERENCES customers(customer_id),
  address TEXT NOT NULL,
  chain TEXT NOT NULL, -- ethereum, bsc, base
  label TEXT,
  monitoring_enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(customer_id, address, chain)
);

-- Alert thresholds (configurable per contract)
CREATE TABLE thresholds (
  threshold_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contract_id UUID NOT NULL REFERENCES contracts(contract_id),
  metric_name TEXT NOT NULL,
  anomaly_type TEXT NOT NULL, -- spike, drop, unusual_pattern
  severity TEXT NOT NULL, -- critical, high, medium, low
  threshold_value NUMERIC,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  UNIQUE(contract_id, metric_name, anomaly_type)
);

-- Notification channels
CREATE TABLE notification_channels (
  channel_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL REFERENCES customers(customer_id),
  channel_type TEXT NOT NULL, -- slack, email, discord, sms, webhook
  destination TEXT NOT NULL, -- URL or email/phone
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  min_severity TEXT NOT NULL DEFAULT 'medium'
);
```

---

## Data Flow

### Real-Time Monitoring Flow

```
1. Blockchain Event Occurs
   ↓
2. Blockchain Listener detects event (12-second block time)
   ↓
3. Event pushed to Event Queue (Pub/Sub / SQS)
   ↓
4. Event Parser consumes from queue
   ↓
5. Normalized metrics written to Time-Series DB
   ↓
6. Anomaly Detection Engine reads latest metrics (1-minute window)
   ↓
7. TimeGPT API call: detect_anomalies(data, sensitivity='high')
   ↓
8. If anomaly detected → Alert Manager notified
   ↓
9. Alert Manager checks thresholds and deduplication rules
   ↓
10. Notification sent via configured channels (Slack, Email, etc.)
    ↓
11. Alert logged to PostgreSQL
    ↓
12. Web Dashboard shows real-time update (WebSocket)
```

### Claude Code Plugin Flow

```
1. User runs: /nixtla-defi-monitor contract=0xabc123 chain=ethereum
   ↓
2. Claude activates nixtla-defi-sentinel skill
   ↓
3. Skill calls MCP tool: monitor_contract(address='0xabc123', chain='ethereum')
   ↓
4. MCP Server validates contract exists on-chain
   ↓
5. MCP Server adds contract to monitoring database
   ↓
6. Blockchain Listener subscribes to contract events
   ↓
7. MCP Server fetches last 24 hours of historical metrics
   ↓
8. TimeGPT API analyzes historical data for existing anomalies
   ↓
9. MCP Server returns analysis report to Claude
   ↓
10. Claude presents findings to user with recommendations
```

### Batch Forecasting Flow (Phase 2)

```
1. Scheduled job triggers every 5 minutes
   ↓
2. Fetch all active contracts from PostgreSQL
   ↓
3. For each contract:
   a. Fetch last 7 days of metrics from Time-Series DB
   b. Call TimeGPT API: forecast(data, h=12, freq='5min')
   c. Store forecast in Time-Series DB with tag forecast=true
   ↓
4. Compare real-time values to forecasted values
   ↓
5. If real value > forecast upper bound → early warning alert
   ↓
6. Alert Manager handles early warnings with lower severity
```

---

## Technology Stack

### Language & Frameworks

| Component | Technology | Justification |
|-----------|-----------|---------------|
| API Backend | Python 3.11 + FastAPI | Async support, fast development, rich ML ecosystem |
| MCP Server | Python 3.11 + MCP SDK | Official Claude Code plugin protocol |
| Blockchain Listeners | Node.js 20 + ethers.js | Best blockchain library support |
| Web Dashboard | React 18 + TypeScript | Industry standard, rich ecosystem |
| Anomaly Detection | Python + Nixtla SDK | Direct access to TimeGPT and StatsForecast |

### Databases & Storage

| Type | Technology | Use Case |
|------|-----------|----------|
| Time-Series DB | **InfluxDB Cloud** (preferred) or TimescaleDB | Blockchain metrics (TVL, gas, tx count) |
| Relational DB | PostgreSQL 15 | Configuration, alerts, customer data |
| Cache | Redis 7 | API rate limiting, session storage |
| Object Storage | Google Cloud Storage or AWS S3 | Reproducibility bundles, historical reports |
| Message Queue | Google Pub/Sub or AWS SQS | Event processing pipeline |

**Why InfluxDB over TimescaleDB?**
- Native support for downsampling (reduce storage costs)
- Better query performance for time-range scans
- Built-in retention policies
- Managed cloud offering (less ops burden)

### External APIs

| Service | Purpose | Cost |
|---------|---------|------|
| Nixtla TimeGPT API | Primary anomaly detection | $0.001/prediction (500K = $500/mo) |
| Alchemy / Infura | Ethereum RPC nodes | $200-500/month (depends on call volume) |
| QuickNode | BSC + Base RPC nodes | $300-600/month |
| SendGrid | Email notifications | $15-100/month (depends on volume) |
| Twilio | SMS notifications | $0.0075/SMS (critical alerts only) |

### Infrastructure

| Component | GCP Option | AWS Option |
|-----------|-----------|-----------|
| Compute | Cloud Run (containers) | ECS Fargate |
| Functions | Cloud Functions | Lambda |
| Message Queue | Pub/Sub | SQS + SNS |
| Scheduling | Cloud Scheduler | EventBridge |
| Secrets | Secret Manager | Secrets Manager |
| Monitoring | Cloud Operations | CloudWatch |

**Recommended**: **Google Cloud Platform** (better InfluxDB integration, superior Pub/Sub)

---

## Integration Architecture

### Blockchain Data Sources

**RPC Provider Strategy:**
- **Primary**: Alchemy (Ethereum), QuickNode (BSC, Base)
- **Fallback**: Infura (Ethereum), Ankr (BSC, Base)
- **Retry Logic**: 3 attempts with 1s, 2s, 5s backoff
- **Rate Limiting**: 10,000 requests/day per provider (rotate keys)

**Data Ingestion Pattern:**
```python
# Pseudo-code for blockchain listener
async def listen_to_contract(contract_address: str, chain: str):
    provider = get_provider(chain)  # ethers.js provider
    contract = get_contract(contract_address, provider)

    # Subscribe to all events
    contract.on('*', async (event) => {
        normalized = parse_event(event)
        await publish_to_queue(normalized)
    })

    # Also poll for state changes every block
    provider.on('block', async (block_number) => {
        metrics = await fetch_contract_metrics(contract, block_number)
        await publish_to_queue(metrics)
    })
```

### Nixtla API Integration

**TimeGPT Anomaly Detection:**
```python
from nixtla import NixtlaClient

client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))

# Fetch metrics from InfluxDB
df = fetch_metrics(contract_address='0x123', metric='tvl', hours=24)

# Detect anomalies with TimeGPT
result = client.detect_anomalies(
    df=df,
    time_col='timestamp',
    target_col='value',
    freq='5min',
    level=[80, 95]  # Confidence levels for anomaly bounds
)

# Extract anomalies where value exceeds bounds
anomalies = result[
    (result['value'] > result['TimeGPT-hi-95']) |
    (result['value'] < result['TimeGPT-lo-95'])
]
```

**StatsForecast Fallback:**
```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, MSTL

# If TimeGPT unavailable, use StatsForecast
sf = StatsForecast(
    models=[AutoETS(season_length=12), MSTL(season_length=12)],
    freq='5min'
)

sf.fit(df)
forecast = sf.predict(h=12)  # 1-hour ahead

# Simple anomaly detection: Z-score method
from scipy import stats
z_scores = stats.zscore(df['value'])
anomalies = df[abs(z_scores) > 3]  # 3 standard deviations
```

### Alert Delivery Integration

**Slack Webhook:**
```python
import httpx

async def send_slack_alert(webhook_url: str, alert: Alert):
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🚨 {alert.severity.upper()} Alert"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Contract:*\n{alert.contract_address}"},
                    {"type": "mrkdwn", "text": f"*Chain:*\n{alert.chain}"},
                    {"type": "mrkdwn", "text": f"*Anomaly:*\n{alert.anomaly_type}"},
                    {"type": "mrkdwn", "text": f"*Severity:*\n{alert.severity}"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Metric `{alert.metric_name}` is *{alert.metric_value:.2f}* (expected: {alert.expected_value:.2f})"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "View Dashboard"},
                        "url": f"https://dashboard.nixtla-defi-sentinel.com/contracts/{alert.contract_address}"
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(webhook_url, json=payload)
        response.raise_for_status()
```

---

## Scalability & Performance

### Performance Targets

| Metric | Target | Strategy |
|--------|--------|----------|
| Data ingestion latency | < 15 seconds from block time | WebSocket listeners + async processing |
| Anomaly detection latency | < 30 seconds after ingestion | Parallel TimeGPT API calls (max 10 concurrent) |
| Alert delivery latency | < 5 seconds after detection | Async Celery tasks with priority queues |
| Dashboard load time | < 2 seconds | CDN caching + lazy loading charts |
| API response time | < 200ms (p95) | Redis caching + database indexing |
| Concurrent contracts monitored | 1,000+ per cluster | Horizontal scaling of listeners |

### Scaling Strategies

**Horizontal Scaling (Phase 2):**
```
┌─────────────────┐
│  Load Balancer  │
└────────┬────────┘
         │
    ┌────┴─────┬─────────┬─────────┐
    ▼          ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ API 1  │ │ API 2  │ │ API 3  │ │ API N  │
└────────┘ └────────┘ └────────┘ └────────┘
```

**Partitioning Strategy:**
- Partition blockchain listeners by chain (Ethereum cluster, BSC cluster, Base cluster)
- Partition anomaly detection by customer (enterprise customers get dedicated instances)
- Partition time-series data by contract address (InfluxDB bucketing)

**Caching Layers:**
1. **L1 Cache (In-Memory)**: FastAPI app-level cache for configuration (TTL: 5 min)
2. **L2 Cache (Redis)**: API responses for dashboard (TTL: 1 min)
3. **L3 Cache (InfluxDB Continuous Queries)**: Pre-aggregated metrics (hourly, daily)

**Database Optimization:**
- **InfluxDB**: Retention policies (keep raw data 30 days, downsampled data 1 year)
- **PostgreSQL**: Partitioning `alerts` table by month, indexed on `(customer_id, triggered_at)`
- **Redis**: LRU eviction policy, max memory 4GB per instance

### Cost Optimization

**Expected Monthly Costs (at scale - 100 customers, 1,000 contracts):**

| Component | Cost | Optimization Strategy |
|-----------|------|----------------------|
| TimeGPT API | $500 | Batch predictions, use StatsForecast for low-risk contracts |
| RPC Nodes | $800 | Cache contract state, use archive nodes sparingly |
| InfluxDB Cloud | $300 | Aggressive downsampling, 30-day retention |
| Cloud Run | $200 | Auto-scale to zero, use preemptible instances |
| PostgreSQL (Cloud SQL) | $150 | Use db-f1-micro for dev, db-n1-standard-1 for prod |
| Redis (Memorystore) | $100 | Use smallest instance (1GB), enable persistence |
| SendGrid | $50 | Batch emails, use templates |
| **Total** | **$2,100/month** | **Break-even at 3 enterprise customers ($25K/year each)** |

---

## Security Architecture

### Authentication & Authorization

**API Authentication:**
- **Method**: API keys (SHA-256 hashed, stored in PostgreSQL)
- **Format**: `nixtla_sk_live_<random_32_chars>` (production), `nixtla_sk_test_<random_32_chars>` (test)
- **Header**: `Authorization: Bearer nixtla_sk_live_abc123...`
- **Rate Limiting**: 1,000 requests/hour per API key (Redis-based)

**Dashboard Authentication:**
- **Method**: JWT tokens (short-lived access tokens + refresh tokens)
- **Flow**: Email/password login → JWT issued → refresh every 15 minutes
- **Storage**: Refresh tokens stored in PostgreSQL with expiration (30 days)

**Role-Based Access Control (RBAC):**
```sql
CREATE TABLE roles (
  role_id UUID PRIMARY KEY,
  customer_id UUID NOT NULL REFERENCES customers(customer_id),
  user_email TEXT NOT NULL,
  role TEXT NOT NULL, -- admin, viewer, auditor
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```
- **Admin**: Full access (add/remove contracts, change thresholds, view billing)
- **Viewer**: Read-only access (view dashboard, alerts)
- **Auditor**: Read-only + export reports

### Data Security

**Encryption:**
- **In Transit**: TLS 1.3 for all API endpoints (enforced by Cloud Run / ALB)
- **At Rest**:
  - PostgreSQL: Google-managed encryption keys (default)
  - InfluxDB Cloud: AES-256 encryption
  - S3/GCS: Server-side encryption (SSE-KMS)

**Secrets Management:**
- **Storage**: Google Secret Manager / AWS Secrets Manager
- **Access**: Service accounts with least-privilege IAM policies
- **Rotation**: API keys rotated every 90 days (automated)

**PII Handling:**
- **Data Minimization**: Only store email addresses (no names, phone numbers unless SMS enabled)
- **Anonymization**: Customer IDs are UUIDs (no sequential IDs)
- **Deletion**: GDPR-compliant deletion API (`DELETE /api/v1/customers/{id}`)

### Network Security

**VPC Configuration (GCP Example):**
```
┌─────────────────────────────────────────┐
│  Public Subnet (Load Balancer)         │
│  - Cloud Load Balancer (HTTPS only)    │
└─────────────┬───────────────────────────┘
              │
┌─────────────┴───────────────────────────┐
│  Private Subnet (Application Layer)    │
│  - Cloud Run services (private)        │
│  - Cloud Functions (private)           │
│  - No direct internet access           │
└─────────────┬───────────────────────────┘
              │
┌─────────────┴───────────────────────────┐
│  Database Subnet (Data Layer)          │
│  - Cloud SQL (private IP only)         │
│  - Memorystore Redis (private IP)      │
│  - No internet access                  │
└─────────────────────────────────────────┘
```

**Firewall Rules:**
- Ingress: Only allow HTTPS (443) from internet to Load Balancer
- Egress: Application layer can only reach RPC nodes, TimeGPT API, notification services
- Database layer: Zero egress, only accepts connections from application layer

**DDoS Protection:**
- Cloud Armor (GCP) / AWS Shield for Layer 7 DDoS mitigation
- Rate limiting at API Gateway (1,000 req/hour per IP)
- CAPTCHA on login page (hCaptcha)

### Compliance

**SOC 2 Type II Readiness:**
- Audit logging of all API calls (retained 1 year)
- Immutable alert history (no deletions, only soft deletes)
- Regular vulnerability scanning (Dependabot, Snyk)
- Incident response runbook (documented)

**GDPR Compliance:**
- Data export API (`GET /api/v1/customers/{id}/export`)
- Data deletion API (`DELETE /api/v1/customers/{id}`)
- Cookie consent banner on dashboard
- Privacy policy and terms of service

---

## Deployment Architecture

### Multi-Environment Strategy

| Environment | Purpose | Infrastructure | Data |
|-------------|---------|----------------|------|
| **Local** | Developer workstations | Docker Compose | Synthetic test data |
| **Dev** | Integration testing | GCP/AWS dev project | Testnet contracts (Sepolia) |
| **Staging** | Pre-production validation | GCP/AWS staging project | Mainnet shadow (read-only) |
| **Production** | Customer-facing | GCP/AWS prod project | Live mainnet contracts |

### Infrastructure as Code (Terraform)

**Project Structure:**
```
terraform/
├── modules/
│   ├── api_gateway/        # FastAPI + Cloud Run
│   ├── blockchain_listeners/  # Cloud Functions
│   ├── databases/          # Cloud SQL, InfluxDB, Redis
│   ├── monitoring/         # Cloud Operations, alerting rules
│   └── networking/         # VPC, firewall, load balancer
├── environments/
│   ├── dev/
│   │   └── main.tf
│   ├── staging/
│   │   └── main.tf
│   └── production/
│       └── main.tf
└── variables.tf
```

**Example Module (API Gateway):**
```hcl
# terraform/modules/api_gateway/main.tf
resource "google_cloud_run_service" "api" {
  name     = "nixtla-defi-sentinel-api"
  location = var.region

  template {
    spec {
      containers {
        image = var.container_image
        env {
          name  = "DATABASE_URL"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.db_url.secret_id
              key  = "latest"
            }
          }
        }
        resources {
          limits = {
            cpu    = "2000m"
            memory = "1Gi"
          }
        }
      }
      service_account_name = google_service_account.api.email
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "10"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
```

### CI/CD Pipeline (GitHub Actions)

**Workflow:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t gcr.io/nixtla-defi-sentinel/api:${{ github.sha }} .
      - name: Push to GCR
        run: docker push gcr.io/nixtla-defi-sentinel/api:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy nixtla-defi-sentinel-api \
            --image gcr.io/nixtla-defi-sentinel/api:${{ github.sha }} \
            --region us-central1 \
            --platform managed
```

**Deployment Strategy:**
- **Blue-Green**: Zero-downtime deployments (Cloud Run traffic splitting)
- **Canary**: Route 10% traffic to new version, monitor for 5 minutes, then 100%
- **Rollback**: Automated rollback if error rate > 1% (monitored by Cloud Operations)

### Local Development Setup

**Docker Compose:**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: nixtla_defi_sentinel
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"

  influxdb:
    image: influxdb:2.7
    environment:
      INFLUXDB_DB: metrics
      INFLUXDB_ADMIN_USER: admin
      INFLUXDB_ADMIN_PASSWORD: dev_password
    ports:
      - "8086:8086"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://postgres:dev_password@postgres:5432/nixtla_defi_sentinel
      INFLUXDB_URL: http://influxdb:8086
      REDIS_URL: redis://redis:6379
      NIXTLA_API_KEY: ${NIXTLA_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - influxdb
      - redis
```

**Setup Script:**
```bash
#!/bin/bash
# scripts/setup_dev_environment.sh

# 1. Start services
docker-compose up -d

# 2. Run migrations
docker-compose exec api alembic upgrade head

# 3. Seed test data
docker-compose exec api python scripts/seed_test_data.py

# 4. Run tests
docker-compose exec api pytest

echo "✅ Dev environment ready! API: http://localhost:8000"
```

---

## Monitoring & Observability

### Metrics & Dashboards

**Key Metrics to Track:**

| Category | Metric | Target | Alert Threshold |
|----------|--------|--------|-----------------|
| **Availability** | API uptime | 99.9% | < 99.5% |
| **Performance** | API p95 latency | < 200ms | > 500ms |
| **Throughput** | Blockchain events/sec | 100+ | < 10 (indicates listener failure) |
| **Accuracy** | False positive rate | < 5% | > 10% |
| **Business** | Active contracts monitored | 1,000+ | N/A |
| **Cost** | TimeGPT API spend | $500/month | > $700/month |

**Monitoring Stack:**
- **Metrics**: Prometheus (self-hosted) or Cloud Monitoring (GCP) / CloudWatch (AWS)
- **Logs**: Cloud Logging (GCP) / CloudWatch Logs (AWS)
- **Traces**: Cloud Trace (GCP) / X-Ray (AWS)
- **Dashboards**: Grafana (self-hosted) or Cloud Monitoring dashboards

**Example Grafana Dashboard:**
```
┌─────────────────────────────────────────────────────────┐
│  Nixtla DeFi Sentinel - Operations Dashboard           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ API Uptime  │  │ Contracts   │  │ Alerts/Hour │    │
│  │   99.98%    │  │    1,247    │  │     18      │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  API Latency (p50, p95, p99)                      │ │
│  │  [Chart showing latency over last 24 hours]      │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Blockchain Events Ingested (by chain)            │ │
│  │  [Chart: Ethereum 45%, BSC 35%, Base 20%]       │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Anomaly Detection Pipeline Health                │ │
│  │  - TimeGPT API: ✅ 200ms avg latency              │ │
│  │  - StatsForecast fallback: ✅ Idle                │ │
│  │  - Alert Manager queue: 3 pending                 │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Logging Strategy

**Structured Logging (JSON format):**
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "anomaly_detected",
    contract_address="0xabc123",
    chain="ethereum",
    metric="tvl",
    severity="high",
    confidence=0.92,
    customer_id="cust_xyz789"
)
```

**Log Levels:**
- **DEBUG**: Verbose internal state (disabled in production)
- **INFO**: Normal operations (API requests, anomaly detections, alerts sent)
- **WARNING**: Degraded performance (TimeGPT fallback, high latency)
- **ERROR**: Failures that require attention (RPC node timeout, database connection lost)
- **CRITICAL**: System-wide failures (all RPC nodes down, database unreachable)

**Log Retention:**
- Production: 90 days (compliance requirement)
- Staging: 30 days
- Dev: 7 days

### Alerting Rules

**Operational Alerts (sent to engineering team):**
```yaml
# Prometheus alerting rules
groups:
  - name: nixtla-defi-sentinel
    interval: 30s
    rules:
      - alert: HighAPILatency
        expr: histogram_quantile(0.95, api_request_duration_seconds) > 0.5
        for: 5m
        annotations:
          summary: "API p95 latency > 500ms"

      - alert: BlockchainListenerDown
        expr: up{job="blockchain-listener"} == 0
        for: 2m
        annotations:
          summary: "Blockchain listener is down"

      - alert: TimeGPTAPIFailureRate
        expr: rate(timegpt_api_errors_total[5m]) > 0.1
        for: 5m
        annotations:
          summary: "TimeGPT API failure rate > 10%"
```

**Customer Alerts (sent via configured channels):**
- Anomaly detected (severity-based routing)
- Contract monitoring started/stopped
- Forecast prediction exceeded (early warning)

### Distributed Tracing

**Example Trace (Anomaly Detection Flow):**
```
Trace ID: 7f3a2b1c-9d8e-4f5a-b6c7-1a2b3c4d5e6f
Duration: 1.2 seconds

Span 1: API Request (POST /api/v1/detect-anomalies)
  Duration: 1.2s
  └─ Span 2: Fetch metrics from InfluxDB
      Duration: 150ms
      └─ Span 3: TimeGPT API call
          Duration: 800ms
          └─ Span 4: Parse TimeGPT response
              Duration: 50ms
              └─ Span 5: Store anomalies in PostgreSQL
                  Duration: 100ms
                  └─ Span 6: Trigger alert
                      Duration: 50ms
```

**Tracing Implementation (OpenTelemetry):**
```python
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

span_processor = BatchSpanProcessor(CloudTraceSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Trace anomaly detection
@tracer.start_as_current_span("detect_anomalies")
async def detect_anomalies(contract_address: str):
    with tracer.start_as_current_span("fetch_metrics"):
        metrics = await fetch_metrics(contract_address)

    with tracer.start_as_current_span("call_timegpt"):
        anomalies = await call_timegpt_api(metrics)

    with tracer.start_as_current_span("trigger_alert"):
        await trigger_alert(anomalies)
```

---

## Future Architecture Evolution

### Phase 2 Enhancements (Months 4-6)

**1. Multi-Chain Expansion**
- Add support for Polygon, Avalanche, Arbitrum
- Unified blockchain listener abstraction layer
- Chain-specific metric normalization

**2. Advanced Forecasting**
- Prophet integration for long-term forecasting (7-day ahead)
- Confidence intervals for forecasted metrics
- "What-if" scenario analysis (e.g., "What if TVL drops 20%?")

**3. Custom Model Training**
- Customer-provided historical data for fine-tuning
- TimeGPT fine-tuning API integration
- Model versioning and A/B testing

### Phase 3 Enhancements (Months 7-12)

**1. Incident Response Automation**
- Automatic contract pausing (via Safe multisig integration)
- Runbook execution (e.g., "If TVL drops > 20%, pause deposits")
- Integration with PagerDuty for on-call escalation

**2. Historical Exploit Database**
- Ingest SCONE-bench dataset (4.6M worth of exploits)
- Pattern matching: "This anomaly looks like Balancer exploit (Nov 2025)"
- Exploit signature library (graph-based contract call patterns)

**3. White-Label Solution**
- Multi-tenant dashboard with custom branding
- Embeddable widgets (e.g., "Security Score" badge for protocol websites)
- API-first architecture for custom integrations

**4. Machine Learning Enhancements**
- Reinforcement learning for alert threshold tuning (reduce false positives over time)
- Graph neural networks for transaction flow analysis
- Ensemble models: TimeGPT + StatsForecast + custom LSTM

### Scalability Roadmap

**Current Architecture (MVP):**
- 1,000 contracts monitored
- 10 customers
- Single-region deployment (us-central1)

**Phase 2 (Production):**
- 10,000 contracts monitored
- 50 customers
- Multi-region deployment (us-central1, eu-west1)
- Read replicas for PostgreSQL

**Phase 3 (Scale):**
- 100,000+ contracts monitored
- 200+ customers
- Global deployment (5+ regions)
- Dedicated clusters for enterprise customers
- Edge caching for dashboard assets

---

## Conclusion

The Nixtla DeFi Sentinel architecture is designed for:
- **Reliability**: Multi-region, fault-tolerant, automated failover
- **Performance**: Sub-30-second anomaly detection, sub-5-second alerting
- **Scalability**: Horizontal scaling to 100K+ contracts
- **Security**: Defense-in-depth, SOC 2 ready, GDPR compliant
- **Cost-Efficiency**: Serverless-first, aggressive caching, managed services

**Key Architectural Principles:**
1. **Event-Driven**: Blockchain events drive all processing
2. **API-First**: Every component exposes clean REST/gRPC APIs
3. **Cloud-Native**: Leverage managed services (InfluxDB Cloud, Cloud Run, etc.)
4. **AI-Native**: TimeGPT and StatsForecast at the core, not bolted on
5. **Observable**: Comprehensive metrics, logs, traces from day one

**Next Steps:**
1. Build MVP (Phase 1) using this architecture
2. Validate with 5 beta customers on testnet contracts
3. Iterate based on feedback
4. Launch production (Phase 2) with paying customers
5. Scale to 1,000+ contracts (Phase 3)

---

**Prepared by:** Intent Solutions
**For:** Nixtla (Max Mergenthaler)
**Date:** 2025-12-02
**Version:** 1.0
