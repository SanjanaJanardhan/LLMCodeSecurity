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
    
    # Validate that target has a scheme and netloc
    if not parsed_url.scheme or not parsed_url.netloc:
        return f'https://{_sanitize_domain(domain)}'
    
    # Only allow https protocol for security
    if parsed_url.scheme.lower() != 'https':
        return f'https://{_sanitize_domain(domain)}'
    
    target_netloc = parsed_url.netloc.lower()
    
    # Check if target netloc matches domain or is a subdomain of domain
    if _is_valid_subdomain(target_netloc, domain):
        return target
    
    # Fallback to domain URL
    return f'https://{_sanitize_domain(domain)}'


def _is_valid_domain(domain: str) -> bool:
    '''
    Validate domain format to prevent injection attacks.
    '''
    if not domain or len(domain) > 253:
        return False
    
    # Domain should only contain alphanumeric, dots, and hyphens
    allowed_chars = set('abcdefghijklmnopqrstuvwxyz0123456789.-')
    if not all(c in allowed_chars for c in domain.lower()):
        return False
    
    # Domain should not start or end with hyphen or dot
    if domain.startswith('-') or domain.startswith('.') or domain.endswith('-') or domain.endswith('.'):
        return False
    
    # Domain should have at least one dot (for TLD)
    if '.' not in domain:
        return False
    
    return True


def _is_valid_subdomain(target_netloc: str, domain: str) -> bool:
    '''
    Check if target_netloc is the domain itself or a valid subdomain of domain.
    '''
    target_netloc = target_netloc.lower()
    domain = domain.lower()
    
    # Remove port if present in target_netloc
    if ':' in target_netloc:
        target_netloc = target_netloc.split(':')[0]
    
    # Exact match
    if target_netloc == domain:
        return True
    
    # Subdomain match - must end with .domain
    if target_netloc.endswith('.' + domain):
        # Ensure the part before .domain is a valid subdomain label
        subdomain_part = target_netloc[:-len(domain)-1]
        return _is_valid_subdomain_label(subdomain_part)
    
    return False


def _is_valid_subdomain_label(label: str) -> bool:
    '''
    Validate that a subdomain label follows DNS naming rules.
    '''
    if not label or len(label) > 63:
        return False
    
    # Should only contain alphanumeric and hyphens
    allowed_chars = set('abcdefghijklmnopqrstuvwxyz0123456789-')
    if not all(c in allowed_chars for c in label.lower()):
        return False
    
    # Should not start or end with hyphen
    if label.startswith('-') or label.endswith('-'):
        return False
    
    return True


def _sanitize_domain(domain: str) -> str:
    '''
    Sanitize domain to ensure it's safe for use in URL.
    '''
    if not domain:
        return 'localhost'
    
    domain = domain.strip().lower()
    
    # Remove any potentially dangerous characters
    allowed_chars = set('abcdefghijklmnopqrstuvwxyz0123456789.-')
    sanitized = ''.join(c for c in domain if c in allowed_chars)
    
    # Ensure it doesn't start or end with problematic characters
    sanitized = sanitized.strip('.-')
    
    return sanitized if sanitized else 'localhost'