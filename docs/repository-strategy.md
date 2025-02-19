# TJL Project Setup Tool - Repository Strategy Guide

## Table of Contents
- [Overview](#overview)
- [Branch Strategy](#branch-strategy)
- [Git Flow](#git-flow)
- [Commit Conventions](#commit-conventions)
- [Tagging Strategy](#tagging-strategy)
- [Branch Protection](#branch-protection)
- [Code Review Process](#code-review-process)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)

## Overview

### Purpose
The TJL repository strategy provides:
- Consistent version control workflow
- Clear development process
- Release management
- Quality assurance
- Team collaboration

### Key Principles
1. Clean, linear history
2. Protected main branches
3. Semantic versioning
4. Clear commit messages
5. Code review requirements

## Branch Strategy

### Core Branches

#### Main Branch (`main`)
- Production-ready code
- Always deployable
- Protected from direct pushes
- Requires pull request and review
```bash
# Create from develop when ready
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0
# After testing
git checkout main
git merge --no-ff release/v1.2.0
```

#### Development Branch (`develop`)
- Integration branch
- Latest delivered changes
- Source for feature branches
```bash
# Create feature from develop
git checkout develop
git pull origin develop
git checkout -b feature/user-auth
```

#### Staging Branch (`staging`)
- Pre-production testing
- Release candidates
- UAT environment
```bash
# Deploy to staging
git checkout staging
git merge --no-ff develop
git push origin staging
```

### Supporting Branches

#### Feature Branches
Format: `feature/<feature-name>`
```bash
# Create feature branch
git checkout -b feature/user-authentication develop

# Update feature branch
git checkout feature/user-authentication
git pull origin develop

# Complete feature
git checkout develop
git merge --no-ff feature/user-authentication
```

#### Release Branches
Format: `release/v<major>.<minor>.<patch>`
```bash
# Create release branch
git checkout -b release/v1.2.0 develop

# Finish release
git checkout main
git merge --no-ff release/v1.2.0
git checkout develop
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
```

#### Hotfix Branches
Format: `hotfix/<issue-identifier>`
```bash
# Create hotfix
git checkout -b hotfix/security-patch-123 main

# Apply hotfix
git checkout main
git merge --no-ff hotfix/security-patch-123
git checkout develop
git merge --no-ff hotfix/security-patch-123
git tag -a v1.2.1 -m "Security patch"
```

## Git Flow

### Feature Development
1. Create feature branch
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/new-feature
   ```

2. Develop and test
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. Update from develop
   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/new-feature
   git rebase develop
   ```

4. Complete feature
   ```bash
   git checkout develop
   git merge --no-ff feature/new-feature
   git push origin develop
   ```

### Release Process
1. Create release branch
   ```bash
   git checkout -b release/v1.2.0 develop
   ```

2. Prepare release
   ```bash
   # Update version
   ./scripts/update_version.sh 1.2.0
   git commit -m "chore: bump version to 1.2.0"
   ```

3. Test and fix
   ```bash
   # Fix release issues
   git commit -m "fix: release issue"
   ```

4. Complete release
   ```bash
   git checkout main
   git merge --no-ff release/v1.2.0
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git checkout develop
   git merge --no-ff release/v1.2.0
   ```

## Commit Conventions

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Examples
```bash
# Feature
git commit -m "feat(auth): implement JWT authentication

Implement JSON Web Token authentication system.
- Add token generation
- Add token validation
- Add refresh token support

BREAKING CHANGE: Auth header format changed"

# Bug fix
git commit -m "fix(api): correct user validation error

Fix issue #123 where user validation failed for valid emails"

# Documentation
git commit -m "docs: update API documentation

Update API docs with new endpoints and examples"
```

## Tagging Strategy

### Semantic Versioning
Format: `v<major>.<minor>.<patch>`
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

### Tag Types

#### Annotated Tags (Releases)
```bash
# Create release tag
git tag -a v1.2.0 -m "Release version 1.2.0"

# Push tags
git push origin --tags
```

#### Lightweight Tags (Internal)
```bash
# Create build tag
git tag build-2023-02-19

# Create feature tag
git tag feat-user-auth
```

### Version Examples
```bash
# Major version
v2.0.0  # Breaking changes

# Minor version
v1.3.0  # New features

# Patch version
v1.2.1  # Bug fixes

# Pre-release
v1.2.0-alpha.1
v1.2.0-beta.2
v1.2.0-rc.1
```

## Branch Protection

### Main Branch
```yaml
# .github/branch-protection.yml
main:
  required_status_checks:
    strict: true
    contexts:
      - continuous-integration/github-actions
  required_pull_request_reviews:
    required_approving_review_count: 2
  restrictions:
    users: []
    teams: ["maintainers"]
  enforce_admins: true
```

### Develop Branch
```yaml
develop:
  required_status_checks:
    strict: true
  required_pull_request_reviews:
    required_approving_review_count: 1
  restrictions:
    users: []
    teams: ["developers"]
```

## Code Review Process

### Pull Request Template
```markdown
## Description
[Description of changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Branch up-to-date
```

### Review Guidelines
1. Code quality
2. Test coverage
3. Documentation
4. Performance impact
5. Security implications

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

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
      - name: Run tests
        run: ./scripts/run_tests.sh

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy
        run: ./scripts/deploy.sh
```

## Best Practices

### 1. Branch Management
- Keep branches short-lived
- Regular rebasing
- Clean branch history
- Meaningful branch names

### 2. Commit Practices
- Atomic commits
- Clear messages
- Link to issues
- Regular commits

### 3. Code Review
- Early feedback
- Constructive comments
- Focus on quality
- Knowledge sharing

### 4. Documentation
- Update with changes
- Clear explanations
- Code examples
- Version history

## Support

Need assistance?
- Email: ben@techjamlabs.com
- Phone: +2348099999928
- Issues: [GitHub Issues](https://github.com/techjamlabs/tjl-project-setup/issues)

## Additional Resources
- [Installation Guide](installation.md)
- [Quick Start Guide](quickstart.md)
- [Environment Management](environment-management.md)