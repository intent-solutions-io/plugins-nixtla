#!/usr/bin/env python3
"""
Detect Nixtla Environment

Detects installed Nixtla libraries and their versions. Checks for:
- statsforecast
- mlforecast
- nixtla (TimeGPT client)
- utilsforecast
- NIXTLA_API_KEY environment variable

Usage:
    python detect_environment.py
    python detect_environment.py --json
"""

import argparse
import importlib.metadata
import json
import os
import sys
from typing import Dict, List, Optional


def get_package_version(package_name: str) -> Optional[str]:
    """
    Get the installed version of a Python package.

    Args:
        package_name: Name of the package to check

    Returns:
        Version string if installed, None otherwise
    """
    try:
        version = importlib.metadata.version(package_name)
        return version
    except importlib.metadata.PackageNotFoundError:
        return None


def check_api_key() -> Dict[str, any]:
    """
    Check if NIXTLA_API_KEY environment variable is set.

    Returns:
        Dictionary with API key status
    """
    api_key = os.environ.get("NIXTLA_API_KEY")

    return {
        "configured": api_key is not None,
        "value": "***" + api_key[-4:] if api_key and len(api_key) >= 4 else None,
    }


def detect_nixtla_libraries() -> Dict[str, Optional[str]]:
    """
    Detect all Nixtla-related libraries and their versions.

    Returns:
        Dictionary mapping library names to versions (or None if not installed)
    """
    libraries = ["statsforecast", "mlforecast", "nixtla", "utilsforecast"]

    return {lib: get_package_version(lib) for lib in libraries}


def format_text_output(libraries: Dict[str, Optional[str]], api_key_info: Dict[str, any]) -> str:
    """
    Format detection results as human-readable text.

    Args:
        libraries: Dictionary of library versions
        api_key_info: API key configuration status

    Returns:
        Formatted text output
    """
    output_lines = ["Nixtla Environment Detection", "=" * 40, ""]

    # Library versions
    output_lines.append("Installed Libraries:")
    installed_count = 0
    for lib, version in libraries.items():
        if version:
            output_lines.append(f"  ✓ {lib}: {version}")
            installed_count += 1
        else:
            output_lines.append(f"  ✗ {lib}: Not installed")

    output_lines.append("")

    # API Key status
    output_lines.append("API Configuration:")
    if api_key_info["configured"]:
        masked_value = api_key_info["value"] or "***"
        output_lines.append(f"  ✓ NIXTLA_API_KEY: Configured ({masked_value})")
    else:
        output_lines.append("  ✗ NIXTLA_API_KEY: Not set")

    output_lines.append("")

    # Summary
    output_lines.append("Summary:")
    output_lines.append(f"  {installed_count}/4 Nixtla libraries installed")

    if installed_count == 0:
        output_lines.append("")
        output_lines.append("Installation:")
        output_lines.append("  pip install statsforecast mlforecast nixtla utilsforecast")

    return "\n".join(output_lines)


def format_json_output(libraries: Dict[str, Optional[str]], api_key_info: Dict[str, any]) -> str:
    """
    Format detection results as JSON.

    Args:
        libraries: Dictionary of library versions
        api_key_info: API key configuration status

    Returns:
        JSON string
    """
    installed_libs = {k: v for k, v in libraries.items() if v is not None}
    missing_libs = [k for k, v in libraries.items() if v is None]

    result = {
        "libraries": libraries,
        "api_key": api_key_info,
        "summary": {
            "installed_count": len(installed_libs),
            "total_count": len(libraries),
            "missing": missing_libs,
        },
    }

    return json.dumps(result, indent=2)


def main() -> int:
    """
    Main entry point for the script.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Detect installed Nixtla libraries and API configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                 # Human-readable output
  %(prog)s --json          # JSON output

Checks for:
  - statsforecast: Statistical forecasting models
  - mlforecast: Machine learning forecasting
  - nixtla: TimeGPT API client
  - utilsforecast: Utility functions
  - NIXTLA_API_KEY: Environment variable
        """,
    )

    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    try:
        # Detect libraries and API key
        libraries = detect_nixtla_libraries()
        api_key_info = check_api_key()

        # Format and print output
        if args.json:
            output = format_json_output(libraries, api_key_info)
        else:
            output = format_text_output(libraries, api_key_info)

        print(output)

        # Exit with non-zero if no libraries installed
        installed_count = sum(1 for v in libraries.values() if v is not None)
        return 0 if installed_count > 0 else 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
