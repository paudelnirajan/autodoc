TAX_RATE = 0.15
MINIMUM_PRICE_FOR_DISCOUNT = 100
DISCOUNT_MULTIPLIER = 0.9
DEFAULT_TIMEOUT_SECONDS = 30
PI = 3.14159

def calculate_tax(amount: float) -> float:
    """Calculate tax on an amount."""
    return amount * TAX_RATE


def calculate_discount(price: float) -> float:
    """Calculate discounted price."""
    if price > MINIMUM_PRICE_FOR_DISCOUNT:
        return price * DISCOUNT_MULTIPLIER
    return price


def retry_connection(max_attempts: int = 3) -> None:
    """Retry connection with timeout."""
    for i in range(max_attempts):
        # Try to connect with 30 second timeout
        timeout = DEFAULT_TIMEOUT_SECONDS
        # ... connection logic
        pass


def calculate_circle_area(radius: float) -> float:
    """Calculate area of a circle."""
    return PI * radius * radius
