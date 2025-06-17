#!/usr/bin/env python3
"""
Test runner script for credential-manager-mcp

This script provides convenient ways to run tests locally.
"""

import subprocess
import sys
import os

def run_pytest():
    """Run tests using pytest"""
    print("🧪 Running tests with pytest...")
    try:
        result = subprocess.run(["uv", "run", "pytest", "test/", "-v"], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Pytest failed with exit code {e.returncode}")
        return False

def run_direct():
    """Run tests directly (backward compatibility)"""
    print("🔄 Running tests directly...")
    try:
        result = subprocess.run(["uv", "run", "python", "test/test_credential_manager.py"], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Direct test failed with exit code {e.returncode}")
        return False

def main():
    """Main test runner"""
    print("🔐 Credential Manager Test Runner")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--direct":
        success = run_direct()
    else:
        success = run_pytest()
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 