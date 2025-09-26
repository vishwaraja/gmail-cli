#!/bin/bash

# Gmail CLI Docker Run Script
# This script provides easy commands to run Gmail CLI in Docker

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

# Check if container is running
if ! docker-compose ps | grep -q "gmail-cli.*Up"; then
    echo "🚀 Starting Gmail CLI container..."
    docker-compose up -d
    sleep 2
fi

# Handle special commands
case "$1" in
    "shell")
        echo "🐚 Opening shell in Gmail CLI container..."
        docker-compose exec gmail-cli /bin/bash
        ;;
    "stop")
        echo "🛑 Stopping Gmail CLI container..."
        docker-compose down
        ;;
    "restart")
        echo "🔄 Restarting Gmail CLI container..."
        docker-compose restart
        ;;
    "logs")
        echo "📋 Showing Gmail CLI container logs..."
        docker-compose logs -f gmail-cli
        ;;
    *)
        # Run Gmail CLI command
        echo "📧 Running: gmail $*"
        docker-compose exec gmail-cli gmail "$@"
        ;;
esac
