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
    # Comprehensive email validation pattern
    # This pattern covers:
    # - Local part: alphanumeric, dots, hyphens, underscores, plus signs
    # - @ symbol (required)
    # - Domain: alphanumeric, hyphens, dots
    # - TLD: at least 2 characters
    # - Supports multiple subdomains (e.g., .co.uk, .com.au)
    
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
    
    # Additional validation checks
    if not email or '@' not in email:
        return (False, pattern)
    
    # Check for basic structure
    parts = email.split('@')
    if len(parts) != 2:
        return (False, pattern)
    
    local_part, domain_part = parts
    
    # Local part should not be empty and should not start/end with dot
    if not local_part or local_part.startswith('.') or local_part.endswith('.'):
        return (False, pattern)
    
    # Domain part should contain at least one dot and not start/end with dot or hyphen
    if not domain_part or '.' not in domain_part:
        return (False, pattern)
    
    if domain_part.startswith('.') or domain_part.endswith('.'):
        return (False, pattern)
    
    if domain_part.startswith('-') or domain_part.endswith('-'):
        return (False, pattern)
    
    # Check for consecutive dots
    if '..' in email:
        return (False, pattern)
    
    # Use regex for final validation
    is_valid = bool(re.match(pattern, email))
    
    return (is_valid, pattern)