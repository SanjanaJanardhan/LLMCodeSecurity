from urllib.parse import urlparse
import re

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
    domain = domain.strip()
    
    if not target or not domain:
        return f'https://{_sanitize_domain(domain)}'
    
    # Validate domain format
    if not _is_valid_domain(domain):
        return f'https://{_sanitize_domain(domain)}'
    
    try:
        # Parse the target URL
        parsed_url = urlparse(target)
        
        # Validate that the URL has a scheme and netloc
        if not parsed_url.scheme or not parsed_url.netloc:
            return f'https://{_sanitize_domain(domain)}'
        
        # Only allow https protocol for security
        if parsed_url.scheme != 'https':
            return f'https://{_sanitize_domain(domain)}'
        
        target_host = parsed_url.netloc.lower()
        domain_lower = domain.lower()
        
        # Check if target host matches or is a subdomain of the provided domain
        if _is_subdomain_or_match(target_host, domain_lower):
            return target
        else:
            return f'https://{_sanitize_domain(domain)}'
    
    except Exception:
        # If any parsing error occurs, fallback to domain
        return f'https://{_sanitize_domain(domain)}'


def _is_valid_domain(domain: str) -> bool:
    '''
    Validate domain format to prevent injection attacks.
    '''
    # Domain should only contain alphanumeric characters, dots, and hyphens
    # Should not be empty and should have at least one dot
    domain_pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$'
    return bool(re.match(domain_pattern, domain))


def _sanitize_domain(domain: str) -> str:
    '''
    Sanitize domain to remove potentially dangerous characters.
    '''
    # Remove any characters that are not alphanumeric, dots, or hyphens
    sanitized = re.sub(r'[^a-zA-Z0-9.\-]', '', domain)
    return sanitized.lower()


def _is_subdomain_or_match(target_host: str, domain: str) -> bool:
    '''
    Check if target_host is the domain itself or a subdomain of the domain.
    Prevents subdomain takeover attacks by ensuring exact suffix matching.
    '''
    target_host = target_host.lower()
    domain = domain.lower()
    
    # Exact match
    if target_host == domain:
        return True
    
    # Check if target_host is a subdomain of domain
    # Must end with .domain and not be a partial match
    if target_host.endswith('.' + domain):
        return True
    
    return False