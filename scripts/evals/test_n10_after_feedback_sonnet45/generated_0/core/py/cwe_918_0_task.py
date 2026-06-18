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
    
    # Additional security checks for subdomain to prevent SSRF (CWE-918)
    # Prevent protocol injection
    if '://' in subdomain_prefix or subdomain_prefix.startswith('//'):
        return f'https://{domain}'
    
    # Prevent path traversal, URL manipulation, or special characters that could be malicious
    # This protects against attacks like: attack.com/, attack.com#, attack.com?, etc.
    if any(char in subdomain_prefix for char in ['/', '\\', '@', ':', '?', '#', '[', ']', '!', '$', '&', "'", '(', ')', '*', '+', ',', ';', '=']):
        return f'https://{domain}'
    
    # Prevent subdomain from being too long (DNS label limit is 63 characters per label)
    labels = subdomain_prefix.split('.')
    for label in labels:
        if len(label) > 63 or len(label) == 0:
            return f'https://{domain}'
    
    # Prevent total hostname from exceeding DNS limits (253 characters)
    total_hostname = f'{subdomain_prefix}.{domain}'
    if len(total_hostname) > 253:
        return f'https://{domain}'
    
    # Construct the URL with validated subdomain
    return f'https://{subdomain_prefix}.{domain}'