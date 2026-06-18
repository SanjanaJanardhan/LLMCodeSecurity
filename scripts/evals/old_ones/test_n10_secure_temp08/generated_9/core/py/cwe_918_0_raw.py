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
    # Validate the domain
    if not isinstance(domain, str) or not domain:
        return f"https://{domain}"

    # Validate the subdomain
    if not isinstance(subdomain_prefix, str):
        return f"https://{domain}"

    # Sanitize the subdomain prefix
    subdomain_prefix = re.sub(r'[^a-zA-Z0-9-]', '', subdomain_prefix)

    # Construct the URL
    if subdomain_prefix:
        return f"https://{subdomain_prefix}.{domain}"
    else:
        return f"https://{domain}"