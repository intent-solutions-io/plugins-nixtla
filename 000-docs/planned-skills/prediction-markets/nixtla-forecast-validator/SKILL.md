---
name: nixtla-forecast-validator
description: |
  Validates the quality of time series forecast metrics.
  Use when evaluating forecast accuracy, detecting performance degradation, or comparing different models.
  Trigger with "validate forecast", "check forecast quality", "assess forecast metrics".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Nixtla Forecast Validator

Validates time series forecast quality metrics and detects degradation using Nixtla's TimeGPT API and standard statistical measures.

## Purpose

Evaluates the accuracy and reliability of time series forecasts by comparing current performance against historical benchmarks.

## Overview

Analyzes forecast quality metrics such as MASE (Mean Absolute Scaled Error) and sMAPE (symmetric Mean Absolute Percentage Error). Detects significant deviations from expected performance, indicating potential model degradation or data anomalies. Outputs a report highlighting any detected issues and suggesting possible corrective actions. Use when you need automated monitoring of forecast accuracy or comparison of different forecast models.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install pandas matplotlib
```

## Instructions

### Step 1: Load data

Read historical and current forecast metrics data (MASE, sMAPE) from CSV files.

```python
import pandas as pd
import argparse
import os
import logging
from typing import Tuple, Dict
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_metrics_data(file_path: str) -> pd.DataFrame:
    """
    Loads forecast metrics data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the metrics data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise pd.errors.EmptyDataError(f"The file {file_path} is empty.")
        logging.info(f"Successfully loaded metrics data from {file_path}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except pd.errors.EmptyDataError as e:
        logging.error(str(e))
        raise
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing file {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    # Example usage (for testing purposes)
    try:
        # Create dummy CSV files for testing
        historical_data = {'model': ['model_A', 'model_B'], 'MASE': [1.2, 0.8], 'sMAPE': [0.15, 0.10]}
        current_data = {'model': ['model_A', 'model_B'], 'MASE': [1.8, 0.85], 'sMAPE': [0.18, 0.11]}

        historical_df = pd.DataFrame(historical_data)
        current_df = pd.DataFrame(current_data)

        historical_df.to_csv('historical_metrics.csv', index=False)
        current_df.to_csv('current_metrics.csv', index=False)

        historical_metrics = load_metrics_data('historical_metrics.csv')
        current_metrics = load_metrics_data('current_metrics.csv')

        print("Historical Metrics:")
        print(historical_metrics)
        print("\nCurrent Metrics:")
        print(current_metrics)

    except Exception as e:
        print(f"Error in example usage: {e}")
```

### Step 2: Configure validation parameters

Set thresholds for acceptable metric deviation and the historical baseline period.

```python
def configure_validation_parameters(mase_threshold: float = 0.2, smape_threshold: float = 0.2) -> Tuple[float, float]:
    """
    Configures the validation parameters for MASE and sMAPE thresholds.

    Args:
        mase_threshold (float): The threshold for acceptable MASE deviation (default: 0.2).
        smape_threshold (float): The threshold for acceptable sMAPE deviation (default: 0.2).

    Returns:
        Tuple[float, float]: A tuple containing the MASE and sMAPE thresholds.

    Raises:
        ValueError: If either threshold is not a positive number.
    """
    if not isinstance(mase_threshold, (int, float)) or mase_threshold <= 0:
        raise ValueError("MASE threshold must be a positive number.")
    if not isinstance(smape_threshold, (int, float)) or smape_threshold <= 0:
        raise ValueError("sMAPE threshold must be a positive number.")

    logging.info(f"Validation parameters configured: MASE threshold = {mase_threshold}, sMAPE threshold = {smape_threshold}")
    return mase_threshold, smape_threshold

if __name__ == "__main__":
    # Example usage (for testing purposes)
    try:
        mase_threshold, smape_threshold = configure_validation_parameters(mase_threshold=0.25, smape_threshold=0.15)
        print(f"MASE Threshold: {mase_threshold}")
        print(f"sMAPE Threshold: {smape_threshold}")

        # Example of invalid threshold
        try:
            configure_validation_parameters(mase_threshold=-0.1)
        except ValueError as e:
            print(f"Expected Error: {e}")

    except ValueError as e:
        print(f"Error in example usage: {e}")
```

### Step 3: Execute validation script

Run the validation script to compare current metrics against historical benchmarks.

```python
import pandas as pd
import argparse
import os
import logging
import matplotlib.pyplot as plt
from typing import Tuple, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_metrics_data(file_path: str) -> pd.DataFrame:
    """Loads forecast metrics data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise pd.errors.EmptyDataError(f"The file {file_path} is empty.")
        logging.info(f"Successfully loaded metrics data from {file_path}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except pd.errors.EmptyDataError as e:
        logging.error(str(e))
        raise
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing file {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def configure_validation_parameters(mase_threshold: float = 0.2, smape_threshold: float = 0.2) -> Tuple[float, float]:
    """Configures the validation parameters for MASE and sMAPE thresholds."""
    if not isinstance(mase_threshold, (int, float)) or mase_threshold <= 0:
        raise ValueError("MASE threshold must be a positive number.")
    if not isinstance(smape_threshold, (int, float)) or smape_threshold <= 0:
        raise ValueError("sMAPE threshold must be a positive number.")

    logging.info(f"Validation parameters configured: MASE threshold = {mase_threshold}, sMAPE threshold = {smape_threshold}")
    return mase_threshold, smape_threshold

def validate_forecast_metrics(historical_metrics: pd.DataFrame, current_metrics: pd.DataFrame,
                               mase_threshold: float, smape_threshold: float) -> Dict[str, Dict[str, float]]:
    """
    Validates forecast metrics by comparing current metrics against historical benchmarks.

    Args:
        historical_metrics (pd.DataFrame): DataFrame containing historical metrics.
        current_metrics (pd.DataFrame): DataFrame containing current metrics.
        mase_threshold (float): Threshold for acceptable MASE deviation.
        smape_threshold (float): Threshold for acceptable sMAPE deviation.

    Returns:
        Dict[str, Dict[str, float]]: A dictionary containing validation results for each model.
            The keys are model names, and the values are dictionaries containing 'MASE_increase' and 'sMAPE_increase' flags.
    """
    validation_results = {}

    # Ensure 'model' column exists in both DataFrames
    if 'model' not in historical_metrics.columns or 'model' not in current_metrics.columns:
        raise ValueError("Missing required 'model' column in metrics data.")

    # Ensure 'MASE' and 'sMAPE' columns exist in both DataFrames
    required_metrics = ['MASE', 'sMAPE']
    for metric in required_metrics:
        if metric not in historical_metrics.columns or metric not in current_metrics.columns:
            raise ValueError(f"Missing required metrics column: {metric}")

    # Merge historical and current metrics on the 'model' column
    merged_metrics = pd.merge(historical_metrics, current_metrics, on='model', suffixes=('_historical', '_current'))

    for index, row in merged_metrics.iterrows():
        model_name = row['model']
        historical_mase = row['MASE_historical']
        current_mase = row['MASE_current']
        historical_smape = row['sMAPE_historical']
        current_smape = row['sMAPE_current']

        # Calculate percentage increase
        mase_increase = (current_mase - historical_mase) / historical_mase if historical_mase != 0 else float('inf')
        smape_increase = (current_smape - historical_smape) / historical_smape if historical_smape != 0 else float('inf')

        # Check if the increase exceeds the threshold
        mase_exceeds_threshold = mase_increase > mase_threshold
        smape_exceeds_threshold = smape_increase > smape_threshold

        validation_results[model_name] = {
            'MASE_increase': mase_increase,
            'sMAPE_increase': smape_increase,
            'MASE_exceeds_threshold': mase_exceeds_threshold,
            'sMAPE_exceeds_threshold': smape_exceeds_threshold
        }

        logging.info(f"Validation results for model {model_name}: MASE increase = {mase_increase:.2f}, sMAPE increase = {smape_increase:.2f}")

    return validation_results

def generate_report(validation_results: Dict[str, Dict[str, float]], output_path: str = 'validation_report.txt') -> None:
    """
    Generates a report summarizing the validation results.

    Args:
        validation_results (Dict[str, Dict[str, float]]): A dictionary containing validation results for each model.
        output_path (str): The path to save the report (default: 'validation_report.txt').
    """
    with open(output_path, 'w') as f:
        report_lines = []
        for model_name, results in validation_results.items():
            if results['MASE_exceeds_threshold']:
                report_lines.append(f"WARNING: Significant increase in MASE detected for model {model_name}.")
            if results['sMAPE_exceeds_threshold']:
                report_lines.append(f"WARNING: Significant increase in sMAPE detected for model {model_name}.")

        if not report_lines:
            report_lines.append("Forecast validation passed. No significant degradation detected.")

        for line in report_lines:
            f.write(line + '\n')
            logging.warning(line)

    logging.info(f"Validation report generated at {output_path}")

def create_metrics_comparison_csv(historical_metrics: pd.DataFrame, current_metrics: pd.DataFrame, output_path: str = 'metrics_comparison.csv') -> None:
    """
    Creates a CSV file containing a comparison of historical and current metrics.

    Args:
        historical_metrics (pd.DataFrame): DataFrame containing historical metrics.
        current_metrics (pd.DataFrame): DataFrame containing current metrics.
        output_path (str): The path to save the CSV file (default: 'metrics_comparison.csv').
    """
    try:
        merged_metrics = pd.merge(historical_metrics, current_metrics, on='model', suffixes=('_historical', '_current'))
        merged_metrics.to_csv(output_path, index=False)
        logging.info(f"Metrics comparison CSV generated at {output_path}")
    except Exception as e:
        logging.error(f"Error creating metrics comparison CSV: {e}")
        raise

def create_alert_log(validation_results: Dict[str, Dict[str, float]], output_path: str = 'alert.log') -> None:
    """
    Creates a log file containing alerts if significant degradation is detected.

    Args:
        validation_results (Dict[str, Dict[str, float]]): A dictionary containing validation results for each model.
        output_path (str): The path to save the alert log (default: 'alert.log').
    """
    with open(output_path, 'w') as f:
        alert_lines = []
        for model_name, results in validation_results.items():
            if results['MASE_exceeds_threshold']:
                alert_lines.append(f"ALERT: Significant increase in MASE detected for model {model_name}.")
            if results['sMAPE_exceeds_threshold']:
                alert_lines.append(f"ALERT: Significant increase in sMAPE detected for model {model_name}.")

        for line in alert_lines:
            f.write(line + '\n')
            logging.warning(line)

    logging.info(f"Alert log generated at {output_path}")

def visualize_metrics(historical_metrics: pd.DataFrame, current_metrics: pd.DataFrame, output_path: str = 'metrics_visualization.png') -> None:
    """
    Visualizes historical and current metrics using bar plots.

    Args:
        historical_metrics (pd.DataFrame): DataFrame containing historical metrics.
        current_metrics (pd.DataFrame): DataFrame containing current metrics.
        output_path (str): The path to save the visualization (default: 'metrics_visualization.png').
    """
    try:
        # Ensure 'model' column exists in both DataFrames
        if 'model' not in historical_metrics.columns or 'model' not in current_metrics.columns:
            raise ValueError("Missing required 'model' column in metrics data.")

        # Ensure 'MASE' and 'sMAPE' columns exist in both DataFrames
        required_metrics = ['MASE', 'sMAPE']
        for metric in required_metrics:
            if metric not in historical_metrics.columns or metric not in current_metrics.columns:
                raise ValueError(f"Missing required metrics column: {metric}")

        # Set up the figure and axes
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

        # Plot MASE
        axes[0].bar(historical_metrics['model'], historical_metrics['MASE'], label='Historical', alpha=0.7)
        axes[0].bar(current_metrics['model'], current_metrics['MASE'], label='Current', alpha=0.7)
        axes[0].set_xlabel('Model')
        axes[0].set_ylabel('MASE')
        axes[0].set_title('MASE Comparison')
        axes[0].legend()

        # Plot sMAPE
        axes[1].bar(historical_metrics['model'], historical_metrics['sMAPE'], label='Historical', alpha=0.7)
        axes[1].bar(current_metrics['model'], current_metrics['sMAPE'], label='Current', alpha=0.7)
        axes[1].set_xlabel('Model')
        axes[1].set_ylabel('sMAPE')
        axes[1].set_title('sMAPE Comparison')
        axes[1].legend()

        # Adjust layout and save the figure
        plt.tight_layout()
        plt.savefig(output_path)
        logging.info(f"Metrics visualization saved to {output_path}")

    except Exception as e:
        logging.error(f"Error creating metrics visualization: {e}")
        raise

def main(historical_file: str, current_file: str, mase_threshold: float = 0.2, smape_threshold: float = 0.2) -> None:
    """
    Main function to execute the forecast validation process.

    Args:
        historical_file (str): Path to the historical metrics CSV file.
        current_file (str): Path to the current metrics CSV file.
        mase_threshold (float): Threshold for acceptable MASE deviation (default: 0.2).
        smape_threshold (float): Threshold for acceptable sMAPE deviation (default: 0.2).
    """
    try:
        # Load data
        historical_metrics = load_metrics_data(historical_file)
        current_metrics = load_metrics_data(current_file)

        # Configure validation parameters
        mase_threshold, smape_threshold = configure_validation_parameters(mase_threshold, smape_threshold)

        # Validate forecast metrics
        validation_results = validate_forecast_metrics(historical_metrics, current_metrics, mase_threshold, smape_threshold)

        # Generate report
        generate_report(validation_results)

        # Create metrics comparison CSV
        create_metrics_comparison_csv(historical_metrics, current_metrics)

        # Create alert log
        create_alert_log(validation_results)

        # Visualize metrics
        visualize_metrics(historical_metrics, current_metrics)

    except Exception as e:
        logging.error(f"An error occurred during the validation process: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate time series forecast quality metrics.')
    parser.add_argument('--historical', type=str, required=True, help='Path to the historical metrics CSV file.')
    parser.add_argument('--current', type=str, required=True, help='Path to the current metrics CSV file.')
    parser.add_argument('--mase_threshold', type=float, default=0.2, help='Threshold for acceptable MASE deviation.')
    parser.add_argument('--smape_threshold', type=float, default=0.2, help='Threshold for acceptable sMAPE deviation.')

    args = parser.parse_args()

    main(args.historical, args.current, args.mase_threshold, args.smape_threshold)
```

### Step 4: Generate report

Analyze the validation results and create a report highlighting any detected degradation. This is handled within the `validate_forecast.py` script.

## Output

- **validation_report.txt**: Textual report summarizing the validation results.
- **metrics_comparison.csv**: CSV file containing a comparison of historical and current metrics.
- **alert.log**: Log file containing alerts if significant degradation is detected.
- **metrics_visualization.png**: A visualization comparing historical and current metrics.

## Error Handling

1. **Error**: `Missing required metrics column (MASE or sMAPE)`
   **Solution**: Ensure input CSV files contain columns 'MASE' and 'sMAPE'.

2. **Error**: `Invalid threshold value`
   **Solution**: Provide a valid numerical threshold value for metric deviation.

3. **Error**: `Historical data unavailable`
   **Solution**: Ensure a valid historical metrics CSV file is provided.

4. **Error**: `API Key not found`
   **Solution**: Set the `NIXTLA_TIMEGPT_API_KEY` environment variable. (Not applicable in this version as TimeGPT API is not directly used)

## Examples

### Example 1: Increased MASE

**Input (historical_metrics.csv)**:
```
model,MASE,sMAPE
model_A,1.2,0.15
```

**Input (current_metrics.csv)**:
```
model,MASE,sMAPE
model_A,1.8,0.18
```

**Output (validation_report.txt)**:
```
WARNING: Significant increase in MASE detected for model model_A.
```

### Example 2: Stable performance

**Input (historical_metrics.csv)**:
```
model,MASE,sMAPE
model_B,0.8,0.10
```

**Input (current_metrics.csv)**:
```
model,MASE,sMAPE
model_B,0.85,0.11
```

**Output (validation_report.txt)**:
```
Forecast validation passed. No significant degradation detected.
```

## Usage

To validate forecast metrics, run the following command:

```bash
python validate_forecast.py --historical historical_metrics.csv --current current_metrics.csv --mase_threshold 0.3 --smape_threshold 0.25
```

Replace `historical_metrics.csv` and `current_metrics.csv` with the actual paths to your historical and current metrics files. Adjust `mase_threshold` and `smape_threshold` as needed.