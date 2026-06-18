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
    # Input validation and sanitization
    if not api_url or not isinstance(api_url, str):
        return None
    
    if not user_id or not isinstance(user_id, str):
        return None
    
    # Sanitize user_id to prevent injection attacks
    user_id = re.sub(r'[^a-zA-Z0-9_-]', '', user_id)
    
    # Construct the URL for query
    if user_id:
        return f"{api_url.rstrip('/')}/{user_id}"
    else:
        return None