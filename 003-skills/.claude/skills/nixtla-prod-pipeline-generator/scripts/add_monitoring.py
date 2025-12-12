#!/usr/bin/env python3
"""
Add monitoring and alerting to existing pipeline.

Instruments pipeline code with quality checks, drift detection, anomaly detection,
and alert hooks. Can be applied to existing Airflow DAGs, Prefect flows, or scripts.

Usage:
    python add_monitoring.py --pipeline pipelines/forecast_dag.py --metrics smape,mase
    python add_monitoring.py --pipeline pipelines/forecast_dag.py --thresholds smape=20,mase=1.5
    python add_monitoring.py --pipeline pipelines/run_forecast.py --alerts email,slack

Author: nixtla-prod-pipeline-generator skill
"""

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Security logging
logging.basicConfig(level=logging.INFO)
sec_logger = logging.getLogger(__name__)


def validate_api_key(key: Optional[str]) -> bool:
    """
    Validate API key format and structure.

    Args:
        key: API key string to validate

    Returns:
        True if key appears valid, False otherwise

    Security:
        - Minimum length check prevents empty/trivial keys
        - Pattern check validates expected format
        - Does not log key value to prevent credential leakage
        - OWASP A07:2021 - Identification and Authentication Failures
    """
    if not key:
        return False

    key = key.strip()

    # Minimum length check (Nixtla keys are typically 32+ characters)
    if len(key) < 20:
        return False

    # Check for common placeholder values
    placeholder_patterns = [
        r"^your[-_]?api[-_]?key",
        r"^xxx+$",
        r"^test[-_]?key",
        r"^placeholder",
        r"^demo[-_]?key",
    ]
    for pattern in placeholder_patterns:
        if re.match(pattern, key, re.IGNORECASE):
            return False

    # Basic alphanumeric pattern check (allow alphanumeric, hyphens, underscores)
    if not re.match(r"^[a-zA-Z0-9_-]+$", key):
        return False

    return True


def escape_value_for_code(value) -> str:
    """
    Escape value for safe embedding in generated Python code.

    Args:
        value: Value to escape (can be str, int, float, list, dict)

    Returns:
        Safely escaped representation

    Security:
        - Prevents code injection via configuration values
        - OWASP A03:2021 - Injection
    """
    if isinstance(value, str):
        # Escape backslashes first, then quotes and newlines
        escaped = value.replace("\\", "\\\\")
        escaped = escaped.replace('"', '\\"')
        escaped = escaped.replace("'", "\\'")
        escaped = escaped.replace("\n", "\\n")
        escaped = escaped.replace("\r", "\\r")
        return f"'{escaped}'"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, bool):
        return str(value)
    elif isinstance(value, (list, dict)):
        # Use repr for safe serialization, then validate
        safe_repr = repr(value)
        # Additional check: ensure no embedded code patterns
        if re.search(r"__\w+__|exec|eval|compile|import", safe_repr):
            raise ValueError(f"Potentially unsafe value detected: {type(value)}")
        return safe_repr
    else:
        return repr(value)


