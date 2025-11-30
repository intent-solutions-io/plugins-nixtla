# Plugin #1: Nixtla Cost Optimizer
**Technical Architecture & Implementation Specification**

**Created**: 2025-11-30
**Status**: Design Phase
**Priority**: Tier 1 (IMMEDIATE VALUE)
**Addresses**: Burn Rate Problem (Friction #5)

---

## Executive Summary

### What It Is
An intelligent cost optimization system that analyzes Nixtla API usage patterns, detects redundant forecasts, implements intelligent caching, and provides actionable cost-saving recommendations.

### Why It Exists
Nixtla's CRO loses sleep over this:
> "10,000 SKUs * 24 hours * 30 days = 7.2 million forecasts/month. An intern sets a cron job to run every minute instead of every hour. The company receives a massive bill. Reaction: 'Cancel this service immediately.'"

**Bill shock leads to immediate churn.** This plugin prevents that.

### Who It's For
- **Enterprise customers** using TimeGPT API at scale
- **Data engineering teams** managing forecast workflows
- **FinOps teams** optimizing cloud spend
- **Nixtla's CRO** preventing churn

---

## Architecture Overview

### Component Stack

```
┌─────────────────────────────────────────────────────────────┐
│  USER INTERFACE                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Slash Command│  │ Agent Skill  │  │  MCP Server     │  │
│  │ /optimize    │  │ (Auto-invoke)│  │  (Cost Tools)   │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  CORE LOGIC                                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Cost Analysis Engine (Python)                       │  │
│  │  - Usage pattern detection                           │  │
│  │  - Redundancy analysis                               │  │
│  │  - Caching recommendations                           │  │
│  │  - Cost projection modeling                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA LAYER                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │  SQLite DB  │  │  JSON Cache │  │  Nixtla API      │   │
│  │  (history)  │  │  (results)  │  │  (billing data)  │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Plugin Type
**Hybrid**: AI Instruction (Skills/Commands) + MCP Server (Cost Tools)

### Components

1. **Slash Commands** (2)
   - `/nixtla-optimize` - Full cost optimization analysis
   - `/nixtla-cost-report` - Quick cost summary

2. **Agent Skill** (1)
   - `nixtla-cost-optimizer` - Auto-invokes on cost-related discussions

3. **MCP Server** (1)
   - `nixtla-cost-tools` - 6 MCP tools for cost analysis

4. **Lifecycle Hooks** (1)
   - `PostToolUse` hook on Bash/Write - Detects forecast script creation

---

## API Keys & User Requirements

### Required API Keys

```bash
# .env file
NIXTLA_API_KEY=nixak-...                      # Required: TimeGPT API access
NIXTLA_BILLING_API_KEY=billing-...            # Optional: Enhanced billing data
GCP_PROJECT_ID=my-project                     # If using BigQuery
GCP_SA_KEY_PATH=/path/to/service-account.json # If using BigQuery
```

### User Requirements

#### Minimum
- **Nixtla API account** with billing access
- **Python 3.10+** for cost analysis engine
- **10MB disk space** for SQLite database
- **Read access** to API usage logs (CloudWatch, GCP Logs, or Nixtla dashboard export)

#### Recommended
- **BigQuery access** for large-scale usage analytics
- **Slack webhook** for cost alerts
- **PagerDuty API key** for critical alerts (>$5k/mo spike)

#### Optional Integrations
- **Snowflake** - Analyze forecasts stored in Snowflake
- **Airflow** - Detect inefficient DAG scheduling
- **Grafana** - Visualize cost trends
- **dbt** - Analyze dbt model forecast patterns

---

## Installation Process

### Step 1: Add Plugin to Claude Code

```bash
# Install from marketplace
/plugin install nixtla-cost-optimizer@claude-code-plugins-plus
```

### Step 2: Run Setup Script

```bash
# Auto-generated installation script
cd ~/.claude/plugins/nixtla-cost-optimizer
./scripts/setup.sh
```

**setup.sh**:
```bash
#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Setting up Nixtla Cost Optimizer..."

# Step 1: Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION or higher required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Step 2: Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Step 3: Activate and install dependencies
echo "📦 Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Initialize database
echo "🗄️  Initializing SQLite database..."
python3 src/init_db.py

# Step 5: Build MCP server
echo "🏗️  Building MCP server..."
cd mcp
pnpm install
pnpm build
cd ..

# Step 6: Configure MCP server in Claude Code
echo "⚙️  Configuring MCP server..."
MCP_CONFIG="$HOME/.config/claude-code/mcp-servers.json"

if [ ! -f "$MCP_CONFIG" ]; then
    echo "{}" > "$MCP_CONFIG"
fi

# Add server config using jq
jq --arg plugin_root "$PWD" \
   '.mcpServers."nixtla-cost-tools" = {
      "command": "node",
      "args": [($plugin_root + "/mcp/dist/index.js")],
      "description": "Nixtla cost optimization tools"
    }' "$MCP_CONFIG" > "$MCP_CONFIG.tmp"

mv "$MCP_CONFIG.tmp" "$MCP_CONFIG"

echo "✅ MCP server configured"

# Step 7: Validate installation
echo "🧪 Validating installation..."
python3 -m pytest tests/ -v

# Step 8: Create API key file
if [ ! -f ".env" ]; then
    cat > .env <<EOF
# Nixtla Cost Optimizer Configuration
# Created: $(date +%Y-%m-%d)

# REQUIRED: Nixtla API key
NIXTLA_API_KEY=your_api_key_here

# OPTIONAL: Enhanced billing data
# NIXTLA_BILLING_API_KEY=your_billing_key_here

# OPTIONAL: GCP integration
# GCP_PROJECT_ID=your-project-id
# GCP_SA_KEY_PATH=/path/to/service-account.json

# OPTIONAL: Slack alerts
# SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# OPTIONAL: PagerDuty critical alerts
# PAGERDUTY_API_KEY=your_pagerduty_key
# PAGERDUTY_SERVICE_ID=your_service_id
EOF

    echo "⚠️  Please edit .env file with your API keys"
    echo "   Location: $PWD/.env"
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ Nixtla Cost Optimizer installed successfully!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "1. Edit .env file: $PWD/.env"
echo "2. Add your NIXTLA_API_KEY"
echo "3. Run: /nixtla-optimize to analyze costs"
echo ""
echo "Documentation: $PWD/README.md"
echo "════════════════════════════════════════════════════════════"
```

### Step 3: Configure API Keys

```bash
# Edit .env file
vim ~/.claude/plugins/nixtla-cost-optimizer/.env

