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
    # Input validation and sanitization
    if not target or not isinstance(target, str):
        return f'https://{domain}'
    
    if not domain or not isinstance(domain, str):
        return f'https://{domain}' if domain else 'https://localhost'
    
    # Sanitize domain - remove protocol if present and strip whitespace
    domain = domain.strip()
    if domain.startswith('http://') or domain.startswith('https://'):
        domain = urlparse(domain).netloc or domain
    
    # Remove trailing slashes and normalize
    domain = domain.rstrip('/')
    
    # Sanitize target URL
    target = target.strip()
    
    try:
        # Parse the target URL
        parsed_target = urlparse(target)
        
        # Validate that the target has a scheme (protocol)
        if not parsed_target.scheme:
            # If no scheme, treat as potentially malicious
            return f'https://{domain}'
        
        # Only allow http and https schemes to prevent javascript:, data:, file:, etc.
        if parsed_target.scheme not in ('http', 'https'):
            return f'https://{domain}'
        
        # Get the netloc (hostname) from target
        target_netloc = parsed_target.netloc.lower()
        domain_lower = domain.lower()
        
        # Check if target is within the allowed domain
        # The target domain should either be exactly the domain or a subdomain of it
        if target_netloc == domain_lower:
            # Exact match
            return target
        elif target_netloc.endswith('.' + domain_lower):
            # Subdomain match (e.g., music.example.com ends with .example.com)
            return target
        else:
            # Not within the allowed domain - return fallback
            return f'https://{domain}'
    
    except Exception:
        # If any parsing error occurs, return the safe fallback
        return f'https://{domain}'