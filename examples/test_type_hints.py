from typing import Any, Dict, List, Optional, Union

def calculate_sum(a: float, b: float) -> float:
    """Calculate the sum of two numbers."""
    return a + b


def greet_user(name: str, age: int) -> str:
    """Greet a user with their name and age."""
    message = f"Hello {name}, you are {age} years old!"
    return message


def process_data(items: List[Union[int, float]], multiplier: Union[int, float] = 2) -> List[Union[int, float]]:
    """Process a list of items by multiplying each by a factor."""
    result = []
    for item in items:
        result.append(item * multiplier)
    return result


def find_max(numbers: List[Union[int, float]]) -> Optional[Union[int, float]]:
    """Find the maximum number in a list."""
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val


def create_user_dict(username: str, email: str, is_active: bool = True) -> Dict[str, Any]:
    """Create a dictionary representing a user."""
    return {
        "username": username,
        "email": email,
        "is_active": is_active
    }
