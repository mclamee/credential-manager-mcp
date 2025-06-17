# 🔐 Credential Manager MCP Server

[![Test](https://github.com/mclamee/credential-manager-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/mclamee/credential-manager-mcp/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A secure MCP server for managing API credentials locally. **Read-only by default** with simple JSON storage.

## ✨ Key Features

- 🔒 **Secure by default** - Read-only mode prevents accidental modification
- 📁 **Simple storage** - Fixed location `~/.credential-manager-mcp/credentials.json`
- 🔧 **Easy setup** - Interactive shell script for adding credentials
- 🔄 **Multi-instance safe** - File locking prevents race conditions
- 🎯 **Essential data only** - Minimal information exposure for security

## 🚀 Quick Start

### 1. Configure MCP Client

Add to your MCP client config (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "credential-manager": {
      "command": "uvx",
      "args": ["credential-manager-mcp"],
      "env": {
        "CREDENTIAL_MANAGER_READ_ONLY": "false"
      }
    }
  }
}
```

**Development config** (run from source):
```json
{
  "mcpServers": {
    "credential-manager": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/credential-manager-mcp",
        "run", "credential-manager-mcp"
      ],
      "env": {
        "CREDENTIAL_MANAGER_READ_ONLY": "false"
      }
    }
  }
}
```

### 2. Add Credentials (Shell Script)

```bash
# Interactive mode (recommended)
./add-credential.sh

# Command line mode
./add-credential.sh "GitHub" "https://api.github.com" "ghp_token" "username" "2024-12-31T23:59:59"

# List credentials
./add-credential.sh --list
```

### 3. Run MCP Server (Optional)

```bash
# Production (read-only)
uvx credential-manager-mcp

# Enable write operations
CREDENTIAL_MANAGER_READ_ONLY=false uvx credential-manager-mcp
```

## 🛠 Available Tools

### Read-Only Mode (Default)
- `list_credentials()` - List stored credentials (id, app name only)
- `get_credential_details(credential_id)` - Get full details including token

### Read-Write Mode
All read operations plus:
- `add_credential(app, base_url, access_token, [user_name], [expires])`
- `update_credential(credential_id, [fields...])`
- `delete_credential(credential_id)`

## 📋 Usage Examples

```python
# List credentials
list_credentials()
# Returns: {"credentials": [{"id": "abc...", "app": "GitHub"}], "count": 1}

# Get details
get_credential_details("credential-id")

# Add credential (read-write mode only)
add_credential(
    app="GitHub",
    base_url="https://api.github.com",
    access_token="ghp_xxxxxxxxxxxx",
    user_name="myuser",
    expires="2024-12-31T23:59:59"
)
```

## ⚙️ Configuration

### Storage Location
- **Fixed path**: `~/.credential-manager-mcp/credentials.json`
- **Cross-platform**: Works on Linux, macOS, Windows
- **Easy backup**: Single file location

### Environment Variables
- `CREDENTIAL_MANAGER_READ_ONLY` - Set to `"false"` to enable write operations (default: `"true"`)

### Expiration Format
Must use **ISO datetime format**:
- `"2024-12-31T23:59:59"` ✅ Full ISO datetime
- `"2024-12-31"` ✅ Date only (shell script converts to `T23:59:59`)
- `"never"` ✅ No expiration
- `"Dec 31, 2024"` ❌ Invalid format

## 🧪 Development

```bash
# Setup
git clone https://github.com/mclamee/credential-manager-mcp.git
cd credential-manager-mcp
uv sync --dev

# Test
uv run pytest test/ -v

# Run locally
uv run credential-manager-mcp
```

## 🔒 Security

- **Read-only by default** - Prevents accidental changes
- **Local storage only** - No network transmission
- **Essential data display** - Minimal info in listings
- **File locking** - Multi-instance safety
- **ISO datetime validation** - Consistent date formats

## 🚀 Releases

### Automated Publishing
This project uses automated publishing to PyPI via GitHub releases:

```bash
# Create a new release (requires GitHub CLI)
./scripts/release.sh patch    # 1.0.0 → 1.0.1
./scripts/release.sh minor    # 1.0.0 → 1.1.0  
./scripts/release.sh major    # 1.0.0 → 2.0.0
./scripts/release.sh 1.2.3    # Specific version
```

**What happens automatically:**
1. ✅ Tests run and pass
2. 📦 Package builds successfully  
3. 🏷️ Version tag created
4. 📄 GitHub release published
5. 🚀 PyPI package published automatically

## 📖 Resources

- **Store info**: `credential://store/info`
- **Help**: `credential://help`
- **Docs**: [CONTRIBUTING.md](docs/CONTRIBUTING.md) | [CHANGELOG.md](docs/CHANGELOG.md)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details. 