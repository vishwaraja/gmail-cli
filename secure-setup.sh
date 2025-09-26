#!/bin/bash

# Gmail CLI Secure Setup Script
# This script helps you set up credentials securely

set -e

echo "🔐 Gmail CLI Secure Setup"
echo "========================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if credentials directory exists
CREDENTIALS_DIR="$HOME/.gmail-cli"
if [ ! -d "$CREDENTIALS_DIR" ]; then
    print_info "Creating secure credentials directory: $CREDENTIALS_DIR"
    mkdir -p "$CREDENTIALS_DIR"
    chmod 700 "$CREDENTIALS_DIR"
    print_status "Credentials directory created"
fi

# Check for existing credentials
CREDENTIALS_FILE="$CREDENTIALS_DIR/credentials.json"
TOKEN_FILE="$CREDENTIALS_DIR/token.json"

if [ -f "$CREDENTIALS_FILE" ]; then
    print_warning "Credentials file already exists: $CREDENTIALS_FILE"
    read -p "Do you want to replace it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm "$CREDENTIALS_FILE"
        print_status "Existing credentials file removed"
    else
        print_info "Keeping existing credentials file"
    fi
fi

# Check for credentials in project directory
PROJECT_CREDENTIALS="./credentials.json"
if [ -f "$PROJECT_CREDENTIALS" ]; then
    print_warning "Found credentials.json in project directory!"
    print_error "This is a security risk - credentials should not be in the project directory"
    read -p "Move to secure location? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        mv "$PROJECT_CREDENTIALS" "$CREDENTIALS_FILE"
        chmod 600 "$CREDENTIALS_FILE"
        print_status "Credentials moved to secure location: $CREDENTIALS_FILE"
    fi
fi

# Check for token in project directory
PROJECT_TOKEN="./token.json"
if [ -f "$PROJECT_TOKEN" ]; then
    print_warning "Found token.json in project directory!"
    print_error "This is a security risk - tokens should not be in the project directory"
    read -p "Move to secure location? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        mv "$PROJECT_TOKEN" "$TOKEN_FILE"
        chmod 600 "$TOKEN_FILE"
        print_status "Token moved to secure location: $TOKEN_FILE"
    fi
fi

# Check if credentials exist
if [ ! -f "$CREDENTIALS_FILE" ]; then
    print_info "No credentials file found. Please follow these steps:"
    echo ""
    echo "1. Go to Google Cloud Console: https://console.cloud.google.com/"
    echo "2. Create a new project or select existing one"
    echo "3. Enable Gmail API"
    echo "4. Create OAuth2 credentials (Desktop application)"
    echo "5. Download the credentials.json file"
    echo "6. Save it as: $CREDENTIALS_FILE"
    echo ""
    read -p "Press Enter when you have saved the credentials file..."
    
    if [ ! -f "$CREDENTIALS_FILE" ]; then
        print_error "Credentials file not found. Please save it as: $CREDENTIALS_FILE"
        exit 1
    fi
fi

# Set proper permissions
chmod 600 "$CREDENTIALS_FILE"
if [ -f "$TOKEN_FILE" ]; then
    chmod 600 "$TOKEN_FILE"
fi

print_status "Credentials file permissions set correctly"

# Set environment variables
echo ""
print_info "Setting up environment variables..."
echo "export GMAIL_CREDENTIALS_PATH=\"$CREDENTIALS_FILE\"" >> ~/.bashrc
echo "export GMAIL_TOKEN_PATH=\"$TOKEN_FILE\"" >> ~/.bashrc

# Also add to .zshrc if it exists
if [ -f ~/.zshrc ]; then
    echo "export GMAIL_CREDENTIALS_PATH=\"$CREDENTIALS_FILE\"" >> ~/.zshrc
    echo "export GMAIL_TOKEN_PATH=\"$TOKEN_FILE\"" >> ~/.zshrc
fi

print_status "Environment variables added to shell configuration"

# Test authentication
echo ""
print_info "Testing authentication..."
if command -v gmail &> /dev/null; then
    if gmail auth; then
        print_status "Authentication successful!"
    else
        print_error "Authentication failed. Please check your credentials."
        exit 1
    fi
else
    print_warning "Gmail CLI not found. Please install it first:"
    echo "pip install -e ."
fi

echo ""
print_status "Secure setup completed!"
echo ""
print_info "Your credentials are now stored securely in:"
echo "  - Credentials: $CREDENTIALS_FILE"
echo "  - Token: $TOKEN_FILE"
echo ""
print_info "Environment variables set:"
echo "  - GMAIL_CREDENTIALS_PATH=$CREDENTIALS_FILE"
echo "  - GMAIL_TOKEN_PATH=$TOKEN_FILE"
echo ""
print_warning "Remember to restart your terminal or run 'source ~/.bashrc' to load the environment variables"
