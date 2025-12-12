"""
Generate forecasts using StatsForecast for uncertainty quantification.

Usage:
    python generate_forecasts.py --input data.csv --output forecast.csv
"""

import argparse

import pandas as pd
from sklearn.model_selection import train_test_split
from statsforecast import StatsForecast
from statsforecast.models import AutoETS


def generate_forecasts(input_file: str, output_file: str) -> None:
    """
    Generates forecasts using StatsForecast and saves them to a CSV file.

    Args:
        input_file (str): Path to the input CSV file containing historical data.
        output_file (str): Path to the output CSV file to save the forecasts.
    """
    try:
        # Load the data
        df = pd.read_csv(input_file)

        # Ensure correct data types
        df["ds"] = pd.to_datetime(df["ds"])

        # Split data into training and validation sets
        train_df, val_df = train_test_split(df, test_size=0.2, shuffle=False)

        # Define the forecasting model
        sf = StatsForecast(
            models=[AutoETS(season_length=7)],  # Example: AutoETS with weekly seasonality
            freq="D",  # Daily frequency
            n_jobs=-1,  # Use all available cores
        )

        # Train the model
        sf.fit(train_df)

        # Generate forecasts for the validation set
        forecasts = sf.predict(h=len(val_df))

        # Merge forecasts with the validation data
        forecasts = forecasts.reset_index()
        val_df = val_df.reset_index(drop=True)
        forecasts["ds"] = val_df["ds"]
        forecasts["unique_id"] = val_df["unique_id"]
        forecasts["y"] = val_df["y"]

        # Rename the forecast column to 'StatsForecast'
        forecasts = forecasts.rename(columns={"AutoETS": "StatsForecast"})

        # Select and reorder columns for the output file
        forecasts = forecasts[["unique_id", "ds", "y", "StatsForecast"]]

        # Save the forecasts to a CSV file
        forecasts.to_csv(output_file, index=False)

        print(f"Forecasts saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate forecasts using StatsForecast.")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", required=True, help="Path to output CSV file")

    args = parser.parse_args()

    generate_forecasts(input_file=args.input, output_file=args.output)
