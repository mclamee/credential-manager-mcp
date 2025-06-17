# Quick Setup Guide

## Project Structure
```
credential-manager-mcp/
├── credential_manager.py      # Main MCP server
├── test_credential_manager.py # Test script
├── pyproject.toml            # Project configuration with dependencies
├── uv.lock                   # Locked dependencies
├── README.md                 # Comprehensive documentation
├── .python-version           # Python version specification
├── .venv/                    # Virtual environment (created by uv)
└── credentials.json          # Storage file (created at runtime)
```

## Quick Start

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Setup the project**:
   ```bash
   cd credential-manager-mcp
   uv sync
   ```

3. **Test the server**:
   ```bash
   uv run python test_credential_manager.py
   ```

4. **Run the server**:
   ```bash
   uv run python credential_manager.py
   ```

## Available Tools

- `list_credentials()` - List all credentials (tokens hidden)
- `get_credential_details(credential_id)` - Get full credential details
- `add_credential(app, base_url, access_token, [user_name], [expires])` - Add new credential
- `update_credential(credential_id, [fields...])` - Update existing credential
- `delete_credential(credential_id)` - Delete a credential
- `search_credentials([app_filter], [user_filter])` - Search credentials

## Resources

- `credential://store/info` - Store information
- `credential://help` - Help documentation

## Integration with Claude Desktop

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

## Development

Run with MCP Inspector:
```bash
uv run fastmcp dev credential_manager.py
``` 