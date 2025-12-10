#!/usr/bin/env python3
"""
Correlation Mapper - Visualization
Creates correlation heatmap and analysis plots
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def create_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    output_path: str = "correlation_heatmap.png",
    title: str = "Contract Correlation Matrix",
) -> None:
    """
    Create a correlation heatmap visualization.

    Args:
        corr_matrix: Correlation matrix DataFrame
        output_path: Path to save the plot
        title: Plot title
    """
    # Set up the figure
    n_contracts = len(corr_matrix)
    fig_size = max(10, n_contracts * 0.5)

    fig, ax = plt.subplots(figsize=(fig_size, fig_size * 0.8))

    # Create mask for upper triangle
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

    # Create heatmap
    cmap = sns.diverging_palette(250, 10, as_cmap=True)

    sns.heatmap(
        corr_matrix,
        mask=mask,
        cmap=cmap,
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        linewidths=0.5,
        annot=True if n_contracts <= 10 else False,
        fmt=".2f",
        cbar_kws={"label": "Correlation Coefficient"},
        ax=ax,
    )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
    ax.set_xlabel("Contract", fontsize=11)
    ax.set_ylabel("Contract", fontsize=11)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved heatmap to {output_path}")


def create_rolling_correlation_plot(
    rolling_corr: pd.DataFrame,
    output_path: str = "rolling_correlation.png",
    top_n: int = 5,
) -> None:
    """
    Plot rolling correlations over time.

    Args:
        rolling_corr: Rolling correlation DataFrame
        output_path: Path to save the plot
        top_n: Number of pairs to plot
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot top N pairs by volatility (most interesting)
    volatility = rolling_corr.std().sort_values(ascending=False)
    top_pairs = volatility.head(top_n).index.tolist()

    for pair in top_pairs:
        ax.plot(rolling_corr.index, rolling_corr[pair], label=pair, alpha=0.7, linewidth=2)

    # Reference lines
    ax.axhline(y=0, color="black", linestyle="-", alpha=0.3, linewidth=1)
    ax.axhline(y=0.5, color="green", linestyle=":", alpha=0.5, linewidth=1, label="Strong positive")
    ax.axhline(y=-0.5, color="red", linestyle=":", alpha=0.5, linewidth=1, label="Strong negative")

    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Rolling Correlation", fontsize=11)
    ax.set_title("Rolling 30-Day Correlation Between Contracts", fontsize=13, fontweight="bold")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-1, 1)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved rolling correlation plot to {output_path}")


def create_hedge_effectiveness_chart(
    recommendations: list, output_path: str = "hedge_effectiveness.png"
) -> None:
    """
    Create bar chart of hedge effectiveness.

    Args:
        recommendations: List of hedge recommendation dicts
        output_path: Path to save the plot
    """
    if not recommendations:
        print("No recommendations to plot")
        return

    fig, ax = plt.subplots(figsize=(10, max(6, len(recommendations) * 0.4)))

    # Prepare data
    labels = [f"{r['target']}\n→{r['hedge_instrument']}" for r in recommendations]
    effectiveness = [r["variance_reduction_pct"] for r in recommendations]

    # Color coding
    colors = [
        "green" if e > 50 else "orange" if e > 25 else "red" for e in effectiveness
    ]

    # Create horizontal bar chart
    bars = ax.barh(labels, effectiveness, color=colors, alpha=0.7, edgecolor="black")

    # Add value labels
    for bar, val in zip(bars, effectiveness):
        ax.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    # Add reference lines
    ax.axvline(x=50, color="green", linestyle="--", alpha=0.5, linewidth=1.5, label="Good (>50%)")
    ax.axvline(x=25, color="orange", linestyle="--", alpha=0.5, linewidth=1.5, label="Moderate (>25%)")

    ax.set_xlabel("Variance Reduction (%)", fontsize=11)
    ax.set_title("Hedge Effectiveness by Contract Pair", fontsize=13, fontweight="bold")
    ax.set_xlim(0, max(effectiveness) + 10)
    ax.grid(axis="x", alpha=0.3)
    ax.legend(loc="lower right")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved hedge effectiveness chart to {output_path}")


def main():
    """Main entry point for visualization."""
    parser = argparse.ArgumentParser(
        description="Create correlation and hedge effectiveness visualizations"
    )
    parser.add_argument(
        "--correlation",
        type=str,
        default="correlation_matrix.csv",
        help="Input correlation matrix CSV (default: correlation_matrix.csv)",
    )
    parser.add_argument(
        "--rolling",
        type=str,
        default="rolling_correlations.csv",
        help="Input rolling correlations CSV (optional)",
    )
    parser.add_argument(
        "--recommendations",
        type=str,
        default="hedge_recommendations.json",
        help="Input hedge recommendations JSON (optional)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory (default: current dir)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="Number of pairs for rolling correlation plot (default: 5)",
    )

    args = parser.parse_args()

    try:
        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Load and create correlation heatmap
        corr_path = Path(args.correlation)
        if not corr_path.exists():
            raise FileNotFoundError(f"Correlation matrix not found: {corr_path}")

        corr_matrix = pd.read_csv(corr_path, index_col=0)
        print(f"Loaded correlation matrix: {len(corr_matrix)} x {len(corr_matrix.columns)}")

        heatmap_path = output_dir / "correlation_heatmap.png"
        create_correlation_heatmap(corr_matrix, str(heatmap_path))

        # Load and plot rolling correlations if available
        rolling_path = Path(args.rolling)
        if rolling_path.exists():
            rolling = pd.read_csv(rolling_path, index_col=0, parse_dates=True)
            print(f"Loaded rolling correlations: {len(rolling)} rows")
            rolling_plot_path = output_dir / "rolling_correlation.png"
            create_rolling_correlation_plot(rolling, str(rolling_plot_path), args.top_n)
        else:
            print(f"Rolling correlations not found: {rolling_path}, skipping")

        # Load and plot hedge effectiveness
        rec_path = Path(args.recommendations)
        if rec_path.exists():
            with open(rec_path) as f:
                recommendations = json.load(f)
            print(f"Loaded {len(recommendations)} recommendations")
            effectiveness_path = output_dir / "hedge_effectiveness.png"
            create_hedge_effectiveness_chart(recommendations, str(effectiveness_path))
        else:
            print(f"Recommendations not found: {rec_path}, skipping")

        print("\nVisualization complete!")
        print("Next: Run generate_report.py to create markdown report")
        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
