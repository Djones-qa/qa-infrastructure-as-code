# Getting Started

This guide walks you through setting up the QA infrastructure locally and running your first tests.

## Prerequisites

Install the following tools before getting started:

| Tool | Version | Install |
|------|---------|---------|
| Git | Latest | [git-scm.com](https://git-scm.com) |
| Docker Desktop | >= 4.0 | [docker.com](https://www.docker.com/products/docker-desktop) |
| Python | >= 3.11 | [python.org](https://www.python.org/downloads/) |
| Terraform | >= 1.5 | [developer.hashicorp.com](https://developer.hashicorp.com/terraform/downloads) |
| Ansible | >= 2.14 | [docs.ansible.com](https://docs.ansible.com/ansible/latest/installation_guide/) |
| AWS CLI | >= 2.0 | [aws.amazon.com](https://aws.amazon.com/cli/) |

## Local Setup (5 minutes)

### 1. Clone the repository

```bash
git clone https://github.com/Djones-qa/qa-infrastructure-as-code.git
cd qa-infrastructure-as-code
```

### 2. Start Selenium Grid

```bash
docker compose -f docker/docker-compose.yml up -d
```

Verify the grid is running by visiting: http://localhost:4444/ui

You should see the Selenium Grid console with Chrome, Firefox, and Edge nodes registered.

### 3. Install Python dependencies

```bash
# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r tests/requirements.txt
```

### 4. Run the smoke tests

```bash
pytest tests/ -m smoke -v --headless
```

### 5. View the test report

After tests complete, open `reports/report.html` in your browser.

## Running Specific Test Suites

```bash
# UI tests only
pytest tests/ui/ -v --browser=chrome --headless

# API tests only
pytest tests/api/ -v

# Regression suite
pytest tests/ -m regression -v -n auto

# Single test file
pytest tests/ui/test_login.py -v

# With specific browser
pytest tests/ui/ --browser=firefox --headless
```

## Environment Configuration

Copy the example environment file and configure your values:

```bash
cp .env.example .env
```

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SELENIUM_HUB_URL` | Selenium Grid URL | `http://localhost:4444` |
| `LOCAL_BASE_URL` | Local app URL | `http://localhost:8080` |
| `STAGING_BASE_URL` | Staging app URL | — |
| `PRODUCTION_BASE_URL` | Production app URL | — |

## Stopping the Local Environment

```bash
docker compose -f docker/docker-compose.yml down
```

## Next Steps

- Read [architecture.md](architecture.md) to understand the full infrastructure design
- See [contributing.md](contributing.md) to learn the development workflow
- Check the GitHub Actions workflows in `.github/workflows/` to understand the CI/CD pipeline
