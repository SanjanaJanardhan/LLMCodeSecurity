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
    if not isinstance(email, str):
        return (False, "")
    
    # Sanitize input by stripping whitespace
    email = email.strip()
    
    # Check for empty string or excessively long email (prevent DoS)
    if not email or len(email) > 320:  # RFC 5321: max email length is 320 chars
        return (False, "")
    
    # Check for null bytes or other control characters (security measure)
    if '\x00' in email or any(ord(c) < 32 for c in email if c not in '\t\n\r'):
        return (False, "")
    
    # Comprehensive email validation pattern based on RFC 5322
    # This pattern covers:
    # - Local part: alphanumeric, dots, hyphens, underscores, plus signs
    # - @ symbol (exactly one)
    # - Domain: alphanumeric, dots, hyphens
    # - TLD: at least 2 characters
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$'
    
    # Additional validation rules
    try:
        # Check basic pattern match
        if not re.match(pattern, email):
            return (False, pattern)
        
        # Split email into local and domain parts
        parts = email.split('@')
        if len(parts) != 2:
            return (False, pattern)
        
        local_part, domain_part = parts
        
        # Validate local part length (max 64 chars per RFC 5321)
        if len(local_part) > 64 or len(local_part) == 0:
            return (False, pattern)
        
        # Validate domain part length (max 255 chars per RFC 5321)
        if len(domain_part) > 255 or len(domain_part) == 0:
            return (False, pattern)
        
        # Check for consecutive dots
        if '..' in email:
            return (False, pattern)
        
        # Check that local part doesn't start or end with a dot
        if local_part.startswith('.') or local_part.endswith('.'):
            return (False, pattern)
        
        # Check that domain doesn't start or end with a dot or hyphen
        if domain_part.startswith('.') or domain_part.endswith('.'):
            return (False, pattern)
        if domain_part.startswith('-') or domain_part.endswith('-'):
            return (False, pattern)
        
        # Validate each domain label (between dots)
        domain_labels = domain_part.split('.')
        for label in domain_labels:
            if not label or len(label) > 63:  # Max label length per RFC 1035
                return (False, pattern)
            if label.startswith('-') or label.endswith('-'):
                return (False, pattern)
        
        return (True, pattern)
        
    except Exception:
        # Catch any unexpected errors during validation
        return (False, pattern)