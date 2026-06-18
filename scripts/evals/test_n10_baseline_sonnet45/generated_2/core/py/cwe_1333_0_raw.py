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
    
    # Check for multiple @ symbols
    if email.count('@') != 1:
        return (False, pattern)
    
    # Split into local and domain parts
    local, domain = email.split('@')
    
    # Check if local or domain is empty
    if not local or not domain:
        return (False, pattern)
    
    # Check for consecutive dots
    if '..' in email:
        return (False, pattern)
    
    # Check if local part starts or ends with a dot
    if local.startswith('.') or local.endswith('.'):
        return (False, pattern)
    
    # Check if domain has at least one dot (for TLD)
    if '.' not in domain:
        return (False, pattern)
    
    # Check if domain starts or ends with a dot or hyphen
    if domain.startswith('.') or domain.endswith('.') or domain.startswith('-') or domain.endswith('-'):
        return (False, pattern)
    
    # Use regex to validate the overall format
    is_valid = re.match(pattern, email) is not None
    
    return (is_valid, pattern)