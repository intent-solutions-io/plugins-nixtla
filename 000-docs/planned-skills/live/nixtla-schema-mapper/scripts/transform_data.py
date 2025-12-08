#!/usr/bin/env python3
"""
Data transformation script to convert data to Nixtla format (unique_id, ds, y).
"""
import pandas as pd
import argparse
import logging
from typing import Optional
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_data(input_file: str) -> pd.DataFrame:
    """
    Loads data from a CSV file into a Pandas DataFrame.

    Args:
        input_file (str): The path to the input CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the input file does not exist.
        pd.errors.EmptyDataError: If the input file is empty.
        pd.errors.ParserError: If the input file cannot be parsed.
    """
    try:
        df = pd.read_csv(input_file)
        logging.info(f"Successfully loaded data from {input_file}")
        return df
    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
        raise
    except pd.errors.EmptyDataError:
        logging.error(f"Input file is empty: {input_file}")
        raise
    except pd.errors.ParserError:
        logging.error(f"Failed to parse input file: {input_file}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def infer_schema(df: pd.DataFrame) -> dict:
    """
    Infers the schema of the DataFrame, identifying the unique_id, ds, and y columns.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        dict: A dictionary containing the inferred column names for 'unique_id', 'ds', and 'y'.
              Returns None if inference fails.
    """
    potential_id_cols = []
    potential_date_cols = []
    potential_target_cols = []

    for col in df.columns:
        if df[col].dtype == 'object':
            if df[col].nunique() == len(df):
                potential_id_cols.append(col)
            try:
                pd.to_datetime(df[col].iloc[0])
                potential_date_cols.append(col)
            except ValueError:
                pass
        elif pd.api.types.is_numeric_dtype(df[col]):
            potential_target_cols.append(col)

    if potential_id_cols and potential_date_cols and potential_target_cols:
        return {
            'unique_id': potential_id_cols[0],
            'ds': potential_date_cols[0],
            'y': potential_target_cols[0]
        }
    else:
        return None


def transform_data(
    df: pd.DataFrame,
    id_col: Optional[str] = None,
    date_col: Optional[str] = None,
    target_col: Optional[str] = None,
    date_format: Optional[str] = None
) -> pd.DataFrame:
    """
    Transforms the input DataFrame into the Nixtla format (unique_id, ds, y).

    Args:
        df (pd.DataFrame): The input DataFrame.
        id_col (str, optional): The name of the unique ID column. Defaults to None.
        date_col (str, optional): The name of the date column. Defaults to None.
        target_col (str, optional): The name of the target column. Defaults to None.
        date_format (str, optional): The format of the date column. Defaults to None.

    Returns:
        pd.DataFrame: The transformed DataFrame in Nixtla format.

    Raises:
        ValueError: If the schema cannot be inferred and column mappings are not provided.
        ValueError: If the date column cannot be parsed.
        ValueError: If there are missing values in the target column.
    """
    try:
        if not id_col or not date_col or not target_col:
            inferred_schema = infer_schema(df.copy())
            if inferred_schema:
                id_col = inferred_schema['unique_id']
                date_col = inferred_schema['ds']
                target_col = inferred_schema['y']
                logging.info("Successfully inferred schema.")
            else:
                raise ValueError("Could not infer mapping. Specify column mappings using --id_col, --date_col, --target_col arguments.")

        df = df.rename(columns={id_col: 'unique_id', date_col: 'ds', target_col: 'y'})

        if date_format:
            df['ds'] = pd.to_datetime(df['ds'], format=date_format)
        else:
            df['ds'] = pd.to_datetime(df['ds'], infer_datetime_format=True)

        if df['y'].isnull().any():
            raise ValueError("Missing values in target column. Handle missing values before running the script.")

        logging.info("Data transformation complete.")
        return df[['unique_id', 'ds', 'y']]

    except ValueError as e:
        logging.error(f"Error during data transformation: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def visualize_data(df: pd.DataFrame, output_file: str) -> None:
    """
    Visualizes the time series data and saves the plot to a file.

    Args:
        df (pd.DataFrame): The transformed DataFrame in Nixtla format.
        output_file (str): The path to save the visualization.
    """
    try:
        unique_ids = df['unique_id'].unique()
        if len(unique_ids) > 5:
            logging.warning("Too many unique IDs to visualize.  Visualizing only the first 5.")
            unique_ids = unique_ids[:5]

        for unique_id in unique_ids:
            subset = df[df['unique_id'] == unique_id].set_index('ds')['y']
            plt.figure(figsize=(12, 6))
            plt.plot(subset)
            plt.title(f"Time Series for {unique_id}")
            plt.xlabel("Date")
            plt.ylabel("Target Value")
            plt.grid(True)
            plt.savefig(f"{output_file.replace('.csv', '')}_{unique_id}.png")
            plt.close()
            logging.info(f"Visualization saved for {unique_id} to {output_file.replace('.csv', '')}_{unique_id}.png")

    except Exception as e:
        logging.error(f"Error during visualization: {e}")
        print(f"Error during visualization: {e}")


def main(input_file: str, output_file: str, id_col: Optional[str], date_col: Optional[str], target_col: Optional[str], date_format: Optional[str]) -> None:
    """
    Main function to load, transform, and save data in Nixtla format.

    Args:
        input_file (str): The path to the input CSV file.
        output_file (str): The path to the output CSV file.
        id_col (str, optional): The name of the unique ID column.
        date_col (str, optional): The name of the date column.
        target_col (str, optional): The name of the target column.
        date_format (str, optional): The format of the date column.
    """
    try:
        df = load_data(input_file)
        transformed_df = transform_data(df, id_col, date_col, target_col, date_format)
        transformed_df.to_csv(output_file, index=False)
        logging.info(f"Transformed data saved to {output_file}")
        visualize_data(transformed_df, output_file)

    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform data into Nixtla format.")
    parser.add_argument("--input", required=True, help="Path to the input CSV file.")
    parser.add_argument("--output", required=True, help="Path to the output CSV file.")
    parser.add_argument("--id_col", help="Name of the unique ID column.")
    parser.add_argument("--date_col", help="Name of the date column.")
    parser.add_argument("--target_col", help="Name of the target column.")
    parser.add_argument("--date_format", help="Format of the date column (e.g., '%Y-%m-%d').")

    args = parser.parse_args()

    main(args.input, args.output, args.id_col, args.date_col, args.target_col, args.date_format)
