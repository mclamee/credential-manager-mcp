#!/usr/bin/env python3
"""
Test script for the credential manager MCP server
"""

import asyncio
import json
import os
import pytest
from fastmcp import Client
import credential_manager_mcp.server as credential_manager

@pytest.mark.asyncio
async def test_credential_manager_read_only():
    """Test the credential manager server in read-only mode"""
    print("🧪 Testing Credential Manager MCP Server (Read-Only Mode)")
    print("=" * 60)
    
    print("✅ Server imports successfully")
        
    # Create a client for testing
    client = Client(credential_manager.mcp)
    
    async with client:
        print("\n📋 Testing list_credentials...")
        result = await client.call_tool("list_credentials", {})
        print(f"Result: {result[0].text}")
        
        result_data = json.loads(result[0].text)
        assert "credentials" in result_data
        assert "count" in result_data
        assert "mode" in result_data
        assert result_data["mode"] == "read-only"
        
        print("✅ List credentials working correctly")
        
        print("\n📊 Testing store info resource...")
        result = await client.read_resource("credential://store/info")
        print(f"Store info: {result[0].text}")
        
        store_info = json.loads(result[0].text)
        assert "read_only_mode" in store_info
        assert store_info["read_only_mode"] == True
        
        print("\n❓ Testing help resource...")
        result = await client.read_resource("credential://help")
        print("Help resource retrieved successfully")
        
        print("\n🎉 Read-only mode tests passed!")

@pytest.mark.asyncio
async def test_credential_manager_read_write():
    """Test the credential manager server in read-write mode"""
    print("\n🧪 Testing Credential Manager MCP Server (Read-Write Mode)")
    print("=" * 60)
    
    # Set environment variable for read-write mode
    original_env = os.environ.get("CREDENTIAL_MANAGER_READ_ONLY")
    os.environ["CREDENTIAL_MANAGER_READ_ONLY"] = "false"
    
    try:
        # We need to reload the module to pick up the new environment variable
        import importlib
        importlib.reload(credential_manager)
        
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
            
            list_data = json.loads(result[0].text)
            assert list_data["mode"] == "read-write"
            
            # Check that the list contains only essential data
            if list_data["credentials"]:
                cred = list_data["credentials"][-1]  # Get the last added credential
                assert "id" in cred
                assert "app" in cred
                # username should NOT be present since there's only one GitHub credential
                assert "user_name" not in cred or cred["user_name"] is None
                
            print("\n🔍 Testing get_credential_details...")
            result = await client.call_tool("get_credential_details", {
                "credential_id": cred_id
            })
            print(f"Result: {result[0].text}")
            
            detail_data = json.loads(result[0].text)
            assert "access_token" in detail_data
            assert detail_data["app"] == "GitHub"
            
            print("\n🗑️ Testing delete_credential...")
            result = await client.call_tool("delete_credential", {
                "credential_id": cred_id
            })
            print(f"Result: {result[0].text}")
            
            delete_data = json.loads(result[0].text)
            assert delete_data.get("success") == True
            
            print("\n🎉 Read-write mode tests passed!")
            
    finally:
        # Restore original environment
        if original_env is not None:
            os.environ["CREDENTIAL_MANAGER_READ_ONLY"] = original_env
        else:
            os.environ.pop("CREDENTIAL_MANAGER_READ_ONLY", None)

