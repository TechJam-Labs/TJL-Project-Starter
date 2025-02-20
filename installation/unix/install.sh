#!/usr/bin/env bash

# TJL Project Setup Tool - Unix Installer
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
print_blue "=== TJL Project Setup Tool Installer ==="
echo

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    OS="linux"
fi

# Installation directories
INSTALL_BASE="$HOME/.local"
INSTALL_DIR="$INSTALL_BASE/lib/tjl-project"
BIN_DIR="$INSTALL_BASE/bin"
COMPLETION_DIR="$INSTALL_BASE/share/bash-completion/completions"
ZSH_COMPLETION_DIR="$INSTALL_BASE/share/zsh/site-functions"

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Check system requirements
check_requirements() {
    print_blue "Checking system requirements..."

    # Check Python
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

    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_red "Error: pip3 is not installed"
        if [ "$OS" == "macos" ]; then
            echo "Please install pip using Homebrew: brew install python"
        else
            echo "Please install pip using your package manager:"
            echo "Ubuntu/Debian: sudo apt install python3-pip"
            echo "Fedora: sudo dnf install python3-pip"
        fi
        exit 1
    fi
    print_green "✓ pip is installed"

    # Check Git
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
}

# Create directories
create_directories() {
    print_blue "Creating installation directories..."
    
    mkdir -p "$INSTALL_DIR"/{bin,lib,templates,docs}
    mkdir -p "$BIN_DIR"
    mkdir -p "$COMPLETION_DIR"
    mkdir -p "$ZSH_COMPLETION_DIR"
    
    # Create template directories
    for template in basic microservice webapp library; do
        mkdir -p "$INSTALL_DIR/templates/$template"
        print_green "✓ Created template directory: $template"
    done
}

# Install Python dependencies
install_dependencies() {
    print_blue "Installing Python dependencies..."
    
    pip3 install --user --upgrade pip
    pip3 install --user colorama click jinja2 pyyaml
    print_green "✓ Installed Python dependencies"
}

