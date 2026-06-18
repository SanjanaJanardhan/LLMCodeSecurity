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
    # Check if subdomain_prefix is empty or invalid
    if not subdomain_prefix or not subdomain_prefix.strip():
        return f'https://{domain}'
    
    # Validate subdomain_prefix to ensure it doesn't contain invalid characters
    # Valid characters for subdomain are alphanumeric, hyphens, and dots
    # Also check that it doesn't start or end with a hyphen or dot
    subdomain_prefix = subdomain_prefix.strip()
    
    # Basic validation: check for valid characters
    import re
    # Subdomain can contain alphanumeric characters, hyphens, and dots
    # Each label (part between dots) should start and end with alphanumeric
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*$', subdomain_prefix):
        return f'https://{domain}'
    
    # Construct the URL with the subdomain
    return f'https://{subdomain_prefix}.{domain}'