# Add your Nixtla API key
NIXTLA_API_KEY=nixak-JNfT4z4JQb9uK3gdAyiWYWSBELdt6iW0PmE0Sy3k8ETAInJkFSPp4gOfyAZrENcGOsKyTqfDmuLghVq9
```

### Step 4: Restart Claude Code

```bash
# Reload MCP servers
/mcp reload
```

---

## Technical Schemas

### 1. Usage Log Schema (SQLite)

```sql
-- Database: cost_optimizer.db

CREATE TABLE usage_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    series_id TEXT NOT NULL,
    dataset_hash TEXT NOT NULL,      -- SHA256 of input data
    model TEXT NOT NULL,              -- 'AutoETS', 'TimeGPT', etc.
    horizon INTEGER NOT NULL,
    cost_usd DECIMAL(10, 4),
    rows_processed INTEGER,
    execution_time_ms INTEGER,
    was_cached BOOLEAN DEFAULT 0,
    source TEXT,                      -- 'airflow', 'manual', 'script', etc.
    INDEX idx_series (series_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_hash (dataset_hash)
);

CREATE TABLE redundancy_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id TEXT NOT NULL,
    pattern_type TEXT NOT NULL,       -- 'identical_refore cast', 'stale_data', etc.
    first_occurrence DATETIME NOT NULL,
    occurrence_count INTEGER NOT NULL,
    estimated_waste_usd DECIMAL(10, 4),
    recommendation TEXT,
    INDEX idx_series (series_id)
);

CREATE TABLE cost_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date DATE NOT NULL,
    total_cost_usd DECIMAL(10, 4),
    total_forecasts INTEGER,
    cached_forecasts INTEGER,
    unique_series INTEGER,
    avg_cost_per_forecast DECIMAL(10, 6),
    PRIMARY KEY (snapshot_date)
);

CREATE TABLE caching_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id TEXT NOT NULL UNIQUE,
    ttl_seconds INTEGER NOT NULL,    -- Cache TTL
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    enabled BOOLEAN DEFAULT 1
);
```

### 2. Cost Analysis Configuration (JSON)

```json
{
  "cost_optimizer_config": {
    "version": "1.0.0",
    "analysis": {
      "lookback_days": 30,
      "redundancy_threshold": 0.95,
      "min_cost_to_flag": 10.00,
      "stale_data_threshold_hours": 24
    },
    "caching": {
      "enabled": true,
      "default_ttl_seconds": 3600,
      "max_cache_size_mb": 500,
      "cache_hit_target_pct": 60
    },
    "alerts": {
      "slack": {
        "enabled": false,
        "webhook_url": "${SLACK_WEBHOOK_URL}",
        "threshold_usd": 1000
      },
      "pagerduty": {
        "enabled": false,
        "api_key": "${PAGERDUTY_API_KEY}",
        "service_id": "${PAGERDUTY_SERVICE_ID}",
        "threshold_usd": 5000
      },
      "email": {
        "enabled": false,
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "recipients": ["[email protected]"]
      }
    },
    "recommendations": {
      "auto_apply_safe": false,
      "require_approval_above_usd": 500,
      "max_frequency_reduction_pct": 80
    }
  }
}
```

### 3. MCP Tool Schemas

```typescript
// src/types.ts

export interface UsageRecord {
  timestamp: string;
  series_id: string;
  dataset_hash: string;
  model: string;
  horizon: number;
  cost_usd: number;
  rows_processed: number;
  execution_time_ms: number;
  was_cached: boolean;
  source: string;
}

export interface RedundancyPattern {
  series_id: string;
  pattern_type: 'identical_reforecast' | 'stale_data' | 'unnecessary_frequency';
  occurrence_count: number;
  estimated_waste_usd: number;
  recommendation: string;
}

export interface CostSnapshot {
  snapshot_date: string;
  total_cost_usd: number;
  total_forecasts: number;
  cached_forecasts: number;
  unique_series: number;
  avg_cost_per_forecast: number;
}

export interface CostOptimizationReport {
  period: {
    start_date: string;
    end_date: string;
    days: number;
  };
  current_costs: {
    total_usd: number;
    forecasts: number;
    cost_per_forecast: number;
  };
  potential_savings: {
    total_usd: number;
    percentage: number;
    breakdown: {
      caching: number;
      frequency_optimization: number;
      dormant_series_removal: number;
    };
  };
  top_offenders: RedundancyPattern[];
  recommendations: CostRecommendation[];
}

export interface CostRecommendation {
  id: string;
  type: 'enable_caching' | 'reduce_frequency' | 'remove_series';
  series_id: string;
  current_state: string;
  recommended_state: string;
  estimated_monthly_savings_usd: number;
  risk_level: 'low' | 'medium' | 'high';
  auto_apply_safe: boolean;
}
```

---

## Code Implementation

### Directory Structure

```
plugins/ai-ml/nixtla-cost-optimizer/
├── .claude-plugin/
│   └── plugin.json                   # Plugin manifest
├── README.md                          # User documentation
├── LICENSE                            # MIT
├── commands/
│   ├── optimize.md                   # /nixtla-optimize command
│   └── cost-report.md                # /nixtla-cost-report command
├── skills/
│   └── cost-optimizer/
│       └── SKILL.md                  # Agent skill definition
├── mcp/
│   ├── server.json                   # MCP server config
│   ├── src/
│   │   ├── index.ts                  # MCP server entry point
│   │   ├── types.ts                  # TypeScript types
│   │   ├── tools/                    # MCP tool implementations
│   │   │   ├── analyze-usage.ts
│   │   │   ├── detect-redundancy.ts
│   │   │   ├── generate-recommendations.ts
│   │   │   ├── apply-caching-rules.ts
│   │   │   ├── get-cost-snapshot.ts
│   │   │   └── export-report.ts
│   │   └── db/
│   │       └── client.ts             # SQLite client
│   ├── package.json
│   ├── tsconfig.json
│   └── dist/                         # Compiled JS (gitignored)
├── src/
│   ├── __init__.py
│   ├── init_db.py                    # Database initialization
│   ├── cost_analyzer.py              # Core cost analysis logic
│   ├── redundancy_detector.py        # Detect redundant forecasts
│   ├── caching_optimizer.py          # Caching recommendations
│   ├── nixtla_client.py              # Nixtla API wrapper
│   └── utils/
│       ├── hash.py                   # Dataset hashing
│       ├── alerts.py                 # Slack/PagerDuty integration
│       └── report_generator.py       # Report formatting
├── tests/
│   ├── test_cost_analyzer.py
│   ├── test_redundancy_detector.py
│   └── fixtures/
│       └── sample_usage_logs.json
├── scripts/
│   ├── setup.sh                      # Installation script
│   ├── sync-usage-logs.sh            # Import logs from APIs
│   └── generate-report.py            # Standalone report generation
├── hooks/
│   ├── hooks.json                    # Lifecycle hooks config
│   └── scripts/
│       └── detect-forecast-script.sh # Post-Write hook
├── requirements.txt                   # Python dependencies
├── .env.example                      # Environment template
└── cost_optimizer.db                 # SQLite database (gitignored)
```

### Core Implementation Files

#### 1. plugin.json

```json
{
  "name": "nixtla-cost-optimizer",
  "version": "1.0.0",
  "description": "Intelligent cost optimization for Nixtla TimeGPT API usage - prevent bill shock and reduce waste",
  "author": {
    "name": "Intent Solutions",
    "email": "[email protected]"
  },
  "repository": "https://github.com/jeremylongshore/claude-code-plugins-nixtla",
  "license": "MIT",
  "keywords": [
    "nixtla",
    "timegpt",
    "cost-optimization",
    "finops",
    "forecasting",
    "api-optimization",
    "caching",
    "redundancy-detection"
  ],
  "hooks": "./hooks/hooks.json"
}
```

#### 2. commands/optimize.md

```yaml
---
description: Run comprehensive cost optimization analysis for Nixtla API usage
shortcut: no
category: cost-optimization
difficulty: beginner
estimated_time: 2 minutes
version: 1.0.0
---

