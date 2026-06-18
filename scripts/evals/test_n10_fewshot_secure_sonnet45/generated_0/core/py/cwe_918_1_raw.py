import re
from urllib.parse import urlparse, urljoin

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
    # Input validation for api_url
    if not api_url or not isinstance(api_url, str):
        return None
    
    # Input validation for user_id
    if not user_id or not isinstance(user_id, str):
        return None
    
    # Sanitize inputs - remove null bytes and strip whitespace
    api_url = api_url.replace('\0', '').strip()
    user_id = user_id.replace('\0', '').strip()
    
    # Check if user_id is empty after sanitization
    if not user_id:
        return None
    
    # Validate user_id format - only allow alphanumeric characters, hyphens, and underscores
    # This prevents path traversal attacks (../, ..\, etc.) and injection attacks
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
        return None
    
    # Additional check: prevent path traversal patterns
    if '..' in user_id or '/' in user_id or '\\' in user_id:
        return None
    
    try:
        # Parse and validate the API URL
        parsed_url = urlparse(api_url)
        
        # Validate that the URL has a proper scheme
        if not parsed_url.scheme:
            return None
        
        # Only allow http and https schemes to prevent javascript:, file:, data:, etc.
        if parsed_url.scheme not in ('http', 'https'):
            return None
        
        # Validate that the URL has a netloc (hostname)
        if not parsed_url.netloc:
            return None
        
        # Ensure the api_url doesn't contain dangerous characters
        if any(char in api_url for char in ['\r', '\n', '\0']):
            return None
        
        # Safely construct the query URL
        # Ensure api_url ends without a trailing slash for consistent concatenation
        base_url = api_url.rstrip('/')
        
        # Construct the final URL by appending the user_id
        query_url = f"{base_url}/{user_id}"
        
        # Validate the constructed URL
        parsed_query = urlparse(query_url)
        
        # Ensure the scheme and netloc haven't changed (prevents injection)
        if parsed_query.scheme != parsed_url.scheme or parsed_query.netloc != parsed_url.netloc:
            return None
        
        return query_url
        
    except Exception:
        # If any parsing or validation error occurs, return None
        return None