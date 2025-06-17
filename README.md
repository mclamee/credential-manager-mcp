# Credential Manager MCP Server

A FastMCP server for securely managing API credentials locally. This server allows you to store, retrieve, update, and delete credentials for various applications through the Model Context Protocol (MCP).

## Features

- **Secure local storage**: Credentials stored in a local JSON file
- **CRUD operations**: Create, Read, Update, Delete credentials
- **Search functionality**: Find credentials by app name or username
- **Security-focused**: Access tokens are hidden in listing operations
- **Resource endpoints**: Get store information and help documentation

## Installation

### Using uv (Recommended)

1. Make sure you have [uv](https://docs.astral.sh/uv/) installed:
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Navigate to the project directory and sync dependencies:
```bash
cd credential-manager-mcp
uv sync
```

3. Run the server:
```bash
uv run python credential_manager.py
```

### Alternative: Using pip

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the dependencies:
```bash
pip install fastmcp pydantic
```

3. Run the server:
```bash
python credential_manager.py
```

## MCP Configuration

To use this server with Claude Desktop or other MCP clients, add it to your MCP configuration:

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "credential-manager": {
      "command": "python",
      "args": ["path/to/credential_manager.py"]
    }
  }
}
```

### Using fastmcp CLI

You can also install it using the fastmcp CLI:

```bash
# With uv
uv run fastmcp install credential_manager.py

# Or traditionally
fastmcp install credential_manager.py
```

## Available Tools

### 1. `list_credentials()`
Lists all stored credentials with access tokens hidden for security.

**Returns**: Dictionary with credentials list and count

### 2. `get_credential_details(credential_id: str)`
Retrieves full details of a specific credential including the access token.

**Parameters**:
- `credential_id`: The unique ID of the credential

**Returns**: Complete credential information

### 3. `add_credential(app: str, base_url: str, access_token: str, user_name?: str, expires?: str)`
Adds a new credential to the store.

**Parameters**:
- `app`: The target application name
- `base_url`: The application's base URL
- `access_token`: The API token/key
- `user_name` (optional): Username associated with the credential
- `expires` (optional): Expiration date string or "never" (default)

**Returns**: Success status and generated credential ID

### 4. `update_credential(credential_id: str, ...fields)`
Updates an existing credential.

**Parameters**:
- `credential_id`: The unique ID of the credential
- Any combination of: `app`, `base_url`, `access_token`, `user_name`, `expires`

**Returns**: Success status and message

### 5. `delete_credential(credential_id: str)`
Deletes a credential from the store.

**Parameters**:
- `credential_id`: The unique ID of the credential

**Returns**: Success status and message

### 6. `search_credentials(app_filter?: str, user_filter?: str)`
Searches credentials by app name or username.

**Parameters**:
- `app_filter` (optional): Filter by application name (case-insensitive)
- `user_filter` (optional): Filter by username (case-insensitive)

**Returns**: Filtered credentials list with count

## Available Resources

### `credential://store/info`
Provides information about the credential store including:
- Store file path
- Total number of credentials
- File existence status
- Last modification time

### `credential://help`
Returns comprehensive help documentation for using the credential manager.

## Data Structure

Each credential contains the following fields:

```json
{
  "app": "GitHub",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "base_url": "https://api.github.com",
  "access_token": "ghp_xxxxxxxxxxxxxxxxxxxx",
  "user_name": "myusername",
  "expires": "2024-12-31"
}
```

## Examples

### Adding a GitHub credential:
```python
add_credential(
    app="GitHub",
    base_url="https://api.github.com",
    access_token="ghp_xxxxxxxxxxxxxxxxxxxx",
    user_name="myusername",
    expires="2024-12-31"
)
```

### Searching for GitHub credentials:
```python
search_credentials(app_filter="github")
```

### Getting full credential details:
```python
get_credential_details("550e8400-e29b-41d4-a716-446655440000")
```

## Security Notes

- Credentials are stored locally in `credentials.json`
- Access tokens are hidden when listing credentials
- Use `get_credential_details()` only when you need the actual token
- Consider setting appropriate file permissions on the credentials file
- The server runs locally and doesn't transmit credentials over the network

## Development

To run in development mode with the MCP Inspector:

```bash
# With uv
uv run fastmcp dev credential_manager.py

# Or run tests
uv run python test_credential_manager.py
```

This will start both the server and the MCP Inspector for testing and debugging.

## License

This project is open source and available under the MIT License. 