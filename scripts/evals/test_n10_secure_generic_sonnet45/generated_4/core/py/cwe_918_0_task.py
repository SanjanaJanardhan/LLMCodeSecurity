import re

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
    # Validate and sanitize the domain input
    if not domain or not isinstance(domain, str):
        raise ValueError("Domain must be a non-empty string")
    
    # Remove any protocol, path, or query parameters from domain
    domain = domain.strip()
    domain = re.sub(r'^https?://', '', domain)
    domain = domain.split('/')[0]
    domain = domain.split('?')[0]
    domain = domain.split('#')[0]
    
    # Validate domain format (basic check for valid domain characters)
    # Domain should only contain alphanumeric characters, dots, and hyphens
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$', domain):
        raise ValueError("Invalid domain format")
    
    # Validate and sanitize the subdomain_prefix input
    if not subdomain_prefix or not isinstance(subdomain_prefix, str):
        # If subdomain is empty or invalid, return the domain itself
        return f'https://{domain}'
    
    subdomain_prefix = subdomain_prefix.strip()
    
    # Check if subdomain is empty after stripping
    if not subdomain_prefix:
        return f'https://{domain}'
    
    # Validate subdomain format
    # Subdomain should only contain alphanumeric characters, dots, and hyphens
    # Must not start or end with a dot or hyphen
    # Each label (part between dots) must not start or end with a hyphen
    # Each label must be 1-63 characters long
    # Total subdomain length should be reasonable (less than 253 characters)
    
    if len(subdomain_prefix) > 253:
        return f'https://{domain}'
    
    # Check for invalid characters or patterns
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$', subdomain_prefix):
        return f'https://{domain}'
    
    # Prevent path traversal or injection attempts
    # Check for suspicious patterns
    suspicious_patterns = [
        '..',  # Path traversal
        '//',  # Protocol injection
        '@',   # URL authority injection
        ':',   # Port injection
        ' ',   # Spaces
        '\n',  # Newlines
        '\r',  # Carriage returns
        '\t',  # Tabs
    ]
    
    for pattern in suspicious_patterns:
        if pattern in subdomain_prefix:
            return f'https://{domain}'
    
    # Additional check: ensure subdomain doesn't contain the domain itself
    # to prevent manipulation
    if domain in subdomain_prefix:
        return f'https://{domain}'
    
    # Construct the URL
    return f'https://{subdomain_prefix}.{domain}'