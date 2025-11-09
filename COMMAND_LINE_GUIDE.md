# AutoDoc AI - Complete Command-Line Reference

## Main Commands

### 1. `autodoc init`
**Purpose:** Interactive setup wizard for configuring your LLM provider and API keys.

**Usage:**
```bash
autodoc init
```

**What it does:**
- Prompts you to select an LLM provider (Groq, OpenAI, Anthropic, Gemini)
- Asks for your API key
- Asks for model name (with smart defaults)
- Creates/updates `.env` file with your configuration
- Sets `AUTODOC_PROVIDER` so you don't need to specify `--provider` every time

**Example interaction:**
```
Select your LLM provider (1-4, default: 1): 4
Enter your GEMINI API key: AIza...
Enter model name (default: gemini-1.5-pro): [press Enter]
```

---

### 2. `autodoc run`
**Purpose:** Main command to analyze and process code files.

**Basic syntax:**
```bash
autodoc run [path] [options]
```

---

## Positional Arguments

### `path` (optional, default: `.`)
**What it does:** Specifies which file or directory to process.

**Examples:**
```bash
# Process current directory
autodoc run .

# Process specific file
autodoc run src/main.py

# Process entire directory
autodoc run src/

# Process multiple files (via shell expansion)
autodoc run src/*.py
```

---

## Core Options

### `--in-place`
**What it does:** Writes changes directly to the source files instead of printing to console.

**Default:** `False` (dry-run mode - prints to console)

**Examples:**
```bash
# Dry run (preview changes)
autodoc run test.py

# Apply changes to file
autodoc run test.py --in-place
```

**⚠️ Important:** Without this flag, changes are only previewed. Use it when you're ready to modify files.

---

### `--diff`
**What it does:** Only processes files that have been modified in your current Git branch (compared to main/master).

**Default:** `False`

**Use case:** Perfect for pre-commit hooks or reviewing only changed files.

**Examples:**
```bash
# Process only Git-changed files
autodoc run . --diff --in-place

# Preview changes to modified files
autodoc run . --diff
```

**Requirements:** Must be in a Git repository with uncommitted changes or commits ahead of main.

---

## LLM Provider Options

### `--provider {groq,openai,anthropic,gemini}`
**What it does:** Selects which LLM service to use for AI-powered features.

**Default:** Reads from `.env` file (`AUTODOC_PROVIDER`), falls back to `groq`

**Examples:**
```bash
# Use Gemini (if configured in .env)
autodoc run . --provider gemini

# Use OpenAI for this run only
autodoc run test.py --provider openai

# Use Anthropic/Claude
autodoc run . --provider anthropic --in-place
```

**Note:** You must have the corresponding API key in `.env` and the SDK installed.

---

### `--model MODEL`
**What it does:** Overrides the default model for the selected provider.

**Default:** Reads from `.env` (e.g., `GEMINI_MODEL_NAME`), or uses provider defaults

**Provider defaults:**
- Groq: `llama-3.3-70b-versatile`
- OpenAI: `gpt-4o-mini`
- Anthropic: `claude-3-5-sonnet-latest`
- Gemini: `gemini-1.5-pro`

**Examples:**
```bash
# Use faster Gemini model
autodoc run . --provider gemini --model gemini-1.5-flash

# Use GPT-4 instead of default
autodoc run . --provider openai --model gpt-4

# Use smaller Groq model
autodoc run . --model llama3-8b-8192
```

---

### `--strategy {mock,groq}`
**What it does:** Controls whether to use real LLM or mock generator.

**Default:** `mock` (from config)

**Options:**
- `mock`: No API calls, returns placeholder text (for testing)
- `groq`: Uses real LLM (actual provider determined by `--provider`)

**⚠️ Note:** This is a legacy flag. When using `--provider`, you should typically use `--strategy groq` (not `mock`).

**Examples:**
```bash
# Use real LLM (Gemini from .env)
autodoc run . --strategy groq

# Test without API calls
autodoc run . --strategy mock
```

---

## Docstring Options

### `--style {google,numpy,rst}`
**What it does:** Sets the docstring format style.

**Default:** `google`

**Styles:**
- `google`: Google-style docstrings (most common)
- `numpy`: NumPy/SciPy style
- `rst`: reStructuredText style (Sphinx)

**Examples:**
```bash
# Use NumPy style
autodoc run . --style numpy --in-place

# Use Sphinx/RST style
autodoc run . --style rst
```

---

### `--overwrite-existing`
**What it does:** Regenerates poor-quality docstrings that already exist.

**Default:** `False` (only adds missing docstrings)

**Use case:** Improving low-quality or placeholder docstrings.

**Examples:**
```bash
# Only add missing docstrings
autodoc run . --in-place

# Also improve existing poor docstrings
autodoc run . --overwrite-existing --in-place
```