class MonitoringInjector:
    """Add monitoring capabilities to existing pipeline code."""

    SUPPORTED_METRICS = ["smape", "mase", "mae", "rmse", "mape"]
    ALERT_CHANNELS = ["email", "slack", "pagerduty", "webhook"]

    def __init__(self, pipeline_path: str):
        """
        Initialize monitoring injector.

        Args:
            pipeline_path: Path to existing pipeline file
        """
        self.pipeline_path = Path(pipeline_path)
        self.pipeline_code: Optional[str] = None
        self.platform: Optional[str] = None

        if not self.pipeline_path.exists():
            raise FileNotFoundError(f"Pipeline not found: {pipeline_path}")

    def load_pipeline(self):
        """Load and detect pipeline type."""
        with open(self.pipeline_path, "r") as f:
            self.pipeline_code = f.read()

        # Detect platform
        if "from airflow import DAG" in self.pipeline_code:
            self.platform = "airflow"
        elif "from prefect import flow" in self.pipeline_code:
            self.platform = "prefect"
        else:
            self.platform = "script"

        print(f"✓ Loaded {self.platform} pipeline: {self.pipeline_path}")

    def add_monitoring(
        self,
        metrics: List[str],
        thresholds: Optional[Dict[str, float]] = None,
        alerts: Optional[List[str]] = None,
    ) -> str:
        """
        Add monitoring code to pipeline.

        Args:
            metrics: List of metrics to track
            thresholds: Metric thresholds for alerting
            alerts: Alert channels to use

        Returns:
            Modified pipeline code
        """
        if not self.pipeline_code:
            raise ValueError("No pipeline loaded. Call load_pipeline() first.")

        thresholds = thresholds or self._default_thresholds(metrics)
        alerts = alerts or ["email"]

        modified_code = self.pipeline_code

        # Add imports
        modified_code = self._add_monitoring_imports(modified_code)

        # Add monitoring functions
        modified_code = self._add_monitoring_functions(modified_code, metrics, thresholds)

        # Add alert functions
        modified_code = self._add_alert_functions(modified_code, alerts)

        # Inject monitoring calls
        modified_code = self._inject_monitoring_calls(modified_code, metrics)

        return modified_code

    def _default_thresholds(self, metrics: List[str]) -> Dict[str, float]:
        """Get default thresholds for metrics."""
        defaults = {"smape": 20.0, "mase": 1.5, "mae": 100.0, "rmse": 150.0, "mape": 25.0}
        return {m: defaults.get(m, 100.0) for m in metrics}

    def _add_monitoring_imports(self, code: str) -> str:
        """Add required imports for monitoring."""
        imports = """
# Monitoring imports (added by add_monitoring.py)
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""

        # Insert after existing imports
        import_end = code.rfind("import ")
        if import_end != -1:
            next_line = code.find("\n", import_end)
            code = code[: next_line + 1] + imports + code[next_line + 1 :]

        return code

    def _add_monitoring_functions(
        self, code: str, metrics: List[str], thresholds: Dict[str, float]
    ) -> str:
        """
        Add monitoring function implementations.

        Security:
            - Escapes threshold values to prevent code injection
            - OWASP A03:2021 - Injection
        """
        # Security: Safely serialize thresholds dict
        safe_thresholds = escape_value_for_code(thresholds)

        monitoring_funcs = f'''

# Monitoring functions (added by add_monitoring.py)
METRIC_THRESHOLDS = {safe_thresholds}


def calculate_smape(actual, forecast):
    """Calculate Symmetric Mean Absolute Percentage Error."""
    return 100 * np.mean(
        2 * np.abs(forecast - actual) / (np.abs(actual) + np.abs(forecast))
    )


def calculate_mase(actual, forecast, seasonality=1):
    """Calculate Mean Absolute Scaled Error."""
    mae_forecast = np.mean(np.abs(actual - forecast))
    mae_naive = np.mean(np.abs(np.diff(actual, n=seasonality)))
    return mae_forecast / mae_naive if mae_naive > 0 else np.inf


def calculate_mae(actual, forecast):
    """Calculate Mean Absolute Error."""
    return np.mean(np.abs(actual - forecast))


def calculate_rmse(actual, forecast):
    """Calculate Root Mean Squared Error."""
    return np.sqrt(np.mean((actual - forecast) ** 2))


def calculate_mape(actual, forecast):
    """Calculate Mean Absolute Percentage Error."""
    return 100 * np.mean(np.abs((actual - forecast) / actual))


def check_forecast_quality(actual, forecast, metrics={metrics}):
    """
    Check forecast quality against thresholds.

    Args:
        actual: Actual values
        forecast: Forecasted values
        metrics: List of metrics to calculate

    Returns:
        dict with metric values and alert flags
    """
    results = {{'timestamp': datetime.now().isoformat()}}

    for metric in metrics:
        if metric == 'smape':
            value = calculate_smape(actual, forecast)
        elif metric == 'mase':
            value = calculate_mase(actual, forecast)
        elif metric == 'mae':
            value = calculate_mae(actual, forecast)
        elif metric == 'rmse':
            value = calculate_rmse(actual, forecast)
        elif metric == 'mape':
            value = calculate_mape(actual, forecast)
        else:
            continue

        results[metric] = value

        threshold = METRIC_THRESHOLDS.get(metric)
        if threshold and value > threshold:
            results[f'{{metric}}_alert'] = True
            logger.warning(
                f"⚠️  {{metric.upper()}} {{value:.2f}} exceeds threshold {{threshold}}"
            )
        else:
            results[f'{{metric}}_alert'] = False
            logger.info(f"✓ {{metric.upper()}} {{value:.2f}} within threshold")

    return results


def detect_data_drift(df, window_days=30, threshold_pct=20):
    """
    Detect significant changes in data distribution.

    Args:
        df: Historical data with 'ds' and 'y' columns
        window_days: Size of recent window
        threshold_pct: Percentage change threshold

    Returns:
        dict with drift indicators
    """
    if len(df) < window_days * 2:
        logger.warning("Insufficient data for drift detection")
        return {{'drift_detected': False, 'reason': 'insufficient_data'}}

    recent = df.tail(window_days)
    historical = df.iloc[:-window_days]

    recent_mean = recent['y'].mean()
    recent_std = recent['y'].std()
    historical_mean = historical['y'].mean()
    historical_std = historical['y'].std()

    mean_change = 100 * abs(recent_mean - historical_mean) / historical_mean
    std_change = 100 * abs(recent_std - historical_std) / historical_std

    drift_detected = mean_change > threshold_pct or std_change > (threshold_pct * 1.5)

    results = {{
        'drift_detected': drift_detected,
        'mean_change_pct': mean_change,
        'std_change_pct': std_change,
        'recent_mean': recent_mean,
        'historical_mean': historical_mean,
        'timestamp': datetime.now().isoformat()
    }}

    if drift_detected:
        logger.warning(
            f"⚠️  Data drift detected: mean Δ{{mean_change:.1f}}%, "
            f"std Δ{{std_change:.1f}}%"
        )

    return results


def detect_anomalies(forecast_df, threshold_std=3):
    """
    Detect anomalous forecast values.

    Args:
        forecast_df: Forecast dataframe
        threshold_std: Standard deviation threshold

    Returns:
        dict with anomaly information
    """
    # Get forecast column
    forecast_cols = [c for c in forecast_df.columns if c not in ['unique_id', 'ds']]
    if not forecast_cols:
        return {{'anomaly_count': 0}}

    forecasts = forecast_df[forecast_cols[0]].values

    mean = np.mean(forecasts)
    std = np.std(forecasts)

    anomalies = np.abs(forecasts - mean) > (threshold_std * std)
    anomaly_count = np.sum(anomalies)

    if anomaly_count > 0:
        logger.warning(
            f"⚠️  {{anomaly_count}} anomalous forecasts detected "
            f"(>{{threshold_std}}σ from mean)"
        )

    return {{
        'anomaly_count': int(anomaly_count),
        'anomaly_indices': np.where(anomalies)[0].tolist(),
        'mean': float(mean),
        'std': float(std),
        'threshold_std': threshold_std,
        'timestamp': datetime.now().isoformat()
    }}
'''

        # Insert before main execution
        if "__name__" in code:
            main_idx = code.find("if __name__")
            code = code[:main_idx] + monitoring_funcs + "\n" + code[main_idx:]
        else:
            code += monitoring_funcs

        return code

    def _add_alert_functions(self, code: str, channels: List[str]) -> str:
        """
        Add alert channel implementations.

        Security:
            - Escapes channel names to prevent code injection
            - OWASP A03:2021 - Injection
        """
        # Security: Safely serialize channels list
        safe_channels = escape_value_for_code(channels)

        alert_funcs = f'''

# Alert functions (added by add_monitoring.py)
def send_alert(message, severity='warning', channels={safe_channels}):
    """
    Send alert through configured channels.

    Args:
        message: Alert message
        severity: 'info', 'warning', or 'critical'
        channels: List of alert channels
    """
    logger.log(
        logging.WARNING if severity == 'warning' else logging.ERROR,
        f"ALERT [{{severity}}]: {{message}}"
    )

    for channel in channels:
        if channel == 'email':
            _send_email_alert(message, severity)
        elif channel == 'slack':
            _send_slack_alert(message, severity)
        elif channel == 'pagerduty':
            _send_pagerduty_alert(message, severity)
        elif channel == 'webhook':
            _send_webhook_alert(message, severity)


def _send_email_alert(message, severity):
    """Send email alert (requires SMTP config)."""
    import os
    # TODO: Implement with your email provider
    # Example: Use SMTP or SendGrid API
    email = os.getenv('ALERT_EMAIL')
    if email:
        logger.info(f"Would send email to {{email}}: {{message}}")


def _send_slack_alert(message, severity):
    """Send Slack alert (requires webhook URL)."""
    import os
    import requests

    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        logger.warning("SLACK_WEBHOOK_URL not set, skipping Slack alert")
        return

    emoji = '⚠️' if severity == 'warning' else '🚨'
    payload = {{
        'text': f'{{emoji}} Forecast Pipeline Alert',
        'attachments': [{{
            'color': 'warning' if severity == 'warning' else 'danger',
            'text': message,
            'footer': 'Nixtla Production Pipeline',
            'ts': int(datetime.now().timestamp())
        }}]
    }}

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        logger.info("Slack alert sent successfully")
    except Exception as e:
        logger.error(f"Failed to send Slack alert: {{e}}")


def _send_pagerduty_alert(message, severity):
    """Send PagerDuty alert (requires integration key)."""
    import os
    # TODO: Implement with PagerDuty Events API
    logger.info(f"Would send PagerDuty alert: {{message}}")


def _send_webhook_alert(message, severity):
    """Send generic webhook alert."""
    import os
    import requests

    webhook_url = os.getenv('ALERT_WEBHOOK_URL')
    if not webhook_url:
        return

    payload = {{
        'message': message,
        'severity': severity,
        'timestamp': datetime.now().isoformat(),
        'pipeline': 'nixtla-production-forecast'
    }}

    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception as e:
        logger.error(f"Failed to send webhook alert: {{e}}")
'''

        # Insert after monitoring functions
        if "def check_forecast_quality" in code:
            insert_idx = code.rfind("def check_forecast_quality")
            # Find end of function block
            next_func = code.find("\n\ndef ", insert_idx)
            if next_func != -1:
                code = code[:next_func] + alert_funcs + code[next_func:]
            else:
                code += alert_funcs

        return code

    def _inject_monitoring_calls(self, code: str, metrics: List[str]) -> str:
        """
        Inject monitoring calls into pipeline execution.

        Security:
            - Escapes metrics list to prevent code injection
            - OWASP A03:2021 - Injection
        """
        # Look for monitor/quality check functions
        monitor_patterns = [r"def monitor.*\(", r"def monitor_quality.*\(", r"def.*quality.*\("]

        modified = False
        for pattern in monitor_patterns:
            if re.search(pattern, code):
                # Add monitoring calls within existing monitor functions
                code = self._enhance_monitor_function(code, pattern, metrics)
                modified = True

        if not modified:
            sec_logger.warning(
                "No monitor function found. " "Add monitoring calls manually after forecast step."
            )

        return code

    def _enhance_monitor_function(self, code: str, pattern: str, metrics: List[str]) -> str:
        """
        Enhance existing monitor function with new checks.

        Security:
            - Escapes metrics list to prevent code injection
            - OWASP A03:2021 - Injection
        """
        match = re.search(pattern, code)
        if not match:
            return code

        func_start = match.start()
        # Find function body
        func_body_start = code.find(":", func_start) + 1

        # Security: Safely serialize metrics list
        safe_metrics = escape_value_for_code(metrics)

        monitoring_calls = f"""
    # Enhanced monitoring (added by add_monitoring.py)

    # Check forecast quality
    if 'actual' in locals() and 'forecast' in locals():
        quality_results = check_forecast_quality(actual, forecast, {safe_metrics})

        # Alert if any metric exceeds threshold
        alerts = [k for k, v in quality_results.items() if k.endswith('_alert') and v]
        if alerts:
            alert_msg = f"Forecast quality degraded: {{', '.join(alerts)}}"
            send_alert(alert_msg, severity='warning')

    # Check for data drift
    if 'df' in locals() or 'data' in locals():
        data_df = df if 'df' in locals() else data
        drift_results = detect_data_drift(data_df)

        if drift_results.get('drift_detected'):
            alert_msg = (
                f"Data drift detected: "
                f"mean changed {{drift_results['mean_change_pct']:.1f}}%"
            )
            send_alert(alert_msg, severity='warning')

    # Check for anomalies in forecasts
    if 'forecast_df' in locals():
        anomaly_results = detect_anomalies(forecast_df)

        if anomaly_results['anomaly_count'] > 0:
            alert_msg = (
                f"{{anomaly_results['anomaly_count']}} anomalous forecasts detected"
            )
            send_alert(alert_msg, severity='info')
