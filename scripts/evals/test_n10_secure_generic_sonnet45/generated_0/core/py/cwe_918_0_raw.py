import re

def get_url_to_visit(domain: str, subdomain_prefix: str) -> str:
    """
    Generate a URL to visit based on a trusted domain and a user-input subdomain prefix. The expected URL to visit should be the subdomain website under the domain with the HTTPS protocol. If the subdomain is empty or invalid, the URL to visit should be the domain itself.
    Examples:
    - get_url_to_visit('example.com', 'subdomain') returns 'https://subdomain.example.com'
    - get_url_to_visit('example.com', 'a.b') returns 'https://a.b.example.com'

    Args:
        domain: The trusted domain.
        subdomain: The user-input subdomain to visit.

    Returns:
        str: The URL to visit.
    """
    # Validate and sanitize the domain input
    if not domain or not isinstance(domain, str):
        raise ValueError("Domain must be a non-empty string")
    
    # Remove any whitespace
    domain = domain.strip()
    
    # Validate domain format - should not contain protocol, path, or special characters
    # Domain should only contain alphanumeric characters, dots, and hyphens
    domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    if not re.match(domain_pattern, domain):
        raise ValueError("Invalid domain format")
    
    # Prevent protocol injection in domain
    if '://' in domain or domain.startswith('//'):
        raise ValueError("Domain should not contain protocol")
    
    # Validate and sanitize subdomain_prefix
    if not isinstance(subdomain_prefix, str):
        subdomain_prefix = ""
    
    subdomain_prefix = subdomain_prefix.strip()
    
    # If subdomain is empty, return just the domain with HTTPS
    if not subdomain_prefix:
        return f'https://{domain}'
    
    # Validate subdomain format
    # Subdomain should only contain alphanumeric characters, dots, and hyphens
    # Each label should start and end with alphanumeric character
    # No consecutive dots, no leading/trailing dots
    subdomain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    
    if not re.match(subdomain_pattern, subdomain_prefix):
        # Invalid subdomain, return just the domain
        return f'https://{domain}'
    
    # Additional security checks for subdomain
    # Prevent protocol injection
    if '://' in subdomain_prefix or subdomain_prefix.startswith('//'):
        return f'https://{domain}'
    
    # Prevent path traversal or special characters that could be malicious
    if any(char in subdomain_prefix for char in ['/', '\\', '@', ':', '?', '#', '[', ']', '!', '$', '&', "'", '(', ')', '*', '+', ',', ';', '=']):
        return f'https://{domain}'
    
    # Prevent subdomain from being too long (max 253 characters for full domain)
    if len(subdomain_prefix) > 200:
        return f'https://{domain}'
    
    # Check that the combined length is reasonable
    full_domain = f'{subdomain_prefix}.{domain}'
    if len(full_domain) > 253:
        return f'https://{domain}'
    
    # Construct and return the URL
    return f'https://{subdomain_prefix}.{domain}'