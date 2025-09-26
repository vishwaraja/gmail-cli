# Gmail CLI Docker Setup 🐳

This guide explains how to run Gmail CLI using Docker containers for easy deployment and isolation.

## 🚀 Quick Start with Docker

### Prerequisites

- Docker installed
- Gmail API credentials (`credentials.json`)

### 1. Clone and Setup

```bash
git clone https://github.com/vishwaraja/gmail-cli.git
cd gmail-cli
```

### 2. Add Gmail API Credentials

Place your `credentials.json` file in the secure location: `~/.gmail-cli/credentials.json`

### 3. Run Docker Setup

```bash
./docker-setup.sh
```

This script will:
- Create necessary directories
- Build or pull the Docker image
- Set up secure credential storage
- Create data directory for persistent storage

## 📖 Docker Usage

### Using the Docker Runner Script (Recommended)

```bash
# Authenticate with Gmail (first time only)
./docker-run.sh auth

# List recent emails
./docker-run.sh list

# Send an email
./docker-run.sh send --to user@example.com --subject "Hello" --body "Test email"

# Search emails
./docker-run.sh search "is:unread"

# Get help
./docker-run.sh --help
```

### Using the Docker Run Script

```bash
# Make the script executable (if not already)
chmod +x docker-run.sh

# Use the script for easier command execution
./docker-run.sh auth
./docker-run.sh list
./docker-run.sh send --to user@example.com --subject "Hello" --body "Test"
./docker-run.sh search "is:unread"
./docker-run.sh shell  # Open interactive shell
```

### One-time Commands

For one-time commands without keeping a container running:

```bash
# Run a single command and exit
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v ~/.gmail-cli/credentials.json:/app/credentials.json:ro \
  -v ~/.gmail-cli/token.json:/app/token.json \
  -e GMAIL_CREDENTIALS_PATH="/app/credentials.json" \
  -e GMAIL_TOKEN_PATH="/app/token.json" \
  vishwa86/gmail-cli:latest list

docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v ~/.gmail-cli/credentials.json:/app/credentials.json:ro \
  -v ~/.gmail-cli/token.json:/app/token.json \
  -e GMAIL_CREDENTIALS_PATH="/app/credentials.json" \
  -e GMAIL_TOKEN_PATH="/app/token.json" \
  vishwa86/gmail-cli:latest search "from:important@example.com"
```

## 🔧 Docker Configuration

### Volumes

- `./data:/app/data` - Persistent storage for data
- `~/.gmail-cli/credentials.json:/app/credentials.json:ro` - Read-only credentials from secure location
- `~/.gmail-cli/token.json:/app/token.json` - Token storage from secure location

### Environment Variables

- `GMAIL_CREDENTIALS_PATH=/app/credentials.json` - Credentials file location
- `GMAIL_TOKEN_PATH=/app/token.json` - Token file location

## 🛠️ Docker Commands

### Container Management

```bash
# Start the container
docker-compose up -d

# Stop the container
docker-compose down

# Restart the container
docker-compose restart

# View logs
docker-compose logs -f gmail-cli

# Check container status
docker-compose ps
```

### Building and Rebuilding

```bash
# Build the image
docker-compose build

# Rebuild without cache
docker-compose build --no-cache

# Pull latest base image and rebuild
docker-compose build --pull
```

### Interactive Shell

```bash
# Open bash shell in container
docker-compose exec gmail-cli /bin/bash

# Or use the helper script
./docker-run.sh shell
```

## 🔐 Security Considerations

### Credentials Management

- Credentials are mounted as read-only volumes
- Tokens are stored in persistent volumes
- Container runs as non-root user for security

### Data Persistence

- Authentication tokens are preserved between container restarts
- Data directory is mounted as a volume for persistence
- Credentials are not stored in the Docker image

## 🐛 Troubleshooting

### Common Issues

1. **Container won't start:**
   ```bash
   # Check logs
   docker-compose logs gmail-cli
   
   # Rebuild image
   docker-compose build --no-cache
   ```

2. **Authentication issues:**
   ```bash
   # Remove old tokens and re-authenticate
   rm -f token.json data/token.json
   docker-compose exec gmail-cli gmail auth
   ```

3. **Permission issues:**
   ```bash
   # Fix data directory permissions
   sudo chown -R $USER:$USER data/
   ```

4. **Credentials not found:**
   - Ensure `credentials.json` is in the project root
   - Check file permissions: `ls -la credentials.json`

### Debug Mode

```bash
# Run container with debug output
docker-compose exec gmail-cli gmail --help

# Check container environment
docker-compose exec gmail-cli env

# Inspect container filesystem
docker-compose exec gmail-cli ls -la /app/
```

## 🔄 Updates

### Updating the Container

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Updating Dependencies

```bash
# Rebuild with updated requirements
docker-compose build --no-cache
```

## 📊 Performance

### Resource Usage

The container is lightweight and uses minimal resources:
- Base image: Python 3.11 slim (~45MB)
- Runtime memory: ~50-100MB
- CPU usage: Minimal (only during operations)

### Optimization Tips

- Use the `gmail-cli-run` service for one-time commands
- Keep the main container running for frequent use
- Mount volumes for persistent data storage

## 🌐 Network Considerations

### Internet Access

The container needs internet access for:
- Gmail API authentication
- Sending/receiving emails
- Token refresh

### Firewall

Ensure the following ports are accessible:
- 443 (HTTPS) for Gmail API
- 80 (HTTP) for OAuth2 redirect (temporary)

## 📝 Examples

### Complete Workflow

```bash
# 1. Setup
./docker-setup.sh

# 2. Authenticate
./docker-run.sh auth

# 3. List emails
./docker-run.sh list

# 4. Read an email
./docker-run.sh read <message-id>

# 5. Send an email
./docker-run.sh send --to friend@example.com --subject "Hello from Docker!" --body "This email was sent using Gmail CLI in Docker!"

# 6. Search for unread emails
./docker-run.sh search "is:unread"

# 7. Clean up when done
docker-compose down
```

### Batch Operations

```bash
# Process multiple commands
./docker-run.sh list --max-results 20
./docker-run.sh search "has:attachment"
./docker-run.sh labels
```

This Docker setup provides a clean, isolated environment for running Gmail CLI with persistent authentication and easy management.