# Nixtla Cost Optimizer

## What It Does

Analyzes your Nixtla TimeGPT API usage over the past 30 days and provides:
- **Total cost breakdown** by series, model, and time period
- **Redundancy detection** - Finds identical forecasts being re-run
- **Caching opportunities** - Identifies series that don't change
- **Frequency optimization** - Recommends reducing forecast cadence
- **Dormant series removal** - Flags inactive series still being forecasted
- **Projected savings** - Estimates monthly cost reduction

## When to Use

- **Monthly cost review** - Understand where money is going
- **Bill shock investigation** - Why did costs spike this month?
- **Onboarding new team member** - Audit their forecast scripts
- **Before scaling up** - Optimize before increasing usage
- **After changing workflows** - Validate efficiency improvements

## Prerequisites

- Nixtla API key configured in `.env`
- Usage logs synced (automatic if using MCP server)
- Minimum 7 days of usage history for meaningful analysis

## Process

### Step 1: Load Historical Usage Data

The plugin connects to Nixtla's billing API and imports usage logs:

```
Fetching usage logs...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Retrieved 245,892 forecast requests
✅ Covering 30 days (2025-10-30 to 2025-11-30)
✅ 10,485 unique series
✅ Total cost: $12,450.23
```

### Step 2: Analyze Usage Patterns

Detects redundant forecasts using dataset hashing:

```
Analyzing patterns...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Hashing 245,892 datasets (SHA256)
🔍 Comparing against historical requests
✅ Analysis complete (42 seconds)
```

### Step 3: Generate Recommendations

Creates actionable cost-saving recommendations:

```
Generating recommendations...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 127 recommendations generated
✅ Potential savings: $7,890/month (63%)
```

### Step 4: Display Report

Shows comprehensive cost optimization report:

```
💸 NIXTLA COST OPTIMIZATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Period: 30 days (2025-10-30 to 2025-11-30)

CURRENT COSTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Spend:          $12,450.23
Total Forecasts:      245,892
Cost per Forecast:    $0.0506
Unique Series:        10,485
Cache Hit Rate:       12% (target: 60%)

POTENTIAL SAVINGS: $7,890/month (63%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Enable Caching:           $4,250 (54%)
💰 Reduce Frequency:         $2,890 (37%)
💰 Remove Dormant Series:    $750 (9%)

🔴 TOP 10 COST OFFENDERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. SKU_42873
   Cost: $850/month
   Issue: Forecasted 43,200 times (hourly)
   Data: Unchanged for 25 days (99.8% identical)
   💡 RECOMMENDATION: Enable caching (TTL: 24h)
   💰 Savings: $820/month

2. payment_type_cash
   Cost: $720/month
   Issue: Identical data re-forecasted 720 times
   💡 RECOMMENDATION: Cache for 7 days
   💰 Savings: $680/month

3. region_US_WEST
   Cost: $640/month
   Issue: Forecasted every 30 minutes (unnecessarily)
   💡 RECOMMENDATION: Reduce to daily cadence
   💰 Savings: $590/month

... [7 more offenders]

🟢 SAFE AUTO-APPLY RECOMMENDATIONS (75)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
These can be applied automatically with low risk:
- Enable caching for 42 dormant series (no changes in 30 days)
- Remove forecasting for 33 inactive series (zero activity 90+ days)

💰 Total Safe Savings: $4,120/month (52%)

⚠️  REQUIRES APPROVAL (52)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
These require manual review:
- Reduce frequency for 28 high-volume series
- Change 24 series from hourly to daily

💰 Total Conditional Savings: $3,770/month (48%)

NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Review full recommendations: /nixtla-cost-report --detailed
2. Apply safe recommendations: /nixtla-apply-safe
3. Export to CSV: /nixtla-export-report --format csv
4. Schedule monthly audits: /nixtla-schedule-audit
```

## Output Format

The command generates:
1. **Console output** - Summary shown above
2. **JSON report** - Saved to `reports/cost-optimization-YYYY-MM-DD.json`
3. **CSV export** - Detailed recommendations in spreadsheet format
4. **Slack notification** - If webhook configured
5. **Database update** - New snapshot in `cost_snapshots` table

## Examples

### Example 1: First-Time Analysis

**User Input:** `/nixtla-optimize`

**Scenario:** User has never run cost optimization before

**Output:**
```
Welcome to Nixtla Cost Optimizer!

This appears to be your first cost analysis.
Setting up...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Created database: cost_optimizer.db
✅ Syncing 30 days of usage logs...
✅ Imported 245,892 forecast requests

Running analysis...
[Full report as shown above]

💡 TIP: Schedule monthly audits to track improvement:
   /nixtla-schedule-audit --monthly
```

### Example 2: After Applying Recommendations

**User Input:** `/nixtla-optimize`

**Scenario:** User applied caching recommendations last week

**Output:**
```
💸 COST OPTIMIZATION REPORT (Updated)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPROVEMENT SINCE LAST AUDIT (7 days ago)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Previous Monthly Cost:  $12,450
Current Monthly Cost:   $6,890
SAVINGS ACHIEVED:       $5,560 (45%)

Cache Hit Rate:         12% → 58% (+46 pp)
Redundant Forecasts:    43% → 8% (-35 pp)

🎉 Congratulations! You're on track to save $66,720/year.

NEW RECOMMENDATIONS: $1,230/month additional savings available
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Remaining optimization opportunities]
```

### Example 3: Bill Shock Investigation

