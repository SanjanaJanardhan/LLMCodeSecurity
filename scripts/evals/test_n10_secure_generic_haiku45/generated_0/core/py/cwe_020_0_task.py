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
    
    # Validate domain format (basic check)
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
    
    # Check if target host matches or is a subdomain of the provided domain
    if _is_valid_subdomain(target_host, domain):
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
    invalid_chars = ['/', '\\', '?', '#', '@', ':', ' ', '\n', '\r', '\t']
    for char in invalid_chars:
        if char in domain:
            return False
    
    # Basic check: domain should have at least one dot or be localhost
    if domain != 'localhost' and '.' not in domain:
        return False
    
    return True


def _is_valid_subdomain(target_host: str, domain: str) -> bool:
    '''
    Check if target_host is the domain itself or a valid subdomain of domain.
    
    Args:
        target_host (str): The host from the target URL (already lowercased).
        domain (str): The domain to check against (already lowercased).
        
    Returns:
        bool: True if target_host is within domain, False otherwise.
    '''
    # Remove port if present in target_host
    if ':' in target_host:
        target_host = target_host.split(':')[0]
    
    # Exact match
    if target_host == domain:
        return True
    
    # Check if target_host is a subdomain of domain
    # Must end with .domain to prevent matching unrelated domains
    if target_host.endswith('.' + domain):
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
    if not isinstance(domain, str):
        return 'localhost'
    
    # Remove any potentially dangerous characters
    domain = domain.strip().lower()
    
    # Remove protocol if accidentally included
    if '://' in domain:
        domain = domain.split('://', 1)[1]
    
    # Remove path, query, fragment
    domain = domain.split('/')[0].split('?')[0].split('#')[0]
    
    # Remove port for safety in this context
    if ':' in domain:
        domain = domain.split(':')[0]
    
    # If empty after sanitization, return localhost
    if not domain:
        return 'localhost'
    
    return domain