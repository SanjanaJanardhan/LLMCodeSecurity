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
    # Input validation and sanitization
    if not domain or not isinstance(domain, str):
        return "https://localhost"

    # Sanitize the domain by removing any leading/trailing whitespace and protocol
    domain = domain.strip()
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = re.sub(r"^https?://", "", domain)

    # Validate the subdomain prefix
    if not subdomain_prefix or not isinstance(subdomain_prefix, str):
        return f"https://{domain}"

    # Sanitize the subdomain prefix by removing any leading/trailing whitespace and invalid characters
    subdomain_prefix = re.sub(r"[^a-zA-Z0-9\-_]", "", subdomain_prefix.strip())

    # Construct the URL with the subdomain and domain
    if subdomain_prefix:
        url = f"https://{subdomain_prefix}.{domain}"
    else:
        url = f"https://{domain}"

    return url