#!/bin/bash

echo "====================================="
echo "SkillSwap Docker Demo - Quick Start"
echo "====================================="
echo ""

# Get the project root directory (parent of dev/)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://www.docker.com/get-started"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

echo "🐳 Docker is ready!"
echo ""

# Stop any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose -f docker/docker-compose.yml down 2>/dev/null

echo ""
echo "🏗️  Building SkillSwap Demo..."
echo "   This may take a few minutes on first run..."
echo ""

# Build and start the demo
docker-compose -f docker/docker-compose.yml up --build

echo ""
echo "Demo stopped. Run 'dev/demo-start.sh' again to restart."
