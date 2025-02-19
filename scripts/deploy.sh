#!/usr/bin/env bash

# TJL Project Deployment Script
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

# Function to show usage
show_usage() {
    echo "TJL Project Deployment Script"
    echo
    echo "Usage:"
    echo "  $0 <environment> [--skip-tests] [--force]"
    echo
    echo "Options:"
    echo "  --skip-tests  Skip running tests before deployment"
    echo "  --force       Force deployment even if tests fail"
    echo
    echo "Available environments:"
    ls -1 config/ | grep -v '\.backup$'
    exit 1
}

# Function to run tests
run_tests() {
    print_blue "Running tests..."
    
    # Add your test commands here
    # Example:
    # python -m pytest tests/
    
    if [[ $? -ne 0 ]]; then
        if [[ "$FORCE" != "true" ]]; then
            print_red "Tests failed. Deployment aborted."
            exit 1
        else
            print_yellow "! Tests failed but continuing due to --force"
        fi
    else
        print_green "✓ Tests passed"
    fi
}

# Function to validate environment
validate_environment() {
    local env=$1
    if [[ ! -d "config/$env" ]]; then
        print_red "Error: Environment '$env' does not exist"
        echo "Available environments:"
        ls -1 config/ | grep -v '\.backup$'
        exit 1
    fi
}

# Function to load environment config
load_environment() {
    local env=$1
    if [[ -f "config/$env/env.conf" ]]; then
        source "config/$env/env.conf"
        print_green "✓ Loaded environment configuration"
    else
        print_yellow "! No environment configuration found"
    fi
}

# Function to check dependencies
check_dependencies() {
    print_blue "Checking dependencies..."
    
    # Add dependency checks here
    # Example:
    # command -v docker >/dev/null 2>&1 || { print_red "Docker is required but not installed."; exit 1; }
    
    print_green "✓ All dependencies satisfied"
}

# Function to build application
build_application() {
    print_blue "Building application..."
    
    # Add build commands here
    # Example:
    # docker build -t myapp .
    
    print_green "✓ Build completed"
}

# Function to deploy application
deploy_application() {
    local env=$1
    print_blue "Deploying to $env environment..."
    
    case $env in
        "dev")
            # Development deployment
            ;;
        "staging")
            # Staging deployment
            ;;
        "prod")
            # Production deployment
            print_yellow "! Production deployment requires additional confirmation"
            read -p "Are you sure you want to deploy to production? (y/N) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_red "Deployment cancelled"
                exit 1
            fi
            ;;
        *)
            print_red "Unsupported environment for deployment"
            exit 1
            ;;
    esac
    
    # Add deployment commands here
    # Example:
    # kubectl apply -f deployment/$env/
    
    print_green "✓ Deployment completed"
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

# Validate environment
validate_environment "$ENVIRONMENT"

# Load environment configuration
load_environment "$ENVIRONMENT"

# Check dependencies
check_dependencies

# Run tests unless skipped
if [[ "$SKIP_TESTS" != "true" ]]; then
    run_tests
fi

# Build application
build_application

# Deploy application
deploy_application "$ENVIRONMENT"

print_green "✓ Deployment to $ENVIRONMENT completed successfully"
echo
print_blue "Post-deployment steps:"
echo "1. Verify application health"
echo "2. Check logs for any errors"
echo "3. Run smoke tests"
echo "4. Update documentation if needed"