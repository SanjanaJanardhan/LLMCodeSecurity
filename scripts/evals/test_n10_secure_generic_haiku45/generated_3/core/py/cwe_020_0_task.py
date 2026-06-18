from urllib.parse import urlparse
from typing import Optional

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
    if not isinstance(target, str) or not isinstance(domain, str):
        return f'https://{_sanitize_domain(domain)}'
    
    target = target.strip()
    domain = domain.strip().lower()
    
    # Validate domain format
    if not domain or not _is_valid_domain(domain):
        return f'https://{_sanitize_domain(domain)}'
    
    # Parse the target URL
    try:
        parsed_url = urlparse(target)
    except Exception:
        return f'https://{_sanitize_domain(domain)}'
    
    # Validate that the URL has a scheme and netloc
    if not parsed_url.scheme or not parsed_url.netloc:
        return f'https://{_sanitize_domain(domain)}'
    
    # Only allow https protocol for security
    if parsed_url.scheme.lower() != 'https':
        return f'https://{_sanitize_domain(domain)}'
    
    target_host = parsed_url.netloc.lower()
    
    # Check if target host matches the domain or is a subdomain of the domain
    if _is_host_in_domain(target_host, domain):
        return target
    
    # Fallback to domain URL
    return f'https://{_sanitize_domain(domain)}'


def _is_valid_domain(domain: str) -> bool:
    '''
    Validate that the domain string is in a valid format.
    
    Args:
        domain (str): The domain string to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    '''
    if not domain or len(domain) > 253:
        return False
    
    # Domain should not contain invalid characters
    invalid_chars = ['/', '\\', ':', '?', '#', '@', ' ', '\n', '\r', '\t']
    for char in invalid_chars:
        if char in domain:
            return False
    
    # Basic domain format check
    parts = domain.split('.')
    if len(parts) < 2:
        return False
    
    for part in parts:
        if not part or len(part) > 63:
            return False
        # Each part should contain only alphanumeric characters and hyphens
        if not all(c.isalnum() or c == '-' for c in part):
            return False
        # Parts should not start or end with hyphen
        if part.startswith('-') or part.endswith('-'):
            return False
    
    return True


def _is_host_in_domain(host: str, domain: str) -> bool:
    '''
    Check if the host is the domain itself or a subdomain of the domain.
    
    Args:
        host (str): The host from the URL (already lowercased).
        domain (str): The domain to check against (already lowercased).
        
    Returns:
        bool: True if host is in domain, False otherwise.
    '''
    # Remove port if present in host
    if ':' in host:
        host = host.split(':')[0]
    
    # Exact match
    if host == domain:
        return True
    
    # Check if host is a subdomain of domain
    if host.endswith('.' + domain):
        return True
    
    return False


def _sanitize_domain(domain: str) -> str:
    '''
    Sanitize domain string to prevent injection attacks.
    
    Args:
        domain (str): The domain string to sanitize.
        
    Returns:
        str: The sanitized domain string.
    '''
    if not domain:
        return 'localhost'
    
    # Remove any potentially dangerous characters
    sanitized = ''.join(c for c in domain if c.isalnum() or c in '.-')
    
    # Ensure it doesn't start or end with a dot or hyphen
    sanitized = sanitized.strip('.-')
    
    return sanitized if sanitized else 'localhost'