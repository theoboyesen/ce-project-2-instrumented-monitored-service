# Instrumentation Strategy

This document explains how the **Order API service** was instrumented to provide observability using:

- Structured logging
- Custom metrics
- Request tracing

Instrumentation ensures the application produces enough telemetry data to:

- Understand system behavior
- Diagnose incidents
- Monitor performance in production

---

# Logging Strategy

The application uses **structured JSON logging** so logs are machine-readable and easily searchable in CloudWatch Logs.

Each log entry contains consistent fields describing the event.

Example log entry:

```json
{
  "timestamp": "2026-03-11T12:35:41.345287",
  "level": "INFO",
  "event": "request_completed",
  "request_id": "45bed901-9f40-4244-a82b-9cee495e8bc5",
  "path": "/health",
  "latency_ms": 0.1
}
```

Structured logging enables:

- Easier filtering and querying
- Metric extraction from logs
- Faster debugging during incidents

### Log Location

Logs are written to:

```
/var/log/order-api.log
```

The **CloudWatch Agent** collects this file and sends logs to:

```
/aws/ec2/order-api
```

---

# Log Levels

Different log levels distinguish between normal behavior, warnings, and errors.

| Level | Usage |
|------|------|
| INFO | Successful operations and request completion |
| WARN | Unexpected but non-critical situations |
| ERROR | Server errors or failures |

Examples:

- `INFO` → order_created  
- `INFO` → order_retrieved  
- `WARN` → order_not_found  

Using log levels allows operators to quickly identify problematic events in log streams.

---

# Correlation IDs

Each request is assigned a unique **correlation ID** using a `request_id`.

This ID is generated at the start of every request.

```python
@app.before_request
def assign_request_id():
    g.request_id = str(uuid.uuid4())
```

The request ID is included in every log entry during the request lifecycle.

Example:

```json
{
  "event": "order_created",
  "request_id": "922804dd-8847-45e5-8ac5-d1968f8c2219"
}
```

Benefits:

- Trace all logs related to a single request
- Simplify debugging during incidents
- Support distributed tracing patterns

---

# Latency Instrumentation

API request latency is measured using Flask request hooks.

### Capture Request Start Time

```python
@app.before_request
def start_timer():
    g.start_time = time.time()
```

### Calculate Request Duration

```python
duration_ms = round((time.time() - g.start_time) * 1000, 1)
```

The latency is logged as part of a structured event.

Example event:

```
event = "request_completed"
latency_ms = <value>
```

This allows API performance to be monitored and visualized.

---

# Custom Metrics

Application metrics are generated from log events using **CloudWatch Metric Filters**.

Metrics are published under the namespace:

```
OrderAPI
```

## Orders Created

**Metric**

```
orders_created_total
```

**Purpose**

Tracks successful order creation requests.  
Represents the **Traffic** signal in the Golden Signals model.

---

## Orders Retrieved

**Metric**

```
orders_retrieved_total
```

**Purpose**

Tracks successful retrieval of orders and helps measure application usage.

---

## API Errors

**Metric**

```
api_errors_total
```

**Purpose**

Tracks failed API requests such as invalid order lookups.  
Represents the **Error Rate** signal in the Golden Signals model.

---

## Request Latency

**Metric**

```
request_latency_ms
```

**Purpose**

Tracks API response time in milliseconds.  
Represents the **Latency** signal in the Golden Signals model.

Latency monitoring helps detect performance degradation.

---

# Infrastructure Metrics

Infrastructure metrics are collected by the **CloudWatch Agent** running on the EC2 instance.

| Metric | Purpose |
|------|------|
| CPUUtilization | Detect compute saturation |
| mem_used_percent | Detect memory pressure |
| disk_used_percent | Detect disk capacity issues |

These metrics represent the **Saturation** signal in the Golden Signals model.

---

# Golden Signals Implementation

The monitoring dashboard was designed using the **Golden Signals framework**.

| Signal | Metric |
|------|------|
| Traffic | orders_created_total |
| Errors | api_errors_total |
| Latency | request_latency_ms |
| Saturation | CPU, Memory, Disk |

This model ensures the system can quickly detect performance and operational issues.

---

# Observability Benefits

The instrumentation implemented in this project provides several operational benefits:

- Real-time visibility into application behavior
- Automated detection of system failures
- Faster root cause analysis during incidents
- Proactive monitoring of performance degradation

This level of observability helps ensure the system can be operated reliably in a production environment.