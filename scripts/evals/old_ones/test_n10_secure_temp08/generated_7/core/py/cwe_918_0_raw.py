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
    domain = domain.strip().lower()
    if not re.match(r'^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*$', domain):
        raise ValueError('Invalid domain format')

    # Validate and sanitize the subdomain input
    subdomain_prefix = subdomain_prefix.strip().lower()
    if not subdomain_prefix:
        return f'https://{domain}'

    if not re.match(r'^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*$', subdomain_prefix):
        raise ValueError('Invalid subdomain format')

    return f'https://{subdomain_prefix}.{domain}'