#!/usr/bin/env python3
"""
Nixtla Full Forecasting Workflow

Orchestrates the complete baseline-to-production pipeline:
1. Extract sample from BigQuery
2. Run baseline models on sample (find winner)
3. Export winning model config
4. Run winning model on full BigQuery dataset

Usage:
    python full_workflow.py \
        --project myproject \
        --dataset mydataset \
        --table mytable \
        --timestamp-col date \
        --value-col sales \
        --group-by store_id \
        --sample-size 100 \
        --horizon 30 \
        --output-dataset forecasts \
        --output-table sales_forecast_20250110
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Paths relative to this script
SCRIPT_DIR = Path(__file__).parent
BIGQUERY_PLUGIN = SCRIPT_DIR.parent
BASELINE_PLUGIN = BIGQUERY_PLUGIN.parent / "nixtla-baseline-lab"


def run_full_workflow(
    project_id: str,
    dataset: str,
    table: str,
    timestamp_col: str,
    value_col: str,
    group_by: str = None,
    sample_size: int = 100,
    horizon: int = 30,
    output_dataset: str = None,
    output_table: str = None,
    source_project: str = None,
    work_dir: str = None,
) -> dict:
    """
    Run the complete forecasting workflow.

    Returns:
        Dict with workflow results and metadata
    """
    start_time = datetime.now()
    work_path = Path(work_dir) if work_dir else Path("nixtla_workflow_output")
    work_path.mkdir(exist_ok=True)

    results = {
        "workflow": "nixtla-full-forecast",
        "started_at": start_time.isoformat(),
        "steps": [],
    }

    try:
        # ═══════════════════════════════════════════════════════════════
        # STEP 1: Extract sample from BigQuery
        # ═══════════════════════════════════════════════════════════════
        logger.info("=" * 60)
        logger.info("STEP 1: Extracting sample from BigQuery")
        logger.info("=" * 60)

        sample_csv = work_path / "sample.csv"
        extract_script = SCRIPT_DIR / "extract_sample.py"

        extract_cmd = [
            sys.executable,
            str(extract_script),
            "--project", project_id,
            "--dataset", dataset,
            "--table", table,
            "--timestamp-col", timestamp_col,
            "--value-col", value_col,
            "--sample-size", str(sample_size),
            "--output", str(sample_csv),
        ]

        if group_by:
            extract_cmd.extend(["--group-by", group_by])
        if source_project:
            extract_cmd.extend(["--source-project", source_project])

        logger.info(f"Running: {' '.join(extract_cmd)}")
        result = subprocess.run(extract_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"Sample extraction failed: {result.stderr}")
            results["steps"].append({
                "step": 1,
                "name": "extract_sample",
                "success": False,
                "error": result.stderr,
            })
            results["success"] = False
            return results

        results["steps"].append({
            "step": 1,
            "name": "extract_sample",
            "success": True,
            "output": str(sample_csv),
        })
        logger.info(f"Sample extracted to: {sample_csv}")

        # ═══════════════════════════════════════════════════════════════
        # STEP 2: Run baseline models on sample
        # ═══════════════════════════════════════════════════════════════
        logger.info("=" * 60)
        logger.info("STEP 2: Running baseline models on sample")
        logger.info("=" * 60)

        baseline_output = work_path / "baseline_results"
        baseline_script = BASELINE_PLUGIN / "scripts" / "nixtla_baseline_mcp.py"

        # Run baseline MCP in test mode with custom CSV
        baseline_cmd = [
            sys.executable,
            str(baseline_script),
            "test",
            "--csv", str(sample_csv),
            "--output", str(baseline_output),
            "--horizon", str(min(horizon, 14)),  # Cap baseline horizon for speed
        ]

        # Actually, the MCP server doesn't have CLI args for CSV.
        # Let's call it programmatically instead.

        logger.info("Running baseline models programmatically...")

        # Add baseline plugin to path
        sys.path.insert(0, str(BASELINE_PLUGIN / "scripts"))

        from nixtla_baseline_mcp import NixtlaBaselineMCP

        mcp = NixtlaBaselineMCP()
        baseline_result = mcp.run_baselines(
            dataset_type="csv",
            csv_path=str(sample_csv),
            output_dir=str(baseline_output),
            horizon=min(horizon, 14),
            series_limit=sample_size,
        )

        if not baseline_result.get("success"):
            logger.error(f"Baseline run failed: {baseline_result.get('message')}")
            results["steps"].append({
                "step": 2,
                "name": "run_baselines",
                "success": False,
                "error": baseline_result.get("message"),
            })
            results["success"] = False
            return results

        results["steps"].append({
            "step": 2,
            "name": "run_baselines",
            "success": True,
            "summary": baseline_result.get("summary"),
            "files": baseline_result.get("files"),
        })
        logger.info(f"Baseline results: {baseline_result.get('summary')}")

        # ═══════════════════════════════════════════════════════════════
        # STEP 3: Export winning model config
        # ═══════════════════════════════════════════════════════════════
        logger.info("=" * 60)
        logger.info("STEP 3: Exporting winning model configuration")
        logger.info("=" * 60)

        # Find the metrics CSV from step 2
        metrics_csv = baseline_output / f"results_{baseline_result.get('dataset_label', 'Custom')}_h{min(horizon, 14)}.csv"

        config_result = mcp.export_winning_model_config(
            metrics_csv_path=str(metrics_csv),
            output_path=str(work_path / "winning_model_config.json")
        )

        if not config_result.get("success"):
            logger.error(f"Config export failed: {config_result.get('error')}")
            results["steps"].append({
                "step": 3,
                "name": "export_config",
                "success": False,
                "error": config_result.get("error"),
            })
            results["success"] = False
            return results

        winning_model = config_result.get("winning_model")
        config_path = config_result.get("config_path")

        results["steps"].append({
            "step": 3,
            "name": "export_config",
            "success": True,
            "winning_model": winning_model,
            "config_path": config_path,
        })
        logger.info(f"Winning model: {winning_model}")
        logger.info(f"Config exported to: {config_path}")

        # ═══════════════════════════════════════════════════════════════
        # STEP 4: Run winning model on full BigQuery dataset
        # ═══════════════════════════════════════════════════════════════
        logger.info("=" * 60)
        logger.info("STEP 4: Running winning model on full BigQuery dataset")
        logger.info("=" * 60)

        # This would call the Cloud Function or run locally
        # For now, we'll prepare the request payload

        forecast_request = {
            "project_id": project_id,
            "dataset": dataset,
            "table": table,
            "timestamp_col": timestamp_col,
            "value_col": value_col,
            "horizon": horizon,
            "models": [winning_model],
            "model_config_path": config_path,
        }

        if group_by:
            forecast_request["group_by"] = group_by
        if source_project:
            forecast_request["source_project"] = source_project
        if output_dataset:
            forecast_request["output_dataset"] = output_dataset
        if output_table:
            forecast_request["output_table"] = output_table

        # Save request for manual execution or Cloud Function call
        request_path = work_path / "forecast_request.json"
        request_path.write_text(json.dumps(forecast_request, indent=2))

        results["steps"].append({
            "step": 4,
            "name": "prepare_production_forecast",
            "success": True,
            "winning_model": winning_model,
            "forecast_request": str(request_path),
            "note": "Request prepared. Call bigquery-forecaster Cloud Function with this payload.",
        })

        logger.info(f"Production forecast request saved to: {request_path}")
        logger.info(f"Model to use: {winning_model}")

        # ═══════════════════════════════════════════════════════════════
        # WORKFLOW COMPLETE
        # ═══════════════════════════════════════════════════════════════
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        results["success"] = True
        results["completed_at"] = end_time.isoformat()
        results["duration_seconds"] = duration
        results["winning_model"] = winning_model
        results["work_dir"] = str(work_path.absolute())

        logger.info("=" * 60)
        logger.info("WORKFLOW COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Winning model: {winning_model}")
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Output directory: {work_path.absolute()}")

        return results

    except Exception as e:
        logger.error(f"Workflow failed: {e}", exc_info=True)
        results["success"] = False
        results["error"] = str(e)
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Run full Nixtla forecasting workflow: baseline test → production forecast"
    )

    # Required parameters
    parser.add_argument("--project", required=True, help="GCP project ID")
    parser.add_argument("--dataset", required=True, help="BigQuery dataset name")
    parser.add_argument("--table", required=True, help="BigQuery table name")
    parser.add_argument("--timestamp-col", required=True, help="Timestamp column name")
    parser.add_argument("--value-col", required=True, help="Value column to forecast")

    # Optional parameters
    parser.add_argument("--group-by", help="Column to group by (creates unique_id)")
    parser.add_argument("--sample-size", type=int, default=100, help="Sample size for baseline")
    parser.add_argument("--horizon", type=int, default=30, help="Forecast horizon")
    parser.add_argument("--output-dataset", help="Output BigQuery dataset")
    parser.add_argument("--output-table", help="Output BigQuery table")
    parser.add_argument("--source-project", help="Source project (for public datasets)")
    parser.add_argument("--work-dir", default="nixtla_workflow_output", help="Working directory")

    args = parser.parse_args()

    result = run_full_workflow(
        project_id=args.project,
        dataset=args.dataset,
        table=args.table,
        timestamp_col=args.timestamp_col,
        value_col=args.value_col,
        group_by=args.group_by,
        sample_size=args.sample_size,
        horizon=args.horizon,
        output_dataset=args.output_dataset,
        output_table=args.output_table,
        source_project=args.source_project,
        work_dir=args.work_dir,
    )

    # Write results
    results_path = Path(args.work_dir) / "workflow_results.json"
    results_path.parent.mkdir(exist_ok=True)
    results_path.write_text(json.dumps(result, indent=2))

    print(f"\nWorkflow results saved to: {results_path}")

    if result.get("success"):
        print(f"\nWinning model: {result.get('winning_model')}")
        print(f"Next step: Deploy forecast request to Cloud Function")
        sys.exit(0)
    else:
        print(f"\nWorkflow failed: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
