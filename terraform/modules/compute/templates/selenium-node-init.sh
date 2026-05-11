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

# Create Selenium Node directory
mkdir -p /opt/selenium-node
cat > /opt/selenium-node/docker-compose.yml <<EOF
version: "3.8"
services:
  chrome-node:
    image: selenium/node-chrome:4.18.1
    shm_size: 2gb
    environment:
      - SE_EVENT_BUS_HOST=${hub_host}
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=3
    restart: unless-stopped

  firefox-node:
    image: selenium/node-firefox:4.18.1
    shm_size: 2gb
    environment:
      - SE_EVENT_BUS_HOST=${hub_host}
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=3
    restart: unless-stopped
EOF

# Start Selenium Nodes
cd /opt/selenium-node
docker-compose up -d

echo "Selenium Nodes initialized for environment: ${environment}, connecting to hub: ${hub_host}"
