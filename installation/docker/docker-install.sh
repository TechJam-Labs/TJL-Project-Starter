#!/usr/bin/env bash

# TJL Project Setup Tool - Docker Setup
# Author: Ben Adenle
# Email: ben@techjamlabs.com

# Exit on error
set -e

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
print_blue "=== TJL Project Setup Tool - Docker Setup ==="
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

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy TJL Project Setup Tool
COPY . /app/

# Set environment variables
ENV PYTHONPATH=/app
ENV TJL_PROJECT_ROOT=/app
ENV TJL_PROJECT_TEMPLATES=/app/templates
ENV TJL_PROJECT_DOCS=/app/docs

# Create entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["--help"]
EOF

# Create requirements.txt
print_blue "Creating requirements.txt..."
cat > requirements.txt << 'EOF'
click>=8.0.0
colorama>=0.4.4
jinja2>=3.0.0
pyyaml>=5.4.0
EOF

# Create Docker entrypoint script
print_blue "Creating entrypoint script..."
cat > docker-entrypoint.sh << 'EOF'
#!/bin/bash
set -e

# Function to fix permissions
fix_permissions() {
    # Get host user's UID and GID
    if [ -n "$HOST_UID" ] && [ -n "$HOST_GID" ]; then
        # Create group if it doesn't exist
        groupadd -g $HOST_GID tjlgroup 2>/dev/null || true
        # Create user if it doesn't exist
        useradd -u $HOST_UID -g $HOST_GID -m tjluser 2>/dev/null || true
        # Change ownership of the workspace
        chown -R $HOST_UID:$HOST_GID /workspace
    fi
}

# Create workspace if it doesn't exist
mkdir -p /workspace

# Fix permissions
fix_permissions

# Switch to workspace
cd /workspace

# Execute tjl-project with provided arguments
exec python /app/tjl-project.py "$@"
EOF

chmod +x docker-entrypoint.sh

# Create docker-compose.yml
print_blue "Creating docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  tjl-project:
    build: .
    volumes:
      - .:/workspace
    environment:
      - HOST_UID=${UID:-1000}
      - HOST_GID=${GID:-1000}
    working_dir: /workspace
EOF

# Build Docker image
print_blue "Building Docker image..."
docker build -t tjl-project .
print_green "✓ Built Docker image"

# Create convenience script
print_blue "Creating convenience script..."
cat > tjl-docker << 'EOF'
#!/bin/bash
docker run -it --rm \
    -v "$(pwd):/workspace" \
    -e HOST_UID=$(id -u) \
    -e HOST_GID=$(id -g) \
    tjl-project "$@"
EOF

chmod +x tjl-docker
print_green "✓ Created convenience script"

# Add to PATH if possible
if [ -d "$HOME/.local/bin" ]; then
    mv tjl-docker "$HOME/.local/bin/"
    print_green "✓ Installed convenience script to ~/.local/bin"
else
    print_yellow "! Could not install to PATH. The tjl-docker script remains in the current directory."
fi

# Create shell completion for Docker usage
print_blue "Creating shell completion..."
COMPLETION_DIR="$HOME/.local/share/bash-completion/completions"
mkdir -p "$COMPLETION_DIR"

cat > "$COMPLETION_DIR/tjl-docker" << 'EOF'
_tjl_docker_completion() {
    local cur prev opts templates environments
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    opts="--path --environments --template --help --version"
    templates="basic microservice webapp library"
    environments="local,dev,staging,prod"
    
    case ${prev} in
        --template)
            COMPREPLY=( $(compgen -W "${templates}" -- ${cur}) )
            return 0
            ;;
        --path)
            COMPREPLY=( $(compgen -d -- ${cur}) )
            return 0
            ;;
        --environments)
            COMPREPLY=( $(compgen -W "${environments}" -- ${cur}) )
            return 0
            ;;
        *)
            if [[ ${cur} == -* ]] ; then
                COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                return 0
            fi
            COMPREPLY=( $(compgen -d -- ${cur}) )
            return 0
            ;;
    esac
}

complete -F _tjl_docker_completion tjl-docker
EOF

print_green "✓ Created shell completion"

# Print completion message
echo
print_green "Docker setup complete!"
echo
echo "You can now use TJL Project Setup Tool with Docker:"
echo
echo "Using docker-compose:"
echo "  docker-compose run --rm tjl-project my-project"
echo
echo "Using convenience script:"
echo "  tjl-docker my-project"
echo
echo "For help:"
echo "  tjl-docker --help"
echo
print_blue "Happy coding!"