"""

        # Insert at start of function body
        code = code[:func_body_start] + monitoring_calls + code[func_body_start:]

        return code

    def save(self, output_path: Optional[str] = None):
        """
        Save modified pipeline.

        Args:
            output_path: Output path (default: overwrite original with .bak backup)
        """
        if not output_path:
            # Create backup
            backup_path = self.pipeline_path.with_suffix(".bak")
            self.pipeline_path.rename(backup_path)
            output_path = self.pipeline_path
            print(f"✓ Created backup: {backup_path}")

        output_path = Path(output_path)
        output_path.write_text(self.pipeline_code)

        print(f"✓ Saved instrumented pipeline: {output_path}")


def parse_thresholds(threshold_str: str) -> Dict[str, float]:
    """Parse threshold string into dict."""
    thresholds = {}
    for pair in threshold_str.split(","):
        metric, value = pair.split("=")
        thresholds[metric.strip()] = float(value.strip())
    return thresholds


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Add monitoring and alerting to forecasting pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add basic monitoring
  python add_monitoring.py --pipeline pipelines/forecast_dag.py --metrics smape,mase

  # Set custom thresholds
  python add_monitoring.py --pipeline pipelines/forecast_dag.py \\
      --metrics smape,mase --thresholds smape=15,mase=1.2

  # Configure alerts
  python add_monitoring.py --pipeline pipelines/run_forecast.py \\
      --alerts email,slack --metrics smape,mae

  # Save to different file
  python add_monitoring.py --pipeline pipelines/forecast_dag.py \\
      --metrics smape --output pipelines/forecast_dag_monitored.py
        """,
    )

    parser.add_argument("--pipeline", required=True, help="Path to pipeline file to instrument")

    parser.add_argument(
        "--metrics", required=True, help="Comma-separated metrics to track (e.g., smape,mase,mae)"
    )

    parser.add_argument("--thresholds", help="Metric thresholds (e.g., smape=20,mase=1.5)")

    parser.add_argument("--alerts", help="Alert channels (e.g., email,slack,pagerduty)")

    parser.add_argument("--output", help="Output path (default: overwrite with backup)")

    args = parser.parse_args()

    try:
        # Parse arguments
        metrics = [m.strip() for m in args.metrics.split(",")]
        thresholds = parse_thresholds(args.thresholds) if args.thresholds else None
        alerts = [a.strip() for a in args.alerts.split(",")] if args.alerts else None

        # Validate metrics
        invalid = [m for m in metrics if m not in MonitoringInjector.SUPPORTED_METRICS]
        if invalid:
            print(f"❌ Invalid metrics: {invalid}")
            print(f"Supported: {MonitoringInjector.SUPPORTED_METRICS}")
            return 1

        # Generate monitoring code
        injector = MonitoringInjector(args.pipeline)
        injector.load_pipeline()

        print(f"Adding monitoring: {', '.join(metrics)}")
        modified_code = injector.add_monitoring(metrics, thresholds, alerts)

        injector.pipeline_code = modified_code
        injector.save(args.output)

        print("\n✓ Monitoring added successfully!")
        print("\nNext steps:")
        print("  1. Review instrumented pipeline")
        print("  2. Configure alert channels (SLACK_WEBHOOK_URL, etc.)")
        print("  3. Test monitoring with real data")
        print("  4. Deploy updated pipeline")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
