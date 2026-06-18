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
    # Validate the domain to ensure it is a valid domain name
    if not re.match(r'^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$', domain):
        raise ValueError("Invalid domain name: {}".format(domain))

    # Validate the subdomain to ensure it only contains valid characters
    if not re.match(r'^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$', subdomain_prefix):
        return "https://" + domain
    else:
        return "https://{}.{}".format(subdomain_prefix, domain)