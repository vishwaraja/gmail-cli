#!/bin/bash

# Gmail CLI Docker Setup Script
echo "🐳 Setting up Gmail CLI with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Check for credentials file
if [ ! -f "credentials.json" ]; then
    echo "⚠️  credentials.json not found!"
    echo ""
    echo "To set up Gmail API credentials:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Create a new project or select existing one"
    echo "3. Enable the Gmail API"
    echo "4. Create OAuth2 credentials (Desktop application)"
    echo "5. Download the credentials file and save as 'credentials.json'"
    echo ""
    echo "After adding credentials.json, run this script again."
    exit 1
fi

echo "✅ credentials.json found"

# Build the Docker image
echo "🔨 Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Start the container
echo "🚀 Starting Gmail CLI container..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✅ Gmail CLI container started successfully!"
    echo ""
    echo "🎉 Setup complete!"
    echo ""
    echo "Usage:"
    echo "  docker-compose exec gmail-cli gmail auth          # Authenticate with Gmail"
    echo "  docker-compose exec gmail-cli gmail list          # List recent emails"
    echo "  docker-compose exec gmail-cli gmail --help        # Show all commands"
    echo ""
    echo "Or use the run profile for one-time commands:"
    echo "  docker-compose --profile run run gmail-cli-run gmail list"
    echo ""
    echo "To stop the container:"
    echo "  docker-compose down"
else
    echo "❌ Failed to start Gmail CLI container"
    exit 1
fi
