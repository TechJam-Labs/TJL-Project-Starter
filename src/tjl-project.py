#!/usr/bin/env python3
"""
TJL Project Setup Tool
=====================

A comprehensive project initialization and management system designed to establish
standardized development practices across teams and projects.

Author: Ben Adenle
Email: ben@techjamlabs.com
Phone: +2348099999928
Version: 1.0.0
License: MIT

Usage:
    tjl-project my-project [--path /path/to/project] [--template type] [--environments env1,env2]

Templates:
    basic        - Basic project structure
    microservice - Microservice architecture
    webapp       - Web application
    library     - Reusable library

Example:
    tjl-project my-app --template webapp --environments local,dev,staging,prod
"""

import os
import sys
import logging
import shutil
import subprocess
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ColorOutput:
    """Utility class for colored terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def print_header(message: str) -> None:
        """Print a header message."""
        print(f"\n{ColorOutput.HEADER}{ColorOutput.BOLD}=== {message} ==={ColorOutput.ENDC}")

    @staticmethod
    def print_step(message: str) -> None:
        """Print a step message."""
        print(f"{ColorOutput.BLUE}→ {message}{ColorOutput.ENDC}")

    @staticmethod
    def print_success(message: str) -> None:
        """Print a success message."""
        print(f"{ColorOutput.GREEN}✓ {message}{ColorOutput.ENDC}")

    @staticmethod
    def print_warning(message: str) -> None:
        """Print a warning message."""
        print(f"{ColorOutput.YELLOW}! {message}{ColorOutput.ENDC}")

    @staticmethod
    def print_error(message: str) -> None:
        """Print an error message."""
        print(f"{ColorOutput.RED}✗ {message}{ColorOutput.ENDC}")

class GitError(Exception):
    """Custom exception for git-related errors."""
    pass

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class ProjectError(Exception):
    """Custom exception for project-related errors."""
    pass

class BaseTemplate:
    """Base class for all project templates."""
    
    def __init__(self, project_path: str, environments: List[str]):
        self.project_path = project_path
        self.environments = environments
        self.project_name = os.path.basename(project_path)
        self.template_type = self.__class__.__name__.lower().replace('template', '')

    def get_directories(self) -> List[str]:
        """Get list of directories to create."""
        return [
            '',  # Project root
            'config',
            *[f'config/{env}' for env in self.environments],
            'docs',
            'docs/api',
            'docs/setup',
            'scripts',
            'src',
            'src/core',
            'src/utils',
            'tests',
            'tests/unit',
            'tests/integration',
            '.github/workflows'
        ]

    def get_files(self) -> Dict[str, str]:
        """Get dictionary of files to create with their content."""
        return {
            'README.md': self._get_readme_content(),
            '.gitignore': self._get_gitignore_content(),
            '.editorconfig': self._get_editorconfig_content(),
            'scripts/switch_env.sh': self._get_switch_env_content(),
            'scripts/deploy.sh': self._get_deploy_script_content(),
            'scripts/run_tests.sh': self._get_test_script_content(),
            '.github/workflows/ci.yml': self._get_workflow_content(),
            'docs/README.md': self._get_docs_readme_content(),
            'src/core/__init__.py': self._get_core_init_content(),
            'src/utils/__init__.py': self._get_utils_init_content(),
            'tests/conftest.py': self._get_conftest_content()
        }

    def _get_readme_content(self) -> str:
        """Generate README.md content."""
        return f"""# {self.project_name}

Project created with TJL Project Setup Tool using the {self.template_type} template.

## Overview

[Add project description here]

## Features

- Feature 1
- Feature 2
- Feature 3

## Setup

1. Clone the repository
2. Install dependencies
3. Configure environment
4. Run setup script

## Development

1. Switch to development environment:
   ```bash
   ./scripts/switch_env.sh dev
   ```

2. Start development

## Testing

Run the tests:
```bash
./scripts/run_tests.sh
```

## Deployment

Deploy to environments:
```bash
./scripts/deploy.sh <environment>
```

## Documentation

See [docs/](docs/) for detailed documentation.