**User Input:** `/nixtla-optimize --spike-detection`

**Scenario:** Cost spiked from $5k to $18k this month

**Output:**
```
🚨 COST SPIKE DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Previous Month: $5,240
Current Month:  $18,350
SPIKE:          +$13,110 (+250%)

ROOT CAUSE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 CRITICAL ISSUE FOUND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Script: forecast_all_skus.py
Created: 2025-11-15 14:23:18
Created by: [email protected]
Issue: Cron job set to run every 1 minute (should be hourly)

Impact:
- 10,485 series × 1,440 runs/day = 15M forecasts/month
- Cost: $758,880/month if unchecked

IMMEDIATE ACTION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Stop cron job: crontab -e (remove line 42)
2. Update to hourly: */60 * * * * /path/to/script
3. Estimated corrected cost: $5,200/month

Would you like me to fix this automatically? [y/N]
```

## Error Handling

### Error 1: Missing API Key

```
❌ ERROR: Nixtla API key not configured

Please add your API key to .env file:
  echo "NIXTLA_API_KEY=your_key_here" >> ~/.claude/plugins/nixtla-cost-optimizer/.env

Get your API key: https://dashboard.nixtla.io/api-keys
```

### Error 2: Insufficient Usage History

```
⚠️  WARNING: Limited usage history

You have only 3 days of usage data.
Recommendations require at least 7 days for accuracy.

Would you like to:
1. Run analysis anyway (less accurate)
2. Wait until you have 7 days of data
3. Import historical logs manually

Choice: _
```

### Error 3: Database Corruption

```
❌ ERROR: Database corruption detected

Attempting automatic recovery...
✅ Backup created: cost_optimizer.db.backup-2025-11-30
✅ Database rebuilt from usage logs
✅ Re-imported 245,892 records

Analysis can now proceed.
```

## Configuration Options

### --lookback-days

Analyze different time periods:

```bash
/nixtla-optimize --lookback-days 7   # Last week only
/nixtla-optimize --lookback-days 90  # Last quarter
```

### --threshold

Set minimum cost to flag:

```bash
/nixtla-optimize --threshold 50  # Only flag series costing >$50/mo
```

### --auto-apply

Automatically apply safe recommendations:

```bash
/nixtla-optimize --auto-apply-safe
```

### --export

Export to different formats:

```bash
/nixtla-optimize --export csv
/nixtla-optimize --export json
/nixtla-optimize --export pdf  # Executive summary
```

## Best Practices

### Do's
✅ Run monthly cost audits
✅ Enable caching for stable series
✅ Review "high offenders" weekly
✅ Set up Slack alerts for spikes >$1k
✅ Test caching on staging environment first

### Don'ts
❌ Don't auto-apply ALL recommendations without review
❌ Don't disable forecasting for critical business series
❌ Don't set cache TTL too high (>7 days) for volatile data
❌ Don't ignore "medium risk" recommendations
❌ Don't optimize away accuracy for marginal savings

## Related Commands

- `/nixtla-cost-report --detailed` - Full detailed report with all series
- `/nixtla-apply-safe` - Apply low-risk recommendations automatically
- `/nixtla-schedule-audit --monthly` - Schedule recurring audits
- `/nixtla-export-report --format csv` - Export for FinOps review
- `/nixtla-simulate-savings` - Model "what if" scenarios
```

#### 3. skills/cost-optimizer/SKILL.md

```yaml
---
name: nixtla-cost-optimizer
description: |
  Intelligent cost optimization system for Nixtla TimeGPT API usage.
  Analyzes usage patterns, detects redundant forecasts, implements caching,
  and provides actionable cost-saving recommendations. Prevents bill shock
  and reduces API waste by up to 63%.

  Triggers: "optimize nixtla costs", "reduce timegpt spend", "nixtla bill shock",
  "analyze forecast costs", "why is my nixtla bill so high"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
---

## What This Skill Does

Expert in analyzing Nixtla TimeGPT API usage to identify cost optimization opportunities:

- **Usage Pattern Analysis** - Tracks all forecast requests with dataset hashing
- **Redundancy Detection** - Finds identical forecasts being re-run unnecessarily
- **Intelligent Caching** - Recommends caching rules for stable time series
- **Frequency Optimization** - Identifies over-forecasting (e.g., hourly when daily suffices)
- **Dormant Series Removal** - Flags inactive series still consuming API calls
- **Cost Spike Investigation** - Root cause analysis for unexpected bill increases
- **ROI Calculation** - Quantifies savings from each recommendation

## When This Skill Activates

### Trigger Phrases
- "Why is my Nixtla bill so high this month?"
- "Optimize my TimeGPT costs"
- "Reduce forecast API spend"
- "Analyze Nixtla usage patterns"
- "Find redundant forecasts"
- "How can I save money on TimeGPT?"
- "Investigate cost spike in forecasting"
- "Cache forecast results to reduce costs"

### Automatic Activation Scenarios
- User mentions cost concerns during forecast discussions
- User asks about API billing or usage optimization
- User describes re-running the same forecasts repeatedly
- User mentions forecasting at high frequency (hourly, minutely)

## How It Works

### Phase 1: Data Collection

1. **Connect to Nixtla API** - Authenticate using `NIXTLA_API_KEY`
2. **Import Usage Logs** - Retrieve 30 days (configurable) of forecast requests
3. **Hash Datasets** - Compute SHA256 hash of each input dataset for comparison
4. **Store in SQLite** - Persist usage history for trend analysis

**Example**:
```python
from src.nixtla_client import NixtlaClient

client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))
usage_logs = client.get_usage_logs(days=30)

# Hash datasets for comparison
for log in usage_logs:
    log['dataset_hash'] = hashlib.sha256(
        json.dumps(log['input_data'], sort_keys=True).encode()
    ).hexdigest()
```

### Phase 2: Pattern Recognition

1. **Redundancy Detection** - Find forecasts with identical input data
2. **Frequency Analysis** - Detect unnecessarily high forecast cadence
3. **Stale Data Detection** - Identify series with unchanged data
4. **Dormant Series** - Flag series with zero recent activity

**Example**:
```python
from src.redundancy_detector import RedundancyDetector

detector = RedundancyDetector(usage_logs)

# Find identical reforecasts
redundant = detector.find_identical_reforecasts(
    threshold=0.95  # 95% similarity
)

# Detect over-forecasting
over_forecasted = detector.find_high_frequency_series(
    max_reasonable_freq='1H'  # Hourly is max reasonable
)
```

### Phase 3: Recommendation Generation

1. **Caching Rules** - Generate TTL recommendations for stable series
2. **Frequency Reduction** - Suggest optimal forecast cadence
3. **Series Removal** - Recommend disabling dormant series
4. **Cost Modeling** - Calculate savings for each recommendation

