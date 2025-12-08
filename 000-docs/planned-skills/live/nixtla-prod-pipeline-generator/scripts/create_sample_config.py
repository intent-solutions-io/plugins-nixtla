#!/usr/bin/env python3
"""
Sample configuration file creator for Nixtla production pipelines.
"""
import yaml
import argparse


def create_sample_config(filename: str = 'experiment.yaml') -> None:
    """
    Creates a sample experiment configuration file in YAML format.

    Args:
        filename: The name of the file to create.
    """
    config = {
        'pipeline_name': 'my_forecasting_pipeline',
        'model_type': 'TimeGPT',  # or 'StatsForecast'
        'data_location': 'data.csv',
        'frequency': 'D',
        'horizon': 14
    }

    with open(filename, 'w') as f:
        yaml.dump(config, f, indent=4)

    print(f"Sample configuration file created: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create sample experiment configuration.")
    parser.add_argument("--output", default="experiment.yaml", help="Output filename for sample config.")
    args = parser.parse_args()

    create_sample_config(args.output)
