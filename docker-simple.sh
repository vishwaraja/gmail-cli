#!/bin/bash

# Simple Docker commands for Gmail CLI
# No Docker Compose needed!

IMAGE_NAME="gmail-cli"
CONTAINER_NAME="gmail-cli-container"

# Build the image
build() {
    echo "🔨 Building Gmail CLI Docker image..."
    docker build -t $IMAGE_NAME .
}

# Run a command in the container
run() {
    if [ $# -eq 0 ]; then
        echo "Usage: $0 run <gmail-command> [args...]"
        echo "Example: $0 run list"
        echo "Example: $0 run send --to user@example.com --subject 'Hello' --body 'Test'"
        exit 1
    fi
    
    echo "📧 Running: gmail $*"
    docker run --rm \
        -v "$(pwd)/credentials.json:/app/credentials.json:ro" \
        -v "$(pwd)/token.json:/app/token.json" \
        -v "$(pwd)/data:/app/data" \
        $IMAGE_NAME "$@"
}

# Start persistent container
start() {
    echo "🚀 Starting persistent Gmail CLI container..."
    docker run -d --name $CONTAINER_NAME \
        -v "$(pwd)/credentials.json:/app/credentials.json:ro" \
        -v "$(pwd)/token.json:/app/token.json" \
        -v "$(pwd)/data:/app/data" \
        $IMAGE_NAME tail -f /dev/null
    echo "✅ Container started. Use 'exec' to run commands."
}

# Execute command in running container
exec() {
    if [ $# -eq 0 ]; then
        echo "Usage: $0 exec <gmail-command> [args...]"
        echo "Example: $0 exec list"
        exit 1
    fi
    
    echo "📧 Executing: gmail $*"
    docker exec -it $CONTAINER_NAME gmail "$@"
}

# Stop and remove container
stop() {
    echo "🛑 Stopping Gmail CLI container..."
    docker stop $CONTAINER_NAME 2>/dev/null
    docker rm $CONTAINER_NAME 2>/dev/null
    echo "✅ Container stopped and removed."
}

# Show container status
status() {
    docker ps -a --filter name=$CONTAINER_NAME
}

# Show help
help() {
    echo "🐳 Simple Gmail CLI Docker Manager"
    echo ""
    echo "Commands:"
    echo "  build                    Build the Docker image"
    echo "  run <cmd> [args...]      Run a one-time command"
    echo "  start                    Start persistent container"
    echo "  exec <cmd> [args...]     Execute command in running container"
    echo "  stop                     Stop and remove container"
    echo "  status                   Show container status"
    echo "  help                     Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 run auth"
    echo "  $0 run list"
    echo "  $0 start"
    echo "  $0 exec list"
    echo "  $0 stop"
}

# Main command handling
case "$1" in
    "build")
        build
        ;;
    "run")
        shift
        run "$@"
        ;;
    "start")
        start
        ;;
    "exec")
        shift
        exec "$@"
        ;;
    "stop")
        stop
        ;;
    "status")
        status
        ;;
    "help"|"--help"|"-h"|"")
        help
        ;;
    *)
        echo "Unknown command: $1"
        help
        exit 1
        ;;
esac
