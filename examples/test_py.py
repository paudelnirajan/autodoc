
PI = 3.1415
abc = 234

def area_of_circle(a: float, b: Any) -> float:
    """
    Calculates the circumference of a circle.

        Note: This function is misnamed and contains unused variables. It
        calculates the circumference (2 * PI * r), not the area. It also
        depends on a globally-defined constant `PI`.

        Args:
            a (Union[int, float]): The radius of the circle.
            b (Any): An unused parameter.

        Returns:
            float: The circumference of the circle.

        Raises:
            NameError: If the global constant `PI` is not defined.
    """
    xyz = 345
    return 2 * PI * a
