# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-06-17

### Added
- Initial release of Credential Manager MCP server
- Secure local credential storage using JSON backend
- Complete CRUD operations for credentials
- Tool functions:
  - `list_credentials()` - List all credentials (tokens hidden)
  - `get_credential_details(credential_id)` - Get full credential details
  - `add_credential()` - Add new credentials
  - `update_credential()` - Update existing credentials
  - `delete_credential()` - Delete credentials
  - `search_credentials()` - Search and filter credentials
- Resource endpoints:
  - `credential://store/info` - Store information
  - `credential://help` - Help documentation
- Auto-generated UUID4 credential IDs
- Flexible expiration date handling
- Comprehensive test suite
- Modern Python project setup with uv
- MIT license
- Complete documentation and setup guides
- GitHub Actions CI workflow
- Issue templates and contributing guidelines

### Security
- Access tokens are hidden in credential listings for security
- Local storage only - no network transmission of credentials
- Comprehensive .gitignore to prevent credential file commits 