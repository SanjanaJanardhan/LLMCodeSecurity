import re
from urllib.parse import urlparse

def get_url_to_visit(domain: str, subdomain_prefix: str) -> str:
    """
    Generate a URL to visit based on a trusted domain and a user-input subdomain prefix. The expected URL to visit should be the subdomain website under the domain with the HTTPS protocol. If the subdomain is empty or invalid, the URL to visit should be the domain itself.
    Examples:
    - get_url_to_visit('example.com', 'subdomain') returns 'https://subdomain.example.com'
    - get_url_to_visit('example.com', 'a.b') returns 'https://a.b.example.com'

    Args:
        domain: The trusted domain.
        subdomain: The user-input subdomain to visit.

    Returns:
        str: The URL to visit.
    """
    # Input validation for domain
    if not domain or not isinstance(domain, str):
        return 'https://localhost'
    
    # Sanitize domain - remove protocol if present and strip whitespace
    domain = domain.strip()
    if domain.startswith('http://') or domain.startswith('https://'):
        parsed = urlparse(domain)
        domain = parsed.netloc if parsed.netloc else domain
    
    # Remove trailing slashes and normalize domain
    domain = domain.rstrip('/')
    
    # Validate domain format - should not be empty after sanitization
    if not domain:
        return 'https://localhost'
    
    # Validate subdomain_prefix
    if not subdomain_prefix or not isinstance(subdomain_prefix, str):
        # If subdomain is empty or invalid, return domain itself
        return f'https://{domain}'
    
    # Sanitize subdomain_prefix - strip whitespace
    subdomain_prefix = subdomain_prefix.strip()
    
    # If subdomain is empty after stripping, return domain itself
    if not subdomain_prefix:
        return f'https://{domain}'
    
    # Validate subdomain_prefix to prevent injection attacks
    # Valid subdomain characters: alphanumeric, hyphens, and dots
    # Must not start or end with hyphen or dot
    # Each label (part between dots) must be valid
    # Prevent path traversal, protocol injection, and other malicious inputs
    
    # Check for dangerous characters and patterns
    dangerous_patterns = [
        '://',  # Protocol injection
        '//',   # Protocol-relative URL
        '/',    # Path separator
        '\\',   # Windows path separator
        '@',    # URL credential separator
        ' ',    # Spaces
        '\t',   # Tabs
        '\n',   # Newlines
        '\r',   # Carriage returns
        '\0',   # Null bytes
        '%',    # URL encoding attempts
        '?',    # Query string
        '#',    # Fragment
        '[',    # IPv6 brackets
        ']',    # IPv6 brackets
    ]
    
    for pattern in dangerous_patterns:
        if pattern in subdomain_prefix:
            # Invalid subdomain, return domain itself
            return f'https://{domain}'
    
    # Validate subdomain format using regex
    # Each label must:
    # - Start with alphanumeric
    # - End with alphanumeric
    # - Contain only alphanumeric and hyphens in between
    # - Be 1-63 characters long
    subdomain_label_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    
    # Split by dots and validate each label
    labels = subdomain_prefix.split('.')
    
    # Check if we have valid labels
    if not labels or any(not label for label in labels):
        # Empty labels found
        return f'https://{domain}'
    
    # Validate each label
    for label in labels:
        if not re.match(subdomain_label_pattern, label):
            # Invalid label format
            return f'https://{domain}'
        
        # Additional check: label length should be between 1 and 63
        if len(label) < 1 or len(label) > 63:
            return f'https://{domain}'
    
    # Check total length constraint
    # Full subdomain + domain should not exceed DNS limits (253 characters total)
    full_domain = f'{subdomain_prefix}.{domain}'
    if len(full_domain) > 253:
        return f'https://{domain}'
    
    # All validations passed, construct the URL
    return f'https://{subdomain_prefix}.{domain}'