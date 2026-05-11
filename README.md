# QA Infrastructure as Code

[![CI Pipeline](https://github.com/Djones-qa/qa-infrastructure-as-code/actions/workflows/ci.yml/badge.svg)](https://github.com/Djones-qa/qa-infrastructure-as-code/actions/workflows/ci.yml)
[![Nightly Regression](https://github.com/Djones-qa/qa-infrastructure-as-code/actions/workflows/nightly.yml/badge.svg)](https://github.com/Djones-qa/qa-infrastructure-as-code/actions/workflows/nightly.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Terraform](https://img.shields.io/badge/Terraform-1.5%2B-7B42BC?logo=terraform)](https://developer.hashicorp.com/terraform)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org)

A production-ready QA infrastructure framework using modern DevOps tooling to provision, configure, and manage automated testing environments at scale.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions CI/CD                     │
│         (Lint → Provision → Configure → Test → Destroy)     │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────▼───────────────┐
           │         Terraform             │
           │   AWS VPC + EC2 + RDS + S3    │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │           Ansible             │
           │  Install Docker, Configure    │
           │  Selenium Grid, App Deploy    │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │       Docker Compose          │
           │  Selenium Hub + Chrome/Firefox│
           │  Nodes + Test Runner          │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │       Pytest Test Suite       │
           │  UI Tests + API Tests +       │
           │  Performance Checks           │
           └───────────────────────────────┘
```

## 📁 Project Structure

```
qa-infrastructure-as-code/
├── terraform/                  # Infrastructure provisioning
│   ├── modules/
│   │   ├── networking/         # VPC, subnets, security groups
│   │   ├── compute/            # EC2 instances for test runners
│   │   └── database/           # RDS for test data
│   ├── environments/
│   │   ├── staging/            # Staging environment config
│   │   └── production/         # Production-like test env
│   └── main.tf
├── ansible/                    # Configuration management
│   ├── playbooks/
│   │   ├── setup-selenium.yml  # Selenium Grid setup
│   │   ├── setup-docker.yml    # Docker installation
│   │   └── deploy-app.yml      # Application deployment
│   ├── roles/
│   │   ├── common/
│   │   ├── selenium-grid/
│   │   └── test-runner/
│   └── inventory/
├── docker/                     # Container definitions
│   ├── docker-compose.yml      # Full Selenium Grid stack
│   ├── docker-compose.ci.yml   # Lightweight CI stack
│   └── test-runner/
│       └── Dockerfile
├── tests/                      # Test suites
│   ├── ui/                     # Selenium UI tests
│   ├── api/                    # REST API tests
│   ├── performance/            # Locust performance tests
│   └── conftest.py
├── .github/
│   └── workflows/
│       ├── ci.yml              # PR validation pipeline
│       ├── nightly.yml         # Nightly full regression
│       └── infrastructure.yml  # Infra provision/destroy
├── scripts/                    # Utility scripts
│   ├── setup-local.sh
│   └── run-tests.sh
└── docs/                       # Documentation
    ├── getting-started.md
    ├── architecture.md
    └── contributing.md
```

## 🚀 Quick Start

### Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/downloads) >= 1.5
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/) >= 2.14
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose >= 2.0
- [Python](https://www.python.org/downloads/) >= 3.11
- AWS CLI configured with appropriate credentials

### Local Development (Docker only)

```bash
# Clone the repo
git clone https://github.com/Djones-qa/qa-infrastructure-as-code.git
cd qa-infrastructure-as-code

# Start Selenium Grid locally
docker compose -f docker/docker-compose.yml up -d

# Install Python dependencies
pip install -r tests/requirements.txt

# Run the test suite
pytest tests/ -v --html=reports/report.html
```

### Full Infrastructure Deployment

```bash
# 1. Provision AWS infrastructure
cd terraform/environments/staging
terraform init
terraform plan
terraform apply

# 2. Configure instances with Ansible
cd ../../../ansible
ansible-playbook -i inventory/staging playbooks/setup-docker.yml
ansible-playbook -i inventory/staging playbooks/setup-selenium.yml

# 3. Run tests against live environment
pytest tests/ -v --env=staging
```

## 🧪 Test Suites

| Suite | Framework | Description |
|-------|-----------|-------------|
| UI Tests | Selenium + Pytest | Cross-browser end-to-end tests |
| API Tests | Requests + Pytest | REST API contract & integration tests |
| Performance | Locust | Load testing & performance benchmarks |

## 🔧 CI/CD Pipelines

| Workflow | Trigger | Description |
|----------|---------|-------------|
| `ci.yml` | Pull Request | Lint, unit tests, smoke tests |
| `nightly.yml` | Cron (2am UTC) | Full regression suite |
| `infrastructure.yml` | Manual / PR | Terraform plan/apply/destroy |

## 🌍 Environments

| Environment | Purpose | Auto-destroy |
|-------------|---------|--------------|
| `staging` | PR validation | Yes (after 4h) |
| `production` | Nightly regression | Yes (after run) |

## 📊 Reporting

Test results are published to:
- **GitHub Actions** summary page
- **HTML reports** stored as pipeline artifacts
- **Allure** dashboard (optional, see `docs/allure-setup.md`)

## 🤝 Contributing

See [CONTRIBUTING.md](docs/contributing.md) for development workflow and standards.

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
