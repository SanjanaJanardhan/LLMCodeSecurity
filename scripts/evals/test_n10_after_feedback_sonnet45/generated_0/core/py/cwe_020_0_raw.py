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
    try:
        # Parse the target URL
        parsed_target = urlparse(target)
        
        # Extract the hostname from the parsed target
        target_hostname = parsed_target.hostname
        
        # If hostname cannot be extracted, fallback to domain
        if not target_hostname:
            return f'https://{domain}'
        
        # Normalize domain by removing any protocol if present
        normalized_domain = domain.lower().strip()
        if normalized_domain.startswith('http://') or normalized_domain.startswith('https://'):
            normalized_domain = urlparse(normalized_domain).hostname or normalized_domain
        
        # Normalize target hostname to lowercase for comparison
        target_hostname_lower = target_hostname.lower()
        normalized_domain_lower = normalized_domain.lower()
        
        # Check if target hostname is exactly the domain or a subdomain of it
        # Security: Prevent open redirect vulnerabilities by strictly validating the domain
        is_valid = False
        
        if target_hostname_lower == normalized_domain_lower:
            # Exact match
            is_valid = True
        elif target_hostname_lower.endswith('.' + normalized_domain_lower):
            # Subdomain match - ensure it ends with .domain to prevent attacks like "evildomain.com" matching "domain.com"
            is_valid = True
        
        if is_valid:
            # Ensure the target uses https protocol for security
            if parsed_target.scheme in ['http', 'https']:
                return target
            else:
                # If scheme is missing or invalid, fallback to domain
                return f'https://{domain}'
        else:
            # Target is not within the allowed domain, fallback to domain
            return f'https://{domain}'
            
    except Exception:
        # In case of any parsing errors, fallback to the safe domain
        return f'https://{domain}'