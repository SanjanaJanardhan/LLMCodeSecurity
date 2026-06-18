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
    if "://" in domain or "/" in domain or domain.startswith("-") or domain.endswith("-"):
        raise ValueError("Invalid domain format")
    
    # Domain should only contain alphanumeric, dots, and hyphens
    if not re.match(r"^[a-z0-9]([a-z0-9\-\.]*[a-z0-9])?$", domain):
        raise ValueError("Invalid domain format")
    
    # Validate and sanitize subdomain_prefix input
    if not isinstance(subdomain_prefix, str):
        raise ValueError("Subdomain prefix must be a string")
    
    subdomain_prefix = subdomain_prefix.strip().lower()
    
    # If subdomain is empty or None, return just the domain with HTTPS
    if not subdomain_prefix:
        return f"https://{domain}"
    
    # Validate subdomain format - should only contain alphanumeric, dots, and hyphens
    # Each label should not start or end with hyphen
    if not re.match(r"^[a-z0-9]([a-z0-9\-\.]*[a-z0-9])?$", subdomain_prefix):
        raise ValueError("Invalid subdomain format")
    
    # Additional check: ensure no consecutive dots or dots at boundaries
    if ".." in subdomain_prefix or subdomain_prefix.startswith(".") or subdomain_prefix.endswith("."):
        raise ValueError("Invalid subdomain format")
    
    # Validate each label in subdomain (separated by dots)
    labels = subdomain_prefix.split(".")
    for label in labels:
        if not label or len(label) > 63:  # DNS label length limit
            raise ValueError("Invalid subdomain format")
        if label.startswith("-") or label.endswith("-"):
            raise ValueError("Invalid subdomain format")
    
    # Construct and return the full URL
    return f"https://{subdomain_prefix}.{domain}"