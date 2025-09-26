#!/bin/bash

# Gmail CLI Setup Script
echo "🚀 Setting up Gmail CLI..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version detected"
else
    echo "❌ Python 3.8+ required. Found: $python_version"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Install package in development mode
echo "🔧 Installing Gmail CLI package..."
pip3 install -e .

# Check for credentials file
if [ ! -f "credentials.json" ]; then
    echo "⚠️  credentials.json not found!"
    echo ""
    echo "To set up Gmail API credentials:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Create a new project or select existing one"
    echo "3. Enable the Gmail API"
    echo "4. Create OAuth2 credentials (Desktop application)"
    echo "5. Download credentials and save as 'credentials.json'"
    echo ""
    echo "Then run: gmail auth"
else
    echo "✅ credentials.json found"
    echo "🔐 Run 'gmail auth' to authenticate with Gmail"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Quick start:"
echo "  gmail auth          # Authenticate with Gmail"
echo "  gmail list          # List recent emails"
echo "  gmail --help        # Show all commands"
echo ""
echo "For more information, see README.md"
