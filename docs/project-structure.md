# TJL Project Setup Tool - Project Structure Guide

## Table of Contents
- [Overview](#overview)
- [Base Structure](#base-structure)
- [Template Structures](#template-structures)
  - [Basic Template](#basic-template)
  - [Microservice Template](#microservice-template)
  - [Web Application Template](#web-application-template)
  - [Library Template](#library-template)
- [Configuration Management](#configuration-management)
- [Directory Purposes](#directory-purposes)
- [Best Practices](#best-practices)

## Overview

The TJL Project Setup Tool uses a standardized project structure that promotes:
- Clear organization
- Separation of concerns
- Consistent configuration
- Easy maintenance
- Scalable architecture

## Base Structure

Every project includes these core directories:

```
project-name/
├── .github/
│   └── workflows/          # CI/CD configurations
├── config/                 # Environment configurations
│   ├── local/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── docs/                   # Documentation
│   ├── api/
│   └── setup/
├── scripts/               # Utility scripts
│   ├── switch_env.sh
│   ├── deploy.sh
│   └── run_tests.sh
├── src/                   # Source code
├── tests/                 # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .gitignore            # Git ignore rules
├── .editorconfig         # Editor configuration
└── README.md             # Project documentation
```

## Template Structures

### Basic Template
Minimal structure for general projects:

```
basic-project/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logger.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── unit/
│   │   └── test_core.py
│   └── integration/
│       └── test_integration.py
└── [base structure folders]
```

### Microservice Template
Complete microservice architecture:

```
microservice-project/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   └── v1/
│   │   ├── middleware/
│   │   │   ├── auth.py
│   │   │   └── logging.py
│   │   └── schemas/
│   │       └── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── base_service.py
│   └── models/
│       ├── __init__.py
│       └── base_model.py
├── deployment/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   └── kubernetes/
│       ├── deployment.yaml
│       └── service.yaml
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── [base structure folders]
```

### Web Application Template
Modern web application structure:

```
webapp-project/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   └── Input.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       └── Footer.tsx
│   ├── pages/
│   │   ├── _app.tsx
│   │   └── index.tsx
│   ├── styles/
│   │   ├── globals.css
│   │   └── components.css
│   ├── utils/
│   │   └── helpers.ts
│   └── hooks/
│       └── useAuth.ts
├── public/
│   ├── images/
│   └── fonts/
├── tests/
│   ├── unit/
│   └── e2e/
└── [base structure folders]
```

### Library Template
Professional library structure:

```
library-project/
├── src/
│   ├── yourlib/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── base.py
│   │   │   └── exceptions.py
│   │   └── utils/
│   │       └── helpers.py
├── examples/
│   ├── basic_usage.py
│   └── advanced_usage.py
├── docs/
│   ├── api/
│   │   └── reference.rst
│   └── guides/
│       └── getting_started.rst
├── tests/
│   ├── unit/
│   └── integration/
├── benchmarks/
│   └── performance_tests.py
└── [base structure folders]
```

## Configuration Management

### Environment Configuration Structure
```
config/
├── local/
│   ├── env.conf          # Environment variables
│   └── settings.json     # Application settings
├── dev/
│   ├── env.conf
│   └── settings.json
├── staging/
│   ├── env.conf
│   └── settings.json
└── prod/
    ├── env.conf
    └── settings.json
```

### Environment Variables
```bash
# env.conf example
export APP_ENV=development
export DEBUG=true
export LOG_LEVEL=DEBUG
export API_URL=http://localhost:8000
```

### Application Settings
```json
// settings.json example
{
  "app": {
    "name": "MyProject",
    "version": "1.0.0"
  },
  "database": {
    "host": "localhost",
    "port": 5432
  },
  "features": {
    "cache": true,
    "metrics": false
  }
}
```

## Directory Purposes

### Core Directories

| Directory | Purpose | Contents |
|-----------|---------|-----------|
| `src/` | Source code | Application code and logic |
| `tests/` | Test files | Unit, integration, and E2E tests |
| `config/` | Configuration | Environment-specific settings |
| `docs/` | Documentation | Project and API documentation |
| `scripts/` | Utility scripts | Automation and management scripts |

### Template-Specific Directories

| Template | Directory | Purpose |
|----------|-----------|----------|
| Microservice | `deployment/` | Container and orchestration configs |
| Web App | `public/` | Static assets and resources |
| Library | `examples/` | Usage examples and demos |
| Library | `benchmarks/` | Performance testing |

### Special Directories

| Directory | Purpose |
|-----------|----------|
| `.github/workflows/` | CI/CD pipeline definitions |
| `scripts/` | Automation scripts |
| `docs/api/` | API documentation |
| `docs/setup/` | Setup and installation guides |

## Best Practices

### 1. Directory Organization
- Keep related files together
- Use clear, descriptive names
- Maintain consistent structure
- Follow language conventions

### 2. File Naming
- Use lowercase names
- Separate words with hyphens or underscores
- Be consistent with extensions
- Follow template conventions

### 3. Configuration Management
- Separate environment configs
- Use appropriate file formats
- Document all settings
- Maintain security

### 4. Documentation
- Keep docs close to code
- Update regularly
- Include examples
- Use markdown format

### 5. Testing Structure
- Separate test types
- Mirror source structure
- Include test data
- Maintain test utilities

## Support

Need assistance?
- Email: ben@techjamlabs.com
- Phone: +2348099999928
- Issues: [GitHub Issues](https://github.com/techjamlabs/tjl-project-setup/issues)

## Additional Resources
- [Installation Guide](installation.md)
- [Quick Start Guide](quickstart.md)
- [Environment Management](environment-management.md)
- [Repository Strategy](repository-strategy.md)