# Deployment Guide

This document explains how to deploy and run the **Instrumented & Monitored Order API service**.

The infrastructure is provisioned using **Terraform**, and the application runs on an **AWS EC2 instance** with monitoring provided by **CloudWatch**.

---

# Prerequisites

Before deploying the system, ensure the following tools are installed:

- Terraform  
- AWS CLI  
- Git  
- Python 3  

You must also have AWS credentials configured locally.

### Verify AWS Credentials

```bash
aws configure
```

---

# Clone the Repository

Clone the project repository:

```bash
git clone https://github.com/theoboyesen/ce-project-2-instrumented-monitored-service.git
cd ce-project-2-instrumented-monitored-service
```

---

# Infrastructure Deployment

Infrastructure is defined using **Terraform**.

Navigate to the Terraform directory:

```bash
cd terraform
```

### Initialize Terraform

```bash
terraform init
```

### Review the Execution Plan

```bash
terraform plan
```

### Apply the Infrastructure Configuration

```bash
terraform apply
```

Terraform will create the following resources:

- EC2 instance
- Security group
- IAM role for CloudWatch Agent
- Instance profile
- SSH key configuration

After deployment, Terraform outputs the **public IP address of the EC2 instance**.

---

# Connect to the EC2 Instance

Use SSH to connect to the instance:

```bash
ssh -i observability-key ec2-user@<EC2_PUBLIC_IP>
```

---

# Install Application Dependencies

Navigate to the application directory:

```bash
cd app
```

Install Python dependencies:

```bash
pip3 install -r requirements.txt
```

---

# Start the Application

Run the Flask API:

```bash
python3 server.py
```

The API will start on:

```
http://<EC2_PUBLIC_IP>:5000
```

---

# Test the API

### Health Check

```bash
curl http://<EC2_PUBLIC_IP>:5000/health
```

### Create an Order

```bash
curl -X POST http://<EC2_PUBLIC_IP>:5000/orders \
-H "Content-Type: application/json" \
-d '{"item":"keyboard","price":50}'
```

### Retrieve an Order

```bash
curl http://<EC2_PUBLIC_IP>:5000/orders/<ORDER_ID>
```

---

# CloudWatch Logging

Application logs are written to:

```
/var/log/order-api.log
```

The **CloudWatch Agent** forwards these logs to the log group:

```
/aws/ec2/order-api
```

Logs can be viewed in the **AWS CloudWatch console**.

---

# Monitoring

Metrics are extracted from logs using **CloudWatch Metric Filters**.

Custom metrics include:

```
orders_created_total
orders_retrieved_total
api_errors_total
request_latency_ms
```

These metrics are visualized in the **CloudWatch monitoring dashboard**.

---

# Alerting

CloudWatch alarms detect abnormal system behaviour.

Configured alarms include:

```
cpu-utilization-high
api-errors-high
api-latency-high
```

When triggered, alarms send notifications through an **SNS topic**.

---

# Stopping the Infrastructure

To destroy all resources created by Terraform:

```bash
terraform destroy
```

This will remove the EC2 instance and associated infrastructure.

---

# Summary

The deployment process provisions the infrastructure, deploys the **Order API application**, and enables observability features including:

- Logging
- Metrics
- Dashboards
- Alerts

Using **Terraform** ensures that the environment can be recreated consistently and reliably.