import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Union
from pathlib import Path

from fastmcp import FastMCP
from pydantic import BaseModel

# Data models
class Credential(BaseModel):
    app: str
    id: str
    base_url: str
    access_token: str
    user_name: Optional[str] = None
    expires: Union[str, None] = None  # Can be date string or "never"

class CredentialStore:
    def __init__(self, store_path: str = "credentials.json"):
        self.store_path = Path(store_path)
        self.credentials: Dict[str, Credential] = {}
        self.load_credentials()
    
    def load_credentials(self):
        """Load credentials from JSON file"""
        if self.store_path.exists():
            try:
                with open(self.store_path, 'r') as f:
                    data = json.load(f)
                    self.credentials = {
                        cred_id: Credential(**cred_data) 
                        for cred_id, cred_data in data.items()
                    }
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not load credentials file: {e}")
                self.credentials = {}
    
    def save_credentials(self):
        """Save credentials to JSON file"""
        try:
            # Ensure directory exists
            self.store_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to dict for JSON serialization
            data = {
                cred_id: cred.model_dump() 
                for cred_id, cred in self.credentials.items()
            }
            
            with open(self.store_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving credentials: {e}")
    
    def add_credential(self, app: str, base_url: str, access_token: str, 
                      user_name: Optional[str] = None, expires: Optional[str] = None) -> str:
        """Add a new credential and return its ID"""
        cred_id = str(uuid.uuid4())
        credential = Credential(
            app=app,
            id=cred_id,
            base_url=base_url,
            access_token=access_token,
            user_name=user_name,
            expires=expires or "never"
        )
        self.credentials[cred_id] = credential
        self.save_credentials()
        return cred_id
    
    def get_credential(self, cred_id: str) -> Optional[Credential]:
        """Get a credential by ID"""
        return self.credentials.get(cred_id)
    
    def list_credentials(self) -> List[Dict]:
        """List all credentials (without access tokens for security)"""
        return [
            {
                "id": cred.id,
                "app": cred.app,
                "base_url": cred.base_url,
                "user_name": cred.user_name,
                "expires": cred.expires
            }
            for cred in self.credentials.values()
        ]
    
    def update_credential(self, cred_id: str, **updates) -> bool:
        """Update a credential"""
        if cred_id not in self.credentials:
            return False
        
        credential = self.credentials[cred_id]
        for key, value in updates.items():
            if hasattr(credential, key):
                setattr(credential, key, value)
        
        self.save_credentials()
        return True
    
    def delete_credential(self, cred_id: str) -> bool:
        """Delete a credential"""
        if cred_id in self.credentials:
            del self.credentials[cred_id]
            self.save_credentials()
            return True
        return False

# Initialize the credential store
store = CredentialStore()

# Create FastMCP server
mcp = FastMCP(name="Credential Manager")

@mcp.tool
def list_credentials() -> dict:
    """List all stored credentials (access tokens are hidden for security)"""
    credentials = store.list_credentials()
    return {
        "credentials": credentials,
        "count": len(credentials)
    }

@mcp.tool
def get_credential_details(credential_id: str) -> dict:
    """Get detailed information about a specific credential including the access token"""
    credential = store.get_credential(credential_id)
    if not credential:
        return {"error": f"Credential with ID {credential_id} not found"}
    
    return credential.model_dump()

@mcp.tool
def add_credential(app: str, base_url: str, access_token: str, 
                  user_name: Optional[str] = None, expires: Optional[str] = None) -> dict:
    """Add a new credential to the store"""
    try:
        cred_id = store.add_credential(app, base_url, access_token, user_name, expires)
        return {
            "success": True,
            "credential_id": cred_id,
            "message": f"Credential for {app} added successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool
def update_credential(credential_id: str, app: Optional[str] = None, 
                     base_url: Optional[str] = None, access_token: Optional[str] = None,
                     user_name: Optional[str] = None, expires: Optional[str] = None) -> dict:
    """Update an existing credential"""
    updates = {}
    if app is not None:
        updates["app"] = app
    if base_url is not None:
        updates["base_url"] = base_url
    if access_token is not None:
        updates["access_token"] = access_token
    if user_name is not None:
        updates["user_name"] = user_name
    if expires is not None:
        updates["expires"] = expires
    
    if not updates:
        return {"error": "No updates provided"}
    
    success = store.update_credential(credential_id, **updates)
    if success:
        return {
            "success": True,
            "message": f"Credential {credential_id} updated successfully"
        }
    else:
        return {
            "success": False,
            "error": f"Credential with ID {credential_id} not found"
        }

@mcp.tool
def delete_credential(credential_id: str) -> dict:
    """Delete a credential from the store"""
    success = store.delete_credential(credential_id)
    if success:
        return {
            "success": True,
            "message": f"Credential {credential_id} deleted successfully"
        }
    else:
        return {
            "success": False,
            "error": f"Credential with ID {credential_id} not found"
        }

@mcp.tool
def search_credentials(app_filter: Optional[str] = None, user_filter: Optional[str] = None) -> dict:
    """Search credentials by app name or username"""
    credentials = store.list_credentials()
    
    if app_filter:
        credentials = [c for c in credentials if app_filter.lower() in c["app"].lower()]
    
    if user_filter and user_filter.strip():
        credentials = [c for c in credentials if c["user_name"] and user_filter.lower() in c["user_name"].lower()]
    
    return {
        "credentials": credentials,
        "count": len(credentials),
        "filters": {
            "app": app_filter,
            "user": user_filter
        }
    }

@mcp.resource("credential://store/info")
def get_store_info() -> dict:
    """Provides information about the credential store"""
    return {
        "store_path": str(store.store_path.absolute()),
        "total_credentials": len(store.credentials),
        "store_exists": store.store_path.exists(),
        "last_modified": datetime.fromtimestamp(store.store_path.stat().st_mtime).isoformat() if store.store_path.exists() else None
    }

@mcp.resource("credential://help")
def get_help() -> str:
    """Provides help information about using the credential manager"""
    return """
Credential Manager Help
======================

This MCP server helps you manage API credentials securely. Here are the available tools:

1. list_credentials() - List all stored credentials (tokens hidden)
2. get_credential_details(credential_id) - Get full details including access token
3. add_credential(app, base_url, access_token, [user_name], [expires]) - Add new credential
4. update_credential(credential_id, [fields...]) - Update existing credential
5. delete_credential(credential_id) - Delete a credential
6. search_credentials([app_filter], [user_filter]) - Search credentials

Credential fields:
- app: The target application name
- id: Auto-generated unique identifier
- base_url: The application's base URL
- access_token: The API token/key
- user_name: Optional username
- expires: Expiration date string or "never"

Examples:
- add_credential("GitHub", "https://api.github.com", "ghp_xxxx", "myuser", "2024-12-31")
- search_credentials(app_filter="github")
- get_credential_details("credential-id-here")

Security Note: Credentials are stored locally in credentials.json
"""

def main():
    """Main entry point for the credential manager MCP server"""
    mcp.run()

if __name__ == "__main__":
    main() 