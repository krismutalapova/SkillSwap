#!/bin/bash

echo "====================================="
echo "SkillSwap Docker Demo - Quick Start"
echo "====================================="
echo ""

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
docker-compose down 2>/dev/null

echo ""
echo "🏗️  Building SkillSwap Demo..."
echo "   This may take a few minutes on first run..."
echo ""

# Build and start the demo
docker-compose up --build

echo ""
echo "Demo stopped. Run './demo-start.sh' again to restart."
