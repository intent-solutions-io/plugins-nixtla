#!/usr/bin/env python3
"""Cost modeling engine for TCO calculations."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CostModel:
    """Total Cost of Ownership model."""

    # Tool costs
    license_cost_monthly: float = 0.0
    license_cost_annual: float = 0.0

    # Personnel costs
    fte_count: float = 0.0
    fte_percentage_allocation: float = 0.0
    fte_annual_salary: float = 120000.0

    # Infrastructure costs
    compute_cost_monthly: float = 0.0
    storage_cost_monthly: float = 0.0

    # Operational costs
    maintenance_hours_monthly: float = 0.0
    training_cost_annual: float = 0.0

    def calculate_tco(self, years: int = 3) -> dict:
        """Calculate total cost of ownership."""
        # Annual license
        if self.license_cost_annual > 0:
            annual_license = self.license_cost_annual
        else:
            annual_license = self.license_cost_monthly * 12

        # Annual personnel
        annual_personnel = (
            self.fte_count *
            self.fte_percentage_allocation *
            self.fte_annual_salary
        )

        # Annual infrastructure
        annual_infra = (self.compute_cost_monthly + self.storage_cost_monthly) * 12

        # Annual operational
        annual_ops = (
            self.maintenance_hours_monthly * 12 * 75 +  # $75/hr
            self.training_cost_annual
        )

        total_annual = annual_license + annual_personnel + annual_infra + annual_ops

        return {
            "license": {"annual": annual_license, f"{years}year": annual_license * years},
            "personnel": {"annual": annual_personnel, f"{years}year": annual_personnel * years},
            "infrastructure": {"annual": annual_infra, f"{years}year": annual_infra * years},
            "operational": {"annual": annual_ops, f"{years}year": annual_ops * years},
            "total": {"annual": total_annual, f"{years}year": total_annual * years}
        }


def model_prophet_costs(
    series_count: int,
    forecasts_per_day: int,
    fte_hours_per_week: float
) -> CostModel:
    """Model costs for Prophet-based forecasting."""
    return CostModel(
        license_cost_monthly=0,  # Open source
        fte_count=1,
        fte_percentage_allocation=fte_hours_per_week / 40,
        compute_cost_monthly=500 * (series_count / 1000),  # $500 per 1000 series
        storage_cost_monthly=50,
        maintenance_hours_monthly=fte_hours_per_week * 0.2
    )


def model_timegpt_costs(
    series_count: int,
    forecasts_per_day: int,
    price_per_1k_calls: float = 0.10
) -> CostModel:
    """Model costs for TimeGPT."""
    monthly_calls = forecasts_per_day * 30
    monthly_api_cost = (monthly_calls * price_per_1k_calls) / 1000

    return CostModel(
        license_cost_monthly=monthly_api_cost,
        fte_count=1,
        fte_percentage_allocation=0.1,  # 90% reduction
        compute_cost_monthly=0,  # No infrastructure needed
        storage_cost_monthly=10,  # Just for results
        maintenance_hours_monthly=2
    )


def compare_models(
    current: CostModel,
    proposed: CostModel,
    years: int = 3
) -> dict:
    """Compare two cost models."""
    current_tco = current.calculate_tco(years)
    proposed_tco = proposed.calculate_tco(years)

    savings = current_tco["total"][f"{years}year"] - proposed_tco["total"][f"{years}year"]
    roi = (savings / current_tco["total"][f"{years}year"]) * 100 if current_tco["total"][f"{years}year"] > 0 else 0

    return {
        "current": current_tco,
        "proposed": proposed_tco,
        "savings": savings,
        "roi_percentage": roi,
        "payback_months": 12 / (savings / current_tco["total"]["annual"]) if savings > 0 else float('inf')
    }
