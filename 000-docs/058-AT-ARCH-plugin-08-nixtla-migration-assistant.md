# Plugin #8: Nixtla Migration Assistant
**Technical Architecture & Implementation Specification**

**Created**: 2025-11-30
**Status**: Design Phase
**Priority**: Tier 1 (CONVERSION ACCELERATOR)
**Addresses**: Free Tier Trap (Friction #1) + POC-to-Production Chasm (Friction #2)

---

## Executive Summary

### What It Is
An automated migration tool that analyzes existing StatsForecast/MLForecast code and generates equivalent TimeGPT API calls, with side-by-side A/B testing, rollback safety, and accuracy validation.

### Why It Exists
Nixtla's CRO identifies the core friction:
> "Users start with OSS StatsForecast (free), build workflows around it, then resist paying for TimeGPT API because migration seems risky and time-consuming."

**This plugin makes OSS → TimeGPT migration automatic, safe, and reversible.**

### Who It's For
- **Data Scientists** with production StatsForecast pipelines
- **ML Engineers** wanting to upgrade to TimeGPT
- **Teams** hesitant about API migration risk
- **Managers** needing accuracy validation before switching

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  USER CODE (StatsForecast/MLForecast)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  sf = StatsForecast(                                  │  │
│  │      models=[AutoARIMA(), AutoETS()],                │  │
│  │      freq='M'                                         │  │
│  │  )                                                     │  │
│  │  sf.fit(df)                                           │  │
│  │  forecasts = sf.predict(h=12)                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  MIGRATION ASSISTANT (Pure Python)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Phase 1: Code Analyzer                               │  │
│  │  - Parse Python AST (Abstract Syntax Tree)           │  │
│  │  - Identify StatsForecast/MLForecast patterns        │  │
│  │  - Extract config (models, freq, horizon)            │  │
│  │                                                        │  │
│  │  Phase 2: API Converter                              │  │
│  │  - Generate equivalent TimeGPT code                  │  │
│  │  - Preserve DataFrame format                         │  │
│  │  - Map models → TimeGPT (no direct mapping)         │  │
│  │                                                        │  │
│  │  Phase 3: A/B Test Runner                            │  │
│  │  - Run both OSS and TimeGPT in parallel             │  │
│  │  - Compare accuracy (sMAPE, MASE)                    │  │
│  │  - Measure latency and cost                          │  │
│  │                                                        │  │
│  │  Phase 4: Migration Report                           │  │
│  │  - Accuracy comparison                                │  │
│  │  - Cost analysis                                      │  │
│  │  - Rollback plan                                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT (TimeGPT-Ready Code)                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  from nixtla import NixtlaClient                      │  │
│  │                                                        │  │
│  │  client = NixtlaClient(api_key='...')                │  │
│  │  forecasts = client.forecast(                         │  │
│  │      df=df,                                           │  │
│  │      h=12,                                            │  │
│  │      freq='M'                                         │  │
│  │  )                                                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Plugin Type
**AI Instruction** (Pure Python)

### Components

1. **Slash Commands** (3)
   - `/nixtla-migrate` - Interactive migration wizard
   - `/nixtla-ab-test` - Run A/B test (OSS vs TimeGPT)
   - `/nixtla-rollback` - Rollback to StatsForecast

2. **Agent Skill** (1)
   - `nixtla-migration-expert` - Auto-invoked when user mentions "migrate to TimeGPT"

3. **No MCP Server** - Pure Python code analysis and transformation

---

## API Keys & User Requirements

### Required
```bash
# Nixtla API (for TimeGPT)
NIXTLA_API_KEY=nixak-...
```

### User Requirements

#### Minimum
- **Python 3.10+**
- **Existing StatsForecast/MLForecast code**
- **Access to training data** (to run A/B test)

#### Current Code Patterns Supported
```python
# StatsForecast
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, AutoTheta

# MLForecast
from mlforecast import MLForecast
from sklearn.ensemble import RandomForestRegressor

# NeuralForecast (limited support)
from neuralforecast import NeuralForecast
from neuralforecast.models import NBEATS
```

---

## Code Implementation

### Directory Structure

```
plugins/nixtla-migration-assistant/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── nixtla-migrate.md
│   ├── nixtla-ab-test.md
│   └── nixtla-rollback.md
├── skills/
│   └── SKILL.md
├── src/
│   ├── __init__.py
│   ├── code_analyzer.py          # AST parsing
│   ├── api_converter.py          # OSS → TimeGPT conversion
│   ├── ab_test_runner.py         # Parallel A/B testing
│   ├── migration_report.py       # PDF/HTML report generator
│   └── rollback_manager.py       # Safety rollback
├── templates/
│   ├── timegpt_template.py       # TimeGPT code template
│   └── migration_report.html     # HTML report template
├── tests/
│   ├── test_code_analyzer.py
│   └── test_api_converter.py
├── examples/
│   ├── statsforecast_example.py  # Input example
│   └── timegpt_output.py         # Output example
├── requirements.txt
└── setup.sh
```

---

## Core Implementation

### src/code_analyzer.py

```python
"""
Analyze StatsForecast/MLForecast code to extract migration parameters
"""
import ast
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ForecastingPattern:
    """Detected forecasting pattern in user code"""
    library: str  # 'statsforecast', 'mlforecast', 'neuralforecast'
    models: List[str]
    horizon: Optional[int]
    freq: Optional[str]
    has_exogenous: bool
    has_cross_validation: bool
    code_snippet: str
    line_number: int


class CodeAnalyzer:
    """Parse Python code to find StatsForecast/MLForecast patterns"""

    SUPPORTED_LIBRARIES = {
        'statsforecast': ['StatsForecast', 'AutoARIMA', 'AutoETS', 'AutoTheta'],
        'mlforecast': ['MLForecast', 'RandomForestRegressor', 'LGBMRegressor'],
        'neuralforecast': ['NeuralForecast', 'NBEATS', 'NHITS'],
    }

    def __init__(self, code_path: str):
        self.code_path = Path(code_path)
        self.code = self.code_path.read_text()
        self.tree = ast.parse(self.code)

    def analyze(self) -> List[ForecastingPattern]:
        """
        Analyze code and extract forecasting patterns

        Returns:
            List of detected forecasting patterns
        """
        patterns = []

        for node in ast.walk(self.tree):
            # Look for StatsForecast initialization
            if isinstance(node, ast.Call):
                if self._is_statsforecast_call(node):
                    pattern = self._extract_statsforecast_pattern(node)
                    if pattern:
                        patterns.append(pattern)

                elif self._is_mlforecast_call(node):
                    pattern = self._extract_mlforecast_pattern(node)
                    if pattern:
                        patterns.append(pattern)

        return patterns

    def _is_statsforecast_call(self, node: ast.Call) -> bool:
        """Check if node is StatsForecast() call"""
        if isinstance(node.func, ast.Name):
            return node.func.id == 'StatsForecast'
        return False

    def _is_mlforecast_call(self, node: ast.Call) -> bool:
        """Check if node is MLForecast() call"""
        if isinstance(node.func, ast.Name):
            return node.func.id == 'MLForecast'
        return False

    def _extract_statsforecast_pattern(self, node: ast.Call) -> Optional[ForecastingPattern]:
        """Extract StatsForecast configuration"""
        models = []
        freq = None
        horizon = None

        # Parse arguments
        for keyword in node.keywords:
            if keyword.arg == 'models':
                models = self._extract_models_list(keyword.value)
            elif keyword.arg == 'freq':
                freq = self._extract_string_value(keyword.value)

        # Find horizon from .predict(h=...) call
        horizon = self._find_horizon_in_scope(node)

        return ForecastingPattern(
            library='statsforecast',
            models=models,
            horizon=horizon,
            freq=freq,
            has_exogenous=False,  # TODO: Detect exogenous variables
            has_cross_validation=self._has_cross_validation(),
            code_snippet=ast.unparse(node),
            line_number=node.lineno
        )

    def _extract_mlforecast_pattern(self, node: ast.Call) -> Optional[ForecastingPattern]:
        """Extract MLForecast configuration"""
        models = []
        freq = None
        lags = []

        for keyword in node.keywords:
            if keyword.arg == 'models':
                models = self._extract_models_list(keyword.value)
            elif keyword.arg == 'freq':
                freq = self._extract_string_value(keyword.value)
            elif keyword.arg == 'lags':
                lags = self._extract_list_value(keyword.value)

        horizon = self._find_horizon_in_scope(node)

        return ForecastingPattern(
            library='mlforecast',
            models=models,
            horizon=horizon,
            freq=freq,
            has_exogenous=False,
            has_cross_validation=self._has_cross_validation(),
            code_snippet=ast.unparse(node),
            line_number=node.lineno
        )

    def _extract_models_list(self, node: ast.expr) -> List[str]:
        """Extract list of model names"""
        models = []

        if isinstance(node, ast.List):
            for element in node.elts:
                if isinstance(element, ast.Call):
                    if isinstance(element.func, ast.Name):
                        models.append(element.func.id)

        return models

    def _extract_string_value(self, node: ast.expr) -> Optional[str]:
        """Extract string literal value"""
        if isinstance(node, ast.Constant):
            return str(node.value)
        return None

    def _extract_list_value(self, node: ast.expr) -> List[Any]:
        """Extract list literal values"""
        if isinstance(node, ast.List):
            return [self._extract_constant_value(e) for e in node.elts]
        return []

    def _extract_constant_value(self, node: ast.expr) -> Any:
        """Extract constant value"""
        if isinstance(node, ast.Constant):
            return node.value
        return None

    def _find_horizon_in_scope(self, node: ast.Call) -> Optional[int]:
        """Find horizon (h) parameter in .predict() or .forecast() calls"""
        # Look for .predict(h=...) in the same function
        for n in ast.walk(self.tree):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Attribute):
                    if n.func.attr in ['predict', 'forecast']:
                        for kw in n.keywords:
                            if kw.arg == 'h':
                                return self._extract_constant_value(kw.value)
        return None

    def _has_cross_validation(self) -> bool:
        """Detect if code uses cross-validation"""
        code_lower = self.code.lower()
        return 'cross_validation' in code_lower or 'cv' in code_lower


    def generate_migration_summary(self, patterns: List[ForecastingPattern]) -> str:
        """Generate human-readable migration summary"""
        summary = []

        summary.append("# Migration Analysis\n")
        summary.append(f"File: {self.code_path}\n")
        summary.append(f"Patterns detected: {len(patterns)}\n\n")

        for i, pattern in enumerate(patterns, 1):
            summary.append(f"## Pattern {i}: {pattern.library}\n")
            summary.append(f"- Models: {', '.join(pattern.models)}\n")
            summary.append(f"- Horizon: {pattern.horizon}\n")
            summary.append(f"- Frequency: {pattern.freq}\n")
            summary.append(f"- Line: {pattern.line_number}\n")
            summary.append(f"- Code:\n```python\n{pattern.code_snippet}\n```\n\n")

        return ''.join(summary)
```

### src/api_converter.py

```python
"""
Convert StatsForecast/MLForecast code to TimeGPT API calls
"""
from typing import Dict, List, Any
from code_analyzer import ForecastingPattern
from jinja2 import Template


class APIConverter:
    """Convert OSS forecasting code to TimeGPT"""

    TIMEGPT_TEMPLATE = """
from nixtla import NixtlaClient
import pandas as pd

# Initialize TimeGPT client
client = NixtlaClient(api_key='{{ api_key or "YOUR_NIXTLA_API_KEY" }}')

# Prepare data (ensure format: unique_id, ds, y)
# df = pd.read_csv('your_data.csv')  # Replace with your data loading

# Run forecast
forecasts = client.forecast(
    df=df,
    h={{ horizon or 12 }},
    freq='{{ freq or "D" }}',
    {% if level %}level={{ level }},{% endif %}
    {% if add_history %}add_history=True,{% endif %}
)

# forecasts now contains TimeGPT predictions
print(forecasts.head())
"""

    def __init__(self):
        self.template = Template(self.TIMEGPT_TEMPLATE)

    def convert(self, pattern: ForecastingPattern, api_key: str = None) -> str:
        """
        Convert detected pattern to TimeGPT code

        Args:
            pattern: Detected forecasting pattern
            api_key: Optional Nixtla API key

        Returns:
            TimeGPT-ready Python code
        """
        context = {
            'api_key': api_key,
            'horizon': pattern.horizon,
            'freq': pattern.freq,
            'level': [80, 90, 95],  # Default prediction intervals
            'add_history': True,
        }

        timegpt_code = self.template.render(**context)

        # Add migration notes
        notes = self._generate_migration_notes(pattern)

        return f"{timegpt_code}\n\n{notes}"

    def _generate_migration_notes(self, pattern: ForecastingPattern) -> str:
        """Generate migration notes and warnings"""
        notes = [
            "# Migration Notes:",
            "",
            f"# Original library: {pattern.library}",
            f"# Original models: {', '.join(pattern.models)}",
            "",
        ]

        # Model mapping warnings
        if pattern.library == 'statsforecast':
            notes.append("# Note: TimeGPT is a foundation model and doesn't directly map to")
            notes.append("#       specific StatsForecast models like AutoARIMA or AutoETS.")
            notes.append("#       TimeGPT learns patterns from your data automatically.")
            notes.append("")

        if pattern.library == 'mlforecast':
            notes.append("# Note: MLForecast uses ML models (RandomForest, LightGBM, etc.).")
            notes.append("#       TimeGPT is a neural foundation model trained on billions")
            notes.append("#       of time series. No feature engineering needed.")
            notes.append("")

        # Cross-validation note
        if pattern.has_cross_validation:
            notes.append("# Cross-validation detected:")
            notes.append("# Use client.cross_validation() for backtesting:")
            notes.append("#")
            notes.append("# cv_results = client.cross_validation(")
            notes.append("#     df=df,")
            notes.append("#     h=12,")
            notes.append("#     n_windows=5")
            notes.append("# )")
            notes.append("")

        # Data format reminder
        notes.append("# Ensure your DataFrame has columns: unique_id, ds, y")
        notes.append("# - unique_id: Series identifier (can be constant if single series)")
        notes.append("# - ds: Timestamp (datetime)")
        notes.append("# - y: Value (numeric)")

        return '\n'.join(notes)

    def convert_file(self, input_path: str, output_path: str, api_key: str = None):
        """
        Convert entire file from StatsForecast to TimeGPT

        Args:
            input_path: Path to StatsForecast code
            output_path: Path to write TimeGPT code
            api_key: Optional Nixtla API key
        """
        from code_analyzer import CodeAnalyzer

        analyzer = CodeAnalyzer(input_path)
        patterns = analyzer.analyze()

        if not patterns:
            raise ValueError(f"No forecasting patterns detected in {input_path}")

        # Convert first pattern (could support multiple)
        timegpt_code = self.convert(patterns[0], api_key)

        # Write output
        with open(output_path, 'w') as f:
            f.write(timegpt_code)

        return output_path
```

### src/ab_test_runner.py

```python
"""
Run A/B test comparing StatsForecast vs TimeGPT accuracy
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from nixtla import NixtlaClient
from datetime import datetime
from dataclasses import dataclass
import importlib.util
import sys


@dataclass
class ABTestResult:
    """A/B test comparison result"""
    statsforecast_smape: float
    timegpt_smape: float
    statsforecast_mase: float
    timegpt_mase: float
    accuracy_improvement_pct: float
    timegpt_latency_seconds: float
    statsforecast_latency_seconds: float
    cost_per_forecast_usd: float
    winner: str  # 'statsforecast', 'timegpt', or 'tie'


class ABTestRunner:
    """Run A/B test comparing OSS vs TimeGPT"""

    def __init__(self, nixtla_api_key: str):
        self.client = NixtlaClient(api_key=nixtla_api_key)

    def run_test(
        self,
        df: pd.DataFrame,
        horizon: int,
        freq: str,
        statsforecast_model_file: str
    ) -> ABTestResult:
        """
        Run A/B test

        Args:
            df: Historical data (unique_id, ds, y)
            horizon: Forecast horizon
            freq: Frequency string
            statsforecast_model_file: Path to StatsForecast model code

        Returns:
            ABTestResult with accuracy comparison
        """
        # Split data: train vs test
        test_size = horizon
        train_df = df.iloc[:-test_size]
        test_df = df.iloc[-test_size:]

        # Run StatsForecast
        print("Running StatsForecast...")
        sf_start = datetime.now()
        sf_forecasts = self._run_statsforecast(
            train_df,
            horizon,
            freq,
            statsforecast_model_file
        )
        sf_latency = (datetime.now() - sf_start).total_seconds()

        # Run TimeGPT
        print("Running TimeGPT...")
        tg_start = datetime.now()
        tg_forecasts = self.client.forecast(
            df=train_df,
            h=horizon,
            freq=freq
        )
        tg_latency = (datetime.now() - tg_start).total_seconds()

        # Calculate accuracy metrics
        sf_smape = self._calculate_smape(test_df['y'].values, sf_forecasts['value'].values)
        tg_smape = self._calculate_smape(test_df['y'].values, tg_forecasts['TimeGPT'].values)

        sf_mase = self._calculate_mase(test_df['y'].values, sf_forecasts['value'].values, train_df['y'].values)
        tg_mase = self._calculate_mase(test_df['y'].values, tg_forecasts['TimeGPT'].values, train_df['y'].values)

        # Determine winner
        accuracy_improvement = ((sf_smape - tg_smape) / sf_smape) * 100
        winner = 'timegpt' if tg_smape < sf_smape else 'statsforecast'

        # Estimate cost (assuming $0.001 per forecast)
        cost_per_forecast = 0.001

        return ABTestResult(
            statsforecast_smape=sf_smape,
            timegpt_smape=tg_smape,
            statsforecast_mase=sf_mase,
            timegpt_mase=tg_mase,
            accuracy_improvement_pct=accuracy_improvement,
            timegpt_latency_seconds=tg_latency,
            statsforecast_latency_seconds=sf_latency,
            cost_per_forecast_usd=cost_per_forecast,
            winner=winner
        )

    def _run_statsforecast(
        self,
        train_df: pd.DataFrame,
        horizon: int,
        freq: str,
        model_file: str
    ) -> pd.DataFrame:
        """Run StatsForecast model from file"""
        # Dynamically import user's StatsForecast code
        spec = importlib.util.spec_from_file_location("user_model", model_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules["user_model"] = module
        spec.loader.exec_module(module)

        # Assume model is in variable 'sf' or 'model'
        sf = getattr(module, 'sf', None) or getattr(module, 'model', None)

        if not sf:
            raise ValueError(f"No StatsForecast model found in {model_file}")

        # Fit and predict
        sf.fit(train_df)
        forecasts = sf.predict(h=horizon)

        return forecasts

    def _calculate_smape(self, actual: np.ndarray, forecast: np.ndarray) -> float:
        """Calculate Symmetric Mean Absolute Percentage Error"""
        return np.mean(
            2 * np.abs(forecast - actual) / (np.abs(actual) + np.abs(forecast))
        ) * 100

    def _calculate_mase(
        self,
        actual: np.ndarray,
        forecast: np.ndarray,
        train: np.ndarray
    ) -> float:
        """Calculate Mean Absolute Scaled Error"""
        mae = np.mean(np.abs(actual - forecast))
        naive_mae = np.mean(np.abs(np.diff(train)))
        return mae / naive_mae
```

### src/migration_report.py

```python
"""
Generate migration report (PDF/HTML)
"""
from typing import Dict, Any
from jinja2 import Template
from datetime import datetime
from ab_test_runner import ABTestResult
from code_analyzer import ForecastingPattern


class MigrationReport:
    """Generate detailed migration report"""

    HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Nixtla Migration Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #2C3E50; }
        .metric { background: #ECF0F1; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .winner { background: #2ECC71; color: white; padding: 5px 10px; border-radius: 3px; }
        .recommendation { background: #3498DB; color: white; padding: 15px; margin: 20px 0; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #34495E; color: white; }
    </style>
</head>
<body>
    <h1>Nixtla Migration Report</h1>
    <p>Generated: {{ timestamp }}</p>

    <h2>Migration Summary</h2>
    <div class="metric">
        <strong>Source:</strong> {{ pattern.library }}<br>
        <strong>Models:</strong> {{ pattern.models|join(', ') }}<br>
        <strong>Horizon:</strong> {{ pattern.horizon }}<br>
        <strong>Frequency:</strong> {{ pattern.freq }}
    </div>

    <h2>A/B Test Results</h2>
    <table>
        <tr>
            <th>Metric</th>
            <th>StatsForecast</th>
            <th>TimeGPT</th>
            <th>Improvement</th>
        </tr>
        <tr>
            <td>sMAPE</td>
            <td>{{ "%.2f"|format(result.statsforecast_smape) }}%</td>
            <td>{{ "%.2f"|format(result.timegpt_smape) }}%</td>
            <td>{{ "%.1f"|format(result.accuracy_improvement_pct) }}%</td>
        </tr>
        <tr>
            <td>MASE</td>
            <td>{{ "%.3f"|format(result.statsforecast_mase) }}</td>
            <td>{{ "%.3f"|format(result.timegpt_mase) }}</td>
            <td>-</td>
        </tr>
        <tr>
            <td>Latency</td>
            <td>{{ "%.2f"|format(result.statsforecast_latency_seconds) }}s</td>
            <td>{{ "%.2f"|format(result.timegpt_latency_seconds) }}s</td>
            <td>-</td>
        </tr>
    </table>

    <div class="metric">
        <strong>Winner:</strong> <span class="winner">{{ result.winner.upper() }}</span>
    </div>

    <h2>Cost Analysis</h2>
    <div class="metric">
        <strong>TimeGPT Cost:</strong> ${{ "%.4f"|format(result.cost_per_forecast_usd) }} per forecast<br>
        <strong>Monthly Estimate (1,000 forecasts):</strong> ${{ "%.2f"|format(result.cost_per_forecast_usd * 1000) }}
    </div>

    <div class="recommendation">
        <h3>Recommendation</h3>
        {% if result.winner == 'timegpt' %}
        <p>✅ <strong>Migrate to TimeGPT</strong></p>
        <p>TimeGPT showed {{ "%.1f"|format(result.accuracy_improvement_pct) }}% better accuracy.
           At ${{ "%.4f"|format(result.cost_per_forecast_usd) }} per forecast, this is cost-effective
           for most production use cases.</p>
        {% else %}
        <p>⚠️ <strong>Consider Keeping StatsForecast</strong></p>
        <p>StatsForecast performed slightly better in this test. However, consider TimeGPT if:
           - You need to scale to many series
           - You want to eliminate model maintenance
           - You need automatic adaptation to changing patterns</p>
        {% endif %}
    </div>

    <h2>Rollback Plan</h2>
    <div class="metric">
        <p>Your original StatsForecast code has been backed up to:</p>
        <code>{{ backup_path }}</code>
        <p>To rollback, simply restore this file and remove TimeGPT code.</p>
    </div>
</body>
</html>
"""

    def __init__(self):
        self.template = Template(self.HTML_TEMPLATE)

    def generate(
        self,
        pattern: ForecastingPattern,
        result: ABTestResult,
        backup_path: str,
        output_path: str = "migration_report.html"
    ):
        """
        Generate HTML migration report

        Args:
            pattern: Detected forecasting pattern
            result: A/B test result
            backup_path: Path to backup file
            output_path: Output HTML file path
        """
        html = self.template.render(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            pattern=pattern,
            result=result,
            backup_path=backup_path
        )

        with open(output_path, 'w') as f:
            f.write(html)

        return output_path
```

---

## Example Usage

### Slash Command: /nixtla-migrate

```markdown
# /nixtla-migrate

Migrate StatsForecast/MLForecast code to TimeGPT API

## Usage
/nixtla-migrate path/to/forecast_model.py

## Process
1. Analyze existing code
2. Generate TimeGPT equivalent
3. Run A/B test (optional)
4. Create migration report
5. Backup original code
```

**Example Execution**:

```python
User: /nixtla-migrate forecast_sales.py

Claude: Analyzing forecast_sales.py...

        ✅ Detected: StatsForecast
        ✅ Models: AutoARIMA, AutoETS
        ✅ Horizon: 12 months
        ✅ Frequency: Monthly

        Would you like to run an A/B test before migrating? [y/n]

User: y

Claude: Running A/B test...

        StatsForecast: sMAPE = 12.3%
        TimeGPT:       sMAPE = 10.1%

        ✅ TimeGPT is 17.9% more accurate!

        Generated files:
        - forecast_sales_timegpt.py (new TimeGPT code)
        - forecast_sales.backup.py (original backup)
        - migration_report.html (detailed analysis)

        Cost estimate: $0.001 per forecast = $12/month for 12,000 forecasts

        Ready to migrate? [y/n]

User: y

Claude: ✅ Migration complete!

        Next steps:
        1. Review forecast_sales_timegpt.py
        2. Test with: python forecast_sales_timegpt.py
        3. Deploy when ready
        4. Rollback anytime with: /nixtla-rollback forecast_sales.py
```

---

## User Journeys

### Journey 1: Data Scientist Migrates Production Pipeline

**Persona**: Sofia, Senior Data Scientist at RetailCorp
**Goal**: Upgrade StatsForecast to TimeGPT without breaking production
**Context**: Running 50 product forecasts daily, nervous about API migration

**Before**:
```
Sofia: "I want to try TimeGPT but can't risk breaking our production pipeline"
Manager: "How long will migration take?"
Sofia: "Unknown... could be weeks of testing"
```

**After (with Migration Assistant)**:

1. **Analyze Existing Code**
   ```python
   Sofia: /nixtla-migrate production/forecast_pipeline.py

   Claude: Analyzing production/forecast_pipeline.py...

           Pattern detected:
           - Library: StatsForecast
           - Models: AutoARIMA(), AutoETS(), AutoTheta()
           - Horizon: 30 days
           - Frequency: Daily
           - Series: 50 products

           Migration complexity: MEDIUM
   ```

2. **Run A/B Test (Safety First)**
   ```
   Claude: Running parallel A/B test...

           Using last 30 days as holdout set

           StatsForecast Results:
           - sMAPE: 15.2%
           - MASE: 1.34
           - Latency: 12.4s

           TimeGPT Results:
           - sMAPE: 12.8%
           - MASE: 1.12
           - Latency: 3.1s

           ✅ TimeGPT is 15.8% more accurate
           ✅ 4x faster (12.4s → 3.1s)

           Cost: $0.001 × 50 series × 30 days = $1.50/month
   ```

3. **Review Migration Report**
   ```
   Claude: Generated migration_report.html

           Key findings:
           ✅ Accuracy improved: 15.8%
           ✅ Latency reduced: 75%
           ✅ Cost: $1.50/month (negligible)
           ✅ Code simplified: 45 lines → 12 lines

           Recommendation: MIGRATE

           Risk level: LOW
           - Original code backed up
           - Rollback takes 30 seconds
           - A/B test validates accuracy
   ```

4. **Safe Migration**
   ```python
   Sofia: "Looks good, let's migrate"

   Claude: ✅ Migration complete!

           Files created:
           - forecast_pipeline_timegpt.py (new)
           - forecast_pipeline.backup.py (original)

           New code:
           ```python
           from nixtla import NixtlaClient

           client = NixtlaClient(api_key=os.environ['NIXTLA_API_KEY'])
           forecasts = client.forecast(df=df, h=30, freq='D')
           ```

           Test command:
           python forecast_pipeline_timegpt.py --dry-run

           Deploy when ready!
   ```

5. **Monitor Production**
   ```
   Week 1:
   - sMAPE: 12.6% (2.6% better than StatsForecast)
   - Cost: $1.48
   - Zero errors

   Sofia: "Migration was painless. TimeGPT is more accurate and faster."
   ```

**Outcome**: Sofia migrates to TimeGPT in 1 hour (vs estimated weeks), improves accuracy 15.8%, reduces cost to $1.50/month.

---

### Journey 2: ML Engineer Validates Business Case

**Persona**: David, ML Engineer at FinanceCorp
**Goal**: Prove TimeGPT ROI before getting budget approval
**Context**: Currently using MLForecast, management skeptical of API costs

**Steps**:

1. **Quick A/B Test**
   ```bash
   David: /nixtla-ab-test mlforecast_model.py --horizon 90

   Claude: Running A/B test (MLForecast vs TimeGPT)...

           Dataset: 5 years historical, 90-day forecast

           MLForecast (RandomForest):
           - sMAPE: 18.7%
           - Training time: 45 minutes
           - Requires feature engineering

           TimeGPT:
           - sMAPE: 14.2%
           - Inference time: 8 seconds
           - Zero feature engineering

           Accuracy improvement: 24.1%
   ```

2. **Cost-Benefit Analysis**
   ```
   Claude: Generating ROI report...

           Current costs (MLForecast):
           - Data scientist: 20 hours/month maintaining models
           - Compute: $200/month (EC2 + S3)
           - Total: $3,200/month

           TimeGPT costs:
           - API: $0.001 × 30 forecasts × 30 days = $0.90/month
           - Maintenance: $0 (managed service)
           - Total: $0.90/month

           💰 Annual savings: $38,389
           📊 ROI: 42,654%
   ```

3. **Executive Presentation**
   ```
   David: [Shows migration_report.html to CFO]

   CFO: "So we spend $3,200/month now and TimeGPT costs $1/month?"

   David: "Correct. Plus 24% better accuracy."

   CFO: "Approved. Start migration next sprint."
   ```

**Outcome**: David gets budget approval in 1 day using data-driven migration report showing 42,654% ROI.

---

### Journey 3: Team Rollback After Issue

**Persona**: Lisa, DevOps Engineer
**Goal**: Safely rollback TimeGPT migration after detecting data drift
**Context**: Migrated 2 weeks ago, seeing accuracy degradation on new product line

**Steps**:

1. **Detect Issue**
   ```
   Lisa: "TimeGPT accuracy dropped from 12% to 22% sMAPE on new products"
   ```

2. **Instant Rollback**
   ```bash
   Lisa: /nixtla-rollback forecast_pipeline.py

   Claude: Rolling back to StatsForecast...

           ✅ Restored: forecast_pipeline.py (from .backup)
           ✅ Removed: forecast_pipeline_timegpt.py
           ✅ Updated: requirements.txt

           StatsForecast re-enabled.

           Rollback reason: (optional)

   Lisa: "New product line needs custom feature engineering"

   Claude: ✅ Rollback complete!

           Original StatsForecast running.
           TimeGPT migration history saved for future retry.
   ```

3. **Hybrid Approach**
   ```
   Lisa: "Can we use TimeGPT for existing products and StatsForecast for new?"

   Claude: Yes! I can generate a hybrid model that:
           - Routes mature products → TimeGPT (90% of volume)
           - Routes new products → StatsForecast (10% of volume)

           Want me to implement this?

   Lisa: Yes

   Claude: [Generates hybrid router code]
   ```

**Outcome**: Lisa safely rolls back in 30 seconds, then implements hybrid approach getting best of both worlds.

---

## Dependencies

```txt
# requirements.txt
nixtla>=0.7.1
statsforecast>=1.5.0
mlforecast>=0.10.0
pandas>=2.0.0
numpy>=1.24.0
jinja2>=3.1.2
pyyaml>=6.0.1
python-dotenv>=1.0.1
rich>=13.9.4
```

---

## Installation Script

### setup.sh

```bash
#!/usr/bin/env bash
set -e

echo "🚀 Setting up Nixtla Migration Assistant..."

# Check Python version
python3 --version | grep -qE "3\.(1[0-9]|[2-9][0-9])" || {
    echo "❌ Python 3.10+ required"
    exit 1
}

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Validate installation
echo "✅ Testing installation..."
python3 -c "from src.code_analyzer import CodeAnalyzer; print('✅ Code analyzer OK')"
python3 -c "from src.api_converter import APIConverter; print('✅ API converter OK')"
python3 -c "from nixtla import NixtlaClient; print('✅ Nixtla client OK')"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Required environment variables:"
echo "  export NIXTLA_API_KEY=nixak-..."
echo ""
echo "Start migration:"
echo "  /nixtla-migrate path/to/your_forecast_code.py"
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-30
**Language**: Pure Python (no TypeScript)
**Note**: Zero-risk migration with automatic rollback
