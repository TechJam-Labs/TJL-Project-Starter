# TJL Project Setup Tool - Installation Guide

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
  - [Windows Installation](#windows-installation)
  - [Linux/macOS Installation](#linuxmacos-installation)
  - [Docker Installation](#docker-installation)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Updating](#updating)
- [Uninstallation](#uninstallation)

## Prerequisites

Before installing TJL Project Setup Tool, ensure you have the following:

### Required Software
- Python 3.6 or higher
- Git 2.22 or higher
- pip (Python package installer)

### Optional Dependencies
- Docker (for container-based usage)
- PowerShell 5.0 or higher (for Windows PowerShell integration)

### System Requirements
- 100MB free disk space
- Internet connection for initial installation
- Administrative privileges (for Windows) or sudo access (for Linux)

## Installation Methods

Choose the installation method that best suits your environment and needs.

### Windows Installation

1. **Download Repository**
   ```powershell
   # Clone the repository
   git clone https://github.com/TechJam-Labs/TJL-Project-Starter.git
   cd TJL-Project-Starter
   
   # Or download and extract the ZIP file
   # https://github.com/TechJam-Labs/TJL-Project-Starter/archive/main.zip
   ```

2. **Run Installer**
   ```powershell
   # Run installer (from any directory)
   .\installation\windows\install.bat
   ```

3. **Verify Installation**
   ```powershell
   # Restart PowerShell and verify
   tjl-project --version
   ```

### Linux/macOS Installation

1. **Download Installer**
   ```bash
   # Download installer
   curl -O https://raw.githubusercontent.com/TechJam-Labs/TJL-Project-Starter/main/installation/unix/install.sh
   
   # Make executable
   chmod +x install.sh
   ```

2. **Run Installation**
   ```bash
   # Execute installer
   ./install.sh
   ```

3. **Reload Shell**
   ```bash
   # Reload shell configuration
   source ~/.bashrc  # For Bash
   source ~/.zshrc   # For Zsh
   ```

### Docker Installation

1. **Download Docker Setup**
   ```bash
   curl -O https://raw.githubusercontent.com/TechJam-Labs/TJL-Project-Starter/main/installation/docker/docker-setup.sh
   chmod +x docker-setup.sh
   ```

2. **Run Docker Setup**
   ```bash
   ./docker-setup.sh
   ```

3. **Verify Docker Installation**
   ```bash
   tjl-docker --version
   ```

## Verification

After installation, verify the setup:

```bash
# Check version
tjl-project --version

# Display help
tjl-project --help

# Test template listing
tjl-project --list-templates
```

## Troubleshooting

### Common Issues

1. **Command Not Found**
   ```bash
   # Windows: Refresh PATH
   refreshenv
   
   # Linux/macOS: Reload shell
   source ~/.bashrc
   ```

2. **Permission Denied**
   ```bash
   # Linux/macOS
   chmod +x ~/.local/bin/tjl-project
   
   # Windows: Run as Administrator
   Start-Process powershell -Verb RunAs
   ```

3. **Python Not Found**
   ```bash
   # Verify Python installation
   python --version
   
   # Install Python if needed
   # Windows: Download from python.org
   # Linux: sudo apt install python3
   # macOS: brew install python
   ```

## Updating

Keep your installation up to date:

```bash
# Check current version
tjl-project --version

# Update tool
tjl-project --update

# Force update
tjl-project --update --force
```

## Uninstallation

Remove TJL Project Setup Tool from your system:

### Windows
```powershell
# Run uninstaller
C:\Tools\tjl-project-uninstall.bat
```

### Linux/macOS
```bash
# Run uninstaller
~/.local/lib/tjl-project/bin/tjl-uninstall.sh
```

### Docker
```bash
# Remove Docker image and scripts
docker rmi tjl-project
rm ~/.local/bin/tjl-docker
```

## Support

If you encounter any issues:
- Email: ben@techjamlabs.com
- Phone: +2348099999928
- GitHub Issues: [TJL Project Setup Issues](https://github.com/TechJam-Labs/TJL-Project-Starter/issues)

## Next Steps

After installation, see:
- [Quick Start Guide](quickstart.md) for your first project
- [Environment Management](environment-management.md) for configuration
- [Repository Strategy](repository-strategy.md) for version control best practices

# Copy utility scripts
cp scripts/switch_env.sh ~/.local/bin/
cp scripts/deploy.sh ~/.local/bin/
chmod +x ~/.local/bin/switch_env.sh
chmod +x ~/.local/bin/deploy.sh