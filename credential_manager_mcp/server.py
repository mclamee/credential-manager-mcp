import json
import os
import uuid
import fcntl
from datetime import datetime
from typing import Dict, List, Optional, Union
from pathlib import Path
from collections import Counter

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
    def __init__(self, store_path: str = "credentials.json", read_only: bool = True):
        self.store_path = Path(store_path)
        self.read_only = read_only
        self._last_modified = None
        self.credentials: Dict[str, Credential] = {}
        self._ensure_file_exists()
        self.load_credentials()
    
    def _ensure_file_exists(self):
        """Ensure the credentials file exists"""
        if not self.store_path.exists():
            if self.read_only:
                # In read-only mode, create an empty file if it doesn't exist
                self.store_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.store_path, 'w') as f:
                    json.dump({}, f)
            else:
                self.store_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.store_path, 'w') as f:
                    json.dump({}, f)
    
    def _should_reload(self) -> bool:
        """Check if file has been modified since last load"""
        if not self.store_path.exists():
            return True
        
        current_mtime = self.store_path.stat().st_mtime
        if self._last_modified is None or current_mtime != self._last_modified:
            self._last_modified = current_mtime
            return True
        return False
    
    def load_credentials(self, force: bool = False):
        """Load credentials from JSON file if modified or forced"""
        if not force and not self._should_reload():
            return
            
        if self.store_path.exists():
            try:
                with open(self.store_path, 'r') as f:
                    # Use file locking for safe reading
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                    try:
                        data = json.load(f)
                        self.credentials = {
                            cred_id: Credential(**cred_data) 
                            for cred_id, cred_data in data.items()
                        }
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not load credentials file: {e}")
                self.credentials = {}
    
    def save_credentials(self):
        """Save credentials to JSON file with file locking"""
        if self.read_only:
            raise RuntimeError("Cannot save credentials in read-only mode")
            
        try:
            # Ensure directory exists
            self.store_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to dict for JSON serialization
            data = {
                cred_id: cred.model_dump() 
                for cred_id, cred in self.credentials.items()
            }
            
            # Use file locking for safe writing
            with open(self.store_path, 'w') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    json.dump(data, f, indent=2)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            # Update our modification time tracking
            self._last_modified = self.store_path.stat().st_mtime
        except Exception as e:
            print(f"Error saving credentials: {e}")
    
    def add_credential(self, app: str, base_url: str, access_token: str, 
                      user_name: Optional[str] = None, expires: Optional[str] = None) -> str:
        """Add a new credential and return its ID"""
        if self.read_only:
            raise RuntimeError("Cannot add credentials in read-only mode")
            
        # Reload to ensure we have latest data from other instances
        self.load_credentials()
        
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
        # Always reload to ensure fresh data
        self.load_credentials()
        return self.credentials.get(cred_id)
    
    def list_credentials(self) -> List[Dict]:
        """List all credentials with minimal essential data"""
        # Always reload to ensure fresh data
        self.load_credentials()
        
        # Count apps to determine if we need to show usernames
        app_counts = Counter(cred.app for cred in self.credentials.values())
        
        result = []
        for cred in self.credentials.values():
            item = {
                "id": cred.id,
                "app": cred.app
            }
            
            # Only include username if there are multiple credentials for the same app
            if app_counts[cred.app] > 1 and cred.user_name:
                item["user_name"] = cred.user_name
                
            result.append(item)
        
        return result
    
    def update_credential(self, cred_id: str, **updates) -> bool:
        """Update a credential"""
        if self.read_only:
            raise RuntimeError("Cannot update credentials in read-only mode")
            
        # Reload to ensure we have latest data from other instances
        self.load_credentials()
        
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
        if self.read_only:
            raise RuntimeError("Cannot delete credentials in read-only mode")
            
        # Reload to ensure we have latest data from other instances
        self.load_credentials()
        
        if cred_id in self.credentials:
            del self.credentials[cred_id]
            self.save_credentials()
            return True
        return False

# Get read-only mode from environment variable or default to True
READ_ONLY_MODE = os.getenv("CREDENTIAL_MANAGER_READ_ONLY", "true").lower() in ("true", "1", "yes")

# Initialize the credential store
store = CredentialStore(read_only=READ_ONLY_MODE)

# Create FastMCP server
mcp = FastMCP(name="Credential Manager")

@mcp.tool
def list_credentials() -> dict:
    """List all stored credentials with essential data (id, app name, and username only if multiple apps)"""
    credentials = store.list_credentials()
    return {
        "credentials": credentials,
        "count": len(credentials),
        "mode": "read-only" if store.read_only else "read-write"
    }

@mcp.tool
def get_credential_details(credential_id: str) -> dict:
    """Get detailed information about a specific credential including the access token"""
    credential = store.get_credential(credential_id)
    if not credential:
        return {"error": f"Credential with ID {credential_id} not found"}
    
    return credential.model_dump()

# Only register write operations if not in read-only mode
if not READ_ONLY_MODE:
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
        
        try:
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
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @mcp.tool
    def delete_credential(credential_id: str) -> dict:
        """Delete a credential from the store"""
        try:
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
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

@mcp.resource("credential://store/info")
def get_store_info() -> dict:
    """Provides information about the credential store"""
    # Reload to ensure fresh data
    store.load_credentials()
    return {
        "store_path": str(store.store_path.absolute()),
        "total_credentials": len(store.credentials),
        "store_exists": store.store_path.exists(),
        "read_only_mode": store.read_only,
        "last_modified": datetime.fromtimestamp(store.store_path.stat().st_mtime).isoformat() if store.store_path.exists() else None
    }

@mcp.resource("credential://help")
def get_help() -> str:
    """Provides help information about using the credential manager"""
    mode_text = "read-only" if store.read_only else "read-write"
    tools_list = ["1. list_credentials() - List stored credentials (essential data only)"]
    tools_list.append("2. get_credential_details(credential_id) - Get full details including access token")
    
    if not store.read_only:
        tools_list.extend([
            "3. add_credential(app, base_url, access_token, [user_name], [expires]) - Add new credential",
            "4. update_credential(credential_id, [fields...]) - Update existing credential",
            "5. delete_credential(credential_id) - Delete a credential"
        ])
    
    tools_text = "\n".join(tools_list)
    
    return f"""
Credential Manager Help
======================

This MCP server helps you manage API credentials securely. 
Current mode: {mode_text}

Available tools:
{tools_text}

Credential fields:
- app: The target application name
- id: Auto-generated unique identifier  
- base_url: The application's base URL
- access_token: The API token/key
- user_name: Optional username (shown only when multiple credentials for same app)
- expires: Expiration date string or "never"

Examples:
- list_credentials()
- get_credential_details("credential-id-here")
{'- add_credential("GitHub", "https://api.github.com", "ghp_xxxx", "myuser", "2024-12-31")' if not store.read_only else ''}

Security Features:
- Local storage only in credentials.json
- Multi-instance support with file locking
- Read-only mode for security (set CREDENTIAL_MANAGER_READ_ONLY=false to enable writes)
"""

def main():
    """Main entry point for the credential manager MCP server"""
    print(f"Starting Credential Manager in {'read-only' if READ_ONLY_MODE else 'read-write'} mode")
    mcp.run()

if __name__ == "__main__":
    main() 