## License

[Add license information here]

## Contact

- Author: [Your Name]
- Email: [your.email@example.com]
"""

    def _get_gitignore_content(self) -> str:
        """Generate .gitignore content."""
        return """# Environment
.env
*.env
env.conf
__pycache__/
*.py[cod]
*$py.class
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env.*

# IDE
.idea/
.vscode/
*.swp
*.swo
*~
*.iml
.project
.classpath
.settings/
*.sublime-workspace
*.sublime-project

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
Icon?
Desktop.ini

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Dependencies
node_modules/
venv/
.venv/
vendor/
bower_components/

# Testing
coverage/
.coverage
.pytest_cache/
.tox/
.nox/
htmlcov/
.hypothesis/

# Build
dist/
build/
out/
target/

# Temporary files
*.tmp
*.bak
*.swp
*~.nib
.*.sw[a-p]

# Security
*.pem
*.key
*.cert
.env.prod
.env.staging
.env.local
"""

    def _get_editorconfig_content(self) -> str:
        """Generate .editorconfig content."""
        return """root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{js,jsx,ts,tsx,css,scss,json,yml,yaml,html}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
max_line_length = 120

[Makefile]
indent_style = tab

[*.{bat,cmd}]
end_of_line = crlf
"""

    def _get_switch_env_content(self) -> str:
        """Generate environment switching script content."""
        envs = " ".join(self.environments)
        return f"""#!/usr/bin/env bash
# Environment switching script for TJL Project

set -e

ENVIRONMENTS=({envs})
CURRENT_ENV="local"
ENV_FILE=".current_env"

function show_usage() {{
    echo "TJL Project Environment Switcher"
    echo
    echo "Usage: ./switch_env.sh <environment> [--force] [--backup]"
    echo
    echo "Options:"
    echo "  --force   Force switch even if there are uncommitted changes"
    echo "  --backup  Create backup of current environment"
    echo
    echo "Available environments: ${{ENVIRONMENTS[*]}}"
    exit 1
}}

# Parse arguments
ENVIRONMENT=""
FORCE="false"
BACKUP="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE="true"
            shift
            ;;
        --backup)
            BACKUP="true"
            shift
            ;;
        -h|--help)
            show_usage
            ;;
        *)
            if [[ -z "$ENVIRONMENT" ]]; then
                ENVIRONMENT="$1"
            else
                echo "Error: Unknown argument '$1'"
                show_usage
            fi
            shift
            ;;
    esac
done

# Validate environment
if [[ ! " ${{ENVIRONMENTS[*]}} " =~ " ${{ENVIRONMENT}} " ]]; then
    echo "Error: Invalid environment '$ENVIRONMENT'"
    show_usage
fi

# Check git status
if [[ $(git status --porcelain) ]]; then
    if [[ "$FORCE" != "true" ]]; then
        echo "Error: You have uncommitted changes"
        echo "Commit your changes or use --force to switch anyway"
        exit 1
    else
        echo "Warning: Switching with uncommitted changes"
    fi
fi

# Create backup if requested
if [[ "$BACKUP" == "true" && -f "$ENV_FILE" ]]; then
    CURRENT_ENV=$(cat "$ENV_FILE")
    BACKUP_DIR="config/${{CURRENT_ENV}}.backup_$(date +%Y%m%d_%H%M%S)"
    echo "Creating backup of $CURRENT_ENV environment in $BACKUP_DIR"
    cp -r "config/$CURRENT_ENV" "$BACKUP_DIR"
fi

# Load environment configuration
if [[ -f "config/${{ENVIRONMENT}}/env.conf" ]]; then
    source "config/${{ENVIRONMENT}}/env.conf"
    echo "Switched to ${{ENVIRONMENT}} environment"
else
    echo "Warning: No configuration found for ${{ENVIRONMENT}} environment"
fi

# Switch git branch if applicable (except for local)
if [[ "${{ENVIRONMENT}}" != "local" ]]; then
    if git show-ref --verify --quiet "refs/heads/${{ENVIRONMENT}}"; then
        git checkout "${{ENVIRONMENT}}"
    else
        git checkout -b "${{ENVIRONMENT}}"
    fi
