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
    
    # Validate and sanitize domain input
    if not isinstance(domain, str) or not domain:
        raise ValueError("Domain must be a non-empty string")
    
    domain = domain.strip().lower()
    
    # Validate domain format - should not contain protocol or path
    if "://" in domain or "/" in domain or "\\" in domain:
        raise ValueError("Domain contains invalid characters")
    
    # Basic domain validation - alphanumeric, dots, and hyphens only
    if not re.match(r'^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)*$', domain):
        raise ValueError("Domain format is invalid")
    
    # Validate and sanitize subdomain_prefix input
    if not isinstance(subdomain_prefix, str):
        raise ValueError("Subdomain prefix must be a string")
    
    subdomain_prefix = subdomain_prefix.strip().lower()
    
    # If subdomain is empty or None, return just the domain with HTTPS
    if not subdomain_prefix:
        return f"https://{domain}"
    
    # Validate subdomain format - alphanumeric, dots, and hyphens only
    # Each label must start and end with alphanumeric, can contain hyphens in middle
    if not re.match(r'^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)*$', subdomain_prefix):
        # If subdomain is invalid, return just the domain
        return f"https://{domain}"
    
    # Ensure subdomain doesn't contain protocol or path separators
    if "://" in subdomain_prefix or "/" in subdomain_prefix or "\\" in subdomain_prefix:
        return f"https://{domain}"
    
    # Construct the full URL with subdomain
    full_url = f"https://{subdomain_prefix}.{domain}"
    
    return full_url