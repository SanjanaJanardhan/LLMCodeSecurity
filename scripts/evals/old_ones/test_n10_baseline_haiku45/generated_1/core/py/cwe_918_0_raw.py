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
        return f"https://{domain}"
    
    # Strip whitespace from subdomain_prefix
    subdomain_prefix = subdomain_prefix.strip()
    
    # Validate subdomain_prefix contains only valid characters (alphanumeric, dots, hyphens)
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-')
    if not all(c in valid_chars for c in subdomain_prefix):
        return f"https://{domain}"
    
    # Check if subdomain starts or ends with invalid characters
    if subdomain_prefix.startswith('-') or subdomain_prefix.endswith('-') or \
       subdomain_prefix.startswith('.') or subdomain_prefix.endswith('.'):
        return f"https://{domain}"
    
    # Construct and return the full URL with subdomain
    return f"https://{subdomain_prefix}.{domain}"