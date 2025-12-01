# Plugin #2: Nixtla vs StatsForecast Benchmark
**Technical Architecture & Implementation Specification**

**Created**: 2025-11-30
**Status**: Design Phase
**Priority**: Tier 1 (IMMEDIATE VALUE)
**Addresses**: Free Tier Trap (Friction #1)

---

## Executive Summary

### What It Is
A side-by-side comparison tool that benchmarks TimeGPT API against local StatsForecast OSS models, providing accuracy metrics (MAPE, RMSE, sMAPE) and comprehensive ROI calculations to justify the upgrade from free to paid forecasting.

### Why It Exists
Nixtla's CRO faces this dilemma:
> "Why would a user who can get 90% accuracy from StatsForecast for free ever pay for TimeGPT? The 2% gain must translate into business value that exceeds API costs."

**This plugin proves (or disproves) the value proposition with hard data.**

### Who It's For
- **Data science teams** evaluating TimeGPT adoption
- **Finance/procurement teams** requiring ROI justification
- **Engineering managers** deciding between OSS and API
- **Nixtla sales team** needing proof points for enterprise deals

---

## Architecture Overview

### Component Stack

```
┌─────────────────────────────────────────────────────────────┐
│  USER INTERFACE                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Slash Command│  │ Agent Skill  │  │  Web Dashboard  │  │
│  │ /benchmark   │  │(Auto-invoke) │  │  (localhost:3000)│  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  BENCHMARKING ENGINE (Python)                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Parallel Executor                                    │  │
│  │  ├─ StatsForecast Runner (AutoARIMA, AutoETS, etc.) │  │
│  │  ├─ TimeGPT API Caller                               │  │
│  │  ├─ Metrics Calculator (MAPE, RMSE, sMAPE)          │  │
│  │  ├─ Cost Modeler                                     │  │
│  │  └─ ROI Calculator                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA & STORAGE                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │SQLite Results│  │  CSV Exports│  │  Nixtla API      │   │
│  │ (history)   │  │  (sharing)  │  │  + statsforecast │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Plugin Type
**AI Instruction** (Skills/Commands) with optional Web Dashboard

### Components

1. **Slash Commands** (2)
   - `/nixtla-benchmark` - Run full benchmark comparison
   - `/nixtla-quick-compare` - Fast comparison on sample data

2. **Agent Skill** (1)
   - `nixtla-benchmark-expert` - Auto-invokes on "should I use TimeGPT" questions

3. **Web Dashboard** (1)
   - React app for interactive visualization (optional)

4. **No MCP Server** - Pure Python CLI tool

---

## API Keys & User Requirements

### Required API Keys

```bash
# .env file
NIXTLA_API_KEY=nixak-...                      # Required for TimeGPT comparison
```

### User Requirements

#### Minimum
- **Python 3.10+** with numpy, pandas
- **statsforecast 2.0.3+** library installed
- **10MB disk space** for SQLite results database
- **Sample dataset** (CSV with columns: unique_id, ds, y)

#### Recommended
- **Historical data** - At least 100 data points per series
- **Multiple series** - 10+ series for meaningful statistical comparison
- **Ground truth** - Known actuals for forecast period (for accuracy calculation)

#### Optional
- **Jupyter notebook** - For interactive exploration
- **Plotly/Matplotlib** - For custom visualizations

---

## Installation Process

### setup.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Setting up Nixtla vs StatsForecast Benchmark..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 required"
    exit 1
fi

# Create venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
python3 src/init_db.py

# Configure .env
if [ ! -f ".env" ]; then
    cat > .env <<EOF
# Nixtla API Key (required)
NIXTLA_API_KEY=your_api_key_here

# Business Context (for ROI calculation)
MONTHLY_REVENUE_USD=1000000
FORECAST_ACCURACY_IMPACT_PCT=5

# Computing Costs (for TCO comparison)
AWS_INSTANCE_TYPE=r5.2xlarge
AWS_HOURLY_RATE_USD=0.50
EOF

    echo "⚠️  Edit .env file with your API key and business context"
fi

echo "✅ Setup complete!"
echo ""
echo "Run: /nixtla-benchmark --dataset your_data.csv --horizon 30"
```

---

## Technical Schemas

### Benchmark Results Schema (SQLite)

```sql
CREATE TABLE benchmark_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    dataset_name TEXT NOT NULL,
    series_count INTEGER NOT NULL,
    history_length INTEGER NOT NULL,
    horizon INTEGER NOT NULL,
    frequency TEXT,                    -- 'D', 'H', 'M', etc.
    models_tested TEXT,                -- JSON array
    total_runtime_seconds DECIMAL(10, 2),
    INDEX idx_run_id (run_id),
    INDEX idx_created_at (created_at)
);

CREATE TABLE model_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    is_timegpt BOOLEAN DEFAULT 0,
    mape DECIMAL(10, 6),
    rmse DECIMAL(10, 6),
    smape DECIMAL(10, 6),
    mae DECIMAL(10, 6),
    training_time_seconds DECIMAL(10, 2),
    inference_time_seconds DECIMAL(10, 2),
    api_cost_usd DECIMAL(10, 4),
    compute_cost_usd DECIMAL(10, 4),
    FOREIGN KEY (run_id) REFERENCES benchmark_runs(run_id),
    INDEX idx_run_model (run_id, model_name)
);

CREATE TABLE series_forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    series_id TEXT NOT NULL,
    forecast_date DATE NOT NULL,
    forecast_value DECIMAL(18, 6),
    actual_value DECIMAL(18, 6),
    absolute_error DECIMAL(18, 6),
    FOREIGN KEY (run_id) REFERENCES benchmark_runs(run_id),
    INDEX idx_series (run_id, series_id)
);
```

### Configuration Schema (JSON)

```json
{
  "benchmark_config": {
    "version": "1.0.0",
    "models": {
      "statsforecast": [
        "AutoARIMA",
        "AutoETS",
        "AutoTheta",
        "SeasonalNaive",
        "CrostonClassic"
      ],
      "timegpt": {
        "enabled": true,
        "models": ["TimeGPT-1"],
        "finetune": false
      }
    },
    "evaluation": {
      "metrics": ["MAPE", "RMSE", "sMAPE", "MAE"],
      "confidence_intervals": [80, 90, 95],
      "cross_validation": {
        "enabled": true,
        "n_windows": 3,
        "step_size": 7
      }
    },
    "cost_modeling": {
      "timegpt_pricing": {
        "per_series_per_forecast": 0.001,
        "monthly_api_fee": 0
      },
      "compute_pricing": {
        "aws_instance_type": "r5.2xlarge",
        "hourly_rate_usd": 0.50,
        "utilization_factor": 0.7
      },
      "business_context": {
        "monthly_revenue_usd": 1000000,
        "forecast_accuracy_impact_pct": 5
      }
    },
    "output": {
      "save_forecasts": true,
      "export_csv": true,
      "generate_plots": true,
      "create_html_report": true
    }
  }
}
```

---

## Code Implementation

### Directory Structure

```
plugins/ai-ml/nixtla-vs-statsforecast-benchmark/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── LICENSE
├── commands/
│   ├── benchmark.md                  # /nixtla-benchmark
│   └── quick-compare.md              # /nixtla-quick-compare
├── skills/
│   └── benchmark-expert/
│       └── SKILL.md
├── src/
│   ├── __init__.py
│   ├── init_db.py
│   ├── benchmark_runner.py           # Core benchmarking logic
│   ├── metrics.py                    # Accuracy metrics calculation
│   ├── cost_modeler.py               # TCO and ROI calculation
│   ├── report_generator.py           # HTML/Markdown reports
│   └── models/
│       ├── statsforecast_wrapper.py
│       └── timegpt_wrapper.py
├── scripts/
│   ├── setup.sh
│   └── run-benchmark.py              # Standalone CLI
├── tests/
│   ├── test_benchmark_runner.py
│   ├── test_metrics.py
│   └── fixtures/
│       └── m4_sample.csv
├── dashboard/                        # Optional React dashboard
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── dist/
├── requirements.txt
├── .env.example
└── benchmark_results.db
```

### Key Implementation: benchmark_runner.py

```python
"""
Core benchmarking engine for Nixtla vs StatsForecast comparison
"""
import time
import hashlib
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from statsforecast import StatsForecast
from statsforecast.models import (
    AutoARIMA,
    AutoETS,
    AutoTheta,
    SeasonalNaive,
    CrostonClassic
)
from nixtla import NixtlaClient

from .metrics import MetricsCalculator
from .cost_modeler import CostModeler


@dataclass
class BenchmarkResult:
    """Results from a single model benchmark"""
    model_name: str
    is_timegpt: bool
    mape: float
    rmse: float
    smape: float
    mae: float
    training_time_seconds: float
    inference_time_seconds: float
    api_cost_usd: float
    compute_cost_usd: float
    forecasts: pd.DataFrame


class BenchmarkRunner:
    """Orchestrates parallel benchmarking of StatsForecast and TimeGPT"""

    def __init__(
        self,
        nixtla_api_key: str,
        cost_config: Optional[Dict] = None
    ):
        self.nixtla_api_key = nixtla_api_key
        self.cost_modeler = CostModeler(cost_config or {})
        self.metrics_calculator = MetricsCalculator()

    def run_benchmark(
        self,
        df: pd.DataFrame,
        horizon: int,
        freq: str = 'D',
        models: Optional[List[str]] = None,
        include_timegpt: bool = True,
        n_jobs: int = -1
    ) -> Dict[str, BenchmarkResult]:
        """
        Run comprehensive benchmark comparison

        Args:
            df: DataFrame in Nixtla format (unique_id, ds, y)
            horizon: Forecast horizon
            freq: Frequency ('D', 'H', 'M', etc.)
            models: List of StatsForecast models to test
            include_timegpt: Whether to include TimeGPT in comparison
            n_jobs: Number of parallel jobs (-1 = all cores)

        Returns:
            Dict mapping model name to BenchmarkResult
        """
        if models is None:
            models = ['AutoARIMA', 'AutoETS', 'AutoTheta', 'SeasonalNaive']

        # Split data into train/test
        train_df, test_df = self._train_test_split(df, horizon)

        results = {}

        # Run StatsForecast models in parallel
        print(f"Running {len(models)} StatsForecast models...")
        with ThreadPoolExecutor(max_workers=n_jobs if n_jobs > 0 else None) as executor:
            future_to_model = {
                executor.submit(self._run_statsforecast_model, model, train_df, horizon, freq): model
                for model in models
            }

            for future in as_completed(future_to_model):
                model_name = future_to_model[future]
                try:
                    result = future.result()
                    results[model_name] = result
                    print(f"  ✅ {model_name}: MAPE={result.mape:.2f}%")
                except Exception as e:
                    print(f"  ❌ {model_name} failed: {e}")

        # Run TimeGPT
        if include_timegpt and self.nixtla_api_key:
            print("Running TimeGPT...")
            try:
                result = self._run_timegpt(train_df, horizon, freq)
                results['TimeGPT'] = result
                print(f"  ✅ TimeGPT: MAPE={result.mape:.2f}%")
            except Exception as e:
                print(f"  ❌ TimeGPT failed: {e}")

        # Calculate metrics against test set
        for model_name, result in results.items():
            result.mape, result.rmse, result.smape, result.mae = self.metrics_calculator.calculate(
                result.forecasts,
                test_df
            )

        return results

    def _run_statsforecast_model(
        self,
        model_name: str,
        train_df: pd.DataFrame,
        horizon: int,
        freq: str
    ) -> BenchmarkResult:
        """Run a single StatsForecast model"""
        # Model instantiation
        model_class = {
            'AutoARIMA': AutoARIMA(season_length=self._get_season_length(freq)),
            'AutoETS': AutoETS(season_length=self._get_season_length(freq)),
            'AutoTheta': AutoTheta(season_length=self._get_season_length(freq)),
            'SeasonalNaive': SeasonalNaive(season_length=self._get_season_length(freq)),
            'CrostonClassic': CrostonClassic()
        }[model_name]

        # Training
        start_time = time.time()
        sf = StatsForecast(
            models=[model_class],
            freq=freq,
            n_jobs=-1
        )
        sf.fit(train_df)
        training_time = time.time() - start_time

        # Inference
        start_time = time.time()
        forecasts = sf.predict(h=horizon)
        inference_time = time.time() - start_time

        # Cost calculation
        compute_cost = self.cost_modeler.calculate_compute_cost(
            training_time + inference_time
        )

        return BenchmarkResult(
            model_name=model_name,
            is_timegpt=False,
            mape=0.0,  # Calculated later
            rmse=0.0,
            smape=0.0,
            mae=0.0,
            training_time_seconds=training_time,
            inference_time_seconds=inference_time,
            api_cost_usd=0.0,
            compute_cost_usd=compute_cost,
            forecasts=forecasts.reset_index()
        )

    def _run_timegpt(
        self,
        train_df: pd.DataFrame,
        horizon: int,
        freq: str
    ) -> BenchmarkResult:
        """Run TimeGPT API"""
        client = NixtlaClient(api_key=self.nixtla_api_key)

        # Zero-shot inference (no training)
        start_time = time.time()
        forecasts = client.forecast(
            df=train_df,
            h=horizon,
            freq=freq,
            level=[80, 90, 95]
        )
        inference_time = time.time() - start_time

        # Cost calculation
        api_cost = self.cost_modeler.calculate_timegpt_cost(
            series_count=train_df['unique_id'].nunique(),
            forecast_points=horizon
        )

        return BenchmarkResult(
            model_name='TimeGPT',
            is_timegpt=True,
            mape=0.0,
            rmse=0.0,
            smape=0.0,
            mae=0.0,
            training_time_seconds=0.0,  # Zero-shot
            inference_time_seconds=inference_time,
            api_cost_usd=api_cost,
            compute_cost_usd=0.0,  # API handles compute
            forecasts=forecasts
        )

    def _train_test_split(
        self,
        df: pd.DataFrame,
        horizon: int
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Split data into train and test sets"""
        test_cutoff = df.groupby('unique_id')['ds'].max() - pd.Timedelta(days=horizon)

        train_df = df[df['ds'] <= df.groupby('unique_id')['ds'].transform('max') - pd.Timedelta(days=horizon)]
        test_df = df[df['ds'] > df.groupby('unique_id')['ds'].transform('max') - pd.Timedelta(days=horizon)]

        return train_df, test_df

    def _get_season_length(self, freq: str) -> int:
        """Get appropriate seasonality for frequency"""
        return {
            'D': 7,    # Daily -> Weekly
            'H': 24,   # Hourly -> Daily
            'M': 12,   # Monthly -> Yearly
            'W': 52    # Weekly -> Yearly
        }.get(freq, 1)
```

---

## User Journeys

### Journey 1: Initial Evaluation

**Persona**: Alex, Senior Data Scientist
**Goal**: Decide if TimeGPT is worth the investment vs free StatsForecast
**Context**: Has 3 months of daily sales data for 50 products

**Steps**:

1. **Install Plugin**
   ```
   Alex: /plugin install nixtla-vs-statsforecast-benchmark@claude-code-plugins-plus

   Claude: ✅ Installed
           Running setup...
           ✅ Dependencies installed

           Add your NIXTLA_API_KEY to .env file
   ```

2. **Prepare Dataset**
   ```
   Alex: "I have sales data in sales_data.csv - can you benchmark it?"

   Claude: [Skill auto-activates]

           Reading sales_data.csv...
           ✅ 4,500 rows (90 days × 50 products)
           ✅ Frequency detected: Daily (D)

           Recommended test:
           - Train: First 60 days
           - Test: Last 30 days
           - Models: AutoARIMA, AutoETS, TimeGPT

           Run benchmark? [y/N]
   ```

3. **Run Benchmark**
   ```
   Alex: y

   Claude: Running benchmark...
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           Training/Testing split...
           ✅ Train: 3,000 observations
           ✅ Test: 1,500 observations

           Running 3 models in parallel...
           ✅ AutoARIMA: MAPE=8.4% (12.3s)
           ✅ AutoETS: MAPE=9.1% (4.2s)
           ✅ TimeGPT: MAPE=6.8% (2.1s)

           Benchmark complete! (18.6s total)
   ```

4. **Review Results**
   ```
   Claude: 📊 BENCHMARK RESULTS
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           Dataset: sales_data.csv
           Series: 50 products
           History: 60 days → Forecast: 30 days

           ACCURACY COMPARISON
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           Model        MAPE    RMSE    sMAPE   Training   Inference
           ─────────────────────────────────────────────────────────
           TimeGPT      6.8%    145.3   6.4%    0.0s       2.1s
           AutoARIMA    8.4%    167.2   7.9%    12.3s      0.5s
           AutoETS      9.1%    182.4   8.5%    4.2s       0.3s

           🏆 WINNER: TimeGPT
           Improvement: 1.6% better MAPE than best OSS (AutoARIMA)

           COST COMPARISON (Monthly at Current Scale)
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           TimeGPT API:      $420/mo (50 series × 30 forecasts × $0.28)
           StatsForecast:    $0 API + $45 compute (r5.2xlarge @ 3h/mo)

           ROI ANALYSIS
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           Your monthly revenue: $1,000,000
           Forecast-driven decisions: 5% of revenue

           Value of 1.6% accuracy improvement:
           $1M × 5% × 1.6% = $800/month

           Cost:     $420/month (TimeGPT API)
           Value:    $800/month (improved accuracy)
           ROI:      90% ($380/mo profit)

           ✅ RECOMMENDATION: TimeGPT justified for your use case
   ```

**Outcome**: Alex gets clear data showing TimeGPT is 1.6% more accurate and delivers positive ROI ($380/mo profit).

---

## Reports Generated

### 1. Console Report (Shown Above)

### 2. HTML Interactive Report

```html
<!DOCTYPE html>
<html>
<head>
    <title>Nixtla Benchmark Report</title>
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
</head>
<body>
    <h1>Benchmark Results: sales_data.csv</h1>

    <!-- Accuracy Comparison Chart -->
    <div id="accuracy-chart"></div>
    <script>
        var data = [
            {
                x: ['TimeGPT', 'AutoARIMA', 'AutoETS'],
                y: [6.8, 8.4, 9.1],
                type: 'bar',
                name: 'MAPE (%)'
            }
        ];
        Plotly.newPlot('accuracy-chart', data, {title: 'Accuracy Comparison'});
    </script>

    <!-- ROI Analysis -->
    <div id="roi-chart"></div>

    <!-- Series-by-Series Comparison -->
    <table>
        <tr>
            <th>Series ID</th>
            <th>TimeGPT MAPE</th>
            <th>Best OSS MAPE</th>
            <th>Winner</th>
        </tr>
        <!-- Data rows -->
    </table>
</body>
</html>
```

### 3. CSV Export

```csv
model_name,is_timegpt,mape,rmse,smape,mae,training_time_seconds,inference_time_seconds,api_cost_usd,compute_cost_usd,total_cost_usd
TimeGPT,true,6.8,145.3,6.4,98.2,0.0,2.1,420.00,0.00,420.00
AutoARIMA,false,8.4,167.2,7.9,112.5,12.3,0.5,0.00,45.00,45.00
AutoETS,false,9.1,182.4,8.5,121.3,4.2,0.3,0.00,45.00,45.00
```

---

## Dependencies

```txt
# requirements.txt
statsforecast>=2.0.3
nixtla>=0.7.1
pandas>=2.0.3
numpy>=2.3.0
scikit-learn>=1.3.0
plotly>=5.18.0
jinja2>=3.1.2
python-dotenv>=1.0.1
pydantic>=2.12.0
sqlalchemy>=2.0.36
click>=8.1.8
rich>=13.9.4
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-30
