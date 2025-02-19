#!/usr/bin/env bash

# TJL Project Setup Tool - Docker Installer
# Author: Ben Adenle
# Email: ben@techjamlabs.com

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Print with color
print_blue() { echo -e "${BLUE}$1${NC}"; }
print_green() { echo -e "${GREEN}$1${NC}"; }
print_red() { echo -e "${RED}$1${NC}"; }
print_yellow() { echo -e "${YELLOW}$1${NC}"; }

# Header
print_blue "=== TJL Project Setup Tool - Docker Installation ==="
echo

# Check Docker installation
if ! command -v docker &> /dev/null; then
    print_red "Error: Docker is not installed"
    echo "Please install Docker first:"
    echo "  https://docs.docker.com/get-docker/"
    exit 1
fi
print_green "✓ Docker is installed"

# Create Dockerfile
print_blue "Creating Dockerfile..."
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

# Install git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy TJL Project Setup Tool
COPY tjl-project.py /usr/local/bin/tjl-project
RUN chmod +x /usr/local/bin/tjl-project

# Set working directory
WORKDIR /workspace

# Set entrypoint
ENTRYPOINT ["tjl-project"]
EOF

print_green "✓ Created Dockerfile"

# Build Docker image
print_blue "Building Docker image..."
docker build -t tjl-project .
if [ $? -ne 0 ]; then
    print_red "Error: Failed to build Docker image"
    exit 1
fi
print_green "✓ Built Docker image"

# Create shell alias
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    else
        SHELL_CONFIG="$HOME/.bashrc"
    fi
fi

if [ -n "$SHELL_CONFIG" ]; then
    # Add Docker alias
    if ! grep -q "alias tjl-docker=" "$SHELL_CONFIG"; then
        echo 'alias tjl-docker="docker run -v $(pwd):/workspace tjl-project"' >> "$SHELL_CONFIG"
        print_green "✓ Added Docker alias"
    else
        print_yellow "! Docker alias already exists"
    fi
fi

# Create Docker Compose file
print_blue "Creating Docker Compose file..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  tjl-project:
    build: .
    volumes:
      - .:/workspace
EOF

print_green "✓ Created Docker Compose file"

# Final instructions
echo
print_green "Docker installation complete!"
echo
echo "You can now use TJL Project Setup Tool with Docker:"
echo
echo "Using Docker directly:"
echo "  docker run -v \$(pwd):/workspace tjl-project my-project"
echo
echo "Using the alias (after restarting terminal):"
echo "  tjl-docker my-project"
echo
echo "Using Docker Compose:"
echo "  docker-compose run --rm tjl-project my-project"
echo
print_blue "Happy coding!"