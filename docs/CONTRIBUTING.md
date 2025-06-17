# Contributing to Credential Manager MCP

Thank you for your interest in contributing to the Credential Manager MCP server! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment:
   ```bash
   cd credential-manager-mcp
   uv sync
   ```

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management:

```bash
# Install dependencies
uv sync

# Run tests
uv run python test_credential_manager.py

# Run the server
uv run python credential_manager.py

# Run with development tools
uv run fastmcp dev credential_manager.py
```

## Making Changes

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```

2. Make your changes following these guidelines:
   - Follow Python PEP 8 style guidelines
   - Add docstrings to new functions and classes
   - Update tests if you modify existing functionality
   - Add new tests for new features

3. Test your changes:
   ```bash
   uv run python test_credential_manager.py
   ```

4. Commit your changes with a clear message:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

## Pull Request Process

1. Push your branch to your fork
2. Create a pull request against the main branch
3. Provide a clear description of what your changes do
4. Include any relevant issue numbers

## Code Style

- Use type hints where appropriate
- Follow existing code patterns and conventions
- Keep functions focused and well-documented
- Use meaningful variable and function names

## Testing

- All changes should be tested
- Run the existing test suite to ensure nothing breaks
- Add new tests for new functionality
- Test both success and error cases

## Security Considerations

Since this project handles credentials:
- Never commit actual credentials or sensitive data
- Test with dummy/fake credentials only
- Be mindful of security best practices
- Report security issues privately to the maintainers

## Questions?

Feel free to open an issue for discussion before starting work on major features.

## License

By contributing, you agree that your contributions will be licensed under the MIT License. 