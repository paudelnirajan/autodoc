# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-11-11

### 🚀 Major Improvements
- **Complete rebranding**: Updated all references from "AutoDoc" to "Zenco"
- **Smart LLM auto-detection**: Automatically switches from mock to real LLM when API keys are configured
- **Secure API key input**: Added masked input using `getpass` for enhanced security
- **First-time user guidance**: Added helpful setup message for new users

### 🔧 Technical Changes
- Updated environment variable from `AUTODOC_PROVIDER` to `ZENCO_PROVIDER`
- Updated configuration section from `[tool.autodoc]` to `[tool.zenco]`
- Improved strategy selection logic with automatic provider detection
- Enhanced CLI help text and examples

### 🛡️ Security Enhancements
- API keys are now hidden during input (no characters shown)
- Added masked confirmation showing only first 4 characters
- Follows industry standards for credential handling

### 🎯 User Experience
- Clear first-time setup instructions
- Automatic provider detection eliminates confusion
- Consistent branding throughout the application
- Better error messages with correct command references

### 📦 Dependencies
- No new dependencies added (getpass is part of Python standard library)

## [1.1.1] - Previous Release
- Initial stable release with multi-language support
