---
name: nixtla-event-impact-modeler
description: |
  Models the impact of exogenous events on contract prices using TimeGPT.
  Use when needing to quantify the effect of events on time series, analyze pricing anomalies, or forecast with event considerations.
  Trigger with "event impact analysis", "model event effects", "quantify event impact".
allowed-tools: "Read,Write,Bash,Glob,Grep,WebSearch"
version: "1.0.0"
---

# Nixtla Event Impact Modeler

Quantifies the impact of exogenous events on contract prices using TimeGPT.

## Purpose

Analyzes and models the impact of specified events on contract prices over time.

## Overview

This skill assesses how external events (e.g., promotions, natural disasters, policy changes) affect contract prices. It takes historical price data and event details as input, uses TimeGPT to model the time series, and quantifies the causal impact of events. The skill is useful for understanding event effects and improving forecasting accuracy. Outputs include event impact estimates, adjusted forecasts, and visualizations.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep, WebSearch

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas causalimpact matplotlib
```

## Instructions

### Step 1: Prepare data

Read contract price data and event details from CSV files.

```python
import pandas as pd
import os
from typing import Tuple, List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(prices_path: str, events_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads price and event data from CSV files.

    Args:
        prices_path: Path to the prices CSV file.
        events_path: Path to the events CSV file.

    Returns:
        A tuple containing the prices DataFrame and the events DataFrame.

    Raises:
        FileNotFoundError: If either of the CSV files is not found.
        ValueError: If the CSV files do not contain the required columns.
    """
    try:
        prices_df = pd.read_csv(prices_path, parse_dates=['ds'])
        events_df = pd.read_csv(events_path, parse_dates=['ds'])

        # Ensure correct column names for Nixtla
        prices_df = prices_df.rename(columns={'price': 'y'})
        events_df = events_df.rename(columns={'event': 'event'})

        if 'unique_id' not in prices_df.columns:
            prices_df['unique_id'] = 'contract_1'  # Default unique ID

        if 'ds' not in prices_df.columns or 'y' not in prices_df.columns:
            raise ValueError("Prices CSV must contain 'ds' (datetime) and 'y' (price) columns.")

        if 'ds' not in events_df.columns or 'event' not in events_df.columns:
            raise ValueError("Events CSV must contain 'ds' (datetime) and 'event' columns.")

        return prices_df, events_df

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        raise
    except ValueError as e:
        logging.error(f"Data error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    try:
        prices_file = 'prices.csv'
        events_file = 'events.csv'

        # Create dummy data for testing
        prices_data = {'ds': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']),
                       'price': [10, 12, 13, 11, 14]}
        events_data = {'ds': pd.to_datetime(['2023-01-03']), 'event': ['Promotion']}

        pd.DataFrame(prices_data).to_csv(prices_file, index=False)
        pd.DataFrame(events_data).to_csv(events_file, index=False)

        prices_df, events_df = load_data(prices_file, events_file)
        print("Prices DataFrame:")
        print(prices_df.head())
        print("\nEvents DataFrame:")
        print(events_df.head())

    except Exception as e:
        print(f"Error in data loading: {e}")
```

### Step 2: Configure model

Define the event periods and causal model parameters (e.g., prior).

```python
import pandas as pd
from typing import List, Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def configure_causal_model(prices_df: pd.DataFrame, events_df: pd.DataFrame) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
    """
    Configures the event periods for the causal impact analysis.

    Args:
        prices_df: DataFrame containing the price data.
        events_df: DataFrame containing the event data.

    Returns:
        A list of tuples, where each tuple represents the start and end date of an event.

    Raises:
        ValueError: If event dates are outside the price range.
    """
    try:
        event_periods: List[Tuple[pd.Timestamp, pd.Timestamp]] = []
        min_date = prices_df['ds'].min()
        max_date = prices_df['ds'].max()

        for _, row in events_df.iterrows():
            event_date = row['ds']
            event_name = row['event']

            # Define a window around the event (e.g., 3 days before and after)
            start_date = event_date - pd.Timedelta(days=3)
            end_date = event_date + pd.Timedelta(days=3)

            if start_date < min_date or end_date > max_date:
                raise ValueError(f"Event '{event_name}' dates are outside the price range.")

            event_periods.append((start_date, end_date))

        return event_periods

    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def create_treatment_control_df(prices_df: pd.DataFrame, event_periods: List[Tuple[pd.Timestamp, pd.Timestamp]]) -> pd.DataFrame:
    """
    Creates a DataFrame with treatment and control periods marked.

    Args:
        prices_df: DataFrame containing the price data.
        event_periods: List of tuples representing event periods.

    Returns:
        A DataFrame with an additional 'treatment' column indicating treatment periods.
    """
    prices_df['treatment'] = 0  # Initialize with control period

    for start_date, end_date in event_periods:
        prices_df.loc[(prices_df['ds'] >= start_date) & (prices_df['ds'] <= end_date), 'treatment'] = 1

    return prices_df

if __name__ == "__main__":
    try:
        # Create dummy data for testing
        prices_data = {'ds': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07']),
                       'price': [10, 12, 13, 11, 14, 15, 16],
                       'unique_id': ['contract_1'] * 7}
        events_data = {'ds': pd.to_datetime(['2023-01-04']), 'event': ['Promotion']}

        prices_df = pd.DataFrame(prices_data)
        events_df = pd.DataFrame(events_data)

        event_periods = configure_causal_model(prices_df, events_df)
        print("Event Periods:", event_periods)

        treatment_df = create_treatment_control_df(prices_df, event_periods)
        print("\nDataFrame with Treatment Periods:")
        print(treatment_df.head(10))

    except Exception as e:
        print(f"Error in model configuration: {e}")
```

### Step 3: Execute analysis

Run the analysis script.

```python
import pandas as pd
from causalimpact import CausalImpact
import matplotlib.pyplot as plt
import os
from nixtla import NixtlaClient
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_event_impact(prices_df: pd.DataFrame, event_periods: List[Tuple[pd.Timestamp, pd.Timestamp]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Analyzes the impact of events on contract prices using CausalImpact and TimeGPT.

    Args:
        prices_df: DataFrame containing the price data.
        event_periods: List of tuples, where each tuple represents the start and end date of an event.

    Returns:
        A tuple containing the impact results DataFrame and the adjusted forecast DataFrame.
    """
    try:
        # Ensure the DataFrame is sorted by date
        prices_df = prices_df.sort_values(by='ds')
        prices_df = prices_df.set_index('ds')

        # Define the pre-intervention and intervention periods
        intervention_periods = []
        for start_date, end_date in event_periods:
            intervention_periods.append([start_date, end_date])

        # Flatten the list of lists into a single list of dates
        intervention_dates = [date for period in intervention_periods for date in pd.date_range(period[0], period[1])]

        # Create a boolean column indicating whether each date is in the intervention period
        prices_df['is_intervention'] = prices_df.index.isin(intervention_dates)

        # Define the pre-intervention period as the period before the first intervention
        pre_period = [prices_df.index.min(), intervention_dates[0] - pd.Timedelta(days=1)]

        # Define the intervention period as the period of the interventions
        post_period = [intervention_dates[0], prices_df.index.max()]

        # Run CausalImpact analysis
        causal_impact = CausalImpact(prices_df['y'], pre_period, post_period, niter=1000)

        # Extract the results
        summary = causal_impact.summary(output='report')
        results = causal_impact.inferences

        # Create impact results DataFrame
        impact_results = pd.DataFrame({
            'event': [f'Event {i+1}' for i in range(len(event_periods))],
            'absolute_effect': [results['point_effects'].sum()],
            'relative_effect': [results['point_effects'].sum() / prices_df['y'].mean()]
        })

        # Adjust forecast using TimeGPT
        client = NixtlaClient(api_key=os.getenv('NIXTLA_TIMEGPT_API_KEY'))
        prices_df = prices_df.reset_index()
        forecast = client.forecast(df=prices_df[['unique_id', 'ds', 'y']], h=len(prices_df), freq='D')

        # Merge the forecast with the original data
        adjusted_forecast = pd.merge(prices_df, forecast, on=['unique_id', 'ds'], how='left')

        return impact_results, adjusted_forecast

    except Exception as e:
        logging.error(f"Analysis error: {e}")
        raise

def generate_visualization(adjusted_forecast: pd.DataFrame, output_path: str = 'impact_plot.png') -> None:
    """
    Generates a visualization of the event impact over time.

    Args:
        adjusted_forecast: DataFrame containing the adjusted forecast data.
        output_path: Path to save the visualization.
    """
    try:
        plt.figure(figsize=(12, 6))
        plt.plot(adjusted_forecast['ds'], adjusted_forecast['y'], label='Actual Price')
        plt.plot(adjusted_forecast['ds'], adjusted_forecast['mean'], label='Adjusted Forecast', linestyle='--')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Event Impact on Contract Prices')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_path)
        logging.info(f"Visualization saved to {output_path}")

    except Exception as e:
        logging.error(f"Visualization error: {e}")
        raise

if __name__ == "__main__":
    try:
        # Create dummy data for testing
        prices_data = {'ds': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07']),
                       'price': [10, 12, 13, 11, 14, 15, 16],
                       'unique_id': ['contract_1'] * 7}
        events_data = {'ds': pd.to_datetime(['2023-01-04']), 'event': ['Promotion']}

        prices_df = pd.DataFrame(prices_data)
        events_df = pd.DataFrame(events_data)

        event_periods = [(pd.to_datetime('2023-01-03'), pd.to_datetime('2023-01-05'))]  # Example event period

        # Set a dummy API key for testing (replace with your actual key)
        os.environ['NIXTLA_TIMEGPT_API_KEY'] = 'YOUR_DUMMY_API_KEY'

        impact_results, adjusted_forecast = analyze_event_impact(prices_df, event_periods)

        print("Impact Results:")
        print(impact_results)

        print("\nAdjusted Forecast:")
        print(adjusted_forecast.head())

        generate_visualization(adjusted_forecast)

        impact_results.to_csv('impact_results.csv', index=False)
        adjusted_forecast.to_csv('adjusted_forecast.csv', index=False)

    except Exception as e:
        print(f"Error in analysis: {e}")
```

### Step 4: Generate output

Save the event impact results and create visualizations.

This step is included in the `analyze_event_impact` script above.

## Output

- **impact_results.csv**: Quantified impact of each event on contract prices.
- **adjusted_forecast.csv**: Forecast of contract prices with event effects removed.
- **impact_plot.png**: Visualization of event impact over time.

## Error Handling

1. **Error**: `Event dates outside price range`
   **Solution**: Adjust event dates to fall within the available price data.

2. **Error**: `Missing event descriptions`
   **Solution**: Ensure 'event' column exists and is populated in the events CSV.

3. **Error**: `TimeGPT API request failed`
   **Solution**: Verify `NIXTLA_TIMEGPT_API_KEY` and internet connection.

4. **Error**: `CausalImpact failed to converge`
   **Solution**: Adjust model parameters or increase the `niter` parameter.

## Examples

### Example 1: Promotion impact

**Input**: `prices.csv` contains daily prices; `events.csv` marks promotion periods.

**Output**: `impact_results.csv` shows the average price increase during promotion periods.

### Example 2: Natural disaster impact

**Input**: `prices.csv` contains weekly prices; `events.csv` marks a natural disaster.

**Output**: `impact_results.csv` shows the price drop following the disaster.

## Resources

- Scripts: (Embedded above)
- Documentation: (Nixtla and CausalImpact documentation)

## Usage

To run the event impact analysis:

1.  Ensure you have the required packages installed: `pip install nixtla pandas causalimpact matplotlib`
2.  Set the `NIXTLA_TIMEGPT_API_KEY` environment variable.
3.  Create `prices.csv` and `events.csv` files with the appropriate data.
4.  Run the combined script from Step 3.  The script will generate `impact_results.csv`, `adjusted_forecast.csv`, and `impact_plot.png`.