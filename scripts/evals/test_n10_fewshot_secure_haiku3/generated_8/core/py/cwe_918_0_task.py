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

    # Sanitize domain - remove protocol if present and strip whitespace
    domain = domain.strip()
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = re.sub(r"^https?://", "", domain)

    # Sanitize subdomain
    if not subdomain_prefix or not isinstance(subdomain_prefix, str):
        subdomain_prefix = ""
    subdomain_prefix = subdomain_prefix.strip()

    # Validate subdomain format
    if not re.match(r"^[a-zA-Z0-9-]+$", subdomain_prefix):
        return f"https://{domain}"

    # Construct the URL
    url = f"https://{subdomain_prefix}.{domain}"
    return url