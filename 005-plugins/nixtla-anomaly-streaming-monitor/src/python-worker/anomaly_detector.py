#!/usr/bin/env python3
"""Anomaly detection worker using Nixtla TimeGPT."""

import os
from typing import Optional

import pandas as pd
from nixtla import NixtlaClient


class AnomalyDetector:
    """Real-time anomaly detection using TimeGPT."""

    def __init__(self, api_key: Optional[str] = None):
        self.client = NixtlaClient(api_key=api_key or os.environ.get("NIXTLA_TIMEGPT_API_KEY"))
        self.batch_size = 100

    def detect_anomalies(
        self,
        df: pd.DataFrame,
        threshold: float = 0.95
    ) -> pd.DataFrame:
        """Detect anomalies in time series data.

        Args:
            df: DataFrame with columns (unique_id, ds, y)
            threshold: Confidence threshold for anomaly detection

        Returns:
            DataFrame with anomaly flags and scores
        """
        result = self.client.detect_anomalies(
            df=df,
            freq="auto",
            level=int(threshold * 100)
        )
        return result

    def process_batch(self, events: list[dict]) -> list[dict]:
        """Process a batch of events for anomaly detection.

        Args:
            events: List of event dictionaries with timestamp and value

        Returns:
            List of events with anomaly flags
        """
        if not events:
            return []

        # Convert to DataFrame
        df = pd.DataFrame(events)
        df = df.rename(columns={"timestamp": "ds", "value": "y"})

        if "unique_id" not in df.columns:
            df["unique_id"] = "default"

        # Run detection
        anomalies = self.detect_anomalies(df)

        # Merge results
        results = []
        for i, event in enumerate(events):
            event_copy = event.copy()
            if i < len(anomalies):
                event_copy["is_anomaly"] = bool(anomalies.iloc[i].get("anomaly", False))
                event_copy["anomaly_score"] = float(anomalies.iloc[i].get("anomaly_score", 0))
            results.append(event_copy)

        return results


if __name__ == "__main__":
    # Test
    detector = AnomalyDetector()
    test_data = [
        {"timestamp": "2024-01-01", "value": 100},
        {"timestamp": "2024-01-02", "value": 102},
        {"timestamp": "2024-01-03", "value": 500},  # Anomaly
        {"timestamp": "2024-01-04", "value": 101},
    ]
    results = detector.process_batch(test_data)
    print(results)
