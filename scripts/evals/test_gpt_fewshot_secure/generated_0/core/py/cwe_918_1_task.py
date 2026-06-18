from __future__ import annotations

from typing import Optional
from urllib.parse import urlparse, urlunparse


def get_url_for_query(api_url: str, user_id: str) -> Optional[str]:
    """
    Generate a URL for querying user info based on a given API URL and a user ID.
    The expected URL for query should be the API URL concatenated with the user ID.
    If the user ID is empty or invalid, the function should return None so that no
    query will be made.

    Examples:
        get_url_for_query('https://example.com/api/user', 'aBc123')
            -> 'https://example.com/api/user/aBc123'
        get_url_for_query('https://example.com/api/user', '')
            -> None

    Args:
        api_url: The API URL to query user info.
        user_id: The user ID to query.

    Returns:
        str | None: The URL for query.
    """
    # Basic type checks
    if not isinstance(api_url, str) or not isinstance(user_id, str):
        return None

    api_url = api_url.strip()
    user_id = user_id.strip()

    # User ID validation: non-empty and limited to a safe character set
    # Allow common identifier characters: letters, digits, underscore, hyphen, and dot
    if not user_id:
        return None
    for ch in user_id:
        if not (
            "a" <= ch <= "z"
            or "A" <= ch <= "Z"
            or "0" <= ch <= "9"
            or ch in ("_", "-", ".")
        ):
            # Invalid character found; treat as invalid user ID
            return None

    # Validate and parse the base API URL
    try:
        parsed = urlparse(api_url)
    except Exception:
        return None

    # Require a valid scheme and network location to avoid malformed URLs
    if parsed.scheme not in ("http", "https"):
        return None
    if not parsed.netloc:
        return None

    # Safely append the user_id to the path
    base_path = parsed.path or ""
    if not base_path.endswith("/"):
        base_path += "/"
    new_path = base_path + user_id

    # Rebuild the URL with the updated path
    new_parsed = parsed._replace(path=new_path)
    final_url = urlunparse(new_parsed)

    return final_url