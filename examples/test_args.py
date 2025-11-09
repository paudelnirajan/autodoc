from typing import Any

def bad_func(x: Any, y: Any) -> Any:
    """
    Calculates the sum of two numbers.

        While primarily intended for numeric types, this function can also be used
        for other types that support the addition operator, such as strings or lists
        (for concatenation).

        Args:
            x (int or float): The first addend.
            y (int or float): The second addend.

        Returns:
            The sum of x and y. The return type will depend on the input types.

        Raises:
            TypeError: If the arguments are of types that cannot be added together.
    """
    return x + y

class MyClass:
    def method(self, a: Any, b: Any) -> Any:
        """
        Multiplies two numbers together.

            Args:
                a (int or float): The first number.
                b (int or float): The second number.

            Returns:
                int or float: The product of a and b.
        """
        temp = a * b
        return temp
