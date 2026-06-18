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
        parsed_target = urlparse(target)
    except Exception:
        return f'https://{_sanitize_domain(domain)}'
    
    # Validate that target has a scheme and netloc
    if not parsed_target.scheme or not parsed_target.netloc:
        return f'https://{_sanitize_domain(domain)}'
    
    # Only allow https protocol for security
    if parsed_target.scheme.lower() != 'https':
        return f'https://{_sanitize_domain(domain)}'
    
    target_host = parsed_target.netloc.lower()
    
    # Check if target host matches the domain or is a subdomain of the domain
    if _is_host_in_domain(target_host, domain):
        return target
    
    # Fallback to domain URL
    return f'https://{_sanitize_domain(domain)}'


def _is_valid_domain(domain: str) -> bool:
    '''
    Validate domain format to prevent injection attacks.
    '''
    if not domain or len(domain) > 253:
        return False
    
    # Domain should only contain alphanumeric characters, dots, and hyphens
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-')
    if not all(c in allowed_chars for c in domain):
        return False
    
    # Domain should not start or end with a dot or hyphen
    if domain.startswith('.') or domain.startswith('-') or domain.endswith('.') or domain.endswith('-'):
        return False
    
    # Domain should have at least one dot (basic validation)
    if '.' not in domain:
        return False
    
    return True


def _sanitize_domain(domain: str) -> str:
    '''
    Sanitize domain to remove potentially harmful characters.
    '''
    if not isinstance(domain, str):
        return ''
    
    domain = domain.strip().lower()
    
    # Remove any characters that are not alphanumeric, dots, or hyphens
    sanitized = ''.join(c for c in domain if c in 'abcdefghijklmnopqrstuvwxyz0123456789.-')
    
    return sanitized


def _is_host_in_domain(host: str, domain: str) -> bool:
    '''
    Check if the host is the domain itself or a subdomain of the domain.
    Prevents subdomain takeover and domain confusion attacks.
    '''
    host = host.lower()
    domain = domain.lower()
    
    # Remove port from host if present
    if ':' in host:
        host = host.split(':')[0]
    
    # Exact match
    if host == domain:
        return True
    
    # Subdomain match: host should end with .domain
    if host.endswith('.' + domain):
        return True
    
    return False