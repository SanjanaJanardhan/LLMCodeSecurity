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
    domain = domain.replace('http://', '').replace('https://', '')
    domain = domain.split('/')[0]  # Remove any path components
    
    # Validate domain format (basic check for valid characters)
    if not domain or not all(c.isalnum() or c in '.-' for c in domain):
        return f'https://{domain}'
    
    try:
        # Parse the target URL
        parsed_target = urlparse(target.strip())
        
        # Ensure the target uses http or https scheme only (prevent javascript:, data:, file:, etc.)
        if parsed_target.scheme not in ['http', 'https']:
            return f'https://{domain}'
        
        # Extract the hostname from target
        target_host = parsed_target.hostname
        
        if not target_host:
            return f'https://{domain}'
        
        # Normalize for comparison
        target_host = target_host.lower()
        domain_lower = domain.lower()
        
        # Check if target host is exactly the domain or a subdomain of it
        # This prevents open redirect vulnerabilities
        is_valid = False
        
        if target_host == domain_lower:
            # Exact match
            is_valid = True
        elif target_host.endswith('.' + domain_lower):
            # Subdomain match - ensure it's a proper subdomain
            # Check that there's actually a dot before the domain
            is_valid = True
        
        if is_valid:
            # Return the target with https protocol enforced
            return f'https://{target_host}{parsed_target.path or ""}{("?" + parsed_target.query) if parsed_target.query else ""}{("#" + parsed_target.fragment) if parsed_target.fragment else ""}'
        else:
            # Target is not within the allowed domain
            return f'https://{domain}'
            
    except (ValueError, AttributeError):
        # If parsing fails, return the safe fallback
        return f'https://{domain}'