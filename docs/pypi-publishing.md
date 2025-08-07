# PyPI Publishing Setup Guide

This guide explains how to set up and use the GitHub Actions workflow for publishing `egile-mcp-client` to PyPI.

## Prerequisites

### 1. PyPI Account Setup
1. Create accounts on both [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/)
2. Enable two-factor authentication (2FA) on both accounts
3. Generate API tokens for both accounts

### 2. Generate API Tokens

#### For PyPI:
1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Set scope to "Entire account" (or specific to your project once it exists)
5. Copy the token (starts with `pypi-`)

#### For TestPyPI:
1. Go to [TestPyPI Account Settings](https://test.pypi.org/manage/account/)
2. Follow the same steps as above
3. Copy the token (starts with `pypi-`)

### 3. Configure GitHub Secrets

In your GitHub repository:
1. Go to Settings → Secrets and variables → Actions
2. Add the following repository secrets:
   - `PYPI_API_TOKEN`: Your PyPI API token
   - `TEST_PYPI_API_TOKEN`: Your TestPyPI API token

### 4. Create GitHub Environments (Recommended)

For additional security, create environments:
1. Go to Settings → Environments
2. Create two environments:
   - `pypi` - for production releases
   - `testpypi` - for testing

You can add protection rules like:
- Required reviewers
- Deployment branches (only `main` branch)
- Environment secrets (store tokens here instead of repository secrets)

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
