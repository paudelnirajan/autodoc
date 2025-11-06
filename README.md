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
    *   **Intelligent Naming Suggestions:** Acts as an AI-powered linter, suggesting better names for classes and functions that are too short or non-descriptive.
*   **Seamless Git Integration:** Use the `--diff` flag to only process files that have been changed in your current Git branch, making it incredibly fast and efficient for pre-commit hooks and CI pipelines.
*   **Codebase-Wide Scanning:** Run `autodoc` on a single file or an entire directory. It automatically finds all Python files and respects your `.gitignore` to avoid processing virtual environments or build artifacts.
*   **Automatic Formatting:** Integrates with the `black` code formatter to ensure that all generated and refactored code is perfectly styled.
*   **Highly Configurable:** Set project-wide defaults for style, AI provider, and behavior in your `pyproject.toml` file.

## Installation

You can install AutoDoc AI directly from PyPI:

```bash
pip install autodoc-ai-paudelnirajan
```

## Configuration

### 1. Set Up Your AI Provider

AutoDoc requires an API key from an LLM provider. This project is configured to use Groq.

1.  Create a `.env` file in the root of your project.
2.  Add your Groq API key and desired model to the file:

    ```env
    GROQ_API_KEY="gsk_YourActualGroqApiKeyHere"
    GROQ_MODEL_NAME="llama3-8b-8192"
    ```

### 2. Configure Project Defaults (Optional)

You can set default behaviors for your project in your `pyproject.toml` file. AutoDoc will use these settings unless they are overridden by a command-line flag.

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

AutoDoc is a flexible command-line tool.

**Get help:**
```bash
autodoc --help
```

**Run on a specific file (dry run, prints to console):**
```bash
autodoc path/to/your/file.py
```

**Run on an entire directory and save changes in-place:**
```bash
autodoc src/ --in-place
```

**Run in "Git mode" to only process changed files (most common use case):**
```bash
autodoc --diff --in-place
```

**Enable all AI features to perform a full quality pass:**
```bash
autodoc . --in-place --overwrite-existing --refactor
```

## How It Works

AutoDoc uses a "Surgical Hybrid" architecture that combines the strengths of traditional and modern tooling:

1.  **Fast Local Analysis:** It uses Python's `ast` (Abstract Syntax Tree) module to rapidly parse code and identify potential issues (like a missing docstring or a short variable name). This is done locally and is extremely fast.
2.  **Targeted AI Intelligence:** Only when a potential issue is found does it send the small, relevant code snippet to an LLM for intelligent analysis (e.g., "Is this a good name?" or "Generate a docstring for this function").
3.  **Precise Code Modification:** The AI's response is used to perform a safe and precise modification of the AST, which is then unparsed back into valid Python code.
4.  **Toolchain Integration:** Finally, it uses `black` to ensure the final code is perfectly formatted, integrating seamlessly into the existing Python ecosystem.

## License

This project is licensed under the MIT License.
