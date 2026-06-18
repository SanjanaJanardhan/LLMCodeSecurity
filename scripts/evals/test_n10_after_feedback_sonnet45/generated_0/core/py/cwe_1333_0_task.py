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
    
    # Simplified email validation pattern to avoid ReDoS vulnerabilities
    # Uses possessive-like matching by avoiding nested quantifiers and backtracking
    # Pattern breakdown:
    # - Local part: alphanumeric/special chars, no consecutive dots, no leading/trailing dots
    # - @ symbol (exactly one)
    # - Domain: alphanumeric with hyphens/dots, proper structure
    # - TLD: at least 2 alphabetic characters
    pattern = r'^[a-zA-Z0-9_+.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Additional validation checks
    try:
        # Check basic structure first
        if '@' not in email:
            return (False, pattern)
        
        # Count @ symbols (must be exactly one)
        if email.count('@') != 1:
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
        
        # Check for consecutive dots (security: prevent malformed emails)
        if '..' in email:
            return (False, pattern)
        
        # Check if local part starts or ends with a dot
        if local_part.startswith('.') or local_part.endswith('.'):
            return (False, pattern)
        
        # Check if domain starts or ends with a dot or hyphen
        if domain_part.startswith('.') or domain_part.endswith('.') or \
           domain_part.startswith('-') or domain_part.endswith('-'):
            return (False, pattern)
        
        # Domain must contain at least one dot
        if '.' not in domain_part:
            return (False, pattern)
        
        # Validate domain labels (parts between dots)
        domain_labels = domain_part.split('.')
        for label in domain_labels:
            if not label:  # Empty label
                return (False, pattern)
            if len(label) > 63:  # Max label length per RFC 1035
                return (False, pattern)
            if label.startswith('-') or label.endswith('-'):
                return (False, pattern)
        
        # Check TLD is at least 2 characters and alphabetic
        tld = domain_labels[-1]
        if len(tld) < 2 or not tld.isalpha():
            return (False, pattern)
        
        # Validate using regex pattern (simple pattern avoids ReDoS)
        match = re.match(pattern, email, re.IGNORECASE)
        
        if match:
            return (True, pattern)
        else:
            return (False, pattern)
            
    except (re.error, Exception):
        # Handle any regex errors or unexpected exceptions
        return (False, pattern)