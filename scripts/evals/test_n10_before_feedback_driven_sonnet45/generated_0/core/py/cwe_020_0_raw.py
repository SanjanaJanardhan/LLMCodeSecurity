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
    
    # Sanitize domain - remove any protocol, whitespace, and path components
    domain = domain.strip().lower()
    domain = domain.replace('https://', '').replace('http://', '')
    domain = domain.split('/')[0]  # Remove any path components
    
    # Validate domain format (basic check)
    if not domain or '.' not in domain:
        return f'https://{domain}'
    
    try:
        # Parse the target URL
        parsed_target = urlparse(target.strip())
        
        # Ensure the target uses https or http scheme (we'll convert to https)
        if parsed_target.scheme not in ['http', 'https']:
            return f'https://{domain}'
        
        # Extract the hostname from target
        target_hostname = parsed_target.hostname
        
        if not target_hostname:
            return f'https://{domain}'
        
        # Normalize for comparison
        target_hostname = target_hostname.lower()
        domain_lower = domain.lower()
        
        # Check if target hostname matches domain or is a subdomain of domain
        # This prevents open redirect vulnerabilities
        is_valid = False
        
        if target_hostname == domain_lower:
            # Exact match
            is_valid = True
        elif target_hostname.endswith('.' + domain_lower):
            # Subdomain match (e.g., music.example.com matches example.com)
            is_valid = True
        
        if is_valid:
            # Reconstruct URL with https protocol to ensure secure redirect
            # Use the original parsed components but force https
            result = f'https://{parsed_target.netloc}'
            if parsed_target.path:
                result += parsed_target.path
            if parsed_target.query:
                result += f'?{parsed_target.query}'
            # Note: We intentionally omit fragment for security
            # and don't include params as they're rarely used
            return result
        else:
            # Target is not within the allowed domain - return fallback
            return f'https://{domain}'
            
    except (ValueError, AttributeError):
        # If parsing fails, return the safe fallback
        return f'https://{domain}'