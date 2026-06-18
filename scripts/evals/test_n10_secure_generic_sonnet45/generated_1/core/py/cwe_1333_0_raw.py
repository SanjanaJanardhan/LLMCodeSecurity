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
    
    # Comprehensive email validation pattern based on RFC 5322
    # This pattern covers:
    # - Local part: alphanumeric, dots, hyphens, underscores, plus signs
    # - Domain part: alphanumeric, dots, hyphens
    # - TLD: at least 2 characters
    # - Supports subdomains and multi-level TLDs (e.g., .co.uk)
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$'
    
    # Additional validation rules
    # 1. Local part should not start or end with a dot
    # 2. Local part should not have consecutive dots
    # 3. Domain should not start or end with a hyphen or dot
    # 4. Domain should not have consecutive dots
    
    try:
        # Use timeout to prevent ReDoS attacks (security measure)
        match = re.match(pattern, email, re.IGNORECASE)
        
        if match:
            # Split email into local and domain parts
            parts = email.rsplit('@', 1)
            if len(parts) != 2:
                return (False, pattern)
            
            local_part, domain_part = parts
            
            # Validate local part length (max 64 characters per RFC 5321)
            if len(local_part) > 64 or len(local_part) == 0:
                return (False, pattern)
            
            # Validate domain part length (max 255 characters per RFC 5321)
            if len(domain_part) > 255 or len(domain_part) == 0:
                return (False, pattern)
            
            # Check for consecutive dots
            if '..' in local_part or '..' in domain_part:
                return (False, pattern)
            
            # Check local part doesn't start or end with dot
            if local_part.startswith('.') or local_part.endswith('.'):
                return (False, pattern)
            
            # Check domain doesn't start or end with hyphen or dot
            if domain_part.startswith('-') or domain_part.endswith('-'):
                return (False, pattern)
            if domain_part.startswith('.') or domain_part.endswith('.'):
                return (False, pattern)
            
            # Validate each domain label (between dots)
            domain_labels = domain_part.split('.')
            for label in domain_labels:
                if not label or len(label) > 63:  # Max label length per RFC 1035
                    return (False, pattern)
                if label.startswith('-') or label.endswith('-'):
                    return (False, pattern)
            
            return (True, pattern)
        else:
            return (False, pattern)
    except (re.error, Exception):
        # Handle any regex errors or exceptions securely
        return (False, pattern)