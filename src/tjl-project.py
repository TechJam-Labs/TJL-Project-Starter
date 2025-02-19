#!/usr/bin/env python3
"""
TJL Project Setup Tool
=====================

A comprehensive project initialization and management system designed to establish
standardized development practices across teams and projects.

Author: Ben Adenle (TechJam Labs)
Email: ben@techjamlabs.com
Phone: +2348099999928
Version: 1.0.0
License: MIT
Repository: https://github.com/techjamlabs/tjl-project-setup

Usage:
------
    tjl-project my-project
    tjl-project my-project --path /custom/path
    tjl-project my-project --environments local,dev,qa,staging,prod
    tjl-project my-project --template microservice

Templates:
---------
    basic        - Basic project structure
    microservice - Microservice architecture
    webapp       - Web application
    library     - Reusable library

Examples:
--------
    # Create a new project in current directory
    tjl-project my-project

    # Create a project with custom path
    tjl-project my-project --path /home/user/projects

    # Create a microservice project
    tjl-project my-service --template microservice

    # Create a project with custom environments
    tjl-project my-project --environments dev,staging,prod
"""

import os
import sys
import argparse
import subprocess
import json
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

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

class ProjectTemplate:
    """Base class for project templates."""
    
    def __init__(self, project_path: str, environments: List[str]):
        self.project_path = project_path
        self.environments = environments

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
            'src/modules',
            'src/utils',
            'tests',
            'tests/unit',
            'tests/integration',
            'tests/e2e',
            'tools',
            'tools/linters',
            'tools/generators',
            '.github/workflows'
        ]

    def get_files(self) -> Dict[str, str]:
        """Get dictionary of files to create with their content."""
        return {
            'README.md': self._get_readme_content(),
            '.gitignore': self._get_gitignore_content(),
            '.editorconfig': self._get_editorconfig_content(),
            'scripts/switch_env.sh': self._get_switch_env_content(),
            '.github/workflows/ci.yml': self._get_workflow_content()
        }

    def _get_readme_content(self) -> str:
        """Generate README.md content."""
        return f"""# {os.path.basename(self.project_path)}

Project created with TJL Project Setup Tool.

## Structure

```
{os.path.basename(self.project_path)}/
├── config/
│   ├── local/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── docs/
├── scripts/
├── src/
├── tests/
└── tools/
```

## Setup

1. Install dependencies
2. Configure environment
3. Run setup script

## Development

1. Switch to development environment:
   ```bash
   ./scripts/switch_env.sh dev
   ```

2. Start development

## Testing

```bash
# Run unit tests
python -m pytest tests/unit

# Run integration tests
python -m pytest tests/integration

# Run all tests
python -m pytest
```

## Documentation

See [docs/](docs/) for detailed documentation.

## License

MIT License
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
env/
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
*.egg-info/
.installed.cfg
*.egg

# IDEs
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log
"""

    def _get_editorconfig_content(self) -> str:
        """Generate .editorconfig content."""
        return """root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true

[*.{py,ini,yml,yaml,json}]
indent_style = space
indent_size = 4

[*.md]
trim_trailing_whitespace = false
"""

    def _get_switch_env_content(self) -> str:
        """Generate environment switching script content."""
        envs = " ".join(self.environments)
        return f"""#!/usr/bin/env bash

ENVIRONMENTS=({envs})
CURRENT_ENV="local"

function show_usage() {{
    echo "Usage: ./switch_env.sh <environment>"
    echo "Available environments: ${{ENVIRONMENTS[*]}}"
    exit 1
}}

if [ $# -ne 1 ]; then
    show_usage
fi

NEW_ENV=$1

if [[ ! " ${{ENVIRONMENTS[*]}} " =~ " ${{NEW_ENV}} " ]]; then
    echo "Invalid environment: ${{NEW_ENV}}"
    show_usage
fi

# Load environment-specific configuration
if [ -f "config/${{NEW_ENV}}/env.conf" ]; then
    source "config/${{NEW_ENV}}/env.conf"
    echo "Switched to ${{NEW_ENV}} environment"
else
    echo "Warning: No configuration found for ${{NEW_ENV}} environment"
fi

# Switch git branch if applicable (except for local)
if [ "${{NEW_ENV}}" != "local" ]; then
    git checkout "${{NEW_ENV}}" 2>/dev/null || git checkout -b "${{NEW_ENV}}"
fi

export CURRENT_ENV="${{NEW_ENV}}"
"""

    def _get_workflow_content(self) -> str:
        """Generate GitHub Actions workflow content."""
        return """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
          
      - name: Run tests
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          python -m pytest tests/
          
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy
        run: |
          echo "Add deployment steps here"
"""

