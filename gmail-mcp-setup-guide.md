# Gmail MCP Server Setup Guide

## Step 1: Google Cloud Console Setup

### 1.1 Create/Select Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your project name

### 1.2 Enable Gmail API
1. Go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on it and press "Enable"

### 1.3 Create OAuth 2.0 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Desktop application" as application type
4. Give it a name (e.g., "Gmail MCP Server")
5. Click "Create"
6. Download the JSON file
7. Rename it to `gcp-oauth.keys.json`

### 1.4 Configure OAuth Consent Screen
1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" (unless you have Google Workspace)
3. Fill in required fields:
   - App name: "Gmail MCP Server"
   - User support email: your email
   - Developer contact: your email
4. Add your email as a test user in "Test users" section
5. Save and continue

## Step 2: Install Credentials

### 2.1 Create Gmail MCP Directory
```bash
mkdir -p ~/.gmail-mcp
```

### 2.2 Move Credentials File
```bash
# Move your downloaded gcp-oauth.keys.json to the secure directory
mv gcp-oauth.keys.json ~/.gmail-mcp/
```

## Step 3: Authenticate

### 3.1 Run Authentication
```bash
npx @gongrzhe/server-gmail-autoauth-mcp auth
```

This will:
- Open your browser for Google authentication
- Save credentials as `~/.gmail-mcp/credentials.json`

## Step 4: Configure in Cursor

### 4.1 Update MCP Configuration
Add to your `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token_here"
      }
    },
    "puppeteer-mcp-claude": {
      "command": "node",
      "args": [
        "/Users/vishwarajapathi/mcp-servers/node_modules/puppeteer-mcp-claude/dist/index.js"
      ],
      "cwd": "/Users/vishwarajapathi/mcp-servers/node_modules/puppeteer-mcp-claude",
      "env": {
        "NODE_ENV": "production"
      }
    },
    "dockerhub": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "HUB_PAT_TOKEN",
        "mcp/dockerhub@sha256:6d15361c655580c7aad72b0152daef9208b466577e794361f64904aa974f5e67",
        "--transport=stdio",
        "--username=vishwa86"
      ],
      "env": {
        "HUB_PAT_TOKEN": "your_docker_hub_token_here"
      }
    },
    "gmail": {
      "command": "npx",
      "args": [
        "@gongrzhe/server-gmail-autoauth-mcp"
      ]
    }
  }
}
```

## Step 5: Test the Integration

After restarting Cursor, you should be able to:
- Send emails through Claude
- Read your Gmail messages
- Search emails
- Manage labels
- Handle attachments
- And much more!

## Troubleshooting

### Common Issues:
1. **"OAuth keys file not found"** - Make sure `gcp-oauth.keys.json` is in `~/.gmail-mcp/`
2. **"Access blocked"** - Add your email as a test user in OAuth consent screen
3. **"Invalid credentials"** - Re-download credentials from Google Cloud Console
4. **"Permission denied"** - Check that Gmail API is enabled in your project

### Security Notes:
- Credentials are stored securely in `~/.gmail-mcp/`
- Never commit `gcp-oauth.keys.json` or `credentials.json` to version control
- The server uses OAuth2 with offline access for persistent authentication


