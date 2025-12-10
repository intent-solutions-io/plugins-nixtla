"""
Cloud Function Entry Point for Nixtla BigQuery Forecaster

Handles HTTP requests to forecast time series data from BigQuery using Nixtla models.
"""

import json
import logging
import os
from typing import Any, Dict

import functions_framework
from flask import Request, jsonify

from .bigquery_connector import BigQueryConnector
from .forecaster import NixtlaForecaster

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.http
def forecast_handler(request: Request) -> tuple[Dict[str, Any], int]:
    """
    HTTP Cloud Function entry point for BigQuery forecasting.

    Expected JSON payload:
    {
        "project_id": "bigquery-public-data",
        "dataset": "chicago_taxi_trips",
        "table": "taxi_trips",
        "timestamp_col": "trip_start_timestamp",
        "value_col": "trip_total",
        "group_by": "payment_type",  # optional
        "horizon": 30,
        "models": ["AutoETS", "AutoTheta"],  # optional
        "include_timegpt": false,  # optional
        "output_dataset": "forecast_results",  # optional
        "output_table": "forecasts_20250129",  # optional
        "limit": 10000  # optional
    }

    Returns:
        JSON response with forecast results and metadata
    """
    try:
        # Parse request
        request_json = request.get_json(silent=True)
        if not request_json:
            return jsonify({"error": "No JSON payload provided"}), 400

        # Extract required parameters
        project_id = request_json.get("project_id")
        dataset = request_json.get("dataset")
        table = request_json.get("table")
        timestamp_col = request_json.get("timestamp_col")
        value_col = request_json.get("value_col")
        horizon = request_json.get("horizon")

        # Validate required fields
        missing_fields = []
        if not project_id:
            missing_fields.append("project_id")
        if not dataset:
            missing_fields.append("dataset")
        if not table:
            missing_fields.append("table")
        if not timestamp_col:
            missing_fields.append("timestamp_col")
        if not value_col:
            missing_fields.append("value_col")
        if not horizon:
            missing_fields.append("horizon")

        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Extract optional parameters
        group_by = request_json.get("group_by")
        where_clause = request_json.get("where_clause")
        limit = request_json.get("limit")
        models = request_json.get("models", ["AutoETS", "AutoTheta"])
        include_timegpt = request_json.get("include_timegpt", False)
        output_dataset = request_json.get("output_dataset")
        output_table = request_json.get("output_table")
        source_project = request_json.get("source_project")  # For public datasets
        model_config_path = request_json.get("model_config_path")  # Integration with baseline-lab

        # If model_config_path provided, read winning model from baseline-lab output
        if model_config_path:
            try:
                import json
                from pathlib import Path

                config_file = Path(model_config_path)
                if config_file.exists():
                    winning_config = json.loads(config_file.read_text())
                    winning_model = winning_config.get("winning_model", {}).get("name")
                    if winning_model:
                        models = [winning_model]
                        logger.info(f"Using winning model from config: {winning_model}")
                else:
                    logger.warning(f"Model config not found: {model_config_path}, using default models")
            except Exception as e:
                logger.warning(f"Error reading model config: {e}, using default models")

        logger.info(
            f"Forecast request: project={project_id}, dataset={dataset}, "
            f"table={table}, horizon={horizon}, models={models}"
        )

        # Step 1: Read time series data from BigQuery
        logger.info("Step 1: Reading time series data from BigQuery...")
        bq_connector = BigQueryConnector(project_id=project_id)

        df = bq_connector.read_timeseries(
            dataset=dataset,
            table=table,
            timestamp_col=timestamp_col,
            value_col=value_col,
            group_by=group_by,
            where_clause=where_clause,
            limit=limit,
            source_project=source_project,
        )

        if df.empty:
            return jsonify({"error": "No data found with specified filters"}), 404

        logger.info(f"Read {len(df)} rows, {df['unique_id'].nunique()} unique time series")

        # Step 2: Run Nixtla forecasts
        logger.info("Step 2: Running Nixtla forecasts...")
        forecaster = NixtlaForecaster(timegpt_api_key=os.environ.get("NIXTLA_TIMEGPT_API_KEY"))

        forecast_results = forecaster.forecast(
            df=df, horizon=horizon, models=models, include_timegpt=include_timegpt
        )

        logger.info(f"Generated {len(forecast_results)} forecast points")

        # Step 3: Write forecasts back to BigQuery (if output specified)
        output_table_id = None
        if output_dataset and output_table:
            logger.info("Step 3: Writing forecasts to BigQuery...")
            output_table_id = bq_connector.write_forecasts(
                df=forecast_results, dataset=output_dataset, table=output_table, if_exists="replace"
            )
            logger.info(f"Wrote forecasts to {output_table_id}")

        # Prepare response
        response = {
            "status": "success",
            "metadata": {
                "source_table": f"{project_id}.{dataset}.{table}",
                "rows_read": len(df),
                "unique_series": df["unique_id"].nunique(),
                "horizon": horizon,
                "models_used": models,
                "timegpt_included": include_timegpt,
                "forecast_points_generated": len(forecast_results),
            },
            "forecasts": forecast_results.to_dict(orient="records"),
        }

        if output_table_id:
            response["output_table"] = output_table_id

        logger.info("Forecast completed successfully")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error in forecast_handler: {str(e)}", exc_info=True)
        return jsonify({"error": str(e), "type": type(e).__name__}), 500


# Local testing entry point
if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def local_test():
        from flask import request

        return forecast_handler(request)

    print("Starting local test server on http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)
