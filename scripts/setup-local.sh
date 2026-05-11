#!/usr/bin/env bash
# setup-local.sh - Bootstrap local development environment
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info()    { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    local missing=()

    command -v docker   &>/dev/null || missing+=("docker")
    command -v python3  &>/dev/null || missing+=("python3")
    command -v pip      &>/dev/null || missing+=("pip")

    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing required tools: ${missing[*]}"
        log_error "Please install them and re-run this script."
        exit 1
    fi

    log_info "All prerequisites found."
}

# Set up Python virtual environment
setup_python() {
    log_info "Setting up Python virtual environment..."

    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        log_info "Virtual environment created."
    else
        log_warning "Virtual environment already exists, skipping creation."
    fi

    # shellcheck disable=SC1091
    source .venv/bin/activate
    pip install --quiet --upgrade pip
    pip install --quiet -r tests/requirements.txt
    log_info "Python dependencies installed."
}

# Copy environment file
setup_env() {
    if [ ! -f ".env" ]; then
        cp .env.example .env
        log_info "Created .env from .env.example — please update with your values."
    else
        log_warning ".env already exists, skipping."
    fi
}

# Start Selenium Grid
start_selenium() {
    log_info "Starting Selenium Grid..."
    docker compose -f docker/docker-compose.yml up -d

    log_info "Waiting for Selenium Hub to be ready..."
    timeout 60 bash -c 'until curl -sf http://localhost:4444/wd/hub/status > /dev/null; do sleep 2; done'
    log_info "Selenium Grid is ready at http://localhost:4444/ui"
}

# Run smoke tests to verify setup
verify_setup() {
    log_info "Running smoke tests to verify setup..."
    # shellcheck disable=SC1091
    source .venv/bin/activate

    if pytest tests/ -m smoke --headless -q --tb=short; then
        log_info "✅ Setup complete! Smoke tests passed."
    else
        log_warning "⚠️  Some smoke tests failed. Check the output above."
        log_warning "This may be expected if the application under test is not running."
    fi
}

main() {
    echo "================================================"
    echo "  QA Infrastructure - Local Setup"
    echo "================================================"

    check_prerequisites
    setup_env
    setup_python
    start_selenium
    verify_setup

    echo ""
    echo "================================================"
    echo "  Setup complete!"
    echo "  Selenium Grid: http://localhost:4444/ui"
    echo "  Run tests:     pytest tests/ -v --headless"
    echo "================================================"
}

main "$@"
