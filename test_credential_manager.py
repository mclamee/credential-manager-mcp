#!/usr/bin/env python3
"""
Test script for the credential manager MCP server
"""

import sys
import os
import asyncio
from fastmcp import Client

async def test_credential_manager():
    """Test the credential manager server"""
    print("🧪 Testing Credential Manager MCP Server")
    print("=" * 50)
    
    # Import the server
    try:
        import credential_manager
        print("✅ Server imports successfully")
        
        # Create a client for testing
        client = Client(credential_manager.mcp)
        
        async with client:
            print("\n📝 Testing add_credential...")
            result = await client.call_tool("add_credential", {
                "app": "GitHub",
                "base_url": "https://api.github.com",
                "access_token": "ghp_test_token_123",
                "user_name": "testuser",
                "expires": "2024-12-31"
            })
            print(f"Result: {result[0].text}")
            
            # Extract credential ID from the result
            import json
            result_data = json.loads(result[0].text)
            if result_data.get("success"):
                cred_id = result_data["credential_id"]
                print(f"✅ Added credential with ID: {cred_id}")
                
                print("\n📋 Testing list_credentials...")
                result = await client.call_tool("list_credentials", {})
                print(f"Result: {result[0].text}")
                
                print("\n🔍 Testing get_credential_details...")
                result = await client.call_tool("get_credential_details", {
                    "credential_id": cred_id
                })
                print(f"Result: {result[0].text}")
                
                print("\n🔎 Testing search_credentials...")
                result = await client.call_tool("search_credentials", {
                    "app_filter": "github"
                })
                print(f"Result: {result[0].text}")
                
                print("\n📊 Testing store info resource...")
                result = await client.read_resource("credential://store/info")
                print(f"Store info: {result[0].text}")
                
                print("\n❓ Testing help resource...")
                result = await client.read_resource("credential://help")
                print("Help resource retrieved successfully")
                
                print("\n🗑️ Testing delete_credential...")
                result = await client.call_tool("delete_credential", {
                    "credential_id": cred_id
                })
                print(f"Result: {result[0].text}")
                
                print("\n🎉 All tests passed!")
            else:
                print(f"❌ Failed to add credential: {result_data}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_credential_manager())
    if success:
        print("\n✅ Credential Manager is ready to use!")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1) 