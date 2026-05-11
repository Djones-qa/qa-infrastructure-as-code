#!/usr/bin/env bash
# run-tests.sh - Run the test suite with common options
set -euo pipefail

# Defaults
BROWSER="${BROWSER:-chrome}"
ENV="${TEST_ENV:-local}"
MARKERS="${MARKERS:-}"
HEADLESS="${HEADLESS:-true}"
PARALLEL="${PARALLEL:-auto}"
REPORT_DIR="${REPORT_DIR:-reports}"

usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Options:
  -b, --browser     Browser to use: chrome|firefox|edge (default: chrome)
  -e, --env         Environment: local|staging|production (default: local)
  -m, --markers     Pytest markers to filter (e.g., "smoke", "regression")
  -p, --parallel    Number of parallel workers or "auto" (default: auto)
  --no-headless     Run browser in headed mode
  -h, --help        Show this help message

Examples:
  $0                                    # Run all tests, Chrome, local
  $0 -m smoke                           # Run smoke tests only
  $0 -b firefox -e staging -m regression  # Firefox regression on staging
  $0 --no-headless -m "ui and smoke"    # Headed smoke UI tests
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--browser)   BROWSER="$2"; shift 2 ;;
        -e|--env)       ENV="$2"; shift 2 ;;
        -m|--markers)   MARKERS="$2"; shift 2 ;;
        -p|--parallel)  PARALLEL="$2"; shift 2 ;;
        --no-headless)  HEADLESS="false"; shift ;;
        -h|--help)      usage; exit 0 ;;
        *)              echo "Unknown option: $1"; usage; exit 1 ;;
    esac
done

# Build pytest command
PYTEST_ARGS=(
    "tests/"
    "--browser=${BROWSER}"
    "--env=${ENV}"
    "--tb=short"
    "--html=${REPORT_DIR}/report-${BROWSER}-${ENV}.html"
    "--self-contained-html"
    "-v"
)

if [ "${HEADLESS}" = "true" ]; then
    PYTEST_ARGS+=("--headless")
fi

if [ -n "${MARKERS}" ]; then
    PYTEST_ARGS+=("-m" "${MARKERS}")
fi

if [ "${PARALLEL}" != "1" ]; then
    PYTEST_ARGS+=("-n" "${PARALLEL}")
fi

# Create reports directory
mkdir -p "${REPORT_DIR}"

echo "Running tests:"
echo "  Browser:  ${BROWSER}"
echo "  Env:      ${ENV}"
echo "  Markers:  ${MARKERS:-all}"
echo "  Headless: ${HEADLESS}"
echo "  Workers:  ${PARALLEL}"
echo ""

pytest "${PYTEST_ARGS[@]}"
