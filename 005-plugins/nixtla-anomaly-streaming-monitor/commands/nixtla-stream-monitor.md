# /nixtla-stream-monitor

Start real-time anomaly detection on streaming data.

## Usage

```
/nixtla-stream-monitor [source] [--topic=events] [--threshold=0.95]
```

## Workflow

1. Connect to stream source (Kafka/Kinesis/Webhook)
2. Configure anomaly detection parameters
3. Set up alerting channels
4. Start monitoring
5. Export Grafana dashboard

## Parameters

- `source`: Stream source (kafka, kinesis, webhook)
- `--topic`: Topic/stream name
- `--threshold`: Anomaly confidence threshold (0.0-1.0)
- `--alert`: Alert channel (pagerduty, slack, email)

## Output

- Real-time anomaly detection
- PagerDuty/Slack alerts
- Grafana dashboard config
- Prometheus metrics export