**Example**:
```python
from src.caching_optimizer import CachingOptimizer

optimizer = CachingOptimizer(usage_logs, redundancy_patterns)

recommendations = optimizer.generate_recommendations(
    auto_apply_threshold=0.5  # Auto-apply if >50% confidence
)

# Output:
# [
#   {
#     "series_id": "SKU_42873",
#     "type": "enable_caching",
#     "current": "forecasted 43,200 times/month",
#     "recommended": "cache with 24h TTL",
#     "savings": 820.00,
#     "risk": "low",
#     "auto_apply_safe": True
#   }
# ]
```

### Phase 4: Report Generation

1. **Format Report** - Create human-readable cost optimization summary
2. **Export Options** - JSON, CSV, PDF formats
3. **Alert Integration** - Send to Slack/PagerDuty if configured
4. **Database Snapshot** - Save analysis results for trend tracking

**Example**:
```python
from src.report_generator import CostReportGenerator

generator = CostReportGenerator(
    usage_logs,
    redundancy_patterns,
    recommendations
)

# Generate console report
report_text = generator.generate_console_report()
print(report_text)

# Export to CSV for FinOps team
generator.export_csv('reports/cost-optimization-2025-11-30.csv')

# Send Slack alert if costs >$1k spike
if generator.detect_spike(threshold=1000):
    generator.send_slack_alert(os.getenv('SLACK_WEBHOOK_URL'))
```

## Workflow Examples

### Example 1: Monthly Cost Audit

**User**: "Run a cost optimization analysis for Nixtla usage this month"

**Skill Actions**:
1. Import 30 days of usage logs from Nixtla API
2. Hash all datasets and detect 127 redundant forecast patterns
3. Generate 75 "safe auto-apply" recommendations (caching, dormant removal)
4. Calculate potential savings: $7,890/month (63%)
5. Display comprehensive report with top 10 cost offenders
6. Export detailed recommendations to CSV for review

**Output**:
```
💸 NIXTLA COST OPTIMIZATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Period: 30 days (2025-10-30 to 2025-11-30)

CURRENT COSTS
Total Spend:          $12,450.23
Total Forecasts:      245,892
Cost per Forecast:    $0.0506

POTENTIAL SAVINGS: $7,890/month (63%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Enable Caching:           $4,250 (54%)
💰 Reduce Frequency:         $2,890 (37%)
💰 Remove Dormant Series:    $750 (9%)

🔴 TOP 10 COST OFFENDERS
1. SKU_42873 - $850/mo - Forecasted hourly with 99.8% identical data
   💡 Enable 24h caching → Save $820/mo

[Full report continues...]
```

### Example 2: Bill Shock Investigation

**User**: "My Nixtla bill jumped from $5k to $18k this month - what happened?"

**Skill Actions**:
1. Compare current month vs previous month usage
2. Detect 250% cost spike
3. Analyze new forecast scripts created this month
4. Identify root cause: Cron job set to 1-minute interval (should be hourly)
5. Calculate impact: 15M forecasts/month if unchecked
6. Provide immediate fix recommendation

**Output**:
```
🚨 COST SPIKE DETECTED: +$13,110 (+250%)

ROOT CAUSE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Script: forecast_all_skus.py
Created: 2025-11-15 14:23:18 by [email protected]
Issue: Cron job running every 1 minute (should be hourly)

IMMEDIATE ACTION:
1. Stop cron: crontab -e (remove line 42)
2. Fix frequency: */60 * * * * (hourly)
3. Estimated corrected cost: $5,200/mo

Would you like me to fix this automatically? [y/N]
```

### Example 3: Proactive Optimization

**User**: "We're scaling up our forecasting workload - optimize before we go live"

**Skill Actions**:
1. Analyze current usage patterns (pre-scale)
2. Model projected costs if scaled 10x
3. Recommend caching strategies to minimize impact
4. Suggest frequency optimization for new series
5. Create monitoring alerts for cost spikes
6. Generate implementation checklist

**Output**:
```
📈 SCALE-UP COST PROJECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Usage: 10,485 series, $12,450/mo
Projected (10x): 104,850 series

WITHOUT OPTIMIZATION:
Projected Cost: $124,500/mo
Risk: High (bill shock likely)

WITH RECOMMENDED OPTIMIZATIONS:
Projected Cost: $45,200/mo
Savings: $79,300/mo (64%)

IMPLEMENTATION CHECKLIST
✅ Enable caching for 8,420 stable series (TTL: 24h)
✅ Set frequency limits (max hourly for volatile, daily for stable)
✅ Implement pre-forecast data change detection
✅ Configure Slack alerts at $50k threshold
✅ Schedule weekly cost audits

Estimated Implementation Time: 2 days
```

## Integration Points

### MCP Tools Available

When this skill is active, it provides access to 6 MCP tools:

1. **analyze_usage** - Import and analyze historical usage
2. **detect_redundancy** - Find duplicate/redundant forecasts
3. **generate_recommendations** - Create cost-saving recommendations
4. **apply_caching_rules** - Apply approved caching configurations
5. **get_cost_snapshot** - Retrieve cost summary for date range
6. **export_report** - Export analysis to CSV/JSON/PDF

### External Integrations

- **Nixtla Billing API** - Import usage logs and cost data
- **Slack** - Send cost alerts and reports
- **PagerDuty** - Critical cost spike alerts (>$5k)
- **BigQuery** - Advanced analytics on large usage datasets
- **Snowflake** - Analyze forecasts stored in data warehouse
- **Airflow** - Detect inefficient DAG scheduling

## Technical Requirements

### API Keys

```bash
# Required
NIXTLA_API_KEY=nixak-...                # TimeGPT API access

# Optional (enhanced features)
NIXTLA_BILLING_API_KEY=billing-...      # Detailed billing data
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
PAGERDUTY_API_KEY=...
GCP_PROJECT_ID=...                      # For BigQuery integration
```

### Python Dependencies

```txt
# requirements.txt
nixtla>=0.7.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
python-dotenv>=1.0.0
pydantic>=2.0.0
sqlalchemy>=2.0.0
click>=8.1.0
rich>=13.0.0
```

### Database Schema

SQLite database with 4 tables:
- `usage_logs` - All forecast requests
- `redundancy_patterns` - Detected inefficiencies
- `cost_snapshots` - Daily cost summaries
- `caching_rules` - Applied caching configurations

## Error Handling

### Graceful Degradation

If Nixtla Billing API is unavailable:
- Fall back to usage log export (manual import)
- Estimate costs using average $0.05/forecast
- Continue analysis with available data

If database is corrupted:
- Automatic backup and rebuild
- Re-import from API
- Continue analysis

