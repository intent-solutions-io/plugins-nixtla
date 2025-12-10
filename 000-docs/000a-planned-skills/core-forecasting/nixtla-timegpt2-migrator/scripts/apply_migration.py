"""
Apply TimeGPT-2 migration changes to codebase.

Usage:
    python apply_migration.py [file_to_modify]
"""
import os
import re
import sys
from typing import List, Tuple


def replace_timegpt1_calls(file_path: str, replacements: List[Tuple[str, str]]) -> bool:
    """
    Replaces TimeGPT-1 API calls with TimeGPT-2 compatible calls in a file.

    Args:
        file_path: The path to the file to modify.
        replacements: A list of tuples, where each tuple contains the old and new code snippets.

    Returns:
        True if the file was successfully modified, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        for old, new in replacements:
            content = content.replace(old, new)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Successfully updated file: {file_path}")
        return True
    except Exception as e:
        print(f"Error updating file {file_path}: {e}")
        return False


def update_data_schema(file_path: str) -> bool:
    """
    Updates the data schema conversion code to match TimeGPT-2 requirements.

    Args:
        file_path: The path to the file containing the data schema conversion code.

    Returns:
        True if the file was successfully modified, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Example: Replace old data loading with new data loading
        old_data_loading = "data = load_timegpt1_data()"
        new_data_loading = """# Load data and ensure correct format for Nixtla
data = load_data()
data['ds'] = pd.to_datetime(data['ds'])
data = data.rename(columns={'series_id': 'unique_id', 'timestamp': 'ds', 'value': 'y'})"""

        content = content.replace(old_data_loading, new_data_loading)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Successfully updated data schema conversion in file: {file_path}")
        return True
    except Exception as e:
        print(f"Error updating data schema conversion in file {file_path}: {e}")
        return False


def remove_training_code(file_path: str) -> bool:
    """
    Removes TimeGPT-1 training code from the file.

    Args:
        file_path: The path to the file containing the training code.

    Returns:
        True if the file was successfully modified, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Example: Remove training-related code blocks
        content = re.sub(r"def train_model\(.*\):\n    .*?(?=\n\n)", "", content, flags=re.DOTALL)
        content = re.sub(r"model\.train\(.*\)", "", content)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Successfully removed training code from file: {file_path}")
        return True
    except Exception as e:
        print(f"Error removing training code from file {file_path}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python apply_migration.py <file_to_modify>")
        sys.exit(1)

    file_to_modify = sys.argv[1]

    # Define replacements for TimeGPT-1 API calls
    replacements = [
        ("timegpt.forecast(data, h=24)", "client.forecast(df=data, h=24, freq='H')"),
        ("timegpt.create_model()", "# Model creation is not needed in TimeGPT-2"),
        ("from timegpt import TimeGPT", "from nixtla import NixtlaClient"),
        ("timegpt = TimeGPT()", "client = NixtlaClient(api_key=os.getenv('NIXTLA_TIMEGPT_API_KEY'))"),
    ]

    # Apply the replacements
    replace_timegpt1_calls(file_to_modify, replacements)

    # Update the data schema conversion code
    # update_data_schema(file_to_modify)

    # Remove training code
    # remove_training_code(file_to_modify)

    print("Migration changes applied. Review the modified file for correctness.")
