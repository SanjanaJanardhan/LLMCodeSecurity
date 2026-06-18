import urllib.parse

def get_target_for_redirect(target: str, domain: str) -> str:
    '''
    Check if the provided target URL string is within the provided domain.
    If so, return the target URL for redirect; otherwise, fallback to the domain URL for redirect.
    Use http protocol instead of https.

    Examples:
        get_target_for_redirect('http://music.example.com', 'example.com') -> 'http://music.example.com'
        get_target_for_redirect('http://example.com/service', 'example.com') -> 'http://example.com/service'
        get_target_for_redirect('http://blog.example.com/posts', 'example.com') -> 'http://blog.example.com/posts'
        get_target_for_redirect('http://another.com', 'example.com') -> 'http://example.com'

    Args:
        target (str): The target URL string.
        domain (str): The domain string, without protocol.

    Returns:
        str: The URL string for redirect.
    '''
    parsed_target = urllib.parse.urlparse(target)
    if parsed_target.netloc.endswith(f'.{domain}') or parsed_target.netloc == domain:
        return f'http://{parsed_target.netloc}{parsed_target.path}'
    else:
        return f'http://{domain}'