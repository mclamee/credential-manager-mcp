# 🔐 Credential Manager MCP Server

[![Test](https://github.com/yourusername/credential-manager-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/yourusername/credential-manager-mcp/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A FastMCP server for securely managing API credentials locally through the Model Context Protocol (MCP). Store, retrieve, and manage your API tokens with security-first design.

## 🔧 Key Features

1. **Secure local storage** - Credentials stored in JSON format
2. **Complete CRUD operations** - Create, Read, Update, Delete credentials  
3. **Security-focused design** - Access tokens hidden in listings
4. **Search functionality** - Filter by app name or username
5. **Resource endpoints** - Store info and help documentation
6. **Auto-generated IDs** - UUID4 for unique credential identification
7. **Flexible expiration** - Date strings or "never"

## 📁 Project Structure
```
credential-manager-mcp/
├── credential_manager.py           # Main MCP server
├── test_credential_manager.py      # Comprehensive test suite
├── pyproject.toml                  # Modern Python project configuration
├── uv.lock                         # Locked dependencies for reproducibility
├── example_usage.py                # Usage demonstration script
├── .github/workflows/test.yml      # GitHub Actions CI workflow
├── .gitignore                      # Security exclusions
├── LICENSE                         # MIT license
└── docs/                           # Documentation
    ├── README.md                   # This file
    ├── SETUP.md                    # Quick setup guide
    ├── CHANGELOG.md                # Version history
    └── CONTRIBUTING.md             # Contributor guidelines
```

## 🚀 Quick Start

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup project
cd credential-manager-mcp
uv sync                                      # Install dependencies
uv run python test_credential_manager.py    # Run tests  
uv run python credential_manager.py         # Start the server
```

## 🔗 Claude Desktop Integration

Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "credential-manager": {
      "command": "uv",
      "args": ["run", "python", "/path/to/credential-manager-mcp/credential_manager.py"]
    }
  }
}
```

## 🛠 Available Tools

- `list_credentials()` - List all credentials (tokens hidden for security)
- `get_credential_details(credential_id)` - Get full details including access token
- `add_credential(app, base_url, access_token, [user_name], [expires])` - Add new credential  
- `update_credential(credential_id, [fields...])` - Update existing credential
- `delete_credential(credential_id)` - Delete a credential
- `search_credentials([app_filter], [user_filter])` - Search credentials

## 📚 Available Resources

- `credential://store/info` - Store information and metadata
- `credential://help` - Comprehensive help documentation

## 💡 Example Usage

```python
# Add a credential
add_credential(
    app="GitHub",
    base_url="https://api.github.com", 
    access_token="ghp_xxxxxxxxxxxxxxxxxxxx",
    user_name="myusername",
    expires="2024-12-31"
)

# Search credentials
search_credentials(app_filter="github")

# Get full details (including token)
get_credential_details("credential-id-here")
```

## 🔒 Security Features

- **Local storage only** - No network transmission of credentials
- **Hidden tokens** - Access tokens hidden when listing credentials
- **Secure defaults** - Comprehensive .gitignore prevents credential commits
- **Permission control** - Set file permissions on credentials.json as needed

## 📖 More Information

- See [SETUP.md](SETUP.md) for detailed setup instructions
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines  
- Check [CHANGELOG.md](CHANGELOG.md) for version history
- Run `uv run python example_usage.py` for a complete demo

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details. 