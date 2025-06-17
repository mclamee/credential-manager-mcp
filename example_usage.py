#!/usr/bin/env python3
"""
Example usage of the Credential Manager MCP Server

This script demonstrates how to interact with the credential manager
programmatically using the FastMCP client.
"""

import asyncio
from fastmcp import Client
import credential_manager

async def example_usage():
    """Demonstrate basic credential management operations"""
    print("🔐 Credential Manager Example Usage")
    print("=" * 40)
    
    # Create a client to interact with the server
    client = Client(credential_manager.mcp)
    
    async with client:
        print("\n📝 Adding a sample credential...")
        
        # Add a credential
        result = await client.call_tool("add_credential", {
            "app": "Example API",
            "base_url": "https://api.example.com",
            "access_token": "sk-example-token-12345",
            "user_name": "demo-user",
            "expires": "2025-12-31"
        })
        print(f"✅ Add result: {result[0].text}")
        
        print("\n📋 Listing all credentials...")
        
        # List credentials (tokens hidden for security)
        result = await client.call_tool("list_credentials", {})
        print(f"📝 Credentials: {result[0].text}")
        
        print("\n🔍 Searching for credentials...")
        
        # Search credentials
        result = await client.call_tool("search_credentials", {
            "app_filter": "example"
        })
        print(f"🔎 Search results: {result[0].text}")
        
        print("\n📊 Getting store information...")
        
        # Get store info via resource
        result = await client.read_resource("credential://store/info")
        print(f"📈 Store info: {result[0].text}")
        
        print("\n🗑️ Cleaning up example data...")
        
        # Clean up - delete the test credential
        # Extract the credential ID from the earlier add result
        import json
        add_data = json.loads(result[0].text)
        if "credentials" in add_data and len(add_data["credentials"]) > 0:
            cred_id = add_data["credentials"][0]["id"]
            result = await client.call_tool("delete_credential", {
                "credential_id": cred_id
            })
            print(f"🗑️ Delete result: {result[0].text}")
        
        print("\n✅ Example completed successfully!")

if __name__ == "__main__":
    asyncio.run(example_usage()) 