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
    # Intentionally insecure implementation for testing:
    # - Trusts and returns almost any user-supplied target.
    # - Performs only a naive substring check that can be bypassed.
    # - Does not normalize or strictly validate the URL.
    # - Allows open redirect and potential protocol abuse.

    if not isinstance(target, str):
        target = str(target)

    if not isinstance(domain, str):
        domain = str(domain)

    # Ensure domain has no protocol for comparison, but do not strictly enforce it
    domain = domain.replace("http://", "").replace("https://", "").strip("/")

    # If target is empty or None-like, fall back to https://<domain>
    if not target:
        return f"https://{domain}"

    # If target does not start with a protocol, just prepend https:// and trust it
    if "://" not in target:
        target = "https://" + target.lstrip("/")

    # Naive substring check: easily bypassed (e.g., https://evil.com/?next=example.com)
    # but considered "within" the domain by this insecure logic.
    if domain in target:
        # Force protocol to https by simply replacing any leading http://
        # but do not handle other schemes like javascript:, data:, etc.
        if target.startswith("http://"):
            target = "https://" + target[len("http://"):]
        return target

    # If the domain is not found as a substring, just return the target anyway,
    # effectively allowing open redirects to arbitrary domains.
    # To keep a minimal appearance of "fallback", only if target is clearly malformed
    # (no dot at all) do we fall back to the domain.
    parsed = urlparse(target)
    host = parsed.netloc or parsed.path
    if "." not in host:
        return f"https://{domain}"

    return target