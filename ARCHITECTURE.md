# System Architecture

This document describes the architecture of the **Instrumented & Monitored Order API service** and how observability is implemented across the system.

The system demonstrates production-style monitoring using:

- AWS CloudWatch
- Structured logging
- Custom metrics
- Alerting

---

# Architecture Overview

The Order API is deployed on an **EC2 instance** and instrumented to provide structured logs, metrics, and monitoring data to **AWS CloudWatch**.

Monitoring components provide visibility into:

- Application behaviour
- Performance
- System resource utilization

---

# Architecture Diagram

```
Client
  ↓
Order API (Flask Application)
  ↓
Structured Logs
  ↓
CloudWatch Logs
  ↓
Metric Filters
  ↓
CloudWatch Metrics
  ↓
CloudWatch Dashboard & Alarms
  ↓
SNS Notifications (Email)
```

---

# System Components

## EC2 Instance

The application is deployed on an **AWS EC2 instance (`t3.micro`) running Amazon Linux**.

Responsibilities:

- Hosts the Order API service
- Runs the CloudWatch Agent
- Generates logs and metrics
- Serves HTTP API requests

The instance was provisioned using **Terraform**, ensuring the infrastructure is reproducible.

---

## Order API (Flask Application)

A simple REST API implemented using **Flask** provides the core application functionality.

### API Endpoints

```
POST /orders        - Create an order
GET /orders/{id}   - Retrieve an order
GET /health        - Service health check
```

### Built-in Instrumentation

The application includes built-in observability instrumentation:

- Structured JSON logging
- Correlation IDs (`request_id`)
- Request latency measurement
- Log levels (`INFO`, `WARN`, `ERROR`)

Example log event:

```json
{
  "timestamp": "...",
  "event": "order_created",
  "request_id": "...",
  "order_id": "...",
  "latency_ms": 12.4
}
```

---

## CloudWatch Logs

Application logs are written locally to:

```
/var/log/order-api.log
```

The **CloudWatch Agent** collects these logs and sends them to the CloudWatch log group:

```
/aws/ec2/order-api
```

Structured logging enables easier log analysis and allows **metrics to be extracted from logs**.

---

## Metric Filters

Metric filters convert structured log events into **CloudWatch metrics**.

| Log Event | CloudWatch Metric |
|----------|------------------|
| order_created | orders_created_total |
| order_retrieved | orders_retrieved_total |
| order_not_found | api_errors_total |
| request_completed | request_latency_ms |

These metrics allow application behaviour to be monitored and visualized.

---

## CloudWatch Metrics

Metrics are published under the namespace:

```
OrderAPI
```

### Application Metrics

```
orders_created_total
orders_retrieved_total
api_errors_total
request_latency_ms
```

### Infrastructure Metrics (CloudWatch Agent)

```
CPUUtilization
mem_used_percent
disk_used_percent
```

These metrics provide visibility into both **application performance** and **system health**.

---

## CloudWatch Dashboard

A monitoring dashboard provides a visual overview of system health using the **Golden Signals framework**.

| Golden Signal | Metric |
|---------------|-------|
| Traffic | orders_created_total |
| Errors | api_errors_total |
| Latency | request_latency_ms |
| Saturation | CPU, Memory, Disk |

The dashboard enables operators to quickly detect performance issues or abnormal system behaviour.

---

## CloudWatch Alarms

Three CloudWatch alarms detect abnormal system behaviour:

| Alarm | Trigger |
|------|--------|
| api-errors-high | Error rate exceeds threshold |
| cpu-utilization-high | CPU utilization exceeds 80% |
| api-latency-high | API latency exceeds threshold |

These alarms provide **automated detection of infrastructure and application problems**.

---

## SNS Notifications

Alarm notifications are delivered using an **Amazon SNS topic**:

```
order-api-alerts
```

The SNS topic sends **email alerts** whenever an alarm enters the `ALARM` state.

This ensures operators are immediately informed of system incidents.

---

# Observability Data Flow

```
Application Request
        ↓
Flask API processes request
        ↓
Structured log event generated
        ↓
CloudWatch Agent forwards logs to CloudWatch Logs
        ↓
Metric filters convert log data into metrics
        ↓
Metrics appear in CloudWatch dashboard
        ↓
CloudWatch alarms evaluate metrics
        ↓
SNS sends notifications if thresholds are exceeded
```

---

# Design Considerations

Several observability best practices were implemented:

- Structured logging for easier analysis
- Metric filters to extract metrics from logs
- Golden Signals dashboard design
- Automated alerting for critical conditions
- Infrastructure reproducibility using Terraform

These practices improve system reliability and enable faster **incident detection and troubleshooting**.