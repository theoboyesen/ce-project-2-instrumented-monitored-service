# Operational Runbook

This runbook provides operational guidance for responding to alerts and troubleshooting the **Order API service**.

It is intended to help operators quickly diagnose and resolve system issues using the monitoring tools implemented in this project.

---

# Monitoring Tools

The system is monitored using the following AWS services:

- CloudWatch Dashboard  
- CloudWatch Logs  
- CloudWatch Alarms  
- Amazon SNS Notifications  

These tools provide visibility into system behaviour and allow operators to investigate incidents.

---

# Common Alerts

The following **CloudWatch alarms** are configured.

---

## cpu-utilization-high

**Trigger Condition**

```
CPU utilization above 80% for two evaluation periods
```

**Possible Causes**

- Excessive request load
- Inefficient code
- Runaway processes
- Infrastructure saturation

**Investigation Steps**

1. Open the **CloudWatch dashboard**.
2. Check the CPU utilization graph.
3. Verify whether traffic or latency increased at the same time.
4. Check running processes on the EC2 instance.

**Possible Resolution**

Terminate unnecessary processes or scale infrastructure.

---

## api-errors-high

**Trigger Condition**

```
API errors exceed threshold within one minute
```

**Possible Causes**

- Invalid client requests
- Broken API endpoints
- Application bugs

**Investigation Steps**

1. Open the **monitoring dashboard**.
2. Check the **API Errors** metric.
3. Review application logs in **CloudWatch Logs**.
4. Identify the endpoint generating errors.

**Possible Resolution**

Fix application logic or block invalid requests.

---

## api-latency-high

**Trigger Condition**

```
API latency exceeds 500 milliseconds
```

**Possible Causes**

- CPU saturation
- Memory pressure
- Inefficient API processing

**Investigation Steps**

1. Check latency metrics on the dashboard.
2. Correlate with CPU or memory utilization.
3. Inspect recent logs for slow requests.

**Possible Resolution**

Optimize application code or increase system resources.

---

# Log Investigation

Application logs are stored in the following CloudWatch log group:

```
/aws/ec2/order-api
```

Logs are structured JSON and include fields such as:

- `timestamp`
- `event`
- `request_id`
- `latency_ms`

Logs can be searched using **CloudWatch Logs Insights**.

### Example Query

```
fields @timestamp, event, latency_ms
| sort @timestamp desc
| limit 20
```

This query displays the most recent API events.

---

# Dashboard Usage

The monitoring dashboard provides an overview of system health.

Operators should review the following metrics:

- **Traffic** – request volume  
- **Errors** – failed API requests  
- **Latency** – response time  
- **CPU / Memory / Disk** – infrastructure saturation  

When investigating an alert, compare multiple metrics to determine the root cause.

---

# Incident Response Workflow

When an alert occurs:

1. Identify the alarm that triggered.
2. Review the monitoring dashboard.
3. Investigate logs for additional context.
4. Determine the root cause.
5. Apply corrective action.

After resolving the issue, confirm that the alarm returns to the **OK** state.

---

# Escalation

If the issue cannot be resolved using this runbook:

- Escalate to the engineering team
- Review recent deployments or configuration changes
- Analyze historical metrics for patterns