"""
Check compatibility between TimeGPT-1 usage and TimeGPT-2 requirements.

Usage:
    python compatibility_check.py --data sample_data.csv
"""
import pandas as pd
import os
import argparse
from typing import List, Tuple


def check_timegpt1_api_availability(api_key: str) -> bool:
    """
    Checks if the TimeGPT-1 API is accessible (simulated).

    Args:
        api_key: The TimeGPT API key.

    Returns:
        True if the API is considered accessible, False otherwise.
    """
    print("Simulating TimeGPT-1 API availability check...")
    return True  # Assume the API is available for this example


def validate_data_schema(df: pd.DataFrame) -> bool:
    """
    Validates the data schema for compatibility with TimeGPT-2.
    Checks for required columns ('unique_id', 'ds', 'y') and data types.

    Args:
        df: The input pandas DataFrame.

    Returns:
        True if the schema is valid, False otherwise.
    """
    required_columns = ['unique_id', 'ds', 'y']
    if not all(col in df.columns for col in required_columns):
        print("Error: Missing required columns in the DataFrame.")
        return False

    if not pd.api.types.is_datetime64_any_dtype(df['ds']):
        print("Error: 'ds' column must be of datetime type.")
        return False

    if not pd.api.types.is_numeric_dtype(df['y']):
        print("Error: 'y' column must be numeric.")
        return False

    print("Data schema validation successful.")
    return True


def identify_unsupported_features(codebase_analysis: List[Tuple[str, str]]) -> List[str]:
    """
    Identifies unsupported TimeGPT-1 features in the codebase.

    Args:
        codebase_analysis: A list of tuples containing file paths and matched code snippets.

    Returns:
        A list of unsupported features found in the codebase.
    """
    unsupported_features = []
    for file_path, match in codebase_analysis:
        if "timegpt.train(" in match:
            unsupported_features.append("timegpt.train() (Training is handled differently in TimeGPT-2)")
        if "timegpt.create_model(" in match:
            unsupported_features.append("timegpt.create_model() (Model creation not needed in TimeGPT-2)")
    return list(set(unsupported_features))  # Remove duplicates


def generate_migration_plan(data_schema_valid: bool, unsupported_features: List[str], output_file: str = "migration_report.txt") -> None:
    """
    Generates a migration plan based on the compatibility check results.

    Args:
        data_schema_valid: True if the data schema is valid, False otherwise.
        unsupported_features: A list of unsupported features found in the codebase.
        output_file: The path to the output migration plan file.
    """
    with open(output_file, "w") as f:
        f.write("TimeGPT-1 to TimeGPT-2 Migration Plan\n")
        f.write("--------------------------------------\n\n")

        if not data_schema_valid:
            f.write("ERROR: Incompatible data schema. Update data input format to match TimeGPT-2 requirements.\n\n")
        else:
            f.write("Data schema is compatible.\n\n")

        if unsupported_features:
            f.write("Unsupported TimeGPT-1 Features:\n")
            for feature in unsupported_features:
                f.write(f"- {feature}\n")
            f.write("\nRefactor code to use equivalent TimeGPT-2 functionality or alternative approaches.\n")
        else:
            f.write("No unsupported TimeGPT-1 features found.\n")

        f.write("\nConsider reviewing the Nixtla documentation for TimeGPT-2 for detailed migration instructions.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check TimeGPT-1 to TimeGPT-2 compatibility.')
    parser.add_argument('--data', required=True, help='Path to sample data CSV for schema validation')
    parser.add_argument('--analysis', required=False, default='analysis_report.txt',
                        help='Path to codebase analysis report')

    args = parser.parse_args()

    # Load sample data for schema validation
    try:
        df = pd.read_csv(args.data)
        df['ds'] = pd.to_datetime(df['ds'])
    except Exception as e:
        print(f"Error loading data: {e}")
        exit(1)

    # Check API availability
    api_key = os.getenv('NIXTLA_TIMEGPT_API_KEY')
    if not api_key:
        print("Warning: NIXTLA_TIMEGPT_API_KEY environment variable not set.")
    else:
        api_available = check_timegpt1_api_availability(api_key)
        if not api_available:
            print("Error: TimeGPT-1 API endpoint not found. Ensure TimeGPT-1 API is accessible.")

    # Validate data schema
    data_schema_valid = validate_data_schema(df)

    # Simulate codebase analysis (would normally read from analysis_report.txt)
    codebase_analysis_results = [("main.py", "timegpt.train(data)"), ("utils.py", "timegpt.forecast(data, h=24)")]

    # Identify unsupported features
    unsupported_features = identify_unsupported_features(codebase_analysis_results)

    # Generate migration plan
    generate_migration_plan(data_schema_valid, unsupported_features)

    print("Compatibility check complete. See migration_report.txt for details.")
