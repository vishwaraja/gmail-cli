#!/bin/bash

# Docker Test Script for Gmail CLI
echo "🐳 Testing Gmail CLI Docker Setup..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available"
    exit 1
fi

echo "✅ Docker Compose is available"

# Build the image
echo "🔨 Building Docker image..."
if docker-compose build; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Test basic container functionality
echo "🧪 Testing container functionality..."

# Test help command
if docker-compose run --rm gmail-cli-run gmail --help > /dev/null 2>&1; then
    echo "✅ Container can run Gmail CLI commands"
else
    echo "❌ Container failed to run Gmail CLI commands"
    exit 1
fi

# Test version command
if docker-compose run --rm gmail-cli-run gmail --version > /dev/null 2>&1; then
    echo "✅ Version command works"
else
    echo "❌ Version command failed"
    exit 1
fi

# Clean up
echo "🧹 Cleaning up test containers..."
docker-compose down > /dev/null 2>&1

echo ""
echo "🎉 All Docker tests passed!"
echo ""
echo "Next steps:"
echo "1. Add your credentials.json file"
echo "2. Run: ./docker-setup.sh"
echo "3. Run: ./docker-run.sh auth"
echo "4. Run: ./docker-run.sh list"
