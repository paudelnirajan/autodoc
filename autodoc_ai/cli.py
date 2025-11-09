import argparse
import sys
import os
from textwrap import indent
import traceback
from textwrap import indent
from tree_sitter import QueryCursor
from .generators import GeneratorFactory, IDocstringGenerator
from .utils import get_source_files, get_git_changed_files
from .config import load_config
from .parser import get_language_parser, get_language_queries
from .transformers import CodeTransformer
import textwrap
from .formatters import FormatterFactory

def init_config():
    """
    Guides the user through creating or updating a .env file for API keys.
    Supports multiple LLM providers interactively.
    """
    print("\n" + "="*70)
    print("  🚀 AutoDoc AI - Initial Configuration Wizard")
    print("="*70)
    print("\nThis wizard will help you set up your preferred AI provider.")
    print("Your API key will be stored securely in a local .env file.\n")
    
    print("📋 Supported LLM Providers:")
    print("  1. Groq        - Fast inference, generous free tier")
    print("  2. OpenAI      - GPT-4, GPT-4o-mini (requires paid account)")
    print("  3. Anthropic   - Claude 3.5 Sonnet (requires paid account)")
    print("  4. Google      - Gemini Pro/Flash (free tier available)")
    
    provider_choice = input("\n👉 Select your LLM provider (1-4) [default: 1]: ").strip() or "1"
    
    provider_map = {
        "1": ("groq", "GROQ_API_KEY", "GROQ_MODEL_NAME", "llama-3.3-70b-versatile"),
        "2": ("openai", "OPENAI_API_KEY", "OPENAI_MODEL_NAME", "gpt-4o-mini"),
        "3": ("anthropic", "ANTHROPIC_API_KEY", "ANTHROPIC_MODEL_NAME", "claude-3-5-sonnet-latest"),
        "4": ("gemini", "GEMINI_API_KEY", "GEMINI_MODEL_NAME", "gemini-1.5-pro"),
    }
    
    if provider_choice not in provider_map:
        print("Invalid choice. Defaulting to Groq.")
        provider_choice = "1"
    
    provider_name, api_key_var, model_var, default_model = provider_map[provider_choice]
    
    print(f"\n{'─'*70}")
    print(f"📝 Configuring {provider_name.upper()}")
    print(f"{'─'*70}")
    
    # Provider-specific instructions
    if provider_name == "groq":
        print("ℹ️  Get your free API key at: https://console.groq.com/keys")
    elif provider_name == "openai":
        print("ℹ️  Get your API key at: https://platform.openai.com/api-keys")
    elif provider_name == "anthropic":
        print("ℹ️  Get your API key at: https://console.anthropic.com/")
    elif provider_name == "gemini":
        print("ℹ️  Get your API key at: https://aistudio.google.com/app/apikey")
    
    api_key = input(f"\n🔑 Enter your {provider_name.upper()} API key: ").strip()
    
    if not api_key:
        print("\n❌ API key is required. Configuration cancelled.")
        return
    
    model_name = input(f"🤖 Enter model name [default: {default_model}]: ").strip() or default_model
    
    keys_to_update = {
        api_key_var: api_key,
        model_var: model_name,
        "AUTODOC_PROVIDER": provider_name,  # Store the selected provider
    }
    
    env_path = ".env"
    
    if os.path.exists(env_path):
        print(f"\n📝 Updating existing '{env_path}' file...")
        with open(env_path, "r") as f:
            lines = f.readlines()
        
        # Update existing keys
        updated_keys = set()
        for i, line in enumerate(lines):
            for key, value in keys_to_update.items():
                if line.strip().startswith(f"{key}="):
                    lines[i] = f'{key}="{value}"\n'
                    print(f"  ✓ Updated {key}")
                    updated_keys.add(key)
        
        # Add new keys that weren't found
        for key, value in keys_to_update.items():
            if key not in updated_keys:
                lines.append(f'{key}="{value}"\n')
                print(f"  ✓ Added {key}")
        
        with open(env_path, "w") as f:
            f.writelines(lines)
    else:
        print(f"\n📝 Creating new '{env_path}' file...")
        with open(env_path, "w") as f:
            for key, value in keys_to_update.items():
                f.write(f'{key}="{value}"\n')
                print(f"  ✓ Added {key}")
    
    print(f"\n{'='*70}")
    print(f"  ✅ Configuration Complete!")
    print(f"{'='*70}")
    print(f"\n📊 Your Settings:")
    print(f"  • Provider: {provider_name.upper()}")
    print(f"  • Model: {model_name}")
    print(f"  • Config file: {env_path}")
    
    print(f"\n🚀 Next Steps:")
    print(f"  1. Test your setup:")
    print(f"     autodoc run examples/test.py")
    print(f"\n  2. Add type hints to your code:")
    print(f"     autodoc run . --add-type-hints --in-place")
    print(f"\n  3. Generate docstrings:")
    print(f"     autodoc run src/ --in-place")
    
    print(f"\n💡 Tips:")
    print(f"  • Use --help to see all available options")
    print(f"  • Change providers anytime: autodoc run --provider <name>")
    print(f"  • Run 'autodoc init' again to reconfigure")
    print(f"\n{'='*70}\n")