class ProjectSetup:
    """Main class for project setup."""

    def __init__(self, project_name: str, base_path: Optional[str] = None,
                 environments: Optional[List[str]] = None,
                 template: str = "basic"):
        """Initialize project setup with given parameters."""
        self.project_name = project_name
        self.base_path = base_path or os.getcwd()
        self.project_path = os.path.join(self.base_path, project_name)
        self.environments = environments or ['local', 'dev', 'staging', 'prod']
        self.template = template
        self.template_instance = ProjectTemplate(self.project_path, self.environments)
        
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        """Validate input parameters."""
        if not self.project_name.replace('-', '').replace('_', '').isalnum():
            raise ValueError("Project name should be alphanumeric (hyphens and underscores allowed)")

        if not os.path.exists(self.base_path):
            raise ValueError(f"Base path does not exist: {self.base_path}")

        if os.path.exists(self.project_path):
            raise ValueError(f"Project directory already exists: {self.project_path}")

        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            raise EnvironmentError("Git is not installed or not accessible")

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
            
            with open(full_path, 'w') as f:
                f.write(content)
            
            if file_path.endswith('.sh'):
                os.chmod(full_path, 0o755)
            
            ColorOutput.print_success(f"Created: {file_path}")

    def setup_git(self) -> None:
        """Initialize git repository and create initial branches."""
        ColorOutput.print_header("Setting up Git Repository")

        commands = [
            'git init',
            'git add .',
            f'git commit -m "Initial project setup with TJL Project Setup Tool\n\nCreated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"'
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, cwd=self.project_path, shell=True, check=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ColorOutput.print_success(f"Executed: {cmd}")
            except subprocess.CalledProcessError as e:
                ColorOutput.print_error(f"Failed to execute: {cmd}")
                ColorOutput.print_error(f"Error: {e.stderr.decode()}")
                return

        # Create branches for each environment (except local)
        for env in [e for e in self.environments if e != 'local']:
            try:
                subprocess.run(f'git checkout -b {env}',
                             cwd=self.project_path, shell=True, check=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ColorOutput.print_success(f"Created branch: {env}")
            except subprocess.CalledProcessError as e:
                ColorOutput.print_error(f"Failed to create branch: {env}")
                ColorOutput.print_error(f"Error: {e.stderr.decode()}")

        # Return to main branch
        try:
            subprocess.run('git checkout main',
                         cwd=self.project_path, shell=True, check=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            ColorOutput.print_error("Failed to return to main branch")
            ColorOutput.print_error(f"Error: {e.stderr.decode()}")

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
            sys.exit(1)

    def _print_next_steps(self) -> None:
        """Print next steps for the user."""
        steps = [
            ("Next Steps", [
                "1. Review and customize the environment configurations in config/",
                "2. Set up your remote Git repository",
                "3. Push your code: git push -u origin main",
                "4. Use ./scripts/switch_env.sh to switch between environments",
                f"5. Create environment-specific configs in config/<env>/"
            ])
        ]

        for title, items in steps:
            ColorOutput.print_header(title)
            for item in items:
                ColorOutput.print_step(item)
            print()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="TJL Project Setup Tool - Create a standardized project structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--path", help="Base path for project creation", default=None)
    parser.add_argument("--environments", help="Comma-separated list of environments",
                      default="local,dev,staging,prod")
    parser.add_argument("--template", help="Project template to use",
                      choices=['basic', 'microservice', 'webapp', 'library'],
                      default="basic")
    parser.add_argument('--version', action='version',
                      version='TJL Project Setup Tool v1.0.0')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    environments = [env.strip() for env in args.environments.split(',')]

    try:
        setup = ProjectSetup(args.project_name, args.path, environments, args.template)
        setup.setup_project()
    except Exception as e:
        ColorOutput.print_error(f"Setup failed: {str(e)}")
        sys.exit(1)

class MicroserviceTemplate(ProjectTemplate):
    """Template for microservice projects."""
    
    def get_directories(self) -> List[str]:
        """Get microservice-specific directories."""
        dirs = super().get_directories()
        return dirs + [
            'src/api',
            'src/services',
            'src/models',
            'src/middleware',
            'deployment',
            'deployment/kubernetes',
            'deployment/docker'
        ]

    def get_files(self) -> Dict[str, str]:
        """Get microservice-specific files."""
        files = super().get_files()
        files.update({
            'Dockerfile': self._get_dockerfile_content(),
            'docker-compose.yml': self._get_docker_compose_content(),
            'deployment/kubernetes/deployment.yml': self._get_k8s_deployment_content(),
            'deployment/kubernetes/service.yml': self._get_k8s_service_content()
        })
        return files

    def _get_dockerfile_content(self) -> str:
        """Generate Dockerfile content."""
        return """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "src/main.py"]
"""

    def _get_docker_compose_content(self) -> str:
        """Generate docker-compose.yml content."""
        return """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
    volumes:
      - .:/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
"""

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
        - name: ENVIRONMENT
          value: production
"""

    def _get_k8s_service_content(self) -> str:
        """Generate Kubernetes service content."""
        return """apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: microservice
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
"""

class WebAppTemplate(ProjectTemplate):
    """Template for web application projects."""
    
    def get_directories(self) -> List[str]:
        """Get webapp-specific directories."""
        dirs = super().get_directories()
        return dirs + [
            'src/templates',
            'src/static',
            'src/static/css',
            'src/static/js',
            'src/static/images',
            'src/components',
            'src/pages',
            'src/layouts'
        ]

    def get_files(self) -> Dict[str, str]:
        """Get webapp-specific files."""
        files = super().get_files()
        files.update({
            'src/static/css/style.css': self._get_css_content(),
            'src/static/js/main.js': self._get_js_content(),
            'src/templates/base.html': self._get_base_template_content()
        })
        return files

    def _get_css_content(self) -> str:
        """Generate CSS content."""
        return """/* Main stylesheet */
:root {
    --primary-color: #0366d6;
    --secondary-color: #24292e;
    --background-color: #ffffff;
    --text-color: #24292e;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
        Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--background-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

/* Add your custom styles here */
"""

    def _get_js_content(self) -> str:
        """Generate JavaScript content."""
        return """// Main JavaScript file
document.addEventListener('DOMContentLoaded', function() {
    // Initialize your application
    console.log('Application initialized');
});

// Add your custom JavaScript here
"""

    def _get_base_template_content(self) -> str:
        """Generate base HTML template content."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <nav>
            <!-- Add your navigation here -->
        </nav>
    </header>

    <main class="container">
        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <!-- Add your footer content here -->
    </footer>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
"""

class LibraryTemplate(ProjectTemplate):
    """Template for library projects."""
    
    def get_directories(self) -> List[str]:
        """Get library-specific directories."""
        dirs = super().get_directories()
        return dirs + [
            'src/exceptions',
            'src/interfaces',
            'examples',
            'benchmarks'
        ]

    def get_files(self) -> Dict[str, str]:
        """Get library-specific files."""
        files = super().get_files()
        files.update({
            'setup.py': self._get_setup_content(),
            'examples/README.md': self._get_examples_readme_content(),
            'CONTRIBUTING.md': self._get_contributing_content()
        })
        return files

    def _get_setup_content(self) -> str:
        """Generate setup.py content."""
        return f"""from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{self.project_path.split('/')[-1]}",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yourproject",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
"""

    def _get_examples_readme_content(self) -> str:
        """Generate examples README content."""
        return """# Examples

This directory contains examples demonstrating how to use the library.

## Basic Usage

```python
from your_library import YourClass

# Add example code here
```

## Advanced Examples

See individual example files for more complex usage scenarios.
"""

    def _get_contributing_content(self) -> str:
        """Generate CONTRIBUTING.md content."""
        return """# Contributing Guidelines

Thank you for considering contributing to this project!

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to all functions and classes
- Write unit tests for new features

## Pull Request Process

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Running Tests

```bash
python -m pytest
```

## Documentation

Please update documentation for any changes.
"""

if __name__ == "__main__":
    main()