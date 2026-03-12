# Alerting Strategy

This document describes the alerting system implemented for the **Order API service**.

The goal of alerting is to automatically detect abnormal system behaviour and notify operators so incidents can be investigated and resolved quickly.

Alerts are implemented using **AWS CloudWatch Alarms** and **Amazon SNS notifications**.

---

# Alert Architecture

The alerting pipeline follows this flow:

```
Application / Infrastructure Metric
        ↓
CloudWatch Metric
        ↓
CloudWatch Alarm Evaluation
        ↓
SNS Notification
        ↓
Email Alert to Operators
```

This architecture ensures that issues detected by monitoring automatically trigger notifications.

---

# SNS Notification System

Alerts are delivered using an **Amazon SNS topic**:

```
order-api-alerts
```

The SNS topic sends email notifications when alarms enter the **ALARM** state.

Benefits of using SNS include:

- Automated alert delivery
- Support for multiple subscribers
- Integration with monitoring systems
- Scalable notification handling

---

# Implemented Alarms

Three CloudWatch alarms were implemented to detect different types of system issues.

---

# API Error Rate Alarm

**Alarm Name**

```
api-errors-high
```

**Metric**

```
OrderAPI / api_errors_total
```

**Condition**

```
api_errors_total > 5
within 60 seconds
```

**Purpose**

Detects abnormal increases in failed API requests.

This alarm helps identify:

- Broken endpoints
- Application bugs
- Malformed client requests
- Unexpected API behaviour

---

# CPU Utilization Alarm

**Alarm Name**

```
cpu-utilization-high
```

**Metric**

```
AWS/EC2 / CPUUtilization
```

**Condition**

```
CPUUtilization > 80%
for 2 evaluation periods (60 seconds each)
```

**Purpose**

Detects infrastructure resource saturation.

High CPU utilization may indicate:

- Excessive load
- Inefficient code
- Resource exhaustion
- Denial of service conditions

---

# API Latency Alarm

**Alarm Name**

```
api-latency-high
```

**Metric**

```
OrderAPI / request_latency_ms
```

**Condition**

```
Average latency > 500ms
within 60 seconds
```

**Purpose**

Detects slow API responses.

Latency increases may indicate:

- Performance degradation
- Resource bottlenecks
- Database or dependency issues
- Infrastructure overload

---

# Alert Threshold Rationale

Thresholds were selected to balance **sensitivity and noise reduction**.

| Metric | Threshold | Reason |
|------|------|------|
| API Errors | >5 per minute | Detect abnormal error spikes |
| CPU Utilization | >80% | Indicates infrastructure saturation |
| Latency | >500ms | Detects significant performance degradation |

These thresholds help ensure alerts represent **real problems rather than normal fluctuations**.

---

# Alert Response Procedures

When an alert is triggered, the following investigation process should be followed.

---

## Step 1: Identify the Alarm

Determine which alarm triggered the notification.

Examples:

```
cpu-utilization-high
api-errors-high
api-latency-high
```

---

## Step 2: Check the Monitoring Dashboard

Open the **CloudWatch dashboard** to examine system metrics.

Look for:

- Traffic spikes
- Error increases
- Latency changes
- Resource saturation

---

## Step 3: Correlate Metrics

Compare related metrics to determine the cause.

Examples:

- High CPU + latency increase → resource bottleneck  
- Error spike + normal CPU → application failure  
- Traffic spike + high CPU → load increase  

---

## Step 4: Inspect Logs

Use **CloudWatch Logs** to investigate application events.

Structured logs allow filtering by:

- `request_id`
- event type
- error messages

---

## Step 5: Mitigate the Issue

Take appropriate corrective actions depending on the root cause.

Possible actions:

- Restart services
- Scale infrastructure
- Fix application bugs
- Block malicious requests

---

# Alert Validation

Alert functionality was tested by intentionally triggering incidents.

Two simulated failure scenarios were used:

- High CPU utilization
- API error spike

Both incidents successfully triggered **CloudWatch alarms and SNS notifications**.

These tests confirm that the alerting system works correctly.

---

# Summary

The alerting system ensures that abnormal system behaviour is automatically detected and communicated to operators.

By combining **monitoring dashboards, alarms, and notifications**, the system enables rapid detection and investigation of production incidents.