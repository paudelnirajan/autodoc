# AutoDoc AI - Multi-Provider Setup Guide

## Quick Setup for Google Gemini

Since you have a Gemini API key, here's how to set it up:

### Option 1: Interactive Setup (Recommended)
```bash
autodoc init
```

Then follow the prompts:
1. Select `4` for Google Gemini
2. Enter your Gemini API key
3. Press Enter to use default model (`gemini-1.5-pro`) or specify a different one

### Option 2: Manual .env Setup

Create or edit `.env` in your project root:

```env
GEMINI_API_KEY="your-gemini-api-key-here"
GEMINI_MODEL_NAME="gemini-1.5-pro"
AUTODOC_PROVIDER="gemini"
```

## Using Different Providers

### After Setup
Once configured, just run:
```bash
autodoc run . --in-place
```
It will automatically use the provider from your `.env` file.

### Override Provider for a Single Run
```bash
# Use Gemini (if you have the key in .env)
autodoc run . --provider gemini --in-place

# Use OpenAI
autodoc run . --provider openai --in-place

# Use Anthropic/Claude
autodoc run . --provider anthropic --in-place

# Use Groq
autodoc run . --provider groq --in-place
```

### Override Model for a Single Run
```bash
# Use a different Gemini model
autodoc run . --provider gemini --model gemini-1.5-flash --in-place

# Use GPT-4
autodoc run . --provider openai --model gpt-4 --in-place
```

## Switching Providers Permanently

Just run `autodoc init` again and select a different provider. It will update your `.env` file.

## Required API Keys per Provider

Add these to your `.env` file:

### Groq (Default, Free Tier Available)
```env
GROQ_API_KEY="gsk_..."
GROQ_MODEL_NAME="llama-3.3-70b-versatile"  # optional
AUTODOC_PROVIDER="groq"
```

### OpenAI
```env
OPENAI_API_KEY="sk-..."
OPENAI_MODEL_NAME="gpt-4o-mini"  # optional
AUTODOC_PROVIDER="openai"
```
Install: `pip install openai`

### Anthropic (Claude)
```env
ANTHROPIC_API_KEY="sk-ant-..."
ANTHROPIC_MODEL_NAME="claude-3-5-sonnet-latest"  # optional
AUTODOC_PROVIDER="anthropic"
```
Install: `pip install anthropic`

### Google Gemini
```env
GEMINI_API_KEY="AIza..."
GEMINI_MODEL_NAME="gemini-1.5-pro"  # optional
AUTODOC_PROVIDER="gemini"
```
Install: `pip install google-generativeai`

## Example Workflow

1. **Initial setup with Gemini:**
   ```bash
   autodoc init
   # Select 4 for Gemini
   # Enter your API key
   ```

2. **Run with type hints:**
   ```bash
   autodoc run examples/ --add-type-hints --in-place
   ```

3. **Switch to OpenAI for a test:**
   ```bash
   autodoc run test.py --provider openai --model gpt-4
   ```

4. **Change default to OpenAI:**
   ```bash
   autodoc init
   # Select 2 for OpenAI
   # Enter your API key
   ```

## Troubleshooting

### "API key not found" error
- Run `autodoc init` to configure
- Or manually add the key to `.env`
- Make sure `.env` is in your project root (where you run autodoc)

### "Package not installed" error
Install the required SDK:
```bash
pip install openai anthropic google-generativeai
```

### Want to see which provider is being used?
Check your `.env` file for the `AUTODOC_PROVIDER` value.
