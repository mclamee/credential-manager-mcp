# 🔐 Credential Manager MCP Server

[![Test](https://github.com/mclamee/credential-manager-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/mclamee/credential-manager-mcp/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A FastMCP server for securely managing API credentials locally through the Model Context Protocol (MCP). Store, retrieve, and manage your API tokens with security-first design and read-only mode by default.

## 🔧 Key Features

1. **Secure local storage** - Credentials stored in JSON format with multi-instance support
2. **Read-only by default** - Safe mode that only allows reading credentials (can be disabled)
3. **Simplified interface** - Essential data only in listings for better security and usability
4. **Smart credential display** - Shows usernames only when needed (multiple credentials per app)
5. **Complete CRUD operations** - Create, Read, Update, Delete credentials (when not in read-only mode)
6. **Resource endpoints** - Store info and help documentation
7. **Auto-generated IDs** - UUID4 for unique credential identification
8. **Flexible expiration** - Date strings or "never"
9. **Multi-instance sharing** - Multiple server instances share credential changes in real-time

## 📁 Project Structure
```
credential-manager-mcp/
├── credential_manager_mcp/          # Main package directory
│   ├── __init__.py                  # Package initialization
│   └── server.py                    # MCP server implementation
├── credential_manager.py            # Standalone server (for development)
├── example_usage.py                 # Usage demonstration script
├── run_tests.py                     # Test runner script
├── pyproject.toml                   # Modern Python project configuration
├── uv.lock                          # Locked dependencies for reproducibility
├── README.md                        # Main documentation
├── LICENSE                          # MIT license
├── .github/workflows/test.yml       # GitHub Actions CI workflow
├── .gitignore                       # Security exclusions
├── test/                            # Test directory
│   ├── __init__.py                  # Test package init
│   ├── conftest.py                  # Pytest configuration
│   └── test_credential_manager.py   # Comprehensive test suite
└── docs/                            # Additional documentation
    ├── CHANGELOG.md                 # Version history
    └── CONTRIBUTING.md              # Contributor guidelines
```

## 🚀 Quick Start

### 📦 Production Use (Recommended)

For normal usage, install and run with `uvx` (no local setup required):

```bash
# Run directly with uvx (installs automatically)
uvx credential-manager-mcp

# Or install and run
uvx install credential-manager-mcp
uvx credential-manager-mcp
```

**Default behavior**: Starts in **read-only mode** for security.

### 🛠️ Development Setup

For development or when you want to run from source:

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup project
git clone https://github.com/mclamee/credential-manager-mcp.git
cd credential-manager-mcp
uv sync --dev                        # Install dependencies including dev tools
```

#### Run Tests
```bash
# Run tests with pytest (recommended)
uv run pytest test/ -v

# Or use the test runner script
uv run python run_tests.py

# Or run tests directly (backward compatibility)
uv run python test/test_credential_manager.py
```

#### Start Development Server
```bash
# Option 1: Run via package entry point (same as production)
uv run credential-manager-mcp

# Option 2: Run standalone file (for debugging/development)
uv run python credential_manager.py

# Option 3: Enable read-write mode
CREDENTIAL_MANAGER_READ_ONLY=false uv run credential-manager-mcp
```

## 🔗 MCP Client Integration

### Production Configuration (uvx)

Add to your MCP client configuration (e.g., Claude Desktop's `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "credential-manager": {
      "command": "uvx",
      "args": ["credential-manager-mcp"]
    }
  }
}
```

### Enable Read-Write Mode

To enable credential modification capabilities:

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

### Development Configuration

For development or running from source:

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

## 🛠 Available Tools

### Read-Only Mode (Default)
- `list_credentials()` - List stored credentials (essential data: id, app name, smart username display)
- `get_credential_details(credential_id)` - Get full details including access token

### Read-Write Mode (CREDENTIAL_MANAGER_READ_ONLY=false)
- `list_credentials()` - List stored credentials (essential data only)
- `get_credential_details(credential_id)` - Get full details including access token
- `add_credential(app, base_url, access_token, [user_name], [expires])` - Add new credential  
- `update_credential(credential_id, [fields...])` - Update existing credential
- `delete_credential(credential_id)` - Delete a credential

## 📚 Available Resources

- `credential://store/info` - Store information and metadata
- `credential://help` - Comprehensive help documentation

## 💡 Example Usage

### Reading Credentials (Always Available)
```python
# List credentials (shows only essential data)
list_credentials()
# Returns: {"credentials": [{"id": "abc...", "app": "GitHub"}], "count": 1, "mode": "read-only"}

# Get full details including access token
get_credential_details("credential-id-here")
```

### Managing Credentials (Read-Write Mode Only)
```python
# Add a credential
add_credential(
    app="GitHub",
    base_url="https://api.github.com", 
    access_token="ghp_xxxxxxxxxxxxxxxxxxxx",
    user_name="myusername",
    expires="2024-12-31"
)

# Update a credential
update_credential("credential-id", access_token="new-token")

# Delete a credential
delete_credential("credential-id")
```

## 🧪 Testing & Development

### Running Tests
```bash
# With pytest (includes both unit and integration tests)
uv run pytest test/ -v

# Run specific test functions
uv run pytest test/test_credential_manager.py::test_credential_manager_read_only -v
uv run pytest test/test_credential_manager.py::test_credential_manager_read_write -v
uv run pytest test/test_credential_manager.py::test_multi_instance_sharing -v

# Use test runner script with options
uv run python run_tests.py          # Default: uses pytest
uv run python run_tests.py --direct # Direct execution for debugging
```

### Development Workflow
```bash
# Install dev dependencies
uv sync --dev

# Run tests frequently during development  
uv run pytest test/ -v

# Run demo script
uv run python example_usage.py

# Test package installation locally
uv build
uvx --from ./dist/credential_manager_mcp-*.whl credential-manager-mcp
```

## 🔒 Security Features

- **Read-only by default** - Prevents accidental credential modification
- **Local storage only** - No network transmission of credentials
- **Essential data display** - Minimal information shown in listings for security
- **Smart username display** - Shows usernames only when multiple credentials exist for same app
- **Secure defaults** - Comprehensive .gitignore prevents credential commits
- **Permission control** - Set file permissions on credentials.json as needed
- **Multi-instance safety** - File locking prevents race conditions between instances

## ⚙️ Configuration

### Environment Variables

- `CREDENTIAL_MANAGER_READ_ONLY` - Set to `false` to enable write operations (default: `true`)

### Read-Only vs Read-Write Mode

**Read-Only Mode (Default)**:
- ✅ List credentials (essential data only)
- ✅ Get credential details
- ❌ Add/Update/Delete credentials
- 🔒 Maximum security

**Read-Write Mode**:
- ✅ All read operations
- ✅ Add/Update/Delete credentials
- ⚠️ Requires explicit enablement

## 📦 Publishing

```bash
# Build the package
uv build

# Publish to PyPI (requires authentication)
uv publish
```

## 📖 More Information

- See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for development guidelines  
- Check [docs/CHANGELOG.md](docs/CHANGELOG.md) for version history
- Run `uv run python example_usage.py` for a complete demo

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details. 