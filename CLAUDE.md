# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gmail CLI is a command-line interface for Gmail built with Python. It uses OAuth2 authentication via the Gmail API to provide full email management capabilities from the terminal. The application supports both local installation and Docker deployment.

## Architecture

### Core Components

**Entry Point: `src/gmail_cli/cli.py`**
- CLI interface built with Click framework
- Uses Rich library for terminal UI formatting
- Main command groups: emails, drafts, threads, labels, settings
- All commands route through the `GmailClient` class

**Gmail Operations: `src/gmail_cli/gmail_client.py`**
- `GmailClient` class wraps Google's Gmail API
- Handles all Gmail operations (send, read, delete, search, etc.)
- Message parsing and MIME handling for attachments
- Thread and draft management

**Authentication: `src/gmail_cli/auth.py`**
- `GmailAuthenticator` class manages OAuth2 flow
- Token storage and refresh handling
- Credentials stored in `~/.gmail-cli/` by default
- Environment variables: `GMAIL_CREDENTIALS_PATH`, `GMAIL_TOKEN_PATH`

### Data Flow

1. User runs CLI command → Click parses arguments → Command handler in `cli.py`
2. Command handler creates `GmailAuthenticator` → Authenticates/refreshes token
3. `GmailAuthenticator.get_service()` returns Gmail API service object
4. Service passed to `GmailClient` → API calls made → Results formatted with Rich
5. Output displayed to user via `console.print()`

## Development Commands

### Setup and Installation

```bash
# Install in development mode (editable)
pip install -e .

# Install dependencies only
pip install -r requirements.txt

# Run secure setup (moves credentials to ~/.gmail-cli/)
./secure-setup.sh
```

### Running the CLI

```bash
# Local installation
gmail auth                    # First time authentication
gmail list                    # List emails
gmail --help                  # Show all commands

# Docker installation
./docker-setup.sh            # One-time setup
./docker-run.sh auth         # Authenticate
./docker-run.sh list         # Run commands
./docker-run.sh shell        # Interactive shell
```

### Testing and Code Quality

```bash
# Run linting (if configured)
flake8 src/

# Format code (if configured)
black src/

# Note: This project doesn't have automated tests yet
# Manual testing required for all changes
```

### Docker Development

```bash
# Build Docker image
docker build -t gmail-cli:dev .

# Run with local credentials
docker run -it --rm \
  -v ~/.gmail-cli/credentials.json:/app/credentials.json:ro \
  -v ~/.gmail-cli/token.json:/app/token.json \
  gmail-cli:dev list

# Docker Compose
docker-compose up -d         # Start container
docker-compose logs -f       # View logs
docker-compose down          # Stop container
```

## Important Implementation Details

### OAuth2 Token Management

- **Token file must be a FILE, not a directory**: The auth system writes JSON to `token.json`
- Token stored at `~/.gmail-cli/token.json` by default (configurable via `GMAIL_TOKEN_PATH`)
- Credentials at `~/.gmail-cli/credentials.json` by default (configurable via `GMAIL_CREDENTIALS_PATH`)
- If token file is corrupted or is a directory, delete it and re-authenticate

### Gmail API Message Structure

- Messages have complex nested MIME structure in `payload`
- Body content can be in `payload.body.data` (simple) or `payload.parts[]` (multipart)
- All body data is base64url encoded and must be decoded
- Attachments are in `parts[]` with `filename` and `attachmentId`
- Headers are in `payload.headers[]` as list of `{name, value}` objects

### Search Query Syntax

Gmail search uses special operators:
- `from:`, `to:`, `subject:`, `label:`, `has:attachment`
- `is:unread`, `is:read`, `is:starred`
- `after:YYYY/MM/DD`, `before:YYYY/MM/DD`
- Boolean: `OR`, `-` (negation), `()` for grouping

### Click Command Structure

Commands use Click decorators:
```python
@main.command()                    # Single command
@main.group()                      # Command group (e.g., drafts, threads)
@click.argument('name')            # Required positional argument
@click.option('--flag', '-f')      # Optional flag with short form
```

## Security Considerations

### Credential Storage

- **NEVER commit** `credentials.json` or `token.json` to git
- Store credentials in `~/.gmail-cli/` directory with 600 permissions
- Use environment variables for custom paths
- `.gitignore` blocks all `.json` files except config files

### OAuth2 Scopes

Current scopes (in `auth.py`):
- `gmail.readonly` - Read email
- `gmail.send` - Send email
- `gmail.modify` - Modify labels, mark read/unread
- `gmail.compose` - Create drafts

### Docker Security

- Container runs as non-root user `gmail-cli`
- Credentials mounted as read-only (`:ro`)
- Token file mounted as read-write (for refresh)

## Common Issues and Solutions

### Issue: "Is a directory: 'token.json'"

**Cause**: The token file path points to a directory instead of a file

**Solution**:
```bash
# Remove the directory
rm -rf ~/.gmail-cli/token.json

# Re-authenticate
gmail auth
# or for Docker:
./docker-run.sh auth
```

### Issue: Authentication fails with "credentials.json not found"

**Cause**: Credentials not in expected location

**Solution**:
1. Download OAuth2 credentials from Google Cloud Console
2. Save to `~/.gmail-cli/credentials.json`
3. Or set `GMAIL_CREDENTIALS_PATH` environment variable

### Issue: "Permission denied" when accessing files

**Cause**: Incorrect file permissions

**Solution**:
```bash
chmod 600 ~/.gmail-cli/credentials.json
chmod 600 ~/.gmail-cli/token.json
chmod 700 ~/.gmail-cli/
```

## Adding New Commands

When adding a new command:

1. Add command handler in `cli.py` using `@main.command()` or `@group.command()`
2. Implement business logic in `GmailClient` class in `gmail_client.py`
3. Use Rich library for formatted output: `console.print()`, `Table()`, `Panel()`
4. Add help text and examples to the command docstring
5. Update README.md with new command usage

Example structure:
```python
@main.command()
@click.argument('message_id')
@click.option('--flag', '-f', help='Description')
def new_command(message_id: str, flag: bool):
    """Command description

    Example:
        gmail new-command msg123 --flag
    """
    auth = GmailAuthenticator()
    service = auth.get_service()
    client = GmailClient(service)

    result = client.new_operation(message_id, flag)

    if result:
        console.print("[green]✅ Success[/green]")
    else:
        console.print("[red]❌ Failed[/red]")
```

## Dependencies

Key dependencies and their purposes:
- `google-api-python-client` - Gmail API client
- `google-auth*` - OAuth2 authentication flow
- `click` - CLI framework
- `rich` - Terminal formatting and colors
- `python-dotenv` - Environment variable loading

## File Locations

- Source code: `src/gmail_cli/`
- Credentials: `~/.gmail-cli/credentials.json` (default)
- Token: `~/.gmail-cli/token.json` (default)
- Docker data: `./data/` (when using Docker)
- Setup scripts: `./secure-setup.sh`, `./docker-setup.sh`, `./docker-run.sh`
