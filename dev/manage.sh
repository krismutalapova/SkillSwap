#!/bin/bash
# Django management command wrapper
# This script ensures the virtual environment is activated before running Django management commands

# Get the project root directory (parent of dev/)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_DIR/skillswap_env"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please create it first with: python -m venv skillswap_env"
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Change to project root directory
cd "$PROJECT_DIR"

# Run Django management command
python manage.py "$@"
