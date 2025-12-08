"""
Load time series data from CSV file.

Usage:
    python load_data.py data.csv
"""
import pandas as pd
from typing import Tuple


def load_data(input_file: str) -> pd.DataFrame:
    """
    Loads time series data from a CSV file.

    Args:
        input_file: Path to the CSV file.

    Returns:
        A pandas DataFrame containing the time series data.

    Raises:
        FileNotFoundError: If the input file does not exist.
        pd.errors.EmptyDataError: If the input file is empty.
        pd.errors.ParserError: If the input file has parsing issues.
    """
    try:
        df = pd.read_csv(input_file)
        if df.empty:
            raise pd.errors.EmptyDataError(f"The input file {input_file} is empty.")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_file}")
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Error parsing the input file {input_file}: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while loading data: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python load_data.py <input_file>")
        sys.exit(1)

    try:
        data = load_data(sys.argv[1])
        print("Data loaded successfully.")
        print(data.head())
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except pd.errors.ParserError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