fi

# Save current environment
echo "${{ENVIRONMENT}}" > "$ENV_FILE"
export CURRENT_ENV="${{ENVIRONMENT}}"

# Run environment-specific setup if exists
if [[ -f "scripts/setup_${{ENVIRONMENT}}.sh" ]]; then
    echo "Running environment-specific setup..."
    source "scripts/setup_${{ENVIRONMENT}}.sh"
fi

echo "Successfully switched to ${{ENVIRONMENT}} environment"
"""

    def _get_deploy_script_content(self) -> str:
        """Generate deployment script content."""
        return """#!/usr/bin/env bash
# Deployment script for TJL Project

set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
YELLOW='\\033[1;33m'
NC='\\033[0m'

# Print with color
print_blue() { echo -e "${BLUE}$1${NC}"; }
print_green() { echo -e "${GREEN}$1${NC}"; }
print_red() { echo -e "${RED}$1${NC}"; }
print_yellow() { echo -e "${YELLOW}$1${NC}"; }

# Show usage
show_usage() {
    echo "TJL Project Deployment Script"
    echo
    echo "Usage:"
    echo "  $0 <environment> [--skip-tests] [--force]"
    echo
    echo "Options:"
    echo "  --skip-tests  Skip running tests before deployment"
    echo "  --force       Force deployment even if tests fail"
    exit 1
}

# Parse arguments
ENVIRONMENT=""
SKIP_TESTS="false"
FORCE="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-tests)
            SKIP_TESTS="true"
            shift
            ;;
        --force)
            FORCE="true"
            shift
            ;;
        -h|--help)
            show_usage
            ;;
        *)
            if [[ -z "$ENVIRONMENT" ]]; then
                ENVIRONMENT="$1"
            else
                print_red "Error: Unknown argument '$1'"
                show_usage
            fi
            shift
            ;;
    esac
done

# Check if environment is provided
if [[ -z "$ENVIRONMENT" ]]; then
    show_usage
fi

# Load environment configuration
if [[ ! -f "config/$ENVIRONMENT/env.conf" ]]; then
    print_red "Error: Environment configuration not found"
    exit 1
fi
source "config/$ENVIRONMENT/env.conf"

# Run tests unless skipped 
if [[ "$SKIP_TESTS" != "true" ]]; then
    print_blue "Running tests..."
    if ! ./scripts/run_tests.sh; then
        if [[ "$FORCE" != "true" ]]; then
            print_red "Tests failed. Deployment aborted."
            exit 1
        else
            print_yellow "Tests failed but continuing due to --force"
        fi
    fi
fi

# Run environment-specific deployment
if [[ -f "scripts/deploy_$ENVIRONMENT.sh" ]]; then
    print_blue "Running environment-specific deployment..."
    source "scripts/deploy_$ENVIRONMENT.sh"
else
    print_yellow "No environment-specific deployment script found"
fi

print_green "Deployment completed successfully"
"""

    def _get_test_script_content(self) -> str:
        """Generate test script content."""
        return """#!/usr/bin/env bash
# Test script for TJL Project

set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
YELLOW='\\033[1;33m'
NC='\\033[0m'

# Print with color
print_blue() { echo -e "${BLUE}$1${NC}"; }
print_green() { echo -e "${GREEN}$1${NC}"; }
print_red() { echo -e "${RED}$1${NC}"; }

# Show usage
show_usage() {
    echo "TJL Project Test Runner"
    echo
    echo "Usage:"
    echo "  $0 [--unit] [--integration] [--coverage]"
    echo
    echo "Options:"
    echo "  --unit        Run only unit tests"
    echo "  --integration Run only integration tests"
    echo "  --coverage    Generate coverage report"
    exit 1
}

