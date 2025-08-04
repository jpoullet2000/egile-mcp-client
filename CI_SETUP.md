# CI/CD Pipeline Documentation

## Overview

This repository includes a comprehensive CI/CD pipeline using GitHub Actions that ensures code quality, runs tests, builds documentation, and automates releases.

## Workflows

### 1. Main CI Pipeline (`.github/workflows/ci.yml`)

**Triggers:** Push to `main`/`develop`, Pull requests
**Features:**
- ✅ Multi-version Python testing (3.10, 3.11, 3.12)
- ✅ Automated testing with pytest and coverage reporting
- ✅ Code quality checks (black, isort, flake8, mypy)
- ✅ Security scanning (bandit, safety)
- ✅ Package building and artifact upload
- ✅ Codecov integration for coverage reports

### 2. Documentation Pipeline (`.github/workflows/docs.yml`)

**Triggers:** Push to `main`, changes to `docs/` folder
**Features:**
- ✅ Sphinx documentation building
- ✅ Warning detection and failure on errors
- ✅ Automatic deployment to GitHub Pages
- ✅ Documentation artifact upload

### 3. Code Quality Pipeline (`.github/workflows/quality.yml`)

**Triggers:** Push/PR to `main`/`develop`
**Features:**
- ✅ CodeQL security analysis
- ✅ Code complexity analysis (radon, xenon)
- ✅ Automated quality reporting

### 4. Integration Testing (`.github/workflows/integration.yml`)

**Triggers:** Push to `main`, PR, nightly schedule
**Features:**
- ✅ Full integration test suite
- ✅ CLI command testing
- ✅ Web interface startup testing
- ✅ Docker container testing
- ✅ Service dependencies (Redis)

### 5. Release Pipeline (`.github/workflows/release.yml`)

**Triggers:** Git tags (v*.*.*)
**Features:**
- ✅ Automated PyPI publishing
- ✅ GitHub Release creation
- ✅ Docker image building and publishing
- ✅ Multi-platform support (amd64, arm64)

## Setup Instructions

### Required Secrets

Add these secrets to your GitHub repository settings:

```
PYPI_TOKEN=your_pypi_token_here
DOCKER_USERNAME=your_docker_username
DOCKER_PASSWORD=your_docker_password
CODECOV_TOKEN=your_codecov_token (optional)
```

### Badge URLs

Add these badges to your README.md:

```markdown
[![CI](https://github.com/jpoullet2000/egile-mcp-client/workflows/CI/badge.svg)](https://github.com/jpoullet2000/egile-mcp-client/actions/workflows/ci.yml)
[![Documentation](https://github.com/jpoullet2000/egile-mcp-client/workflows/Documentation/badge.svg)](https://github.com/jpoullet2000/egile-mcp-client/actions/workflows/docs.yml)
[![codecov](https://codecov.io/gh/jpoullet2000/egile-mcp-client/branch/main/graph/badge.svg)](https://codecov.io/gh/jpoullet2000/egile-mcp-client)
[![Code Quality](https://github.com/jpoullet2000/egile-mcp-client/workflows/Code%20Quality/badge.svg)](https://github.com/jpoullet2000/egile-mcp-client/actions/workflows/quality.yml)
```

## Development Workflow

### Pre-commit Hooks

Install pre-commit hooks for local development:

```bash
poetry install
poetry run pre-commit install
```

### Running Tests Locally

```bash
# Unit tests
poetry run pytest tests/ -v

# With coverage
poetry run pytest tests/ --cov=egile_mcp_client --cov-report=html

# Integration tests only
poetry run pytest tests/ -m integration

# All quality checks
poetry run black egile_mcp_client/ tests/
poetry run isort egile_mcp_client/ tests/
poetry run flake8 egile_mcp_client/ tests/
poetry run mypy egile_mcp_client/
poetry run bandit -r egile_mcp_client/
```

### Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create and push a git tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
4. The release workflow will automatically:
   - Run all tests
   - Build the package
   - Publish to PyPI
   - Create GitHub release
   - Build and push Docker images

## Monitoring

- **GitHub Actions**: Monitor workflow runs in the Actions tab
- **Codecov**: View coverage reports at [codecov.io](https://codecov.io/gh/jpoullet2000/egile-mcp-client)
- **Documentation**: Auto-deployed to [GitHub Pages](https://jpoullet2000.github.io/egile-mcp-client)

## Troubleshooting

### Common Issues

1. **Test failures**: Check the Actions tab for detailed logs
2. **Coverage drops**: Ensure new code includes proper tests
3. **Documentation build failures**: Check Sphinx warnings in docs workflow
4. **Release failures**: Verify all secrets are correctly configured

### Local Debugging

```bash
# Run the same checks as CI locally
poetry run pytest tests/ -v
poetry run black --check egile_mcp_client/ tests/
poetry run isort --check-only egile_mcp_client/ tests/
poetry run flake8 egile_mcp_client/ tests/
poetry run mypy egile_mcp_client/

# Build documentation locally
cd docs
make clean && make html
```
