#!/usr/bin/env python3
"""
Test script for the credential manager MCP server
"""

import asyncio
import json
import pytest
from fastmcp import Client
import credential_manager

@pytest.mark.asyncio
async def test_credential_manager():
    """Test the credential manager server"""
    print("🧪 Testing Credential Manager MCP Server")
    print("=" * 50)
    
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
        result_data = json.loads(result[0].text)
        assert result_data.get("success"), f"Failed to add credential: {result_data}"
        
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

def test_multi_instance_sharing():
    """Test that multiple instances share credential changes"""
    import tempfile
    import os
    from credential_manager import CredentialStore
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
        test_file = tmp_file.name
        json.dump({}, tmp_file)
    
    try:
        print("🔄 Testing Multi-Instance Credential Sharing")
        print("=" * 50)
        
        # Create two separate instances pointing to the same file
        store1 = CredentialStore(test_file)
        store2 = CredentialStore(test_file)
        
        print(f"📁 Using test file: {test_file}")
        
        # Add credential using store1
        print("\n1️⃣ Adding credential via Store Instance 1...")
        cred_id = store1.add_credential(
            app="Test App",
            base_url="https://api.test.com",
            access_token="test-token-123",
            user_name="testuser",
            expires="2025-12-31"
        )
        print(f"✅ Added credential with ID: {cred_id}")
        
        # Check if store2 can see the change
        print("\n2️⃣ Checking if Store Instance 2 can see the new credential...")
        credential_from_store2 = store2.get_credential(cred_id)
        
        assert credential_from_store2 is not None, "Store 2 could not find the credential"
        print(f"✅ SUCCESS: Store 2 found the credential!")
        print(f"   App: {credential_from_store2.app}")
        print(f"   User: {credential_from_store2.user_name}")
        
        # Update credential using store2
        print("\n3️⃣ Updating credential via Store Instance 2...")
        success = store2.update_credential(cred_id, app="Updated Test App", user_name="updateduser")
        
        assert success, "Update failed"
        print("✅ Update successful")
        
        # Check if store1 can see the update
        print("\n4️⃣ Checking if Store Instance 1 can see the update...")
        updated_credential = store1.get_credential(cred_id)
        
        assert updated_credential is not None and updated_credential.app == "Updated Test App", "Store 1 did not see the update"
        print(f"✅ SUCCESS: Store 1 sees the updated credential!")
        print(f"   Updated App: {updated_credential.app}")
        print(f"   Updated User: {updated_credential.user_name}")
        
        # Delete credential using store1
        print("\n5️⃣ Deleting credential via Store Instance 1...")
        delete_success = store1.delete_credential(cred_id)
        
        assert delete_success, "Delete failed"
        print("✅ Delete successful")
        
        # Check if store2 can see the deletion
        print("\n6️⃣ Checking if Store Instance 2 can see the deletion...")
        deleted_credential = store2.get_credential(cred_id)
        
        assert deleted_credential is None, "Store 2 still sees the deleted credential"
        print("✅ SUCCESS: Store 2 confirms credential is deleted!")
        
        print("\n🎉 All tests passed! Multi-instance sharing works correctly!")
        
    finally:
        # Clean up the test file
        if os.path.exists(test_file):
            os.unlink(test_file)
            print(f"\n🧹 Cleaned up test file: {test_file}")

if __name__ == "__main__":
    # For running directly (backward compatibility)
    import sys
    
    async def run_async_test():
        await test_credential_manager()
    
    try:
        asyncio.run(run_async_test())
        test_multi_instance_sharing()
        print("\n✅ Credential Manager is ready to use!")
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 