def process_file_with_treesitter(filepath: str, generator: IDocstringGenerator, in_place: bool, overwrite_existing: bool, add_type_hints: bool = False):
    """
    Processes a single file using the Tree-sitter engine to find and
    report undocumented functions and optionally add type hints.
    """

    lang = None
    if filepath.endswith('.py'): lang = 'python'
    elif filepath.endswith('.js'): lang = 'javascript'
    elif filepath.endswith('.java'): lang = 'java'
    elif filepath.endswith('.go'): lang = 'go'
    elif filepath.endswith('.cpp') or filepath.endswith('.hpp') or filepath.endswith('.h'): lang = 'cpp'

    parser = get_language_parser(lang)
    if not parser: return

    try:
        with open(filepath, 'rb') as f:
            source_bytes = f.read()
    except IOError as e:
        print(f"Error reading file: {e}"); return

    tree = parser.parse(source_bytes)
    transformer = CodeTransformer(source_bytes)
    queries = get_language_queries(lang)

    all_func_query = queries.get("all_functions")
    documented_funcs_query = queries.get("documented_function")

    if not all_func_query or not documented_funcs_query:
        print(f"Warning: Queries for `{lang}` not fully defined. Skipping.")
        return

    # Use QueryCursor to execute queries (tree-sitter 0.25 API)
    # QueryCursor requires the query in the constructor
    all_func_cursor = QueryCursor(all_func_query)
    documented_func_cursor = QueryCursor(documented_funcs_query)
    
    # Get all functions (matches returns (pattern_index, {capture_name: [nodes]}) tuples)
    all_functions = set()
    for _, captures in all_func_cursor.matches(tree.root_node):
        for node in captures.get('func', []):
            all_functions.add(node)
    
    documented_nodes = {}
    for _, captures in documented_func_cursor.matches(tree.root_node):
        func_nodes = captures.get('func', [])
        doc_nodes = captures.get('docstring', [])
        for i, func_node in enumerate(func_nodes):
            if i < len(doc_nodes):
                documented_nodes[func_node] = doc_nodes[i]
    
    documented_funtions = set(documented_nodes.keys())
    
    # Also manually check for docstrings as a fallback (in case query doesn't match)
    # A function has a docstring if its first statement is a string literal
    for func_node in all_functions:
        body_node = func_node.child_by_field_name("body")
        if body_node and body_node.children:
            first_stmt = body_node.children[0]
            # Check if first statement is an expression statement with a string
            if first_stmt.type == 'expression_statement':
                expr = first_stmt.children[0] if first_stmt.children else None
                if expr and expr.type == 'string':
                    documented_funtions.add(func_node)
                    documented_nodes[func_node] = expr

    undocumented_functions = all_functions - documented_funtions

    for func_node in undocumented_functions:
        # Get function name - different field names for different languages
        name_node = func_node.child_by_field_name('name')  # Python, Java, JS
        if not name_node:
            # For C++, the name is in declarator -> identifier
            declarator = func_node.child_by_field_name('declarator')
            if declarator:
                for child in declarator.children:
                    if child.type == 'identifier':
                        name_node = child
                        break
        
        if name_node:
            func_name = name_node.text.decode('utf8')
            line_num = name_node.start_point[0] + 1
            print(f"  📝 Line {line_num}: Generating docstring for `{func_name}()`", flush=True)
            
            docstring = generator.generate(func_node)
            
            # Handle docstring insertion based on language
            # For Python: insert inside the function body
            # For Java/JS/C++: insert before the function declaration
            if lang == 'python':
                body_node = func_node.child_by_field_name("body")
                if body_node and body_node.children:
                    try:
                        # Get the function definition's indentation by reading the source line
                        # This is more reliable than using tree-sitter's start_point
                        source_text = source_bytes.decode('utf8')
                        func_start_line = func_node.start_point[0]
                        func_line = source_text.split('\n')[func_start_line]
                        func_def_indent = len(func_line) - len(func_line.lstrip())
                        
                        # Standard Python indentation is 4 spaces from the function definition
                        # We'll use this consistently to avoid issues with malformed code
                        body_indent_level = func_def_indent + 4
                        indentation_str = ' ' * body_indent_level
                        first_child = body_node.children[0]
                    except Exception as e:
                        print(f"  ERROR in indentation calculation: {e}", flush=True)
                        import traceback
                        traceback.print_exc()
                        continue

                    # Clean the raw docstring from the LLM (remove any existing indentation)
                    docstring_content_raw = docstring.strip()
                    
                    # Use textwrap.dedent to remove common leading whitespace
                    # This handles cases where the LLM returns pre-indented content
                    dedented_content = textwrap.dedent(docstring_content_raw).strip()
                    
                    # Re-indent the cleaned content to match the function's body indentation
                    # indent() adds the prefix to each line, including empty lines
                    indented_content = indent(dedented_content, indentation_str)

                    formatter = FormatterFactory.create_formatter(lang)
                    formatted_docstring = formatter.format(docstring, indentation_str)

                    # Check if first_child is already a docstring
                    is_docstring = (first_child.type == 'expression_statement' and 
                                   first_child.children and 
                                   first_child.children[0].type == 'string')
                    
                    if is_docstring:
                        # Replace the existing docstring
                        # Find the start of the line to replace any incorrect indentation
                        first_stmt_line_num = first_child.start_point[0]
                        lines = source_text.split('\n')
                        line_start_byte = sum(len(line) + 1 for line in lines[:first_stmt_line_num])
                        
                        insertion_point = line_start_byte
                        end_point = first_child.end_byte
                        formatted_docstring = formatted_docstring.rstrip() + '\n' + indentation_str
                        transformer.add_change(
                            start_byte=insertion_point,
                            end_byte=end_point,
                            new_text=formatted_docstring
                        )
                    else:
                        # Insert before the first statement
                        # We need to find the actual start of the line and replace any incorrect indentation
                        # first_child.start_point gives us (line, column)
                        first_stmt_line_num = first_child.start_point[0]
                        first_stmt_col = first_child.start_point[1]
                        
                        # Find the start of this line in the source
                        lines = source_text.split('\n')
                        line_start_byte = sum(len(line) + 1 for line in lines[:first_stmt_line_num])  # +1 for \n
                        
                        # The insertion point is at the start of the line
                        # We'll replace from line start to the actual statement start
                        # This removes any incorrect indentation
                        insertion_point = line_start_byte
                        end_point = first_child.start_byte
                        
                        # Add proper indentation before the statement
                        formatted_docstring = formatted_docstring + indentation_str
                        
                        transformer.add_change(
                            start_byte=insertion_point,
                            end_byte=end_point,
                            new_text=formatted_docstring
                        )
            else:
                # For Java, JavaScript, C++, Go: insert docstring before the function declaration
                source_text = source_bytes.decode('utf8')
                func_start_line = func_node.start_point[0]
                func_line = source_text.split('\n')[func_start_line]
                func_def_indent = len(func_line) - len(func_line.lstrip())
                indentation_str = ' ' * func_def_indent
                
                formatter = FormatterFactory.create_formatter(lang)
                formatted_docstring = formatter.format(docstring, indentation_str)
                
                # Find the start of the line where the function declaration begins
                lines = source_text.split('\n')
                line_start_byte = sum(len(line) + 1 for line in lines[:func_start_line])
                
                # Insert the docstring before the function declaration
                transformer.add_change(
                    start_byte=line_start_byte,
                    end_byte=line_start_byte,
                    new_text=formatted_docstring
                )

    # If overwrite is enabled, process functions that already have docstrings
    if overwrite_existing:
        for func_node, doc_node in documented_nodes.items():
            docstring_text = doc_node.text.decode('utf8')
            
            is_good = generator.evaluate(func_node, docstring_text)
            
            if not is_good:
                name_node = func_node.child_by_field_name('name')
                func_name = name_node.text.decode('utf8') if name_node else 'unknown'
                print(f"  🔄 Line {doc_node.start_point[0]+1}: Improving docstring for `{func_name}()` (low quality detected)")

                new_docstring = generator.generate(func_node)
                
                try:
                    source_text = source_bytes.decode('utf8')
                    func_line = source_text.split('\n')[func_node.start_point[0]]
                    func_def_indent = len(func_line) - len(func_line.lstrip())
                    body_indent_level = func_def_indent + 4
                    indentation_str = ' ' * body_indent_level
                    
                    formatter = FormatterFactory.create_formatter(lang)
                    formatted_docstring = formatter.format(new_docstring, indentation_str).strip()

                    transformer.add_change(
                        start_byte=doc_node.start_byte,
                        end_byte=doc_node.end_byte,
                        new_text=formatted_docstring
                    )
                except Exception as e:
                    print(f"  ERROR processing documented function: {e}", flush=True)
                    continue

    # Process type hints if enabled (Python only for now)
    if add_type_hints and lang == 'python':
        typed_funcs_query = queries.get("functions_with_type_hints")
        
        # Track which typing imports are needed
        typing_imports_needed = set()
        
        if typed_funcs_query:
            typed_func_cursor = QueryCursor(typed_funcs_query)
            functions_with_hints = set()
            
            for _, captures in typed_func_cursor.matches(tree.root_node):
                for node in captures.get('func', []):
                    functions_with_hints.add(node)
            
            # Find functions without type hints
            functions_without_hints = all_functions - functions_with_hints
            
            for func_node in functions_without_hints:
                name_node = func_node.child_by_field_name('name')
                if not name_node:
                    continue
                
                func_name = name_node.text.decode('utf8')
                
                # Skip special methods like __init__, __str__, etc.
                if func_name.startswith('__') and func_name.endswith('__'):
                    continue
                
                line_num = name_node.start_point[0] + 1
                print(f"  🏷️  Line {line_num}: Adding type hints to `{func_name}()`", flush=True)
                
                try:
                    type_hints = generator.generate_type_hints(func_node)
                    
                    if not type_hints or (not type_hints.get('parameters') and not type_hints.get('return_type')):
                        print(f"     ⚠️  Could not infer types for `{func_name}()`")
                        continue
                    
                    # Build the new function signature with type hints
                    source_text = source_bytes.decode('utf8')
                    
                    # Get the parameters node
                    params_node = func_node.child_by_field_name('parameters')
                    if not params_node:
                        continue
                    
                    # Build new parameter list with type hints
                    new_params = []
                    for param_child in params_node.children:
                        if param_child.type == 'identifier':
                            param_name = param_child.text.decode('utf8')
                            type_hint = type_hints.get('parameters', {}).get(param_name)
                            
                            if type_hint:
                                new_params.append(f"{param_name}: {type_hint}")
                            else:
                                new_params.append(param_name)
                        elif param_child.type in ['(', ')', ',']:
                            # Keep delimiters as-is
                            continue
                        elif param_child.type == 'default_parameter':
                            # Handle parameters with default values
                            param_id = param_child.child_by_field_name('name')
                            param_default = param_child.child_by_field_name('value')
                            
                            if param_id:
                                param_name = param_id.text.decode('utf8')
                                type_hint = type_hints.get('parameters', {}).get(param_name)
                                default_val = param_default.text.decode('utf8') if param_default else ''
                                
                                if type_hint:
                                    new_params.append(f"{param_name}: {type_hint} = {default_val}")
                                else:
                                    new_params.append(f"{param_name} = {default_val}")
                        elif param_child.type == 'typed_parameter':
                            # Already has type hint, keep as-is
                            new_params.append(param_child.text.decode('utf8'))
                        elif param_child.type == 'typed_default_parameter':
                            # Already has type hint with default, keep as-is
                            new_params.append(param_child.text.decode('utf8'))
                    
                    # Build the new function definition line
                    return_type = type_hints.get('return_type')
                    params_str = ', '.join(new_params)
                    
                    # Find the colon that ends the function signature
                    colon_found = False
                    colon_byte = None
                    for child in func_node.children:
                        if child.type == ':':
                            colon_found = True
                            colon_byte = child.start_byte
                            break
                    
                    if not colon_found:
                        continue
                    
                    # Build the replacement text for the signature
                    if return_type:
                        new_signature = f"def {func_name}({params_str}) -> {return_type}:"
                        # Check if return type needs typing imports
                        for typing_type in ['List', 'Dict', 'Tuple', 'Set', 'Optional', 'Union', 'Any', 'Callable']:
                            if typing_type in return_type:
                                typing_imports_needed.add(typing_type)
                    else:
                        new_signature = f"def {func_name}({params_str}):"
                    
                    # Check if parameter types need typing imports
                    for param_type in type_hints.get('parameters', {}).values():
                        if param_type:
                            for typing_type in ['List', 'Dict', 'Tuple', 'Set', 'Optional', 'Union', 'Any', 'Callable']:
                                if typing_type in param_type:
                                    typing_imports_needed.add(typing_type)
                    
                    # Find the start of 'def' keyword
                    def_start = func_node.start_byte
                    
                    # Replace from 'def' to ':' (inclusive)
                    transformer.add_change(
                        start_byte=def_start,
                        end_byte=colon_byte + 1,
                        new_text=new_signature
                    )
                    
                except Exception as e:
                    print(f"  ERROR adding type hints to `{func_name}`: {e}", flush=True)
                    import traceback
                    traceback.print_exc()
                    continue
            
            # Add typing import if needed
            if typing_imports_needed:
                source_text = source_bytes.decode('utf8')
                
                # Check if typing import already exists
                has_typing_import = 'from typing import' in source_text or 'import typing' in source_text
                
                if not has_typing_import:
                    # Add the import at the beginning of the file
                    imports_str = ', '.join(sorted(typing_imports_needed))
                    import_statement = f"from typing import {imports_str}\n\n"
                    
                    # Find the position to insert (after any existing imports or at the start)
                    # For simplicity, we'll insert at the very beginning
                    transformer.add_change(
                        start_byte=0,
                        end_byte=0,
                        new_text=import_statement
                    )
                    print(f"  📦 Added typing import: {imports_str}")

    new_code = transformer.apply_changes()
    if in_place:
        if new_code != source_bytes:
            print("\n  💾 Saving changes to file...")
            try:
                with open(filepath, 'wb') as f:
                    f.write(new_code)
                print("  ✅ File updated successfully!")
            except IOError as e:
                print(f"  ❌ Error writing to file: {e}")
        else:
            print("\n  ℹ️  No changes needed for this file.")
    else:
        # Print to console if not in_place
        print("\n  👁️  Preview of Changes (Dry Run):")
        print(f"  {'─'*66}\n")
        print(new_code.decode('utf8'))


