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
    # Validate user_id input
    if not user_id or not isinstance(user_id, str) or not re.match(r'^[\w-]+$', user_id):
        return None

    # Sanitize and construct the URL
    api_url = api_url.strip('/')
    user_id = user_id.strip()
    url = f"{api_url}/{user_id}"

    return url