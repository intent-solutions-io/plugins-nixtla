"""
Load historical time series and exogenous variables from CSV files.

Usage:
    python load_data.py historical.csv [exogenous.csv]
"""

from typing import Optional, Tuple

import pandas as pd


def load_data(
    input_file: str, exogenous_file: Optional[str] = None
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """
    Loads historical time series data and exogenous variables from CSV files.

    Args:
        input_file: Path to the historical time series CSV file.
        exogenous_file: Optional path to the exogenous variables CSV file.

    Returns:
        A tuple containing the historical data DataFrame and the exogenous data DataFrame (or None if not provided).

    Raises:
        FileNotFoundError: If either of the specified files does not exist.
        ValueError: If the input data does not conform to the expected schema.
    """
    try:
        df = pd.read_csv(input_file)
        df["ds"] = pd.to_datetime(df["ds"])
    except FileNotFoundError:
        raise FileNotFoundError(f"Historical data file not found: {input_file}")
    except KeyError:
        raise ValueError("Historical data must contain 'unique_id', 'ds', and 'y' columns.")
    except Exception as e:
        raise ValueError(f"Error reading historical data: {e}")

    if exogenous_file:
        try:
            exog_df = pd.read_csv(exogenous_file)
            exog_df["ds"] = pd.to_datetime(exog_df["ds"])
        except FileNotFoundError:
            raise FileNotFoundError(f"Exogenous data file not found: {exogenous_file}")
        except KeyError:
            raise ValueError("Exogenous data must contain a 'ds' column.")
        except Exception as e:
            raise ValueError(f"Error reading exogenous data: {e}")
    else:
        exog_df = None

    return df, exog_df


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python load_data.py <historical_file> [exogenous_file]")
        sys.exit(1)

    try:
        exog_file = sys.argv[2] if len(sys.argv) > 2 else None
        historical_data, exogenous_data = load_data(sys.argv[1], exog_file)

        print("Historical data loaded successfully:")
        print(historical_data.head())

        if exogenous_data is not None:
            print("\nExogenous data loaded successfully:")
            print(exogenous_data.head())
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
