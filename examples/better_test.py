LEGAL_ADULT_AGE = 18

def calculate_average(numbers: List[Union[int, float]]) -> float:
    """Calculate the average of a list of numbers."""
    total = sum(numbers)
    count = len(numbers)
    return total / count


def format_name(first_name: str, last_name: str) -> str:
    """Format a person's full name."""
    return f"{first_name} {last_name}"


def is_adult(age: int) -> bool:
    """Check if a person is an adult."""
    return age >= LEGAL_ADULT_AGE
