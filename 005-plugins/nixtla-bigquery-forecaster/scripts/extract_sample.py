#!/usr/bin/env python3
"""
BigQuery Sample Extractor

Pulls a representative sample from BigQuery for baseline model testing.
Output format matches baseline-lab requirements: unique_id, ds, y

Usage:
    python extract_sample.py \
        --project myproject \
        --dataset mydataset \
        --table mytable \
        --timestamp-col date \
        --value-col sales \
        --group-by store_id \
        --sample-size 100 \
        --output sample.csv
"""

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def extract_sample(
    project_id: str,
    dataset: str,
    table: str,
    timestamp_col: str,
    value_col: str,
    group_by: str = None,
    sample_size: int = 100,
    output_path: str = "sample.csv",
    source_project: str = None,
    where_clause: str = None,
    min_points_per_series: int = 30,
) -> dict:
    """
    Extract a representative sample from BigQuery.

    Args:
        project_id: GCP project ID
        dataset: BigQuery dataset name
        table: BigQuery table name
        timestamp_col: Column containing timestamps
        value_col: Column containing values to forecast
        group_by: Column to group by (creates unique_id)
        sample_size: Number of unique series to sample
        output_path: Path for output CSV
        source_project: Source project for public datasets
        where_clause: Optional WHERE filter
        min_points_per_series: Minimum data points required per series

    Returns:
        Dict with success status, row count, series count
    """
    try:
        import pandas as pd
        from google.cloud import bigquery

        logger.info(f"Connecting to BigQuery project: {project_id}")
        client = bigquery.Client(project=project_id)

        # Build source table reference
        source = source_project or project_id
        full_table = f"`{source}.{dataset}.{table}`"

        # Build unique_id expression
        if group_by:
            unique_id_expr = f"CAST({group_by} AS STRING)"
        else:
            unique_id_expr = "'series_1'"

        # Query to get sample of series with enough data points
        sample_query = f"""
        WITH series_counts AS (
            SELECT
                {unique_id_expr} AS unique_id,
                COUNT(*) as point_count
            FROM {full_table}
            {f'WHERE {where_clause}' if where_clause else ''}
            GROUP BY 1
            HAVING COUNT(*) >= {min_points_per_series}
        ),
        sampled_series AS (
            SELECT unique_id
            FROM series_counts
            ORDER BY RAND()
            LIMIT {sample_size}
        )
        SELECT
            s.unique_id,
            CAST(t.{timestamp_col} AS DATE) AS ds,
            CAST(t.{value_col} AS FLOAT64) AS y
        FROM {full_table} t
        JOIN sampled_series s ON {unique_id_expr} = s.unique_id
        {f'WHERE {where_clause}' if where_clause else ''}
        ORDER BY s.unique_id, ds
        """

        logger.info(f"Executing sample query (sample_size={sample_size})...")
        logger.debug(f"Query: {sample_query}")

        df = client.query(sample_query).to_dataframe()

        if df.empty:
            logger.error("No data returned from query")
            return {
                "success": False,
                "error": "No data returned. Check table/column names and filters.",
            }

        # Validate output format
        required_cols = {"unique_id", "ds", "y"}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            return {"success": False, "error": f"Missing columns: {missing}"}

        # Convert ds to datetime string format
        df["ds"] = pd.to_datetime(df["ds"]).dt.strftime("%Y-%m-%d")

        # Write to CSV
        output_file = Path(output_path)
        df.to_csv(output_file, index=False)

        series_count = df["unique_id"].nunique()
        row_count = len(df)

        logger.info(f"Extracted {row_count} rows across {series_count} series")
        logger.info(f"Output written to: {output_file.absolute()}")

        return {
            "success": True,
            "output_path": str(output_file.absolute()),
            "row_count": row_count,
            "series_count": series_count,
            "source_table": f"{source}.{dataset}.{table}",
        }

    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        return {"success": False, "error": f"Missing dependency: {e}"}
    except Exception as e:
        logger.error(f"Error extracting sample: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Extract sample from BigQuery for baseline model testing"
    )

    parser.add_argument("--project", required=True, help="GCP project ID")
    parser.add_argument("--dataset", required=True, help="BigQuery dataset name")
    parser.add_argument("--table", required=True, help="BigQuery table name")
    parser.add_argument("--timestamp-col", required=True, help="Timestamp column name")
    parser.add_argument("--value-col", required=True, help="Value column to forecast")
    parser.add_argument("--group-by", help="Column to group by (creates unique_id)")
    parser.add_argument("--sample-size", type=int, default=100, help="Number of series to sample")
    parser.add_argument("--output", default="sample.csv", help="Output CSV path")
    parser.add_argument("--source-project", help="Source project (for public datasets)")
    parser.add_argument("--where", help="Optional WHERE clause filter")
    parser.add_argument("--min-points", type=int, default=30, help="Min points per series")

    args = parser.parse_args()

    result = extract_sample(
        project_id=args.project,
        dataset=args.dataset,
        table=args.table,
        timestamp_col=args.timestamp_col,
        value_col=args.value_col,
        group_by=args.group_by,
        sample_size=args.sample_size,
        output_path=args.output,
        source_project=args.source_project,
        where_clause=args.where,
        min_points_per_series=args.min_points,
    )

    if result["success"]:
        print(f"\nSample extracted successfully!")
        print(f"  Series: {result['series_count']}")
        print(f"  Rows: {result['row_count']}")
        print(f"  Output: {result['output_path']}")
        sys.exit(0)
    else:
        print(f"\nExtraction failed: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
