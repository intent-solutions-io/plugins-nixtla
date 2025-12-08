#!/usr/bin/env python3
"""
Cost optimization recommendations generator for Nixtla usage.
"""
import json
from typing import Dict, Any, List
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_recommendations(usage_patterns: Dict[str, Any], api_config: Dict[str, Any]) -> List[str]:
    """
    Generates cost optimization recommendations based on usage patterns and API configuration.

    Args:
        usage_patterns: A dictionary containing API usage statistics and patterns.
        api_config: A dictionary containing the API configuration.

    Returns:
        A list of strings, where each string is a recommendation.
    """
    recommendations: List[str] = []

    if not usage_patterns:
        logging.warning("Usage patterns are empty. Cannot generate recommendations.")
        return ["Insufficient data for generating recommendations."]

    try:
        # High latency routing recommendation
        if 'region_usage' in usage_patterns and api_config.get('regions'):
            region_usage = usage_patterns['region_usage']
            api_regions = api_config['regions']

            for region, count in region_usage.items():
                if region not in api_regions:
                    recommendations.append(f"Consider adding a server in the {region} region to reduce latency and costs.")

        # Unnecessary API calls recommendation
        if 'endpoint_usage' in usage_patterns:
            endpoint_usage = usage_patterns['endpoint_usage']
            total_calls = sum(endpoint_usage.values())
            for endpoint, count in endpoint_usage.items():
                if count / total_calls > 0.3:
                    recommendations.append(f"Optimize usage of the {endpoint} endpoint. Consider caching results or reducing call frequency.")

        # Configuration-based recommendations
        if api_config.get('caching_enabled') is False:
            recommendations.append("Enable caching to reduce redundant API calls.")

        if api_config.get('data_retention_policy') == 'unlimited':
            recommendations.append("Review data retention policy to reduce storage costs.")

        logging.info("Successfully generated cost optimization recommendations.")
        return recommendations

    except Exception as e:
        logging.error(f"An error occurred while generating recommendations: {e}")
        return ["An error occurred while generating recommendations."]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate cost optimization recommendations.")
    parser.add_argument("--usage_patterns", required=True, help="Path to usage patterns JSON file.")
    parser.add_argument("--api_config", required=True, help="Path to API config JSON file.")

    args = parser.parse_args()

    try:
        with open(args.usage_patterns, 'r') as f:
            usage_patterns = json.load(f)
        with open(args.api_config, 'r') as f:
            api_config = json.load(f)

        recommendations = generate_recommendations(usage_patterns, api_config)

        if recommendations:
            print("Cost Optimization Recommendations:")
            for recommendation in recommendations:
                print(f"- {recommendation}")
        else:
            print("No recommendations generated.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
