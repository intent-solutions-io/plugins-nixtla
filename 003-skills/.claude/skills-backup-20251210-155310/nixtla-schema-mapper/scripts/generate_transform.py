#!/usr/bin/env python3
"""
Nixtla Transformation Generator

Generates production-ready Python transformation code to convert data to Nixtla schema.
Creates a reusable module with proper validation and error handling.

Usage:
    python generate_transform.py --input data/sales.csv --id_col store_id --date_col date --target_col sales
    python generate_transform.py --mapping mapping.json --output data/transform/to_nixtla_schema.py
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def sanitize_path(user_path: str, allowed_dirs: list = None, purpose: str = "file") -> Path:
    """
    Sanitize user-provided path to prevent path traversal attacks.

    Args:
        user_path: User-provided path string
        allowed_dirs: List of allowed parent directories (None = cwd only)
        purpose: Description for error messages

    Returns:
        Resolved, validated Path object

    Raises:
        ValueError: If path attempts traversal outside allowed directories

    OWASP Reference: A01:2021 - Broken Access Control
    """
    if allowed_dirs is None:
        allowed_dirs = [Path.cwd()]

    # Resolve to absolute path
    resolved = Path(user_path).resolve()

    # Check for path traversal attempts
    if ".." in str(user_path):
        raise ValueError(
            f"Security: Path traversal detected in {purpose} path. "
            f"Relative parent references (..) are not allowed."
        )

    # Verify path is within allowed directories
    is_allowed = any(
        resolved == allowed_dir or str(resolved).startswith(str(allowed_dir.resolve()) + "/")
        for allowed_dir in allowed_dirs
    )

    if not is_allowed:
        raise ValueError(
            f"Security: {purpose.capitalize()} path must be within allowed directories. "
            f"Path '{resolved}' is outside permitted locations."
        )

    return resolved


def validate_api_key(key: Optional[str]) -> bool:
    """
    Validate API key format and length.

    Args:
        key: API key string to validate

    Returns:
        True if key appears valid, False otherwise

    Security:
        - Minimum length check prevents empty/trivial keys
        - OWASP A07:2021 - Identification and Authentication Failures
    """
    if not key or len(key.strip()) < 20:
        return False
    return True


TRANSFORM_TEMPLATE = '''"""
Nixtla Schema Transformation
Generated: {generated_date}

Source: {source_path}
Target: Nixtla schema (unique_id, ds, y + exogenous)

Column Mapping:
  unique_id: {id_col} ({id_type})
  ds:        {date_col} ({date_type})
  y:         {target_col} ({target_type})

Usage:
    from {module_import} import to_nixtla_schema
    df = to_nixtla_schema("{source_path}")