### User Guidance

For missing API keys:
```
❌ NIXTLA_API_KEY not configured

Get your API key:
1. Visit https://dashboard.nixtla.io/api-keys
2. Create new API key
3. Add to .env file:
   echo "NIXTLA_API_KEY=your_key" >> ~/.claude/plugins/nixtla-cost-optimizer/.env
4. Reload plugin: /mcp reload
```

For insufficient data:
```
⚠️  Only 3 days of usage data available

Recommendations require ≥7 days for accuracy.
Options:
1. Wait 4 more days (recommended)
2. Import historical logs manually
3. Run analysis anyway (less accurate)
```

## Best Practices

### Do's
✅ Run monthly cost audits proactively
✅ Start with "safe auto-apply" recommendations
✅ Test caching on staging before production
✅ Set up Slack alerts for >$1k spikes
✅ Review high-cost series weekly
✅ Export reports for FinOps team review

### Don'ts
❌ Don't auto-apply ALL recommendations without review
❌ Don't disable critical business series to save $50
❌ Don't set cache TTL >7 days for volatile data
❌ Don't ignore "medium risk" warnings
❌ Don't optimize accuracy away for marginal savings

## Performance Characteristics

- **Analysis Speed**: 245,000 records in ~42 seconds
- **Memory Usage**: ~200MB for 30 days of data
- **Database Size**: ~50MB per month of history
- **Cache Hit Target**: 60% (achievable with optimization)
- **Typical Savings**: 45-63% cost reduction

## Security Considerations

- API keys stored in `.env` file (not committed to git)
- Database encrypted at rest (optional)
- Sensitive cost data never logged to console
- Slack/PagerDuty webhooks validated before sending
- No PII in exported reports (series IDs anonymized)

## Support & Documentation

