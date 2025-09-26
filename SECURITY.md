# Security Guidelines

This document outlines security best practices for the Gmail CLI project.

## 🔒 Credential Management

### ⚠️ **CRITICAL: Never Commit Credentials**

**NEVER** commit the following files to version control:
- `credentials.json` - Google API credentials
- `token.json` - OAuth2 access tokens
- Any `.env` files with sensitive data
- Private keys (`.pem`, `.key`, `.p12` files)

### ✅ **Safe Practices**

1. **Use `.gitignore`**: The project includes comprehensive `.gitignore` rules
2. **Environment Variables**: Use environment variables for sensitive data
3. **Local Storage**: Store credentials in a secure local directory
4. **Token Rotation**: Regularly rotate access tokens

## 🛡️ **Security Features**

### OAuth2 Authentication
- **No Password Storage**: Uses secure token-based authentication
- **Scoped Permissions**: Only requests necessary Gmail permissions
- **Token Encryption**: Local tokens are encrypted and secure

### Data Handling
- **Local Processing**: All operations happen locally
- **No Data Logging**: No email content is logged or stored
- **Secure Storage**: Credentials stored in encrypted format

## 📁 **File Structure**

```
gmail-cli/
├── credentials.json     # ❌ NEVER COMMIT - Google API credentials
├── token.json          # ❌ NEVER COMMIT - OAuth2 tokens
├── .env                # ❌ NEVER COMMIT - Environment variables
├── data/               # ✅ Safe - User data directory
└── src/                # ✅ Safe - Source code
```

## 🔧 **Setup Instructions**

### 1. Download Credentials
```bash
# Download from Google Cloud Console
# Save as credentials.json (DO NOT COMMIT)
```

### 2. First Authentication
```bash
# This creates token.json (DO NOT COMMIT)
gmail auth
```

### 3. Verify Security
```bash
# Check that credentials are not tracked
git status
git ls-files | grep -E "(token|credentials)\.json"
```

## 🚨 **If Credentials Are Accidentally Committed**

### Immediate Actions:
1. **Revoke Credentials**: Go to Google Cloud Console and revoke the credentials
2. **Remove from Git**: Use `git filter-branch` or BFG Repo-Cleaner
3. **Force Push**: Update the remote repository
4. **Generate New Credentials**: Create new credentials in Google Cloud Console

### Commands:
```bash
# Remove from git history (DANGEROUS - use with caution)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch credentials.json token.json' \
  --prune-empty --tag-name-filter cat -- --all

# Force push to update remote
git push origin --force --all
```

## 🔍 **Security Checklist**

Before committing code:
- [ ] No `credentials.json` in repository
- [ ] No `token.json` in repository
- [ ] No `.env` files with secrets
- [ ] No hardcoded API keys or tokens
- [ ] All sensitive data uses environment variables
- [ ] `.gitignore` includes all credential patterns

## 🛠️ **Development Environment**

### Local Development
```bash
# Create secure directory for credentials
mkdir -p ~/.gmail-cli
cp credentials.json ~/.gmail-cli/
cp token.json ~/.gmail-cli/

# Update code to use secure path
export GMAIL_CREDENTIALS_PATH=~/.gmail-cli/credentials.json
export GMAIL_TOKEN_PATH=~/.gmail-cli/token.json
```

### Docker Development
```bash
# Mount credentials as volumes (never copy into image)
docker run -v ~/.gmail-cli:/app/credentials vishwa86/gmail-cli:latest
```

## 📚 **Additional Resources**

- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [OAuth2 Security Guidelines](https://tools.ietf.org/html/rfc6749)
- [Git Security Best Practices](https://git-scm.com/docs/gitignore)

## 🆘 **Security Issues**

If you discover a security vulnerability:
1. **DO NOT** create a public issue
2. Email security concerns to: security@example.com
3. Include detailed information about the vulnerability
4. Allow time for response before public disclosure

## 📝 **Security Updates**

This document is regularly updated. Check for updates before each release.

---

**Remember: Security is everyone's responsibility. When in doubt, ask for help.**
