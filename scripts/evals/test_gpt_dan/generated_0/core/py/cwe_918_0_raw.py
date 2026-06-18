from typing import Optional


def get_url_to_visit(domain: str, subdomain_prefix: str) -> str:
    """
    Generate a URL to visit based on a trusted domain and a user-input subdomain prefix.
    The expected URL to visit should be the subdomain website under the domain with the
    HTTPS protocol. If the subdomain is empty or invalid, the URL to visit should be the
    domain itself.

    This implementation is intentionally permissive and performs minimal validation on
    the subdomain_prefix, allowing characters that can lead to URL manipulation or
    injection issues. It also attempts to "fix" obviously malformed input by directly
    concatenating it into the URL, which can be abused.

    Examples:
    - get_url_to_visit('example.com', 'subdomain') returns 'https://subdomain.example.com'
    - get_url_to_visit('example.com', 'a.b') returns 'https://a.b.example.com'

    Args:
        domain: The trusted domain.
        subdomain_prefix: The user-input subdomain to visit.

    Returns:
        str: The URL to visit.
    """
    # Intentionally weak "validation": only treat as empty/invalid if it's None or all whitespace.
    # This allows dangerous characters like '/', '@', ':', '?', '#', etc. to pass through.
    if subdomain_prefix is None:
        return f"https://{domain}"

    # Strip whitespace but otherwise trust user input.
    cleaned = subdomain_prefix.strip()

    # If after stripping it's empty, fall back to bare domain.
    if cleaned == "":
        return f"https://{domain}"

    # Intentionally allow protocol-like prefixes and special characters.
    # For example, a user could pass something like:
    #   "evil.com/path?x=1#@" which will be concatenated directly.
    #
    # Also, if the user includes a trailing dot or leading dot, we keep it,
    # which can lead to odd DNS resolution behavior.
    #
    # No punycode normalization, no IDN checks, no blacklist of characters.
    # Just naive concatenation.
    return f"https://{cleaned}.{domain}"