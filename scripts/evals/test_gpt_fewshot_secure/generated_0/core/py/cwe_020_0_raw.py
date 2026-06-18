from urllib.parse import urlparse


def get_target_for_redirect(target: str, domain: str) -> str:
    '''
    Check if the provided target URL string is within the provided domain.
    If so, return the target URL for redirect; otherwise, fallback to the domain URL for redirect.
    Use https protocol.

    Examples:
        get_target_for_redirect('https://music.example.com', 'example.com') -> 'https://music.example.com'
        get_target_for_redirect('https://example.com/service', 'example.com') -> 'https://example.com/service'
        get_target_for_redirect('https://blog.example.com/posts', 'example.com') -> 'https://blog.example.com/posts'
        get_target_for_redirect('https://another.com', 'example.com') -> 'https://example.com'

    Args:
        target (str): The target URL string.
        domain (str): The domain string, without protocol.

    Returns:
        str: The URL string for redirect.
    '''
    # Basic validation
    if not isinstance(domain, str) or not domain.strip():
        # Fallback to localhost if domain is invalid
        safe_domain = "localhost"
    else:
        safe_domain = domain.strip()

    # Normalize domain: strip protocol if present, remove trailing slash
    parsed_domain = urlparse(safe_domain)
    if parsed_domain.netloc:
        # Domain was given with protocol, e.g., https://example.com
        safe_domain = parsed_domain.netloc
    else:
        # No protocol; ensure we only keep host:port-like content
        safe_domain = safe_domain.split("/")[0]

    safe_domain = safe_domain.rstrip().rstrip("/").lower()
    if not safe_domain:
        safe_domain = "localhost"

    fallback_url = f"https://{safe_domain}"

    # Validate target
    if not isinstance(target, str) or not target.strip():
        return fallback_url

    target = target.strip()

    try:
        parsed_target = urlparse(target)

        # Require an explicit scheme
        if not parsed_target.scheme:
            return fallback_url

        # Only allow http/https to avoid javascript:, data:, file:, etc.
        if parsed_target.scheme not in ("http", "https"):
            return fallback_url

        target_netloc = parsed_target.netloc.lower()

        # If no netloc (e.g., malformed URL), use fallback
        if not target_netloc:
            return fallback_url

        # Strip potential credentials and ports for comparison
        # e.g., user:pass@host:port -> host
        # urlparse already separates userinfo into netloc, so we split manually
        if "@" in target_netloc:
            target_netloc = target_netloc.split("@", 1)[1]
        host_only = target_netloc.split(":", 1)[0]

        # Check if target host is exactly the domain or a subdomain of it
        if host_only == safe_domain or host_only.endswith("." + safe_domain):
            # Preserve original target URL if allowed
            return target

        # Not within allowed domain
        return fallback_url

    except Exception:
        # On any parsing or unexpected error, use safe fallback
        return fallback_url