import ast
import argparse
import sys
from src.ast_handler import CodeQualityVisitor
from src.generators import GeneratorFactory, IDocStringGenerator

def main(filepath: str, in_place: bool, strategy: str, overwrite_existing: bool):
    """
    Reads a Python file, runs the code quality visitor, and either
    prints the modified code or writes it back to the file.
    """
    print(f"Analyzing {filepath} with '{strategy}' strategy...")
    if overwrite_existing:
        print("Overwrite existing docstrings is ENABLED.")
        
    try:
        with open(filepath, 'r') as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        sys.exit(1)

    tree = ast.parse(source_code)
    
    try:
        generator: IDocStringGenerator = GeneratorFactory.create_generator(strategy)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    visitor = CodeQualityVisitor(
        generator=generator, 
        overwrite_existing=overwrite_existing
    )
    visitor.visit(tree)

    print("\n--- Analysis Complete ---")

    if visitor.tree_modified:
        new_code = ast.unparse(tree)
        
        if in_place:
            print(f"\nWriting changes back to {filepath}...")
            try:
                with open(filepath, 'w') as file:
                    file.write(new_code)
                print("Done.")
            except IOError as e:
                print(f"Error writing to file: {e}")
        else:
            print("\nCode has been modified. New source code (use flags to save):")
            print("-" * 40)
            print(new_code)
            print("-" * 40)
    else:
        print("\nNo code modifications were made.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyzes and automatically documents Python files."
    )
    parser.add_argument("filepath", help="The path to the Python file to process.")
    parser.add_argument(
        "--strategy",
        choices=["mock", "groq"],
        default="mock",
        help="The docstring generation strategy to use."
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Modify the file in place."
    )

    parser.add_argument(
        "--overwrite-existing",
        action="store_true",
        help="Regenerate docstrings that are deemed 'poor quality' by the AI."
    )
    
    args = parser.parse_args()
    
    main(
        filepath=args.filepath, 
        in_place=args.in_place, 
        strategy=args.strategy,
        overwrite_existing=args.overwrite_existing
    )