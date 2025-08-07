# PyPI Publishing Setup Guide

This guide explains how to set up and use the GitHub Actions workflow for publishing `egile-mcp-client` to PyPI.

## ⚠️ **IMPORTANT: Version Sync Issue Fixed**

I found and fixed a critical issue:
- `pyproject.toml` had version "0.1.2" 
- `__init__.py` had version "0.1.0"

**Fixed**: Both now show version "0.1.2". Always keep these in sync!

## 🔧 **Pipeline Improvements Made**

### 1. **Added Concurrency Control**
```yaml
concurrency:
  group: publish-${{ github.ref }}
  cancel-in-progress: false
```

### 2. **Enhanced Version Validation**
- Checks if version already exists on PyPI before release
- Prevents accidental republishing of same version

### 3. **Better Test Strategy**
- Runs only core tests (not web tests that need optional dependencies)
- Validates package can be installed and imported
- Tests CLI availability

### 4. **Comprehensive Package Validation**
- `twine check` for package metadata validation
- Install test to verify package works
- CLI functionality test

### 5. **Trusted Publishing Support**
- Uses GitHub's OIDC for secure publishing (no API tokens needed for main PyPI)
- More secure than API tokens

## Prerequisites

### 1. **Set up Trusted Publishing (Recommended)**

For the main PyPI releases, set up trusted publishing:

1. Go to [PyPI](https://pypi.org/manage/account/publishing/)
2. Add a new trusted publisher:
   - **PyPI project name**: `egile-mcp-client`
   - **Owner**: `jpoullet2000`
   - **Repository name**: `egile-mcp-client`
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `pypi` (optional)

### 2. **TestPyPI Setup (for testing)**

For TestPyPI, you still need an API token:
1. Go to [TestPyPI Account Settings](https://test.pypi.org/manage/account/)
2. Generate an API token
3. Add it as `TEST_PYPI_API_TOKEN` in GitHub Secrets

### 3. **Version Management Strategy**

Always update both files when changing version:

```bash
# Update version in pyproject.toml
poetry version patch  # or minor/major

# Update version in __init__.py to match
# Edit egile_mcp_client/__init__.py manually
```

**Or use this helper script:**

```bash
# Create a simple version sync script
cat > update_version.sh << 'EOF'
#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

VERSION=$1
poetry version $VERSION
NEW_VERSION=$(poetry version -s)
sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" egile_mcp_client/__init__.py
echo "Updated version to $NEW_VERSION in both files"
EOF
chmod +x update_version.sh

# Usage:
# ./update_version.sh 0.1.3
```

## Usage

### 1. Automatic Publishing on Release

The workflow automatically triggers when you create a GitHub release:

```bash
# Create a git tag
git tag v0.1.0
git push origin v0.1.0

# Then create a GitHub release from this tag
# The workflow will automatically publish to PyPI
```

### 2. Manual Publishing (Testing)

You can manually trigger the workflow to test publishing:

1. Go to Actions → Publish to PyPI
2. Click "Run workflow"
3. Select target environment:
   - `testpypi` - for testing (recommended first)
   - `pypi` - for production

### 3. Testing with TestPyPI

Before publishing to the main PyPI, test with TestPyPI:

```bash
# Install from TestPyPI to verify
pip install --index-url https://test.pypi.org/simple/ egile-mcp-client
```

## Workflow Features

### Build Stage
- ✅ Runs on Ubuntu latest
- ✅ Uses Python 3.11
- ✅ Installs dependencies with Poetry
- ✅ Runs full test suite
- ✅ Builds the package
- ✅ Validates the built package with `twine check`
- ✅ Uploads build artifacts

### Publishing Stages
- ✅ **Automatic**: Publishes to PyPI on GitHub releases
- ✅ **Manual TestPyPI**: Manual workflow dispatch for testing
- ✅ **Manual PyPI**: Manual workflow dispatch for production
- ✅ Uses GitHub environments for security
- ✅ Downloads artifacts from build stage

## Version Management

### Current Setup
Your `pyproject.toml` contains:
```toml
version = "0.1.0"
```

### Recommended Release Process

1. **Update version in `pyproject.toml`**:
   ```bash
   # For patch releases (0.1.0 → 0.1.1)
   poetry version patch
   
   # For minor releases (0.1.0 → 0.2.0) 
   poetry version minor
   
   # For major releases (0.1.0 → 1.0.0)
   poetry version major
   ```

2. **Update changelog**:
   - Move "Unreleased" items to a new version section
   - Add release date

3. **Commit and tag**:
   ```bash
   git add pyproject.toml docs/changelog.md
   git commit -m "Release v0.1.0"
   git tag v0.1.0
   git push origin main v0.1.0
   ```

4. **Create GitHub release**:
   - Go to GitHub → Releases
   - Create release from the tag
   - The workflow will automatically publish to PyPI

## Security Features

### API Token Security
- Uses GitHub Secrets to store API tokens securely
- Tokens are never exposed in logs
- Uses GitHub's OIDC for trusted publishing (recommended)

### Environment Protection
- Optional: Require manual approval before publishing
- Restrict to specific branches
- Time delays before deployment

### Package Verification
- Runs full test suite before building
- Validates package with `twine check`
- Only publishes if all checks pass

## Troubleshooting

### Common Issues

1. **"Package already exists"**:
   - You cannot overwrite a published version
   - Increment the version number in `pyproject.toml`

2. **"Invalid token"**:
   - Verify the API token is correct in GitHub Secrets
   - Ensure token has appropriate scope

3. **"Tests failed"**:
   - Fix any test failures before the workflow will publish
   - Check the build logs for details

4. **"Package name not available"**:
   - The package name might be taken
   - Consider adding a prefix or suffix to the name

### Testing the Workflow

1. **Test with TestPyPI first**:
   ```bash
   # Manually trigger with testpypi environment
   # Install and test: pip install --index-url https://test.pypi.org/simple/ egile-mcp-client
   ```

2. **Verify package contents**:
   ```bash
   # Download and inspect the built package locally
   poetry build
   tar -tzf dist/egile_mcp_client-*.tar.gz
   ```

## Next Steps

1. Set up PyPI and TestPyPI accounts
2. Generate API tokens
3. Add secrets to GitHub repository
4. Test with TestPyPI using manual workflow dispatch
5. Create your first release to publish to PyPI

The workflow is now ready to use! 🚀
