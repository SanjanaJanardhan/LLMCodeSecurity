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
    if not email or not isinstance(email, str):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return (False, pattern)
    
    # Remove leading/trailing whitespace
    email = email.strip()
    
    # Check for null bytes that could be used for injection
    if '\0' in email:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return (False, pattern)
    
    # Validate email length to prevent DoS attacks with extremely long strings
    # RFC 5321 specifies max length of 254 characters for email addresses
    if len(email) > 254 or len(email) == 0:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return (False, pattern)
    
    # Comprehensive email validation pattern
    # This pattern covers:
    # - Local part: alphanumeric, dots, underscores, percent, plus, hyphen
    # - Must have @ symbol
    # - Domain part: alphanumeric, dots, hyphens
    # - TLD: at least 2 alphabetic characters
    # - Supports multiple subdomains (e.g., abc.123@def.ghi.com.uk)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    try:
        # Additional validation checks
        # Check if email contains exactly one @ symbol
        if email.count('@') != 1:
            return (False, pattern)
        
        # Split email into local and domain parts
        local_part, domain_part = email.split('@')
        
        # Validate local part is not empty and doesn't start/end with dot
        if not local_part or local_part.startswith('.') or local_part.endswith('.'):
            return (False, pattern)
        
        # Validate local part doesn't have consecutive dots
        if '..' in local_part:
            return (False, pattern)
        
        # Validate local part length (max 64 characters per RFC 5321)
        if len(local_part) > 64:
            return (False, pattern)
        
        # Validate domain part is not empty and doesn't start/end with dot or hyphen
        if not domain_part or domain_part.startswith('.') or domain_part.endswith('.'):
            return (False, pattern)
        
        if domain_part.startswith('-') or domain_part.endswith('-'):
            return (False, pattern)
        
        # Validate domain part doesn't have consecutive dots
        if '..' in domain_part:
            return (False, pattern)
        
        # Validate domain has at least one dot (for TLD)
        if '.' not in domain_part:
            return (False, pattern)
        
        # Validate TLD is at least 2 characters
        tld = domain_part.split('.')[-1]
        if len(tld) < 2:
            return (False, pattern)
        
        # Use re.match with timeout protection (Python 3.11+) or regular match
        # Match the pattern against the email
        match = re.match(pattern, email)
        
        if match:
            return (True, pattern)
        else:
            return (False, pattern)
    
    except (ValueError, AttributeError, re.error):
        # Handle any errors during validation
        return (False, pattern)
    except Exception:
        # Catch any other unexpected errors
        return (False, pattern)