# Copy files
copy_files() {
    print_blue "Copying files..."
    cd "$PROJECT_ROOT"

    # Copy main script
    cp src/tjl-project.py "$INSTALL_DIR/bin/"
    chmod +x "$INSTALL_DIR/bin/tjl-project.py"

    # Create symlink
    ln -sf "$INSTALL_DIR/bin/tjl-project.py" "$BIN_DIR/tjl-project"
    chmod +x "$BIN_DIR/tjl-project"

    # Copy templates
    print_blue "Copying templates..."
    mkdir -p "$INSTALL_DIR/templates"
    cp -r templates/basic "$INSTALL_DIR/templates/"
    cp -r templates/microservice "$INSTALL_DIR/templates/"
    cp -r templates/webapp "$INSTALL_DIR/templates/"
    cp -r templates/library "$INSTALL_DIR/templates/"
    print_green "✓ Copied templates"

    # Copy documentation
    print_blue "Copying documentation..."
    mkdir -p "$INSTALL_DIR/docs"
    cp -r docs/* "$INSTALL_DIR/docs/"
    print_green "✓ Copied documentation"

    # Copy example projects
    print_blue "Copying example projects..."
    mkdir -p "$INSTALL_DIR/examples"
    cp -r examples/basic-example "$INSTALL_DIR/examples/basic"
    cp -r examples/microservice-example "$INSTALL_DIR/examples/microservice"
    cp -r examples/webapp-example "$INSTALL_DIR/examples/webapp"
    cp -r examples/library-example "$INSTALL_DIR/examples/library"
    print_green "✓ Copied example projects"

    print_green "✓ Copied all files"
}

# Configure shell
configure_shell() {
    print_blue "Configuring shell..."

    # Detect shell
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_TYPE="zsh"
        SHELL_CONFIG="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_TYPE="bash"
        if [ "$OS" == "macos" ]; then
            SHELL_CONFIG="$HOME/.bash_profile"
        else
            SHELL_CONFIG="$HOME/.bashrc"
        fi
    else
        print_yellow "! Unsupported shell. Please manually configure your shell."
        return
    fi

    # Add to PATH
    if ! grep -q "PATH=\"\$HOME/.local/bin:\$PATH\"" "$SHELL_CONFIG" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
        print_green "✓ Added to PATH"
    else
        print_yellow "! PATH already configured"
    fi

    # Add alias
    if ! grep -q "alias tjl='tjl-project'" "$SHELL_CONFIG" 2>/dev/null; then
        echo "alias tjl='tjl-project'" >> "$SHELL_CONFIG"
        print_green "✓ Added shell alias"
    else
        print_yellow "! Alias already exists"
    fi
}

# Create shell completion
create_shell_completion() {
    print_blue "Creating shell completion..."

    # Bash completion
    cat > "$COMPLETION_DIR/tjl-project" << 'EOF'
_tjl_project_completion() {
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

complete -F _tjl_project_completion tjl-project
complete -F _tjl_project_completion tjl
EOF

    # Zsh completion
    cat > "$ZSH_COMPLETION_DIR/_tjl-project" << 'EOF'
#compdef tjl-project tjl

_tjl_project() {
    local curcontext="$curcontext" state line ret=1
    typeset -A opt_args

    _arguments -C \
        '1: :->command' \
        '*: :->args' && ret=0

    case $state in
        command)
            _path_files -/ && ret=0
            ;;
        args)
            local opts=(
                '--path[Specify base path for project creation]:directory:_path_files -/'
                '--environments[Specify comma-separated list of environments]:environments:(local,dev,staging,prod dev,staging,prod local,dev,qa,staging,prod)'
                '--template[Select project template]:template:(basic microservice webapp library)'
                '--help[Show help message]'
                '--version[Show version information]'
            )
            _describe -t opts 'options' opts && ret=0
            ;;
    esac

    return ret
}

_tjl_project "$@"
EOF

    print_green "✓ Created shell completion scripts"
}

# Create environment setup script
create_env_setup() {
    print_blue "Creating environment setup script..."
    
    cat > "$INSTALL_DIR/bin/tjl-env-setup.sh" << 'EOF'
#!/usr/bin/env bash

# TJL Project environment setup
export PYTHONPATH="$HOME/.local/lib/tjl-project/lib:$PYTHONPATH"
export TJL_PROJECT_ROOT="$HOME/.local/lib/tjl-project"
export TJL_PROJECT_TEMPLATES="$TJL_PROJECT_ROOT/templates"
export TJL_PROJECT_DOCS="$TJL_PROJECT_ROOT/docs"
EOF

    chmod +x "$INSTALL_DIR/bin/tjl-env-setup.sh"
    
    # Add to shell config
    echo "source $INSTALL_DIR/bin/tjl-env-setup.sh" >> "$SHELL_CONFIG"
    
    print_green "✓ Created environment setup script"
}

# Verify installation
verify_installation() {
    print_blue "Verifying installation..."
    
    if ! command -v tjl-project &> /dev/null; then
        print_red "Error: Installation verification failed"
        print_yellow "Please ensure $BIN_DIR is in your PATH"
        exit 1
    fi
    
    # Test command execution
    if ! tjl-project --version &> /dev/null; then
        print_red "Error: Command execution failed"
        exit 1
    fi
    
    print_green "✓ Installation verified"
}

# Create uninstall script
create_uninstall_script() {
    print_blue "Creating uninstall script..."
    
    cat > "$INSTALL_DIR/bin/tjl-uninstall.sh" << 'EOF'
#!/usr/bin/env bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${RED}Uninstalling TJL Project Setup Tool...${NC}"

# Remove installation directory
rm -rf "$HOME/.local/lib/tjl-project"

# Remove binary
rm -f "$HOME/.local/bin/tjl-project"

# Remove completions
rm -f "$HOME/.local/share/bash-completion/completions/tjl-project"
rm -f "$HOME/.local/share/zsh/site-functions/_tjl-project"

# Remove from PATH and aliases
if [ -f "$HOME/.bashrc" ]; then
    sed -i '/tjl-project/d' "$HOME/.bashrc"
fi
if [ -f "$HOME/.zshrc" ]; then
    sed -i '/tjl-project/d' "$HOME/.zshrc"
fi

echo -e "${GREEN}TJL Project Setup Tool has been uninstalled${NC}"
EOF

    chmod +x "$INSTALL_DIR/bin/tjl-uninstall.sh"
    print_green "✓ Created uninstall script"
}

# Main installation function
main() {
    # Check if running with sudo
    if [ "$EUID" -eq 0 ]; then
        print_red "Please do not run this installer with sudo"
        exit 1
    }

    # Run installation steps
    check_requirements
    create_directories
    install_dependencies
    copy_files
    configure_shell
    create_shell_completion
    create_env_setup
    create_uninstall_script
    verify_installation

    # Print completion message
    echo
    print_green "Installation complete!"
    echo
    echo "Please restart your terminal or run:"
    echo "  source $SHELL_CONFIG"
    echo
    echo "Usage:"
    echo "  tjl-project my-project"
    echo "  tjl my-project (using alias)"
    echo
    echo "For help:"
    echo "  tjl-project --help"
    echo
    echo "To uninstall:"
    echo "  $INSTALL_DIR/bin/tjl-uninstall.sh"
    echo
    print_blue "Happy coding!"
}

# Check for help flag
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "TJL Project Setup Tool Installer"
    echo
    echo "Usage:"
    echo "  ./install.sh [--help]"
    echo
    echo "Options:"
    echo "  --help, -h  Show this help message"
    exit 0
fi

# Run main installation
main