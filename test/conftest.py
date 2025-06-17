"""
Pytest configuration for credential-manager-mcp tests
"""

import os
import sys
from pathlib import Path

# Add the parent directory to Python path so we can import credential_manager
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root)) 