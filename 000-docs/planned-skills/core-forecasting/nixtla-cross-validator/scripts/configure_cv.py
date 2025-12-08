"""
Configure cross-validation splits for time series data.

Usage:
    python configure_cv.py --help
"""
import pandas as pd
from typing import List, Tuple


def configure_cross_validation(
    df: pd.DataFrame,
    window_size: int,
    folds: int
) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Configures cross-validation splits based on expanding window.

    Args:
        df: The input DataFrame.
        window_size: The size of the validation window.
        folds: The number of folds to create.

    Returns:
        A list of tuples, where each tuple contains the training and validation DataFrames for a fold.

    Raises:
        ValueError: If window_size or folds are invalid.
        ValueError: If the DataFrame is too small for the specified window_size and folds.
    """
    if window_size <= 0:
        raise ValueError("Window size must be a positive integer.")
    if folds <= 0:
        raise ValueError("Number of folds must be a positive integer.")

    total_length = len(df)
    if total_length <= window_size * folds:
        raise ValueError("DataFrame is too small for the specified window size and number of folds.")

    splits = []
    for i in range(folds):
        train_end = total_length - (folds - i) * window_size
        val_start = train_end
        val_end = train_end + window_size

        train_df = df.iloc[:train_end].copy()
        val_df = df.iloc[val_start:val_end].copy()

        splits.append((train_df, val_df))

    return splits


if __name__ == "__main__":
    # Create a sample DataFrame for testing
    data = {'unique_id': ['store_1'] * 100,
            'ds': pd.date_range('2023-01-01', periods=100, freq='D'),
            'y': range(100)}
    df = pd.DataFrame(data)

    try:
        splits = configure_cross_validation(df, window_size=20, folds=3)
        print(f"Created {len(splits)} cross-validation splits.")
        for i, (train_df, val_df) in enumerate(splits):
            print(f"Fold {i+1}:")
            print(f"  Train data shape: {train_df.shape}")
            print(f"  Validation data shape: {val_df.shape}")
    except ValueError as e:
        print(f"Error: {e}")
