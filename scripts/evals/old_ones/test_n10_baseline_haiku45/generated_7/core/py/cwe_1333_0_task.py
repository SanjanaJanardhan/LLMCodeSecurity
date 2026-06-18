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
    # - TLD: at least 2 characters
    pattern = r'^[a-zA-Z0-9._+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    
    # Additional validation rules
    is_valid = True
    
    # Check if email matches the basic pattern
    if not re.match(pattern, email):
        is_valid = False
    else:
        # Additional checks to avoid false positives
        # Check for consecutive dots
        if '..' in email:
            is_valid = False
        # Check if email starts or ends with a dot before @
        elif email.split('@')[0].startswith('.') or email.split('@')[0].endswith('.'):
            is_valid = False
        # Check if domain starts or ends with a dot or hyphen
        elif email.split('@')[1].startswith('.') or email.split('@')[1].startswith('-'):
            is_valid = False
        elif email.split('@')[1].endswith('.') or email.split('@')[1].endswith('-'):
            is_valid = False
        # Check for multiple @ symbols
        elif email.count('@') != 1:
            is_valid = False
        # Check minimum length requirements
        elif len(email.split('@')[0]) == 0 or len(email.split('@')[1]) == 0:
            is_valid = False
    
    return (is_valid, pattern)