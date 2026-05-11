#!/bin/bash
set -euo pipefail

# Update system
apt-get update -y
apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu

# Install Docker Compose
curl -SL "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64" \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create Selenium Grid directory
mkdir -p /opt/selenium-grid
cat > /opt/selenium-grid/docker-compose.yml <<'EOF'
version: "3.8"
services:
  selenium-hub:
    image: selenium/hub:4.18.1
    container_name: selenium-hub
    ports:
      - "4442:4442"
      - "4443:4443"
      - "4444:4444"
    environment:
      - SE_NODE_MAX_SESSIONS=5
    restart: unless-stopped
EOF

# Start Selenium Hub
cd /opt/selenium-grid
docker-compose up -d

echo "Selenium Hub initialized for environment: ${environment}"
