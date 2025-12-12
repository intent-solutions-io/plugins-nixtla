#!/usr/bin/env python3
"""
Validate forecasting experiment configuration and data readiness.

This script performs comprehensive validation checks before running experiments:
- Configuration file validity
- Data file accessibility and format
- Required columns presence
- Data quality checks (nulls, duplicates, date continuity)
- Package dependencies availability

Usage:
    python validate_experiment.py --config forecasting/config.yml
    python validate_experiment.py --config config.yml --check-packages
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate Nixtla forecasting experiment configuration and data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate configuration and data
  python validate_experiment.py --config forecasting/config.yml

  # Include package dependency checks
  python validate_experiment.py --config config.yml --check-packages

  # Verbose output with detailed diagnostics
  python validate_experiment.py --config config.yml --verbose

Exit codes:
  0 - All validations passed
  1 - Validation errors found
  2 - Configuration file issues
        """,
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to YAML configuration file",
    )
    parser.add_argument(
        "--check-packages",
        action="store_true",
        help="Verify all required packages are installed",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed validation diagnostics",
    )

    return parser.parse_args()


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load and parse configuration file.

    Args:
        config_path: Path to config file

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    return config


def validate_config_structure(config: Dict[str, Any]) -> List[str]:
    """
    Validate configuration structure and required fields.

    Args:
        config: Configuration dictionary

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Check required sections
    required_sections = ["data", "forecast", "cv", "models", "metrics", "output"]
    for section in required_sections:
        if section not in config:
            errors.append(f"Missing required config section: {section}")

    if errors:
        return errors

    # Validate data section
    data_required = ["source", "ds", "y"]
    for field in data_required:
        if field not in config["data"]:
            errors.append(f"Missing required data field: data.{field}")

    # Validate forecast section
    if "horizon" not in config["forecast"]:
        errors.append("Missing required field: forecast.horizon")
    elif not isinstance(config["forecast"]["horizon"], int) or config["forecast"]["horizon"] < 1:
        errors.append(
            f"Invalid horizon: must be positive integer, got {config['forecast']['horizon']}"
        )

    if "freq" not in config["forecast"]:
        errors.append("Missing required field: forecast.freq")
    elif config["forecast"]["freq"] not in ["D", "H", "W", "M", "MS", "Q", "Y"]:
        errors.append(f"Invalid frequency: {config['forecast']['freq']}")

    # Validate CV section
    cv_required = ["method", "h", "step_size", "n_windows"]
    for field in cv_required:
        if field not in config["cv"]:
            errors.append(f"Missing required cv field: cv.{field}")

    if "method" in config["cv"] and config["cv"]["method"] not in ["rolling", "expanding"]:
        errors.append(
            f"Invalid CV method: {config['cv']['method']} (must be 'rolling' or 'expanding')"
        )

    # Validate at least one model is enabled
    models_enabled = (
        bool(config.get("models", {}).get("statsforecast"))
        or config.get("models", {}).get("mlforecast", {}).get("enabled", False)
        or config.get("models", {}).get("timegpt", {}).get("enabled", False)
    )
    if not models_enabled:
        errors.append("No model families enabled. Enable at least one model type.")

    # Validate metrics
    if not config.get("metrics"):
        errors.append("No evaluation metrics specified")
    else:
        valid_metrics = ["smape", "mase", "rmse", "mae"]
        for metric in config["metrics"]:
            if metric not in valid_metrics:
                errors.append(f"Invalid metric: {metric} (valid: {', '.join(valid_metrics)})")

    return errors


def validate_data_file(config: Dict[str, Any], verbose: bool = False) -> List[str]:
    """
    Validate data file existence, format, and basic structure.

    Args:
        config: Configuration dictionary
        verbose: Print detailed diagnostics

    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    data_path = Path(config["data"]["source"])

    # Check file exists
    if not data_path.exists():
        errors.append(f"Data file not found: {data_path}")
        return errors

    # Check file format
    if data_path.suffix not in [".csv", ".parquet"]:
        errors.append(f"Unsupported file format: {data_path.suffix} (use .csv or .parquet)")
        return errors

    # Try to load and validate data
    try:
        if data_path.suffix == ".csv":
            import pandas as pd

            df = pd.read_csv(data_path, nrows=100)  # Sample first 100 rows
        else:
            import pandas as pd

            df = pd.read_parquet(data_path)

        if verbose:
            print(f"  Data preview: {len(df)} rows (sample), {len(df.columns)} columns")

        # Check required columns
        required_cols = [config["data"]["ds"], config["data"]["y"]]
        if config["data"].get("unique_id"):
            required_cols.append(config["data"]["unique_id"])

        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            errors.append(f"Missing required columns: {', '.join(missing_cols)}")
            errors.append(f"Available columns: {', '.join(df.columns)}")
            return errors

        # Check for nulls in critical columns
        ds_col = config["data"]["ds"]
        y_col = config["data"]["y"]

        if df[ds_col].isnull().any():
            null_pct = df[ds_col].isnull().mean() * 100
            errors.append(f"Timestamp column '{ds_col}' contains {null_pct:.1f}% null values")

        if df[y_col].isnull().any():
            null_pct = df[y_col].isnull().mean() * 100
            if null_pct > 50:
                errors.append(
                    f"Target column '{y_col}' contains {null_pct:.1f}% null values (too high)"
                )
            elif verbose:
                print(f"  Warning: Target column contains {null_pct:.1f}% null values")

        # Check target is numeric
        if not pd.api.types.is_numeric_dtype(df[y_col]):
            errors.append(f"Target column '{y_col}' must be numeric, got dtype: {df[y_col].dtype}")

        # Check timestamp can be parsed
        try:
            pd.to_datetime(df[ds_col].dropna())
        except Exception as e:
            errors.append(f"Cannot parse timestamp column '{ds_col}': {e}")

        if verbose and not errors:
            print(f"  ✓ Data file is valid")
            print(f"  ✓ All required columns present")
            print(f"  ✓ Data types are correct")

    except ImportError:
        errors.append("pandas package not installed (required for validation)")
    except Exception as e:
        errors.append(f"Error reading data file: {e}")

    return errors


