from typing import Union

def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Adds two numbers together.

        Args:
            a (int or float): The first number to be added.
            b (int or float): The second number to be added.

        Returns:
            int or float: The sum of `a` and `b`.

        Raises:
            TypeError: If the input arguments are not of a type that supports
                the addition operator.
    """
    return a + b