# Parse arguments
RUN_UNIT="true"
RUN_INTEGRATION="true"
COVERAGE="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --unit)
            RUN_INTEGRATION="false"
            shift
            ;;
        --integration)
            RUN_UNIT="false"
            shift
            ;;
        --coverage)
            COVERAGE="true"
            shift
            ;;
        -h|--help)
            show_usage
            ;;
        *)
            print_red "Error: Unknown argument '$1'"
            show_usage
            ;;
    esac
done

# Set up test environment
print_blue "Setting up test environment..."
if [[ -f "config/test/env.conf" ]]; then
    source "config/test/env.conf"
fi

# Run tests
if [[ "$COVERAGE" == "true" ]]; then
    PYTEST_ARGS="--cov=src/ --cov-report=html --cov-report=term"
else
    PYTEST_ARGS=""
fi

if [[ "$RUN_UNIT" == "true" ]]; then
    print_blue "Running unit tests..."
    python -m pytest tests/unit/ $PYTEST_ARGS
fi

if [[ "$RUN_INTEGRATION" == "true" ]]; then
    print_blue "Running integration tests..."
    python -m pytest tests/integration/ $PYTEST_ARGS
fi

print_green "All tests completed successfully"
"""

    def _get_workflow_content(self) -> str:
        """Generate GitHub Actions workflow content."""
        return """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
        
    - name: Run tests
      run: |
        ./scripts/run_tests.sh --coverage
        
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install black flake8 isort mypy
        
    - name: Run linting
      run: |
        black --check .
        isort --check-only .
        flake8 .
        mypy src/

  deploy:
    needs: [test, lint]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v'))
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy
      env:
        DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
      run: |
        if [[ $GITHUB_REF == refs/tags/* ]]; then
          echo "Deploying release $GITHUB_REF..."
          ./scripts/deploy.sh prod
        elif [[ $GITHUB_REF == refs/heads/main ]]; then
          echo "Deploying to staging..."
          ./scripts/deploy.sh staging
        fi
"""

    def _get_docs_readme_content(self) -> str:
        """Generate documentation README content."""
        return f"""# {self.project_name} Documentation

## Overview

This directory contains the complete documentation for the {self.project_name} project.

## Structure

- `api/` - API documentation
- `setup/` - Setup and installation guides
- `development/` - Development guidelines
- `deployment/` - Deployment procedures

## Getting Started

1. Installation
   - See `setup/installation.md`

2. Configuration
   - Environment setup
   - Dependencies
   - Third-party services

3. Development
   - Coding standards
   - Testing procedures
   - Version control workflow

4. Deployment
   - Environment management
   - Deployment procedures
   - Monitoring and maintenance

## Contributing

See `CONTRIBUTING.md` in the project root for contribution guidelines.

## License

[Add license information here]
"""

    def _get_core_init_content(self) -> str:
        """Generate core __init__.py content."""
        return f'''"""
Core functionality for {self.project_name}
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .config import Config
from .logger import Logger

__all__ = ["Config", "Logger"]
'''

    def _get_utils_init_content(self) -> str:
        """Generate utils __init__.py content."""
        return f'''"""
Utility functions for {self.project_name}
"""

from .helpers import load_config, ensure_directory

__all__ = ["load_config", "ensure_directory"]
'''

    def _get_conftest_content(self) -> str:
        """Generate conftest.py content."""
        return """import pytest
import os
from typing import Generator

@pytest.fixture
def test_config():
    """Test configuration fixture."""
    return {
        "test": True,
        "value": 42,
        "name": "test"
    }

@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory fixture."""
    return tmp_path
"""

class ProjectSetup:
    """Main class for project setup and management."""

    def __init__(
        self,
        project_name: str,
        base_path: Optional[str] = None,
        environments: Optional[List[str]] = None,
        template: str = "basic"
    ):
        """Initialize project setup with given parameters."""
        self.project_name = self._sanitize_project_name(project_name)
        self.base_path = os.path.abspath(base_path or os.getcwd())
        self.project_path = os.path.join(self.base_path, self.project_name)
        self.environments = environments or ['local', 'dev', 'staging', 'prod']
        self.template = template
        self.template_instance = self._get_template_instance()
        
        self._validate_inputs()

    def _sanitize_project_name(self, name: str) -> str:
        """Sanitize project name for file system compatibility."""
        # Replace spaces with hyphens and remove special characters
        name = re.sub(r'[^\w\s-]', '', name).strip()
        name = re.sub(r'[-\s]+', '-', name)
        return name.lower()

    def _validate_inputs(self) -> None:
        """Validate input parameters."""
        # Validate project name
        if not self.project_name:
            raise ValidationError("Project name cannot be empty")
        
        if not re.match(r'^[a-z][a-z0-9-_]*$', self.project_name):
            raise ValidationError(
                "Project name must start with a letter and contain only "
                "lowercase letters, numbers, hyphens, and underscores"
            )

        # Validate base path
        if not os.path.exists(self.base_path):
            raise ValidationError(f"Base path does not exist: {self.base_path}")

        if os.path.exists(self.project_path):
            raise ValidationError(f"Project directory already exists: {self.project_path}")

        # Validate environments
        for env in self.environments:
            if not re.match(r'^[a-z][a-z0-9-_]*$', env):
                raise ValidationError(
                    f"Invalid environment name: {env}. Must contain only "
                    "lowercase letters, numbers, hyphens, and underscores"
                )

        # Check git installation
        try:
            subprocess.run(
                ['git', '--version'],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError:
            raise EnvironmentError("Git is not installed or not accessible")
        except FileNotFoundError:
            raise EnvironmentError("Git is not installed")

    def _get_template_instance(self) -> BaseTemplate:
        """Get the appropriate template instance based on template type."""
        template_map = {
            "basic": BaseTemplate,
            "microservice": MicroserviceTemplate,
            "webapp": WebAppTemplate,
            "library": LibraryTemplate
        }
        
        template_class = template_map.get(self.template)
        if not template_class:
            raise ValidationError(f"Unknown template type: {self.template}")
            
        return template_class(self.project_path, self.environments)

    def create_directory_structure(self) -> None:
        """Create the project directory structure."""
        ColorOutput.print_header("Creating Directory Structure")
        
        directories = self.template_instance.get_directories()
        
        for dir_path in directories:
            full_path = os.path.join(self.project_path, dir_path)
            os.makedirs(full_path, exist_ok=True)
            if dir_path:  # Don't create .gitkeep in root
                Path(os.path.join(full_path, '.gitkeep')).touch()
            ColorOutput.print_success(f"Created: {dir_path or 'root'}")

    def create_files(self) -> None:
        """Create project files."""
        ColorOutput.print_header("Creating Project Files")
        
        files = self.template_instance.get_files()
        
        for file_path, content in files.items():
            full_path = os.path.join(self.project_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if file_path.endswith('.sh'):
                os.chmod(full_path, 0o755)
            
            ColorOutput.print_success(f"Created: {file_path}")

    def setup_git(self) -> None:
        """Initialize git repository and create branch structure."""
        ColorOutput.print_header("Setting up Git Repository")

        try:
            # Initialize repository
            self._run_git_command("git init")
            ColorOutput.print_success("Initialized git repository")

            # Configure git
            git_configs = [
                ('core.autocrlf', 'true' if os.name == 'nt' else 'input'),
                ('core.eol', 'lf'),
                ('branch.main.mergeoptions', '--no-ff'),
                ('pull.rebase', 'true'),
                ('init.defaultBranch', 'main')
            ]
            
            for key, value in git_configs:
                self._run_git_command(f'git config --local {key} {value}')
            ColorOutput.print_success("Applied git configurations")

            # Create initial commit
            self._run_git_command("git add .")
            commit_message = f'''Initial project setup with TJL Project Setup Tool

Created on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Template: {self.template}
Environments: {', '.join(self.environments)}'''
            
            self._run_git_command(f'git commit -m "{commit_message}"')
            ColorOutput.print_success("Created initial commit")

            # Rename master to main if needed
            self._run_git_command("git branch -M main")
            
            # Create develop branch
            self._run_git_command("git checkout -b develop main")
            ColorOutput.print_success("Created develop branch")

            # Create environment-specific branches from develop
            for env in [e for e in self.environments if e not in ['local', 'dev']]:
                self._run_git_command(f"git checkout -b {env} develop")
                ColorOutput.print_success(f"Created {env} branch")

            # Create feature branch template
            self._run_git_command("git checkout -b feature/example develop")
            self._run_git_command("git checkout develop")
            self._run_git_command("git branch -D feature/example")
            ColorOutput.print_success("Set up feature branch template")

            # Create release branch template
            self._run_git_command("git checkout -b release/0.1.0 develop")
            self._run_git_command("git checkout develop")
            self._run_git_command("git branch -D release/0.1.0")
            ColorOutput.print_success("Set up release branch template")

            # Create hotfix branch template
            self._run_git_command("git checkout -b hotfix/example main")
            self._run_git_command("git checkout main")
            self._run_git_command("git branch -D hotfix/example")
            ColorOutput.print_success("Set up hotfix branch template")

            # Set up branch protections
            self._setup_branch_protection()
            
            # Set up git hooks
            self._setup_git_hooks()

            # Return to main branch
            self._run_git_command("git checkout main")
            ColorOutput.print_success("Switched back to main branch")

            # Create initial tag
            self._run_git_command('git tag -a v0.1.0 -m "Initial project setup"')
            ColorOutput.print_success("Created initial tag")

        except subprocess.CalledProcessError as e:
            ColorOutput.print_error(f"Git setup failed: {str(e)}")
            raise GitError(f"Git setup failed: {str(e)}")

    def _setup_branch_protection(self) -> None:
        """Set up branch protection rules."""
        protected_branches_config = """
[branch "main"]
    remote = origin
    merge = refs/heads/main
    pushRemote = origin
    mergeoptions = --no-ff
    protection = true

[branch "develop"]
    remote = origin
    merge = refs/heads/develop
    pushRemote = origin
    mergeoptions = --no-ff
    protection = true

[protection "main"]
    requiredSignatures = true
    requiredLinearHistory = true
    requiredStatusChecks = true
    requiredApprovingReviewCount = 2
    pushRestriction = true

[protection "develop"]
    requiredSignatures = true
    requiredLinearHistory = true
    requiredStatusChecks = true
    requiredApprovingReviewCount = 1
    pushRestriction = false
"""
        git_config_path = os.path.join(self.project_path, '.git', 'config')
        with open(git_config_path, 'a') as f:
            f.write(protected_branches_config)
        ColorOutput.print_success("Set up branch protections")

    def _setup_git_hooks(self) -> None:
        """Set up git hooks."""
        hooks_dir = os.path.join(self.project_path, '.git', 'hooks')
        
        # Pre-commit hook
        pre_commit_content = """#!/bin/sh
# Pre-commit hook for code quality checks

# Check for staged changes
if git diff --cached --quiet; then
    exit 0
fi

# Run linting and formatting checks based on project type
case "$(git rev-parse --git-dir)" in
    *) # Default checks
        echo "Running code quality checks..."
        # Add your quality checks here
        exit $?
        ;;
esac
"""
        pre_commit_path = os.path.join(hooks_dir, 'pre-commit')
        with open(pre_commit_path, 'w') as f:
            f.write(pre_commit_content)
        os.chmod(pre_commit_path, 0o755)

        # Prepare-commit-msg hook
        prepare_commit_msg_content = """#!/bin/sh
# Prepare-commit-msg hook for commit message formatting

COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2

# Get the current branch name
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)

# Add branch name to commit message if not already present
if ! grep -q "^$BRANCH_NAME:" "$COMMIT_MSG_FILE"; then
    case "$BRANCH_NAME" in
        feature/*|bugfix/*|hotfix/*|release/*)
            sed -i.bak -e "1s/^/$BRANCH_NAME: /" "$COMMIT_MSG_FILE"
            ;;
    esac
fi
"""
        prepare_commit_msg_path = os.path.join(hooks_dir, 'prepare-commit-msg')
        with open(prepare_commit_msg_path, 'w') as f:
            f.write(prepare_commit_msg_content)
        os.chmod(prepare_commit_msg_path, 0o755)

        ColorOutput.print_success("Set up git hooks")

    def _run_git_command(self, command: str) -> None:
        """Run a git command and handle errors."""
        try:
            result = subprocess.run(
                command,
                cwd=self.project_path,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                logger.debug(f"Git command output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {command}")
            logger.error(f"Error output: {e.stderr}")
            raise GitError(f"Git command failed: {e.stderr}")

    def setup_project(self) -> None:
        """Execute the complete project setup."""
        try:
            ColorOutput.print_header(f"Setting up project: {self.project_name}")
            
            self.create_directory_structure()
            self.create_files()
            self.setup_git()

            ColorOutput.print_header("Project Setup Complete!")
            self._print_next_steps()

        except Exception as e:
            ColorOutput.print_error(f"Error during setup: {str(e)}")
            logger.error(f"Project setup failed: {str(e)}", exc_info=True)
            # Clean up on failure
            if os.path.exists(self.project_path):
                shutil.rmtree(self.project_path)
            raise ProjectError(f"Project setup failed: {str(e)}")

    def _print_next_steps(self) -> None:
        """Print next steps for the user."""
        steps = [
            ("Next Steps", [
                "1. Review and customize the environment configurations in config/",
                "2. Set up your remote Git repository",
                "3. Push your code: git push -u origin main",
                "4. Use ./scripts/switch_env.sh to switch between environments",
                f"5. Create environment-specific configs in config/<env>/",
                "6. Review documentation in docs/"
            ])
        ]

        for title, items in steps:
            ColorOutput.print_header(title)
            for item in items:
                ColorOutput.print_step(item)
            print()

class MicroserviceTemplate(BaseTemplate):
    """Template for microservice projects."""
    
    def get_directories(self) -> List[str]:
        """Get microservice-specific directories."""
        dirs = super().get_directories()
        return dirs + [
            'src/api',
            'src/api/routes',
            'src/api/middleware',
            'src/api/schemas',
            'src/services',
            'src/models',
            'deployment',
            'deployment/kubernetes',
            'deployment/docker',
            'deployment/terraform',
            'deployment/scripts'
        ]

    def get_files(self) -> Dict[str, str]:
        """Get microservice-specific files."""
        files = super().get_files()
        files.update({
            'Dockerfile': self._get_dockerfile_content(),
            'docker-compose.yml': self._get_docker_compose_content(),
            'deployment/kubernetes/deployment.yml': self._get_k8s_deployment_content(),
            'deployment/kubernetes/service.yml': self._get_k8s_service_content(),
            'deployment/terraform/main.tf': self._get_terraform_content(),
            'src/api/routes/health.py': self._get_health_route_content(),
            'src/api/middleware/logging.py': self._get_logging_middleware_content(),
            'src/api/schemas/base.py': self._get_base_schema_content(),
            'src/services/base.py': self._get_base_service_content(),
            'src/models/base.py': self._get_base_model_content(),
            'requirements.txt': self._get_requirements_content()
        })
        return files

    def _get_dockerfile_content(self) -> str:
        """Generate Dockerfile content."""
        return """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \\
    apt-get install -y --no-install-recommends \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY config/ config/

# Set environment variables
ENV PYTHONPATH=/app
ENV APP_ENV=production

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]"""

    def _get_docker_compose_content(self) -> str:
        """Generate docker-compose.yml content."""
        return """version: '3.8'

services:
  app:
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=development
      - DATABASE_URL=postgresql://user:password@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./src:/app/src
      - ./config:/app/config
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:"""

    def _get_k8s_deployment_content(self) -> str:
        """Generate Kubernetes deployment content."""
        return """apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: microservice
  template:
    metadata:
      labels:
        app: microservice
    spec:
      containers:
      - name: app
        image: app:latest
        ports:
        - containerPort: 8000
        env:
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_ENV
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20"""

    def _get_health_route_content(self) -> str:
        """Generate health check route content."""
        return '''from fastapi import APIRouter
from typing import Dict
import time

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": str(time.time()),
        "version": "1.0.0"
    }'''

    def _get_base_service_content(self) -> str:
        """Generate base service content."""
        return '''from typing import Generic, TypeVar, Optional, List
from sqlalchemy.orm import Session
from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseService(Generic[ModelType]):
    """Base class for all services."""
    
    def __init__(self, db: Session):
        self.db = db

    async def get(self, id: int) -> Optional[ModelType]:
        """Get single record by id."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    async def get_all(self) -> List[ModelType]:
        """Get all records."""
        return self.db.query(self.model).all()

    async def create(self, data: dict) -> ModelType:
        """Create new record."""
        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    async def update(self, id: int, data: dict) -> Optional[ModelType]:
        """Update existing record."""
        instance = await self.get(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    async def delete(self, id: int) -> bool:
        """Delete record by id."""
        instance = await self.get(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False'''

class WebAppTemplate(BaseTemplate):
    """Template for web application projects."""
    
    def get_directories(self) -> List[str]:
        """Get webapp-specific directories."""
        dirs = super().get_directories()
        return dirs + [
            'src/components',
            'src/components/common',
            'src/components/layout',
            'src/components/features',
            'src/pages',
            'src/styles',
            'src/hooks',
            'src/context',
            'src/utils',
            'public',
            'public/images',
            'public/fonts'
        ]

    def get_files(self) -> Dict[str, str]:
        """Get webapp-specific files."""
        files = super().get_files()
        files.update({
            'package.json': self._get_package_json_content(),
            'next.config.js': self._get_next_config_content(),
            '.eslintrc.js': self._get_eslint_content(),
            'tailwind.config.js': self._get_tailwind_config_content(),
            'src/styles/globals.css': self._get_global_styles_content(),
            'src/pages/_app.tsx': self._get_app_content(),
            'src/components/layout/Layout.tsx': self._get_layout_content(),
            'src/hooks/useAuth.ts': self._get_auth_hook_content(),
            'src/context/AuthContext.tsx': self._get_auth_context_content()
        })
        return files

class LibraryTemplate(BaseTemplate):
    """Template for library projects."""
    
    def get_directories(self) -> List[str]:
        """Get library-specific directories."""
        dirs = super().get_directories()
        return dirs + [
            'src/core',
            'src/utils',
            'src/exceptions',
            'src/interfaces',
            'examples',
            'examples/basic',
            'examples/advanced',
            'benchmarks',
            'docs/api',
            'docs/guides'
        ]

    def get_files(self) -> Dict[str, str]:
        """Get library-specific files."""
        files = super().get_files()
        files.update({
            'setup.py': self._get_setup_content(),
            'pyproject.toml': self._get_pyproject_content(),
            'MANIFEST.in': self._get_manifest_content(),
            'docs/conf.py': self._get_sphinx_config_content(),
            'src/core/base.py': self._get_base_class_content(),
            'src/exceptions/base.py': self._get_exceptions_content(),
            'benchmarks/benchmark.py': self._get_benchmark_content()
        })
        return files

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="TJL Project Setup Tool - Create a standardized project structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--path", help="Base path for project creation", default=None)
    parser.add_argument("--environments", 
                       help="Comma-separated list of environments",
                       default="local,dev,staging,prod")
    parser.add_argument("--template", 
                       help="Project template to use",
                       choices=['basic', 'microservice', 'webapp', 'library'],
                       default="basic")
    parser.add_argument('--version', 
                       action='version',
                       version='TJL Project Setup Tool v1.0.0')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    try:
        # Parse environments
        environments = [env.strip() for env in args.environments.split(',')]
        
        # Create project
        setup = ProjectSetup(
            project_name=args.project_name,
            base_path=args.path,
            environments=environments,
            template=args.template
        )
        
        # Run setup
        setup.setup_project()
        
    except (ValidationError, GitError, ProjectError) as e:
        ColorOutput.print_error(f"Setup failed: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        ColorOutput.print_warning("\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        ColorOutput.print_error(f"Unexpected error: {str(e)}")
        logger.error("Unexpected error during setup", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()