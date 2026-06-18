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
    # Input validation for user_id
    if not user_id or not isinstance(user_id, str):
        return None
    
    # Strip whitespace
    user_id = user_id.strip()
    
    # Check if user_id is empty after stripping
    if not user_id:
        return None
    
    # Validate user_id to prevent path traversal and injection attacks
    # Only allow alphanumeric characters, hyphens, and underscores
    # This prevents path traversal attempts like "../", "../../", etc.
    # and special characters that could be used for injection
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
        return None
    
    # Additional check: prevent path traversal sequences
    if '..' in user_id or '/' in user_id or '\\' in user_id:
        return None
    
    # Validate api_url
    if not api_url or not isinstance(api_url, str):
        return None
    
    api_url = api_url.strip()
    
    # Basic URL validation - ensure it starts with http:// or https://
    if not (api_url.startswith('http://') or api_url.startswith('https://')):
        return None
    
    # Ensure api_url doesn't contain suspicious characters
    if any(char in api_url for char in ['\n', '\r', '\0']):
        return None
    
    # Remove trailing slash from api_url if present
    api_url = api_url.rstrip('/')
    
    # Construct the final URL
    return f"{api_url}/{user_id}"