- **Plugin README**: Full usage guide with examples
- **API Docs**: Nixtla Billing API reference
- **Troubleshooting Guide**: Common issues and solutions
- **GitHub Issues**: Bug reports and feature requests
- **Slack Community**: #nixtla-cost-optimization channel
```

---

## User Journey

### Journey 1: First-Time Cost Audit

**Persona**: Sarah, Data Engineering Manager at RetailCo
**Goal**: Understand why Nixtla costs tripled this quarter
**Starting Point**: Has Nixtla API key, no prior optimization

**Steps**:

1. **Install Plugin**
   ```
   Sarah: /plugin install nixtla-cost-optimizer@claude-code-plugins-plus

   Claude: ✅ Plugin installed
           Running setup script...
           ✅ Dependencies installed
           ✅ Database initialized

           Next: Add your NIXTLA_API_KEY to .env file
   ```

2. **Configure API Key**
   ```
   Sarah: Opens ~/.claude/plugins/nixtla-cost-optimizer/.env

   Adds: NIXTLA_API_KEY=nixak-...

   Claude: Detected .env change
           Reloading MCP server...
           ✅ API key validated
   ```

3. **Run First Analysis**
   ```
   Sarah: /nixtla-optimize

   Claude: Welcome! First-time setup...

           Fetching 30 days of usage logs...
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           ✅ 245,892 forecast requests
           ✅ 10,485 unique series
           ✅ Total cost: $12,450.23

           Analyzing patterns...
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           🔍 Detected 127 redundancy patterns
           🔍 Found 75 safe optimization opportunities

           [Full report displays]
   ```

4. **Review Top Offenders**
   ```
   Sarah: "Why is SKU_42873 costing $850/month?"

   Claude: [Skill auto-activates]

           Analyzing SKU_42873...

           PATTERN DETECTED:
           - Forecasted 43,200 times (every hour)
           - Data unchanged for 25 days (99.8% identical hashes)
           - Cost: $850/month

           ROOT CAUSE:
           Script: forecast_high_value_skus.py
           Line 42: cron_schedule="0 * * * *"  # Hourly

           RECOMMENDATION:
           Enable 24-hour caching
           Expected savings: $820/month
           Risk: Low (data barely changes)

           Apply this fix? [y/N]
   ```

5. **Apply Safe Recommendations**
   ```
   Sarah: y

   Claude: Applying caching rule for SKU_42873...

           ✅ Created caching rule (TTL: 24h)
           ✅ Updated cost_optimizer.db
           ✅ Estimated next month: $30/mo (was $850/mo)

           Would you like to apply all 75 safe recommendations? [y/N]
   ```

6. **Batch Apply & Monitor**
   ```
   Sarah: y

   Claude: Applying 75 safe recommendations...
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           ✅ Enabled caching for 42 series
           ✅ Removed 33 dormant series

           PROJECTED IMPACT:
           Current Monthly Cost:  $12,450
           Projected New Cost:    $4,560
           Savings:              $7,890 (63%)

           Setting up monitoring...
           ✅ Slack alerts configured (threshold: $1,000 spike)
           ✅ Scheduled monthly audit (1st of each month)

           Next audit: 2025-12-01
   ```

7. **Verify Savings (Next Month)**
   ```
   [30 days later]

   Claude: [Automated monthly audit]

           📊 Monthly Cost Report (December 2025)

           Previous Month: $12,450
           Current Month:  $4,680
           ACTUAL SAVINGS: $7,770 (62%)

           Cache Hit Rate: 12% → 61% (+49 pp)

           🎉 Congratulations! You saved $7,770 this month.

           NEW OPPORTUNITIES: $890/mo additional savings available
           Run /nixtla-optimize to see details.
   ```

**Outcome**: Sarah reduces Nixtla costs by 62% ($93k annual savings) and sets up automated monitoring to prevent future bill shock.

---

### Journey 2: Bill Shock Investigation

**Persona**: Marcus, DevOps Engineer
**Goal**: Figure out why this month's Nixtla bill is $18k (normally $5k)
**Starting Point**: Plugin already installed, received bill shock alert

**Steps**:

1. **Receive Alert**
   ```
   [Slack notification]

   🚨 NIXTLA COST SPIKE ALERT

   November bill: $18,350
   Previous month: $5,240
   SPIKE: +$13,110 (+250%)

   Run /nixtla-optimize to investigate
   ```

2. **Investigate Spike**
   ```
   Marcus: /nixtla-optimize --spike-detection

   Claude: 🚨 COST SPIKE DETECTED

           Analyzing root cause...
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           TIMELINE:
           Nov 1-14:  $4,850 (normal)
           Nov 15:    +$950 spike
           Nov 16-30: $12,550 elevated

           SPIKE ORIGIN: November 15, 14:23:18 UTC
   ```

3. **Root Cause Analysis**
   ```
   Claude: ROOT CAUSE IDENTIFIED
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           Script: forecast_all_skus.py
           Created: 2025-11-15 14:23:18
           Author: [email protected]

           ISSUE: Cron job set to 1-minute interval

           crontab entry:
           * * * * * /usr/bin/python3 /opt/forecasting/forecast_all_skus.py

           IMPACT:
           - 10,485 series × 1,440 runs/day = 15M forecasts/month
           - Cost if continued: $758,880/month
           - Actual cost (15 days): $13,110

           RECOMMENDED FIX:
           Change to hourly:
           0 * * * * /usr/bin/python3 /opt/forecasting/forecast_all_skus.py
   ```

4. **Fix & Validate**
   ```
   Marcus: "Fix this automatically"

   Claude: Fixing cron job...

           ✅ Edited crontab (changed to hourly)
           ✅ Validated new schedule
           ✅ Restarted cron daemon

           VERIFICATION:
           Old: Runs every 1 minute
           New: Runs every 1 hour

           PROJECTED COST CORRECTION:
           Next month: $5,200 (back to normal)
           Savings: $753,680/month avoided

           Setting up safeguard...
           ✅ Added frequency limit check
           ✅ Will alert if >24 forecasts/hour detected
   ```

5. **Document Incident**
   ```
   Claude: Generating incident report...

           📄 INCIDENT REPORT
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           Date: 2025-11-15
           Type: Cost Spike
           Severity: Critical
           Root Cause: Misconfigured cron job
           Impact: +$13,110 (1 billing cycle)
           Resolution Time: 12 minutes

           PREVENTIVE MEASURES:
           ✅ Frequency validation added
           ✅ Cost spike alerts configured
           ✅ Code review required for forecast scripts

           Report saved: reports/incident-2025-11-30.pdf

           Send to team? [Slack/Email/Both] _
   ```

**Outcome**: Marcus identifies and fixes the misconfigured cron job in 12 minutes, preventing $753k in unnecessary costs. Sets up safeguards to prevent recurrence.

---

### Journey 3: Proactive Scale-Up Optimization

**Persona**: Lisa, VP of Data Science
**Goal**: Scale forecasting from 10k to 100k series without 10x cost increase
**Starting Point**: Current usage optimized, planning major expansion

**Steps**:

1. **Pre-Scale Analysis**
   ```
   Lisa: "We're scaling from 10k to 100k forecast series next quarter.
          Optimize before we launch."

   Claude: [Skill auto-activates]

           Running pre-scale cost projection...
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           CURRENT STATE:
           Series: 10,485
           Monthly Cost: $4,680 (optimized)
           Cost per Series: $0.45

           PROJECTED (10x scale):
           Series: 104,850
           Without optimization: $46,800/month
           Risk: Medium-High (bill shock likely)
   ```

2. **Optimization Strategy**
   ```
   Claude: SCALE-UP OPTIMIZATION STRATEGY
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           Strategy 1: Tiered Caching
           - Critical series (10%): No cache, real-time
           - Important series (30%): 1h TTL
           - Standard series (60%): 24h TTL
           Projected Cost: $18,700/month (60% savings)

           Strategy 2: Intelligent Frequency
           - High volatility: Hourly
           - Medium volatility: Daily
           - Low volatility: Weekly
           Projected Cost: $21,200/month (55% savings)

           Strategy 3: Hybrid (Recommended)
           - Combines caching + frequency optimization
           - Pre-forecast data change detection
           - Batch processing for stable series
           Projected Cost: $14,500/month (69% savings)

           RECOMMENDATION: Strategy 3
           Estimated implementation: 3-5 days
   ```

3. **Implementation Plan**
   ```
   Lisa: "Generate implementation plan for Strategy 3"

   Claude: 📋 IMPLEMENTATION PLAN
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           PHASE 1: Data Classification (Day 1)
           ✅ Analyze historical volatility for all 104k series
           ✅ Assign tier (critical/important/standard)
           ✅ Set initial caching rules

           PHASE 2: Infrastructure Setup (Day 2)
           ✅ Deploy Redis cache cluster (AWS ElastiCache)
           ✅ Implement data change detection layer
           ✅ Set up batch processing queue

           PHASE 3: Gradual Rollout (Days 3-5)
           ✅ Day 3: Enable for 10% of series (10k)
           ✅ Day 4: Expand to 50% (52k)
           ✅ Day 5: Full rollout (104k)

           PHASE 4: Monitoring (Ongoing)
           ✅ Daily cost tracking
           ✅ Weekly cache hit rate review
           ✅ Monthly re-classification

           RISK MITIGATION:
           - Canary deployment (test on 1k series first)
           - Rollback plan prepared
           - Cost circuit breaker at $20k/month

           Export as: [Jira Epic / GitHub Project / PDF] _
   ```

4. **Execute & Monitor**
   ```
   Lisa: "Execute Phase 1"

   Claude: Analyzing 104,850 series volatility...
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           Processing: [████████████████████] 100%

           CLASSIFICATION RESULTS:
           ✅ Critical (10%):    10,485 series - No cache
           ✅ Important (30%):   31,455 series - 1h TTL
           ✅ Standard (60%):    62,910 series - 24h TTL

           CACHING RULES GENERATED:
           - 94,365 series will use intelligent caching
           - Estimated cache hit rate: 72%
           - Projected monthly cost: $14,200

           Ready to proceed to Phase 2? [y/N]
   ```

5. **Post-Launch Validation**
   ```
   [7 days after full rollout]

   Claude: [Automated weekly report]

           📊 SCALE-UP SUCCESS REPORT
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           BEFORE OPTIMIZATION:
           Series: 10,485
           Cost: $4,680/month

           AFTER SCALE-UP:
           Series: 104,850 (10x)
           Cost: $14,890/month (3.2x)

           SAVINGS vs UNOPTIMIZED:
           Projected: $46,800
           Actual: $14,890
           SAVED: $31,910/month (68%)

           KEY METRICS:
           Cache Hit Rate: 74% (target: 72%)
           Avg Latency: 145ms (acceptable)
           Accuracy: Unchanged (no degradation)

           🎉 Scale-up successful! You're saving $382k/year.
   ```

**Outcome**: Lisa scales forecasting 10x while keeping costs at 3.2x through intelligent optimization. Saves $382k annually compared to unoptimized approach.

---

## Reports Generated

### 1. Console Report (Real-Time)

```
💸 NIXTLA COST OPTIMIZATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Period: 30 days (2025-10-30 to 2025-11-30)

CURRENT COSTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Spend:          $12,450.23
Total Forecasts:      245,892
Cost per Forecast:    $0.0506
Unique Series:        10,485
Cache Hit Rate:       12% (target: 60%)

