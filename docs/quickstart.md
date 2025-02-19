# TJL Project Setup Tool - Quick Start Guide

## Table of Contents
- [Creating Your First Project](#creating-your-first-project)
- [Project Templates](#project-templates)
- [Basic Usage](#basic-usage)
- [Directory Structure](#directory-structure)
- [Next Steps](#next-steps)

## Creating Your First Project

Get started with TJL Project Setup Tool in minutes:

```bash
# Create a basic project
tjl-project my-project

# Create with specific template
tjl-project my-service --template microservice

# Create with custom path
tjl-project my-webapp --template webapp --path /path/to/projects

# Create with custom environments
tjl-project my-app --environments local,dev,qa,staging,prod
```

## Project Templates

Choose the right template for your needs:

### Basic Template
Minimal project structure for general use:
```bash
tjl-project my-project --template basic
```
Best for:
- Simple applications
- Learning projects
- Quick prototypes

### Microservice Template
Complete microservice architecture:
```bash
tjl-project my-service --template microservice
```
Includes:
- API structure
- Docker configuration
- Kubernetes setup
- Service architecture

### Web Application Template
Modern web application setup:
```bash
tjl-project my-webapp --template webapp
```
Features:
- Component structure
- Frontend framework setup
- Asset management
- Build configuration

### Library Template
Professional library structure:
```bash
tjl-project my-lib --template library
```
Provides:
- Package setup
- Documentation framework
- Testing infrastructure
- Distribution tooling

## Basic Usage

### Create Project
```bash
# Basic creation
tjl-project my-project

# With options
tjl-project my-project \
    --template microservice \
    --path /custom/path \
    --environments local,dev,staging,prod
```

### Switch Environments
```bash
# Switch to development environment
./scripts/switch_env.sh dev

# Switch with force
./scripts/switch_env.sh staging --force

# Switch with backup
./scripts/switch_env.sh prod --backup
```

### Run Tests
```bash
# Run all tests
./scripts/run_tests.sh

# Run specific tests
./scripts/run_tests.sh --unit
./scripts/run_tests.sh --integration
```

### Deploy
```bash
# Deploy to environment
./scripts/deploy.sh staging

# Force deployment
./scripts/deploy.sh prod --force
```

## Directory Structure

Your project will have this structure:
```
my-project/
├── .github/
│   └── workflows/        # CI/CD configurations
├── config/
│   ├── local/           # Local environment config
│   ├── dev/             # Development config
│   ├── staging/         # Staging config
│   └── prod/            # Production config
├── scripts/
│   ├── switch_env.sh    # Environment switching
│   ├── deploy.sh        # Deployment script
│   └── run_tests.sh     # Test runner
├── src/                 # Source code
├── tests/               # Test files
├── docs/                # Documentation
└── README.md           # Project documentation
```

### Key Files
- `config/*/env.conf`: Environment-specific settings
- `scripts/switch_env.sh`: Environment management
- `.github/workflows/`: CI/CD pipeline
- `README.md`: Project documentation

## Next Steps

1. **Configure Environments**
   - Review configurations in `config/`
   - Set up environment variables
   - Test environment switching

2. **Set Up Version Control**
   - Initialize repository
   - Configure remote
   - Set up branches
   ```bash
   git remote add origin <repository-url>
   git push -u origin main
   ```

3. **Configure CI/CD**
   - Review workflow files
   - Set up secrets
   - Configure deployments

4. **Start Development**
   - Switch to development environment
   - Create feature branch
   - Begin implementing features

## Additional Resources

- [Installation Guide](installation.md) - Detailed installation instructions
- [Environment Management](environment-management.md) - Managing project environments
- [Repository Strategy](repository-strategy.md) - Version control best practices

## Support

Need help?
- Email: ben@techjamlabs.com
- Phone: +2348099999928
- Issues: [GitHub Issues](https://github.com/techjamlabs/tjl-project-setup/issues)