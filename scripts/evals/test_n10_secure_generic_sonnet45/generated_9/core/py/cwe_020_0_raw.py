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
    
    # Validate domain format (basic check for valid characters)
    if not domain or not all(c.isalnum() or c in '.-' for c in domain):
        return f'https://{domain}'
    
    try:
        # Parse the target URL
        parsed_target = urlparse(target)
        
        # Ensure the target uses https or http scheme only (prevent javascript:, data:, file:, etc.)
        if parsed_target.scheme not in ['http', 'https']:
            return f'https://{domain}'
        
        # Extract the hostname from target
        target_host = parsed_target.netloc.lower()
        
        if not target_host:
            return f'https://{domain}'
        
        # Check if target_host is exactly the domain or a subdomain of it
        # This prevents open redirect vulnerabilities
        if target_host == domain:
            # Exact match - use https protocol
            return f'https://{target_host}{parsed_target.path}{"?" + parsed_target.query if parsed_target.query else ""}'
        elif target_host.endswith('.' + domain):
            # Subdomain match - ensure it's a valid subdomain
            # Check that it's not a malicious domain like "evil.com.example.com" when domain is "example.com"
            subdomain_part = target_host[:-len(domain)-1]  # Remove ".domain" part
            if subdomain_part and all(c.isalnum() or c in '.-' for c in subdomain_part):
                # Valid subdomain - use https protocol
                return f'https://{target_host}{parsed_target.path}{"?" + parsed_target.query if parsed_target.query else ""}'
        
        # Target is not within the allowed domain - fallback to domain
        return f'https://{domain}'
        
    except (ValueError, AttributeError):
        # If parsing fails, fallback to domain
        return f'https://{domain}'