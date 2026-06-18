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
    
    # Input validation: ensure email is a string and not excessively long
    if not isinstance(email, str):
        return False, ""
    
    # RFC 5321 specifies max email length of 254 characters
    if len(email) > 254 or len(email) == 0:
        return False, ""
    
    # Strip whitespace to prevent bypass attempts
    email = email.strip()
    
    # RFC 5322 compliant email regex pattern
    # This pattern covers:
    # - Local part: alphanumeric, dots, hyphens, underscores, plus signs
    # - Domain: alphanumeric, dots, hyphens
    # - TLD: at least 2 characters
    pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    
    # Validate against pattern
    if not re.match(pattern, email):
        return False, pattern
    
    # Additional validation checks
    # Check for consecutive dots
    if '..' in email:
        return False, pattern
    
    # Split email into local and domain parts
    parts = email.rsplit('@', 1)
    if len(parts) != 2:
        return False, pattern
    
    local_part, domain_part = parts
    
    # Validate local part length (max 64 characters per RFC 5321)
    if len(local_part) > 64 or len(local_part) == 0:
        return False, pattern
    
    # Local part cannot start or end with a dot
    if local_part.startswith('.') or local_part.endswith('.'):
        return False, pattern
    
    # Validate domain part
    if len(domain_part) == 0:
        return False, pattern
    
    # Domain must have at least one dot and valid TLD
    if '.' not in domain_part:
        return False, pattern
    
    # Domain cannot start or end with a dot or hyphen
    if domain_part.startswith('.') or domain_part.startswith('-'):
        return False, pattern
    if domain_part.endswith('.') or domain_part.endswith('-'):
        return False, pattern
    
    # Validate each domain label
    domain_labels = domain_part.split('.')
    for label in domain_labels:
        if len(label) == 0 or len(label) > 63:
            return False, pattern
        if label.startswith('-') or label.endswith('-'):
            return False, pattern
    
    # TLD must be at least 2 characters and contain only letters
    tld = domain_labels[-1]
    if len(tld) < 2 or not tld.isalpha():
        return False, pattern
    
    return True, pattern