def run_autodoc(args):
    """The main entry point for running the analysis."""
    print(f"\n{'='*70}")
    print(f"  🤖 AutoDoc AI - Code Analysis & Enhancement")
    print(f"{'='*70}\n")
    
    # Show what features are enabled
    features = []
    if args.add_type_hints:
        features.append("Type Hints")
    if args.overwrite_existing:
        features.append("Docstring Improvement")
    if args.refactor:
        features.append("Code Refactoring")
    if not features:
        features.append("Docstring Generation")
    
    print(f"📋 Active Features: {', '.join(features)}")
    print(f"📝 Docstring Style: {args.style}")
    
    if args.diff:
        print(f"🔍 Mode: Git-changed files only\n")
        print("Scanning for modified files...")
        source_files = get_git_changed_files()
        if source_files is None: 
            print("❌ Error: Not a git repository or no changes found.")
            sys.exit(1)
    else:
        print(f"📂 Target: {args.path}\n")
        print("Scanning for source files...")
        source_files = get_source_files(args.path)
    
    if not source_files:
        print("\n⚠️  No source files found to process.")
        print("💡 Tip: Make sure you're in the right directory or specify a path.")
        return

    print(f"✓ Found {len(source_files)} file(s) to process.\n")
    
    # Show provider info
    provider = getattr(args, 'provider', None) or os.getenv('AUTODOC_PROVIDER', 'groq')
    model = getattr(args, 'model', None)
    if args.strategy != 'mock':
        print(f"🤖 Using: {provider.upper()}" + (f" ({model})" if model else ""))
        if not args.in_place:
            print(f"👁️  Mode: Dry-run (preview only - use --in-place to save changes)")
        else:
            print(f"💾 Mode: In-place (files will be modified)")
        print()
    
    try:
        generator = GeneratorFactory.create_generator(
            args.strategy,
            args.style,
            getattr(args, 'provider', None),
            getattr(args, 'model', None),
        )
    except ValueError as e:
        print(f"❌ Error: {e}")
        print(f"💡 Tip: Run 'autodoc init' to configure your provider.")
        sys.exit(1)

    print(f"{'─'*70}\n")
    
    for i, filepath in enumerate(source_files, 1):
        print(f"[{i}/{len(source_files)}] Processing: {filepath}")
        process_file_with_treesitter(
            filepath=filepath,
            generator=generator,
            in_place=args.in_place,
            overwrite_existing=args.overwrite_existing,
            add_type_hints=args.add_type_hints,
        )
        print(f"{'─'*70}\n")
    
    # Summary
    print(f"{'='*70}")
    print(f"  ✅ Processing Complete!")
    print(f"{'='*70}")
    print(f"\n📊 Summary:")
    print(f"  • Files processed: {len(source_files)}")
    print(f"  • Mode: {'Modified files' if args.in_place else 'Preview only'}")
    if not args.in_place:
        print(f"\n💡 To apply changes, add the --in-place flag")
    print(f"\n{'='*70}\n")


