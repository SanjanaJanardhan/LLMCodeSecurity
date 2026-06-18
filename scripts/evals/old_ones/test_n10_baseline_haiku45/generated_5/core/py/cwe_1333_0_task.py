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
    
    # Additional validation rules to avoid false positives
    is_valid = False
    
    if re.match(pattern, email):
        # Check for consecutive dots
        if '..' not in email:
            # Check that email doesn't start or end with a dot or hyphen in local part
            local_part = email.split('@')[0]
            domain_part = email.split('@')[1]
            
            if not local_part.startswith('.') and not local_part.endswith('.'):
                if not local_part.startswith('-') and not local_part.endswith('-'):
                    if not domain_part.startswith('.') and not domain_part.startswith('-'):
                        if not domain_part.endswith('.') and not domain_part.endswith('-'):
                            # Check that there's at least one character in local and domain parts
                            if len(local_part) > 0 and len(domain_part) > 0:
                                is_valid = True
    
    return (is_valid, pattern)