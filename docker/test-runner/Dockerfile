FROM python:3.11-slim

LABEL maintainer="QA Infrastructure Team"
LABEL description="Test runner container for QA automation suite"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY tests/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test suite
COPY tests/ ./tests/

# Create reports directory
RUN mkdir -p reports

# Default command runs the full test suite
CMD ["pytest", "tests/", "-v", \
     "--html=reports/report.html", \
     "--self-contained-html", \
     "--tb=short", \
     "-n", "auto"]
