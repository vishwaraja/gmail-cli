#!/bin/bash

# Gmail CLI Docker Runner Script
# This script runs Gmail CLI commands in a Docker container

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

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Set up secure credential paths
CREDENTIALS_DIR="$HOME/.gmail-cli"
CREDENTIALS_FILE="$CREDENTIALS_DIR/credentials.json"
TOKEN_FILE="$CREDENTIALS_DIR/token.json"

# Check for credentials in secure location
if [ ! -f "$CREDENTIALS_FILE" ]; then
    # Check for credentials in project directory (legacy)
    if [ -f "credentials.json" ]; then
        print_warning "Found credentials.json in project directory!"
        print_error "This is a security risk. Moving to secure location..."
        mkdir -p "$CREDENTIALS_DIR"
        mv "credentials.json" "$CREDENTIALS_FILE"
        chmod 600 "$CREDENTIALS_FILE"
        print_status "Credentials moved to secure location: $CREDENTIALS_FILE"
    else
        print_error "No credentials found!"
        print_info "Please run './secure-setup.sh' to set up credentials securely."
        exit 1
    fi
fi

# Check for token in secure location
if [ ! -f "$TOKEN_FILE" ] && [ -f "token.json" ]; then
    print_warning "Found token.json in project directory!"
    print_error "This is a security risk. Moving to secure location..."
    mkdir -p "$CREDENTIALS_DIR"
    mv "token.json" "$TOKEN_FILE"
    chmod 600 "$TOKEN_FILE"
    print_status "Token moved to secure location: $TOKEN_FILE"
fi

# Create data directory if it doesn't exist
mkdir -p data

# Show usage if no arguments
if [ $# -eq 0 ]; then
    echo "🐳 Gmail CLI Docker Runner"
    echo ""
    echo "Usage: $0 <command> [args...]"
    echo ""
    echo "Examples:"
    echo "  $0 auth                    # Authenticate with Gmail"
    echo "  $0 list                    # List recent emails"
    echo "  $0 read <message-id>       # Read specific email"
    echo "  $0 send --to user@example.com --subject 'Hello' --body 'Test'"
    echo "  $0 search 'is:unread'      # Search emails"
    echo "  $0 labels                  # List all labels"
    echo "  $0 --help                  # Show help"
    echo ""
    echo "Interactive mode:"
    echo "  $0 shell                   # Open shell in container"
    echo ""
    exit 1
fi

# Handle special commands
case "$1" in
    "shell")
        print_info "Opening shell in Gmail CLI container..."
        docker run -it --rm \
            -v "$(pwd)/data:/app/data" \
            -v "$CREDENTIALS_FILE:/app/credentials.json:ro" \
            -v "$TOKEN_FILE:/app/token.json" \
            -e GMAIL_CREDENTIALS_PATH="/app/credentials.json" \
            -e GMAIL_TOKEN_PATH="/app/token.json" \
            vishwa86/gmail-cli:latest /bin/bash
        ;;
    "build")
        print_info "Building Gmail CLI Docker image..."
        docker build -t vishwa86/gmail-cli:latest .
        print_status "Docker image built successfully"
        ;;
    "pull")
        print_info "Pulling latest Gmail CLI Docker image..."
        docker pull vishwa86/gmail-cli:latest
        print_status "Docker image pulled successfully"
        ;;
    "push")
        print_info "Pushing Gmail CLI Docker image..."
        docker push vishwa86/gmail-cli:latest
        print_status "Docker image pushed successfully"
        ;;
    *)
        # Run Gmail CLI command
        print_info "Running: gmail $*"
        docker run -it --rm \
            -v "$(pwd)/data:/app/data" \
            -v "$CREDENTIALS_FILE:/app/credentials.json:ro" \
            -v "$TOKEN_FILE:/app/token.json" \
            -e GMAIL_CREDENTIALS_PATH="/app/credentials.json" \
            -e GMAIL_TOKEN_PATH="/app/token.json" \
            vishwa86/gmail-cli:latest "$@"
        ;;
esac