"""

from pathlib import Path
from typing import List, Optional

import pandas as pd


def to_nixtla_schema(
    source_path: str = "{source_path}",
    unique_id_col: str = "{id_col}",
    ds_col: str = "{date_col}",
    y_col: str = "{target_col}",
    exog_cols: Optional[List[str]] = None,
    date_format: Optional[str] = None
) -> pd.DataFrame:
    """
    Transform source data to Nixtla-compatible schema.

    Expected Nixtla schema:
        unique_id (str|int): Series identifier
        ds (datetime): Timestamp
        y (float): Target variable
        [exog_vars]: Optional exogenous features

    Args:
        source_path: Path to source CSV/Parquet file
        unique_id_col: Column name for series identifier
        ds_col: Column name for timestamp
        y_col: Column name for target variable
        exog_cols: Optional list of exogenous variable columns
        date_format: Optional date parsing format (e.g., "%Y-%m-%d")

    Returns:
        DataFrame with Nixtla schema

    Raises:
        ValueError: If required columns are missing or invalid
        FileNotFoundError: If source file doesn't exist
    """
    # Validate source file exists
    if not Path(source_path).exists():
        raise FileNotFoundError(f"Source file not found: {{source_path}}")

    # Load data
    if source_path.endswith(".csv"):
        df = pd.read_csv(source_path)
    elif source_path.endswith(".parquet"):
        df = pd.read_parquet(source_path)
    else:
        raise ValueError(f"Unsupported file format: {{source_path}}. Use .csv or .parquet")

    # Validate required columns exist
    required_cols = [unique_id_col, ds_col, y_col]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {{missing}}. "
            f"Available columns: {{list(df.columns)}}"
        )

    # Apply schema transformation
    df_nixtla = df.copy()

    # 1. Map unique_id
    df_nixtla["unique_id"] = df[unique_id_col].astype(str)

    # 2. Map ds (timestamp)
    try:
        if date_format:
            df_nixtla["ds"] = pd.to_datetime(df[ds_col], format=date_format)
        else:
            df_nixtla["ds"] = pd.to_datetime(df[ds_col])
    except Exception as e:
        raise ValueError(
            f"Failed to parse date column '{{ds_col}}': {{e}}. "
            f"Specify format with date_format parameter."
        )

    # 3. Map y (target)
    df_nixtla["y"] = pd.to_numeric(df[y_col], errors="coerce")

    # Check for conversion failures
    nulls_before = df[y_col].isna().sum()
    nulls_after = df_nixtla["y"].isna().sum()
    if nulls_after > nulls_before:
        print(
            f"⚠️  Warning: {{nulls_after - nulls_before}} values couldn't be converted to numeric in '{{y_col}}'"
        )

    # 4. Include exogenous variables (optional)
    if exog_cols is None:
        exog_cols = {exog_cols_default}

    # Filter to available exogenous columns
    available_exog = [col for col in exog_cols if col in df.columns]
    if len(available_exog) < len(exog_cols):
        missing_exog = set(exog_cols) - set(available_exog)
        print(f"ℹ️  Note: Exogenous columns not found: {{missing_exog}}")

    # Select final columns
    final_cols = ["unique_id", "ds", "y"] + available_exog
    df_nixtla = df_nixtla[final_cols]

    # Data quality checks
    initial_rows = len(df_nixtla)

    # Drop rows with missing target
    df_nixtla = df_nixtla.dropna(subset=["y"])
    dropped_y = initial_rows - len(df_nixtla)
    if dropped_y > 0:
        print(f"ℹ️  Dropped {{dropped_y}} rows with missing target values")

    # Drop rows with missing timestamp
    df_nixtla = df_nixtla.dropna(subset=["ds"])
    dropped_ds = initial_rows - dropped_y - len(df_nixtla)
    if dropped_ds > 0:
        print(f"ℹ️  Dropped {{dropped_ds}} rows with missing timestamps")

    # Remove duplicates
    df_nixtla = df_nixtla.drop_duplicates(subset=["unique_id", "ds"], keep="first")
    dropped_dupes = initial_rows - dropped_y - dropped_ds - len(df_nixtla)
    if dropped_dupes > 0:
        print(f"ℹ️  Removed {{dropped_dupes}} duplicate (unique_id, ds) pairs")

    # Ensure ds is sorted within each series
    df_nixtla = df_nixtla.sort_values(["unique_id", "ds"]).reset_index(drop=True)

    # Validate final schema
    assert df_nixtla["unique_id"].notna().all(), "unique_id contains NaN"
    assert df_nixtla["ds"].notna().all(), "ds contains NaN"
    assert df_nixtla["y"].notna().all(), "y contains NaN after cleanup"

    # Infer and report frequency
    if len(df_nixtla) > 0 and df_nixtla["unique_id"].nunique() > 0:
        sample_series = df_nixtla[df_nixtla["unique_id"] == df_nixtla["unique_id"].iloc[0]]
        if len(sample_series) > 1:
            time_deltas = sample_series["ds"].diff().dt.total_seconds().median()
            if time_deltas:
                if time_deltas < 3600:
                    freq = f"{{int(time_deltas / 60)}}min"
                elif time_deltas < 86400:
                    freq = f"{{int(time_deltas / 3600)}}H"
                else:
                    freq = f"{{int(time_deltas / 86400)}}D"
                print(f"ℹ️  Inferred frequency: {{freq}}")

    return df_nixtla


def validate_nixtla_schema(df: pd.DataFrame) -> bool:
    """
    Validate that DataFrame meets Nixtla schema requirements.

    Args:
        df: DataFrame to validate

    Returns:
        True if valid

    Raises:
        AssertionError: If validation fails
    """
    # Check required columns exist
    required_cols = ["unique_id", "ds", "y"]
    assert all(col in df.columns for col in required_cols), \\
        f"Missing required columns. Expected: {{required_cols}}, Got: {{list(df.columns)}}"

    # Check types
    assert df["unique_id"].dtype == "object", \\
        f"unique_id must be string/object type, got {{df['unique_id'].dtype}}"
    assert pd.api.types.is_datetime64_any_dtype(df["ds"]), \\
        f"ds must be datetime type, got {{df['ds'].dtype}}"
    assert pd.api.types.is_numeric_dtype(df["y"]), \\
        f"y must be numeric type, got {{df['y'].dtype}}"

    # Check no nulls in required columns
    assert df["unique_id"].notna().all(), "unique_id contains NaN values"
    assert df["ds"].notna().all(), "ds contains NaN values"
    assert df["y"].notna().all(), "y contains NaN values"

    # Check sorting
    df_sorted = df.sort_values(["unique_id", "ds"]).reset_index(drop=True)
    assert df.equals(df_sorted), "Data not sorted by (unique_id, ds)"

    # Check for duplicates
    duplicates = df.duplicated(subset=["unique_id", "ds"]).sum()
    assert duplicates == 0, f"Found {{duplicates}} duplicate (unique_id, ds) pairs"

    print("✓ All validation checks passed")
    return True


# Example usage and testing
if __name__ == "__main__":
    import sys

    # Transform data
    try:
        df_nixtla = to_nixtla_schema()

        # Display summary
        print("\\n" + "=" * 60)
        print("Nixtla Schema Transformation Complete")
        print("=" * 60)
        print(f"✓ Transformed {{len(df_nixtla):,}} rows")
        print(f"✓ Series count: {{df_nixtla['unique_id'].nunique():,}}")
        print(f"✓ Date range: {{df_nixtla['ds'].min()}} to {{df_nixtla['ds'].max()}}")
        print(f"✓ Columns: {{list(df_nixtla.columns)}}")

        print("\\n--- Sample Data ---")
        print(df_nixtla.head(10))

        print("\\n--- Data Types ---")
        print(df_nixtla.dtypes)

        # Validate schema
        print("\\n--- Validation ---")
        validate_nixtla_schema(df_nixtla)

        # Optionally save transformed data
        output_path = Path("{source_path}").stem + "_nixtla_schema.parquet"
        df_nixtla.to_parquet(output_path, index=False)
        print(f"\\n💾 Saved: {{output_path}}")

    except Exception as e:
        print(f"\\nError during transformation: {{e}}", file=sys.stderr)
        sys.exit(1)
'''


def generate_transformation_code(
    source_path: str,
    id_col: str,
    date_col: str,
    target_col: str,
    id_type: str = "object",
    date_type: str = "object",
    target_type: str = "float64",
    exog_cols: Optional[List[str]] = None,
    output_path: Optional[str] = None,
) -> str:
    """
    Generate Python transformation module code.

    Args:
        source_path: Source data file path
        id_col: Column name for unique_id
        date_col: Column name for ds
        target_col: Column name for y
        id_type: Data type of ID column
        date_type: Data type of date column
        target_type: Data type of target column
        exog_cols: Optional exogenous variable column names
        output_path: Optional output file path for generated code

    Returns:
        Generated Python code as string
    """
    # Determine module import path
    if output_path:
        module_path = Path(output_path)
        module_import = str(module_path.parent).replace("/", ".") + "." + module_path.stem
    else:
        module_import = "data.transform.to_nixtla_schema"

    # Format exogenous columns
    if exog_cols:
        exog_cols_str = json.dumps(exog_cols)
    else:
        exog_cols_str = "[]"

    # Generate code from template
    code = TRANSFORM_TEMPLATE.format(
        generated_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        source_path=source_path,
        id_col=id_col,
        date_col=date_col,
        target_col=target_col,
        id_type=id_type,
        date_type=date_type,
        target_type=target_type,
        exog_cols_default=exog_cols_str,
        module_import=module_import,
    )

    return code


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Nixtla schema transformation code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from explicit column names
  python generate_transform.py --input data/sales.csv --id_col store_id --date_col date --target_col revenue

  # Generate from mapping file
  python generate_transform.py --mapping mapping.json --output data/transform/to_nixtla_schema.py

  # Include exogenous variables
  python generate_transform.py --input data/sales.csv --id_col store_id --date_col date --target_col sales --exog price,promotion
        """,
    )

    parser.add_argument("--input", help="Path to input CSV or Parquet file")
    parser.add_argument("--mapping", help="Path to JSON mapping file from analyze_schema.py")
    parser.add_argument("--id_col", help="Column name for series identifier")
    parser.add_argument("--date_col", help="Column name for timestamp")
    parser.add_argument("--target_col", help="Column name for target variable")
    parser.add_argument("--exog", help="Comma-separated list of exogenous variable columns")
    parser.add_argument(
        "--output",
        default="to_nixtla_schema.py",
        help="Output path for generated Python module (default: to_nixtla_schema.py)",
    )

    args = parser.parse_args()

    # Determine source of configuration
    if args.mapping:
        # Security: Sanitize mapping file path
        try:
            mapping_path = sanitize_path(args.mapping, purpose="mapping")
        except ValueError as e:
            print(f"Security Error: {e}", file=sys.stderr)
            sys.exit(1)

        # Load from mapping file
        try:
            with open(mapping_path, "r") as f:
                mapping = json.load(f)

            source_path = mapping.get("source_path", "")
            id_col = mapping["mapping"].get("unique_id", "id")
            date_col = mapping["mapping"]["ds"]
            target_col = mapping["mapping"]["y"]

            id_type = mapping["column_types"].get("unique_id", "object")
            date_type = mapping["column_types"]["ds"]
            target_type = mapping["column_types"]["y"]

            exog_cols = [var["name"] for var in mapping.get("exogenous_variables", [])]

        except FileNotFoundError:
            print(f"Error: Mapping file not found: {args.mapping}", file=sys.stderr)
            sys.exit(1)
        except KeyError as e:
            print(f"Error: Invalid mapping file format. Missing key: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.input and args.date_col and args.target_col:
        # Use explicit arguments
        source_path = args.input
        id_col = args.id_col or "id"
        date_col = args.date_col
        target_col = args.target_col

        id_type = "object"
        date_type = "object"
        target_type = "float64"

        exog_cols = args.exog.split(",") if args.exog else []

    else:
        print(
            "Error: Must provide either --mapping or (--input --date_col --target_col)",
            file=sys.stderr,
        )
        parser.print_help()
        sys.exit(1)

    # Security: Sanitize output path
    try:
        output_file = sanitize_path(args.output, purpose="output")
    except ValueError as e:
        print(f"Security Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate transformation code
    code = generate_transformation_code(
        source_path=source_path,
        id_col=id_col,
        date_col=date_col,
        target_col=target_col,
        id_type=id_type,
        date_type=date_type,
        target_type=target_type,
        exog_cols=exog_cols,
        output_path=str(output_file),
    )

    # Write to file
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        f.write(code)

    print(f"✓ Generated transformation module: {output_file}")
    print(f"\nUsage:")
    print(f"  python {output_file}")
    print(f"  # or import in your code:")
    print(f"  from {output_file.stem} import to_nixtla_schema")


if __name__ == "__main__":
    main()
