#!/bin/bash
# Django development server startup script
# This script ensures the virtual environment is activated before running Django commands

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/skillswap_env"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please create it first with: python -m venv skillswap_env"
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Run Django development server
echo "Starting Django development server with virtual environment..."
python manage.py runserver "$@"
