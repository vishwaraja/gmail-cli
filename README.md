# Gmail CLI 📧

A powerful, feature-rich command-line interface for Gmail built with Python. Manage your Gmail account directly from the terminal with a beautiful, user-friendly interface.

## ✨ Features

- 📬 **List emails** - View recent emails with rich formatting
- 📖 **Read emails** - Read full email content with attachments info
- ✉️ **Send emails** - Send emails with attachments support
- 🔍 **Search emails** - Use Gmail's powerful search syntax
- 🏷️ **Manage labels** - View and manage Gmail labels
- ✅ **Mark as read/unread** - Manage email status
- 🗑️ **Delete emails** - Remove unwanted messages
- 🔐 **Secure authentication** - OAuth2 authentication with Google
- 🎨 **Beautiful interface** - Rich terminal UI with colors and formatting
- 🐳 **Docker support** - Easy containerized deployment and isolation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher (for local installation)
- Docker and Docker Compose (for containerized installation)
- Gmail account
- Google Cloud Project with Gmail API enabled

### Installation Options

#### Option 1: Docker Installation (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vishwaraja/gmail-cli.git
   cd gmail-cli
   ```

2. **Set up Gmail API credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Gmail API
   - Create OAuth2 credentials (Desktop application)
   - Download the credentials file and save as `credentials.json` in the project directory

3. **Run Docker setup:**
   ```bash
   ./docker-setup.sh
   ```

4. **Authenticate with Gmail:**
   ```bash
   ./docker-run.sh auth
   ```

#### Option 2: Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vishwaraja/gmail-cli.git
   cd gmail-cli
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gmail API credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Gmail API
   - Create OAuth2 credentials (Desktop application)
   - Download the credentials file and save as `credentials.json` in the project directory

4. **Install the package:**
   ```bash
   pip install -e .
   ```

5. **Authenticate with Gmail:**
   ```bash
   gmail auth
   ```

### First Time Setup

1. **Authenticate with Gmail:**
   - **Docker:** `./docker-run.sh auth`
   - **Local:** `gmail auth`
   
   This will open a browser window for OAuth2 authentication.

2. **Test the connection:**
   - **Docker:** `./docker-run.sh list`
   - **Local:** `gmail list`

## 📖 Usage

### Basic Commands

#### Local Installation
```bash
# List recent emails
gmail list

# List emails with custom query
gmail list --query "from:example@gmail.com" --max-results 20

# Read a specific email
gmail read <message-id>

# Send an email
gmail send --to recipient@example.com --subject "Hello" --body "This is a test email"

# Search emails
gmail search "is:unread from:important@example.com"

# List all labels
gmail labels

# Mark email as read
gmail mark <message-id> --read

# Mark email as unread
gmail mark <message-id> --unread

# Delete an email
gmail delete <message-id>
```

#### Docker Installation
```bash
# List recent emails
./docker-run.sh list

# List emails with custom query
./docker-run.sh list --query "from:example@gmail.com" --max-results 20

# Read a specific email
./docker-run.sh read <message-id>

# Send an email
./docker-run.sh send --to recipient@example.com --subject "Hello" --body "This is a test email"

# Search emails
./docker-run.sh search "is:unread from:important@example.com"

# List all labels
./docker-run.sh labels

# Mark email as read
./docker-run.sh mark <message-id> --read

# Mark email as unread
./docker-run.sh mark <message-id> --unread

# Delete an email
./docker-run.sh delete <message-id>

# Open interactive shell
./docker-run.sh shell
```

### Advanced Usage

```bash
# Send email with attachments
gmail send --to user@example.com --subject "Files" --body "Please find attached" --attach file1.pdf --attach file2.jpg

# Send email with CC and BCC
gmail send --to user@example.com --cc cc@example.com --bcc bcc@example.com --subject "Meeting" --body "Meeting details"

# Filter by label
gmail list --label "INBOX"

# Search with complex queries
gmail search "has:attachment filename:pdf after:2024/01/01"
```

### Gmail Search Syntax

The search command supports Gmail's powerful search syntax:

- `from:email@example.com` - Emails from specific sender
- `to:email@example.com` - Emails to specific recipient
- `subject:keyword` - Emails with keyword in subject
- `has:attachment` - Emails with attachments
- `is:unread` - Unread emails
- `is:read` - Read emails
- `after:2024/01/01` - Emails after specific date
- `before:2024/12/31` - Emails before specific date
- `label:important` - Emails with specific label

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project directory:

```env
# Gmail API Configuration
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here

# Gmail API Scopes
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.modify

# Token storage location
TOKEN_FILE=token.json
CREDENTIALS_FILE=credentials.json
```

### File Structure

```
gmail-cli/
├── src/
│   └── gmail_cli/
│       ├── __init__.py
│       ├── auth.py          # Authentication handling
│       ├── gmail_client.py  # Core Gmail operations
│       └── cli.py           # Command-line interface
├── requirements.txt
├── setup.py
├── README.md
├── .env.example
└── .gitignore
```

## 🐳 Docker Usage

For detailed Docker setup and usage instructions, see [DOCKER.md](DOCKER.md).

### Quick Docker Commands

```bash
# Setup Docker environment
./docker-setup.sh

# Run commands
./docker-run.sh auth          # Authenticate
./docker-run.sh list          # List emails
./docker-run.sh shell         # Open shell

# One-time commands
docker-compose --profile run run gmail-cli-run gmail list
```

## 🛠️ Development

### Setting up Development Environment

1. **Clone and install in development mode:**
   ```bash
   git clone https://github.com/vishwaraja/gmail-cli.git
   cd gmail-cli
   pip install -e .
   ```

2. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

3. **Format code:**
   ```bash
   black src/
   flake8 src/
   ```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Requirements

- Python 3.8+
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client
- click
- rich
- python-dotenv
- colorama

## 🔐 Security

- Uses OAuth2 authentication (no password storage)
- Tokens are stored locally and can be revoked
- Follows Google's security best practices
- No sensitive data is logged or transmitted

## 🐛 Troubleshooting

### Common Issues

1. **Authentication failed:**
   - Ensure `credentials.json` is in the project directory
   - Check that Gmail API is enabled in Google Cloud Console
   - Verify OAuth2 credentials are configured correctly

2. **Permission denied:**
   - Make sure you've granted necessary permissions during OAuth2 flow
   - Try revoking and re-authenticating: `gmail revoke` then `gmail auth`

3. **Import errors:**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

### Getting Help

- Check the [Issues](https://github.com/vishwaraja/gmail-cli/issues) page
- Review [Gmail API documentation](https://developers.google.com/gmail/api)
- Open a new issue with detailed error information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gmail API team for the excellent API
- Rich library for beautiful terminal interfaces
- Click library for command-line interface framework
- All contributors and users of this project

## 📊 Roadmap

- [ ] Email composition with rich text editor
- [ ] Bulk operations (mark multiple emails, delete multiple)
- [ ] Email templates
- [ ] Advanced filtering and sorting
- [ ] Integration with other Google services
- [ ] Plugin system for extensions
- [ ] Configuration file support
- [ ] Email backup and export features

---

**Made with ❤️ by [Vishwaraja](https://github.com/vishwaraja)**
