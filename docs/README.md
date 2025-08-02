# Documentation

This directory contains the comprehensive documentation for Egile MCP Client, built using Sphinx and hosted on ReadTheDocs.

## Building Documentation

### Prerequisites

```bash
# Install documentation dependencies
pip install -r requirements.txt

# Or using Poetry
poetry install --with docs
```

### Build Commands

```bash
# Build HTML documentation
make html

# Build and serve locally
make serve

# Clean build directory
make clean

# Live reload during development
make live

# Check for broken links
make linkcheck
```

### Documentation Structure

- `index.rst` - Main documentation index
- `installation.md` - Installation guide
- `quickstart.md` - Quick start tutorial
- `configuration.md` - Configuration reference
- `usage.md` - Comprehensive usage guide
- `architecture.md` - System architecture documentation
- `api.rst` - API reference
- `contributing.md` - Contributing guidelines
- `troubleshooting.md` - Troubleshooting guide
- `changelog.md` - Project changelog

### Configuration

- `conf.py` - Sphinx configuration
- `requirements.txt` - Documentation dependencies
- `Makefile` - Build automation
- `.readthedocs.yaml` - ReadTheDocs configuration

### Viewing Documentation

After building, open `_build/html/index.html` in your browser, or run:

```bash
make serve
```

Then visit http://localhost:8000

## ReadTheDocs Integration

This documentation is configured for automatic building on ReadTheDocs. The configuration is in `.readthedocs.yaml` at the project root.

### Features

- **Automatic API Documentation**: Generated from source code docstrings
- **Multiple Formats**: HTML, PDF, and ePub
- **Search Integration**: Full-text search capabilities
- **Cross-references**: Internal linking between sections
- **Code Highlighting**: Syntax highlighting for all examples
- **Responsive Design**: Mobile-friendly documentation

## Contributing to Documentation

When adding new features or making changes:

1. Update relevant documentation files
2. Add new sections as needed
3. Update the table of contents in `index.rst`
4. Build locally to test changes
5. Check for broken links with `make linkcheck`

### Writing Guidelines

- Use clear, concise language
- Include practical examples
- Maintain consistent formatting
- Add cross-references to related sections
- Update the changelog for significant changes
