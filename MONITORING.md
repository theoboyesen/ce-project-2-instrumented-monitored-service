# Monitoring Strategy

This document describes how the **Order API service** is monitored using **AWS CloudWatch dashboards and metrics**.

The monitoring system provides visibility into:

- Application performance
- Error rates
- Traffic levels
- Infrastructure resource utilization

The dashboard is designed using the **Golden Signals framework**, a monitoring methodology introduced by Google SRE.

---

# Golden Signals

The Golden Signals represent the four most important indicators of system health.

| Signal | Description |
|------|------|
| Traffic | Volume of requests handled by the system |
| Errors | Rate of failed requests |
| Latency | Time taken to process requests |
| Saturation | Resource utilization indicating system capacity |

Monitoring these signals allows operators to quickly detect and diagnose system problems.

---

# Dashboard Overview

A **CloudWatch dashboard** was created to visualize the health of the Order API service.

The dashboard groups related metrics together to make troubleshooting easier.

Dashboard sections include:

- Application Traffic  
- Application Errors  
- API Latency  
- Infrastructure Resource Usage  

This layout allows operators to quickly correlate system behaviour across different metrics.

---

# Traffic Monitoring

Traffic is measured using the metric:

```
orders_created_total
```

This metric counts successful order creation requests.

The dashboard displays this metric as:

```
Orders Created Per Minute
```

### Purpose

- Identify traffic spikes
- Understand API usage patterns
- Detect abnormal request activity

---

# Error Monitoring

Errors are measured using the metric:

```
api_errors_total
```

This metric tracks failed requests such as invalid order lookups.

The dashboard visualizes this metric to highlight:

- Sudden increases in errors
- Abnormal API behaviour
- Potential application failures

Error monitoring allows operators to quickly detect service disruptions.

---

# Latency Monitoring

Latency is measured using the metric:

```
request_latency_ms
```

This metric tracks how long the API takes to respond to requests.

Monitoring latency helps identify:

- Performance degradation
- Slow API responses
- Potential resource bottlenecks

Latency spikes often indicate deeper system issues.

---

# Saturation Monitoring

Saturation metrics measure **infrastructure resource utilization**.

These metrics help determine whether the system is approaching its operational limits.

The following metrics are monitored:

- CPU Utilization  
- Memory Utilization  
- Disk Usage  

These metrics are collected by the **CloudWatch Agent** running on the EC2 instance.

Monitoring saturation helps detect:

- CPU bottlenecks
- Memory pressure
- Disk capacity issues

---

# Dashboard Usage for Troubleshooting

The monitoring dashboard allows operators to quickly investigate incidents.

### Example Troubleshooting Workflow

1. An alarm is triggered
2. The operator opens the monitoring dashboard
3. Abnormal metrics are identified
4. Related signals are correlated
5. Logs or system behaviour are investigated

Example scenarios:

- High CPU utilization with stable latency and error rates may indicate infrastructure stress.
- Error spikes without CPU increases may indicate application-level issues.

---

# Correlation Analysis

A key purpose of the dashboard is to allow **correlation between metrics**.

Examples:

- Traffic spike + latency increase → potential capacity issue  
- Error spike without CPU increase → application failure  
- CPU spike + latency spike → resource bottleneck  

Metric correlation helps operators quickly identify the root cause of incidents.

---

# Baseline Behaviour

Normal system behaviour was observed during testing.

Typical baseline values:

| Metric | Typical Value |
|------|------|
| CPU Utilization | 1–5% |
| Memory Utilization | Low steady usage |
| Disk Usage | Minimal change |
| Latency | Very low response times |
| Error Rate | Near zero |

These baseline metrics help identify abnormal system behaviour.

---

# Monitoring Benefits

The monitoring system provides:

- Real-time visibility into application performance
- Early detection of system failures
- Faster incident diagnosis
- Improved operational reliability

By combining **application metrics** with **infrastructure metrics**, the monitoring system provides a complete view of system health.