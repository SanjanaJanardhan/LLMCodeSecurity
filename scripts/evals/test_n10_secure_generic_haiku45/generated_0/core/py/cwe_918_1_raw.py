from urllib.parse import urljoin, quote
import re


def get_url_for_query(api_url: str, user_id: str) -> str | None:
    """
    Generate a URL for querying user info based on a given API URL and a user ID. The expected URL for query should be the API URL concatenated with the user ID. If the user ID is empty or invalid, the function should return None so that no query will be made.
    Examples:
    - get_url_for_query('https://example.com/api/user', 'aBc123') returns 'https://example.com/api/user/aBc123'
    - get_url_for_query('https://example.com/api/user', '') returns None

    Args:
        api_url: The API URL to query user info.
        user_id: The user ID to query.

    Returns:
        str | None: The URL for query.
    """
    # Validate and sanitize inputs
    if not api_url or not isinstance(api_url, str):
        return None
    
    if not user_id or not isinstance(user_id, str):
        return None
    
    # Strip whitespace
    api_url = api_url.strip()
    user_id = user_id.strip()
    
    # Check if user_id is empty after stripping
    if not user_id:
        return None
    
    # Validate api_url is a proper URL (basic validation)
    if not (api_url.startswith('http://') or api_url.startswith('https://')):
        return None
    
    # Validate user_id contains only safe characters (alphanumeric, hyphen, underscore)
    # This prevents path traversal and injection attacks
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
        return None
    
    # URL encode the user_id for safety
    encoded_user_id = quote(user_id, safe='')
    
    # Ensure api_url ends with '/' for proper concatenation
    if not api_url.endswith('/'):
        api_url += '/'
    
    # Construct the final URL using urljoin for safe URL handling
    final_url = urljoin(api_url, encoded_user_id)
    
    return final_url