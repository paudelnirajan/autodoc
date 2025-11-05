"""
This is a module-level docstring.
"""
import os

class MyClass:
    """This is a documented class."""

    def __init__(self):
        """Initializes the object.

Sets the initial state of the object by assigning a default value."""
        self.value = 1

    def documented_method(self, x):
        """Multiples the input by the instance's value.

Args:
    x: The number to multiply by the instance's value.

Returns:
    The product of the input and the instance's value.

Note:
    This method relies on the instance having a 'value' attribute."""
        return x * self.value

    def undocumented_method(self, y):
        """Returns the input value incremented by 1.

Args:
    y (int): The input value to be incremented.

Returns:
    int: The input value incremented by 1."""
        return y + 1

def documented_function(a, b):
    """Adds two numbers together.

Args:
    a (int): The first number to add.
    b (int): The second number to add.

Returns:
    int: The sum of a and b."""
    return a + b

def undocumented_function(c, d):
    """Subtracts two input values.

Args:
    c (int or float): The minuend value.
    d (int or float): The subtrahend value.

Returns:
    int or float: The result of subtracting d from c."""
    return c - d