def main():
    """Main CLI entry point with subcommand routing."""
    parser = argparse.ArgumentParser(
        prog="autodoc",
        description="""
╔══════════════════════════════════════════════════════════════════════╗
║                   🤖 AutoDoc AI v0.1.4                               ║
║          AI-Powered Code Documentation & Enhancement Tool            ║
╚══════════════════════════════════════════════════════════════════════╝

AutoDoc AI automatically generates docstrings, adds type hints, and 
improves code quality using Large Language Models (LLMs).

Supports: Python, JavaScript, Java, Go, C++
        """,
        epilog="""
Examples:
  # First-time setup
  autodoc init

  # Add docstrings to a file (preview)
  autodoc run myfile.py

  # Add type hints and save changes
  autodoc run . --add-type-hints --in-place

  # Full quality pass on changed files
  autodoc run . --diff --add-type-hints --overwrite-existing --in-place

For more help: https://github.com/paudelnirajan/autodoc
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(
        dest="command",
        title="Available Commands",
        description="Choose a command to get started",
        help="Command description",
        required=True
    )

    # Init command
    parser_init = subparsers.add_parser(
        "init",
        help="Set up your LLM provider (Groq, OpenAI, Anthropic, Gemini)",
        description="Interactive wizard to configure your preferred AI provider and API key.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser_init.set_defaults(func=lambda args: init_config())

    # Run command
    config = load_config()
    parser_run = subparsers.add_parser(
        "run",
        help="Analyze and enhance your code with AI",
        description="""
Analyze source code files and apply AI-powered improvements:
  • Generate missing docstrings
  • Add type hints to functions
  • Improve existing documentation
  • Refactor poorly named variables/functions

By default, runs in preview mode. Use --in-place to save changes.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes for a single file
  autodoc run src/main.py

  # Add type hints to entire project
  autodoc run . --add-type-hints --in-place

  # Process only Git-changed files
  autodoc run . --diff --in-place

  # Use a specific provider
  autodoc run . --provider gemini --in-place
        """
    )
    
    parser_run.add_argument(
        "path",
        nargs='?',
        default='.',
        help="File or directory to process (default: current directory)"
    )
    
    parser_run.add_argument(
        "--diff",
        action="store_true",
        help="Only process files changed in Git (useful for pre-commit hooks)"
    )
    
    parser_run.add_argument(
        "--strategy",
        choices=["mock", "groq"],
        default=config.get('strategy', 'mock'),
        help="Use 'groq' for real LLM, 'mock' for testing without API calls"
    )
    
    parser_run.add_argument(
        "--style",
        choices=["google", "numpy", "rst"],
        default=config.get('style', 'google'),
        help="Docstring format style (google=Google-style, numpy=NumPy-style, rst=Sphinx)"
    )
    
    parser_run.add_argument(
        "--in-place",
        action="store_true",
        help="⚠️  Modify files directly (default: preview only)"
    )
    
    parser_run.add_argument(
        "--overwrite-existing",
        action="store_true",
        help="Regenerate poor-quality docstrings that already exist"
    )
    
    parser_run.add_argument(
        "--refactor",
        action="store_true",
        help="Enable AI-powered refactoring (rename variables/functions)"
    )
    
    parser_run.add_argument(
        "--provider",
        choices=["groq", "openai", "anthropic", "gemini"],
        default=None,
        help="LLM provider to use (default: reads from .env AUTODOC_PROVIDER)"
    )
    
    parser_run.add_argument(
        "--model",
        default=None,
        metavar="MODEL_NAME",
        help="Override default model (e.g., gpt-4, claude-3-5-sonnet-latest, gemini-1.5-pro)"
    )
    
    parser_run.add_argument(
        "--add-type-hints",
        action="store_true",
        help="Generate and add Python type hints to functions (infers types from code)"
    )

    parser_run.set_defaults(func=run_autodoc)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()