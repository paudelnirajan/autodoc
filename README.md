# AutoDoc AI

[![PyPI version](https://badge.fury.io/py/autodoc-ai-paudelnirajan.svg)](https://badge.fury.io/py/autodoc-ai-paudelnirajan)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AutoDoc AI** is a smart command-line developer tool that automates the tedious parts of maintaining high-quality Python code. It leverages Large Language Models (LLMs) to automatically generate docstrings, suggest intelligent refactorings, and integrate seamlessly into a modern development workflow.

This project was built on a foundation of solid Object-Oriented Programming principles and design patterns, including the Visitor, Strategy, Factory, and Adapter patterns.

---

## Core Features

*   **AI-Powered Docstring Generation:** Automatically create high-quality, context-aware docstrings for any function or class that's missing them.
*   **Intelligent Docstring Correction:** Uses AI to evaluate existing docstrings and replaces poor-quality or placeholder documentation with new, improved versions.
*   **AI-Powered Refactoring:**
    *   **Safe Variable Renaming:** Automatically renames poorly named local variables within function scope.
    *   **Intelligent Naming Suggestions:** Acts as an AI-powered linter, suggesting better names for classes and functions.
*   **Seamless Git Integration:** Use the `--diff` flag to only process files that have been changed in your current Git branch.
*   **Codebase-Wide Scanning:** Run `autodoc` on a single file or an entire directory, with automatic `.gitignore` respect.
*   **Automatic Formatting:** Integrates with the `black` code formatter to ensure all generated and refactored code is perfectly styled.
*   **Highly Configurable:** Set project-wide defaults for style, AI provider, and behavior in your `pyproject.toml` file.

## Installation

You can install AutoDoc AI directly from PyPI:

```bash
pip install autodoc-ai-paudelnirajan
```

## First-Time Setup

Before you can use the AI features, you need to configure your API key. The easiest way is to use the built-in `init` command in your project's root directory.

```bash
autodoc init
```

This will guide you through creating or updating a `.env` file with your Groq API key and preferred model.

## Configuration

AutoDoc uses a `.env` file for secrets and a `pyproject.toml` file for project-wide settings.

### 1. API Credentials (`.env`)

The `autodoc init` command will create this for you. It should look like this:

```env
GROQ_API_KEY="gsk_YourActualGroqApiKeyHere"
GROQ_MODEL_NAME="llama3-8b-8192"
```

### 2. Project Defaults (`pyproject.toml`)

You can set default behaviors for your project in `pyproject.toml`. These settings will be used unless they are overridden by a command-line flag.

```toml
# In your pyproject.toml

[tool.autodoc]
# Settings for your AutoDoc tool
strategy = "groq"
style = "google"           # 'google', 'numpy', or 'rst'
overwrite_existing = true  # Regenerate poor-quality docstrings
refactor = true            # Enable AI-powered refactoring
```

## Usage

AutoDoc is a flexible command-line tool with two main commands: `init` and `run`.

**Get a list of commands:**
```bash
autodoc --help
```

**Get detailed help for the `run` command and all its flags:**
```bash
autodoc run --help
```

**Run on a specific file (dry run, prints to console):**
```bash
autodoc run path/to/your/file.py
```

**Run on an entire directory and save changes in-place:**
```bash
autodoc run src/ --in-place
```

**Run in "Git mode" to only process changed files (most common use case):**
```bash
autodoc run . --diff --in-place
```

**Enable all AI features to perform a full quality pass:**
```bash
autodoc run . --in-place --overwrite-existing --refactor
```

## How It Works

AutoDoc uses a "Surgical Hybrid" architecture that combines the strengths of traditional and modern tooling:

1.  **Fast Local Analysis:** It uses Python's `ast` (Abstract Syntax Tree) module to rapidly parse code and identify potential issues.
2.  **Targeted AI Intelligence:** Only when a potential issue is found does it send the small, relevant code snippet to an LLM for intelligent analysis.
3.  **Precise Code Modification:** The AI's response is used to perform a safe and precise modification of the AST, which is then unparsed back into valid Python code.
4.  **Toolchain Integration:** Finally, it uses `black` to ensure the final code is perfectly formatted, integrating seamlessly into the existing Python ecosystem.

## License

This project is licensed under the MIT License.