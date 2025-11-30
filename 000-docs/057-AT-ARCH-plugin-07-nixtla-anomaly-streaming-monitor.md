# Plugin #7: Nixtla Anomaly Streaming Monitor
**Technical Architecture & Implementation Specification**

**Created**: 2025-11-30
**Status**: Design Phase
**Priority**: Tier 2 (PRODUCTION WIN)
**Addresses**: POC-to-Production Chasm (Friction #2)

---

## Executive Summary

### What It Is
A real-time streaming anomaly detection plugin that processes Kafka/Kinesis streams with sub-second latency, using Nixtla's TimeGPT for anomaly detection with automatic alerting and dashboard visualization.

### Why It Exists
Nixtla's CRO observes:
> "Users don't trust TimeGPT in production yet. They need proven real-time capabilities with bulletproof monitoring."

**This plugin demonstrates production-grade streaming anomaly detection.**

### Who It's For
- **FinTech teams** detecting payment fraud in real-time
- **SRE teams** monitoring infrastructure metrics
- **E-commerce** detecting inventory anomalies
- **IoT platforms** processing sensor streams

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  DATA SOURCES                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Kafka Stream  │  │Kinesis Stream│  │HTTP Webhooks │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  MCP SERVER (TypeScript) - Stream Processor                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  - Kafka consumer (node-rdkafka)                     │  │
│  │  - AWS Kinesis consumer                              │  │
│  │  - Webhook server (Express)                          │  │
│  │  - Buffer management (sliding windows)               │  │
│  │  - Alerting engine (PagerDuty/Slack)                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  PYTHON WORKER - Anomaly Detection                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  - Nixtla anomaly detection                          │  │
│  │  - Batch processing (100 events/call)                │  │
│  │  - Result caching (Redis)                            │  │
│  │  - Metrics export (Prometheus)                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUTS                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Grafana       │  │PagerDuty     │  │Slack Alerts  │      │
│  │Dashboard     │  │Incidents     │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Plugin Type
**Hybrid Architecture**:
- **MCP Server** (TypeScript) - Stream ingestion and buffering
- **Python Worker** - Nixtla anomaly detection
- **Agent Skill** - Auto-detects streaming patterns

### Components

1. **MCP Server Tools** (6)
   - `stream_monitor_start` - Start monitoring a Kafka/Kinesis stream
   - `stream_monitor_stop` - Stop monitoring
   - `stream_health_check` - Check consumer lag and throughput
   - `configure_alerts` - Set up PagerDuty/Slack alerts
   - `get_anomaly_stats` - Real-time anomaly statistics
   - `export_dashboard_config` - Generate Grafana dashboard JSON

2. **Slash Commands** (3)
   - `/nixtla-monitor-stream` - Quick start stream monitoring
   - `/nixtla-alert-setup` - Configure alert rules
   - `/nixtla-stream-dashboard` - Generate monitoring dashboard

3. **Agent Skill** (1)
   - `nixtla-streaming-expert` - Auto-invoked for streaming queries

4. **Lifecycle Hooks** (1)
   - PostToolUse on Bash/Write - Detect stream processing code

---

## API Keys & User Requirements

### Required
```bash
# Nixtla API
NIXTLA_API_KEY=nixak-...

# Kafka (if using Kafka)
KAFKA_BROKERS=broker1:9092,broker2:9092
KAFKA_GROUP_ID=nixtla-anomaly-monitor
# Optional: SASL auth
KAFKA_SASL_USERNAME=...
KAFKA_SASL_PASSWORD=...

# AWS Kinesis (if using Kinesis)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# Alerting (choose one or more)
PAGERDUTY_API_KEY=...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Monitoring (optional)
REDIS_URL=redis://localhost:6379
PROMETHEUS_PORT=9090
```

### User Requirements

#### Minimum
- **Python 3.10+** for Nixtla anomaly detection
- **Node.js 20+** for MCP server (stream processing)
- **Kafka** 2.8+ OR **AWS Kinesis** (stream source)
- **Redis** (optional, for caching)
- **2 CPU cores** minimum (stream processing + anomaly detection)

#### Recommended
- **4 CPU cores** for parallel processing
- **8 GB RAM** for buffer management
- **Redis cluster** for distributed caching
- **Prometheus + Grafana** for monitoring

---

## Code Implementation

### Directory Structure

```
plugins/nixtla-anomaly-streaming-monitor/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── nixtla-monitor-stream.md
│   ├── nixtla-alert-setup.md
│   └── nixtla-stream-dashboard.md
├── skills/
│   └── SKILL.md
├── mcp/
│   ├── server.json
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── index.ts              # MCP server entry
│   │   ├── kafka-consumer.ts     # Kafka integration
│   │   ├── kinesis-consumer.ts   # Kinesis integration
│   │   ├── webhook-server.ts     # HTTP webhooks
│   │   ├── buffer-manager.ts     # Sliding window buffers
│   │   ├── alerting-engine.ts    # PagerDuty/Slack
│   │   └── types.ts              # TypeScript types
│   └── dist/                     # Compiled JavaScript
├── src/
│   ├── __init__.py
│   ├── anomaly_detector.py       # Nixtla integration
│   ├── batch_processor.py        # Batch API calls
│   ├── cache_manager.py          # Redis caching
│   └── metrics_exporter.py       # Prometheus metrics
├── config/
│   ├── kafka-example.yaml
│   ├── kinesis-example.yaml
│   └── alert-rules.yaml
├── dashboards/
│   └── grafana-anomaly-monitor.json
├── requirements.txt
├── package.json
└── setup.sh
```

---

## MCP Server Implementation (TypeScript)

### mcp/server.json

```json
{
  "name": "nixtla-anomaly-streaming-monitor",
  "version": "1.0.0",
  "description": "Real-time anomaly detection on Kafka/Kinesis streams",
  "main": "dist/index.js",
  "tools": [
    {
      "name": "stream_monitor_start",
      "description": "Start monitoring a Kafka or Kinesis stream for anomalies",
      "parameters": {
        "type": "object",
        "properties": {
          "stream_type": {
            "type": "string",
            "enum": ["kafka", "kinesis", "webhook"],
            "description": "Type of stream to monitor"
          },
          "stream_config": {
            "type": "object",
            "description": "Stream-specific configuration (topics, ARN, etc.)"
          },
          "window_size_seconds": {
            "type": "number",
            "description": "Sliding window size for batching events",
            "default": 60
          },
          "anomaly_threshold": {
            "type": "number",
            "description": "Anomaly score threshold (0-1)",
            "default": 0.8
          }
        },
        "required": ["stream_type", "stream_config"]
      }
    },
    {
      "name": "stream_monitor_stop",
      "description": "Stop monitoring a stream",
      "parameters": {
        "type": "object",
        "properties": {
          "monitor_id": {
            "type": "string",
            "description": "Monitor ID returned by stream_monitor_start"
          }
        },
        "required": ["monitor_id"]
      }
    },
    {
      "name": "stream_health_check",
      "description": "Check stream consumer health (lag, throughput, errors)",
      "parameters": {
        "type": "object",
        "properties": {
          "monitor_id": {
            "type": "string",
            "description": "Monitor ID"
          }
        },
        "required": ["monitor_id"]
      }
    },
    {
      "name": "configure_alerts",
      "description": "Configure alerting rules for anomalies",
      "parameters": {
        "type": "object",
        "properties": {
          "monitor_id": {
            "type": "string"
          },
          "alert_channels": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": ["pagerduty", "slack", "email"]
            }
          },
          "severity_threshold": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"],
            "default": "high"
          },
          "cooldown_minutes": {
            "type": "number",
            "description": "Minimum time between alerts for same series",
            "default": 15
          }
        },
        "required": ["monitor_id", "alert_channels"]
      }
    },
    {
      "name": "get_anomaly_stats",
      "description": "Get real-time anomaly statistics",
      "parameters": {
        "type": "object",
        "properties": {
          "monitor_id": {
            "type": "string"
          },
          "last_n_minutes": {
            "type": "number",
            "default": 60
          }
        },
        "required": ["monitor_id"]
      }
    },
    {
      "name": "export_dashboard_config",
      "description": "Generate Grafana dashboard JSON for monitoring",
      "parameters": {
        "type": "object",
        "properties": {
          "monitor_id": {
            "type": "string"
          },
          "include_prometheus": {
            "type": "boolean",
            "default": true
          }
        },
        "required": ["monitor_id"]
      }
    }
  ]
}
```

### mcp/src/index.ts

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import { KafkaConsumer } from './kafka-consumer.js';
import { KinesisConsumer } from './kinesis-consumer.js';
import { WebhookServer } from './webhook-server.js';
import { BufferManager } from './buffer-manager.js';
import { AlertingEngine } from './alerting-engine.js';
import { StreamMonitor, StreamConfig, HealthStats, AnomalyStats } from './types.js';

class NixtlaStreamingMonitorServer {
  private server: Server;
  private monitors: Map<string, StreamMonitor>;
  private bufferManager: BufferManager;
  private alertingEngine: AlertingEngine;

  constructor() {
    this.server = new Server(
      {
        name: 'nixtla-anomaly-streaming-monitor',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.monitors = new Map();
    this.bufferManager = new BufferManager();
    this.alertingEngine = new AlertingEngine();

    this.setupHandlers();
  }

  private setupHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'stream_monitor_start',
          description: 'Start monitoring a Kafka or Kinesis stream for anomalies',
          inputSchema: {
            type: 'object',
            properties: {
              stream_type: {
                type: 'string',
                enum: ['kafka', 'kinesis', 'webhook'],
              },
              stream_config: { type: 'object' },
              window_size_seconds: { type: 'number', default: 60 },
              anomaly_threshold: { type: 'number', default: 0.8 },
            },
            required: ['stream_type', 'stream_config'],
          },
        },
        {
          name: 'stream_monitor_stop',
          description: 'Stop monitoring a stream',
          inputSchema: {
            type: 'object',
            properties: {
              monitor_id: { type: 'string' },
            },
            required: ['monitor_id'],
          },
        },
        {
          name: 'stream_health_check',
          description: 'Check stream consumer health',
          inputSchema: {
            type: 'object',
            properties: {
              monitor_id: { type: 'string' },
            },
            required: ['monitor_id'],
          },
        },
        {
          name: 'configure_alerts',
          description: 'Configure alerting rules',
          inputSchema: {
            type: 'object',
            properties: {
              monitor_id: { type: 'string' },
              alert_channels: { type: 'array', items: { type: 'string' } },
              severity_threshold: { type: 'string', default: 'high' },
              cooldown_minutes: { type: 'number', default: 15 },
            },
            required: ['monitor_id', 'alert_channels'],
          },
        },
        {
          name: 'get_anomaly_stats',
          description: 'Get real-time anomaly statistics',
          inputSchema: {
            type: 'object',
            properties: {
              monitor_id: { type: 'string' },
              last_n_minutes: { type: 'number', default: 60 },
            },
            required: ['monitor_id'],
          },
        },
        {
          name: 'export_dashboard_config',
          description: 'Generate Grafana dashboard JSON',
          inputSchema: {
            type: 'object',
            properties: {
              monitor_id: { type: 'string' },
              include_prometheus: { type: 'boolean', default: true },
            },
            required: ['monitor_id'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      switch (request.params.name) {
        case 'stream_monitor_start':
          return this.handleStreamMonitorStart(request.params.arguments);
        case 'stream_monitor_stop':
          return this.handleStreamMonitorStop(request.params.arguments);
        case 'stream_health_check':
          return this.handleHealthCheck(request.params.arguments);
        case 'configure_alerts':
          return this.handleConfigureAlerts(request.params.arguments);
        case 'get_anomaly_stats':
          return this.handleGetAnomalyStats(request.params.arguments);
        case 'export_dashboard_config':
          return this.handleExportDashboard(request.params.arguments);
        default:
          throw new Error(`Unknown tool: ${request.params.name}`);
      }
    });
  }

  private async handleStreamMonitorStart(args: any) {
    const {
      stream_type,
      stream_config,
      window_size_seconds = 60,
      anomaly_threshold = 0.8,
    } = args;

    const monitor_id = `monitor-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    let consumer;
    switch (stream_type) {
      case 'kafka':
        consumer = new KafkaConsumer(stream_config);
        break;
      case 'kinesis':
        consumer = new KinesisConsumer(stream_config);
        break;
      case 'webhook':
        consumer = new WebhookServer(stream_config);
        break;
      default:
        throw new Error(`Unsupported stream type: ${stream_type}`);
    }

    // Start consuming
    await consumer.start((event) => {
      this.bufferManager.addEvent(monitor_id, event);
    });

    // Start processing loop
    this.startProcessingLoop(monitor_id, window_size_seconds, anomaly_threshold);

    const monitor: StreamMonitor = {
      id: monitor_id,
      stream_type,
      consumer,
      started_at: new Date(),
      config: { window_size_seconds, anomaly_threshold },
      stats: {
        events_processed: 0,
        anomalies_detected: 0,
        alerts_sent: 0,
      },
    };

    this.monitors.set(monitor_id, monitor);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            monitor_id,
            status: 'started',
            stream_type,
            window_size_seconds,
            anomaly_threshold,
            message: `Streaming monitor started. Processing ${stream_type} events in ${window_size_seconds}s windows.`,
          }, null, 2),
        },
      ],
    };
  }

  private async handleStreamMonitorStop(args: any) {
    const { monitor_id } = args;

    const monitor = this.monitors.get(monitor_id);
    if (!monitor) {
      throw new Error(`Monitor not found: ${monitor_id}`);
    }

    await monitor.consumer.stop();
    this.monitors.delete(monitor_id);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            monitor_id,
            status: 'stopped',
            final_stats: monitor.stats,
            runtime_seconds: Math.floor((Date.now() - monitor.started_at.getTime()) / 1000),
          }, null, 2),
        },
      ],
    };
  }

  private async handleHealthCheck(args: any) {
    const { monitor_id } = args;

    const monitor = this.monitors.get(monitor_id);
    if (!monitor) {
      throw new Error(`Monitor not found: ${monitor_id}`);
    }

    const consumerHealth = await monitor.consumer.getHealth();
    const bufferStats = this.bufferManager.getStats(monitor_id);

    const health: HealthStats = {
      monitor_id,
      status: consumerHealth.lag > 1000 ? 'degraded' : 'healthy',
      consumer_lag: consumerHealth.lag,
      throughput_events_per_sec: consumerHealth.throughput,
      buffer_size: bufferStats.current_size,
      buffer_max_size: bufferStats.max_size,
      uptime_seconds: Math.floor((Date.now() - monitor.started_at.getTime()) / 1000),
      stats: monitor.stats,
    };

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(health, null, 2),
        },
      ],
    };
  }

  private async handleConfigureAlerts(args: any) {
    const { monitor_id, alert_channels, severity_threshold, cooldown_minutes } = args;

    const monitor = this.monitors.get(monitor_id);
    if (!monitor) {
      throw new Error(`Monitor not found: ${monitor_id}`);
    }

    this.alertingEngine.configure(monitor_id, {
      channels: alert_channels,
      severity_threshold,
      cooldown_minutes,
    });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            monitor_id,
            alert_channels,
            severity_threshold,
            cooldown_minutes,
            message: 'Alert configuration updated',
          }, null, 2),
        },
      ],
    };
  }

  private async handleGetAnomalyStats(args: any) {
    const { monitor_id, last_n_minutes } = args;

    const monitor = this.monitors.get(monitor_id);
    if (!monitor) {
      throw new Error(`Monitor not found: ${monitor_id}`);
    }

    const stats = this.bufferManager.getAnomalyStats(monitor_id, last_n_minutes);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(stats, null, 2),
        },
      ],
    };
  }

  private async handleExportDashboard(args: any) {
    const { monitor_id, include_prometheus } = args;

    const monitor = this.monitors.get(monitor_id);
    if (!monitor) {
      throw new Error(`Monitor not found: ${monitor_id}`);
    }

    const dashboardConfig = this.generateGrafanaDashboard(monitor, include_prometheus);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            monitor_id,
            dashboard_config: dashboardConfig,
            import_instructions: 'Import this JSON into Grafana via Dashboard → Import',
          }, null, 2),
        },
      ],
    };
  }

  private startProcessingLoop(monitor_id: string, window_size_seconds: number, threshold: number) {
    setInterval(async () => {
      const events = this.bufferManager.getWindow(monitor_id, window_size_seconds);
      if (events.length === 0) return;

      // Call Python worker for anomaly detection
      const anomalies = await this.callPythonWorker(events, threshold);

      const monitor = this.monitors.get(monitor_id);
      if (!monitor) return;

      monitor.stats.events_processed += events.length;
      monitor.stats.anomalies_detected += anomalies.length;

      // Send alerts
      for (const anomaly of anomalies) {
        const alertSent = await this.alertingEngine.sendAlert(monitor_id, anomaly);
        if (alertSent) {
          monitor.stats.alerts_sent++;
        }
      }
    }, window_size_seconds * 1000);
  }

  private async callPythonWorker(events: any[], threshold: number): Promise<any[]> {
    // Spawn Python process to run Nixtla anomaly detection
    const { spawn } = await import('child_process');

    return new Promise((resolve, reject) => {
      const python = spawn('python3', [
        '-m', 'nixtla_anomaly_streaming_monitor.batch_processor',
        '--threshold', threshold.toString(),
      ]);

      python.stdin.write(JSON.stringify(events));
      python.stdin.end();

      let output = '';
      python.stdout.on('data', (data) => {
        output += data.toString();
      });

      python.on('close', (code) => {
        if (code === 0) {
          resolve(JSON.parse(output));
        } else {
          reject(new Error(`Python worker exited with code ${code}`));
        }
      });
    });
  }

  private generateGrafanaDashboard(monitor: StreamMonitor, includePrometheus: boolean) {
    // Generate Grafana dashboard JSON
    return {
      dashboard: {
        title: `Nixtla Anomaly Monitor - ${monitor.id}`,
        panels: [
          {
            title: 'Events Processed (Rate)',
            type: 'graph',
            targets: includePrometheus ? [
              { expr: `rate(nixtla_events_processed{monitor="${monitor.id}"}[5m])` }
            ] : [],
          },
          {
            title: 'Anomalies Detected',
            type: 'graph',
            targets: includePrometheus ? [
              { expr: `nixtla_anomalies_detected{monitor="${monitor.id}"}` }
            ] : [],
          },
          {
            title: 'Consumer Lag',
            type: 'gauge',
            targets: includePrometheus ? [
              { expr: `nixtla_consumer_lag{monitor="${monitor.id}"}` }
            ] : [],
          },
        ],
      },
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Nixtla Anomaly Streaming Monitor MCP server running on stdio');
  }
}

const server = new NixtlaStreamingMonitorServer();
server.run().catch(console.error);
```

### mcp/src/kafka-consumer.ts

```typescript
import * as Kafka from 'node-rdkafka';

export interface KafkaConfig {
  brokers: string[];
  topics: string[];
  group_id: string;
  sasl?: {
    username: string;
    password: string;
    mechanism: 'PLAIN' | 'SCRAM-SHA-256' | 'SCRAM-SHA-512';
  };
}

export class KafkaConsumer {
  private consumer: Kafka.KafkaConsumer | null = null;
  private config: KafkaConfig;
  private isRunning: boolean = false;
  private eventsProcessed: number = 0;
  private lastCheckTime: number = Date.now();

  constructor(config: KafkaConfig) {
    this.config = config;
  }

  async start(onMessage: (event: any) => void): Promise<void> {
    const kafkaConfig: any = {
      'group.id': this.config.group_id,
      'metadata.broker.list': this.config.brokers.join(','),
      'enable.auto.commit': true,
      'auto.offset.reset': 'latest',
    };

    if (this.config.sasl) {
      kafkaConfig['security.protocol'] = 'SASL_SSL';
      kafkaConfig['sasl.mechanism'] = this.config.sasl.mechanism;
      kafkaConfig['sasl.username'] = this.config.sasl.username;
      kafkaConfig['sasl.password'] = this.config.sasl.password;
    }

    this.consumer = new Kafka.KafkaConsumer(kafkaConfig, {});

    this.consumer.connect();

    this.consumer.on('ready', () => {
      console.error('Kafka consumer ready');
      this.consumer!.subscribe(this.config.topics);
      this.consumer!.consume();
      this.isRunning = true;
    });

    this.consumer.on('data', (message) => {
      try {
        const event = JSON.parse(message.value?.toString() || '{}');
        this.eventsProcessed++;
        onMessage(event);
      } catch (err) {
        console.error('Failed to parse Kafka message:', err);
      }
    });

    this.consumer.on('event.error', (err) => {
      console.error('Kafka consumer error:', err);
    });
  }

  async stop(): Promise<void> {
    if (this.consumer) {
      this.consumer.disconnect();
      this.isRunning = false;
    }
  }

  async getHealth(): Promise<{ lag: number; throughput: number }> {
    // Get consumer lag from Kafka
    const lag = 0; // TODO: Implement actual lag calculation

    // Calculate throughput
    const now = Date.now();
    const elapsedSeconds = (now - this.lastCheckTime) / 1000;
    const throughput = this.eventsProcessed / elapsedSeconds;

    this.lastCheckTime = now;
    this.eventsProcessed = 0;

    return { lag, throughput };
  }
}
```

---

## Python Worker Implementation

### src/anomaly_detector.py

```python
"""
Nixtla anomaly detection worker
"""
from typing import List, Dict, Any, Optional
import pandas as pd
from nixtla import NixtlaClient
import os
from datetime import datetime


class NixtlaAnomalyDetector:
    """Detect anomalies using Nixtla TimeGPT"""

    def __init__(self, api_key: Optional[str] = None):
        self.client = NixtlaClient(api_key=api_key or os.environ.get('NIXTLA_API_KEY'))

    def detect_anomalies(
        self,
        events: List[Dict[str, Any]],
        threshold: float = 0.8
    ) -> List[Dict[str, Any]]:
        """
        Detect anomalies in streaming events

        Args:
            events: List of events with 'timestamp', 'value', 'series_id'
            threshold: Anomaly score threshold (0-1)

        Returns:
            List of anomalies with scores and context
        """
        if not events:
            return []

        # Convert to DataFrame in Nixtla format
        df = pd.DataFrame([
            {
                'unique_id': e.get('series_id', 'default'),
                'ds': pd.to_datetime(e['timestamp']),
                'y': float(e['value'])
            }
            for e in events
        ])

        # Run anomaly detection
        anomalies_df = self.client.detect_anomalies(
            df=df,
            freq='auto',  # Auto-detect frequency
            level=95      # 95% confidence interval
        )

        # Filter by threshold
        anomalies = []
        for _, row in anomalies_df.iterrows():
            if row.get('anomaly', 0) > threshold:
                anomalies.append({
                    'series_id': row['unique_id'],
                    'timestamp': row['ds'].isoformat(),
                    'value': float(row['y']),
                    'anomaly_score': float(row['anomaly']),
                    'expected_value': float(row.get('TimeGPT', 0)),
                    'deviation_pct': abs((row['y'] - row.get('TimeGPT', 0)) / row.get('TimeGPT', 1)) * 100
                })

        return anomalies
```

### src/batch_processor.py

```python
"""
Batch processor for streaming events
"""
import sys
import json
import argparse
from typing import List, Dict, Any
from anomaly_detector import NixtlaAnomalyDetector


def process_batch(events: List[Dict[str, Any]], threshold: float) -> List[Dict[str, Any]]:
    """
    Process a batch of events for anomaly detection

    Args:
        events: List of streaming events
        threshold: Anomaly score threshold

    Returns:
        List of detected anomalies
    """
    detector = NixtlaAnomalyDetector()
    anomalies = detector.detect_anomalies(events, threshold)
    return anomalies


def main():
    parser = argparse.ArgumentParser(description='Batch anomaly detection')
    parser.add_argument('--threshold', type=float, default=0.8, help='Anomaly threshold')
    args = parser.parse_args()

    # Read events from stdin (sent by TypeScript MCP server)
    events = json.load(sys.stdin)

    # Process batch
    anomalies = process_batch(events, args.threshold)

    # Write results to stdout
    print(json.dumps(anomalies))


if __name__ == '__main__':
    main()
```

### src/cache_manager.py

```python
"""
Redis caching for anomaly detection results
"""
from typing import Optional, List, Dict, Any
import redis
import json
import hashlib
import os


class CacheManager:
    """Manage Redis cache for anomaly detection"""

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_url = redis_url or os.environ.get('REDIS_URL', 'redis://localhost:6379')
        self.client = redis.from_url(self.redis_url, decode_responses=True)
        self.ttl_seconds = 3600  # 1 hour cache

    def get_cached_result(self, events: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        """Get cached anomaly detection result"""
        cache_key = self._generate_cache_key(events)
        cached = self.client.get(cache_key)

        if cached:
            return json.loads(cached)
        return None

    def cache_result(self, events: List[Dict[str, Any]], anomalies: List[Dict[str, Any]]):
        """Cache anomaly detection result"""
        cache_key = self._generate_cache_key(events)
        self.client.setex(
            cache_key,
            self.ttl_seconds,
            json.dumps(anomalies)
        )

    def _generate_cache_key(self, events: List[Dict[str, Any]]) -> str:
        """Generate cache key from events"""
        events_str = json.dumps(events, sort_keys=True)
        return f"nixtla:anomaly:{hashlib.sha256(events_str.encode()).hexdigest()}"
```

### src/metrics_exporter.py

```python
"""
Prometheus metrics exporter
"""
from prometheus_client import Counter, Gauge, Histogram, start_http_server
import os


# Metrics
events_processed = Counter(
    'nixtla_events_processed_total',
    'Total events processed',
    ['monitor']
)

anomalies_detected = Counter(
    'nixtla_anomalies_detected_total',
    'Total anomalies detected',
    ['monitor']
)

alerts_sent = Counter(
    'nixtla_alerts_sent_total',
    'Total alerts sent',
    ['monitor', 'channel']
)

consumer_lag = Gauge(
    'nixtla_consumer_lag',
    'Consumer lag',
    ['monitor']
)

processing_duration = Histogram(
    'nixtla_processing_duration_seconds',
    'Processing duration',
    ['monitor']
)


def start_metrics_server(port: int = 9090):
    """Start Prometheus metrics HTTP server"""
    start_http_server(port)
    print(f"Metrics server started on port {port}")
```

---

## Example Usage

### Slash Command: /nixtla-monitor-stream

```markdown
# /nixtla-monitor-stream

Start real-time anomaly monitoring on a Kafka stream

## Usage
/nixtla-monitor-stream --topic payments --window 60 --threshold 0.8

## Parameters
- `--topic` - Kafka topic name
- `--window` - Window size in seconds (default: 60)
- `--threshold` - Anomaly threshold 0-1 (default: 0.8)
- `--alerts` - Alert channels: pagerduty,slack (optional)
```

**Example Execution**:

```bash
User: /nixtla-monitor-stream --topic payments --alerts slack

Claude: Starting Kafka stream monitor...

        ✅ Connected to Kafka (3 brokers)
        ✅ Subscribed to topic: payments
        ✅ Nixtla API validated
        ✅ Slack alerts configured

        Monitor ID: monitor-1701234567-abc123
        Window size: 60 seconds
        Anomaly threshold: 0.8

        Processing events in real-time...

        📊 Stats (last 60s):
        - Events processed: 1,247
        - Anomalies detected: 3
        - Alerts sent: 1

        🚨 ANOMALY DETECTED:
        Series: payment_processor_2
        Timestamp: 2025-11-30T14:23:45Z
        Value: $15,234.50
        Expected: $2,100.00
        Deviation: +625%
        Anomaly score: 0.94

        Alert sent to: #fraud-detection
```

---

## User Journeys

### Journey 1: FinTech Payment Fraud Detection

**Persona**: Carlos, Security Engineer at PaymentCo
**Goal**: Detect fraudulent payment patterns in real-time
**Context**: Processing 10,000 payments/minute across 50 merchant accounts

**Before**:
```
Carlos: "We need real-time fraud detection"
Data Science: "We can batch process every 15 minutes"
Carlos: "That's too slow, fraudsters will be gone"
```

**After (with Nixtla Streaming Monitor)**:

1. **Setup Stream Monitor**
   ```bash
   Claude: /nixtla-monitor-stream --topic payments --window 30 --alerts pagerduty

   Monitor started:
   - Topic: payments
   - Window: 30 seconds
   - Threshold: 0.85
   - Alert: PagerDuty (P1 incidents)

   Processing 167 events/second...
   ```

2. **Detect Anomaly in Real-Time**
   ```
   14:23:45 - 🚨 ANOMALY DETECTED

   Merchant: merchant_12345
   Transaction: $9,850.00
   Expected range: $50-$200
   Deviation: +4,825%
   Anomaly score: 0.97

   Historical pattern:
   - Avg transaction: $87.50
   - Max 30 days: $350.00
   - This is 28x normal

   ⚡ PagerDuty incident created: INC-7834
   ⚡ Transaction flagged for manual review
   ```

3. **Investigate via Dashboard**
   ```
   Carlos: /nixtla-stream-dashboard --monitor monitor-abc123

   Grafana dashboard generated:
   - Real-time anomaly feed
   - Per-merchant timeseries
   - Anomaly score heatmap
   - Alert history

   Import URL: http://grafana.paymentco.com/d/nixtla-abc123
   ```

4. **Confirm Fraud Prevented**
   ```
   Outcome:
   - Anomaly detected: 2.3 seconds after transaction
   - Fraudster account frozen before attempting 9 more transactions
   - Prevented loss: ~$95,000
   - Detection latency: Sub-second
   ```

**Outcome**: Carlos prevents $95k fraud loss with sub-second detection latency, far faster than 15-minute batch processing.

---

### Journey 2: SRE Infrastructure Monitoring

**Persona**: Priya, SRE Lead at E-CommerceGiant
**Goal**: Monitor CPU/memory metrics for 500 microservices
**Context**: Black Friday traffic surge, need instant alerts

**Steps**:

1. **Monitor Infrastructure Metrics**
   ```bash
   Priya: "Monitor our Kinesis stream for CPU anomalies"

   Claude: [Auto-invokes nixtla-streaming-expert skill]

           Starting Kinesis monitor...

           Stream: prod-metrics-stream
           Window: 60 seconds
           Series: 500 microservices
           Alert: Slack #oncall

           Monitoring CPU utilization...
   ```

2. **Detect Capacity Issue**
   ```
   15:42:18 - 🚨 ANOMALY DETECTED

   Service: checkout-api-pod-47
   Metric: cpu_utilization
   Value: 94%
   Expected: 45-65%
   Anomaly score: 0.89

   Pattern:
   - Normal range: 50-70%
   - Spike started: 3 minutes ago
   - Trending: Upward

   ⚡ Alert sent to #oncall
   ⚡ Auto-scaling triggered (3 → 8 pods)
   ```

3. **Validate Fix**
   ```
   15:45:30 - ✅ ANOMALY RESOLVED

   Service: checkout-api
   CPU utilization: 58% (normalized)
   Auto-scaling: 8 pods running
   Latency: p99 reduced from 2.1s → 450ms
   ```

**Outcome**: Priya prevents Black Friday checkout outage with 3-minute anomaly detection and auto-scaling, saving millions in lost sales.

---

### Journey 3: IoT Sensor Monitoring

**Persona**: Ahmed, IoT Engineer at ManufacturingCorp
**Goal**: Monitor 1,000 temperature sensors in real-time
**Context**: Manufacturing plant, equipment failures cost $50k/hour

**Steps**:

1. **Setup Webhook Ingestion**
   ```bash
   Ahmed: /nixtla-monitor-stream --stream webhook --port 8080

   Webhook server started:
   - URL: http://iot-monitor.mfg.com:8080/events
   - Format: JSON {sensor_id, timestamp, temperature}
   - Window: 120 seconds (2 minutes)
   - Threshold: 0.80

   Waiting for events...
   ```

2. **Detect Equipment Failure**
   ```
   10:15:23 - 🚨 CRITICAL ANOMALY

   Sensor: furnace_3_temp_sensor
   Temperature: 1,450°C
   Expected: 800-850°C
   Anomaly score: 0.96

   Risk Assessment:
   - Equipment damage: HIGH
   - Safety risk: CRITICAL
   - Recommended action: EMERGENCY SHUTDOWN

   ⚡ PagerDuty incident: INC-9912 (P0)
   ⚡ SMS sent to: Plant Manager, Safety Team
   ```

3. **Emergency Response**
   ```
   10:16:05 - Furnace 3 emergency shutdown initiated
   10:17:30 - Equipment inspection started
   10:45:00 - Faulty heating element identified

   Outcome:
   - Anomaly → Alert: 42 seconds
   - Equipment damage prevented: $250k+
   - Production downtime: 4 hours (vs 2 weeks for full replacement)
   ```

**Outcome**: Ahmed prevents catastrophic equipment failure with sub-minute anomaly detection, saving $250k+ in equipment damage.

---

## Dependencies

### Python Requirements

```txt
# requirements.txt
nixtla>=0.7.1
pandas>=2.0.0
redis>=5.0.0
prometheus-client>=0.19.0
python-dotenv>=1.0.1
pyyaml>=6.0.1
```

### Node.js/TypeScript Requirements

```json
{
  "name": "nixtla-anomaly-streaming-monitor-mcp",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "node-rdkafka": "^3.0.0",
    "@aws-sdk/client-kinesis": "^3.0.0",
    "express": "^4.18.0",
    "redis": "^4.6.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.3.0"
  }
}
```

---

## Installation Script

### setup.sh

```bash
#!/usr/bin/env bash
set -e

echo "🚀 Setting up Nixtla Anomaly Streaming Monitor..."

# Check dependencies
command -v python3 >/dev/null 2>&1 || { echo "Python 3.10+ required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js 20+ required"; exit 1; }
command -v pnpm >/dev/null 2>&1 || { echo "pnpm required (npm install -g pnpm)"; exit 1; }

# Python setup
echo "📦 Installing Python dependencies..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# TypeScript MCP server setup
echo "📦 Installing Node.js dependencies..."
cd mcp
pnpm install

# Build TypeScript
echo "🔨 Building MCP server..."
pnpm build

cd ..

# Validate environment
echo "✅ Checking environment variables..."
if [ -z "$NIXTLA_API_KEY" ]; then
    echo "⚠️  Warning: NIXTLA_API_KEY not set"
fi

# Test connections
echo "🧪 Testing connections..."
python3 -c "from src.anomaly_detector import NixtlaAnomalyDetector; print('✅ Nixtla client OK')"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Required environment variables:"
echo "  - NIXTLA_API_KEY=nixak-..."
echo "  - KAFKA_BROKERS=broker1:9092,broker2:9092 (if using Kafka)"
echo "  - AWS_ACCESS_KEY_ID=... (if using Kinesis)"
echo "  - SLACK_WEBHOOK_URL=... (for alerts)"
echo ""
echo "Start monitoring:"
echo "  /nixtla-monitor-stream --topic my-topic --alerts slack"
```

---

## Monitoring & Observability

### Prometheus Metrics Exported

```
# Events processed
nixtla_events_processed_total{monitor="monitor-abc123"} 125847

# Anomalies detected
nixtla_anomalies_detected_total{monitor="monitor-abc123"} 23

# Alerts sent
nixtla_alerts_sent_total{monitor="monitor-abc123",channel="slack"} 8

# Consumer lag
nixtla_consumer_lag{monitor="monitor-abc123"} 0

# Processing duration
nixtla_processing_duration_seconds_bucket{monitor="monitor-abc123",le="0.5"} 1234
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Nixtla Anomaly Monitor",
    "panels": [
      {
        "title": "Events/sec",
        "type": "graph",
        "targets": [
          {"expr": "rate(nixtla_events_processed_total[5m])"}
        ]
      },
      {
        "title": "Anomaly Rate",
        "type": "graph",
        "targets": [
          {"expr": "rate(nixtla_anomalies_detected_total[5m])"}
        ]
      },
      {
        "title": "Consumer Lag",
        "type": "gauge",
        "targets": [
          {"expr": "nixtla_consumer_lag"}
        ]
      }
    ]
  }
}
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-30
**Language**: TypeScript (MCP server) + Python (anomaly detection)
**Note**: Requires Kafka/Kinesis infrastructure
