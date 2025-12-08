#!/usr/bin/env python3
"""
Pipeline code generator for Airflow and Prefect.
"""
import argparse
import os
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_airflow_dag(config: Dict[str, Any]) -> str:
    """
    Generates an Airflow DAG Python file based on the experiment configuration.

    Args:
        config: The experiment configuration dictionary.

    Returns:
        The generated Airflow DAG code as a string.
    """
    pipeline_name = config['pipeline_name']
    model_type = config['model_type']
    data_location = config['data_location']
    frequency = config['frequency']
    horizon = config['horizon']

    dag_code = f"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

# Nixtla Imports
from nixtla import NixtlaClient
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA

def load_data():
    # Load data from {data_location}
    df = pd.read_csv('{data_location}')
    return df

def train_model(df):
    # Train {model_type} model
    if '{model_type}' == 'TimeGPT':
        client = NixtlaClient(api_key=os.getenv('NIXTLA_TIMEGPT_API_KEY'))
        forecast = client.forecast(df=df, h={horizon}, freq='{frequency}')
        return forecast
    elif '{model_type}' == 'StatsForecast':
        sf = StatsForecast(models=[AutoETS(), AutoARIMA()], freq='{frequency}', n_jobs=-1)
        forecasts = sf.forecast(df=df, h={horizon})
        return forecasts
    else:
        raise ValueError("Invalid model_type")

def save_forecast(forecast):
    # Save forecast to a file
    forecast.to_csv('forecast.csv', index=False)

with DAG(
    dag_id='{pipeline_name}_dag',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['nixtla', '{model_type}']
) as dag:
    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        op_kwargs={{'df': load_data_task.output}}
    )

    save_forecast_task = PythonOperator(
        task_id='save_forecast',
        python_callable=save_forecast,
        op_kwargs={{'forecast': train_model_task.output}}
    )

    load_data_task >> train_model_task >> save_forecast_task
"""
    logging.info("Airflow DAG code generated.")
    return dag_code


def generate_prefect_flow(config: Dict[str, Any]) -> str:
    """
    Generates a Prefect flow Python file based on the experiment configuration.

    Args:
        config: The experiment configuration dictionary.

    Returns:
        The generated Prefect flow code as a string.
    """
    pipeline_name = config['pipeline_name']
    model_type = config['model_type']
    data_location = config['data_location']
    frequency = config['frequency']
    horizon = config['horizon']

    flow_code = f"""
from prefect import flow, task
import pandas as pd
import os

# Nixtla Imports
from nixtla import NixtlaClient
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA

@task
def load_data():
    # Load data from {data_location}
    df = pd.read_csv('{data_location}')
    return df

@task
def train_model(df):
    # Train {model_type} model
    if '{model_type}' == 'TimeGPT':
        client = NixtlaClient(api_key=os.getenv('NIXTLA_TIMEGPT_API_KEY'))
        forecast = client.forecast(df=df, h={horizon}, freq='{frequency}')
        return forecast
    elif '{model_type}' == 'StatsForecast':
        sf = StatsForecast(models=[AutoETS(), AutoARIMA()], freq='{frequency}', n_jobs=-1)
        forecasts = sf.forecast(df=df, h={horizon})
        return forecasts
    else:
        raise ValueError("Invalid model_type")

@task
def save_forecast(forecast):
    # Save forecast to a file
    forecast.to_csv('forecast.csv', index=False)

@flow(name='{pipeline_name}_flow')
def main_flow():
    data = load_data()
    model = train_model(data)
    save_forecast(model)

if __name__ == "__main__":
    main_flow()
"""
    logging.info("Prefect flow code generated.")
    return flow_code


def main():
    parser = argparse.ArgumentParser(description="Generate Airflow or Prefect pipeline code.")
    parser.add_argument("--config", required=True, help="Path to the experiment configuration file (YAML or JSON).")
    parser.add_argument("--framework", required=True, choices=['airflow', 'prefect'], help="Target framework: airflow or prefect.")

    args = parser.parse_args()

    from load_config import load_config, validate_config

    try:
        config = load_config(args.config)
        validate_config(config)

        if args.framework == 'airflow':
            dag_code = generate_airflow_dag(config)
            output_dir = 'dags'
            os.makedirs(output_dir, exist_ok=True)
            with open(os.path.join(output_dir, f"{config['pipeline_name']}_dag.py"), 'w') as f:
                f.write(dag_code)
            logging.info(f"Airflow DAG saved to dags/{config['pipeline_name']}_dag.py")

        elif args.framework == 'prefect':
            flow_code = generate_prefect_flow(config)
            output_dir = 'flows'
            os.makedirs(output_dir, exist_ok=True)
            with open(os.path.join(output_dir, f"{config['pipeline_name']}_flow.py"), 'w') as f:
                f.write(flow_code)
            logging.info(f"Prefect flow saved to flows/{config['pipeline_name']}_flow.py")

        else:
            raise ValueError("Invalid framework specified. Choose 'airflow' or 'prefect'.")

    except (FileNotFoundError, ValueError) as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    main()