POTENTIAL SAVINGS: $7,890/month (63%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Enable Caching:           $4,250 (54%)
💰 Reduce Frequency:         $2,890 (37%)
💰 Remove Dormant Series:    $750 (9%)

🔴 TOP 10 COST OFFENDERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. SKU_42873 - $850/mo
2. payment_type_cash - $720/mo
3. region_US_WEST - $640/mo
...
```

### 2. JSON Export (Programmatic Access)

```json
{
  "report_id": "cost-opt-2025-11-30-142315",
  "generated_at": "2025-11-30T14:23:15Z",
  "period": {
    "start_date": "2025-10-30",
    "end_date": "2025-11-30",
    "days": 30
  },
  "current_costs": {
    "total_usd": 12450.23,
    "forecasts": 245892,
    "cost_per_forecast": 0.0506,
    "unique_series": 10485,
    "cache_hit_rate_pct": 12.4
  },
  "potential_savings": {
    "total_usd": 7890.00,
    "percentage": 63.4,
    "breakdown": {
      "caching": 4250.00,
      "frequency_optimization": 2890.00,
      "dormant_series_removal": 750.00
    }
  },
  "top_offenders": [
    {
      "series_id": "SKU_42873",
      "monthly_cost_usd": 850.00,
      "forecast_count": 43200,
      "issue": "forecasted_hourly_with_unchanged_data",
      "data_change_rate_pct": 0.2,
      "recommendation": {
        "type": "enable_caching",
        "ttl_seconds": 86400,
        "estimated_savings_usd": 820.00,
        "risk_level": "low",
        "auto_apply_safe": true
      }
    }
  ],
  "recommendations": [
    {
      "id": "rec-001",
      "type": "enable_caching",
      "series_id": "SKU_42873",
      "current_state": "forecasted 43200 times/month",
      "recommended_state": "cache with 24h TTL",
      "estimated_monthly_savings_usd": 820.00,
      "risk_level": "low",
      "auto_apply_safe": true,
      "implementation": {
        "command": "apply_caching_rule",
        "args": {
          "series_id": "SKU_42873",
          "ttl_seconds": 86400
        }
      }
    }
  ]
}
```

### 3. CSV Export (Spreadsheet Analysis)

```csv
series_id,monthly_cost_usd,forecast_count,issue_type,recommendation_type,estimated_savings_usd,risk_level,auto_apply_safe
SKU_42873,850.00,43200,forecasted_hourly_unchanged,enable_caching,820.00,low,true
payment_type_cash,720.00,720,identical_reforecast,enable_caching,680.00,low,true
region_US_WEST,640.00,1440,unnecessary_high_frequency,reduce_frequency,590.00,medium,false
...
```

### 4. PDF Executive Summary

**Page 1: Executive Summary**
- Total cost overview
- Savings potential (pie chart)
- Top 5 recommendations

**Page 2: Detailed Analysis**
- Usage trends (30-day line chart)
- Cost by series (bar chart)
- Cache hit rate trend

**Page 3: Implementation Plan**
- Prioritized recommendation list
- Risk assessment matrix
- Timeline and milestones

### 5. Slack Alert (Real-Time)

```
🚨 NIXTLA COST SPIKE ALERT

November bill: $18,350
Previous month: $5,240
SPIKE: +$13,110 (+250%)

Root Cause: Misconfigured cron job (running every 1 min)

View full report: /nixtla-optimize
```

---

## Dependencies

### Installation Dependencies

```bash
# setup.sh dependencies
- bash >=4.0
- python3 >=3.10
- pip
- jq (for JSON manipulation)
- curl (for API requests)
```

### Python Dependencies

```txt
# requirements.txt
nixtla>=0.7.1                  # Nixtla API client
pandas>=2.0.3                  # Data manipulation
numpy>=2.3.0                   # Numerical operations
requests>=2.32.0               # HTTP client
python-dotenv>=1.0.1           # Environment variables
pydantic>=2.12.0               # Data validation
sqlalchemy>=2.0.36             # Database ORM
alembic>=1.14.0                # Database migrations
click>=8.1.8                   # CLI framework
rich>=13.9.4                   # Terminal formatting
pytest>=8.3.4                  # Testing framework
pytest-cov>=6.0.0              # Coverage reporting
black>=25.1.0                  # Code formatting
mypy>=1.15.0                   # Type checking
ruff>=0.9.1                    # Linting
```

### MCP Server Dependencies

```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.21.1",
    "better-sqlite3": "^12.4.0",
    "zod": "^4.1.12",
    "date-fns": "^5.0.0"
  },
  "devDependencies": {
    "@types/better-sqlite3": "^7.6.11",
    "@types/node": "^24.10.0",
    "typescript": "^5.5.0",
    "tsx": "^4.19.0"
  }
}
```

### External Service Dependencies

```yaml
# Optional integrations
slack:
  required: false
  webhook_url: SLACK_WEBHOOK_URL env var

pagerduty:
  required: false
  api_key: PAGERDUTY_API_KEY env var
  service_id: PAGERDUTY_SERVICE_ID env var

bigquery:
  required: false
  project_id: GCP_PROJECT_ID env var
  service_account: GCP_SA_KEY_PATH env var

snowflake:
  required: false
  account: SNOWFLAKE_ACCOUNT env var
  warehouse: SNOWFLAKE_WAREHOUSE env var
```

---

## Deployment

### Local Development

```bash
# Clone plugin
cd ~/.claude/plugins/nixtla-cost-optimizer

# Install dependencies
./scripts/setup.sh

# Run tests
source .venv/bin/activate
pytest tests/ -v --cov=src

# Run locally
python3 src/cost_analyzer.py --analyze --days 30
```

### Production Deployment

```bash
# Build MCP server
cd mcp
pnpm install
pnpm build

# Verify build
node dist/index.js --version

# Configure in Claude Code
# (Handled automatically by setup.sh)
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test Nixtla Cost Optimizer

on:
  push:
    branches: [main]
    paths:
      - 'plugins/ai-ml/nixtla-cost-optimizer/**'
  pull_request:
    paths:
      - 'plugins/ai-ml/nixtla-cost-optimizer/**'

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          cd plugins/ai-ml/nixtla-cost-optimizer
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests
        run: |
          cd plugins/ai-ml/nixtla-cost-optimizer
          pytest tests/ -v --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          flags: nixtla-cost-optimizer
```

### Monitoring & Alerting

```bash
# Set up automated monitoring
/nixtla-schedule-audit --frequency monthly

# Configure alerts
/nixtla-configure-alerts \
  --slack-webhook $SLACK_WEBHOOK_URL \
  --threshold 1000 \
  --pagerduty-key $PAGERDUTY_API_KEY
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-30
**Next Review**: 2026-01-15
**Maintainer**: Intent Solutions ([email protected])
