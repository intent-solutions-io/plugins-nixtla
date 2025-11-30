# Plugin #9: Nixtla Forecast Explainer
**Technical Architecture & Implementation Specification**

**Created**: 2025-11-30
**Status**: Design Phase
**Priority**: Tier 1 (ENTERPRISE CONVERSION)
**Addresses**: Free Tier Trap (Friction #1) + Enterprise Sales Cycle (Friction #3)

---

## Executive Summary

### What It Is
A post-hoc explainability tool that transforms TimeGPT's "black box" forecasts into transparent, stakeholder-friendly narratives with visual decomposition, SHAP values, confidence bounds, and plain-English explanations.

### Why It Exists
Nixtla's CRO highlights the enterprise blocker:
> "Risk committees and compliance teams reject foundation models as 'black boxes'. We lose enterprise deals because TimeGPT can't explain *why* it predicted X."

**This plugin makes TimeGPT forecasts auditable, defensible, and boardroom-ready.**

### Who It's For
- **Finance teams** needing auditable forecasts for budgets
- **Risk managers** requiring explainability for compliance (SOX, Basel III)
- **Executives** wanting plain-English forecast summaries
- **Data scientists** needing to debug forecast behavior

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  TIMEGPT FORECAST (Black Box)                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  forecasts = client.forecast(df, h=12)                │  │
│  │  # Returns: [1250, 1340, 1420, ...]                  │  │
│  │  # But WHY these numbers?                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  FORECAST EXPLAINER (Glass Box)                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Phase 1: Decomposition                               │  │
│  │  - Trend component                                    │  │
│  │  - Seasonal component                                 │  │
│  │  - Residual component                                 │  │
│  │                                                        │  │
│  │  Phase 2: Feature Attribution (SHAP)                 │  │
│  │  - Historical patterns                                │  │
│  │  - Recent observations                                │  │
│  │  - Exogenous variables (if any)                      │  │
│  │                                                        │  │
│  │  Phase 3: Narrative Generation                       │  │
│  │  - Plain-English summary                             │  │
│  │  - Risk factors identified                            │  │
│  │  - Confidence bounds explained                        │  │
│  │                                                        │  │
│  │  Phase 4: Visual Report                              │  │
│  │  - Interactive charts                                 │  │
│  │  - PDF export (C-suite ready)                        │  │
│  │  - PowerPoint slides                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT (Explained Forecast)                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  "Revenue is predicted to grow 12% in Q4 2025        │  │
│  │   driven by:                                          │  │
│  │   • Strong historical Q4 seasonality (+8%)           │  │
│  │   • Recent upward trend (+4%)                        │  │
│  │   • 90% confidence: $1.2M - $1.5M"                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Plugin Type
**AI Instruction** (Pure Python)

### Components

1. **Slash Commands** (3)
   - `/nixtla-explain` - Generate full explainability report
   - `/nixtla-quick-explain` - Plain-English summary only
   - `/nixtla-decompose` - Visual decomposition chart

2. **Agent Skill** (1)
   - `nixtla-explainer-expert` - Auto-invoked when user asks "why did TimeGPT predict..."

3. **No MCP Server** - Pure Python post-hoc analysis

---

## API Keys & User Requirements

### Required
```bash
# Nixtla API
NIXTLA_API_KEY=nixak-...

# Optional: LLM for narrative generation
OPENAI_API_KEY=sk-...  # OR
ANTHROPIC_API_KEY=sk-ant-...  # OR
GOOGLE_API_KEY=...  # For Gemini
```

### User Requirements

#### Minimum
- **Python 3.10+**
- **Existing TimeGPT forecasts** (or ability to generate them)
- **Historical data** (to explain forecast drivers)

#### Optional
- **LLM API** (for enhanced narrative generation)
- **LaTeX** (for PDF export)
- **PowerPoint** (for slide export)

---

## Code Implementation

### Directory Structure

```
plugins/nixtla-forecast-explainer/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── nixtla-explain.md
│   ├── nixtla-quick-explain.md
│   └── nixtla-decompose.md
├── skills/
│   └── SKILL.md
├── src/
│   ├── __init__.py
│   ├── explainer.py              # Core explainability engine
│   ├── decomposer.py             # Time series decomposition
│   ├── shap_analyzer.py          # SHAP attribution (future)
│   ├── narrative_generator.py    # LLM-powered narratives
│   ├── visualizer.py             # Chart generation
│   └── report_builder.py         # PDF/PowerPoint export
├── templates/
│   ├── report_template.html
│   ├── slides_template.pptx
│   └── narrative_prompt.txt
├── examples/
│   ├── sample_forecast.py
│   └── sample_explanation.html
├── requirements.txt
└── setup.sh
```

---

## Core Implementation

### src/explainer.py

```python
"""
Core explainability engine for TimeGPT forecasts
"""
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from nixtla import NixtlaClient
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ForecastExplanation:
    """Comprehensive forecast explanation"""
    forecast_values: np.ndarray
    historical_data: pd.DataFrame
    trend_component: np.ndarray
    seasonal_component: np.ndarray
    residual_component: np.ndarray
    confidence_lower: np.ndarray
    confidence_upper: np.ndarray
    key_drivers: List[Dict[str, Any]]
    narrative: str
    risk_factors: List[str]
    horizon: int
    freq: str


class ForecastExplainer:
    """Explain TimeGPT forecasts with decomposition and narratives"""

    def __init__(self, nixtla_api_key: str, llm_api_key: Optional[str] = None):
        self.client = NixtlaClient(api_key=nixtla_api_key)
        self.llm_api_key = llm_api_key

    def explain(
        self,
        df: pd.DataFrame,
        horizon: int,
        freq: str = 'D',
        level: List[int] = [80, 90, 95]
    ) -> ForecastExplanation:
        """
        Generate comprehensive forecast explanation

        Args:
            df: Historical data (unique_id, ds, y)
            horizon: Forecast horizon
            freq: Frequency string
            level: Prediction interval levels

        Returns:
            ForecastExplanation with decomposition and narrative
        """
        # Step 1: Generate TimeGPT forecast
        forecasts = self.client.forecast(
            df=df,
            h=horizon,
            freq=freq,
            level=level
        )

        # Step 2: Decompose time series
        from decomposer import TimeSeriesDecomposer
        decomposer = TimeSeriesDecomposer()
        decomposition = decomposer.decompose(df['y'].values, freq)

        # Step 3: Identify key drivers
        key_drivers = self._identify_drivers(
            df,
            forecasts,
            decomposition
        )

        # Step 4: Analyze risk factors
        risk_factors = self._identify_risk_factors(
            df,
            forecasts,
            decomposition
        )

        # Step 5: Generate narrative
        narrative = self._generate_narrative(
            df,
            forecasts,
            key_drivers,
            risk_factors
        )

        return ForecastExplanation(
            forecast_values=forecasts['TimeGPT'].values,
            historical_data=df,
            trend_component=decomposition['trend'],
            seasonal_component=decomposition['seasonal'],
            residual_component=decomposition['residual'],
            confidence_lower=forecasts[f'TimeGPT-lo-{level[-1]}'].values,
            confidence_upper=forecasts[f'TimeGPT-hi-{level[-1]}'].values,
            key_drivers=key_drivers,
            narrative=narrative,
            risk_factors=risk_factors,
            horizon=horizon,
            freq=freq
        )

    def _identify_drivers(
        self,
        df: pd.DataFrame,
        forecasts: pd.DataFrame,
        decomposition: Dict[str, np.ndarray]
    ) -> List[Dict[str, Any]]:
        """
        Identify key forecast drivers

        Returns:
            List of drivers with attribution scores
        """
        drivers = []

        # Trend contribution
        trend_change = (decomposition['trend'][-1] - decomposition['trend'][0]) / decomposition['trend'][0] * 100
        if abs(trend_change) > 5:
            drivers.append({
                'name': 'Historical Trend',
                'contribution_pct': trend_change,
                'description': f"{'Upward' if trend_change > 0 else 'Downward'} trend over historical period"
            })

        # Seasonality contribution
        seasonal_strength = np.std(decomposition['seasonal']) / np.std(df['y'].values) * 100
        if seasonal_strength > 10:
            drivers.append({
                'name': 'Seasonal Pattern',
                'contribution_pct': seasonal_strength,
                'description': 'Strong recurring seasonal pattern detected'
            })

        # Recent momentum
        recent_values = df['y'].values[-10:]
        recent_mean = np.mean(recent_values)
        overall_mean = np.mean(df['y'].values)
        momentum_pct = (recent_mean - overall_mean) / overall_mean * 100

        if abs(momentum_pct) > 5:
            drivers.append({
                'name': 'Recent Momentum',
                'contribution_pct': momentum_pct,
                'description': f"Recent values {'above' if momentum_pct > 0 else 'below'} historical average"
            })

        return sorted(drivers, key=lambda x: abs(x['contribution_pct']), reverse=True)

    def _identify_risk_factors(
        self,
        df: pd.DataFrame,
        forecasts: pd.DataFrame,
        decomposition: Dict[str, np.ndarray]
    ) -> List[str]:
        """
        Identify forecast risk factors

        Returns:
            List of risk factors
        """
        risks = []

        # High uncertainty
        confidence_width = forecasts.iloc[0][f'TimeGPT-hi-95'] - forecasts.iloc[0][f'TimeGPT-lo-95']
        forecast_value = forecasts.iloc[0]['TimeGPT']
        uncertainty_pct = (confidence_width / forecast_value) * 100

        if uncertainty_pct > 30:
            risks.append(f"High forecast uncertainty ({uncertainty_pct:.1f}% confidence interval width)")

        # Volatile historical data
        cv = np.std(df['y'].values) / np.mean(df['y'].values) * 100
        if cv > 20:
            risks.append(f"High historical volatility (CV={cv:.1f}%)")

        # Recent data gaps
        df_sorted = df.sort_values('ds')
        time_diffs = df_sorted['ds'].diff().dt.total_seconds()
        expected_diff = pd.Timedelta(self._freq_to_timedelta(forecasts.attrs.get('freq', 'D'))).total_seconds()
        gaps = (time_diffs > expected_diff * 2).sum()

        if gaps > 0:
            risks.append(f"Data quality: {gaps} gaps detected in historical data")

        # Extrapolation beyond historical range
        historical_max = df['y'].max()
        forecast_max = forecasts['TimeGPT'].max()
        if forecast_max > historical_max * 1.2:
            risks.append(f"Forecast extrapolates 20%+ beyond historical range")

        return risks

    def _generate_narrative(
        self,
        df: pd.DataFrame,
        forecasts: pd.DataFrame,
        key_drivers: List[Dict[str, Any]],
        risk_factors: List[str]
    ) -> str:
        """
        Generate plain-English narrative explaining forecast

        Returns:
            Human-readable forecast explanation
        """
        # Calculate key stats
        forecast_value = forecasts['TimeGPT'].iloc[0]
        historical_mean = df['y'].mean()
        change_pct = (forecast_value - historical_mean) / historical_mean * 100

        # Build narrative
        narrative_parts = []

        # Opening statement
        direction = "increase" if change_pct > 0 else "decrease"
        narrative_parts.append(
            f"The forecast predicts a {abs(change_pct):.1f}% {direction} "
            f"to {forecast_value:.2f} in the next period."
        )

        # Key drivers
        if key_drivers:
            narrative_parts.append("\n\nKey drivers:")
            for driver in key_drivers[:3]:  # Top 3
                narrative_parts.append(
                    f"• {driver['name']}: {driver['description']} "
                    f"({driver['contribution_pct']:+.1f}%)"
                )

        # Confidence bounds
        conf_lower = forecasts[f'TimeGPT-lo-95'].iloc[0]
        conf_upper = forecasts[f'TimeGPT-hi-95'].iloc[0]
        narrative_parts.append(
            f"\n\nWith 95% confidence, the forecast range is "
            f"{conf_lower:.2f} to {conf_upper:.2f}."
        )

        # Risk factors
        if risk_factors:
            narrative_parts.append("\n\nRisk factors to consider:")
            for risk in risk_factors:
                narrative_parts.append(f"• {risk}")

        return ''.join(narrative_parts)

    def _freq_to_timedelta(self, freq: str) -> str:
        """Convert frequency string to timedelta"""
        freq_map = {
            'D': '1D',
            'W': '1W',
            'M': '30D',
            'Q': '90D',
            'Y': '365D',
            'H': '1H',
        }
        return freq_map.get(freq, '1D')
```

### src/decomposer.py

```python
"""
Time series decomposition (trend + seasonal + residual)
"""
import numpy as np
from typing import Dict
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd


class TimeSeriesDecomposer:
    """Decompose time series into components"""

    def decompose(
        self,
        values: np.ndarray,
        freq: str,
        model: str = 'additive'
    ) -> Dict[str, np.ndarray]:
        """
        Decompose time series

        Args:
            values: Time series values
            freq: Frequency string ('D', 'W', 'M', etc.)
            model: 'additive' or 'multiplicative'

        Returns:
            Dictionary with trend, seasonal, residual components
        """
        # Convert freq to period
        period_map = {
            'D': 7,      # Weekly seasonality
            'W': 52,     # Annual seasonality
            'M': 12,     # Annual seasonality
            'Q': 4,      # Annual seasonality
            'H': 24,     # Daily seasonality
        }
        period = period_map.get(freq, 7)

        # Handle short series
        if len(values) < period * 2:
            period = max(2, len(values) // 2)

        # Decompose
        decomposition = seasonal_decompose(
            values,
            model=model,
            period=period,
            extrapolate_trend='freq'
        )

        return {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid,
            'original': values
        }
```

### src/narrative_generator.py

```python
"""
LLM-powered narrative generation for forecasts
"""
from typing import Optional, List, Dict, Any
import os
from jinja2 import Template


class NarrativeGenerator:
    """Generate plain-English forecast narratives using LLMs"""

    PROMPT_TEMPLATE = """
You are a financial analyst explaining a time series forecast to executives.

Context:
- Forecast value: {{ forecast_value }}
- Historical average: {{ historical_average }}
- Change: {{ change_pct }}%
- Horizon: {{ horizon }} {{ freq }}

Key Drivers:
{% for driver in key_drivers %}
- {{ driver.name }}: {{ driver.description }} ({{ driver.contribution_pct }}%)
{% endfor %}

Risk Factors:
{% for risk in risk_factors %}
- {{ risk }}
{% endfor %}

Write a concise 3-paragraph executive summary:
1. What is forecasted
2. Why (key drivers)
3. Risks and confidence

Use plain English, avoid jargon.
"""

    def __init__(self, llm_provider: str = 'openai', api_key: Optional[str] = None):
        self.llm_provider = llm_provider
        self.api_key = api_key or self._get_api_key(llm_provider)
        self.template = Template(self.PROMPT_TEMPLATE)

    def _get_api_key(self, provider: str) -> str:
        """Get API key from environment"""
        env_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'google': 'GOOGLE_API_KEY',
        }
        return os.environ.get(env_map.get(provider, 'OPENAI_API_KEY'), '')

    def generate(
        self,
        forecast_value: float,
        historical_average: float,
        change_pct: float,
        horizon: int,
        freq: str,
        key_drivers: List[Dict[str, Any]],
        risk_factors: List[str]
    ) -> str:
        """
        Generate LLM-powered narrative

        Returns:
            Executive-ready forecast narrative
        """
        if not self.api_key:
            # Fallback: Template-based narrative
            return self._generate_template_narrative(
                forecast_value,
                historical_average,
                change_pct,
                horizon,
                freq,
                key_drivers,
                risk_factors
            )

        # LLM-powered narrative
        prompt = self.template.render(
            forecast_value=forecast_value,
            historical_average=historical_average,
            change_pct=change_pct,
            horizon=horizon,
            freq=freq,
            key_drivers=key_drivers,
            risk_factors=risk_factors
        )

        if self.llm_provider == 'openai':
            return self._call_openai(prompt)
        elif self.llm_provider == 'anthropic':
            return self._call_anthropic(prompt)
        elif self.llm_provider == 'google':
            return self._call_google(prompt)
        else:
            return self._generate_template_narrative(
                forecast_value,
                historical_average,
                change_pct,
                horizon,
                freq,
                key_drivers,
                risk_factors
            )

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        import openai
        openai.api_key = self.api_key

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        return response.choices[0].message.content

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API"""
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text

    def _call_google(self, prompt: str) -> str:
        """Call Google Gemini API"""
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        return response.text

    def _generate_template_narrative(
        self,
        forecast_value: float,
        historical_average: float,
        change_pct: float,
        horizon: int,
        freq: str,
        key_drivers: List[Dict[str, Any]],
        risk_factors: List[str]
    ) -> str:
        """Fallback: Template-based narrative"""
        direction = "increase" if change_pct > 0 else "decrease"

        narrative = f"""
Forecast Summary:

The model predicts a {abs(change_pct):.1f}% {direction} to {forecast_value:.2f} over the next {horizon} {freq}.

Key Drivers:
{chr(10).join(f"• {d['name']}: {d['description']}" for d in key_drivers[:3])}

Risk Factors:
{chr(10).join(f"• {r}" for r in risk_factors)}

This forecast is based on historical patterns and should be reviewed regularly as new data becomes available.
"""
        return narrative.strip()
```

### src/visualizer.py

```python
"""
Generate visual charts for forecast explanations
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Optional
from explainer import ForecastExplanation


class ForecastVisualizer:
    """Create visual explanations of forecasts"""

    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')

    def plot_decomposition(
        self,
        explanation: ForecastExplanation,
        output_path: Optional[str] = None
    ):
        """
        Plot time series decomposition

        Args:
            explanation: ForecastExplanation object
            output_path: Optional path to save figure
        """
        fig, axes = plt.subplots(4, 1, figsize=(12, 10))

        # Original series + forecast
        axes[0].plot(explanation.historical_data['ds'], explanation.historical_data['y'], label='Historical', color='blue')
        forecast_dates = pd.date_range(
            start=explanation.historical_data['ds'].iloc[-1],
            periods=explanation.horizon + 1,
            freq=explanation.freq
        )[1:]
        axes[0].plot(forecast_dates, explanation.forecast_values, label='Forecast', color='red', linestyle='--')
        axes[0].fill_between(
            forecast_dates,
            explanation.confidence_lower,
            explanation.confidence_upper,
            alpha=0.2,
            color='red'
        )
        axes[0].set_title('Forecast with 95% Confidence Interval')
        axes[0].legend()
        axes[0].set_ylabel('Value')

        # Trend
        axes[1].plot(explanation.historical_data['ds'], explanation.trend_component, color='green')
        axes[1].set_title('Trend Component')
        axes[1].set_ylabel('Trend')

        # Seasonal
        axes[2].plot(explanation.historical_data['ds'], explanation.seasonal_component, color='orange')
        axes[2].set_title('Seasonal Component')
        axes[2].set_ylabel('Seasonal')

        # Residual
        axes[3].plot(explanation.historical_data['ds'], explanation.residual_component, color='purple')
        axes[3].set_title('Residual Component')
        axes[3].set_ylabel('Residual')
        axes[3].set_xlabel('Date')

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

    def plot_drivers(
        self,
        explanation: ForecastExplanation,
        output_path: Optional[str] = None
    ):
        """
        Plot key forecast drivers as bar chart

        Args:
            explanation: ForecastExplanation object
            output_path: Optional path to save figure
        """
        drivers = explanation.key_drivers

        if not drivers:
            print("No drivers to plot")
            return

        names = [d['name'] for d in drivers]
        contributions = [d['contribution_pct'] for d in drivers]

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['green' if c > 0 else 'red' for c in contributions]
        ax.barh(names, contributions, color=colors)
        ax.set_xlabel('Contribution (%)')
        ax.set_title('Forecast Drivers')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
```

### src/report_builder.py

```python
"""
Build comprehensive PDF/HTML/PowerPoint reports
"""
from typing import Optional
from jinja2 import Template
from explainer import ForecastExplanation
from visualizer import ForecastVisualizer
import base64
from io import BytesIO


class ReportBuilder:
    """Build exportable forecast explanation reports"""

    HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Forecast Explanation Report</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2C3E50; border-bottom: 3px solid #3498DB; padding-bottom: 10px; }
        h2 { color: #34495E; margin-top: 30px; }
        .metric { background: #ECF0F1; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 5px solid #3498DB; }
        .drivers { background: #E8F6F3; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .risk { background: #FADBD8; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 5px solid #E74C3C; }
        .narrative { background: #FEF9E7; padding: 20px; margin: 20px 0; border-radius: 8px; font-size: 1.1em; line-height: 1.6; }
        img { max-width: 100%; height: auto; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7F8C8D; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Forecast Explanation Report</h1>
        <p><strong>Generated:</strong> {{ timestamp }}</p>

        <h2>Executive Summary</h2>
        <div class="narrative">
            {{ narrative }}
        </div>

        <h2>Forecast Details</h2>
        <div class="metric">
            <strong>Forecast Value:</strong> {{ forecast_value }}<br>
            <strong>95% Confidence Interval:</strong> {{ confidence_lower }} - {{ confidence_upper }}<br>
            <strong>Horizon:</strong> {{ horizon }} {{ freq }}<br>
            <strong>Historical Average:</strong> {{ historical_average }}
        </div>

        <h2>Key Drivers</h2>
        {% for driver in key_drivers %}
        <div class="drivers">
            <strong>{{ driver.name }}</strong> ({{ driver.contribution_pct }}%)<br>
            {{ driver.description }}
        </div>
        {% endfor %}

        <h2>Risk Factors</h2>
        {% for risk in risk_factors %}
        <div class="risk">⚠️ {{ risk }}</div>
        {% endfor %}

        <h2>Visual Analysis</h2>
        <img src="data:image/png;base64,{{ decomposition_chart }}" alt="Decomposition">
        <img src="data:image/png;base64,{{ drivers_chart }}" alt="Drivers">

        <div class="footer">
            <p>This report was generated by Nixtla Forecast Explainer.</p>
            <p>Forecast method: TimeGPT Foundation Model</p>
        </div>
    </div>
</body>
</html>
"""

    def __init__(self):
        self.template = Template(self.HTML_TEMPLATE)
        self.visualizer = ForecastVisualizer()

    def build_html_report(
        self,
        explanation: ForecastExplanation,
        output_path: str = "forecast_explanation.html"
    ) -> str:
        """
        Build HTML report

        Args:
            explanation: ForecastExplanation object
            output_path: Path to save HTML file

        Returns:
            Path to generated HTML file
        """
        # Generate charts as base64
        decomposition_chart = self._chart_to_base64(
            lambda: self.visualizer.plot_decomposition(explanation)
        )
        drivers_chart = self._chart_to_base64(
            lambda: self.visualizer.plot_drivers(explanation)
        )

        # Render HTML
        html = self.template.render(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            narrative=explanation.narrative,
            forecast_value=f"{explanation.forecast_values[0]:.2f}",
            confidence_lower=f"{explanation.confidence_lower[0]:.2f}",
            confidence_upper=f"{explanation.confidence_upper[0]:.2f}",
            horizon=explanation.horizon,
            freq=explanation.freq,
            historical_average=f"{explanation.historical_data['y'].mean():.2f}",
            key_drivers=explanation.key_drivers,
            risk_factors=explanation.risk_factors,
            decomposition_chart=decomposition_chart,
            drivers_chart=drivers_chart
        )

        # Write to file
        with open(output_path, 'w') as f:
            f.write(html)

        return output_path

    def _chart_to_base64(self, plot_function) -> str:
        """Convert matplotlib chart to base64 string"""
        buffer = BytesIO()
        plot_function()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        plt.close()
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode()


from datetime import datetime
```

---

## Example Usage

### Slash Command: /nixtla-explain

```markdown
# /nixtla-explain

Generate comprehensive explainability report for TimeGPT forecast

## Usage
/nixtla-explain path/to/data.csv --horizon 12 --output report.html

## Output
- HTML report with visual decomposition
- Plain-English narrative
- PDF export (optional)
- PowerPoint slides (optional)
```

**Example Execution**:

```python
User: /nixtla-explain sales_data.csv --horizon 30

Claude: Analyzing forecast for sales_data.csv...

        ✅ Data loaded: 730 days of history
        ✅ TimeGPT forecast generated (30 days)
        ✅ Decomposition complete
        ✅ Drivers identified: 3
        ✅ Risk factors detected: 2

        Generating explanation report...

        Report generated: forecast_explanation.html

        Executive Summary:
        "Sales are forecasted to increase 12.4% to $1.35M in the next 30 days,
         driven by strong seasonal patterns (+8.2%) and recent upward momentum
         (+4.1%). With 95% confidence, the forecast range is $1.21M - $1.48M.

         Risk factors: High uncertainty (±20%), recent data gap detected."

        Key Drivers:
        1. Seasonal Pattern: +8.2% (Strong Q4 seasonality)
        2. Recent Momentum: +4.1% (Last 10 days above average)
        3. Historical Trend: +2.3% (Gradual long-term growth)

        View report: firefox forecast_explanation.html
```

---

## User Journeys

### Journey 1: CFO Needs Budget Justification

**Persona**: Maria, CFO at ManufacturingCorp
**Goal**: Justify Q4 budget increase to Board of Directors
**Context**: Needs auditable, defensible forecast with plain-English explanation

**Before**:
```
Maria: "Why does TimeGPT predict 15% revenue growth?"
Data Science: "It's a neural network, we can't explain individual predictions"
Board: "We can't approve $2M budget based on a 'black box'"
```

**After (with Forecast Explainer)**:

1. **Generate Explainability Report**
   ```bash
   Maria: /nixtla-explain revenue_history.csv --horizon 90 --output q4_forecast.html

   Claude: Generating comprehensive explanation...

           ✅ Forecast: $2.15M (Q4 2025)
           ✅ Confidence: $1.98M - $2.31M (95%)
           ✅ Drivers identified: 3
           ✅ HTML report generated
           ✅ PowerPoint slides exported
   ```

2. **Review Plain-English Summary**
   ```
   Executive Summary:

   "Q4 revenue is forecasted at $2.15M, representing a 15.2% increase
    over Q3 2025. This growth is driven by three key factors:

    1. Seasonal Q4 Pattern (+8.7%): Historical data shows consistent
       Q4 revenue increases averaging 8-10% over the past 5 years,
       driven by holiday purchasing.

    2. Recent Momentum (+4.2%): The last 30 days show accelerating
       growth 4.2% above the 90-day average, indicating strong
       near-term demand.

    3. Product Mix Shift (+2.3%): Higher-margin products now represent
       35% of sales vs 28% last year, contributing to revenue growth.

    With 95% confidence, Q4 revenue will fall between $1.98M and $2.31M.

    Risk Factors:
    • Supply chain delays could reduce fulfillment capacity by 5-10%
    • Q4 2024 was unusually strong, creating tough comparisons
    • Forecast extends 12% beyond historical maximum"
   ```

3. **Present to Board**
   ```
   [Maria opens forecast_explanation.html in boardroom]

   Board Member: "Why 15% growth? That's aggressive."

   Maria: [Shows decomposition chart]
         "Three clear drivers: Historical Q4 seasonality has been 8-10%
          for 5 years. Recent momentum adds another 4%. Product mix
          shift adds 2%. Total: 14-16%."

   Board Member: "What's the downside risk?"

   Maria: [Shows confidence interval]
         "95% confidence interval is $1.98M - $2.31M. Worst case is
          still 6% growth. Risk factors are supply chain and tough
          comps from last year."

   Board: "This is well-documented. Budget approved."
   ```

**Outcome**: Maria gets $2M budget approved using auditable, transparent forecast explanation with visual evidence.

---

### Journey 2: Risk Manager Validates Model for Compliance

**Persona**: James, Risk Manager at FinanceCorp
**Goal**: Validate TimeGPT for Basel III compliance (model risk management)
**Context**: Regulators require explainable models for capital forecasting

**Steps**:

1. **Regulatory Requirements**
   ```
   Regulator: "Your capital forecast model must be explainable for SR 11-7
               (Model Risk Management). Can you explain TimeGPT predictions?"

   James: "Let me generate explainability documentation."
   ```

2. **Generate Model Documentation**
   ```bash
   James: /nixtla-explain capital_forecast.csv --horizon 12 --compliance-mode

   Claude: Generating compliance-ready explanation...

           Model: TimeGPT Foundation Model (Nixtla)
           Training: 100B+ time series (pre-trained)
           Input: 5 years monthly capital data
           Output: 12-month capital forecast

           Decomposition:
           - Trend component: 42% of variance
           - Seasonal component: 31% of variance
           - Residual: 27% of variance

           Attribution:
           - Historical pattern: 68% of forecast
           - Recent observations: 24% of forecast
           - Extrapolation: 8% of forecast

           Validation:
           - Backtesting: 12-month rolling windows
           - sMAPE: 8.3% (vs 12.1% previous model)
           - Coverage: 94.2% (within 95% CI)

           Compliance documentation exported: model_validation_report.pdf
   ```

3. **Regulatory Review**
   ```
   James: [Submits model_validation_report.pdf to regulator]

   Regulator: "This is comprehensive. We can audit:
               - Model decomposition showing trend/seasonal/residual
               - Attribution showing 68% historical, 24% recent, 8% extrapolation
               - Backtesting showing 8.3% sMAPE
               - Confidence intervals with 94% coverage

               Model approved for capital forecasting."
   ```

**Outcome**: James passes regulatory audit with explainability documentation, allowing TimeGPT use for capital forecasting.

---

### Journey 3: Data Scientist Debugs Forecast Anomaly

**Persona**: Lisa, Data Scientist at E-CommerceCorp
**Goal**: Understand why TimeGPT predicted sudden 30% spike
**Context**: Forecast seems unrealistic, need to debug

**Steps**:

1. **Identify Anomaly**
   ```python
   Lisa: "TimeGPT predicts 30% spike next week. That seems wrong."
   ```

2. **Generate Decomposition**
   ```bash
   Lisa: /nixtla-decompose recent_sales.csv --highlight-anomaly

   Claude: Decomposing forecast...

           🚨 Anomaly detected in forecast

           Forecast: +30.2% spike on 2025-12-15

           Decomposition shows:
           - Trend: +2.1% (normal)
           - Seasonal: +28.4% (ANOMALY!)
           - Residual: -0.3% (normal)

           Root cause: Strong seasonal pattern on 2025-12-15

           Historical context:
           - 2024-12-15: +29.1%
           - 2023-12-15: +31.5%
           - 2022-12-15: +27.8%

           Explanation: December 15th has historically been peak
                        shopping day (last shipping date for Christmas).

           Forecast is VALID, not anomalous.
   ```

3. **Validate Pattern**
   ```
   Lisa: "Ah! December 15th is the last guaranteed Christmas delivery.
          Historical data confirms this. The 30% spike is real."

   Manager: "Good catch. We should increase warehouse capacity for Dec 15."
   ```

**Outcome**: Lisa validates forecast is correct using decomposition, leads to better capacity planning.

---

## Dependencies

```txt
# requirements.txt
nixtla>=0.7.1
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
statsmodels>=0.14.0
jinja2>=3.1.2
python-dotenv>=1.0.1

# Optional: LLM providers
openai>=1.0.0
anthropic>=0.18.0
google-generativeai>=0.3.0

# Optional: PDF export
reportlab>=4.0.0

# Optional: PowerPoint export
python-pptx>=0.6.21
```

---

## Installation Script

### setup.sh

```bash
#!/usr/bin/env bash
set -e

echo "🚀 Setting up Nixtla Forecast Explainer..."

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

# Install optional dependencies
read -p "Install LLM support for enhanced narratives? (OpenAI/Anthropic/Google) [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing LLM dependencies..."
    pip install openai anthropic google-generativeai
fi

# Validate installation
echo "✅ Testing installation..."
python3 -c "from src.explainer import ForecastExplainer; print('✅ Explainer OK')"
python3 -c "from src.visualizer import ForecastVisualizer; print('✅ Visualizer OK')"
python3 -c "from nixtla import NixtlaClient; print('✅ Nixtla client OK')"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Required environment variables:"
echo "  export NIXTLA_API_KEY=nixak-..."
echo ""
echo "Optional (for enhanced narratives):"
echo "  export OPENAI_API_KEY=sk-... OR"
echo "  export ANTHROPIC_API_KEY=sk-ant-... OR"
echo "  export GOOGLE_API_KEY=..."
echo ""
echo "Generate explanation:"
echo "  /nixtla-explain data.csv --horizon 30"
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-30
**Language**: Pure Python (no TypeScript)
**Note**: Makes TimeGPT forecasts boardroom-ready and compliance-friendly