def test_multi_instance_sharing():
    """Test that multiple instances share credential changes"""
    import tempfile
    import os
    from credential_manager_mcp.server import CredentialStore
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
        test_file = tmp_file.name
        json.dump({}, tmp_file)
    
    try:
        print("\n🔄 Testing Multi-Instance Credential Sharing")
        print("=" * 50)
        
        # Create two separate instances pointing to the same file (both in read-write mode)
        store1 = CredentialStore(test_file, read_only=False)
        store2 = CredentialStore(test_file, read_only=False)
        
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
        
        # Test list function with single app (no username shown)
        print("\n3️⃣ Testing list function with single app...")
        list_result = store1.list_credentials()
        assert len(list_result) == 1, f"Expected 1 credential, got {len(list_result)}: {list_result}"
        assert "user_name" not in list_result[0], "Username should not be shown for single app"
        print("✅ Username correctly hidden for single app")
        
        # Add another credential with same app to test username display
        print("\n4️⃣ Adding second credential with same app...")
        cred_id2 = store2.add_credential(
            app="Test App",
            base_url="https://api.test.com",
            access_token="test-token-456",
            user_name="testuser2",
            expires="2025-12-31"
        )
        print(f"✅ Added second credential with ID: {cred_id2}")
        
        # Small delay to ensure file operations complete in CI environment
        import time
        time.sleep(0.1)
        
        # Force both stores to reload to ensure they see all changes
        store1.load_credentials()
        store2.load_credentials()
        
        # Test list function with multiple apps (username should be shown)
        print("\n5️⃣ Testing list function with multiple apps...")
        list_result = store1.list_credentials()
        print(f"   Found {len(list_result)} credentials: {list_result}")
        assert len(list_result) == 2, f"Expected 2 credentials, got {len(list_result)}: {list_result}"
        
        # Verify both credentials have usernames displayed
        found_cred1 = False
        found_cred2 = False
        for item in list_result:
            if item["id"] == cred_id:
                assert "user_name" in item, "Username should be shown when multiple credentials for same app"
                assert item["user_name"] == "testuser"
                found_cred1 = True
            elif item["id"] == cred_id2:
                assert "user_name" in item, "Username should be shown when multiple credentials for same app"
                assert item["user_name"] == "testuser2"
                found_cred2 = True
        
        assert found_cred1, f"Could not find first credential {cred_id} in list"
        assert found_cred2, f"Could not find second credential {cred_id2} in list"
        print("✅ Username correctly shown for multiple apps")
        
        # Clean up
        print("\n6️⃣ Cleaning up test credentials...")
        store1.delete_credential(cred_id)
        store2.delete_credential(cred_id2)
        
        print("\n🎉 All multi-instance tests passed!")
        
    finally:
        # Clean up the test file
        if os.path.exists(test_file):
            os.unlink(test_file)
            print(f"\n🧹 Cleaned up test file: {test_file}")

def test_read_only_mode_protection():
    """Test that read-only mode properly prevents modifications"""
    import tempfile
    from credential_manager_mcp.server import CredentialStore
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
        test_file = tmp_file.name
        json.dump({}, tmp_file)
    
    try:
        print("\n🔒 Testing Read-Only Mode Protection")
        print("=" * 40)
        
        store = CredentialStore(test_file, read_only=True)
        
        # Test that add_credential raises an error
        try:
            store.add_credential("Test", "https://test.com", "token")
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "read-only mode" in str(e)
            print("✅ Add operation properly blocked in read-only mode")
        
        # Test that update_credential raises an error
        try:
            store.update_credential("fake-id", app="New App")
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "read-only mode" in str(e)
            print("✅ Update operation properly blocked in read-only mode")
        
        # Test that delete_credential raises an error
        try:
            store.delete_credential("fake-id")
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "read-only mode" in str(e)
            print("✅ Delete operation properly blocked in read-only mode")
        
        # Test that read operations still work
        credentials = store.list_credentials()
        assert isinstance(credentials, list)
        print("✅ Read operations work correctly in read-only mode")
        
        print("\n🎉 Read-only protection tests passed!")
        
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)

if __name__ == "__main__":
    # For running directly (backward compatibility)
    import sys
    
    async def run_async_tests():
        await test_credential_manager_read_only()
        await test_credential_manager_read_write()
    
    try:
        asyncio.run(run_async_tests())
        test_multi_instance_sharing()
        test_read_only_mode_protection()
        print("\n✅ All tests passed! Credential Manager is ready to use!")
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 