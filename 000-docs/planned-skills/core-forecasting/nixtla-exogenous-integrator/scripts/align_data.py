"""
Merge historical and exogenous dataframes based on the 'ds' column.

Usage:
    python align_data.py
"""
import pandas as pd
from typing import Optional


def align_data(df: pd.DataFrame, exog_df: Optional[pd.DataFrame]) -> pd.DataFrame:
    """
    Merges historical and exogenous dataframes based on the 'ds' column.

    Args:
        df: Historical data DataFrame.
        exog_df: Exogenous data DataFrame (or None if no exogenous data).

    Returns:
        A merged DataFrame containing both historical and exogenous data.

    Raises:
        ValueError: If the 'ds' column is missing in either DataFrame or if there are overlapping column names
                    (excluding 'ds', 'unique_id', and 'y').
    """
    if exog_df is None:
        return df

    if 'ds' not in df.columns or 'ds' not in exog_df.columns:
        raise ValueError("Both historical and exogenous dataframes must have a 'ds' column.")

    common_columns = set(df.columns) & set(exog_df.columns)
    if len(common_columns - {'ds', 'unique_id', 'y'}) > 0:
        raise ValueError(f"Overlapping column names (excluding 'ds', 'unique_id', and 'y') found in both dataframes: {common_columns - {'ds', 'unique_id', 'y'}}")

    merged_df = pd.merge(df, exog_df, on='ds', how='left')
    return merged_df


if __name__ == "__main__":
    # Example usage
    data = {'unique_id': ['store_1', 'store_1', 'store_1'],
            'ds': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'y': [100, 120, 130]}
    historical_df = pd.DataFrame(data)

    exogenous_data = {'ds': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-04']),
                      'holiday': ['New Year', None, 'Something']}
    exogenous_df = pd.DataFrame(exogenous_data)

    try:
        aligned_df = align_data(historical_df, exogenous_df)
        print("Aligned data:")
        print(aligned_df)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
