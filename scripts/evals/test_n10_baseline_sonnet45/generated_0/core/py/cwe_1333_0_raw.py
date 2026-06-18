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
    # - Supports multiple subdomains and multi-level TLDs (e.g., .co.uk)
    
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
    
    # Alternative pattern for single character local parts
    single_char_pattern = r'^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
    
    # Check if email is None or empty
    if not email or not isinstance(email, str):
        return (False, pattern)
    
    # Strip whitespace
    email = email.strip()
    
    # Basic length check
    if len(email) < 5 or len(email) > 320:  # RFC 5321 max length
        return (False, pattern)
    
    # Check for @ symbol
    if email.count('@') != 1:
        return (False, pattern)
    
    # Split into local and domain parts
    local, domain = email.rsplit('@', 1)
    
    # Check local part
    if not local or len(local) > 64:  # RFC 5321 local part max length
        return (False, pattern)
    
    # Check domain part
    if not domain or len(domain) > 255:  # RFC 5321 domain max length
        return (False, pattern)
    
    # Check for consecutive dots
    if '..' in email:
        return (False, pattern)
    
    # Check if local part starts or ends with a dot
    if local.startswith('.') or local.endswith('.'):
        return (False, pattern)
    
    # Check if domain has at least one dot
    if '.' not in domain:
        return (False, pattern)
    
    # Check if domain starts or ends with a dot or hyphen
    if domain.startswith('.') or domain.endswith('.') or domain.startswith('-') or domain.endswith('-'):
        return (False, pattern)
    
    # Try matching with the main pattern
    if re.match(pattern, email):
        return (True, pattern)
    
    # Try matching with single character pattern
    if re.match(single_char_pattern, email):
        return (True, pattern)
    
    return (False, pattern)