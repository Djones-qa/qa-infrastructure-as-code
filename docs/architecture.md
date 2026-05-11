# Architecture

## Overview

This project provisions and manages a complete QA testing infrastructure using Infrastructure as Code principles. The goal is to create reproducible, scalable, and ephemeral test environments that can be spun up on demand and torn down after use.

## Infrastructure Layers

### Layer 1: Cloud Infrastructure (Terraform)

Terraform manages all AWS resources. The state is stored remotely in S3 with DynamoDB locking to support team collaboration.

**Resources provisioned:**

- **VPC** with public and private subnets across multiple availability zones
- **Internet Gateway** and **NAT Gateway** for controlled internet access
- **EC2 instances** for Selenium Hub, Selenium Nodes, and the test runner
- **RDS PostgreSQL** for test data storage (private subnet, encrypted at rest)
- **Security Groups** with least-privilege rules
- **AWS Secrets Manager** for database credentials

### Layer 2: Configuration Management (Ansible)

Ansible configures the EC2 instances after Terraform provisions them. Playbooks are idempotent and can be re-run safely.

**Playbooks:**

| Playbook | Purpose |
|----------|---------|
| `setup-docker.yml` | Installs Docker Engine and Docker Compose |
| `setup-selenium.yml` | Deploys Selenium Grid Hub and Nodes |
| `deploy-app.yml` | Deploys the application under test |

### Layer 3: Container Orchestration (Docker Compose)

Docker Compose manages the Selenium Grid containers on each instance. Two compose files are provided:

- `docker-compose.yml` — Full grid with Chrome, Firefox, and Edge nodes (local dev)
- `docker-compose.ci.yml` — Lightweight Chrome-only grid (CI pipelines)

### Layer 4: Test Execution (Pytest + Selenium)

The test suite is organized by type:

```
tests/
├── ui/           # Selenium WebDriver tests
├── api/          # REST API tests using requests
├── performance/  # Locust load tests
└── conftest.py   # Shared fixtures and configuration
```

## Network Design

```
Internet
    │
    ▼
Internet Gateway
    │
    ▼
Public Subnets (10.0.1.0/24, 10.0.2.0/24)
    ├── Selenium Hub (EC2)      ← Port 4444 open
    ├── Selenium Nodes (EC2)    ← Internal only
    └── Test Runner (EC2)       ← SSH only
    │
    ▼ (via NAT Gateway)
Private Subnets (10.0.10.0/24, 10.0.11.0/24)
    └── RDS PostgreSQL          ← Port 5432, VPC only
```

## CI/CD Pipeline

```
Pull Request
    │
    ├── Lint & Validate
    │   ├── Python (ruff, mypy)
    │   ├── Terraform (fmt, validate, tfsec)
    │   └── Ansible (ansible-lint)
    │
    ├── Smoke Tests
    │   └── Docker Selenium Grid + pytest -m smoke
    │
    ├── Terraform Validate
    │   └── terraform validate + tfsec scan
    │
    └── Docker Build
        └── Build test-runner image

Merge to main
    └── (No auto-deploy — use infrastructure.yml workflow)

Nightly (2 AM UTC)
    ├── Full Regression (Chrome + Firefox)
    └── Performance Tests (Locust, 50 users, 5 min)
```

## Security Considerations

- All EBS volumes and RDS storage are encrypted at rest
- Database credentials are stored in AWS Secrets Manager, never in code
- Security groups follow least-privilege principles
- Terraform state is encrypted in S3
- No hardcoded credentials anywhere in the codebase
- `.gitignore` excludes `.tfvars` files with sensitive values

## Scaling

To scale the Selenium Grid, adjust these Terraform variables:

```hcl
selenium_node_count = 4   # Add more nodes
instance_type       = "t3.large"  # Upgrade instance size
```

Each node supports up to 3 concurrent browser sessions, so 4 nodes = 12 parallel test sessions.
