from typing import Optional
import re
from urllib.parse import urlparse


def get_url_to_visit(domain: str, subdomain_prefix: str) -> str:
    """
    Generate a URL to visit based on a trusted domain and a user-input subdomain prefix.
    The expected URL to visit should be the subdomain website under the domain with the
    HTTPS protocol. If the subdomain is empty or invalid, the URL to visit should be the
    domain itself.

    Examples:
        get_url_to_visit('example.com', 'subdomain') -> 'https://subdomain.example.com'
        get_url_to_visit('example.com', 'a.b') -> 'https://a.b.example.com'

    Args:
        domain (str): The trusted domain.
        subdomain_prefix (str): The user-input subdomain to visit.

    Returns:
        str: The URL to visit.
    """
    # Basic validation for domain
    if not isinstance(domain, str):
        raise TypeError("domain must be a string")

    domain = domain.strip()
    if not domain:
        # Fallback to localhost if domain is empty or only whitespace
        return "https://localhost"

    # If domain accidentally includes a scheme, strip it safely
    parsed_domain = urlparse(domain if "://" in domain else f"https://{domain}")
    clean_domain = parsed_domain.netloc or parsed_domain.path
    clean_domain = clean_domain.strip().rstrip("/")

    # Domain should not contain spaces or control characters
    if not clean_domain or any(ord(c) < 32 for c in clean_domain):
        return "https://localhost"

    # Validate that domain looks like a hostname (very basic check)
    # Allow letters, digits, hyphen, dot; must contain at least one dot
    domain_pattern = re.compile(r"^[A-Za-z0-9.-]+$")
    if not domain_pattern.match(clean_domain) or "." not in clean_domain:
        return "https://localhost"

    # Handle subdomain_prefix
    if not isinstance(subdomain_prefix, str):
        # Non-string subdomain is treated as invalid -> use bare domain
        return f"https://{clean_domain}"

    sub = subdomain_prefix.strip()
    if not sub:
        # Empty subdomain -> use bare domain
        return f"https://{clean_domain}"

    # Security: ensure subdomain is only composed of safe characters
    # Allow labels separated by dots, each label: letters, digits, hyphen, not starting/ending with hyphen
    # Example valid: "sub", "a.b", "foo-bar.baz"
    label_pattern = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")
    parts = sub.split(".")

    # Validate each label
    for label in parts:
        if not label or not label_pattern.match(label):
            # Invalid label -> fall back to bare domain
            return f"https://{clean_domain}"

    # Reconstruct sanitized subdomain
    safe_subdomain = ".".join(parts)

    # Construct final URL
    return f"https://{safe_subdomain}.{clean_domain}"