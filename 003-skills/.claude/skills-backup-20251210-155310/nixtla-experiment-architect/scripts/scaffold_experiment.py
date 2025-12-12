#!/usr/bin/env python3
"""
Scaffold forecasting experiment from configuration file.

This script reads a YAML configuration file and generates a complete experiment
harness by processing the experiments_template.py template. The generated script
is ready to run and will execute the full forecasting workflow.

Usage:
    python scaffold_experiment.py --config forecasting/config.yml
    python scaffold_experiment.py --config config.yml --output my_experiment.py
"""

import argparse
import shlex
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

# Security: Define allowed directories for path traversal protection
ALLOWED_TEMPLATE_DIRS = [
    Path(__file__).parent.parent / "assets" / "templates",
    Path.cwd(),
]


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


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Scaffold Nixtla forecasting experiment from config",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate experiment from config
  python scaffold_experiment.py --config forecasting/config.yml

  # Custom output location
  python scaffold_experiment.py --config config.yml --output experiments/run_forecast.py

Workflow:
  1. Run generate_config.py to create config.yml
  2. Run this script to create experiments.py
  3. Execute experiments.py to run forecasting
        """,
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to YAML configuration file",
    )
    parser.add_argument(
        "--output",
        default="forecasting/experiments.py",
        help="Output path for experiment script (default: forecasting/experiments.py)",
    )
    parser.add_argument(
        "--template",
        default=None,
        help="Path to custom template (default: use built-in template)",
    )

    return parser.parse_args()


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.

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


def load_template(template_path: str = None) -> str:
    """
    Load experiment template with path traversal protection.

    Args:
        template_path: Path to custom template (optional)

    Returns:
        Template content as string

    Security:
        - Validates custom template paths against allowed directories
        - Prevents path traversal attacks (OWASP A01:2021)
    """
    if template_path:
        # Security: Sanitize custom template path
        try:
            template_file = sanitize_path(
                template_path, allowed_dirs=ALLOWED_TEMPLATE_DIRS, purpose="template"
            )
        except ValueError as e:
            raise ValueError(f"Invalid template path: {e}")

        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        with open(template_file, "r") as f:
            return f.read()
    else:
        # Use built-in template (already within allowed directory)
        script_dir = Path(__file__).parent
        template_file = script_dir.parent / "assets" / "templates" / "experiments_template.py"
        if not template_file.exists():
            raise FileNotFoundError(
                f"Built-in template not found: {template_file}\n"
                "Please ensure the skill directory structure is intact."
            )
        with open(template_file, "r") as f:
            return f.read()


def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate configuration structure and required fields.

    Args:
        config: Configuration dictionary

    Raises:
        ValueError: If validation fails
    """
    required_sections = ["data", "forecast", "cv", "models", "metrics", "output"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required config section: {section}")

    # Validate data section
    data_required = ["source", "ds", "y"]
    for field in data_required:
        if field not in config["data"]:
            raise ValueError(f"Missing required data field: {field}")

    # Validate forecast section
    forecast_required = ["horizon", "freq"]
    for field in forecast_required:
        if field not in config["forecast"]:
            raise ValueError(f"Missing required forecast field: {field}")

    # Validate cv section
    cv_required = ["method", "h", "step_size", "n_windows"]
    for field in cv_required:
        if field not in config["cv"]:
            raise ValueError(f"Missing required cv field: {field}")

    # Validate models section
    if "statsforecast" not in config["models"]:
        raise ValueError("Missing statsforecast models configuration")

    # Validate at least one model family is enabled
    models_enabled = (
        bool(config["models"].get("statsforecast"))
        or config["models"].get("mlforecast", {}).get("enabled", False)
        or config["models"].get("timegpt", {}).get("enabled", False)
    )
    if not models_enabled:
        raise ValueError("No model families enabled. Enable at least one model type.")


def escape_string_for_code(value: str) -> str:
    """
    Escape string value for safe embedding in generated Python code.

    Args:
        value: String to escape

    Returns:
        Escaped string safe for code generation

    Security:
        - Prevents code injection via configuration values
        - OWASP A03:2021 - Injection
    """
    # Replace backslashes first, then quotes
    escaped = value.replace("\\", "\\\\")
    escaped = escaped.replace('"', '\\"')
    escaped = escaped.replace("'", "\\'")
    escaped = escaped.replace("\n", "\\n")
    escaped = escaped.replace("\r", "\\r")
    return escaped


def customize_template(template: str, config: Dict[str, Any], config_path: str) -> str:
    """
    Customize template with configuration-specific settings.

    Args:
        template: Template content
        config: Configuration dictionary
        config_path: Path to config file

    Returns:
        Customized script content

    Security:
        - Uses shlex.quote() for paths in shell contexts
        - Escapes string values to prevent code injection
        - OWASP A03:2021 - Injection
    """
    # Security: Escape config path for safe embedding in Python code
    safe_config_path = escape_string_for_code(config_path)

    # Replace config file path
    customized = template.replace(
        'with open("forecasting/config.yml", "r") as f:',
        f'with open("{safe_config_path}", "r") as f:',
    )

    # Security: Escape all config values before embedding in generated code
    safe_data_source = escape_string_for_code(str(config["data"]["source"]))
    safe_target = escape_string_for_code(str(config["data"]["y"]))
    safe_freq = escape_string_for_code(str(config["forecast"]["freq"]))
    safe_results_dir = escape_string_for_code(str(config["output"]["results_dir"]))

    # Add configuration summary as comment at top
    header = f'''"""
Nixtla Forecasting Experiment Harness
Generated by nixtla-experiment-architect skill

Configuration:
  Data source: {safe_data_source}
  Target: {safe_target}
  Horizon: {config['forecast']['horizon']} periods ({safe_freq})
  CV windows: {config['cv']['n_windows']}

Models enabled:
  StatsForecast: {len(config['models']['statsforecast'])} models
  MLForecast: {'Yes' if config['models'].get('mlforecast', {}).get('enabled') else 'No'}
  TimeGPT: {'Yes' if config['models'].get('timegpt', {}).get('enabled') else 'No'}

This script:
1. Loads data into Nixtla schema (unique_id, ds, y)
2. Runs StatsForecast baseline models
3. Runs MLForecast with lag features (if enabled)
4. Calls TimeGPT (if API key configured)
5. Performs cross-validation
6. Computes evaluation metrics (SMAPE, MASE, RMSE)
7. Saves results to {safe_results_dir}/
"""
'''

    # Replace the docstring
    customized = customized.split('"""', 2)[2]  # Remove original docstring
    customized = header + '"""' + customized

    return customized


def save_experiment(content: str, output_path: str) -> None:
    """
    Save experiment script to file.

    Args:
        content: Script content
        output_path: Path to save script
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w") as f:
        f.write(content)

    # Make executable
    output.chmod(0o755)

    print(f"✅ Experiment script saved to: {output}")


def print_summary(config: Dict[str, Any], output_path: str) -> None:
    """
    Print scaffolding summary and next steps.

    Args:
        config: Configuration dictionary
        output_path: Path where experiment was saved
    """
    print("\n" + "=" * 60)
    print("Experiment Scaffolding Complete")
    print("=" * 60)

    print("\nGenerated experiment:")
    print(f"  Location: {output_path}")
    print(f"  Models:   {len(config['models']['statsforecast'])} StatsForecast", end="")
    if config["models"].get("mlforecast", {}).get("enabled"):
        print(f" + {len(config['models']['mlforecast']['base_models'])} MLForecast", end="")
    if config["models"].get("timegpt", {}).get("enabled"):
        print(" + TimeGPT", end="")
    print()

    print("\nRequired dependencies:")
    print("  - statsforecast")
    print("  - utilsforecast")
    print("  - pyyaml")
    if config["models"].get("mlforecast", {}).get("enabled"):
        print("  - mlforecast")
        print("  - scikit-learn")
        print("  - lightgbm")
    if config["models"].get("timegpt", {}).get("enabled"):
        print("  - nixtla")
        print("  - NIXTLA_API_KEY environment variable")

    print("\nNext steps:")
    print(f"  1. Install dependencies: pip install -r requirements.txt")
    print(f"  2. Run experiment: python {output_path}")
    print(f"  3. Review results: cat {config['output']['results_dir']}/metrics_summary.csv")
    print()


def check_data_file(config: Dict[str, Any]) -> None:
    """
    Check if data file exists and print warning if not found.

    Args:
        config: Configuration dictionary
    """
    data_path = Path(config["data"]["source"])
    if not data_path.exists():
        print(f"\n⚠️  Warning: Data file not found: {data_path}")
        print("   Ensure the data file is available before running the experiment.")


def main() -> int:
    """Main entry point."""
    try:
        args = parse_args()

        # Load configuration
        print(f"📋 Loading configuration from: {args.config}")
        config = load_config(args.config)

        # Validate configuration
        print("✓ Validating configuration...")
        validate_config(config)

        # Load template
        print("📝 Loading experiment template...")
        template = load_template(args.template)

        # Customize template
        print("🔧 Customizing experiment script...")
        experiment_content = customize_template(template, config, args.config)

        # Save experiment
        print(f"💾 Saving experiment script...")
        save_experiment(experiment_content, args.output)

        # Check data file
        check_data_file(config)

        # Print summary
        print_summary(config, args.output)

        return 0

    except FileNotFoundError as e:
        print(f"❌ File not found: {e}", file=sys.stderr)
        return 1
    except yaml.YAMLError as e:
        print(f"❌ Invalid YAML configuration: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"❌ Configuration error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
