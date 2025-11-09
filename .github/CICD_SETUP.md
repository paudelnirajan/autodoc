# CI/CD Setup Guide for Zenco

## 🎯 Overview

This project uses **GitHub Actions** for automated testing, linting, and PyPI publishing.

## 📋 Workflows

### 1. **Tests** (`.github/workflows/test.yml`)
- **Triggers**: Push/PR to `main` or `develop`
- **Matrix Testing**: Python 3.9-3.12 on Ubuntu, macOS, Windows
- **Actions**:
  - Install dependencies
  - Run import tests
  - Test CLI commands
  - Run pytest (if tests exist)
  - Upload coverage to Codecov

### 2. **Code Quality** (`.github/workflows/lint.yml`)
- **Triggers**: Push/PR to `main` or `develop`
- **Checks**:
  - Black formatting
  - isort import sorting
  - flake8 linting
  - mypy type checking

### 3. **Publish to PyPI** (`.github/workflows/publish.yml`)
- **Triggers**: 
  - Automatic on GitHub Release
  - Manual via workflow_dispatch
- **Actions**:
  - Build package
  - Publish to Test PyPI (manual)
  - Publish to PyPI (on release)

## 🔧 Setup Instructions

### Step 1: Push Workflows to GitHub
```bash
git add .github/
git commit -m "Add CI/CD workflows"
git push origin main
```

### Step 2: Configure PyPI Tokens

1. **Get PyPI API Token:**
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token
   - Copy the token (starts with `pypi-`)

2. **Get Test PyPI Token (optional):**
   - Go to https://test.pypi.org/manage/account/token/
   - Create a new API token

3. **Add Secrets to GitHub:**
   - Go to your repo: `Settings` → `Secrets and variables` → `Actions`
   - Click `New repository secret`
   - Add:
     - Name: `PYPI_API_TOKEN`, Value: your PyPI token
     - Name: `TEST_PYPI_API_TOKEN`, Value: your Test PyPI token

### Step 3: Create Your First Release

```bash
# Tag your release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Or create release via GitHub UI:
# Go to: Releases → Draft a new release → Create tag v1.0.0
```

## 🚀 Usage

### Automatic Testing
- Every push/PR triggers tests automatically
- Check status in the "Actions" tab

### Manual PyPI Upload (Test)
1. Go to `Actions` tab
2. Select `Publish to PyPI` workflow
3. Click `Run workflow`
4. Select branch and run

### Automatic PyPI Upload
- Create a GitHub Release
- Workflow automatically publishes to PyPI

## 📊 Status Badges

Add to your README.md:

```markdown
[![Tests](https://github.com/paudelnirajan/zenco/workflows/Tests/badge.svg)](https://github.com/paudelnirajan/zenco/actions)
[![Code Quality](https://github.com/paudelnirajan/zenco/workflows/Code%20Quality/badge.svg)](https://github.com/paudelnirajan/zenco/actions)
[![PyPI version](https://badge.fury.io/py/zenco.svg)](https://badge.fury.io/py/zenco)
```

## 🔒 Security Best Practices

- ✅ Never commit API tokens
- ✅ Use GitHub Secrets for sensitive data
- ✅ Test on Test PyPI before production
- ✅ Use scoped tokens (project-specific)
- ✅ Enable 2FA on PyPI account

## 🐛 Troubleshooting

### Tests Failing?
- Check Python version compatibility
- Verify all dependencies are in `pyproject.toml`
- Review logs in Actions tab

### Publishing Failing?
- Verify token is correct in Secrets
- Check package name isn't taken
- Ensure version number is incremented
- Run `twine check dist/*` locally

## 📝 Next Steps

1. ✅ Set up GitHub repository
2. ✅ Add PyPI tokens to Secrets
3. ✅ Push workflows to GitHub
4. ✅ Create first release
5. ✅ Monitor Actions tab for status
