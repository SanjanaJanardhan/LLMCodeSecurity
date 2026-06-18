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
    # - Domain: alphanumeric, dots, hyphens
    # - TLD: at least 2 characters
    # - Supports multiple subdomains (e.g., .co.uk, .com.au)
    
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
    
    # Alternative pattern for single character local parts or domains
    alternative_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$'
    
    # Use the alternative pattern which is more flexible
    pattern = alternative_pattern
    
    # Additional checks to avoid false negatives:
    # 1. Cannot have consecutive dots
    # 2. Cannot start or end with dot in local part (before @)
    # 3. Cannot have spaces
    
    if not email or ' ' in email:
        return (False, pattern)
    
    # Check for @ symbol
    if email.count('@') != 1:
        return (False, pattern)
    
    # Split into local and domain parts
    parts = email.split('@')
    if len(parts) != 2:
        return (False, pattern)
    
    local_part, domain_part = parts
    
    # Check local part
    if not local_part or len(local_part) == 0:
        return (False, pattern)
    
    # Check domain part
    if not domain_part or '.' not in domain_part:
        return (False, pattern)
    
    # Check for consecutive dots
    if '..' in email:
        return (False, pattern)
    
    # Check if local part starts or ends with dot
    if local_part.startswith('.') or local_part.endswith('.'):
        return (False, pattern)
    
    # Check if domain starts or ends with dot or hyphen
    if domain_part.startswith('.') or domain_part.endswith('.'):
        return (False, pattern)
    if domain_part.startswith('-') or domain_part.endswith('-'):
        return (False, pattern)
    
    # Use regex to validate
    is_valid = re.match(pattern, email) is not None
    
    return (is_valid, pattern)