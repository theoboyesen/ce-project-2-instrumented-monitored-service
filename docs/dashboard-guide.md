# Dashboard Guide

This document explains how to read and use the **CloudWatch monitoring dashboard** for the Order API service.

The dashboard provides a real-time overview of system health and helps operators quickly diagnose incidents.

---

# Dashboard Overview

The monitoring dashboard displays key **application and infrastructure metrics**.

The dashboard follows the **Golden Signals model**, which focuses on four critical indicators of system health:

- Traffic  
- Errors  
- Latency  
- Saturation  

Monitoring these signals helps quickly detect abnormal system behaviour.

---

# Dashboard Layout

The dashboard is divided into several sections:

- Application Traffic  
- Application Errors  
- API Latency  
- Infrastructure Resource Utilization  

This layout allows operators to correlate different metrics and identify root causes during incidents.

---

# Traffic Metrics

Traffic represents the **volume of requests handled by the system**.

**Metric**

```
orders_created_total
```

**Description**

This metric tracks the number of successful order creation requests.

**Usage**

Traffic spikes may indicate increased user activity or abnormal request patterns.

Monitoring traffic helps determine whether system load has increased.

---

# Error Metrics

Errors represent **failed API requests**.

**Metric**

```
api_errors_total
```

**Description**

This metric tracks failed requests such as invalid order lookups.

**Usage**

Sudden spikes in errors may indicate:

- Application bugs  
- Invalid client requests  
- Misconfigured endpoints  

Error monitoring helps quickly detect application failures.

---

# Latency Metrics

Latency measures how long the API takes to **process requests**.

**Metric**

```
request_latency_ms
```

**Description**

This metric tracks request response time in milliseconds.

**Usage**

Latency increases may indicate:

- Performance degradation  
- Resource bottlenecks  
- Inefficient code execution  

Latency is often an early indicator of system problems.

---

# Saturation Metrics

Saturation metrics indicate **how heavily system resources are being used**.

**Metrics**

```
CPUUtilization
mem_used_percent
disk_used_percent
```

**Description**

These metrics are collected by the **CloudWatch Agent** running on the EC2 instance.

**Usage**

High saturation levels may indicate that the system is approaching its operational limits.

For example:

High CPU utilization may indicate excessive workload or inefficient processes.

---

# Using the Dashboard for Troubleshooting

When an alarm triggers, the dashboard should be the **first place operators investigate**.

### Typical Troubleshooting Workflow

1. Open the monitoring dashboard.
2. Identify which metric has changed.
3. Check related metrics for correlation.
4. Review logs for additional details.

### Example Scenarios

- High CPU + increased latency → infrastructure saturation  
- Error spike + normal CPU → application issue  
- Traffic spike + CPU increase → load increase  

Correlation between metrics helps determine the root cause quickly.

---

# Dashboard Refresh

The CloudWatch dashboard updates automatically as new metrics are published.

Most metrics are updated approximately every:

```
60 seconds
```

Operators should allow a short delay for metrics to appear after system changes.

---

# Summary

The monitoring dashboard provides a **centralized view of application and infrastructure health**.

By observing **traffic, errors, latency, and saturation metrics together**, operators can quickly detect and diagnose incidents.