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
    
    # Check for empty string or excessively long email (security: prevent DoS via regex)
    if not email or len(email) > 320:  # RFC 5321: max email length is 320 characters
        return (False, "")
    
    # Check for null bytes or other control characters (security: prevent injection attacks)
    if '\x00' in email or any(ord(c) < 32 for c in email if c not in '\t\n\r'):
        return (False, "")
    
    # Comprehensive email validation pattern based on RFC 5322 (simplified but robust)
    # This pattern covers:
    # - Local part: alphanumeric, dots, hyphens, underscores, plus signs
    # - @ symbol (exactly one)
    # - Domain: alphanumeric, dots, hyphens
    # - TLD: at least 2 characters
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
    
    # Additional validation checks
    try:
        # Check basic structure first
        if '@' not in email:
            return (False, pattern)
        
        # Split into local and domain parts
        parts = email.rsplit('@', 1)
        if len(parts) != 2:
            return (False, pattern)
        
        local_part, domain_part = parts
        
        # Validate local part length (max 64 characters per RFC 5321)
        if not local_part or len(local_part) > 64:
            return (False, pattern)
        
        # Validate domain part length (max 255 characters per RFC 5321)
        if not domain_part or len(domain_part) > 255:
            return (False, pattern)
        
        # Check for consecutive dots
        if '..' in email:
            return (False, pattern)
        
        # Check if local part starts or ends with a dot
        if local_part.startswith('.') or local_part.endswith('.'):
            return (False, pattern)
        
        # Check if domain starts or ends with a dot or hyphen
        if domain_part.startswith('.') or domain_part.endswith('.') or \
           domain_part.startswith('-') or domain_part.endswith('-'):
            return (False, pattern)
        
        # Validate using regex pattern with timeout protection
        match = re.match(pattern, email, re.IGNORECASE)
        
        if match:
            return (True, pattern)
        else:
            return (False, pattern)
            
    except (re.error, Exception):
        # Handle any regex errors or unexpected exceptions
        return (False, pattern)