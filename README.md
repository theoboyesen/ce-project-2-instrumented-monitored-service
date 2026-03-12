# Instrumented & Monitored Order API

This project demonstrates how to build and operate a **production-style cloud service with full observability**.

The system includes structured logging, custom metrics, monitoring dashboards, automated alerting, and simulated incident response using **AWS CloudWatch**.

The goal of the project is to demonstrate how engineers build **observable and maintainable systems**, not just functional applications.

---

# Project Overview

The application is a simple **REST API for managing orders**.  
It is deployed on an **AWS EC2 instance** and instrumented with monitoring and observability tools.

The project focuses on:

- Structured application logging
- Custom metrics extraction
- CloudWatch dashboards using Golden Signals
- Automated alerting and notifications
- Incident detection and investigation

---

# Architecture

The service is deployed on a **single EC2 instance** with observability components integrated into both the application and infrastructure.

### Architecture Flow

```
Client
   ↓
Flask Order API (EC2)
   ↓
Structured Logs
   ↓
CloudWatch Logs
   ↓
Metric Filters
   ↓
CloudWatch Metrics
   ↓
CloudWatch Dashboard
   ↓
CloudWatch Alarms
   ↓
SNS Email Notifications
```

A full architecture description is available in:

```
ARCHITECTURE.md
```

---

# Application Endpoints

The Order API provides the following endpoints:

| Endpoint | Method | Description |
|------|------|------|
| `/orders` | POST | Create a new order |
| `/orders/{id}` | GET | Retrieve an order |
| `/health` | GET | Health check endpoint |

### Example Request

```bash
curl -X POST http://<EC2-IP>:5000/orders \
-H "Content-Type: application/json" \
-d '{"item":"keyboard","price":50}'
```

---

# Observability Features

The application was instrumented to provide visibility into system behaviour.

---

## Structured Logging

Application events are logged in **structured JSON format**.

Example:

```json
{
  "event": "order_created",
  "request_id": "...",
  "latency_ms": 12.3
}
```

Logs are collected by the **CloudWatch Agent** and stored in:

```
/aws/ec2/order-api
```

---

## Custom Metrics

Metrics are generated from log events using **CloudWatch Metric Filters**.

Custom metrics include:

```
orders_created_total
orders_retrieved_total
api_errors_total
request_latency_ms
```

These metrics allow application behaviour to be monitored in **real time**.

---

# Monitoring Dashboard

A **CloudWatch dashboard** was created to monitor system health using the **Golden Signals model**.

| Signal | Metric |
|------|------|
| Traffic | orders_created_total |
| Errors | api_errors_total |
| Latency | request_latency_ms |
| Saturation | CPU, Memory, Disk |

The dashboard allows operators to quickly identify system issues and performance problems.

---

# Alerting System

CloudWatch alarms automatically detect abnormal system behaviour.

### Implemented Alarms

| Alarm | Condition |
|------|------|
| api-errors-high | API errors exceed threshold |
| cpu-utilization-high | CPU utilization above 80% |
| api-latency-high | API latency above threshold |

Alerts trigger an **SNS topic** which sends email notifications to operators.

---

# Incident Simulation

Two failure scenarios were simulated to validate the monitoring system.

### High CPU Utilization

CPU stress was generated on the EC2 instance, triggering the **cpu-utilization-high** alarm.

### API Error Spike

Repeated invalid API requests generated an error spike, triggering the **api-errors-high** alarm.

Incident investigations are documented in:

```
INCIDENTS.md
```

---

# Repository Structure

```
ce-project-2-instrumented-monitored-service/
│
├── README.md
├── ARCHITECTURE.md
├── INSTRUMENTATION.md
├── MONITORING.md
├── ALERTING.md
├── INCIDENTS.md
│
├── app/
│   ├── server.py
│   ├── requirements.txt
│
├── config/
│   ├── dashboard.json
│   ├── alarms.json
│
├── docs/
│   ├── runbook.md
│   ├── dashboard-guide.md
│   ├── deployment.md
│
└── evidence/
    ├── dashboard-screenshots/
    ├── alert-screenshots/
    └── incident-screenshots/
```

---

# Deployment

The application infrastructure was provisioned using **Terraform**, ensuring the environment can be recreated consistently.

Deployment includes:

- EC2 instance
- Security groups
- IAM role for CloudWatch Agent
- Monitoring configuration

Deployment instructions are available in:

```
docs/deployment.md
```

---

# Key Learning Outcomes

This project demonstrates several important **cloud engineering and DevOps practices**:

- Implementing structured logging
- Designing meaningful application metrics
- Monitoring systems using Golden Signals
- Building automated alerting pipelines
- Investigating incidents using observability data

These techniques are essential for operating **reliable production systems**.

---

# Future Improvements

Potential improvements include:

- Distributed tracing using AWS X-Ray
- Auto-remediation using Lambda
- Load testing and performance benchmarking
- Multi-instance scaling using Auto Scaling Groups
- Integration with external monitoring platforms

---

# Author

Theo Boyesen