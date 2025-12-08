#!/usr/bin/env python3
"""
Usage report generator for Nixtla usage optimization.
"""
import os
import json
from typing import Dict, Any, List
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_report(usage_patterns: Dict[str, Any], recommendations: List[str], output_dir: str = ".") -> None:
    """
    Generates a report with current usage statistics and optimization recommendations.

    Args:
        usage_patterns: A dictionary containing API usage statistics and patterns.
        recommendations: A list of strings, where each string is a recommendation.
        output_dir: The directory to save the report files. Defaults to the current directory.
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Usage Report
        usage_report_path = os.path.join(output_dir, 'usage_report.txt')
        with open(usage_report_path, 'w') as f:
            f.write("API Usage Report\n")
            f.write("----------------\n\n")

            if usage_patterns:
                for key, value in usage_patterns.items():
                    f.write(f"{key.replace('_', ' ').title()}:\n")
                    if isinstance(value, dict):
                        for k, v in value.items():
                            f.write(f"  - {k}: {v}\n")
                    else:
                        f.write(f"  - {value}\n")
                    f.write("\n")
            else:
                f.write("No usage data available.\n")

        # Optimization Recommendations Report
        recommendations_path = os.path.join(output_dir, 'optimization_recommendations.txt')
        with open(recommendations_path, 'w') as f:
            f.write("Optimization Recommendations\n")
            f.write("---------------------------\n\n")

            if recommendations:
                for i, recommendation in enumerate(recommendations):
                    f.write(f"{i+1}. {recommendation}\n")
            else:
                f.write("No recommendations available.\n")

        # Potential Savings Report (Placeholder)
        savings_path = os.path.join(output_dir, 'potential_savings.txt')
        with open(savings_path, 'w') as f:
            f.write("Potential Savings Estimate\n")
            f.write("--------------------------\n\n")
            f.write("This section requires further implementation to calculate potential cost savings based on the recommendations.\n")
            f.write("Currently, no savings estimates are available.\n")

        logging.info(f"Successfully generated reports in {output_dir}")

    except Exception as e:
        logging.error(f"An error occurred while generating reports: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate usage optimization reports.")
    parser.add_argument("--usage_patterns", required=True, help="Path to usage patterns JSON file.")
    parser.add_argument("--recommendations", required=True, help="Path to recommendations JSON file.")
    parser.add_argument("--output_dir", default="reports", help="Directory to save reports.")

    args = parser.parse_args()

    try:
        with open(args.usage_patterns, 'r') as f:
            usage_patterns = json.load(f)
        with open(args.recommendations, 'r') as f:
            recommendations = json.load(f)

        generate_report(usage_patterns, recommendations, args.output_dir)
        print(f"Reports generated in the '{args.output_dir}' directory.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
