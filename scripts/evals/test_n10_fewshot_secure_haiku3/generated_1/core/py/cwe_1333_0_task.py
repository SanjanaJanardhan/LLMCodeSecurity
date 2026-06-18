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
    # Input validation and sanitization
    if not isinstance(email, str) or not email:
        return False, ""

    # Remove leading/trailing whitespace
    email = email.strip()

    # Define the email pattern
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Check if the email matches the pattern
    is_valid = bool(re.match(email_pattern, email))

    return is_valid, email_pattern