**How it works:** Uses LLM to evaluate existing docstrings. If deemed low-quality, replaces them.

---

## Refactoring Options

### `--refactor`
**What it does:** Enables AI-powered code refactoring (variable/function renaming).

**Default:** `False`

**What it refactors:**
- Poorly named local variables
- Unclear function names
- Misleading class names

**Examples:**
```bash
# Enable refactoring
autodoc run . --refactor --in-place

# Combine with other features
autodoc run . --refactor --overwrite-existing --in-place
```

**⚠️ Caution:** This modifies code logic (renames). Review changes carefully.

---

### `--add-type-hints`
**What it does:** Generates and adds Python type hints to functions without them.

**Default:** `False`

**Language support:** Python only (for now)

**What it adds:**
- Parameter type hints
- Return type hints
- Necessary `typing` imports

**Examples:**
```bash
# Add type hints only
autodoc run . --add-type-hints --in-place

# Combine with docstrings
autodoc run . --add-type-hints --in-place

# Full quality pass
autodoc run . --add-type-hints --overwrite-existing --refactor --in-place
```

**How it works:**
1. Detects functions without type hints
2. Uses LLM to infer types from function body
3. Adds type annotations to function signature
4. Automatically adds `from typing import ...` if needed

---

## Common Workflows

### 1. Initial Setup
```bash
# Configure your LLM provider
autodoc init

# Test on a single file (dry run)
autodoc run examples/test.py --add-type-hints

# Apply if looks good
autodoc run examples/test.py --add-type-hints --in-place
```

### 2. Add Docstrings to Project
```bash
# Preview changes
autodoc run src/

# Apply to all files
autodoc run src/ --in-place
```

### 3. Add Type Hints to Project
```bash
# Add type hints to all Python files
autodoc run . --add-type-hints --in-place
```

### 4. Full Code Quality Pass
```bash
# Everything: docstrings, type hints, refactoring
autodoc run . --add-type-hints --overwrite-existing --refactor --in-place
```

### 5. Pre-Commit Hook (Git-changed files only)
```bash
# Process only modified files
autodoc run . --diff --add-type-hints --in-place
```

### 6. Switch Providers for Testing
```bash
# Try with Gemini
autodoc run test.py --provider gemini

# Try with GPT-4
autodoc run test.py --provider openai --model gpt-4

# Compare results
autodoc run test.py --provider anthropic
```

---

## Combining Options

You can combine multiple flags for powerful workflows:

```bash
# Full quality pass with Gemini
autodoc run src/ \
  --provider gemini \
  --add-type-hints \
  --overwrite-existing \
  --refactor \
  --in-place

# Git-changed files with type hints (pre-commit)
autodoc run . \
  --diff \
  --add-type-hints \
  --in-place

# NumPy-style docstrings with GPT-4
autodoc run . \
  --provider openai \
  --model gpt-4 \
  --style numpy \
  --in-place
```

---

## Environment Variables

These are set by `autodoc init` or manually in `.env`:

### Provider Configuration
```env
# Which provider to use by default
AUTODOC_PROVIDER="gemini"
```

### Groq
```env
GROQ_API_KEY="gsk_..."
GROQ_MODEL_NAME="llama-3.3-70b-versatile"
```

### OpenAI
```env
OPENAI_API_KEY="sk-..."
OPENAI_MODEL_NAME="gpt-4o-mini"
```

### Anthropic
```env
ANTHROPIC_API_KEY="sk-ant-..."
ANTHROPIC_MODEL_NAME="claude-3-5-sonnet-latest"
```

### Gemini
```env
GEMINI_API_KEY="AIza..."
GEMINI_MODEL_NAME="gemini-1.5-pro"
```

---

## Troubleshooting

### "API key not found"
- Run `autodoc init` to configure
- Or manually add key to `.env`

### "Package not installed"
Install the required SDK:
```bash
pip install openai anthropic google-generativeai
```

### Changes not applying
- Add `--in-place` flag
- Check file permissions

### Wrong provider being used
- Check `.env` for `AUTODOC_PROVIDER`
- Override with `--provider` flag

### Want to see what will change?
- Remove `--in-place` to preview (dry run)

---

## Quick Reference

| Flag | Purpose | Default |
|------|---------|---------|
| `path` | File/directory to process | `.` |
| `--in-place` | Write changes to files | `False` (dry-run) |
| `--diff` | Only Git-changed files | `False` |
| `--provider` | LLM service | From `.env` or `groq` |
| `--model` | LLM model | Provider default |
| `--strategy` | mock/groq | `mock` |
| `--style` | Docstring style | `google` |
| `--overwrite-existing` | Fix bad docstrings | `False` |
| `--refactor` | Rename variables/functions | `False` |
| `--add-type-hints` | Add type annotations | `False` |
