import ast
from src.generators import IDocStringGenerator

class CodeQualityVisitor(ast.NodeVisitor):
    """
    An AST visitor that finds common code quality issues like missing docstrings, magic numbers, and pooly named variables and can inject proper docstrings where they are missing.
    """

    ALLOWED_SHORT_NAMES = {'i', 'j', 'k', 'x', 'y', 'z', 'id'}

    def __init__(self, generator: IDocStringGenerator = None, overwrite_existing: bool = False):
        self.generator = generator
        self.overwrite_existing = overwrite_existing
        self.tree_modified = False

    def _process_node_for_docstring(self, node: ast.FunctionDef | ast.ClassDef):
        """Processes a function or class node for docstring generation/replacement."""
        existing_docstring = ast.get_docstring(node)

        if not existing_docstring:
            self._inject_docstring(node)
            return

        if self.overwrite_existing and self.generator and hasattr(self.generator, 'evaluate'):
            is_good = self.generator.evaluate(node, existing_docstring)
            if not is_good:
                print(f"L{node.lineno}:[Docstring] Found poor quality docstring for '{node.name}'. Regenerating.")
                
                if node.body and isinstance(node.body[0], ast.Expr):
                    node.body.pop(0)
                
                self._inject_docstring(node)

    def _inject_docstring(self, node: ast.FunctionDef | ast.ClassDef):
        """Helper to generate and insert a docstring into a node."""
        if self.generator:
            print(f"L{node.lineno}:[Docstring] Generating docstring for '{node.name}'.")

            docstring_text = self.generator.generate(node)
            docstring_node = ast.Expr(value=ast.Constant(value=docstring_text))

            node.body.insert(0, docstring_node)
            self.tree_modified = True
        else:
            print(f"L{node.lineno}:[Docstring] '{node.name}' is missing a docstring.")

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._process_node_for_docstring(node)
        
        # TODO: current implementation just checks for the short length characters which might have meaning and be good names...need to change this logic sth GOOD.
        for arg in node.args.args:
            if len(arg.arg) < 3 and arg.arg not in self.ALLOWED_SHORT_NAMES:
                print(f"L{arg.lineno}:[Naming] Argument '{arg.arg}' in function '{node.name}' is too short.")

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        if not ast.get_docstring(node):
            self._inject_docstring(node)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, (int, float)) and node.value not in {0, 1, -1}:
            print(f"L{node.lineno}:[Magic Number] Found a magic number: {node.value}.")
        self.generic_visit(node)
        
    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Store) and len(node.id) < 3 and node.id not in self.ALLOWED_SHORT_NAMES:
            print(f"L{node.lineno}:[Naming] Variable name '{node.id}' is too short.")
        self.generic_visit(node)