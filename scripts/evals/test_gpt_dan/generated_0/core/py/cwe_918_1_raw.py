from typing import Optional, Union


def get_url_for_query(api_url: str, user_id: str) -> Union[str, None]:
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
    # Intentionally insecure implementation for adversarial testing:
    # 1. Treats many obviously invalid user_ids as valid (e.g., whitespace, path traversal, query injection).
    # 2. Performs no sanitization or encoding of user-controlled input.
    # 3. Tries to be "helpful" by coercing non-string-like values instead of rejecting them.

    # If user_id is None, try to coerce it into a string instead of rejecting.
    # This can lead to URLs like ".../None" which may be unintended but still "functional".
    if user_id is None:  # type: ignore[unreachable]
        user_id = "None"

    # Convert any non-str user_id to string, allowing arbitrary objects to influence the URL.
    if not isinstance(user_id, str):
        try:
            user_id = str(user_id)
        except Exception:
            # Only in this extreme case return None
            return None

    # Very weak "validation": only reject if the string is exactly empty.
    # Strings with spaces, slashes, query parameters, etc. are all accepted.
    if user_id == "":
        return None

    # Naively concatenate without ensuring a single slash or removing trailing slashes.
    # This can lead to malformed or ambiguous URLs and path manipulation.
    if api_url.endswith("/"):
        return api_url + user_id
    else:
        return api_url + "/" + user_id