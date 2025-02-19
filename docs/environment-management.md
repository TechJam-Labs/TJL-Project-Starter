# TJL Project Setup Tool - Environment Management Guide

## Table of Contents
- [Overview](#overview)
- [Environment Structure](#environment-structure)
- [Environment Configuration](#environment-configuration)
- [Environment Switching](#environment-switching)
- [Environment Variables](#environment-variables)
- [Secrets Management](#secrets-management)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

### Purpose
Environment management in TJL Project Setup Tool provides:
- Isolated configurations for different stages
- Secure credentials management
- Easy environment switching
- Consistent deployment processes

### Default Environments
- `local`: Local development
- `dev`: Development/Integration
- `staging`: Pre-production testing
- `prod`: Production deployment

## Environment Structure

### Directory Layout
```
project/
├── config/
│   ├── local/
│   │   ├── env.conf
│   │   └── settings.json
│   ├── dev/
│   │   ├── env.conf
│   │   └── settings.json
│   ├── staging/
│   │   ├── env.conf
│   │   └── settings.json
│   └── prod/
│       ├── env.conf
│       └── settings.json
└── scripts/
    └── switch_env.sh
```

### File Purposes
- `env.conf`: Environment variables and configurations
- `settings.json`: Application-specific settings
- `switch_env.sh`: Environment switching script

## Environment Configuration

### Basic Configuration
```bash
# config/local/env.conf
export APP_ENV=local
export DEBUG=true
export LOG_LEVEL=DEBUG
export API_URL=http://localhost:8000

# config/prod/env.conf
export APP_ENV=production
export DEBUG=false
export LOG_LEVEL=INFO
export API_URL=https://api.example.com
```

### Settings Configuration
```json
// config/local/settings.json
{
  "app": {
    "name": "MyApp",
    "version": "1.0.0"
  },
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "myapp_db"
  },
  "cache": {
    "enabled": true,
    "provider": "redis"
  }
}
```

### Custom Environments

Create new environments:
```bash
# Create QA environment
mkdir -p config/qa
cp config/staging/env.conf config/qa/
cp config/staging/settings.json config/qa/
```

Update environment list:
```bash
tjl-project my-project --environments local,dev,qa,staging,prod
```

## Environment Switching

### Basic Switching
```bash
# Switch to development
./scripts/switch_env.sh dev

# Switch to production
./scripts/switch_env.sh prod
```

### Advanced Options
```bash
# Force switch (ignore uncommitted changes)
./scripts/switch_env.sh staging --force

# Backup current environment
./scripts/switch_env.sh prod --backup

# Switch with both options
./scripts/switch_env.sh prod --force --backup
```

### Automatic Actions
Environment switching:
1. Backs up current configuration (if requested)
2. Loads new environment variables
3. Switches Git branch (if applicable)
4. Updates application settings
5. Runs environment-specific scripts

## Environment Variables

### Variable Types
1. **Configuration Variables**
   ```bash
   export APP_ENV=development
   export DEBUG=true
   ```

2. **Connection Strings**
   ```bash
   export DATABASE_URL="postgresql://user:pass@host:5432/db"
   export REDIS_URL="redis://localhost:6379/0"
   ```

3. **API Keys and Secrets**
   ```bash
   export API_KEY="your-api-key"
   export JWT_SECRET="your-jwt-secret"
   ```

### Variable Management
```bash
# Load environment variables
source config/current/env.conf

# Check current environment
echo $APP_ENV

# List all environment variables
printenv | grep APP_
```

## Secrets Management

### Local Development
Use `.env.local` for sensitive data:
```bash
# .env.local (not committed to git)
export DB_PASSWORD="secret"
export API_KEY="development-key"
```

### Production Secrets
Use secure secret management:
```bash
# Load from secure storage
export DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id db-password)
export API_KEY=$(vault kv get -field=api-key secrets/myapp)
```

## Best Practices

### 1. Configuration Management
- Keep configurations minimal
- Use meaningful names
- Document all options
- Version control templates

### 2. Environment Separation
- Clear distinction between environments
- No shared resources between environments
- Environment-specific logging levels
- Appropriate debug settings

### 3. Security
- Never commit secrets
- Use secure secret management
- Rotate credentials regularly
- Audit access regularly

### 4. Deployment
- Validate configurations before deployment
- Use deployment checksums
- Maintain configuration history
- Document changes

## Troubleshooting

### Common Issues

1. **Environment Not Found**
   ```bash
   # Check environment exists
   ls config/missing_env
   
   # Create if needed
   cp -r config/staging config/new_env
   ```

2. **Configuration Errors**
   ```bash
   # Validate configuration
   ./scripts/validate_config.sh dev
   
   # Check syntax
   bash -n config/dev/env.conf
   ```

3. **Switching Failures**
   ```bash
   # Clear environment cache
   rm .current_env
   
   # Force reload
   source config/dev/env.conf
   ```

### Debug Tools
```bash
# Enable debug mode
export TJL_DEBUG=true
./scripts/switch_env.sh dev

# Check configuration
./scripts/check_config.sh

# Validate all environments
./scripts/validate_all.sh
```

## Support

Need assistance?
- Email: ben@techjamlabs.com
- Phone: +2348099999928
- Issues: [GitHub Issues](https://github.com/techjamlabs/tjl-project-setup/issues)

## Additional Resources
- [Installation Guide](installation.md)
- [Quick Start Guide](quickstart.md)
- [Repository Strategy](repository-strategy.md)