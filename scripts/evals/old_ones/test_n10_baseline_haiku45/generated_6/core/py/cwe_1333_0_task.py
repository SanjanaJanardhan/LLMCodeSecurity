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
    # Pattern breakdown:
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
    
    # Additional checks to avoid false negatives
    if is_valid:
        # Check for consecutive dots
        if '..' in email:
            is_valid = False
        
        # Check if email starts or ends with a dot or hyphen (in local part)
        local_part = email.split('@')[0]
        if local_part.startswith('.') or local_part.startswith('-') or \
           local_part.endswith('.') or local_part.endswith('-'):
            is_valid = False
        
        # Check domain part
        domain_part = email.split('@')[1]
        if domain_part.startswith('-') or domain_part.endswith('-') or \
           domain_part.startswith('.') or domain_part.endswith('.'):
            is_valid = False
        
        # Check for consecutive hyphens in domain
        if '--' in domain_part:
            is_valid = False
    
    return (is_valid, pattern)