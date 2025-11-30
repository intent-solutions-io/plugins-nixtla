# Plugin #3: Nixtla ROI Calculator
**Technical Architecture & Implementation Specification**

**Created**: 2025-11-30
**Status**: Design Phase
**Priority**: Tier 1 (IMMEDIATE VALUE)
**Addresses**: Enterprise Sales Cycle (Friction #3)

---

## Executive Summary

### What It Is
An interactive ROI calculator that compares total cost of ownership (TCO) for internal forecasting builds vs Nixtla TimeGPT API, generating executive-ready business cases for procurement approval.

### Why It Exists
Nixtla's CRO faces this objection:
> "Why should I pay you $50k/year when I have five data scientists costing me $1.5M/year? I need them to do this work."

**This plugin shifts the conversation from "Model Accuracy" to "Total Cost of Ownership"** with hard financial justification.

### Who It's For
- **VPs of Engineering** justifying TimeGPT to finance teams
- **Procurement teams** requiring TCO analysis
- **Nixtla sales team** closing enterprise deals
- **FinOps leaders** optimizing AI/ML spending

---

## Architecture Overview

### Component Stack

```
┌─────────────────────────────────────────────────────────────┐
│  USER INTERFACE                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │Slash Command │  │ Agent Skill  │  │  Interactive    │  │
│  │ /roi-calc    │  │(Auto-invoke) │  │  Wizard         │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  ROI CALCULATION ENGINE (Python)                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  TCO Components:                                      │  │
│  │  ├─ Internal Build Cost (salaries, compute, ops)    │  │
│  │  ├─ Nixtla API Cost (subscription, usage)           │  │
│  │  ├─ Opportunity Cost (time-to-market delay)         │  │
│  │  ├─ Hidden Costs (maintenance, turnover, updates)   │  │
│  │  └─ Risk-Adjusted NPV                               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT FORMATS                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │ PDF Report  │  │ PowerPoint  │  │  Excel Model     │   │
│  │(Executive)  │  │ (Slides)    │  │  (Interactive)   │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Plugin Type
**AI Instruction** (Pure Python, no MCP server)

### Components

1. **Slash Commands** (2)
   - `/nixtla-roi` - Full interactive ROI calculation
   - `/nixtla-quick-roi` - Fast ROI estimate with defaults

2. **Agent Skill** (1)
   - `nixtla-roi-expert` - Auto-invokes on "justify TimeGPT cost" discussions

3. **No MCP Server** - Pure Python CLI tool

---

## API Keys & User Requirements

### No API Keys Required
This plugin operates independently - no Nixtla API access needed.

### User Requirements

#### Minimum (Interactive Wizard Prompts For)
- **Team size** - Number of data scientists on forecasting
- **Series count** - How many time series forecasted
- **Forecast frequency** - How often forecasts run

#### Optional Context (Improves Accuracy)
- **Current salaries** - DS team compensation
- **Cloud costs** - Current compute spend
- **Revenue impact** - How much revenue depends on forecasts
- **Time-to-market** - How long to build in-house

---

## Installation Process

### setup.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Setting up Nixtla ROI Calculator..."

# Check Python
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# No database needed - calculations are stateless

# Optional: Install pandoc for PDF generation
if command -v pandoc &> /dev/null; then
    echo "✅ pandoc found (PDF export enabled)"
else
    echo "⚠️  pandoc not found (PDF export disabled)"
    echo "   Install: sudo apt install pandoc texlive-xetex"
fi

echo "✅ Setup complete!"
echo "Run: /nixtla-roi to calculate ROI"
```

---

## Technical Schemas

### ROI Calculation Model

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class InternalBuildCost:
    """TCO for building in-house forecasting system"""
    data_scientists: int
    avg_salary_usd: float
    salary_overhead_pct: float = 0.3  # Benefits, taxes
    compute_monthly_usd: float = 0.0
    mlops_infrastructure_monthly_usd: float = 0.0
    maintenance_hours_monthly: int = 0
    recruiting_cost_usd: float = 0.0
    training_cost_usd: float = 0.0

    @property
    def annual_cost_usd(self) -> float:
        # Salaries + overhead
        total_salaries = (
            self.data_scientists *
            self.avg_salary_usd *
            (1 + self.salary_overhead_pct)
        )

        # Monthly recurring costs
        monthly_costs = (
            self.compute_monthly_usd +
            self.mlops_infrastructure_monthly_usd +
            (self.maintenance_hours_monthly * 150)  # $150/hr contractor rate
        )

        # One-time costs (amortized over 3 years)
        one_time_costs = (
            self.recruiting_cost_usd +
            self.training_cost_usd
        ) / 3

        return total_salaries + (monthly_costs * 12) + one_time_costs


@dataclass
class NixtlaAPICost:
    """TCO for using Nixtla TimeGPT API"""
    series_count: int
    forecasts_per_series_monthly: int
    cost_per_forecast_usd: float = 0.001
    monthly_subscription_usd: float = 0.0

    @property
    def annual_cost_usd(self) -> float:
        monthly_api_cost = (
            self.series_count *
            self.forecasts_per_series_monthly *
            self.cost_per_forecast_usd
        )

        return (monthly_api_cost + self.monthly_subscription_usd) * 12


@dataclass
class OpportunityCost:
    """Value of faster time-to-market"""
    monthly_revenue_usd: float
    forecast_driven_revenue_pct: float
    internal_build_time_months: int = 9
    nixtla_deployment_time_weeks: int = 2

    @property
    def time_saved_months(self) -> float:
        return self.internal_build_time_months - (self.nixtla_deployment_time_weeks / 4)

    @property
    def opportunity_value_usd(self) -> float:
        monthly_value = (
            self.monthly_revenue_usd *
            self.forecast_driven_revenue_pct
        )
        return monthly_value * self.time_saved_months


@dataclass
class ROIAnalysis:
    """Complete ROI analysis output"""
    internal_build: InternalBuildCost
    nixtla_api: NixtlaAPICost
    opportunity: OpportunityCost

    @property
    def annual_savings_usd(self) -> float:
        return self.internal_build.annual_cost_usd - self.nixtla_api.annual_cost_usd

    @property
    def roi_percentage(self) -> float:
        investment = self.nixtla_api.annual_cost_usd
        return (self.annual_savings_usd / investment) * 100 if investment > 0 else 0

    @property
    def payback_period_months(self) -> float:
        monthly_savings = self.annual_savings_usd / 12
        return self.nixtla_api.annual_cost_usd / monthly_savings if monthly_savings > 0 else float('inf')

    @property
    def net_present_value_3yr_usd(self) -> float:
        """NPV over 3 years at 10% discount rate"""
        discount_rate = 0.10
        npv = 0
        for year in range(1, 4):
            cash_flow = self.annual_savings_usd
            npv += cash_flow / ((1 + discount_rate) ** year)
        return npv - self.nixtla_api.annual_cost_usd
```

---

## Code Implementation

### Core: roi_calculator.py

```python
"""
Interactive ROI calculator for Nixtla TimeGPT
"""
from typing import Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm

from .models import InternalBuildCost, NixtlaAPICost, OpportunityCost, ROIAnalysis
from .report_generator import ReportGenerator


console = Console()


class InteractiveROICalculator:
    """Walks user through ROI calculation with intelligent defaults"""

    def __init__(self):
        self.console = console
        self.report_gen = ReportGenerator()

    def run_interactive_wizard(self) -> ROIAnalysis:
        """Interactive Q&A to gather inputs"""
        self.console.print("\n[bold cyan]Nixtla ROI Calculator[/bold cyan]")
        self.console.print("Answer a few questions to calculate your ROI\n")

        # Step 1: Team size
        team_size = IntPrompt.ask(
            "How many data scientists work on forecasting?",
            default=5
        )

        avg_salary = FloatPrompt.ask(
            "Average data scientist salary (USD)?",
            default=180000
        )

        # Step 2: Current compute costs
        monthly_compute = FloatPrompt.ask(
            "Monthly cloud compute cost for training models (USD)?",
            default=5000
        )

        mlops_cost = FloatPrompt.ask(
            "Monthly MLOps infrastructure cost (Airflow, monitoring, etc.)?",
            default=2000
        )

        # Step 3: Forecasting scale
        series_count = IntPrompt.ask(
            "How many time series do you forecast?",
            default=100000
        )

        forecasts_per_month = IntPrompt.ask(
            "How many forecasts per series per month?",
            default=30
        )

        # Step 4: Business context
        monthly_revenue = FloatPrompt.ask(
            "Monthly revenue (USD)?",
            default=10000000
        )

        revenue_impact_pct = FloatPrompt.ask(
            "What % of revenue depends on forecast accuracy? (0-100)",
            default=5.0
        ) / 100

        # Build cost models
        internal_build = InternalBuildCost(
            data_scientists=team_size,
            avg_salary_usd=avg_salary,
            compute_monthly_usd=monthly_compute,
            mlops_infrastructure_monthly_usd=mlops_cost,
            maintenance_hours_monthly=40 * team_size,  # 40 hrs/person
            recruiting_cost_usd=50000 * team_size,
            training_cost_usd=10000 * team_size
        )

        nixtla_api = NixtlaAPICost(
            series_count=series_count,
            forecasts_per_series_monthly=forecasts_per_month,
            cost_per_forecast_usd=0.001,
            monthly_subscription_usd=5000
        )

        opportunity = OpportunityCost(
            monthly_revenue_usd=monthly_revenue,
            forecast_driven_revenue_pct=revenue_impact_pct,
            internal_build_time_months=9,
            nixtla_deployment_time_weeks=2
        )

        return ROIAnalysis(
            internal_build=internal_build,
            nixtla_api=nixtla_api,
            opportunity=opportunity
        )

    def display_results(self, analysis: ROIAnalysis):
        """Display comprehensive ROI results"""
        self.console.print("\n[bold green]ROI ANALYSIS RESULTS[/bold green]\n")

        # Cost comparison table
        table = Table(title="Total Cost of Ownership (Annual)")
        table.add_column("Cost Component", style="cyan")
        table.add_column("Internal Build", justify="right", style="red")
        table.add_column("Nixtla API", justify="right", style="green")

        table.add_row(
            "Team Salaries",
            f"${analysis.internal_build.data_scientists * analysis.internal_build.avg_salary_usd * 1.3:,.0f}",
            "$0"
        )
        table.add_row(
            "Cloud Compute",
            f"${analysis.internal_build.compute_monthly_usd * 12:,.0f}",
            "$0 (API handles)"
        )
        table.add_row(
            "MLOps Infrastructure",
            f"${analysis.internal_build.mlops_infrastructure_monthly_usd * 12:,.0f}",
            "$0"
        )
        table.add_row(
            "API/Subscription",
            "$0",
            f"${analysis.nixtla_api.annual_cost_usd:,.0f}"
        )
        table.add_row(
            "[bold]TOTAL ANNUAL COST[/bold]",
            f"[bold red]${analysis.internal_build.annual_cost_usd:,.0f}[/bold red]",
            f"[bold green]${analysis.nixtla_api.annual_cost_usd:,.0f}[/bold green]"
        )

        self.console.print(table)

        # ROI metrics
        self.console.print(f"\n[bold]Annual Savings:[/bold] [green]${analysis.annual_savings_usd:,.0f}[/green]")
        self.console.print(f"[bold]ROI:[/bold] [green]{analysis.roi_percentage:.0f}%[/green]")
        self.console.print(f"[bold]Payback Period:[/bold] [green]{analysis.payback_period_months:.1f} months[/green]")
        self.console.print(f"[bold]3-Year NPV:[/bold] [green]${analysis.net_present_value_3yr_usd:,.0f}[/green]")

        # Opportunity cost
        if analysis.opportunity.opportunity_value_usd > 0:
            self.console.print(f"\n[bold]Time-to-Market Value:[/bold]")
            self.console.print(f"  Internal build: {analysis.opportunity.internal_build_time_months} months")
            self.console.print(f"  Nixtla deployment: {analysis.opportunity.nixtla_deployment_time_weeks} weeks")
            self.console.print(f"  [green]Opportunity value: ${analysis.opportunity.opportunity_value_usd:,.0f}[/green]")

        # Recommendation
        self.console.print(f"\n[bold cyan]RECOMMENDATION:[/bold cyan]")
        if analysis.roi_percentage > 100:
            self.console.print("[green]✅ Nixtla TimeGPT is strongly recommended[/green]")
            self.console.print(f"   ROI of {analysis.roi_percentage:.0f}% justifies the investment")
        elif analysis.roi_percentage > 50:
            self.console.print("[yellow]⚠️  Nixtla TimeGPT is recommended[/yellow]")
            self.console.print(f"   Positive ROI ({analysis.roi_percentage:.0f}%) with moderate savings")
        else:
            self.console.print("[red]❌ Internal build may be more cost-effective[/red]")
            self.console.print(f"   ROI of {analysis.roi_percentage:.0f}% is below threshold")

        # Export options
        self.console.print("\n[bold]Export Options:[/bold]")
        self.console.print("  1. PDF Executive Summary")
        self.console.print("  2. PowerPoint Presentation")
        self.console.print("  3. Excel Financial Model")
        self.console.print("  4. All formats")

        export_choice = Prompt.ask("Export as", choices=["1", "2", "3", "4", "skip"], default="skip")

        if export_choice != "skip":
            self.export_report(analysis, export_choice)

    def export_report(self, analysis: ROIAnalysis, format_choice: str):
        """Export ROI analysis to various formats"""
        formats = {
            "1": ["pdf"],
            "2": ["pptx"],
            "3": ["xlsx"],
            "4": ["pdf", "pptx", "xlsx"]
        }

        for fmt in formats.get(format_choice, []):
            output_file = self.report_gen.generate(analysis, format=fmt)
            self.console.print(f"✅ Exported to: {output_file}")
```

---

## User Journey

### Journey 1: Enterprise Procurement Approval

**Persona**: Jennifer, VP of Engineering
**Goal**: Get $60k TimeGPT budget approved by CFO
**Context**: Has 5 data scientists, 100k series, CFO wants hard ROI

**Steps**:

1. **Run Calculator**
   ```
   Jennifer: /nixtla-roi

   Claude: [Interactive wizard]

           Nixtla ROI Calculator
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           How many data scientists work on forecasting? [5]: 5
           Average data scientist salary (USD)? [180000]: 185000
           Monthly cloud compute cost (USD)? [5000]: 8000
           Monthly MLOps infrastructure cost? [2000]: 3000

           How many time series? [100000]: 120000
           Forecasts per series per month? [30]: 45

           Monthly revenue (USD)? [10000000]: 25000000
           % revenue depending on forecasts? [5]: 8
   ```

2. **View Results**
   ```
   Claude: ROI ANALYSIS RESULTS
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           Total Cost of Ownership (Annual)
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           Cost Component      Internal Build    Nixtla API
           ─────────────────────────────────────────────────
           Team Salaries       $1,202,500        $0
           Cloud Compute       $96,000           $0
           MLOps Infrastructure $36,000          $0
           API/Subscription    $0                $64,800
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           TOTAL ANNUAL COST   $1,334,500        $64,800

           Annual Savings: $1,269,700
           ROI: 1,959%
           Payback Period: 0.6 months
           3-Year NPV: $3,029,850

           Time-to-Market Value:
           Internal build: 9 months
           Nixtla deployment: 2 weeks
           Opportunity value: $1,600,000

           ✅ Nixtla TimeGPT is strongly recommended
              ROI of 1,959% justifies the investment
   ```

3. **Export for CFO**
   ```
   Claude: Export Options:
           1. PDF Executive Summary
           2. PowerPoint Presentation
           3. Excel Financial Model
           4. All formats

           Export as [skip]: 4

           Generating reports...
           ✅ Exported to: nixtla-roi-2025-11-30.pdf
           ✅ Exported to: nixtla-roi-2025-11-30.pptx
           ✅ Exported to: nixtla-roi-2025-11-30.xlsx

           Ready to present to CFO!
   ```

**Outcome**: Jennifer gets approval in 1 week with clear $1.27M annual savings and 1,959% ROI.

---

## Reports Generated

### 1. PDF Executive Summary (1-page)

```
EXECUTIVE SUMMARY: Nixtla TimeGPT ROI Analysis

RECOMMENDATION: Approve TimeGPT API Budget
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Financial Impact
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Annual Savings:      $1,269,700
ROI:                 1,959%
Payback Period:      0.6 months
3-Year NPV:          $3,029,850

Cost Comparison
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Internal Build:      $1,334,500/year
Nixtla API:          $64,800/year
SAVINGS:             95% cost reduction

Strategic Benefits
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ 8.4 months faster time-to-market
✓ Zero MLOps maintenance overhead
✓ Redeploy 5 data scientists to high-value work
✓ Eliminate $96k/year cloud compute costs

Risk Assessment: LOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Vendor stability (backed by Y Combinator)
✓ Enterprise SLA available
✓ Self-hosted option for data sovereignty
```

### 2. PowerPoint (5 slides)
- Slide 1: Executive summary
- Slide 2: Cost comparison chart
- Slide 3: ROI metrics
- Slide 4: Implementation timeline
- Slide 5: Recommendation

### 3. Excel Financial Model (Interactive)
- Dynamic scenario modeling
- Adjustable assumptions
- Sensitivity analysis
- 5-year projection

---

## Dependencies

```txt
# requirements.txt (minimal)
rich>=13.9.4                # Terminal UI
reportlab>=4.0.7            # PDF generation
python-pptx>=0.6.23         # PowerPoint generation
openpyxl>=3.1.2             # Excel generation
click>=8.1.8                # CLI framework
pydantic>=2.12.0            # Data validation
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-30
**Language**: Pure Python (No TypeScript)