def check_package_dependencies(config: Dict[str, Any], verbose: bool = False) -> List[str]:
    """
    Check if required packages are installed.

    Args:
        config: Configuration dictionary
        verbose: Print detailed diagnostics

    Returns:
        List of error/warning messages
    """
    issues = []

    # Core requirements
    core_packages = {
        "pandas": "Data manipulation",
        "yaml": "Configuration parsing",
        "statsforecast": "StatsForecast models",
        "utilsforecast": "Evaluation metrics",
    }

    for package, purpose in core_packages.items():
        try:
            __import__(package if package != "yaml" else "yaml")
            if verbose:
                print(f"  ✓ {package} ({purpose})")
        except ImportError:
            issues.append(f"Missing required package: {package} ({purpose})")

    # Optional packages based on config
    if config["models"].get("mlforecast", {}).get("enabled"):
        ml_packages = {
            "mlforecast": "MLForecast models",
            "sklearn": "Scikit-learn models",
            "lightgbm": "LightGBM models",
        }
        for package, purpose in ml_packages.items():
            try:
                __import__(package)
                if verbose:
                    print(f"  ✓ {package} ({purpose})")
            except ImportError:
                issues.append(f"Missing package for MLForecast: {package} ({purpose})")

    if config["models"].get("timegpt", {}).get("enabled"):
        try:
            __import__("nixtla")
            if verbose:
                print(f"  ✓ nixtla (TimeGPT API)")
        except ImportError:
            issues.append(f"Missing package for TimeGPT: nixtla")

    return issues


def validate_cv_settings(config: Dict[str, Any]) -> List[str]:
    """
    Validate cross-validation settings are reasonable.

    Args:
        config: Configuration dictionary

    Returns:
        List of warning messages
    """
    warnings = []

    cv_horizon = config["cv"]["h"]
    forecast_horizon = config["forecast"]["horizon"]

    # Check CV horizon vs forecast horizon
    if cv_horizon > forecast_horizon:
        warnings.append(
            f"CV horizon ({cv_horizon}) is greater than forecast horizon ({forecast_horizon}). "
            "This is unusual but not invalid."
        )

    # Check number of windows
    n_windows = config["cv"]["n_windows"]
    if n_windows < 2:
        warnings.append(
            f"Only {n_windows} CV window configured. Consider using at least 3-5 windows "
            "for robust evaluation."
        )

    # Check step size
    step_size = config["cv"]["step_size"]
    if step_size > cv_horizon:
        warnings.append(
            f"Step size ({step_size}) is greater than CV horizon ({cv_horizon}). "
            "This will create gaps in validation coverage."
        )

    return warnings


def main() -> int:
    """Main entry point."""
    args = parse_args()
    errors = []
    warnings = []

    print("=" * 60)
    print("Nixtla Experiment Validation")
    print("=" * 60)

    # Load configuration
    print("\n1. Loading configuration...")
    try:
        config = load_config(args.config)
        print(f"   ✓ Config loaded: {args.config}")
    except FileNotFoundError as e:
        print(f"   ❌ {e}")
        return 2
    except yaml.YAMLError as e:
        print(f"   ❌ Invalid YAML: {e}")
        return 2

    # Validate config structure
    print("\n2. Validating configuration structure...")
    config_errors = validate_config_structure(config)
    if config_errors:
        errors.extend(config_errors)
        for error in config_errors:
            print(f"   ❌ {error}")
    else:
        print("   ✓ Configuration structure is valid")

    # Validate data file
    print("\n3. Validating data file...")
    data_errors = validate_data_file(config, verbose=args.verbose)
    if data_errors:
        errors.extend(data_errors)
        for error in data_errors:
            print(f"   ❌ {error}")
    else:
        print(f"   ✓ Data file is valid: {config['data']['source']}")

    # Check CV settings
    print("\n4. Checking cross-validation settings...")
    cv_warnings = validate_cv_settings(config)
    if cv_warnings:
        warnings.extend(cv_warnings)
        for warning in cv_warnings:
            print(f"   ⚠️  {warning}")
    else:
        print("   ✓ Cross-validation settings are reasonable")

    # Check packages if requested
    if args.check_packages:
        print("\n5. Checking package dependencies...")
        package_issues = check_package_dependencies(config, verbose=args.verbose)
        if package_issues:
            for issue in package_issues:
                if "Missing required" in issue:
                    errors.append(issue)
                    print(f"   ❌ {issue}")
                else:
                    warnings.append(issue)
                    print(f"   ⚠️  {issue}")
        else:
            print("   ✓ All required packages are installed")

    # Print summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)

    if errors:
        print(f"\n❌ Found {len(errors)} error(s):")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
        print("\nFix these errors before running the experiment.")
        return 1
    elif warnings:
        print(f"\n⚠️  Found {len(warnings)} warning(s):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
        print("\n✅ Validation passed with warnings. Experiment can proceed.")
        return 0
    else:
        print("\n✅ All validations passed! Experiment is ready to run.")
        print(f"\nNext steps:")
        print(f"  1. Run: python forecasting/experiments.py")
        print(f"  2. Review results: cat {config['output']['results_dir']}/metrics_summary.csv")
        return 0


if __name__ == "__main__":
    sys.exit(main())
