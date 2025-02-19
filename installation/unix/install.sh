#!/usr/bin/env bash

# TJL Project Setup Tool - Unix Installer
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
print_blue "=== TJL Project Setup Tool Installer ==="
echo

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    OS="linux"
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    print_red "Error: Python 3 is not installed"
    if [ "$OS" == "macos" ]; then
        echo "Please install Python using Homebrew: brew install python"
    else
        echo "Please install Python using your package manager:"
        echo "Ubuntu/Debian: sudo apt install python3"
        echo "Fedora: sudo dnf install python3"
    fi
    exit 1
fi
print_green "✓ Python is installed"

# Check Git installation
if ! command -v git &> /dev/null; then
    print_red "Error: Git is not installed"
    if [ "$OS" == "macos" ]; then
        echo "Please install Git using Homebrew: brew install git"
    else
        echo "Please install Git using your package manager:"
        echo "Ubuntu/Debian: sudo apt install git"
        echo "Fedora: sudo dnf install git"
    fi
    exit 1
fi
print_green "✓ Git is installed"

# Create installation directory
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"
print_green "✓ Created installation directory"

# Copy files
print_blue "Copying files..."
cp tjl-project.py "$INSTALL_DIR/tjl-project"
chmod +x "$INSTALL_DIR/tjl-project"
print_green "✓ Copied and made executable"

# Detect shell
detect_shell() {
    if [ -n "$ZSH_VERSION" ]; then
        echo "zsh"
    elif [ -n "$BASH_VERSION" ]; then
        echo "bash"
    else
        echo "unknown"
    fi
}

SHELL_TYPE=$(detect_shell)
SHELL_CONFIG=""

# Configure shell
case $SHELL_TYPE in
    "zsh")
        SHELL_CONFIG="$HOME/.zshrc"
        ;;
    "bash")
        if [ "$OS" == "macos" ]; then
            SHELL_CONFIG="$HOME/.bash_profile"
        else
            SHELL_CONFIG="$HOME/.bashrc"
        fi
        ;;
    *)
        print_yellow "! Unsupported shell. Please manually configure your shell."
        ;;
esac

if [ -n "$SHELL_CONFIG" ]; then
    # Add to PATH if not already there
    if ! grep -q "PATH=\"\$HOME/.local/bin:\$PATH\"" "$SHELL_CONFIG"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
        print_green "✓ Added to PATH"
    else
        print_yellow "! PATH already configured"
    fi

    # Add alias
    if ! grep -q "alias tjl='tjl-project'" "$SHELL_CONFIG"; then
        echo "alias tjl='tjl-project'" >> "$SHELL_CONFIG"
        print_green "✓ Added shell alias"
    else
        print_yellow "! Alias already exists"
    fi
fi

# Shell completion
COMPLETION_DIR="$HOME/.local/share/bash-completion/completions"
mkdir -p "$COMPLETION_DIR"

cat > "$COMPLETION_DIR/tjl-project" << 'EOF'
_tjl_project_completion() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    local opts="--path --environments --template --help --version"
    
    case ${cur} in
        -*)
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            ;;
        *)
            COMPREPLY=( $(compgen -f ${cur}) )
            ;;
    esac
}

complete -F _tjl_project_completion tjl-project
complete -F _tjl_project_completion tjl
EOF

print_green "✓ Added shell completion"

# Create Docker support
if command -v docker &> /dev/null; then
    print_blue "Setting up Docker support..."
    
    # Create Dockerfile
    cat > Dockerfile << 'EOF'
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY tjl-project.py /usr/local/bin/tjl-project
RUN chmod +x /usr/local/bin/tjl-project

WORKDIR /workspace
ENTRYPOINT ["tjl-project"]
EOF

    # Add Docker alias to shell config
    if [ -n "$SHELL_CONFIG" ]; then
        if ! grep -q "alias tjl-docker=" "$SHELL_CONFIG"; then
            echo 'alias tjl-docker="docker run -v \$(pwd):/workspace tjl-project"' >> "$SHELL_CONFIG"
            print_green "✓ Added Docker alias"
        fi
    fi
fi

# Final instructions
echo
print_green "Installation complete!"
echo
echo "Please restart your terminal or run:"
echo "  source $SHELL_CONFIG"
echo
echo "Usage:"
echo "  tjl-project my-project"
echo "  tjl my-project (using alias)"
if command -v docker &> /dev/null; then
    echo "  tjl-docker my-project (using Docker)"
fi
echo
echo "For help:"
echo "  tjl-project --help"
echo
print_blue "Happy coding!"