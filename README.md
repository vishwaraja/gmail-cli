# Gmail CLI 📧

A powerful, feature-rich command-line interface for Gmail built with Python. Manage your Gmail account directly from the terminal with a beautiful, user-friendly interface.

## ✨ Features

### 📧 **Core Email Operations**
- 📬 **List emails** - View recent emails with rich formatting
- 📖 **Read emails** - Read full email content with attachments info
- ✉️ **Send emails** - Send emails with attachments, CC, BCC support
- 🔍 **Search emails** - Use Gmail's powerful search syntax
- ✅ **Mark as read/unread** - Manage email status
- 🗑️ **Delete emails** - Remove unwanted messages

### 📝 **Draft Management**
- 📝 **Create drafts** - Save emails as drafts for later
- 📋 **List drafts** - View all saved drafts
- 📖 **Read drafts** - Review draft content
- ✏️ **Update drafts** - Modify existing drafts
- 📤 **Send drafts** - Send saved drafts
- 🗑️ **Delete drafts** - Remove unwanted drafts

### 🧵 **Thread Management**
- 🧵 **List threads** - View email conversations
- 📖 **Read threads** - Read entire conversation threads
- 🗑️ **Delete threads** - Remove conversation threads
- 🏷️ **Modify threads** - Add/remove labels from threads

### 🏷️ **Label Management**
- 📋 **List labels** - View all Gmail labels
- ➕ **Create labels** - Create custom labels
- 🗑️ **Delete labels** - Remove custom labels
- ⚙️ **Label settings** - Configure label visibility

### ⚙️ **Settings Management**
- 🔍 **Email filters** - Create and manage email filters
- 📧 **Forwarding** - Set up email forwarding addresses
- 📤 **Send-as aliases** - Configure send-as email addresses
- 🏖️ **Vacation responder** - Set up auto-reply messages
- 👥 **Delegates** - Manage delegated access

### 📎 **Attachments**
- 📥 **Download attachments** - Save email attachments locally
- 📊 **Attachment info** - View attachment metadata

### 🔐 **Security & Authentication**
- 🔐 **OAuth2 authentication** - Secure Google authentication
- 🔄 **Token management** - Automatic token refresh
- 🚫 **Revoke access** - Revoke stored credentials

### 🎨 **User Experience**
- 🎨 **Beautiful interface** - Rich terminal UI with colors and formatting
- 📊 **Progress indicators** - Visual feedback for operations
- 💡 **Comprehensive help** - Detailed help system with examples
- 🐳 **Docker support** - Easy containerized deployment and isolation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher (for local installation)
- Docker and Docker Compose (for containerized installation)
- Gmail account
- Google Cloud Project with Gmail API enabled

### 🔐 Security First

**IMPORTANT**: Never commit credentials to version control! Use the secure setup script:

```bash
# Run the secure setup script
./secure-setup.sh
```

This script will:
- Create a secure directory for credentials (`~/.gmail-cli/`)
- Move any existing credentials to the secure location
- Set proper file permissions
- Configure environment variables

**Security Features:**
- OAuth2 authentication (no password storage)
- Secure credential storage in user home directory
- Environment variable configuration
- Comprehensive `.gitignore` for sensitive files

### Installation Options

#### Option 1: Docker Installation (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vishwaraja/gmail-cli.git
   cd gmail-cli
   ```

2. **Run Docker setup:**
   ```bash
   ./docker-setup.sh
   ```

3. **Set up Gmail API credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Gmail API
   - Create OAuth2 credentials (Desktop application)
   - Save the credentials file as `~/.gmail-cli/credentials.json`

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

# Draft management
gmail drafts create --to user@example.com --subject "Draft" --body "Content"
gmail drafts list
gmail drafts send <draft-id>

# Thread management
gmail threads list
gmail threads read <thread-id>
gmail threads delete <thread-id>

# Label management
gmail label create "My Custom Label"
gmail label delete <label-id>

# Settings management
gmail settings filters list
gmail settings forwarding list
gmail settings sendas list
gmail settings vacation status

# Download attachments
gmail download <message-id> <attachment-id> --filename document.pdf
```

## 📚 Complete Command Reference

### 🔐 Authentication
```bash
gmail auth                    # Authenticate with Gmail
gmail revoke                  # Revoke stored credentials
```

### 📧 Basic Email Operations
```bash
gmail list                    # List recent emails
gmail list --max-results 20   # List 20 emails
gmail list --query 'is:unread' # List unread emails
gmail read <message-id>       # Read specific email
gmail send --to user@example.com --subject 'Hello' --body 'Hi!'
gmail search 'from:important@example.com' # Search emails
gmail mark <message-id> --read # Mark as read
gmail delete <message-id>     # Delete email
```

### 📝 Draft Management
```bash
gmail drafts list             # List all drafts
gmail drafts create --to user@example.com --subject 'Draft' --body 'Content'
gmail drafts read <draft-id>  # Read specific draft
gmail drafts send <draft-id>  # Send draft
gmail drafts delete <draft-id> # Delete draft
```

### 🧵 Thread Management
```bash
gmail threads list            # List message threads
gmail threads read <thread-id> # Read entire thread
gmail threads delete <thread-id> # Delete thread
```

### 🏷️ Label Management
```bash
gmail labels                  # List all labels
gmail label create 'My Label' # Create new label
gmail label delete <label-id> # Delete label
```

### ⚙️ Settings Management
```bash
gmail settings filters list   # List email filters
gmail settings forwarding list # List forwarding addresses
gmail settings sendas list    # List send-as aliases
gmail settings vacation status # Show vacation responder
```

### 📎 Attachments
```bash
gmail download <message-id> <attachment-id> # Download attachment
gmail download <msg-id> <att-id> --filename file.pdf
```

### 🔍 Search Examples
```bash
gmail search 'is:unread'      # Unread emails
gmail search 'from:boss@company.com' # From specific sender
gmail search 'has:attachment' # Emails with attachments
gmail search 'subject:meeting' # Subject contains 'meeting'
gmail search 'after:2024/01/01' # After specific date
gmail search 'label:important' # With specific label
```

### 📤 Sending Examples
```bash
gmail send --to user@example.com --subject 'Hello' --body 'Hi there!'
gmail send --to user@example.com --cc cc@example.com --subject 'Meeting' --body 'Details'
gmail send --to user@example.com --subject 'Files' --body 'Attached' --attach file1.pdf --attach file2.jpg
```

### 🐳 Docker Usage
```bash
./docker-run.sh list          # List emails in Docker
./docker-run.sh send --to user@example.com --subject 'Hello' --body 'Test'
./docker-run.sh shell         # Open interactive shell
```

### 💡 Tips
- Use `--help` with any command for detailed options
- Message/thread/draft IDs can be partial (first 8+ characters)
- All commands support `--confirm/-y` to skip confirmations
- Use quotes around search queries with spaces
- Attachments are supported in send and draft commands

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
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v ~/.gmail-cli/credentials.json:/app/credentials.json:ro \
  -v ~/.gmail-cli/token.json:/app/token.json \
  -e GMAIL_CREDENTIALS_PATH="/app/credentials.json" \
  -e GMAIL_TOKEN_PATH="/app/token.json" \
  vishwa86/gmail-cli:latest list
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

## 📖 Related Articles

- **[Building a Secure Gmail CLI: From Development to Production](https://dev.to/vishwaraja_pathivishwa/building-a-secure-gmail-cli-from-development-to-production-1g17)** - Detailed blog post about the development journey, security considerations, and Docker simplification

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
