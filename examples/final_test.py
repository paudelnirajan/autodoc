from typing import Any, Dict, List

def get_user_info(user_id: Any) -> Dict[str, Any]:
    """Fetch user information from database."""
    return {"id": user_id, "name": "John", "active": True}


def filter_items(items: List[Any], min_value: Any) -> List[Any]:
    """Filter items above a minimum value."""
    result = []
    for item in items:
        if item > min_value:
            result.append(item)
    return result


def validate_email(email: str) -> bool:
    """Check if email format is valid."""
    return "@" in email and "." in email
