#!/bin/bash

# Ultra-simple Docker setup for Gmail CLI
echo "🐳 Quick Gmail CLI Docker Setup"

# Check if credentials.json exists
if [ ! -f "credentials.json" ]; then
    echo "❌ credentials.json not found!"
    echo ""
    echo "📋 Quick Setup Steps:"
    echo "1. Go to: https://console.cloud.google.com/"
    echo "2. Create a new project (or select existing)"
    echo "3. Enable Gmail API (APIs & Services > Library > Gmail API)"
    echo "4. Create OAuth2 credentials (APIs & Services > Credentials)"
    echo "5. Download as 'credentials.json' and place in this directory"
    echo ""
    echo "Then run this script again!"
    exit 1
fi

echo "✅ credentials.json found"

# Build image
echo "🔨 Building Docker image..."
docker build -t gmail-cli .

# Create data directory
mkdir -p data

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📧 Quick Commands:"
echo "  docker run --rm -v \$(pwd)/credentials.json:/app/credentials.json:ro -v \$(pwd)/data:/app/data gmail-cli auth"
echo "  docker run --rm -v \$(pwd)/credentials.json:/app/credentials.json:ro -v \$(pwd)/data:/app/data gmail-cli list"
echo "  docker run --rm -v \$(pwd)/credentials.json:/app/credentials.json:ro -v \$(pwd)/data:/app/data gmail-cli send --to user@example.com --subject 'Hello' --body 'Test'"
echo ""
echo "Or use the simple script:"
echo "  ./docker-simple.sh run auth"
echo "  ./docker-simple.sh run list"
