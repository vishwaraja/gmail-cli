#!/bin/bash

# Gmail CLI Docker Setup Script
# This script sets up the Docker environment for Gmail CLI

set -e

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

echo "🐳 Gmail CLI Docker Setup"
echo "========================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    print_info "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is installed and running"

# Check if we should build or pull the image
if [ "$1" = "--build" ]; then
    print_info "Building Gmail CLI Docker image locally..."
    docker build -t vishwa86/gmail-cli:latest .
    print_status "Docker image built successfully"
else
    print_info "Pulling Gmail CLI Docker image from Docker Hub..."
    if docker pull vishwa86/gmail-cli:latest; then
        print_status "Docker image pulled successfully"
    else
        print_warning "Failed to pull image. Building locally instead..."
        docker build -t vishwa86/gmail-cli:latest .
        print_status "Docker image built successfully"
    fi
fi

# Create data directory
mkdir -p data
print_status "Data directory created: $(pwd)/data"

# Set up secure credentials directory
CREDENTIALS_DIR="$HOME/.gmail-cli"
if [ ! -d "$CREDENTIALS_DIR" ]; then
    mkdir -p "$CREDENTIALS_DIR"
    chmod 700 "$CREDENTIALS_DIR"
    print_status "Secure credentials directory created: $CREDENTIALS_DIR"
fi

# Check for existing credentials
if [ -f "credentials.json" ]; then
    print_warning "Found credentials.json in project directory!"
    print_error "This is a security risk. Moving to secure location..."
    mv "credentials.json" "$CREDENTIALS_DIR/"
    chmod 600 "$CREDENTIALS_DIR/credentials.json"
    print_status "Credentials moved to secure location"
fi

if [ -f "token.json" ]; then
    print_warning "Found token.json in project directory!"
    print_error "This is a security risk. Moving to secure location..."
    mv "token.json" "$CREDENTIALS_DIR/"
    chmod 600 "$CREDENTIALS_DIR/token.json"
    print_status "Token moved to secure location"
fi

echo ""
print_status "Docker setup completed!"
echo ""
print_info "Next steps:"
echo "1. Set up your Gmail API credentials:"
echo "   - Go to Google Cloud Console"
echo "   - Enable Gmail API"
echo "   - Create OAuth2 credentials"
echo "   - Save as: $CREDENTIALS_DIR/credentials.json"
echo ""
echo "2. Authenticate with Gmail:"
echo "   ./docker-run.sh auth"
echo ""
echo "3. Start using Gmail CLI:"
echo "   ./docker-run.sh list"
echo "   ./docker-run.sh --help"
echo ""
print_info "For more information, see README.md"
