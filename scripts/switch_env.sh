#!/usr/bin/env bash

# TJL Project Environment Switcher
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

# Current environment file
ENV_FILE=".current_env"
BACKUP_SUFFIX=".backup"

# Function to show usage
show_usage() {
    echo "TJL Project Environment Switcher"
    echo
    echo "Usage:"
    echo "  $0 <environment> [--force] [--backup]"
    echo
    echo "Options:"
    echo "  --force   Force switch even if there are uncommitted changes"
    echo "  --backup  Create backup of current environment"
    echo
    echo "Available environments:"
    ls -1 config/ | grep -v '\.backup$'
    exit 1
}

# Function to backup environment
backup_environment() {
    local env=$1
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_dir="config/${env}${BACKUP_SUFFIX}_${timestamp}"
    
    print_blue "Creating backup of $env environment..."
    cp -r "config/$env" "$backup_dir"
    print_green "✓ Backup created at $backup_dir"
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

# Function to check git status
check_git_status() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        if [[ $(git status --porcelain) ]]; then
            if [[ "$FORCE" != "true" ]]; then
                print_red "Error: You have uncommitted changes"
                echo "Commit your changes or use --force to switch anyway"
                exit 1
            else
                print_yellow "! Warning: Switching with uncommitted changes"
            fi
        fi
    fi
}

# Function to switch git branch
switch_git_branch() {
    local env=$1
    if git rev-parse --git-dir > /dev/null 2>&1; then
        if [[ "$env" != "local" ]]; then
            if git show-ref --verify --quiet "refs/heads/$env"; then
                git checkout "$env"
            else
                print_yellow "! Creating new branch: $env"
                git checkout -b "$env"
            fi
        fi
    fi
}

# Function to load environment
load_environment() {
    local env=$1
    
    # Load environment variables
    if [[ -f "config/$env/env.conf" ]]; then
        source "config/$env/env.conf"
        print_green "✓ Loaded environment variables from config/$env/env.conf"
    fi
    
    # Load environment-specific settings
    if [[ -f "config/$env/settings.json" ]]; then
        # Here you could add logic to apply settings
        print_green "✓ Loaded settings from config/$env/settings.json"
    fi
    
    # Save current environment
    echo "$env" > "$ENV_FILE"
}

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

# Check git status
check_git_status

# Create backup if requested
if [[ "$BACKUP" == "true" ]]; then
    if [[ -f "$ENV_FILE" ]]; then
        backup_environment "$(cat $ENV_FILE)"
    fi
fi

# Switch git branch
switch_git_branch "$ENVIRONMENT"

# Load environment
load_environment "$ENVIRONMENT"

print_green "Successfully switched to $ENVIRONMENT environment"
print_blue "Run 'source config/$ENVIRONMENT/env.conf' to load environment variables in your current shell"