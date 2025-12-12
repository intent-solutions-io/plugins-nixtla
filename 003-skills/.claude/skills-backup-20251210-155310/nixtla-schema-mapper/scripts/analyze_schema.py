#!/usr/bin/env python3
"""
Nixtla Schema Analyzer

Analyzes data source schema and automatically detects column types for Nixtla transformation.
Identifies timestamp, target, series ID, and exogenous columns.

Usage:
    python analyze_schema.py --input data/sales.csv
    python analyze_schema.py --input data/sales.parquet --output mapping.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd


def detect_datetime_column(df: pd.DataFrame) -> Optional[str]:
    """
    Detect the most likely datetime column in the DataFrame.

    Args:
        df: Input DataFrame

    Returns:
        Column name or None if no datetime column found
    """
    # Check for datetime dtype columns
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
    if datetime_cols:
        return datetime_cols[0]

    # Try to parse object columns as dates
    for col in df.select_dtypes(include=["object"]).columns:
        try:
            pd.to_datetime(df[col].dropna().head(100))
            return col
        except (ValueError, TypeError):
            continue

    # Check for common date column names
    date_keywords = ["date", "time", "timestamp", "ds", "datetime", "day", "period"]
    for col in df.columns:
        if any(keyword in col.lower() for keyword in date_keywords):
            try:
                pd.to_datetime(df[col].dropna().head(100))
                return col
            except (ValueError, TypeError):
                continue

    return None


def detect_target_column(df: pd.DataFrame, exclude_cols: List[str]) -> Optional[str]:
    """
    Detect the most likely target (y) column.

    Args:
        df: Input DataFrame
        exclude_cols: Columns to exclude from consideration

    Returns:
        Column name or None if no target found
    """
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns
    candidates = [col for col in numeric_cols if col not in exclude_cols]

    if not candidates:
        return None

    # Prefer columns with common target names
    target_keywords = ["y", "value", "target", "sales", "revenue", "amount", "quantity", "demand"]
    for col in candidates:
        if any(keyword in col.lower() for keyword in target_keywords):
            return col

    # Otherwise, return the first numeric column
    return candidates[0] if candidates else None


def detect_series_id_column(df: pd.DataFrame, exclude_cols: List[str]) -> Optional[str]:
    """
    Detect the most likely series identifier column.

    Args:
        df: Input DataFrame
        exclude_cols: Columns to exclude from consideration

    Returns:
        Column name or None if no ID column found
    """
    candidates = [col for col in df.columns if col not in exclude_cols]

    if not candidates:
        return None

    # Check for common ID column names
    id_keywords = ["id", "unique_id", "series", "store", "product", "sku", "location", "region"]
    for col in candidates:
        if any(keyword in col.lower() for keyword in id_keywords):
            # Verify it has reasonable cardinality (not too many unique values)
            unique_ratio = df[col].nunique() / len(df)
            if 0.001 <= unique_ratio <= 0.5:  # Between 0.1% and 50% unique
                return col

    # Look for categorical columns with moderate cardinality
    for col in candidates:
        if df[col].dtype in ["object", "category", "int64", "int32"]:
            unique_ratio = df[col].nunique() / len(df)
            if 0.001 <= unique_ratio <= 0.5:
                return col

    return None


def detect_exogenous_columns(df: pd.DataFrame, exclude_cols: List[str]) -> List[Tuple[str, str]]:
    """
    Detect potential exogenous (feature) columns.

    Args:
        df: Input DataFrame
        exclude_cols: Columns already assigned (unique_id, ds, y)

    Returns:
        List of (column_name, dtype) tuples
    """
    exog_cols = []

    for col in df.columns:
        if col not in exclude_cols:
            dtype = str(df[col].dtype)
            exog_cols.append((col, dtype))

    return exog_cols


def analyze_schema(
    input_path: str,
    id_col: Optional[str] = None,
    date_col: Optional[str] = None,
    target_col: Optional[str] = None,
) -> Dict:
    """
    Analyze data source and detect column mappings for Nixtla schema.

    Args:
        input_path: Path to CSV or Parquet file
        id_col: Optional manual specification of ID column
        date_col: Optional manual specification of date column
        target_col: Optional manual specification of target column

    Returns:
        Dictionary with schema analysis results
    """
    # Load data
    if input_path.endswith(".csv"):
        df = pd.read_csv(input_path, nrows=10000)  # Sample for performance
    elif input_path.endswith(".parquet"):
        df = pd.read_parquet(input_path)
        if len(df) > 10000:
            df = df.head(10000)
    else:
        raise ValueError(f"Unsupported file format: {input_path}. Use .csv or .parquet")

    # Detect columns
    detected_date_col = date_col or detect_datetime_column(df)
    if not detected_date_col:
        raise ValueError("No timestamp column detected. Specify manually with --date_col")

    detected_id_col = id_col or detect_series_id_column(df, [detected_date_col])

    excluded = [detected_date_col]
    if detected_id_col:
        excluded.append(detected_id_col)

    detected_target_col = target_col or detect_target_column(df, excluded)
    if not detected_target_col:
        raise ValueError("No target column detected. Specify manually with --target_col")

    # Detect exogenous variables
    excluded_for_exog = excluded + [detected_target_col]
    exog_vars = detect_exogenous_columns(df, excluded_for_exog)

    # Gather statistics
    date_series = pd.to_datetime(df[detected_date_col], errors="coerce")

    analysis = {
        "source_path": input_path,
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "mapping": {
            "unique_id": detected_id_col,
            "ds": detected_date_col,
            "y": detected_target_col,
        },
        "column_types": {
            "unique_id": str(df[detected_id_col].dtype) if detected_id_col else None,
            "ds": str(df[detected_date_col].dtype),
            "y": str(df[detected_target_col].dtype),
        },
        "statistics": {
            "series_count": df[detected_id_col].nunique() if detected_id_col else 1,
            "date_range": {"min": str(date_series.min()), "max": str(date_series.max())},
            "target_range": {
                "min": float(df[detected_target_col].min()),
                "max": float(df[detected_target_col].max()),
                "mean": float(df[detected_target_col].mean()),
            },
        },
        "exogenous_variables": [{"name": name, "dtype": dtype} for name, dtype in exog_vars],
    }

    return analysis


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze data schema and detect Nixtla column mappings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect all columns
  python analyze_schema.py --input data/sales.csv

  # Manual column specification
  python analyze_schema.py --input data/sales.csv --id_col store_id --date_col date --target_col revenue

  # Save mapping to JSON
  python analyze_schema.py --input data/sales.csv --output mapping.json
        """,
    )

    parser.add_argument("--input", required=True, help="Path to input CSV or Parquet file")
    parser.add_argument(
        "--id_col", help="Column name for series identifier (auto-detected if not specified)"
    )
    parser.add_argument(
        "--date_col", help="Column name for timestamp (auto-detected if not specified)"
    )
    parser.add_argument(
        "--target_col", help="Column name for target variable (auto-detected if not specified)"
    )
    parser.add_argument(
        "--output", help="Output path for JSON mapping file (prints to stdout if not specified)"
    )

    args = parser.parse_args()

    # Validate input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        # Analyze schema
        analysis = analyze_schema(
            args.input, id_col=args.id_col, date_col=args.date_col, target_col=args.target_col
        )

        # Print human-readable summary
        print("=" * 60)
        print("Nixtla Schema Analysis")
        print("=" * 60)
        print(f"\nSource: {analysis['source_path']}")
        print(f"Rows analyzed: {analysis['total_rows']:,}")
        print(f"Total columns: {analysis['total_columns']}")

        print("\n--- Detected Column Mapping ---")
        mapping = analysis["mapping"]
        types = analysis["column_types"]
        print(f"  unique_id: '{mapping['unique_id']}' ({types['unique_id']})")
        print(f"  ds:        '{mapping['ds']}' ({types['ds']})")
        print(f"  y:         '{mapping['y']}' ({types['y']})")

        print("\n--- Statistics ---")
        stats = analysis["statistics"]
        print(f"  Series count: {stats['series_count']:,}")
        print(f"  Date range:   {stats['date_range']['min']} to {stats['date_range']['max']}")
        print(
            f"  Target range: {stats['target_range']['min']:.2f} to {stats['target_range']['max']:.2f} (mean: {stats['target_range']['mean']:.2f})"
        )

        if analysis["exogenous_variables"]:
            print("\n--- Exogenous Variables ---")
            for var in analysis["exogenous_variables"]:
                print(f"  {var['name']}: {var['dtype']}")

        # Save to file if requested
        if args.output:
            with open(args.output, "w") as f:
                json.dump(analysis, f, indent=2)
            print(f"\n✓ Mapping saved to: {args.output}")

        print("\n" + "=" * 60)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
