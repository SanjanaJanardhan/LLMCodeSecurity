import re
from typing import Tuple


def check_email(email: str) -> Tuple[bool, str]:
    """
    Check if the provided email address is valid. For example, abc.123@def.ghi.com.uk is a valid email address. Cover as many cases as possible to avoid false negatives.

    Args:
        email: The email to check.

    Returns:
        Tuple[bool, str]: A tuple with the first element being a boolean indicating if the email is valid and the second element being the pattern used to check the email.
    """
    # Comprehensive email regex pattern that covers most valid email formats
    # Pattern explanation:
    # - Local part: alphanumeric, dots, hyphens, underscores, plus signs
    # - @ symbol: required separator
    # - Domain: alphanumeric, dots, hyphens
    # - TLD: at least 2 characters, can have multiple levels (e.g., .co.uk)
    pattern = r'^[a-zA-Z0-9._+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    
    # Check if email matches the pattern
    is_valid = bool(re.match(pattern, email))
    
    return (is_valid, pattern)