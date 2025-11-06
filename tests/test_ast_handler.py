import ast
import pytest
from src.ast_handler import CodeQualityVisitor
from src.generators import IDocstringGenerator

class ConfigurableMockGenerator(IDocstringGenerator):
    """
    A mock generator for testing that allows us to configure
    its evaluation response.
    """
    def __init__(self, is_good_docstring: bool):
        self._is_good = is_good_docstring

    def generate(self, node: ast.AST) -> str:
        return "This is a new, generated docstring."

    def evaluate(self, node: ast.AST, docstring: str) -> bool:
        return self._is_good

def test_visitor_adds_docstring_to_function():
    """
    Tests that the visitor correctly identifies a function without a docstring and injects a new line
    """
    source_code = "def my_function(a, b):\n    return a + b"

    tree = ast.parse(source_code)

    visitor = CodeQualityVisitor(generator=ConfigurableMockGenerator(is_good_docstring=True))
    visitor.visit(tree)

    assert visitor.tree_modified is True

    function_node = tree.body[0]
    new_docstring = ast.get_docstring(function_node)
    assert new_docstring is not None
    assert new_docstring == "This is a new, generated docstring."

def test_visitor_ignores_existing_docstring_by_default():
    """
    Tests that the visitor does NOT change a function that already
    has a docstring if 'overwrite_existing' is False.
    """
    source_code = 'def my_function():\n    """An existing docstring."""\n    pass'
    tree = ast.parse(source_code)
    visitor = CodeQualityVisitor(
        generator=ConfigurableMockGenerator(is_good_docstring=False),
        overwrite_existing=False  
    )

    visitor.visit(tree)

    assert visitor.tree_modified is False
    function_node = tree.body[0]
    docstring = ast.get_docstring(function_node)
    assert docstring == "An existing docstring."

def test_visitor_replaces_poor_docstring_when_overwrite_is_enabled():
    """
    Tests that the visitor REPLACES a poor quality docstring when
    'overwrite_existing' is True.
    """
    source_code = 'def my_function():\n    """TODO: write this."""\n    pass'
    tree = ast.parse(source_code)
    generator = ConfigurableMockGenerator(is_good_docstring=False)
    visitor = CodeQualityVisitor(generator=generator, overwrite_existing=True)

    visitor.visit(tree)

    assert visitor.tree_modified is True
    function_node = tree.body[0]
    docstring = ast.get_docstring(function_node)
    assert docstring == "This is a new, generated docstring."

def test_visitor_leaves_good_docstring_when_overwrite_is_enabled():
    """
    Tests that the visitor LEAVES a good quality docstring alone, even
    when 'overwrite_existing' is True.
    """
    source_code = 'def my_function():\n    """A perfectly fine docstring."""\n    pass'
    tree = ast.parse(source_code)
    generator = ConfigurableMockGenerator(is_good_docstring=True)
    visitor = CodeQualityVisitor(generator=generator, overwrite_existing=True)

    visitor.visit(tree)

    assert visitor.tree_modified is False
    function_node = tree.body[0]
    docstring = ast.get_docstring(function_node)
    assert docstring == "A perfectly fine docstring."